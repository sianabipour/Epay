
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from master import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('make-factor/', views.make_factor),
    path('get-bank-data/', views.get_bank_data),
    path('factor/', views.show_factor),
    path('factor-for-edit/', views.factor_for_edit),
    path('edit-factor/', views.edit_factor),
    path('fill-factor/', views.fill_factor),
    path('gen-code/',views.gen_code),
    path('check-code/',views.check_code),
    path('get-factor-list/',views.get_factor_list),
    path('delete-factor/',views.delete_factor),
    path('pay-factor/',views.pay_factor),
    path('print-factor/',views.print_factor),
    path('send-sms/',views.send_sms),

    path('get-public-key/',views.get_public_key),
    path('is-authenticated/',views.is_authenticated),

    path('request/<int:amount>/<int:pk>/', views.send_request),
    path('verify/<int:pk>/', views.verify),
    path('notifications/', views.notifications),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
