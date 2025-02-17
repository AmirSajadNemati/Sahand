from django import forms
from captcha.fields import CaptchaField
from security.models import User


class PhoneForm(forms.Form):
    phone = forms.CharField(
        label="phone",
        max_length=11,
        error_messages={
            'required': 'شماره همراه خود را وارد کنید !',
        })
    captcha = CaptchaField()

    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     user = User.objects.filter(phone__iexact=phone)
    #     if user is None:
    #         raise forms.ValidationError('Wrong Number!')
    #     return phone


class SMSCodeForm(forms.Form):
    sms_code = forms.CharField(max_length=6)
