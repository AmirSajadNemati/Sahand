from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from frontend_api.serializers import TaskRequestContentSerializer
from serializers import UrlSerializer
from task_manager.models import TaskRequest


class TaskRequestDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(TaskRequestContentSerializer),
        },
    )
    def post(self, request):
        # Extracting the data from request
        en_name = request.data.get('url')

        try:
            # Retrieve the service based on the english_title and is_deleted fields
            task_request = TaskRequest.objects.get(title=en_name, is_deleted=False)
            # Serialize the single service object (do not use `many=True`)
            serializer = TaskRequestContentSerializer(task_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskRequest.DoesNotExist:
            # Handle case where service is not found
            return Response({'message': 'درخواست تسک یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)
