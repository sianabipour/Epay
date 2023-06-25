from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from zeep import Client
from master.models import Factor,Setting
from khayyam import *
from master.models import Key,Profile,KavenegarSetting
from .sms import sms_by_template
from random import randint
from datetime import timedelta, date
from background_task import background
from background_task.models import Task

def check_keys():
    today = date.today()
    keys = Key.objects.exclude(date__gte = today - timedelta(days=7))
    print(f'delete {keys.count()} keys')
    keys.delete()

@background()
def remove_keys():
    check_keys()

try:
    if Task.objects.filter(verbose_name="remove_keys").count() == 0:
        remove_keys(repeat=Task.DAILY,verbose_name="remove_keys")
except:
    pass


def get_bank_data(request):
    s = Setting.objects.last()
    return JsonResponse({'Code':200,'bank_card_number':s.bank_card_number,'card_name':s.card_name})

def get_public_key(request):
    key = Key.objects.create()
    return JsonResponse({'key':key.sessionid})

def is_authenticated(request):
    try:
        session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
        session.date = date.today()
        session.save()
        U = Profile.objects.filter(active_session=session.sessionid)
    except:
        return JsonResponse({'Code':400})
    if U.count() != 0:
        dictionary = {}
        dictionary["phone_number"] = U.first().phone_number
        s = Setting.objects.last()
        return JsonResponse({'Code':200,'User':dictionary,'offline':s.kart_be_kart,'online':s.online_pay})
    else:
        return JsonResponse({'Code':401})

def make_factor(request):
    session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
    U = Profile.objects.filter(active_session=session.sessionid)
    if U.count() != 0:
        price = request.GET.get('price')
        nickname = request.GET.get('nickname')
        if request.GET.get('mode') == "online":
            online_mode = True
        elif request.GET.get('mode') == "offline":
            online_mode = False
        factor = Factor.objects.create(price = int(price), nickname = nickname,online_mode=online_mode)
        return JsonResponse({'Code':200,'id':factor.pk})

def show_factor(request):
    pk = int(request.GET.get('pk'))
    factor = Factor.objects.get(pk = pk)
    context = {'Code':200,'status':factor.status, 'nickname': factor.nickname,'price':factor.price}
    return JsonResponse(context)


def fill_factor(request):
    try:
        pk = int(request.GET.get('pk'))
        factor = Factor.objects.get(pk = pk)
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        try:
            description = request.POST['description']
        except:
            pass
        factor.name = name
        factor.phone = phone
        factor.address = address
        factor.description = description
        factor.save()
        return JsonResponse({'Code':200,'mode':factor.online_mode})
    except:
        return JsonResponse({'Code':401})

def Z():
    Z = Setting.objects.first()
    MERCHANT = Z.api_key
    client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
    description = Z.description
    email = ''
    mobile = ''
    return MERCHANT,client,description,email,mobile
    
    
def send_request(request , amount,pk):
    session = Key.objects.get(sessionid=request.GET.get('sessionid'))
    session.add_to_data('callback',request.GET.get('callback'))

    MERCHANT,client,description,email,mobile = Z()
    host = request.META['HTTP_HOST']
    CallbackURL = f'http://{host}/verify/{pk}/?sessionid=' + request.GET.get('sessionid') # Important: need to edit for realy server.
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request,pk):
    session = Key.objects.get(sessionid=request.GET.get('sessionid'))
    data = session.get_session_data()

    MERCHANT,client,description,email,mobile = Z()
    if request.GET.get('Status') == 'OK':
        p = Factor.objects.get(pk=pk)
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], p.price)
        if result.Status == 100:
            p.status =True
            p.order_condition = '2'
            p.save()
            return redirect(data['callback']) 
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
    
from django.core import serializers
def notifications (request):
    ns = Factor.objects.filter(status=True,notification=False)
    data = serializers.serialize('json', ns)
    ns.update(notification=True)
    return HttpResponse(data)



def check_code(request):
    code = request.GET.get('code')
    session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
    data = session.get_session_data()
    if str(data['check-code']) == str(code):
        U = Profile.objects.get(phone_number=data['phone'])
        U.active_session = session.sessionid
        U.save()
        return JsonResponse({'Code':200})
    else:
        return JsonResponse({'Code':401})


def gen_code(request):
    code = randint(1000,9999)
    phone = request.GET.get('phone')
    try:
        Profile.objects.get(phone_number=phone)
    except:
        return JsonResponse({'Code':401})
    KS = KavenegarSetting.objects.first()
    session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
    session.add_to_data('check-code',int(code))
    session.add_to_data('phone',phone)
    sms_by_template(receptor=phone,apikey=KS.apikey,message=code,template=KS.login_template_name)
    print(code)
    return JsonResponse({'Code':200})


