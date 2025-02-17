from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Video
from cms.serializers import VideoSerializer, VideoGetSerializer, VideoListSerializer
from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import create_property_attribute, get_property_type, role_decorator


class VideoAddOrUpdateView(APIView):

    @extend_schema(
        request=VideoSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update Video"
    )
    @role_decorator
    def post(self, request):
        video_id = request.data.get('id', 0)

        if video_id == 0:
            serializer = VideoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "ویدیو با موفقیت ایجاد شد!", "id": serializer.instance.id}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({'message': 'ویدیوی مورد نظر برای تغییر یافت نشد.', "id": video_id}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ویدیو با موفقیت به روزرسانی شد!", "id": video_id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class VideoGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=VideoListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of Videos"
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

        query = Q(is_deleted=is_deleted)

        for filter_item in filters:
            column = filter_item['column']
            value = filter_item['value']
            query &= Q(**{f"{column}__iexact": value})

        for search_item in searches:
            column = search_item['column']
            value = search_item['value']
            query &= Q(**{f"{column}__icontains": value})

        videos = Video.objects.filter(query)

        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            videos = videos.order_by(sort_field)
        else:
            videos = videos.order_by('id')

        paginator = VideoPagination()
        paginated_videos = paginator.paginate_queryset(videos, request)

        serializer = VideoSerializer(paginated_videos, many=True)
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


class VideoGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=VideoGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Video by ID"
    )
    @role_decorator
    def post(self, request):
        video_id = request.data.get('id', 0)
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
      "propertyName": "photo",
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
      "propertyName": "video",
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
          "value": " فیلم ",
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
    }
  ]
        if video_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not video_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VideoSerializer(video)

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)

class VideoDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Video by ID"
    )
    @role_decorator
    def post(self, request):
        video_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not video_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"message": "ویدیو یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            if video.is_deleted:
                return Response({"message": "ویدیو از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            video.is_deleted = True
            video.save()
            return Response({"message": "ویدیو به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            if video.is_deleted:
                return Response({"message": "ویدیو از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            if video.photo:
                video.photo.is_deleted = True
                video.photo.save()

            if video.video_file:
                video.video_file.is_deleted = True
                video.video_file.save()

            video.is_deleted = True
            video.save()

            return Response({"message": "ویدیو و تمام وابستگی‌های آن به صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            try:
                video.delete()
                return Response({"message": "ویدیو به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            try:
                if video.photo:
                    video.photo.delete()
                if video.video_file:
                    video.video_file.delete()
                video.delete()
                return Response({"message": "ویدیو و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)

class VideoUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Video by ID"
    )
    @role_decorator
    def post(self, request):
        video_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not video_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"message": "ویدیو یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if video.is_deleted:
            if delete_type == 1:
                video.is_deleted = False
                video.save()
                return Response({"message": "ویدیو به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if video.photo:
                    video.photo.is_deleted = False
                    video.photo.save()
                if video.video_file:
                    video.video_file.is_deleted = False
                    video.video_file.save()
                video.is_deleted = False
                video.save()

                return Response({"message": "ویدیو و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "ویدیو مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
