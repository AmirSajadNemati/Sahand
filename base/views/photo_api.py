from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Photo
from base.serializers import PhotoSerializer, PhotoListSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination

from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import role_decorator


class PhotoAddOrUpdateView(APIView):

    @extend_schema(
        request=PhotoSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update Photo"
    )
    @role_decorator
    def post(self, request):
        photo_id = request.data.get('id', 0)

        # If photo_id is 0, it's a new page, so create it
        if photo_id == 0:
            serializer = PhotoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "صفحه با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If photo_id is provided, try to update the existing page
        try:
            photo = Photo.objects.get(pk=photo_id)
        except Photo.DoesNotExist:
            return Response({'message': 'صفحه مورد نظر برای تغییر یافت نشد.', "id": photo_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = PhotoSerializer(photo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "صفحه با موفقیت به روزرسانی شد!", "id": photo_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class PhotoGetListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=PhotoListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of Photos"
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

        photos = Photo.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            photos = photos.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            photos = photos.order_by('id')  # or any field you prefer

        # Pagination
        paginator = PhotoPagination()
        paginated_photos = paginator.paginate_queryset(photos, request)

        # Serialize the paginated data
        # Serialize the paginated data
        serialized_data = PhotoSerializer(paginated_photos, many=True).data  # Correct serialization

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

        # **Error Location (Original Code)**:
        # Returning `serializer.data` directly here would be incorrect as it's expecting
        # a dictionary containing `count`, `next`, `previous`, and `data`.

        # **Change**:
        # We manually construct the `response_data` dictionary to include the correct structure:
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'data': serialized_data,  # Instead of `serializer.data`
            'propertiesAttribute': properties_attribute
        }

        # Return custom paginated response
        return Response(response_data, status=status.HTTP_200_OK)


class PhotoGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=PhotoSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Base Page by ID"
    )
    @role_decorator
    def post(self, request):
        photo_id = request.data.get('id', 0)
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
                "isRoleTree": False,
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
                        "message": "مقدار {0} نمی تواند بیشتر از {1} کاراکتر باشد"
                    },
                    {
                        "type": "RequiredAttribute",
                        "value": "",
                        "message": "ورود {0} الزامی می باشد"
                    }
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
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
                "isRoleTree": False,
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
                        "value": " آدرس صفحه ",
                        "message": None
                    },
                    {
                        "type": "RequiredAttribute",
                        "value": "",
                        "message": "ورود {0}الزامی است"
                    },
                    {
                        "type": "MaxLengthAttribute",
                        "value": "300",
                        "message": "مقدار {0} نمی تواند بیشتر از {1} کاراکتر باشد"
                    }
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
            },
            {
                "order": 1000,
                "propertyName": "file",
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
                        "value": " تصویر ",
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
                "propertyName": "photo_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Base.PartPhotoEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": " اسلایدر ",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": " اسلایدر موبایل ",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": " تبلیغات مربعی ",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": " تبلیغات عریض ",
                        "count": 0
                    },
                    {
                        "value": 5,
                        "label": " تبلیغات بزرگ ",
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
                "isRoleTree": False,
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
                        "value": " نوع تصویر ",
                        "message": None
                    }
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
            },
            {
                "order": 1000,
                "propertyName": "PartPhotoTypeValue",
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
                "isRoleTree": False,
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
                "attribute": [],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
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
                "isRoleTree": False,
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
                        "value": "وضعیت کل : ",
                        "message": None
                    }
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
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
                "isRoleTree": False,
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
                "attribute": [],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
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
                "isRoleTree": False,
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
                "attribute": [],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
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
                "isRoleTree": False,
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
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
            },
            {
                "order": 1000,
                "propertyName": "Is_deleted",
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
                "isRoleTree": False,
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
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
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
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": True,
                "dateType": "",
                "isDate": False,
                "isColor": False,
                "isRoleTree": False,
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
                        "value": "تاریخ ساخت : ",
                        "message": None
                    }
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
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
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": True,
                "dateType": "",
                "isDate": False,
                "isColor": False,
                "isRoleTree": False,
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
                        "value": "تاریخ ویرایش : ",
                        "message": None
                    }
                ],
                "hasTab": False,
                "hasGroup": False,
                "tab": None,
                "group": None
            }
        ]
        if photo_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not photo_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PhotoSerializer(photo)

        # Prepare the response structure with property attributes for Photo fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PhotoDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Photo by ID"
    )
    @role_decorator
    def post(self, request):
        photo_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not photo_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return Response({"message": "عکس/اسلایدر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if photo.is_deleted:
                return Response({"message": "عکس/اسلایدر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            photo.is_deleted = True
            photo.save()
            return Response({"message": "عکس/اسلایدر به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete related content if it exists
            if photo.is_deleted:
                return Response({"message": "عکس/اسلایدر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)

            if photo.content:
                photo.content.is_deleted = True
                photo.content.save()

            # Soft delete the base page itself
            photo.is_deleted = True
            photo.save()

            return Response({"message": "عکس/اسلایدر و محتوا به صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                photo.delete()
                return Response({"message": "عکس/اسلایدر به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if photo.content:
                    photo.content.delete()

                # Finally, delete the base page itself
                photo.delete()
                return Response({"message": "عکس/اسلایدر و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class PhotoUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Photo by ID"
    )
    @role_decorator
    def post(self, request):
        photo_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not photo_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return Response({"message": "عکس/اسلایدر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if photo.is_deleted:
            # If the base page is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                photo.is_deleted = False
                photo.save()
                return Response({"message": "عکس/اسلایدر به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if photo.content:
                    photo.content.is_deleted = False
                    photo.content.save()

                # Restore the base page itself
                photo.is_deleted = False
                photo.save()

                return Response({"message": "عکس/اسلایدر و محتوا به صورت نرم بازیابی شدند."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the base page was not soft-deleted
            return Response({"message": "عکس/اسلایدر مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
