import datetime

from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from security.models import UserLog
from security.serializers import  UserLogRequestSerializer, UserLogResponseSerializer


class UserLogPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        # Try to get 'page' from the request data (body) first, otherwise default to the query params
        return request.data.get('page', 1)  # Default to page 1 if not provided

    def get_page_size(self, request):
        # Try to get 'pageSize' from the request data (body) first, otherwise use the default
        return request.data.get('pageSize', self.page_size)  # Default to class-level page_size if not provided


class UserLogListApiView(APIView):
    @extend_schema(
        request=UserLogRequestSerializer,
        responses={
            200: UserLogResponseSerializer,
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of userlogs"
    )
    def post(self, request):
        # Extract pagination params from the request body (or use defaults)
        page = request.data.get('page', 1)
        page_size = request.data.get('pageSize', 10)

        # Extract date range
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date', timezone.now())  # Default to now if not provided

        if not from_date:
            return Response({"message": "تاریخ از باید ارسال شود!"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure from_date is not later than to_date
        if from_date > str(to_date):
            return Response({"message": "تاریخ از نمی‌تواند از تاریخ تا جلوتر باشد."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the query filter using date range
        query = Q(timestamp__range=(from_date, to_date))

        # If user_id is provided, filter by user
        user_id = request.data.get('user_id')
        if user_id:
            query &= Q(user_id=user_id)

        # Fetch logs based on the query
        logs = UserLog.objects.filter(query)

        # Apply pagination
        paginator = UserLogPagination()
        paginator.page = page
        paginator.page_size = page_size

        # Paginate the logs
        paginated_logs = paginator.paginate_queryset(logs, request)

        # Serialize the logs
        log_serializer = UserLogResponseSerializer(paginated_logs, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(log_serializer.data)