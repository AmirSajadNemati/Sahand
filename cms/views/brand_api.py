from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from serializers import MessageAndIdSerializer, ListRequestSerializer, DeleteSerializer, UrlSerializer
from cms.models import Brand
from cms.serializers import BrandSerializer, BrandGetSerializer, BrandListSerializer
from utils import role_decorator


class BrandAddOrUpdateView(APIView):

    @extend_schema(
        request=BrandSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update Brand"
    )
    @role_decorator
    def post(self, request):
        brand_id = request.data.get('id', 0)

        # If brand_id is 0, it's a new cms, so create it
        if brand_id == 0:
            serializer = BrandSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"brand": "برند با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If brand_id is provided, try to update the existing cms
        try:
            brand = Brand.objects.get(pk=brand_id)
        except Brand.DoesNotExist:
            return Response({'brand': 'برند مورد نظر برای تغییر یافت نشد.', "id": brand_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing cms
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"brand": "برند با موفقیت به روزرسانی شد!", "id": brand_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class BrandGetListView(APIView):
    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=BrandListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of Brands"
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

        brands = Brand.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            brands = brands.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            brands = brands.order_by('id')  # or any field you prefer

        # Pagination
        paginator = BrandPagination()
        paginated_users = paginator.paginate_queryset(brands, request)

        # Serialize the paginated data
        serializer = BrandSerializer(paginated_users, many=True)
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


class BrandGetView(APIView):

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(response=BrandGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Brand by ID"
    )
    @role_decorator
    def post(self, request):
        brand_id = request.data.get('id', 0)
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
                        "brand": None
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
                        "brand": None
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
                        "brand": None
                    }
                ]
            }
        ]
        if brand_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not brand_id:
            return Response({"brand": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response({"brand": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BrandSerializer(brand)

        # Prepare the response structure with manual property attribute definitions for Brand fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class BrandDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Brand by ID"
    )
    @role_decorator
    def post(self, request):
        brand_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not brand_id:
            return Response({"brand": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response({"brand": "برند یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if brand.is_deleted:
                return Response({"brand": "برند از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            brand.is_deleted = True
            brand.save()
            return Response({"brand": "برند به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if brand.is_deleted:
                return Response({"brand": "برند از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            if brand.photo:
                brand.photo.is_deleted = True
                brand.photo.save()

            if brand.content:
                brand.content.is_deleted = True
                brand.content.save()

            if brand.content_category:
                brand.content_category.is_deleted = True
                brand.content_category.save()

            # Soft delete the cms itself
            brand.is_deleted = True
            brand.save()

            # Add any other related models here

            return Response({"brand": "برند و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                brand.delete()
                return Response({"brand": "برند به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"brand": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # Manually delete the associated photo, content, and category if they exist
                if brand.photo:
                    brand.photo.delete()

                if brand.content:
                    brand.content.delete()

                if brand.content_category:
                    brand.content_category.delete()

                # Finally, delete the cms itself
                brand.delete()
                return Response({"brand": "برند و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"brand": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"brand": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class BrandUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Brand by ID"
    )
    @role_decorator
    def post(self, request):
        brand_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not brand_id:
            return Response({"brand": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response({"brand": "برند یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if brand.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                brand.is_deleted = False
                brand.save()
                return Response({"brand": "برند به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:

                if brand.photo:
                    brand.photo.is_deleted = False
                    brand.photo.save()

                if brand.content:
                    brand.content.is_deleted = False
                    brand.content.save()

                if brand.content_category:
                    brand.content_category.is_deleted = False
                    brand.content_category.save()

                # Soft delete the cms itself
                brand.is_deleted = False
                brand.save()

                # Add any other related models here

                return Response({"brand": "برند و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"brand": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"brand": "برند مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)

