from django.urls import path

from payment.views import send_request
from payment.views.buy_course_api import BuyCourseView, VerifyBuyCourseView

urlpatterns = [
    path('request/', send_request, name='zarinpal_request'),
    path('BuyCourse/', BuyCourseView.as_view(), name='buy_course'),
    path('VerifyBuyCourse/', VerifyBuyCourseView.as_view(), name='verify_buy_course')
]