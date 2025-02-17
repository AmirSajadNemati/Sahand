# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from communicating.models import Consult
from communicating.serializers import ConsultSerializer


class ConsultSearchView(APIView):
    def post(self, request):
        url = request.data.get('url')

        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Filtering Consult objects where `page_link` JSON field contains the URL
        consults = Consult.objects.filter(Q(page_link__contains=url))

        # Serialize the filtered consults
        serializer = ConsultSerializer(consults, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
