from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from security.models import User
from serializers import MessageAndIdSerializer, ListRequestSerializer, DeleteSerializer, UrlSerializer, IdSerializer
from task_manager.models import TaskRequest, TaskProject
from task_manager.serializers import TaskRequestSerializer, TaskRequestGetSerializer, TaskRequestListSerializer, \
    TaskProjectIdSerializer
from utilities.sms import send_sms_new_task
from utils import role_decorator


class TaskRequestAddOrUpdateView(APIView):

    @extend_schema(
        request=TaskRequestSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Add or Update TaskRequest"
    )
    @role_decorator
    def post(self, request):
        task_request_id = request.data.get('id', 0)

        # اگر task_request_id صفر باشد، تسک جدید ایجاد شود
        if task_request_id == 0:
            serializer = TaskRequestSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                task_request = serializer.save()

                if task_request.requires_sms:
                    for member in task_request.todo_users:
                        user = User.objects.get(id=member)
                        send_sms_new_task(user.phone_number, user.sex, user.full_name, task_request.title,
                                          task_request.task_project.title)
                return Response({"message": "درخواست تسک با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # اگر `id` مشخص شده باشد، سعی کن تسک موجود را آپدیت کنی
        try:
            task_request = TaskRequest.objects.get(pk=task_request_id)
        except TaskRequest.DoesNotExist:
            return Response({'message': 'درخواست تسک مورد نظر برای تغییر یافت نشد.', "id": task_request_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # به‌روزرسانی تسک موجود
        serializer = TaskRequestSerializer(task_request, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "درخواست تسک با موفقیت به‌روزرسانی شد!", "id": task_request_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskRequestPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class TaskRequestGetListView(APIView):
    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=TaskRequestListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of TaskRequests"
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
            query &= Q(**{f"{column}__exact": value})

        # Apply searches
        for search_item in searches:
            column = search_item['column']
            value = search_item['value']
            query &= Q(**{f"{column}__icontains": value})

        task_requests = TaskRequest.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            task_requests = task_requests.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            task_requests = task_requests.order_by('id')  # or any field you prefer

        # Pagination
        paginator = TaskRequestPagination()
        paginated_users = paginator.paginate_queryset(task_requests, request)

        # Serialize the paginated data
        serializer = TaskRequestSerializer(paginated_users, many=True)
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


class TaskRequestGetView(APIView):

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(response=TaskRequestGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific TaskRequest by ID"
    )
    @role_decorator
    def post(self, request):
        task_request_id = request.data.get('id', 0)
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
                "propertyName": "code",
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
                        "value": "کد تسک : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "pre_tasks",
                "propertyType": "System.Collections.Generic.List`1[System.String]",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "taskManager/TaskRequestList/",
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
                        "value": " تسک های پیش نیاز ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "file",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "fkUrl": "fileManager/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "",
                "fkMultiple": False,
                "isFile": True,
                "fileTypes": [],
                "fileUrl": "/",
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
                        "value": " فایل ",
                        "message": None
                    },
                    {
                        "type": "MaxLengthAttribute",
                        "value": "1000",
                        "message": "len of {0} cant more {1} character"
                    }
                ]
            },
            {
                "order": 1018,
                "propertyName": "is_scheduled",
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
                        "value": "زمان دارد/ندارد",
                        "message": None
                    }
                ]
            },
            {
                "order": 1018,
                "propertyName": "requires_sms",
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
                        "value": "نیاز به پیامک دارد/ندارد",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "deadline",
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
                        "value": "زمان تحویل",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "priority",
                "propertyType": "StructureAndDataBase.Datas.Models.Base.MenuEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": " اولویت بالا (High Priority)",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "اولویت متوسط (Medium Priority)",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": "اولویت پایین (Low Priority)",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": "بدون اولویت (No Priority)",
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
                        "value": " الویت ",
                        "message": None
                    }
                ]
            },
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
                "propertyName": "description",
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
                "isEditor": True,
                "editorType": "full",
                "isLocation": False,
                "isList": False,
                "listProperty": [],
                "listError": [],
                "locationType": None,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "توضیحات",
                        "message": None
                    },
                ]
            },
            {
                "order": 1000,
                "propertyName": "todo_users",
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
                        "value": " افراد موظف ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "task_project",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/taskManager/TaskProjectList/",
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
                        "value": "پروژه مربوطه",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "status",
                "propertyType": "StructureAndDataBase.Datas.Models.Construction.BaseStatusEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": "آماده شروع",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "در حال انجام",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": "در انتظار بازدید",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": "در دست اسقرار",
                        "count": 0
                    },
                    {
                        "value": 5,
                        "label": "انجام شده",
                        "count": 0
                    },
                    {
                        "value": 6,
                        "label": "بسته شده",
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
        if task_request_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not task_request_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_request = TaskRequest.objects.get(id=task_request_id)
        except TaskRequest.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskRequestSerializer(task_request)

        # Prepare the response structure with manual property attribute definitions for TaskRequest fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class TaskRequestDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific TaskRequest by ID"
    )
    @role_decorator
    def post(self, request):
        task_request_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not task_request_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_request = TaskRequest.objects.get(id=task_request_id)
        except TaskRequest.DoesNotExist:
            return Response({"message": "درخواست تسک یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if task_request.is_deleted:
                return Response({"message": "درخواست تسک از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            task_request.is_deleted = True
            task_request.save()
            return Response({"message": "درخواست تسک به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if task_request.is_deleted:
                return Response({"message": "درخواست تسک از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            if task_request.photo:
                task_request.photo.is_deleted = True
                task_request.photo.save()

            if task_request.content:
                task_request.content.is_deleted = True
                task_request.content.save()

            if task_request.content_category:
                task_request.content_category.is_deleted = True
                task_request.content_category.save()

            # Soft delete the cms itself
            task_request.is_deleted = True
            task_request.save()

            # Add any other related models here

            return Response({"message": "درخواست تسک و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                task_request.delete()
                return Response({"message": "درخواست تسک به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # Manually delete the associated photo, content, and category if they exist
                if task_request.photo:
                    task_request.photo.delete()

                if task_request.content:
                    task_request.content.delete()

                if task_request.content_category:
                    task_request.content_category.delete()

                # Finally, delete the cms itself
                task_request.delete()
                return Response({"message": "درخواست تسک و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class TaskRequestUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted TaskRequest by ID"
    )
    @role_decorator
    def post(self, request):
        task_request_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not task_request_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_request = TaskRequest.objects.get(id=task_request_id)
        except TaskRequest.DoesNotExist:
            return Response({"message": "درخواست تسک یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if task_request.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                task_request.is_deleted = False
                task_request.save()
                return Response({"message": "درخواست تسک به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:

                if task_request.photo:
                    task_request.photo.is_deleted = False
                    task_request.photo.save()

                if task_request.content:
                    task_request.content.is_deleted = False
                    task_request.content.save()

                if task_request.content_category:
                    task_request.content_category.is_deleted = False
                    task_request.content_category.save()

                # Soft delete the cms itself
                task_request.is_deleted = False
                task_request.save()

                # Add any other related models here

                return Response({"message": "درخواست تسک و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "درخواست تسک مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)


class MyTasksGetView(APIView):
    @extend_schema(
        request=TaskProjectIdSerializer,
        responses={200: OpenApiResponse(response=TaskRequestListSerializer)},
        description="Retrieve TaskRequests by task_project ID or return all tasks assigned to the authenticated user"
    )
    def post(self, request):
        task_id = request.data.get('id')
        user = request.user

        # Ensure user is authenticated
        if user.is_anonymous:
            return Response({"message": "کاربر نامعتبر."}, status=status.HTTP_400_BAD_REQUEST)

        # If task_id is provided, filter by project ID
        if task_id:
            try:
                project = TaskProject.objects.get(id=task_id, is_deleted=False)
            except TaskProject.DoesNotExist:
                return Response({"message": "پروژه پیدا نشد."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the user is a project manager
            if user.id in project.project_managers:
                my_tasks = TaskRequest.objects.filter(task_project=project, is_deleted=False)
            else:
                # Only return tasks where the user is in todo_users
                my_tasks = TaskRequest.objects.filter(
                    task_project=project,
                    todo_users__contains=user.id,
                    is_deleted=False
                )
        else:
            # If no project ID is provided, return all tasks assigned to the user
            my_tasks = TaskRequest.objects.filter(todo_users__contains=user.id, is_deleted=False)

        # If no tasks are found, return a 404 error
        if not my_tasks.exists():
            return Response({"message": "هیچ تسکی برای این کاربر وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        # Apply pagination similar to TaskRequestNoteListView
        paginator = TaskRequestPagination()
        paginated_tasks = paginator.paginate_queryset(my_tasks, request)
        serializer = TaskRequestSerializer(paginated_tasks, many=True)

        # Return the paginated response with serialized data
        return paginator.get_paginated_response(serializer.data)

class TaskRequestNoteListView(APIView):
    @extend_schema(
        request=IdSerializer,
        responses={200: OpenApiResponse(response={'note_list': 'array'})},
        description="Retrieve the note_list of a specific TaskRequest by ID"
    )
    def post(self, request):
        task_request_id = request.data.get('id')

        if not task_request_id:
            return Response({"message": "شناسه تسک مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_request = TaskRequest.objects.get(id=task_request_id, is_deleted=False)
        except TaskRequest.DoesNotExist:
            return Response({"message": "تسک پیدا نشد."}, status=status.HTTP_400_BAD_REQUEST)

        # مقدار note_list را مستقیم برگردانیم
        return Response(task_request.note_list, status=status.HTTP_200_OK)