from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from cms.models import Gallery
from cms.serializers import GallerySerializer, GalleryListSerializer
from serializers import  ListRequestSerializer, IdSerializer, DeleteSerializer, MessageAndIdSerializer
from django.db.models import Q

from utils import role_decorator


class GalleryAddOrUpdateView(APIView):

    @extend_schema(
        request=GallerySerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Add or Update a Gallery"
    )
    @role_decorator
    def post(self, request):
        gallery_id = request.data.get('id', 0)

        # If gallery_id is 0, it's a new gallery, so create it
        if gallery_id == 0:
            serializer = GallerySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "گالری با موفقیت ایجاد شد!", "id": serializer.instance.id}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If gallery_id is provided, try to update the existing gallery
        try:
            gallery = Gallery.objects.get(pk=gallery_id)
        except Gallery.DoesNotExist:
            return Response({'message': 'گالری مورد نظر برای تغییر یافت نشد.', "id": gallery_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing gallery
        serializer = GallerySerializer(gallery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "گالری با موفقیت به روزرسانی شد!", "id": gallery_id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class GalleryGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={200: OpenApiResponse(response=GalleryListSerializer()), 400: OpenApiResponse(description='Bad Request')},
        description="Get List of Galleries"
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

        galleries = Gallery.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            galleries = galleries.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            galleries = galleries.order_by('id')

        # Pagination
        paginator = GalleryPagination()
        paginated_galleries = paginator.paginate_queryset(galleries, request)

        # Serialize the paginated data
        serializer = GallerySerializer(paginated_galleries, many=True)

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


class GalleryGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={200: OpenApiResponse(response=GallerySerializer), 400: OpenApiResponse(description='Not Found')},
        description="Get a specific Gallery by ID"
    )
    @role_decorator
    def post(self, request):
        gallery_id = request.data.get('id', 0)
        properties_attribute = [
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
      "propertyType": "StructureAndDataBase.Datas.ViewModels.cms.ContentCategoryViewModel",
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
          "value": " تیترصفحه ",
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
      "propertyType": "System.String",
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
      "propertyName": "large_photo",
      "propertyType": "System.String",
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
          "value": " عکس بزرگ ",
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
      "propertyName": "other_photos",
      "propertyType": "System.Collections.Generic.List`1[System.String]",
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
      "isFile": True,
      "fileTypes": [
        {
          "value": 3,
          "label": "Photo",
          "extension": "*.png|*.jpg|*.jpeg"
        }
      ],
      "fileUrl": "/",
      "fileMultiple": True,
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
          "value": " تصاویر دیگر ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "Tags",
      "propertyType": "System.Collections.Generic.List`1[System.String]",
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
      "isTag": True,
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
          "value": " تک ها ",
          "message": None
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
  ]
        if gallery_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not gallery_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GallerySerializer(gallery)

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute  # Add your properties_attribute here
        }

        return Response(response_data, status=status.HTTP_200_OK)


class GalleryDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the gallery
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Gallery by ID"
    )
    @role_decorator
    def post(self, request):
        gallery_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not gallery_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return Response({"message": "گالری یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if gallery.is_deleted:
                return Response({"message": "گالری از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            gallery.is_deleted = True
            gallery.save()
            return Response({"message": "گالری به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete the gallery and associated photo, large_photo, and other content
            if gallery.is_deleted:
                return Response({"message": "گالری از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)

            # Soft delete related files (photo, large_photo, etc.)
            if gallery.photo:
                gallery.photo.is_deleted = True
                gallery.photo.save()

            if gallery.large_photo:
                gallery.large_photo.is_deleted = True
                gallery.large_photo.save()

            # if gallery.other_photos.exists():
            #     for photo in gallery.other_photos.all():
            #         photo.is_deleted = True
            #         photo.save()

            # You can extend this to include other related entities
            gallery.is_deleted = True
            gallery.save()

            return Response({"message": "گالری و تمام وابستگی‌های آن به صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Completely remove the gallery from the database
            try:
                gallery.delete()
                return Response({"message": "گالری به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies (e.g., associated files like photo, large_photo)
            try:
                # if gallery.other_photos.exists():
                #     gallery.other_photos.clear()  # Unlink the many-to-many relationship
                #     gallery.delete()  # Hard delete the gallery object
                if gallery.photo:
                    gallery.photo.delete()

                if gallery.large_photo:
                    gallery.large_photo.delete()

                # Add logic for other related entities if necessary
                gallery.delete()
                return Response({"message": "گالری و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نامعتبر."}, status=status.HTTP_400_BAD_REQUEST)


class GalleryUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the gallery
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Gallery by ID"
    )
    @role_decorator
    def post(self, request):
        gallery_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not gallery_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return Response({"message": "گالری یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if gallery.is_deleted:
            if delete_type == 1:
                # Restore only the gallery (soft undelete)
                gallery.is_deleted = False
                gallery.save()
                return Response({"message": "گالری به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)

            elif delete_type == 2:
                # if gallery.other_photos.exists():
                #     for photo in gallery.other_photos.all():
                #         photo.is_deleted = False
                #         photo.save()
                if gallery.photo:
                    gallery.photo.is_deleted = False
                    gallery.photo.save()

                if gallery.large_photo:
                    gallery.large_photo.is_deleted = False
                    gallery.large_photo.save()

                # Add more logic for any other associated content if necessary
                gallery.is_deleted = False
                gallery.save()

                return Response({"message": "گالری و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نامعتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "گالری مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
