from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from serializers import MessageAndIdSerializer, ListRequestSerializer, DeleteSerializer, UrlSerializer
from task_manager.models import TaskDone
from task_manager.serializers import TaskDoneSerializer, TaskDoneGetSerializer, TaskDoneListSerializer
from utils import role_decorator


class TaskDoneAddOrUpdateView(APIView):

    @extend_schema(
        request=TaskDoneSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update TaskDone"
    )
    @role_decorator
    def post(self, request):
        task_done_id = request.data.get('id', 0)

        # If task_done_id is 0, it's a new cms, so create it
        if task_done_id == 0:
            serializer = TaskDoneSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "تسک انجام شده با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If task_done_id is provided, try to update the existing cms
        try:
            task_done = TaskDone.objects.get(pk=task_done_id)
        except TaskDone.DoesNotExist:
            return Response({'message': 'تسک انجام شده مورد نظر برای تغییر یافت نشد.', "id": task_done_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing cms
        serializer = TaskDoneSerializer(task_done, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "تسک انجام شده با موفقیت به روزرسانی شد!", "id": task_done_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDonePagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class TaskDoneGetListView(APIView):
    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=TaskDoneListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of TaskDones"
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

        task_dones = TaskDone.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            task_dones = task_dones.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            task_dones = task_dones.order_by('id')  # or any field you prefer

        # Pagination
        paginator = TaskDonePagination()
        paginated_users = paginator.paginate_queryset(task_dones, request)

        # Serialize the paginated data
        serializer = TaskDoneSerializer(paginated_users, many=True)
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


class TaskDoneGetView(APIView):

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(response=TaskDoneGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific TaskDone by ID"
    )
    @role_decorator
    def post(self, request):
        task_done_id = request.data.get('id', 0)
        properties_attribute = [
            {
                "order": 1000,
                "propertyName": "done_at",
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
                        "value": "تاریخ انجام تسک",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "done_by",
                "propertyType": "System.Collections.Generic.List`1[System.String]",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "security/UserList/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "",
                "fkMultiple": True,
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
                        "value": " افراد انجام دهنده ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1018,
                "propertyName": "is_done",
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
                        "value": "انجام شده/نشده",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "task_request",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/taskManager/TaskRequestList/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "ContentCategoryData.Title",
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
                        "value": "درخواست تسک مربوطه",
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
        if task_done_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not task_done_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_done = TaskDone.objects.get(id=task_done_id)
        except TaskDone.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskDoneSerializer(task_done)

        # Prepare the response structure with manual property attribute definitions for TaskDone fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class TaskDoneDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific TaskDone by ID"
    )
    @role_decorator
    def post(self, request):
        task_done_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not task_done_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_done = TaskDone.objects.get(id=task_done_id)
        except TaskDone.DoesNotExist:
            return Response({"message": "تسک انجام شده یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if task_done.is_deleted:
                return Response({"message": "تسک انجام شده از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            task_done.is_deleted = True
            task_done.save()
            return Response({"message": "تسک انجام شده به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if task_done.is_deleted:
                return Response({"message": "تسک انجام شده از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            if task_done.photo:
                task_done.photo.is_deleted = True
                task_done.photo.save()

            if task_done.content:
                task_done.content.is_deleted = True
                task_done.content.save()

            if task_done.content_category:
                task_done.content_category.is_deleted = True
                task_done.content_category.save()

            # Soft delete the cms itself
            task_done.is_deleted = True
            task_done.save()

            # Add any other related models here

            return Response({"message": "تسک انجام شده و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                task_done.delete()
                return Response({"message": "تسک انجام شده به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # Manually delete the associated photo, content, and category if they exist
                if task_done.photo:
                    task_done.photo.delete()

                if task_done.content:
                    task_done.content.delete()

                if task_done.content_category:
                    task_done.content_category.delete()

                # Finally, delete the cms itself
                task_done.delete()
                return Response({"message": "تسک انجام شده و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class TaskDoneUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted TaskDone by ID"
    )
    @role_decorator
    def post(self, request):
        task_done_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not task_done_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_done = TaskDone.objects.get(id=task_done_id)
        except TaskDone.DoesNotExist:
            return Response({"message": "تسک انجام شده یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if task_done.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                task_done.is_deleted = False
                task_done.save()
                return Response({"message": "تسک انجام شده به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:

                if task_done.photo:
                    task_done.photo.is_deleted = False
                    task_done.photo.save()

                if task_done.content:
                    task_done.content.is_deleted = False
                    task_done.content.save()

                if task_done.content_category:
                    task_done.content_category.is_deleted = False
                    task_done.content_category.save()

                # Soft delete the cms itself
                task_done.is_deleted = False
                task_done.save()

                # Add any other related models here

                return Response({"message": "تسک انجام شده و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "تسک انجام شده مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
