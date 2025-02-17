from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import HelpCategory
from base.serializers import HelpCategorySerializer, HelpCategoryListSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination

from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import create_property_attribute, role_decorator


class HelpCategoryAddOrUpdateView(APIView):

    @extend_schema(
        request=HelpCategorySerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update HelpCategory"
    )
    @role_decorator
    def post(self, request):
        help_category_id = request.data.get('id', 0)

        # If help_category_id is 0, it's a new page, so create it
        if help_category_id == 0:
            serializer = HelpCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "دسته بندی کمک با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If help_category_id is provided, try to update the existing page
        try:
            help_category = HelpCategory.objects.get(pk=help_category_id)
        except HelpCategory.DoesNotExist:
            return Response({'message': 'دسته بندی کمک مورد نظر برای تغییر یافت نشد.', "id": help_category_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = HelpCategorySerializer(help_category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "دسته بندی کمک با موفقیت به روزرسانی شد!", "id": help_category_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HelpCategoryPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class HelpCategoryGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=HelpCategoryListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of HelpCategorys"
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

        help_categorys = HelpCategory.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            help_categorys = help_categorys.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            help_categorys = help_categorys.order_by('id')  # or any field you prefer

        # Pagination
        paginator = HelpCategoryPagination()
        paginated_help_categorys = paginator.paginate_queryset(help_categorys, request)

        # Serialize the paginated data
        serializer = HelpCategorySerializer(paginated_help_categorys, many=True)

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


class HelpCategoryGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=HelpCategorySerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Base Page by ID"
    )
    @role_decorator
    def post(self, request):
        help_category_id = request.data.get('id', 0)
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
                        "value": "250",
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
                        "value": " عکس ",
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
        if help_category_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not help_category_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            help_category = HelpCategory.objects.get(id=help_category_id)
        except HelpCategory.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HelpCategorySerializer(help_category)

        # Prepare the response structure with property attributes for HelpCategory fields
        properties_attribute = [
            create_property_attribute(
                order=0,
                property_name='id',
                property_type='AutoField',  # AutoField is used for the primary key
                enums_select=[],
                is_enum=False,
                is_enum_list=False,
                is_fk=False,
                fk_url="",
                fk_level=False,
                fk_level_end=True,
                fk_parent="",
                fk_show="",
                fk_multiple=False,
                is_file=False,
                file_types=[],
                file_url="",
                file_multiple=False,
                is_read_only=True,
                is_not_show=False,
                is_hidden=True,
                date_type="",
                is_date=False,
                is_color=False,
                is_price=False,
                price_type=None,
                is_tag=False,
                is_editor=False,
                editor_type=None,
                is_location=False,
                is_list=False,
                list_property=[],
                list_error=[],
                location_type=None,
                display_name="شناسه"  # ID in Persian
            ),
            create_property_attribute(
                order=1,
                property_name='title',
                property_type='CharField',
                enums_select=[],
                is_enum=False,
                is_enum_list=False,
                is_fk=False,
                fk_url="",
                fk_level=False,
                fk_level_end=False,
                fk_parent="",
                fk_show="",
                fk_multiple=False,
                is_file=False,
                file_types=[],
                file_url="",
                file_multiple=False,
                is_read_only=False,
                is_not_show=False,
                is_hidden=False,
                date_type="",
                is_date=False,
                is_color=False,
                is_price=False,
                price_type=None,
                is_tag=False,
                is_editor=False,
                editor_type=None,
                is_location=False,
                is_list=False,
                list_property=[],
                list_error=[],
                location_type=None,
                display_name="عنوان"  # Title in Persian
            ),
            create_property_attribute(
                order=2,
                property_name='photo',
                property_type='ForeignKey',
                enums_select=[],
                is_enum=False,
                is_enum_list=False,
                is_fk=True,
                fk_url="file_manager.FileManager",
                fk_level=False,
                fk_level_end=True,
                fk_parent="",
                fk_show="",
                fk_multiple=False,
                is_file=False,
                file_types=[],
                file_url="",
                file_multiple=False,
                is_read_only=False,
                is_not_show=False,
                is_hidden=False,
                date_type="",
                is_date=False,
                is_color=False,
                is_price=False,
                price_type=None,
                is_tag=False,
                is_editor=False,
                editor_type=None,
                is_location=False,
                is_list=False,
                list_property=[],
                list_error=[],
                location_type=None,
                display_name="عکس"  # Photo in Persian
            ),
            create_property_attribute(
                order=3,
                property_name='create_row_date',
                property_type='DateTimeField',
                enums_select=[],
                is_enum=False,
                is_enum_list=False,
                is_fk=False,
                fk_url="",
                fk_level=False,
                fk_level_end=False,
                fk_parent="",
                fk_show="",
                fk_multiple=False,
                is_file=False,
                file_types=[],
                file_url="",
                file_multiple=False,
                is_read_only=True,
                is_not_show=False,
                is_hidden=False,
                date_type="datetime",
                is_date=True,
                is_color=False,
                is_price=False,
                price_type=None,
                is_tag=False,
                is_editor=False,
                editor_type=None,
                is_location=False,
                is_list=False,
                list_property=[],
                list_error=[],
                location_type=None,
                display_name="تاریخ ایجاد"  # Create Row Date in Persian
            ),
            create_property_attribute(
                order=4,
                property_name='update_row_date',
                property_type='DateTimeField',
                enums_select=[],
                is_enum=False,
                is_enum_list=False,
                is_fk=False,
                fk_url="",
                fk_level=False,
                fk_level_end=False,
                fk_parent="",
                fk_show="",
                fk_multiple=False,
                is_file=False,
                file_types=[],
                file_url="",
                file_multiple=False,
                is_read_only=True,
                is_not_show=False,
                is_hidden=False,
                date_type="datetime",
                is_date=True,
                is_color=False,
                is_price=False,
                price_type=None,
                is_tag=False,
                is_editor=False,
                editor_type=None,
                is_location=False,
                is_list=False,
                list_property=[],
                list_error=[],
                location_type=None,
                display_name="تاریخ بروزرسانی"  # Update Row Date in Persian
            ),
            create_property_attribute(
                order=5,
                property_name='is_deleted',
                property_type='BooleanField',
                enums_select=[],
                is_enum=False,
                is_enum_list=False,
                is_fk=False,
                fk_url="",
                fk_level=False,
                fk_level_end=False,
                fk_parent="",
                fk_show="",
                fk_multiple=False,
                is_file=False,
                file_types=[],
                file_url="",
                file_multiple=False,
                is_read_only=False,
                is_not_show=False,
                is_hidden=False,
                date_type="",
                is_date=False,
                is_color=False,
                is_price=False,
                price_type=None,
                is_tag=False,
                is_editor=False,
                editor_type=None,
                is_location=False,
                is_list=False,
                list_property=[],
                list_error=[],
                location_type=None,
                display_name="حذف شده"  # Is Deleted in Persian
            ),
            create_property_attribute(
                order=6,
                property_name='status',
                property_type='IntegerField',
                enums_select=[],
                is_enum=False,
                is_enum_list=False,
                is_fk=False,
                fk_url="",
                fk_level=False,
                fk_level_end=False,
                fk_parent="",
                fk_show="",
                fk_multiple=False,
                is_file=False,
                file_types=[],
                file_url="",
                file_multiple=False,
                is_read_only=False,
                is_not_show=False,
                is_hidden=False,
                date_type="",
                is_date=False,
                is_color=False,
                is_price=False,
                price_type=None,
                is_tag=False,
                is_editor=False,
                editor_type=None,
                is_location=False,
                is_list=False,
                list_property=[],
                list_error=[],
                location_type=None,
                display_name="وضعیت"  # Status in Persian
            )
        ]

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class HelpCategoryDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific HelpCategory by ID"
    )
    @role_decorator
    def post(self, request):
        help_category_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not help_category_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            help_category = HelpCategory.objects.get(id=help_category_id)
        except HelpCategory.DoesNotExist:
            return Response({"message": "دسته بندی کمک یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if help_category.is_deleted:
                return Response({"message": "دسته بندی کمک از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            help_category.is_deleted = True
            help_category.save()
            return Response({"message": "دسته بندی کمک به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete related content if it exists
            if help_category.is_deleted:
                return Response({"message": "دسته بندی کمک از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)

            if help_category.content:
                help_category.content.is_deleted = True
                help_category.content.save()

            # Soft delete the base page itself
            help_category.is_deleted = True
            help_category.save()

            return Response({"message": "دسته بندی کمک و وابستگی های آن صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                help_category.delete()
                return Response({"message": "دسته بندی کمک  به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if help_category.content:
                    help_category.content.delete()

                # Finally, delete the base page itself
                help_category.delete()
                return Response({"message": "دسته بندی کمک و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class HelpCategoryUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted HelpCategory by ID"
    )
    @role_decorator
    def post(self, request):
        help_category_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not help_category_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            help_category = HelpCategory.objects.get(id=help_category_id)
        except HelpCategory.DoesNotExist:
            return Response({"message": "دسته بندی کمک یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if help_category.is_deleted:
            # If the base page is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                help_category.is_deleted = False
                help_category.save()
                return Response({"message": "دسته بندی کمک به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if help_category.content:
                    help_category.content.is_deleted = False
                    help_category.content.save()

                # Restore the base page itself
                help_category.is_deleted = False
                help_category.save()

                return Response({"message": "دسته بندی کمک و وابستگی های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the base page was not soft-deleted
            return Response({"message": "دسته بندی کمک مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
