import time

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course, CourseUser
from payment.models import Transaction
from payment.serializers import BuyCourseRequestSerializer, BuyCourseResponseSerializer
from payment.views import send_request, verify


class BuyCourseView(APIView):

    @extend_schema(
        request=BuyCourseRequestSerializer,
        responses={
            200: OpenApiResponse(response=BuyCourseResponseSerializer),
        },
        description="Buy Initial request"
    )
    def post(self, request):
        user = request.user

        if not user or not user.is_authenticated:
            return Response(
                {"message": "کاربر نامعتبر یا یافت نشد!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BuyCourseRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "اطلاعات ارسال شده نامعتبر است!", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Retrieve validated data
        # response = send_request(request, 1000)
        course_id = serializer.validated_data['course_id']
        is_full = serializer.validated_data['is_full']
        try:
            course = Course.objects.get(id=course_id)

        except Course.DoesNotExist:
            return Response({'message': "دوره نامعتبر"}, status=status.HTTP_400_BAD_REQUEST)
        # check if user has the course
        course_user = CourseUser.objects.filter(user=request.user, course_id=course_id).first()
        if course_user:
            if course_user.is_completed:
                return Response({'message': "دوره در حال حاضر برای کاربر فعال است"}, status=status.HTTP_400_BAD_REQUEST)
        if is_full:
            pay_request_response = send_request(request, course.price, course_id)
            new_transaction = Transaction(
                user=user,
                authority=pay_request_response.get('authority'),
                pay_price=course.price,
                pay_status="pending"
            )
            new_transaction.save()
            print(new_transaction)
            if course_user:
                if course_user.transactions is None:
                    course_user.transactions = []  # Initialize if it's None
                course_user.transactions.append(new_transaction.id)
                course_user.save()
            else:
                course_user = CourseUser(
                    course=course,
                    is_full=True,
                    user=user,
                    course_price=course.price,
                    course_installment_count=None,
                    transactions=[new_transaction.id],  # Add the transaction ID to a new list
                )
                course_user.save()

            return Response(pay_request_response, status=status.HTTP_200_OK)
        # not full
        else:
            installment_price = course.price / course.installment_count
            pay_request_response = send_request(request, installment_price, course_id)
            if course_user:
                new_transaction = Transaction(
                    user=user,
                    authority=pay_request_response.get('authority'),
                    pay_price=course.price / course.installment_count,
                    pay_status="pending"
                )
                new_transaction.save()
                course_user.transactions.append(new_transaction.id)
                course_user.save()
                return Response(pay_request_response, status=status.HTTP_200_OK)
            else:

                new_transaction = Transaction(
                    user=user,
                    authority=pay_request_response.get('authority'),
                    pay_price=course.price / course.installment_count,
                    pay_status="pending"
                )
                new_transaction.save()

                course_user = CourseUser(
                    course=course,
                    is_full=False,
                    user=user,
                    course_price=course.price,
                    course_installment_count=3,
                    transactions=[new_transaction.id],  # Add the transaction ID to a new list
                )
                course_user.save()

                return Response(pay_request_response, status=status.HTTP_200_OK)


class VerifyBuyCourseView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=BuyCourseRequestSerializer,
        responses={
            200: OpenApiResponse(response=BuyCourseResponseSerializer),
        },
        description="Buy Initial request"
    )
    def post(self, request):
        user = request.user
        authority = request.data.get("authority")

        try:
            transaction = Transaction.objects.get(authority=authority)
        except Transaction.DoesNotExist:
            return Response({'message': "تراکنش یافت نشد."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course_user = CourseUser.objects.get(transactions__contains=transaction.id)
        except CourseUser.DoesNotExist:
            return Response({'message': "دوره برای کاربر ایجاد نشد."}, status=status.HTTP_400_BAD_REQUEST)
        if course_user.is_completed:
            return Response({'message': "دوره در حال حاضر برای کاربر فعال است"}, status=status.HTTP_400_BAD_REQUEST)

        if course_user.is_full:
            verify_response = verify(authority=authority, amount=transaction.pay_price)
            print(verify_response)
            if verify_response['status']:
                transaction.pay_status = 'Success'
                transaction.ref_id = verify_response['RefID']
                transaction.pay_time = timezone.now()
                transaction.save()

                course_user.is_completed = True
                course_user.save()
                return Response(
                    {'message': f"دوره {course_user.course.title} برای کاربر {request.user.full_name} خریداری شد!"},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                transaction.status = 'Failed'
                transaction.pay_time = timezone.now()
                transaction.save()
                return ({'message': f"تراکنش تایید نشد کد {str(verify_response['status'])}"})
        # installment
        else:
            verify_response = verify(authority=authority, amount=transaction.pay_price)
            if verify_response['status']:
                transaction.pay_status = 'Success'
                transaction.ref_id = verify_response['RefID']
                transaction.pay_time = timezone.now()
                transaction.save()

                course_user.paid_installments += 1
                if course_user.paid_installments == course_user.course.installment_count:
                    course_user.is_completed = True
                    course_user.save()
                    return Response(
                        {
                            'message': f"قسط {course_user.paid_installments} دوره {course_user.course.title} برای کاربر {request.user.full_name} خریداری شد!"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                transaction.status = 'Failed'
                transaction.pay_time = timezone.now()
                transaction.save()
                return ({'message': f"تراکنش تایید نشد کد {str(verify_response['status'])}"})
