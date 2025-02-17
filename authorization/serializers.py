from rest_framework import serializers

class VerifyCaptchaAndCredentialsSerializer(serializers.Serializer):
    captcha_key = serializers.CharField(max_length=255)
    captcha_value = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128)

class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)

class GetCaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField(max_length=255)
    captcha_value = serializers.CharField(max_length=255)

class VerifySMSResponseSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=255)
    roles = serializers.JSONField()

class VerifySMSRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    sms_code = serializers.CharField(max_length=15)


class PhoneNumberValidationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=15,  # Adjust the max length if needed
        help_text="The phone number to validate, in international format.",
        required=True
    )
    captcha_key = serializers.CharField(
        help_text="The CAPTCHA key to generate captcha image.",
        required=True
    )
    captcha_value = serializers.CharField(
        help_text="The CAPTCHA response string to validate.",
        required=True
    )

class LoginVerifyPhoneResponseSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    access = serializers.CharField(max_length=255)
    new_user = serializers.BooleanField()

class RegisterVerifiedUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    sex = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)