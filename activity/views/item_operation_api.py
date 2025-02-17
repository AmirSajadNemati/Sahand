from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from activity.models import ItemOperation

from course.models import Course
from course.serializers import CourseSerializer
from serializers import MessageAndIdSerializer, DeleteSerializer, ListRequestSerializer, IdSerializer
from activity.serializers import ItemOperationSerializer, ItemOperationListSerializer, ItemOperationGetSerializer
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse

from utils import create_property_attribute, role_decorator



class ItemOperationAddOrUpdateView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=ItemOperationSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Add or Update ItemOperation"
    )
    def post(self, request):
        item_operation_id = request.data.get('id', 0)

        # Create new item_operation if ID is 0
        if item_operation_id == 0:
            serializer = ItemOperationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "عملیات آیتم با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update an existing item_operation
        try:
            item_operation = ItemOperation.objects.get(pk=item_operation_id)
        except ItemOperation.DoesNotExist:
            return Response({'message': 'عملیات آیتم مورد عملیات آیتم یافت نشد.', "id": item_operation_id},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ItemOperationSerializer(item_operation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "عملیات آیتم با موفقیت به روزرسانی شد!", "id": item_operation_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemOperationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class ItemOperationGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={200: OpenApiResponse(response=ItemOperationListSerializer())},
        description="Get List of ItemOperations"
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

        item_operations = ItemOperation.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            item_operations = item_operations.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            item_operations = item_operations.order_by('id')  # or any field you prefer

        # Pagination
        paginator = ItemOperationPagination()
        paginated_item_operations = paginator.paginate_queryset(item_operations, request)

        # Serialize the paginated data
        serializer = ItemOperationSerializer(paginated_item_operations, many=True)
        data = paginator.get_paginated_response(serializer.data)

        # Define the propertiesAttribute for the ItemOperation model
        properties_attribute = {
            "propertyName": "ItemOperation Text",
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
            "propertyPersianName": "متن عملیات آیتم",
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


class ItemOperationGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=ItemOperationGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific ItemOperation by ID"
    )
    @role_decorator
    def post(self, request):
        item_operation_id = request.data.get('id', 0)

        properties_attribute = [
            {
                "order": 1000,
                "propertyName": "object_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Construction.ObjectTypeEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": "دوره",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "بلاگ",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": "نمونه کار",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": "پست",
                        "count": 0
                    },
                    {
                        "value": 5,
                        "label": "استوری",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": "خدمات",
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
                        "value": " نوع وابستگی ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "User",
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
                "propertyName": "Related_id",
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
                        "value": "شناسه وابستگی ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "operation_date",
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
                        "value": "تاریخ عملیات",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "item_operation_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Construction.ItemOperationEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": " لایک ",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": " دیسلایک ",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": " ذخیره ",
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
                        "value": " نوع عملیات ",
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
        if item_operation_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        elif not item_operation_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item_operation = ItemOperation.objects.get(id=item_operation_id)
        except ItemOperation.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ItemOperationSerializer(item_operation)

        # Prepare the response structure with manual property attribute definitions for ItemOperation fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ItemOperationDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific ItemOperation by ID"
    )
    @role_decorator
    def post(self, request):
        item_operation_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not item_operation_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item_operation = ItemOperation.objects.get(id=item_operation_id)
        except ItemOperation.DoesNotExist:
            return Response({"message": "عملیات آیتم یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if item_operation.is_deleted:
                return Response({"message": "عملیات آیتم از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            item_operation.is_deleted = True
            item_operation.save()
            return Response({"message": "عملیات آیتم به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if item_operation.is_deleted:
                return Response({"message": "عملیات آیتم از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            if item_operation.photo:
                item_operation.photo.is_deleted = True
                item_operation.photo.save()

            if item_operation.content:
                item_operation.content.is_deleted = True
                item_operation.content.save()

            if item_operation.content_category:
                item_operation.content_category.is_deleted = True
                item_operation.content_category.save()

            # Soft delete the cms itself
            item_operation.is_deleted = True
            item_operation.save()

            # Add any other related models here

            return Response({"message": "عملیات آیتم و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                item_operation.delete()
                return Response({"message": "عملیات آیتم به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # if item_operation.photo:
                #     item_operation.photo.delete()

                item_operation.delete()
                return Response({"message": "عملیات آیتم و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class ItemOperationUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted ItemOperation by ID"
    )
    @role_decorator
    def post(self, request):
        item_operation_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not item_operation_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item_operation = ItemOperation.objects.get(id=item_operation_id)
        except ItemOperation.DoesNotExist:
            return Response({"message": "عملیات آیتم یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if item_operation.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                item_operation.is_deleted = False
                item_operation.save()
                return Response({"message": "عملیات آیتم به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                # Soft delete the cms itself
                item_operation.is_deleted = False
                item_operation.save()

                # Add any other related models here

                return Response({"message": "عملیات آیتم و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "عملیات آیتم مورد عملیات آیتم حذف نشده است."},
                            status=status.HTTP_400_BAD_REQUEST)
