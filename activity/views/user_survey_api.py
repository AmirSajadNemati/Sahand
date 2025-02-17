from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from activity.models import UserSurvey
from serializers import MessageAndIdSerializer, DeleteSerializer, ListRequestSerializer, IdSerializer
from activity.serializers import UserSurveySerializer, UserSurveyListSerializer, UserSurveyGetSerializer
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse

from utils import role_decorator


class UserSurveyAddOrUpdateView(APIView):

    @extend_schema(
        request=UserSurveySerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Add or Update UserSurvey"
    )
    @role_decorator
    def post(self, request):
        user_survey_id = request.data.get('id', 0)

        # Create new user_survey if ID is 0
        if user_survey_id == 0:
            serializer = UserSurveySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "نظرسنجی کاربر با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update an existing user_survey
        try:
            user_survey = UserSurvey.objects.get(pk=user_survey_id)
        except UserSurvey.DoesNotExist:
            return Response({'message': 'نظرسنجی کاربر مورد نظرسنجی کاربر یافت نشد.', "id": user_survey_id},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSurveySerializer(user_survey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "نظرسنجی کاربر با موفقیت به روزرسانی شد!", "id": user_survey_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSurveyPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class UserSurveyGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={200: OpenApiResponse(response=UserSurveyListSerializer())},
        description="Get List of UserSurveys"
    )
    @role_decorator
    def post(self, request):
        # Validate and deserialize the request data
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

        user_surveys = UserSurvey.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            user_surveys = user_surveys.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            user_surveys = user_surveys.order_by('id')  # or any field you prefer

        # Pagination
        paginator = UserSurveyPagination()
        paginated_user_surveys = paginator.paginate_queryset(user_surveys, request)

        # Serialize the paginated data
        serializer = UserSurveySerializer(paginated_user_surveys, many=True)
        data = paginator.get_paginated_response(serializer.data)

        # Define the propertiesAttribute for the UserSurvey model
        properties_attribute = {
            "propertyName": "UserSurvey Text",
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
            "propertyPersianName": "متن نظرسنجی کاربر",
            "isSort": True,
            "isUrl": False,
            "isCopy": False,
            "statusFieldData": []
        }

        # Return paginated response
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'data': serializer.data,  # Instead of 'results', now 'data'
            'propertiesAttribute': properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UserSurveyGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=UserSurveyGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific UserSurvey by ID"
    )
    @role_decorator
    def post(self, request):
        user_survey_id = request.data.get('id', 0)
        properties_attribute = [
    {
      "order": 1000,
      "propertyName": "user_id",
      "propertyType": "System.Int64",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": True,
      "fkUrl": "/security/UserList/",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "UserData.FullName",
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
          "value": "کاربر ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "UserData",
      "propertyType": "StructureAndDataBase.Datas.ViewModels.Security.UserViewModel",
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
      "propertyName": "survey_id",
      "propertyType": "System.Int64",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": True,
      "fkUrl": "/cms/SurveyList/",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "SurveyData.Title",
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
          "value": "نظرسنجی ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "SurveyData",
      "propertyType": "StructureAndDataBase.Datas.ViewModels.Cms.SurveyViewModel",
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
      "propertyName": "Answer",
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
          "value": "پاسخ",
          "message": None
        },
        {
          "type": "MaxLengthAttribute",
          "value": "3000",
          "message": "len of {0} cant more {1} character"
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
        if user_survey_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)
        if not user_survey_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_survey = UserSurvey.objects.get(id=user_survey_id)
        except UserSurvey.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSurveySerializer(user_survey)

        # Prepare the response structure with manual property attribute definitions for UserSurvey fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UserSurveyDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific UserSurvey by ID"
    )
    @role_decorator
    def post(self, request):
        user_survey_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not user_survey_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_survey = UserSurvey.objects.get(id=user_survey_id)
        except UserSurvey.DoesNotExist:
            return Response({"message": "نظرسنجی کاربر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if user_survey.is_deleted:
                return Response({"message": "نظرسنجی کاربر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            user_survey.is_deleted = True
            user_survey.save()
            return Response({"message": "نظرسنجی کاربر به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if user_survey.is_deleted:
                return Response({"message": "نظرسنجی کاربر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            # if user_survey.photo:
            #     user_survey.photo.is_deleted = True
            #     user_survey.photo.save()

            user_survey.is_deleted = True
            user_survey.save()

            # Add any other related models here

            return Response({"message": "نظرسنجی کاربر و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                user_survey.delete()
                return Response({"message": "نظرسنجی کاربر به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # if user_survey.photo:
                #     user_survey.photo.delete()

                user_survey.delete()
                return Response({"message": "نظرسنجی کاربر و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class UserSurveyUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted UserSurvey by ID"
    )
    @role_decorator
    def post(self, request):
        user_survey_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not user_survey_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_survey = UserSurvey.objects.get(id=user_survey_id)
        except UserSurvey.DoesNotExist:
            return Response({"message": "نظرسنجی کاربر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if user_survey.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                user_survey.is_deleted = False
                user_survey.save()
                return Response({"message": "نظرسنجی کاربر به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                # Soft delete the cms itself
                user_survey.is_deleted = False
                user_survey.save()

                # Add any other related models here

                return Response({"message": "نظرسنجی کاربر و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "نظرسنجی کاربر مورد نظرسنجی کاربر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
