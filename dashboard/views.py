from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# from course.models import CourseUser
# from course.serializers import CourseUserSerializer
from course.models import CourseUser
from course.serializers import CourseUserSerializer
from dashboard.serializers import UserDashboardSerializer
from dashboard.utils import retrieve_saved_items, retrieve_comments
from payment.models import Transaction


class GetUserProfileView(APIView):

    @extend_schema(
        responses={200: OpenApiResponse(response=UserDashboardSerializer)},
        description="Get user profile with saved items"
    )
    def post(self, request):
        user = request.user
        if not user:
            return Response({"message": "کاربر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare profile data
        profile_data = {
            'id': user.id,
            'sex': user.sex,
            'full_name': user.full_name,
            'photo': user.photo.id if user.photo else None,
            'phone': user.phone_number
        }

        # Retrieve saved items using the helper function
        saved_data = retrieve_saved_items(user)

        comments_data = retrieve_comments(user)

        # Combine profile, saved items, and comments
        user_courses = CourseUser.objects.filter(user=user, is_deleted=False)  # Get the user's active courses
        # courses_data = CourseUserSerializer(user_courses, many=True).data  # Serialize course data
        user_transactions = Transaction.objects.filter(user=user, is_deleted=False)


        # Combine profile, saved items, comments, and courses
        dashboard_data = {
            'profile': profile_data,
            'saved': saved_data,
            'comments': comments_data,
            'courses': user_courses,  # Add courses to the dashboard data
            'transactions': user_transactions  # pass the queryset; TransactionSerializer will handle it

        }

        # Serialize the data
        serializer = UserDashboardSerializer(dashboard_data)

        return Response(serializer.data, status=status.HTTP_200_OK)