from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse

from serializers import ListRequestSerializer, IdSerializer, DeleteSerializer, MessageAndIdSerializer
from utils import create_property_attribute, get_property_type, role_decorator
from ..models import Survey

from ..serializers import SurveySerializer, SurveyGetSerializer, SurveyListSerializer


class SurveyAddOrUpdateView(APIView):

    @extend_schema(
        request=SurveySerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Add or Update Survey"
    )
    @role_decorator
    def post(self, request):
        survey_id = request.data.get('id', 0)

        # If survey_id is 0, it's a new survey, so create it
        if survey_id == 0:
            serializer = SurveySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "نظرسنجی با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If survey_id is provided, try to update the existing survey
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            return Response({'message': 'نظرسنجی مورد نظر برای تغییر یافت نشد.', "id": survey_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing survey
        serializer = SurveySerializer(survey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "نظرسنجی با موفقیت به روزرسانی شد!", "id": survey_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class SurveyGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=SurveyListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of Surveys"
    )
    @role_decorator
    def post(self, request):
        serializer = ListRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        sort = data.get('sort', '')
        page = data.get('page', 1)
        page_size = data.get('pageSize', 10)
        is_deleted = data.get('is_deleted', False)
        searches = data.get('searches', [])
        filters = data.get('filters', [])

        # Build query
        query = Q(is_deleted=is_deleted)

        # Apply filters
        for filter_item in filters:
            column = filter_item['column']
            value = filter_item['value']
            query &= Q(**{f"{column}__iexact": value})

        # Apply searches
        for search_item in searches:
            column = search_item['column']
            value = search_item['value']
            query &= Q(**{f"{column}__icontains": value})

        surveys = Survey.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            surveys = surveys.order_by(sort_field)
        else:
            surveys = surveys.order_by('id')  # Default ordering

        # Pagination
        paginator = SurveyPagination()
        paginated_surveys = paginator.paginate_queryset(surveys, request)

        # Serialize the paginated data
        serializer = SurveySerializer(paginated_surveys, many=True)

        # Custom response format (like BlogGetListView)
        properties_attribute = {
            "propertyName": "Title",
            "propertyType": "System.String",
            "isSearch": True,
            "isFilter": False,
            "isShow": True,
            "isPrice": False,
            "enumsSelect": [],
            "isEnum": False,
            "isFK": False,
            "fkUrl": "",
            "fkShow": "",
            "fkMultiple": False,
            "fkLevelEnd": False,
            "fknLevel": False,
            "fkParent": False,
            "isDate": False,
            "isRangeDate": False,
            "showType": "self",
            "otherFieldName": "",
            "propertyPersianName": "عنوان",
            "isSort": True,
            "isUrl": False,
            "isCopy": False,
            "statusFieldData": []
        }

        # Custom paginated response
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'data': serializer.data,  # Custom key 'data' instead of 'results'
            'propertiesAttribute': properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SurveyGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=SurveyGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Survey by ID"
    )
    @role_decorator
    def post(self, request):
        survey_id = request.data.get('id', 0)
        properties_attribute = [
    {
      "order": 1000,
      "propertyName": "Title",
      "propertyType": "System.String",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": "عنوان  ",
          "message": None
        },
        {
          "type": "RequiredAttribute",
          "value": "",
          "message": "{0} is required"
        },
        {
          "type": "MaxLengthAttribute",
          "value": "300",
          "message": "len of {0} cant more {1} character"
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "Order",
      "propertyType": "System.Int32",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": " ترتیب ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "start_date",
      "propertyType": "System.String",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "date",
      "isDate": True,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": "تاریخ شروع",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "end_date",
      "propertyType": "System.String",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "date",
      "isDate": True,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": "تاریخ پایان",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "count_answer",
      "propertyType": "System.Int32",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": " تعداد پاسخ ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "Options",
      "propertyType": "System.Collections.Generic.List`1[System.String]",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": True,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
          {
              "type": "DisplayAttribute",
              "value": " آپشن ها ",
              "message": None
          }
      ]
    },
    {
      "order": 1000,
      "propertyName": "survey_items",
      "propertyType": "System.Collections.Generic.List`1[StructureAndDataBase.Datas.Models.Cms.SurveyItem]",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": True,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
          {
              "type": "DisplayAttribute",
              "value": "آیتم های نظرسنجی : ",
              "message": None
          }
      ]
    },
    {
      "order": 1000,
      "propertyName": "Status",
      "propertyType": "StructureAndDataBase.Datas.Models.Construction.BaseStatusEnum",
      "enumsSelect": [
        {
          "value": 1,
          "label": "فعال",
          "count": 0
        },
        {
          "value": 2,
          "label": "غیر فعال",
          "count": 0
        }
      ],
      "isEnum": True,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": "وضعیت : ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "StatusValue",
      "propertyType": "System.String",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": True,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": []
    },
    {
      "order": 1000,
      "propertyName": "StatusData",
      "propertyType": "StructureAndDataBase.Datas.ViewModels.Construction.StatusFieldData",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": True,
      "isHidden": False,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": []
    },
    {
      "order": 1000,
      "propertyName": "Id",
      "propertyType": "System.Int64",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": True,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": "شناسه : ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "is_deleted",
      "propertyType": "System.Boolean",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": False,
      "fkUrl": "",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "",
      "fkMultiple": False,
      "isFile": False,
      "fileTypes": [],
      "fileUrl": "",
      "fileMultiple": False,
      "isReadOnly": False,
      "isNotShow": False,
      "isHidden": True,
      "dateType": "",
      "isDate": False,
      "isColor": False,
      "isPrice": False,
      "priceType": None,
      "isTag": False,
      "isEditor": False,
      "editorType": None,
      "isLocation": False,
      "isList": False,
      "listProperty": [],
      "listError": [],
      "locationType": None,
      "attribute": [
        {
          "type": "DisplayAttribute",
          "value": "وضعیت حذف : ",
          "message": None
        }
      ]
    }
  ]
        if survey_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not survey_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SurveyGetSerializer(survey)
        # Prepare the response structure
        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute  # Placeholder for any additional properties
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SurveyDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Survey by ID"
    )
    @role_decorator
    def post(self, request):
        survey_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not survey_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return Response({"message": "نظرسنجی یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete
            if survey.is_deleted:
                return Response({"message": "نظرسنجی از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            survey.is_deleted = True
            survey.save()
            return Response({"message": "نظرسنجی به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete associated resources (if any)
            if survey.is_deleted:
                return Response({"message": "نظرسنجی از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)

            # Perform soft delete on any related resources here (if applicable)

            survey.is_deleted = True
            survey.save()
            return Response({"message": "نظرسنجی و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete
            try:
                survey.delete()
                return Response({"message": "نظرسنجی به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # Manually delete any associated resources here (if applicable)
                survey.delete()
                return Response({"message": "نظرسنجی و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class SurveyUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Survey by ID"
    )
    @role_decorator
    def post(self, request):
        survey_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not survey_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return Response({"message": "نظرسنجی یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if survey.is_deleted:
            if delete_type == 1:
                survey.is_deleted = False
                survey.save()
                return Response({"message": "نظرسنجی به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                # Restore associated resources
                # Restore logic for any related resources here (if applicable)

                survey.is_deleted = False
                survey.save()
                return Response({"message": "نظرسنجی و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "نظرسنجی مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