def get_factor_list(request):
    session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
    U = Profile.objects.filter(active_session=session.sessionid)
    if U.count() != 0:
        result = []
        filtering = {}
        try:
            date_f = request.GET.get('date').split(',')
            start_str = date_f[0].split('-')
            end_str = date_f[1].split('-')
            start = JalaliDate(start_str[0], start_str[1], start_str[2]).todate()
            end = JalaliDate(end_str[0], end_str[1], end_str[2]).todate() + timedelta(days = 1)
            filtering['date__gte'] = start
            filtering['date__lte'] = end
        except:
            pass
        try:
            mode = request.GET.get('mode')
            if mode == 'online':
                filtering['online_mode'] = True
            elif mode == 'offline':
                filtering['online_mode'] = False
        except:
            pass
        for factor in Factor.objects.filter(**filtering).order_by('-pk'):
            result.append({
                'nickname':str(factor.nickname) if factor.nickname else '',
                'name': str(factor.name) if factor.name else '',
                'address': str(factor.address) if factor.address else '',
                'description': str(factor.description) if factor.description else '',
                'phone': str(factor.phone) if factor.phone else '',
                'price': str(factor.price) if factor.price else '',
                'date':JalaliDatetime(factor.date).strftime("%d %B, %Y"),
                'status': 'پرداخت شده' if factor.status else 'در انتظار',
                'status_bool': factor.status,
                'id': str(factor.pk) if factor.pk else '',
                'mode': 'online' if factor.online_mode else 'offline',
            })
        return JsonResponse({'Code':200,'list':result})
    else:
        return JsonResponse({'Code':401})

def factor_for_edit(request):
    session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
    U = Profile.objects.filter(active_session=session.sessionid)
    if U.count() != 0:
        pk = int(request.GET.get('pk'))
        factor = Factor.objects.get(pk = pk)
        context = {
            'Code':200,
            'nickname':str(factor.nickname) if factor.nickname else '',
            'name': str(factor.name) if factor.name else '',
            'address': str(factor.address) if factor.address else '',
            'description': str(factor.description) if factor.description else '',
            'phone': str(factor.phone) if factor.phone else '',
            'price': str(factor.price) if factor.price else '',
            'date':JalaliDatetime(factor.date).strftime("%d %B, %Y"),
            'status': 'پرداخت شده' if factor.status else 'در انتظار',
            'status_bool': factor.status,
            'id': str(factor.pk) if factor.pk else '',
        }
        return JsonResponse(context)
    else:
        return JsonResponse({'Code':401})

def pay_factor(request):
    try:
        session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
        U = Profile.objects.filter(active_session=session.sessionid)
        f = Factor.objects.get(pk=int(request.GET.get('pk')))
        f.status = True
        f.order_condition = '2'
        f.save()
        return JsonResponse({'Code':200})
    except:
        return JsonResponse({'Code':401})
  

def delete_factor(request):
    try:
        session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
        U = Profile.objects.filter(active_session=session.sessionid)
        Factor.objects.get(pk=int(request.GET.get('pk'))).delete()
        return JsonResponse({'Code':200})
    except:
        return JsonResponse({'Code':401})


def print_factor(request):
    try:
        session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
        U = Profile.objects.filter(active_session=session.sessionid)
        f = Factor.objects.get(pk=int(request.GET.get('pk')))
        f.notification = True
        f.save()
        return JsonResponse({'Code':200})
    except:
        return JsonResponse({'Code':401})

def edit_factor(request):
    session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
    U = Profile.objects.filter(active_session=session.sessionid)
    if U.count() != 0:
        try:
            pk = int(request.GET.get('pk'))
            factor = Factor.objects.get(pk = pk)
            nickname = request.POST['nickname']
            price = request.POST['price']
            name = request.POST['name']
            phone = request.POST['phone']
            address = request.POST['address']
            try:
                description = request.POST['description']
            except:
                pass
            factor.nickname = nickname
            factor.price = price
            factor.name = name
            factor.phone = phone
            factor.address = address
            factor.description = description
            factor.save()
            return JsonResponse({'Code':200})
        except:
            return JsonResponse({'Code':401})
    else:
        return JsonResponse({'Code':401})

def send_sms(request):
    try:    
        session = Key.objects.get(sessionid=request.META['HTTP_AUTHORIZATION'])
        U = Profile.objects.filter(active_session=session.sessionid)
        KS = KavenegarSetting.objects.first()
        s = Setting.objects.last()
        f = Factor.objects.get(pk=request.GET.get('pk'))
        sms_by_template(template=KS.EpayReminder_template,apikey=KS.apikey,receptor=f.phone,message=s.description,message2=request.GET.get('link'))
        return JsonResponse({'Code':200})
    except:
        return JsonResponse({'Code':401})