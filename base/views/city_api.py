from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import City
from base.serializers import CitySerializer, CityListSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination

from serializers import MessageAndIdSerializer, ListRequestSerializer, IdSerializer, DeleteSerializer
from utils import create_property_attribute, role_decorator


class CityAddOrUpdateView(APIView):

    @extend_schema(
        request=CitySerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update City"
    )
    @role_decorator
    def post(self, request):
        city_id = request.data.get('id', 0)

        # If city_id is 0, it's a new page, so create it
        if city_id == 0:
            serializer = CitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "شهر با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If city_id is provided, try to update the existing page
        try:
            city = City.objects.get(pk=city_id)
        except City.DoesNotExist:
            return Response({'message': 'شهر مورد نظر برای تغییر یافت نشد.', "id": city_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing page
        serializer = CitySerializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "شهر با موفقیت به روزرسانی شد!", "id": city_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class CityGetListView(APIView):

    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=CityListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of Citys"
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

        citys = City.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('-') else f'-{sort}'
            citys = citys.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            citys = citys.order_by('id')  # or any field you prefer

        # Pagination
        paginator = CityPagination()
        paginated_citys = paginator.paginate_queryset(citys, request)

        # Serialize the paginated data
        serializer = CitySerializer(paginated_citys, many=True)

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


class CityGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=CitySerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Base Page by ID"
    )
    @role_decorator
    def post(self, request):
        city_id = request.data.get('id', 0)
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
      "propertyName": "Country",
      "propertyType": "System.Int64",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": True,
      "fkUrl": "base/CountryList/",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "CountryData.Title",
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
          "value": "کشور ",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "CountryData",
      "propertyType": "StructureAndDataBase.Datas.ViewModels.Base.CountryViewModel",
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
      "propertyName": "Province",
      "propertyType": "System.Int64",
      "enumsSelect": [],
      "isEnum": False,
      "isEnumList": False,
      "isFK": True,
      "fkUrl": "base/ProvinceList/",
      "fknLevel": False,
      "fkLevelEnd": True,
      "fkParent": "",
      "fkShow": "ProvinceData.Title",
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
          "value": "استان",
          "message": None
        }
      ]
    },
    {
      "order": 1000,
      "propertyName": "ProvinceData",
      "propertyType": "StructureAndDataBase.Datas.ViewModels.Base.ProvinceViewModel",
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

        if city_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not city_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CitySerializer(city)

        # Prepare the response structure with property attributes for City fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CityDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific City by ID"
    )
    @role_decorator
    def post(self, request):
        city_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not city_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response({"message": "شهر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if city.is_deleted:
                return Response({"message": "شهر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            city.is_deleted = True
            city.save()
            return Response({"message": "شهر به صورت نرم پاک شد."}, status=status.HTTP_200_OK)

        elif delete_type == 2:
            # Soft delete related content if it exists
            if city.is_deleted:
                return Response({"message": "شهر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)

            if city.content:
                city.content.is_deleted = True
                city.content.save()

            # Soft delete the base page itself
            city.is_deleted = True
            city.save()

            return Response({"message": "شهر و وابستگی های آن صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                city.delete()
                return Response({"message": "شهر  به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                if city.content:
                    city.content.delete()

                # Finally, delete the base page itself
                city.delete()
                return Response({"message": "شهر و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class CityUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the base page
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted City by ID"
    )
    @role_decorator
    def post(self, request):
        city_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not city_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response({"message": "شهر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if city.is_deleted:
            # If the base page is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                city.is_deleted = False
                city.save()
                return Response({"message": "شهر به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                if city.content:
                    city.content.is_deleted = False
                    city.content.save()

                # Restore the base page itself
                city.is_deleted = False
                city.save()

                return Response({"message": "شهر و وابستگی های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع بازیابی نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the base page was not soft-deleted
            return Response({"message": "شهر مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
