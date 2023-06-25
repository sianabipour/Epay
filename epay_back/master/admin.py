from django.contrib import admin
from master.models import Factor,Setting,Profile,KavenegarSetting
from django.contrib.auth.models import Group,User

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(KavenegarSetting)

@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ('name','phone','price','date_html','status')
    list_filter = ("date",)
    search_fields = ("name",'phone','price','pk','address')   

    
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("api_key",'description','bank_card_number','card_name','online_pay','kart_be_kart')
    

    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("phone_number",'active_session')
    

    
