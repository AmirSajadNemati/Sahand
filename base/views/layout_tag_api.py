from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import LayoutTag
from base.serializers import LayoutTagSerializer, LayoutTagListSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination

from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import create_property_attribute, role_decorator


class LayoutTagAddOrUpdateView(APIView):

    @extend_schema(
        request=LayoutTagSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update LayoutTag"
    )
    @role_decorator
    def post(self, request):
        layout_tag_id = request.data.get('id', 0)

        # If layout_tag_id is 0, it's a new page, so create it
        if layout_tag_id == 0:
            serializer = LayoutTagSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "برچسب طرح با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If layout_tag_id is provided, try to update the existing page
        try:
            layout_tag = LayoutTag.objects.get(pk=layout_tag_id)
        except LayoutTag.DoesNotExist:
            return Response({'message': 'برچسب طرح مورد نظر برای تغییر یافت نشد.', "id": layout_tag_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = LayoutTagSerializer(layout_tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "برچسب طرح با موفقیت به روزرسانی شد!", "id": layout_tag_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LayoutTagPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class LayoutTagGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=LayoutTagListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of LayoutTags"
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

        layout_tags = LayoutTag.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            layout_tags = layout_tags.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            layout_tags = layout_tags.order_by('id')  # or any field you prefer

        # Pagination
        paginator = LayoutTagPagination()
        paginated_layout_tags = paginator.paginate_queryset(layout_tags, request)

        # Serialize the paginated data
        serializer = LayoutTagSerializer(paginated_layout_tags, many=True)

        # Define properties attribute for Title only
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

        # Return custom paginated response
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'data': serializer.data,  # Instead of 'results', now 'data'
            'propertiesAttribute': properties_attribute  # Include properties attributes here
        }

        # Return custom paginated response
        return Response(response_data, status=status.HTTP_200_OK)


class LayoutTagGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=LayoutTagSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Base Page by ID"
    )
    @role_decorator
    def post(self, request):
        layout_tag_id = request.data.get('id', 0)
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
                        "value": " عنوان ",
                        "message": None
                    },
                    {
                        "type": "MaxLengthAttribute",
                        "value": "300",
                        "message": "len of {0} cant more {1} character"
                    },
                    {
                        "type": "RequiredAttribute",
                        "value": "",
                        "message": "ورود {0} الزامی می باشد"
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Value",
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
                        "value": " مقدار ",
                        "message": None
                    },
                    {
                        "type": "MaxLengthAttribute",
                        "value": "5000",
                        "message": "len of {0} cant more {1} character"
                    },
                    {
                        "type": "RequiredAttribute",
                        "value": "",
                        "message": "ورود {0} الزامی می باشد"
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Url",
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
                        "value": " URL سایت ",
                        "message": None
                    },
                    {
                        "type": "MaxLengthAttribute",
                        "value": "300",
                        "message": "len of {0} cant more {1} character"
                    },
                    {
                        "type": "RequiredAttribute",
                        "value": "",
                        "message": "ورود {0} الزامی می باشد"
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "layout_tag_status_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Base.LayoutTagStatusEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": " تگ های بالای هدر ",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": " تگ های پایین هدر ",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": " تگ های بالای بادی ",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": " تگ های پایین بادی ",
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
                        "value": " وضعیت تگ ها ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "LayoutTagStatusTypeValue",
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
                "propertyName": "layout_tag_location_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Base.LayoutTagLocationEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": " عمومی ",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": " صفحه خاص ",
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
                        "value": " موقعیت تگ ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "LayoutTagLocationTypeValue",
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
                        "value": "وضعیت حذف  : ",
                        "message": None
                    }
                ]
            }
        ]
        if layout_tag_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not layout_tag_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            layout_tag = LayoutTag.objects.get(id=layout_tag_id)
        except LayoutTag.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LayoutTagSerializer(layout_tag)

        # Prepare the response structure with property attributes for LayoutTag fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class LayoutTagDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific LayoutTag by ID"
    )
    @role_decorator
    def post(self, request):
        layout_tag_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not layout_tag_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            layout_tag = LayoutTag.objects.get(id=layout_tag_id)
        except LayoutTag.DoesNotExist:
            return Response({"message": "برچسب طرح یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if layout_tag.is_deleted:
                return Response({"message": "برچسب طرح از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            layout_tag.is_deleted = True
            layout_tag.save()
            return Response({"message": "برچسب طرح به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete related content if it exists
            if layout_tag.is_deleted:
                return Response({"message": "برچسب طرح از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)

            if layout_tag.content:
                layout_tag.content.is_deleted = True
                layout_tag.content.save()

            # Soft delete the base page itself
            layout_tag.is_deleted = True
            layout_tag.save()

            return Response({"message": "برچسب طرح و وابستگی های آن صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                layout_tag.delete()
                return Response({"message": "برچسب طرح  به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if layout_tag.content:
                    layout_tag.content.delete()

                # Finally, delete the base page itself
                layout_tag.delete()
                return Response({"message": "برچسب طرح و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class LayoutTagUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted LayoutTag by ID"
    )
    @role_decorator
    def post(self, request):
        layout_tag_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not layout_tag_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            layout_tag = LayoutTag.objects.get(id=layout_tag_id)
        except LayoutTag.DoesNotExist:
            return Response({"message": "برچسب طرح یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if layout_tag.is_deleted:
            # If the base page is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                layout_tag.is_deleted = False
                layout_tag.save()
                return Response({"message": "برچسب طرح به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if layout_tag.content:
                    layout_tag.content.is_deleted = False
                    layout_tag.content.save()

                # Restore the base page itself
                layout_tag.is_deleted = False
                layout_tag.save()

                return Response({"message": "برچسب طرح و وابستگی های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the base page was not soft-deleted
            return Response({"message": "برچسب طرح مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
