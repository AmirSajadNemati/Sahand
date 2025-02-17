from django.urls import path, include
from . import views

urlpatterns = [
    path('GetCaptcha/', views.GetCaptcha.as_view(), name='get_captcha'),
    path('VerifyCaptchaAndCredentials/', views.VerifyCaptchaAndCredentials.as_view(),
         name='verify_captcha_and_credentials'),
    path('VerifySMSCode/', views.VerifySMSCode.as_view(), name='verify_sms_code'),
    path('Login/', views.LoginPhoneCaptcha.as_view(), name='login_phone_captcha'),
    path('LoginVerifyPhone/', views.LoginVerifyPhone.as_view(), name='verify_phone_captcha'),
    path('LoginVerifiedUser/', views.RegisterVerifiedUser.as_view(), name='register_user'),

]