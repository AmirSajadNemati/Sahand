from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import SiteInfo
from base.serializers import SiteInfoSerializer, SiteInfoListSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination

from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import create_property_attribute, role_decorator


class SiteInfoAddOrUpdateView(APIView):

    @extend_schema(
        request=SiteInfoSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update SiteInfo"
    )
    @role_decorator
    def post(self, request):
        site_info_id = request.data.get('id', 0)

        # If site_info_id is 0, it's a new page, so create it
        if site_info_id == 0:
            serializer = SiteInfoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "اطلاعات سایت با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If site_info_id is provided, try to update the existing page
        try:
            site_info = SiteInfo.objects.get(pk=site_info_id)
        except SiteInfo.DoesNotExist:
            return Response({'message': 'اطلاعات سایت مورد نظر برای تغییر یافت نشد.', "id": site_info_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = SiteInfoSerializer(site_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "اطلاعات سایت با موفقیت به روزرسانی شد!", "id": site_info_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteInfoPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class SiteInfoGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=SiteInfoListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of SiteInfos"
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

        site_infos = SiteInfo.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            site_infos = site_infos.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            site_infos = site_infos.order_by('id')  # or any field you prefer

        # Pagination
        paginator = SiteInfoPagination()
        paginated_site_infos = paginator.paginate_queryset(site_infos, request)

        # Serialize the paginated data
        serialized_data = SiteInfoSerializer(paginated_site_infos, many=True).data

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


class SiteInfoGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=SiteInfoSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Base Page by ID"
    )
    @role_decorator
    def post(self, request):
        site_info_id = request.data.get('id', 0)
        properties_attribute = [
            {
                "order": 1000,
                "propertyName": "title",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 150,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Title",
                        "message": None
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
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 150,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "English Title",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "site_url",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 150,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Site URL",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "slogan",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 350,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Slogan",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "developer_title",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 150,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Developer Title",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "developer_english_title",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 150,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Developer English Title",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "developer_url",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 150,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Developer URL",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "logo",
                "propertyType": "StructureAndDataBase.Datas.Models.FileManager",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fkShow": "setting_logo",
                "isFile": True,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "لوگو",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "fav_icon",
                "propertyType": "StructureAndDataBase.Datas.Models.FileManager",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fkShow": "fav_icon",
                "isFile": True,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Fav Icon",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "small_logo",
                "propertyType": "StructureAndDataBase.Datas.Models.FileManager",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fkShow": "small_logo",
                "isFile": True,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Small Logo",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "developer_logo",
                "propertyType": "StructureAndDataBase.Datas.Models.FileManager",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fkShow": "dev_logo",
                "isFile": True,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Developer Logo",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "white_logo",
                "propertyType": "StructureAndDataBase.Datas.Models.FileManager",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fkShow": "white_logo",
                "isFile": True,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "White Logo",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "light_base_color",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 16,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Light Base Color",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "dark_base_color",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 16,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Dark Base Color",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "dark_second_color",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 16,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Dark Second Color",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "dark_text_color",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 16,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Dark Text Color",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "dark_box_color",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 16,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Dark Box Color",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "dark_bg_color",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 16,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Dark Background Color",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "dark_third_color",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 16,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Dark Third Color",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "keywords",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 1500,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Keywords",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "description",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 300,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Description",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "robot_txt",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 1000,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Robot.txt",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "video",
                "propertyType": "StructureAndDataBase.Datas.Models.FileManager",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "fileManager/",
                "fkShow": "setting_video",
                "isFile": True,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Video",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "catalog_id",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "maxLength": 100,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Catalog ID",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "features_selected",
                "propertyType": "System.String",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": False,
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": True,
                "isBlank": True,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Selected Features",
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
                "isFile": False,
                "isReadOnly": True,
                "isNotShow": False,
                "isHidden": False,
                "isNull": False,
                "isBlank": False,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Creation Date",
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
                "isFile": False,
                "isReadOnly": True,
                "isNotShow": False,
                "isHidden": False,
                "isNull": False,
                "isBlank": False,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Last Updated Date",
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
                "isFile": False,
                "isReadOnly": False,
                "isNotShow": False,
                "isHidden": False,
                "isNull": False,
                "isBlank": False,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "Deleted Status",
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
                        "value": "Status : ",
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

        ]

        if site_info_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not site_info_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            site_info = SiteInfo.objects.get(id=site_info_id)
        except SiteInfo.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SiteInfoSerializer(site_info)

        # Prepare the response structure with property attributes for SiteInfo fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SiteInfoDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific SiteInfo by ID"
    )
    @role_decorator
    def post(self, request):
        site_info_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not site_info_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            site_info = SiteInfo.objects.get(id=site_info_id)
        except SiteInfo.DoesNotExist:
            return Response({"message": "اطلاعات سایت یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if site_info.is_deleted:
                return Response({"message": "اطلاعات سایت از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            site_info.is_deleted = True
            site_info.save()
            return Response({"message": "اطلاعات سایت به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete related content if it exists
            if site_info.is_deleted:
                return Response({"message": "اطلاعات سایت از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)

            if site_info.content:
                site_info.content.is_deleted = True
                site_info.content.save()

            # Soft delete the base page itself
            site_info.is_deleted = True
            site_info.save()

            return Response({"message": "اطلاعات سایت و وابستگی های آن صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                site_info.delete()
                return Response({"message": "اطلاعات سایت  به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if site_info.content:
                    site_info.content.delete()

                # Finally, delete the base page itself
                site_info.delete()
                return Response({"message": "اطلاعات سایت و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class SiteInfoUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted SiteInfo by ID"
    )
    @role_decorator
    def post(self, request):
        site_info_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not site_info_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            site_info = SiteInfo.objects.get(id=site_info_id)
        except SiteInfo.DoesNotExist:
            return Response({"message": "اطلاعات سایت یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if site_info.is_deleted:
            # If the base page is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                site_info.is_deleted = False
                site_info.save()
                return Response({"message": "اطلاعات سایت به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if site_info.content:
                    site_info.content.is_deleted = False
                    site_info.content.save()

                # Restore the base page itself
                site_info.is_deleted = False
                site_info.save()

                return Response({"message": "اطلاعات سایت و وابستگی های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the base page was not soft-deleted
            return Response({"message": "اطلاعات سایت مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
