from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import SpecialGroupCategory
from base.serializers import SpecialGroupCategorySerializer, SpecialGroupCategoryListSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination

from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import create_property_attribute, role_decorator


class SpecialGroupCategoryAddOrUpdateView(APIView):

    @extend_schema(
        request=SpecialGroupCategorySerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update SpecialGroupCategory"
    )
    @role_decorator
    def post(self, request):
        special_group_category_id = request.data.get('id', 0)

        # If special_group_category_id is 0, it's a new page, so create it
        if special_group_category_id == 0:
            serializer = SpecialGroupCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "دسته بندی گروه مخصوص با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If special_group_category_id is provided, try to update the existing page
        try:
            special_group_category = SpecialGroupCategory.objects.get(pk=special_group_category_id)
        except SpecialGroupCategory.DoesNotExist:
            return Response(
                {'message': 'دسته بندی گروه مخصوص مورد نظر برای تغییر یافت نشد.', "id": special_group_category_id},
                status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = SpecialGroupCategorySerializer(special_group_category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "دسته بندی گروه مخصوص با موفقیت به روزرسانی شد!", "id": special_group_category_id},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialGroupCategoryPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class SpecialGroupCategoryGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=SpecialGroupCategoryListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of SpecialGroupCategorys"
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

        special_group_categorys = SpecialGroupCategory.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            special_group_categorys = special_group_categorys.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            special_group_categorys = special_group_categorys.order_by('id')  # or any field you prefer

        # Pagination
        paginator = SpecialGroupCategoryPagination()
        paginated_special_group_categorys = paginator.paginate_queryset(special_group_categorys, request)

        # Serialize the paginated data
        serializer = SpecialGroupCategorySerializer(paginated_special_group_categorys, many=True)

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


class SpecialGroupCategoryGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=SpecialGroupCategorySerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Base Page by ID"
    )
    @role_decorator
    def post(self, request):
        special_group_category_id = request.data.get('id', 0)
        properties_attribute = [
            {
                "order": 1000,
                "propertyName": "special_category",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/base/SpecialCategoryList/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "special_category_id",
                "fkShow": "title",
                "fkMultiple": False,
                "isFile": False,
                "fileTypes": [],
                "fileUrl": "",
                "fileMultiple": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": False,
                "isBlank": False,
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
                        "value": "دسته بندی ویژه",
                        "message": None
                    }
                ]
            },
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
                "isNull": True,
                "isBlank": True,
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
                        "value": "عنوان",
                        "message": None
                    },
                    {
                        "type": "MaxLengthAttribute",
                        "value": "250",
                        "message": "len of {0} can't be more than {1} characters"
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "photo",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/fileManager/FileManagerAddFile/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "photo",
                "fkShow": "photo",
                "fkMultiple": False,
                "isFile": True,
                "fileTypes": [],
                "fileUrl": "",
                "fileMultiple": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
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
                "isHidden": False,
                "isNull": False,
                "isBlank": False,
                "dateType": "DateTime",
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
                "order": 1000,
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
                "isHidden": False,
                "isNull": False,
                "isBlank": False,
                "dateType": "DateTime",
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
                "isNull": False,
                "isBlank": False,
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
                        "value": "وضعیت حذف",
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
        ]

        if special_group_category_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)
        if not special_group_category_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            special_group_category = SpecialGroupCategory.objects.get(id=special_group_category_id)
        except SpecialGroupCategory.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SpecialGroupCategorySerializer(special_group_category)

        # Prepare the response structure with property attributes for SpecialGroupCategory fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SpecialGroupCategoryDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific SpecialGroupCategory by ID"
    )
    @role_decorator
    def post(self, request):
        special_group_category_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not special_group_category_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            special_group_category = SpecialGroupCategory.objects.get(id=special_group_category_id)
        except SpecialGroupCategory.DoesNotExist:
            return Response({"message": "دسته بندی گروه مخصوص یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if special_group_category.is_deleted:
                return Response({"message": "دسته بندی گروه مخصوص از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            special_group_category.is_deleted = True
            special_group_category.save()
            return Response({"message": "دسته بندی گروه مخصوص به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete related content if it exists
            if special_group_category.is_deleted:
                return Response({"message": "دسته بندی گروه مخصوص از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)

            if special_group_category.content:
                special_group_category.content.is_deleted = True
                special_group_category.content.save()

            # Soft delete the base page itself
            special_group_category.is_deleted = True
            special_group_category.save()

            return Response({"message": "دسته بندی گروه مخصوص و وابستگی های آن صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                special_group_category.delete()
                return Response({"message": "دسته بندی گروه مخصوص  به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if special_group_category.content:
                    special_group_category.content.delete()

                # Finally, delete the base page itself
                special_group_category.delete()
                return Response({"message": "دسته بندی گروه مخصوص و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class SpecialGroupCategoryUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted SpecialGroupCategory by ID"
    )
    @role_decorator
    def post(self, request):
        special_group_category_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not special_group_category_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            special_group_category = SpecialGroupCategory.objects.get(id=special_group_category_id)
        except SpecialGroupCategory.DoesNotExist:
            return Response({"message": "دسته بندی گروه مخصوص یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if special_group_category.is_deleted:
            # If the base page is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                special_group_category.is_deleted = False
                special_group_category.save()
                return Response({"message": "دسته بندی گروه مخصوص به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if special_group_category.content:
                    special_group_category.content.is_deleted = False
                    special_group_category.content.save()

                # Restore the base page itself
                special_group_category.is_deleted = False
                special_group_category.save()

                return Response({"message": "دسته بندی گروه مخصوص و وابستگی های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the base page was not soft-deleted
            return Response({"message": "دسته بندی گروه مخصوص مورد نظر حذف نشده است."},
                            status=status.HTTP_400_BAD_REQUEST)
