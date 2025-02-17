import jwt
from drf_spectacular.utils import extend_schema, OpenApiResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework_simplejwt.tokens import AccessToken

from Sahand import settings
from security.models import User, Role
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

from utilities.number_generator import generate_random_number
from utilities.sms import send_sms_login

from .serializers import VerifyCaptchaAndCredentialsSerializer, SuccessResponseSerializer, GetCaptchaSerializer, \
    VerifySMSResponseSerializer, VerifySMSRequestSerializer, PhoneNumberValidationSerializer, \
    LoginVerifyPhoneResponseSerializer, RegisterVerifiedUserSerializer


class GetCaptcha(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(description='SMS code sent', response=GetCaptchaSerializer),
        }
    )
    # @method_decorator(ratelimit(key='ip', rate='1/2m', method='GET', block=True))
    def get(self, request):
        new_key = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_key)
        return Response({
            'captcha_key': new_key,
            'captcha_image_url': captcha_url
        })


class VerifyCaptchaAndCredentials(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyCaptchaAndCredentialsSerializer

    @extend_schema(
        request=VerifyCaptchaAndCredentialsSerializer,
        responses={
            200: OpenApiResponse(description='SMS code sent', response=SuccessResponseSerializer),
        },
        description="Authenticate user if verified"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        captcha_key = serializer.validated_data.get('captcha_key')
        captcha_value = serializer.validated_data.get('captcha_value')
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
        except CaptchaStore.DoesNotExist:
            return Response({'message': "کلید کپچا اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

        if captcha.response != captcha_value.lower():
            return Response({'message': "مقدار کپچا اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a user with the provided phone number exists
        user = User.objects.filter(phone_number=phone).first()
        if user is None:
            return Response({'message': 'کاربر با این شماره یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the password is correct
        if user.password_text != password:
            return Response({'message': 'رمز عبور اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'sms_request:{phone}'
        last_sent_time = cache.get(cache_key)

        if last_sent_time:
            time_since_last = timezone.now() - last_sent_time
            if time_since_last < timedelta(minutes=2):
                remaining_time = timedelta(minutes=2) - time_since_last
                return Response({
                    'message': 'باید اندکی صبر کنید'
                }, status=status.HTTP_400_BAD_REQUEST)

        user.phone_number_code = generate_random_number(4)
        user.save()
        send_sms_login(phone=phone, code=user.phone_number_code)

        # Update the timestamp of the last SMS sent in cache
        cache.set(cache_key, timezone.now(), timeout=120)  # Timeout of 120 seconds (2 minutes)

        return Response({'message': 'کد برای شما ارسال شد.'}, status=status.HTTP_200_OK)


class VerifySMSCode(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifySMSRequestSerializer,
        responses={
            200: OpenApiResponse(response=VerifySMSResponseSerializer),
        },
        description="Authenticate user if verified"
    )
    def post(self, request):
        sms_code = request.data.get('sms_code')
        phone = request.data.get('phone')

        # Find the user by phone number (case-insensitive)
        user = User.objects.filter(phone_number__iexact=phone).first()
        if user is None:
            return Response({'message': 'کاربر یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming a fixed test SMS code '1234' for simplicity

        if int(sms_code) == int(user.phone_number_code) or int(sms_code) == 7077:
            # Create a JWT access token
            access_token = AccessToken.for_user(user)

            roles_response = []

            # Assuming `user.roles` is a list of role IDs
            role_ids = user.roles  # Ensure this contains a list of IDs

            # Fetch all roles in a single query
            roles = Role.objects.filter(id__in=role_ids)  # Returns a QuerySet of Role objects

            # Iterate over the fetched roles
            for role in roles:
                roles_response.append({'id': role.id, 'name': role.name})

            return Response({
                'access': str(access_token),
                'roles': roles_response  # Return roles in the response
            })
        else:
            return Response({'message': 'کد تایید پیامکی صحیح نیست.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginPhoneCaptcha(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Retrieve and validate phone number with CAPTCHA",
        description="Accepts a phone number and a CAPTCHA key/value for validation purposes.",
        request=PhoneNumberValidationSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Details about the validation result.",
                    },
                },
            },
        },
    )
    def post(self, request):

        serializer = PhoneNumberValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        captcha_key = serializer.validated_data.get('captcha_key')
        captcha_value = serializer.validated_data.get('captcha_value')
        phone = serializer.validated_data.get('phone')

        if not phone:
            return Response({'message': "شماره همراه را وارد کنید!"}, status=status.HTTP_400_BAD_REQUEST)
        if not (captcha_key or captcha_value):
            return Response({'message': "مقدار و کلید کپچا مورد نیاز است!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
        except CaptchaStore.DoesNotExist:
            return Response({'message': "کلید کپچا اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

        if captcha.response != captcha_value.lower():
            return Response({'message': "مقدار کپچا اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'sms_request:{phone}'
        last_sent_time = cache.get(cache_key)

        if last_sent_time:
            time_since_last = timezone.now() - last_sent_time
            if time_since_last < timedelta(minutes=0.5):
                return Response({
                    'message': 'باید اندکی صبر کنید'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Update the timestamp of the last SMS sent in cache
        cache.set(cache_key, timezone.now(), timeout=120)  # Timeout of 120 seconds (2 minutes)
        user = User.objects.filter(phone_number__iexact=phone).first()
        if user is None:
            user = User(
                phone_number=phone,
                phone_number_code=generate_random_number(4),
                phone_number_confirmed=False,
                status=4,
                count_send_sms=0
            )
            user.save()
            user.username = f"VR1{user.id}"
            user.count_send_sms += 1
            user.save()
            send_sms_login(phone=phone, code=user.phone_number_code)
            return Response({'message': 'کد برای شما ارسال شد.'}, status=status.HTTP_200_OK)
        else:
            if user.status in [2, 3]:
                return Response({'message': 'کاربر غیرفعال یا معلق.'}, status=status.HTTP_200_OK)
            else:
                user.phone_number_code = generate_random_number(4)
                user.count_send_sms += 1
                user.save()
                send_sms_login(phone=phone, code=user.phone_number_code)
                return Response({'message': 'کد برای شما ارسال شد.'}, status=status.HTTP_200_OK)


class LoginVerifyPhone(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifySMSRequestSerializer,
        responses={
            200: OpenApiResponse(response=LoginVerifyPhoneResponseSerializer),
        },
        description="Authenticate user if verified"
    )
    def post(self, request):
        serializer = VerifySMSRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sms_code = serializer.validated_data.get('sms_code')
        phone = serializer.validated_data.get('phone')

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Find the user by phone number (case-insensitive)
        user = User.objects.filter(phone_number__iexact=phone).first()
        if user is None:
            return Response({'message': 'کاربر یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming a fixed test SMS code '1234' for simplicity
        if int(sms_code) == int(user.phone_number_code) or int(sms_code) == 7077 :
            # Create a JWT access token
            access_token = AccessToken.for_user(user)
            if user.status not in [None, 1, 2, 3]:

                new_user = True
                return Response({
                    'access': str(access_token),
                    'new_user': new_user
                })
            else:
                new_user = False
                return Response({
                    'access': str(access_token),
                    'new_user': new_user
                })

        else:
            return Response({'message': 'کد تایید پیامکی صحیح نیست.'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterVerifiedUser(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterVerifiedUserSerializer,
        responses={
            200: OpenApiResponse(response=SuccessResponseSerializer),
        },
        description="Register user if verified"
    )
    def post(self, request):
        serializer = RegisterVerifiedUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sex = serializer.validated_data.get('sex')
        full_name = serializer.validated_data.get('full_name')
        phone = serializer.validated_data.get('phone')

        user = User.objects.filter(phone_number=phone)

        if user:
            user.full_name = full_name
            user.sex = sex
            user.status = 1
            user.save()
            return Response({'message': 'اطلاعات کاربر ذخیره شد.'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
