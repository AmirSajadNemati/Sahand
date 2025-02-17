from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Topic
from cms.serializers import TopicGetSerializer, TopicSerializer, TopicListSerializer
from serializers import DeleteSerializer, MessageAndIdSerializer, IdSerializer, ListRequestSerializer
from utils import get_property_type, create_property_attribute, role_decorator


class TopicAddOrUpdateView(APIView):

    @extend_schema(
        request=TopicSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update Topic"
    )
    @role_decorator
    def post(self, request):
        topic_id = request.data.get('id', 0)

        # If topic_id is 0, it's a new topic, so create it
        if topic_id == 0:
            serializer = TopicSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "موضوع با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If topic_id is provided, try to update the existing topic
        try:
            topic = Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            return Response({'message': 'موضوع مورد نظر برای تغییر یافت نشد.', "id": topic_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing topic
        serializer = TopicSerializer(topic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "موضوع با موفقیت به روزرسانی شد!", "id": topic_id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class TopicGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=TopicListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of Topics"
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

        topics = Topic.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            topics = topics.order_by(sort_field)
        else:
            topics = topics.order_by('id')

        # Pagination
        paginator = TopicPagination()
        paginated_topics = paginator.paginate_queryset(topics, request)

        # Serialize the paginated data
        serializer = TopicSerializer(paginated_topics, many=True)

        # Return paginated response
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


class TopicGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=TopicGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Topic by ID"
    )
    @role_decorator
    def post(self, request):
        topic_id = request.data.get('id', 0)
        properties_attribute = [
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
                "propertyName": "Is_user",
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
                        "value": " ایجاد شده توسط کاربر ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "is_verify",
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
                        "value": " تاییدیه ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "content_category",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/cms/ContentCategoryList/",
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
                        "value": "دسته بندی",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "ContentCategoryData",
                "propertyType": "StructureAndDataBase.Datas.ViewModels.Cms.ContentCategoryViewModel",
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
                        "value": " تیتر صفحه ",
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
                "propertyName": "Abstract",
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
                        "value": "خلاصه",
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
                "propertyName": "last_update_date",
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
                        "value": "تاریخ به روز رسانی",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Photo",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "",
                "fkMultiple": False,
                "isFile": True,
                "fileTypes": [
                    {
                        "value": 3,
                        "label": "Photo",
                        "extension": "*.png|*.jpg|*.jpeg"
                    }
                ],
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
                        "value": "عکس",
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
        if topic_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)
        if not topic_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"message": "موضوع یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TopicGetSerializer(topic)

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute  # Add your properties_attribute here if necessary
        }

        return Response(response_data, status=status.HTTP_200_OK)


class TopicDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Topic by ID"
    )
    @role_decorator
    def post(self, request):
        topic_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not topic_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"message": "موضوع یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete
            if topic.is_deleted:
                return Response({"message": "موضوع از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            topic.is_deleted = True
            topic.save()
            return Response({"message": "موضوع به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete with dependencies (photo, etc.)
            if topic.is_deleted:
                return Response({"message": "موضوع از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            if topic.photo:
                topic.photo.is_deleted = True
                topic.photo.save()

            topic.is_deleted = True
            topic.save()
            return Response({"message": "موضوع و عکس آن به صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete
            try:
                topic.delete()
                return Response({"message": "موضوع به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if topic.photo:
                    topic.photo.delete()

                topic.delete()
                return Response({"message": "موضوع و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نامعتبر."}, status=status.HTTP_400_BAD_REQUEST)


class TopicUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Topic by ID"
    )
    @role_decorator
    def post(self, request):
        topic_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not topic_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"message": "موضوع یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if topic.is_deleted:
            if delete_type == 1:
                topic.is_deleted = False
                topic.save()
                return Response({"message": "موضوع به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)

            elif delete_type == 2:
                if topic.photo:
                    topic.photo.is_deleted = False
                    topic.photo.save()

                topic.is_deleted = False
                topic.save()
                return Response({"message": "موضوع و عکس آن به صورت نرم بازیابی شدند."}, status=status.HTTP_200_OK)

            else:
                return Response({"message": "نوع بازیابی نامعتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "موضوع مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
