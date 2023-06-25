from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import naturaltime
import uuid

class Profile(models.Model):
    phone_number = models.CharField(
        max_length=20, unique=True, verbose_name="شماره همراه")
    active_session = models.UUIDField(null=True,blank=True)
    def __str__(self):
        return self.phone_number
    class Meta:
        verbose_name_plural = "کارمند ها"
        verbose_name = 'کارمند ها'
        

import json
class Key(models.Model):
    sessionid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data = models.TextField(default='{}')
    date = models.DateField(auto_now_add=True)
    def get_session_data(self):
        data = json.loads(self.data.replace("'", '"'))
        return data
    def add_to_data(self,key,value):
        data = json.loads(self.data.replace("'", '"'))
        data[key] = value
        self.data = str(data)
        self.save()


class Factor(models.Model):
    nickname = models.CharField(max_length=200)
    name = models.CharField(max_length=200 , blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=13 , blank=True, null=True)
    price = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    ORDER_CHOICES = [
        ('1', 'ثبت شده پرداخت نشده'),
        ('2', 'پرداخت انجام شده'),
    ]
    order_condition  = models.CharField(
        max_length=2,
        choices=ORDER_CHOICES,
        default='1',
    )
    online_mode = models.BooleanField(default=True)
    
    @admin.display
    def date_html(self):
        return format_html(naturaltime(self.date))

    class Meta:
        verbose_name_plural = "فاکتور ها"
        

class Setting(models.Model):
    api_key = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    online_pay = models.BooleanField(default=True)
    bank_card_number = models.CharField(max_length=50,null=True,blank=True)
    card_name = models.CharField(max_length=50,null=True,blank=True)
    kart_be_kart = models.BooleanField(default=True)
    def __str__(self):
        return self.api_key
    class Meta:
        verbose_name_plural = "تنظیمات"
        
class KavenegarSetting (models.Model):
    apikey = models.CharField(max_length=450)
    login_template_name = models.CharField(max_length=50)
    EpayReminder_template = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.apikey
    class Meta:
        verbose_name_plural = "تنظیمات کاوه نگار"
        verbose_name = "تنظیمات کاوه نگار"