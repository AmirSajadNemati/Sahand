from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContentManager
from .serializers import ContentManagerSerializer, ContentManagerListSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination

from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import create_property_attribute


class ContentManagerAddOrUpdateView(APIView):

    @extend_schema(
        request=ContentManagerSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update ContentManager"
    )
    def post(self, request):
        content_id = request.data.get('id', 0)

        # If content_id is 0, it's a new page, so create it
        if content_id == 0:
            serializer = ContentManagerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "محتوا با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If content_id is provided, try to update the existing page
        try:
            content = ContentManager.objects.get(pk=content_id)
        except ContentManager.DoesNotExist:
            return Response({'message': 'محتوا مورد نظر برای تغییر یافت نشد.', "id": content_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = ContentManagerSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "محتوا با موفقیت به روزرسانی شد!", "id": content_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentManagerPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class ContentManagerGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=ContentManagerListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of ContentManagers"
    )
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

        contents = ContentManager.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            contents = contents.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            contents = contents.order_by('id')  # or any field you prefer

        # Pagination
        paginator = ContentManagerPagination()
        paginated_contents = paginator.paginate_queryset(contents, request)

        # Serialize the paginated data
        serialized_data = ContentManagerSerializer(paginated_contents, many=True).data

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
            'data': serialized_data,  # Instead of 'results', now 'data'
            'propertiesAttribute': properties_attribute  # Include properties attributes here
        }

        # Return custom paginated response
        return Response(response_data, status=status.HTTP_200_OK)


class ContentManagerGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=ContentManagerSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Base Page by ID"
    )
    def post(self, request):
        content_id = request.data.get('id', 0)
        properties_attribute = [
            create_property_attribute(
                order=0,
                property_name='id',
                property_type='AutoField',
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
                property_name='content',
                property_type='TextField',
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
                display_name="Content"  # Field name in Persian or desired display name
            ),
            create_property_attribute(
                order=2,
                property_name='create_row_date',
                property_type='DateTimeField',
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
                is_hidden=False,
                date_type="",
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
                display_name="تاریخ ایجاد"  # Creation date in Persian
            ),
            create_property_attribute(
                order=3,
                property_name='update_row_date',
                property_type='DateTimeField',
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
                is_hidden=False,
                date_type="",
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
                display_name="تاریخ بروزرسانی"  # Update date in Persian
            ),
            create_property_attribute(
                order=4,
                property_name='is_deleted',
                property_type='BooleanField',
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
                display_name="حذف شده"  # Is deleted in Persian
            )
        ]
        if content_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not content_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = ContentManager.objects.get(id=content_id)
        except ContentManager.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ContentManagerSerializer(content)

        # Prepare the response structure with property attributes for ContentManager fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ContentManagerDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific ContentManager by ID"
    )
    def post(self, request):
        content_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not content_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = ContentManager.objects.get(id=content_id)
        except ContentManager.DoesNotExist:
            return Response({"message": "محتوا یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if content.is_deleted:
                return Response({"message": "محتوا از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            content.is_deleted = True
            content.save()
            return Response({"message": "محتوا به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete related content if it exists
            if content.is_deleted:
                return Response({"message": "محتوا از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)

            if content.content:
                content.content.is_deleted = True
                content.content.save()

            # Soft delete the base page itself
            content.is_deleted = True
            content.save()

            return Response({"message": "محتوا و وابستگی های آن صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                content.delete()
                return Response({"message": "محتوا  به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if content.content:
                    content.content.delete()

                # Finally, delete the base page itself
                content.delete()
                return Response({"message": "محتوا و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class ContentManagerUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted ContentManager by ID"
    )
    def post(self, request):
        content_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not content_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = ContentManager.objects.get(id=content_id)
        except ContentManager.DoesNotExist:
            return Response({"message": "محتوا یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if content.is_deleted:
            # If the base page is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                content.is_deleted = False
                content.save()
                return Response({"message": "محتوا به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if content.content:
                    content.content.is_deleted = False
                    content.content.save()

                # Restore the base page itself
                content.is_deleted = False
                content.save()

                return Response({"message": "محتوا و وابستگی های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the base page was not soft-deleted
            return Response({"message": "محتوا مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
