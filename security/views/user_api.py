from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from security.models import User
from serializers import MessageAndIdSerializer, DeleteSerializer, ListRequestSerializer, IdSerializer
from security.serializers import UserSerializer, UserListSerializer, UserGetSerializer
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse

from utils import create_property_attribute, role_decorator


class UserAddOrUpdateView(APIView):

    @extend_schema(
        request=UserSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Add or Update User"
    )
    @role_decorator
    def post(self, request):
        user_id = request.data.get('id', 0)

        # Create new user if ID is 0
        if user_id == 0:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "کاربر با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update an existing user
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'کاربر مورد کاربر یافت نشد.', "id": user_id},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کاربر با موفقیت به روزرسانی شد!", "id": user_id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class UserGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={200: OpenApiResponse(response=UserListSerializer())},
        description="Get List of Users"
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

        users = User.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            users = users.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            users = users.order_by('id')  # or any field you prefer

        # Pagination
        paginator = UserPagination()
        paginated_users = paginator.paginate_queryset(users, request)

        # Serialize the paginated data
        serializer = UserSerializer(paginated_users, many=True)
        data = paginator.get_paginated_response(serializer.data)

        # Define the propertiesAttribute for the User model
        properties_attribute = {
            "propertyName": "User Text",
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
            "propertyPersianName": "متن کاربر",
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


class UserGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=UserGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific User by ID",

    )
    @role_decorator
    def post(self, request):
        user_id = request.data.get('id', 0)
        properties_attribute = [
            {
                "order": 1000,
                "propertyName": "create_row_date",
                "propertyType": "System.DateTime",
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
                "isReadOnly": True,
                "isNotShow": False,
                "isHidden": True,
                "dateType": "",
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
                        "value": "تاریخ ایجاد",
                        "message": None
                    }
                ]
            },
            {
                "order": 1001,
                "propertyName": "update_row_date",
                "propertyType": "System.DateTime",
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
                "isReadOnly": True,
                "isNotShow": False,
                "isHidden": True,
                "dateType": "",
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
                        "value": "تاریخ به روزرسانی",
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
                    },
                    {
                        "value": 2,
                        "label": "معلق",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "در انتظار تایید",
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
                        "value": "Id : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "about",
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
                        "value": "درباره کاربر",
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
                "order": 1006,
                "propertyName": "phone_number",
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
                        "value": "شماره همراه",
                        "message": None
                    }
                ]
            },
            {
                "order": 1007,
                "propertyName": "sex",
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
                        "value": "جنسیت",
                        "message": None
                    }
                ]
            },
            {
                "order": 1008,
                "propertyName": "full_name",
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
                        "value": "نام و نام خانوادگی",
                        "message": None
                    }
                ]
            },
            {
                "order": 1009,
                "propertyName": "password_text",
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
                        "value": "رمز عبور",
                        "message": None
                    }
                ]
            }, {
                "order": 1009,
                "propertyName": "username",
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
                        "value": "نام کاربری",
                        "message": None
                    }
                ]
            },
            # {
            #     "order": 1010,
            #     "propertyName": "phone_number_code",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "کد شماره همراه",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1011,
            #     "propertyName": "count_send_sms",
            #     "propertyType": "System.Int32",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "پیامک های ارسال شده",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1012,
            #     "propertyName": "last_send_sms",
            #     "propertyType": "System.DateTime",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": True,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "آخرین پیامک ارسال شده",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1013,
            #     "propertyName": "telephone",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "تلفن",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1014,
            #     "propertyName": "job",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "شغل",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1015,
            #     "propertyName": "access_failed_count",
            #     "propertyType": "System.Int32",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "دسترسی های ناموفق",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1016,
            #     "propertyName": "education",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "تحصیلات",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1000,
            #     "propertyName": "birth_date",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "date",
            #     "isDate": True,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "تاریخ تولد",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1018,
            #     "propertyName": "has_login",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "لاگین شده/نشده",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1019,
            #     "propertyName": "balance",
            #     "propertyType": "System.Int64",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "موجودی",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1020,
            #     "propertyName": "invited_user",
            #     "propertyType": "System.Int64",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": True,
            #     "fkUrl": "/security/UserList/",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "UserData.FullName",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "کاربرهای دعوت شده",
            #             "message": None
            #         }
            #     ]
            # },
            {
                "order": 1021,
                "propertyName": "photo",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "FileManager.Title",
                "fkMultiple": False,
                "isFile": True,
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
                        "value": "عکس",
                        "message": None
                    }
                ]
            },
            # {
            #     "order": 1022,
            #     "propertyName": "email_confirmed",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "تایید ایمیل",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1023,
            #     "propertyName": "phone_number_confirmed",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "تایید شماره همراه",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1024,
            #     "propertyName": "two_factor_enabled",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "احراز هویت دو مرحله ای",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1025,
            #     "propertyName": "lockout_end",
            #     "propertyType": "System.DateTime",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": True,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "پایان قفل",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1026,
            #     "propertyName": "lockout_enabled",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "وضعیت قفل",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1027,
            #     "propertyName": "postal_code",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "کد پستی",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1028,
            #     "propertyName": "address",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "آدرس",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1029,
            #     "propertyName": "is_developer",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "توسعه دهنده",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1030,
            #     "propertyName": "is_consult",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "مشاور",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1031,
            #     "propertyName": "is_support",
            #     "propertyType": "System.Boolean",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "پشتیبان",
            #             "message": None
            #         }
            #     ]
            # },
            # {
            #     "order": 1032,
            #     "propertyName": "url_name",
            #     "propertyType": "System.String",
            #     "enumsSelect": [],
            #     "isEnum": False,
            #     "isEnumList": False,
            #     "isFK": False,
            #     "fkUrl": "",
            #     "fknLevel": False,
            #     "fkLevelEnd": True,
            #     "fkParent": "",
            #     "fkShow": "",
            #     "fkMultiple": False,
            #     "isFile": False,
            #     "fileTypes": [],
            #     "fileUrl": "",
            #     "fileMultiple": False,
            #     "isReadOnly": False,
            #     "isNotShow": False,
            #     "isHidden": False,
            #     "dateType": "",
            #     "isDate": False,
            #     "isColor": False,
            #     "isPrice": False,
            #     "priceType": None,
            #     "isTag": False,
            #     "isEditor": False,
            #     "editorType": None,
            #     "isLocation": False,
            #     "isList": False,
            #     "listProperty": [],
            #     "listError": [],
            #     "locationType": None,
            #     "attribute": [
            #         {
            #             "type": "DisplayAttribute",
            #             "value": "آدرس url",
            #             "message": None
            #         }
            #     ]
            # },
            {
                "order": 1000,
                "propertyName": "roles",
                "propertyType": "System.Collections.Generic.List`1[System.String]",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "security/RoleList/",
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
                        "value": " نقش ها ",
                        "message": None
                    }
                ]
            },
        ]

        if user_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)
        if not user_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)

        # Prepare the response structure with manual property attribute definitions for User fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UserDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific User by ID"
    )
    @role_decorator
    def post(self, request):
        user_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not user_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "کاربر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if user.is_deleted:
                return Response({"message": "کاربر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            user.is_deleted = True
            user.save()
            return Response({"message": "کاربر به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if user.is_deleted:
                return Response({"message": "کاربر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            # if user.photo:
            #     user.photo.is_deleted = True
            #     user.photo.save()

            user.is_deleted = True
            user.save()

            # Add any other related models here

            return Response({"message": "کاربر و تمام وابستگی‌های آن به صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                user.delete()
                return Response({"message": "کاربر به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # if user.photo:
                #     user.photo.delete()

                user.delete()
                return Response({"message": "کاربر و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class UserUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted User by ID"
    )
    @role_decorator
    def post(self, request):
        user_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not user_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "کاربر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                user.is_deleted = False
                user.save()
                return Response({"message": "کاربر به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                # Soft delete the cms itself
                user.is_deleted = False
                user.save()

                # Add any other related models here

                return Response({"message": "کاربر و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "کاربر مورد کاربر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
