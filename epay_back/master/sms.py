from kavenegar import *
import requests


def sms_by_template(receptor,message,template,apikey,message2=None):
    try:
        api = KavenegarAPI(apikey)
        params = {
            'sender': '10008445',
            'receptor' :receptor,
            'token' : message,
            'template': template,
            'type': 'sms'
        }
        if message2:
            params['token2'] = message2

        response = api.verify_lookup(params)
    except:
        pass
