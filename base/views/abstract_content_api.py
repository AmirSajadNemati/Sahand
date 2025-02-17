from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from serializers import MessageAndIdSerializer, ListRequestSerializer, DeleteSerializer, UrlSerializer
from base.models import AbstractContent
from base.serializers import AbstractContentSerializer, AbstractContentGetSerializer, AbstractContentListSerializer
from utils import role_decorator


class AbstractContentAddOrUpdateView(APIView):

    @extend_schema(
        request=AbstractContentSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update AbstractContent"
    )
    @role_decorator
    def post(self, request):
        abstract_content_id = request.data.get('id', 0)

        # If abstract_content_id is 0, it's a new cms, so create it
        if abstract_content_id == 0:
            serializer = AbstractContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "محتوای ابسترکت با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If abstract_content_id is provided, try to update the existing cms
        try:
            abstract_content = AbstractContent.objects.get(pk=abstract_content_id)
        except AbstractContent.DoesNotExist:
            return Response({'message': 'محتوای ابسترکت مورد نظر برای تغییر یافت نشد.', "id": abstract_content_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing cms
        serializer = AbstractContentSerializer(abstract_content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "محتوای ابسترکت با موفقیت به روزرسانی شد!", "id": abstract_content_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbstractContentPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class AbstractContentGetListView(APIView):
    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=AbstractContentListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of AbstractContents"
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

        abstract_contents = AbstractContent.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            abstract_contents = abstract_contents.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            abstract_contents = abstract_contents.order_by('id')  # or any field you prefer

        # Pagination
        paginator = AbstractContentPagination()
        paginated_users = paginator.paginate_queryset(abstract_contents, request)

        # Serialize the paginated data
        serializer = AbstractContentSerializer(paginated_users, many=True)
        data = paginator.get_paginated_response(serializer.data)
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
        # Return paginated response
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'data': serializer.data,  # Instead of 'results', now 'data'
            'propertiesAttribute': properties_attribute
        }

        # Return custom paginated response
        return Response(response_data, status=status.HTTP_200_OK)


class AbstractContentGetView(APIView):

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(response=AbstractContentGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific AbstractContent by ID"
    )
    @role_decorator
    def post(self, request):
        abstract_content_id = request.data.get('id', 0)
        properties_attribute = [
            {
                "order": 1000,
                "propertyName": "title",
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
                        "value": "250",
                        "message": "len of {0} cant more {1} character"
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "english_title",
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
                        "value": " تیتر صفحه",
                        "message": None
                    },
                    {
                        "type": "RequiredAttribute",
                        "value": "",
                        "message": "{0} is required"
                    },
                    {
                        "type": "MaxLengthAttribute",
                        "value": "250",
                        "message": "len of {0} cant more {1} character"
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Content",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "contentManager/ContentManagerList/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "",
                "fkMultiple": False,
                "isFile": False,
                "fileTypes": [
                    {
                        "value": 1,
                        "label": "همه",
                        "extension": "*.*"
                    }
                ],
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
                "isEditor": True,
                "editorType": "minipopup",
                "isLocation": False,
                "isList": False,
                "listProperty": [],
                "listError": [],
                "locationType": None,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": " محتوا ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "content_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Construction.ObjectTypeEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": "درباره ما",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "چرا ما",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": "خدمات",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": "سوالات متداول",
                        "count": 0
                    },
                    {
                        "value": 5,
                        "label": "مقاله",
                        "count": 0
                    },
                    {
                        "value": 6,
                        "label": "نظرات",
                        "count": 0
                    },
                    {
                        "value": 7,
                        "label": "تیم",
                        "count": 0
                    },
                    {
                        "value": 8,
                        "label": "نمونه کار",
                        "count": 0
                    },
                    {
                        "value": 9,
                        "label": "آمار و ارقام",
                        "count": 0
                    },
                    {
                        "value": 10,
                        "label": "هدر",
                        "count": 0
                    },
                    {
                        "value": 11,
                        "label": "دوره",
                        "count": 0
                    },
                    {
                        "value": 12,
                        "label": "آموزش و استخدام",
                        "count": 0
                    },

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
                        "value": " نوع وابستگی ",
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
                        "label": "غیرفعال",
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
        if abstract_content_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not abstract_content_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            abstract_content = AbstractContent.objects.get(id=abstract_content_id)
        except AbstractContent.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AbstractContentSerializer(abstract_content)

        # Prepare the response structure with manual property attribute definitions for AbstractContent fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AbstractContentDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific AbstractContent by ID"
    )
    @role_decorator
    def post(self, request):
        abstract_content_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not abstract_content_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            abstract_content = AbstractContent.objects.get(id=abstract_content_id)
        except AbstractContent.DoesNotExist:
            return Response({"message": "محتوای ابسترکت یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if abstract_content.is_deleted:
                return Response({"message": "محتوای ابسترکت از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            abstract_content.is_deleted = True
            abstract_content.save()
            return Response({"message": "محتوای ابسترکت به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if abstract_content.is_deleted:
                return Response({"message": "محتوای ابسترکت از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            if abstract_content.photo:
                abstract_content.photo.is_deleted = True
                abstract_content.photo.save()

            if abstract_content.content:
                abstract_content.content.is_deleted = True
                abstract_content.content.save()

            if abstract_content.content_category:
                abstract_content.content_category.is_deleted = True
                abstract_content.content_category.save()

            # Soft delete the cms itself
            abstract_content.is_deleted = True
            abstract_content.save()

            # Add any other related models here

            return Response({"message": "محتوای ابسترکت و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                abstract_content.delete()
                return Response({"message": "محتوای ابسترکت به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # Manually delete the associated photo, content, and category if they exist
                if abstract_content.photo:
                    abstract_content.photo.delete()

                if abstract_content.content:
                    abstract_content.content.delete()

                if abstract_content.content_category:
                    abstract_content.content_category.delete()

                # Finally, delete the cms itself
                abstract_content.delete()
                return Response({"message": "محتوای ابسترکت و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class AbstractContentUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted AbstractContent by ID"
    )
    @role_decorator
    def post(self, request):
        abstract_content_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not abstract_content_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            abstract_content = AbstractContent.objects.get(id=abstract_content_id)
        except AbstractContent.DoesNotExist:
            return Response({"message": "محتوای ابسترکت یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if abstract_content.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                abstract_content.is_deleted = False
                abstract_content.save()
                return Response({"message": "محتوای ابسترکت به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:

                if abstract_content.photo:
                    abstract_content.photo.is_deleted = False
                    abstract_content.photo.save()

                if abstract_content.content:
                    abstract_content.content.is_deleted = False
                    abstract_content.content.save()

                if abstract_content.content_category:
                    abstract_content.content_category.is_deleted = False
                    abstract_content.content_category.save()

                # Soft delete the cms itself
                abstract_content.is_deleted = False
                abstract_content.save()

                # Add any other related models here

                return Response({"message": "محتوای ابسترکت و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "محتوای ابسترکت مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
