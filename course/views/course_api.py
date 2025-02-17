from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from serializers import MessageAndIdSerializer, ListRequestSerializer, DeleteSerializer, UrlSerializer
from course.models import Course
from course.serializers import CourseSerializer, CourseGetSerializer, CourseListSerializer
from utils import role_decorator


class CourseAddOrUpdateView(APIView):

    @extend_schema(
        request=CourseSerializer,
        responses={
            200: OpenApiResponse(response=MessageAndIdSerializer),
        },
        description="Add or Update Course"
    )
    @role_decorator
    def post(self, request):
        course_id = request.data.get('id', 0)

        # If course_id is 0, it's a new cms, so create it
        if course_id == 0:
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "دوره با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If course_id is provided, try to update the existing cms
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': 'دوره مورد نظر برای تغییر یافت نشد.', "id": course_id},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the existing cms
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "دوره با موفقیت به روزرسانی شد!", "id": course_id},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoursePagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class CourseGetListView(APIView):
    @extend_schema(
        request=ListRequestSerializer,
        responses={
            200: OpenApiResponse(response=CourseListSerializer()),
            400: OpenApiResponse(description='Bad Request')
        },
        description="Get List of Courses"
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

        courses = Course.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            courses = courses.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            courses = courses.order_by('id')  # or any field you prefer

        # Pagination
        paginator = CoursePagination()
        paginated_users = paginator.paginate_queryset(courses, request)

        # Serialize the paginated data
        serializer = CourseSerializer(paginated_users, many=True)
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


class CourseGetView(APIView):

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(response=CourseGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Course by ID"
    )
    @role_decorator
    def post(self, request):
        course_id = request.data.get('id', 0)
        properties_attribute = [
            {
                "type": "line",
                "className": "col-start-1 col-end-9 h-[1px] border border-dashed relative mt-5",
                "label": "اطلاعات اصلی"
            },
            {
                "order": 1000,
                "propertyName": "category",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/course/CourseCategoryList/",
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
                "propertyName": "student_count",
                "propertyType": "System.Int32",
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
                        "value": " تعداد دانشجو ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Content",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "contentManager/ContentManagerList/",
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
                        "value": " محتوا ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "abstract",
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
                "editorType": "full",
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
                "propertyName": "description",
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
                "editorType": "full",
                "isLocation": False,
                "isList": False,
                "listProperty": [],
                "listError": [],
                "locationType": None,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": "توضیحات",
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
                "propertyName": "Features",
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
                        "value": "ویژگی ها : ",
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
                "type": "line",
                "className": "col-start-1 col-end-9 h-[1px] border border-dashed relative mt-5",
                "label": "اطلاعات قیمتی"
            },
            {
                "order": 1000,
                "propertyName": "has_installment",
                "propertyType": "System.Boolean",
                "enumsSelect": [],
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
                        "value": "خرید اقساطی دارد : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "installment_count",
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
                        "value": "تعداد اقساط  : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Price",
                "propertyType": "System.Decimal",
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
                "isPrice": True,
                "priceType": "Decimal",
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
                        "value": "قیمت",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "is_discount",
                "propertyType": "System.Boolean",
                "enumsSelect": [],
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
                        "value": "تخفیف دارد : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "discount",
                "propertyType": "System.Decimal",
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
                "isPrice": True,
                "priceType": "Decimal",
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
                        "value": "تخفیف",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "discount_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Course.CourseEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": "همیشگی",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "زمان دار",
                        "count": 0
                    },
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
                        "value": " نوع تخفیف ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "is_discount_time",
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
                        "value": "تخفیف زمان دار ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "discount_end",
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
                "dateType": "date",
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
                        "value": "تاریخ پایان تخفیف",
                        "message": None
                    }
                ]
            },

            {
                "type": "line",
                "className": "col-start-1 col-end-9 h-[1px] border border-dashed relative mt-5",
                "label": "اطلاعات محتوایی"
            },
            {
                "order": 1000,
                "propertyName": "consultant",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/security/UserList/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "UserData.FullName",
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
                        "value": "مشاور ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "writer",
                "propertyType": "System.Int64",
                "enumsSelect": [],
                "isEnum": False,
                "isEnumList": False,
                "isFK": True,
                "fkUrl": "/security/UserList/",
                "fknLevel": False,
                "fkLevelEnd": True,
                "fkParent": "",
                "fkShow": "UserData.FullName",
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
                        "value": "نویسنده ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "is_published",
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
                        "value": "وضعیت پابلیش : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "question_value",
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
                "isTag": False,
                "isEditor": False,
                "editorType": None,
                "isLocation": False,
                "isList": True,
                "listProperty": [
                    {
                        "order": 1000,
                        "propertyName": "question",
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
                                "value": "پرسش ",
                                "message": None
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
                        "propertyName": "answer",
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
                                "value": "پاسخ",
                                "message": None
                            },
                            {
                                "type": "MaxLengthAttribute",
                                "value": "250",
                                "message": "len of {0} cant more {1} character"
                            }
                        ]
                    },
                ],
                "listError": [],
                "locationType": None,
                "attribute": [
                    {
                        "type": "DisplayAttribute",
                        "value": " پرسش و پاسخ ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "count_session",
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
                        "value": "تعداد جلسات : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "progress",
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
                        "value": "درصد تکمیل  : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "hours",
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
                        "value": "ساعت : ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "publish_date",
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
                "dateType": "date",
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
                        "value": "تاریخ انتشار",
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
        if course_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        if not course_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CourseSerializer(course)

        # Prepare the response structure with manual property attribute definitions for Course fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CourseDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Course by ID"
    )
    @role_decorator
    def post(self, request):
        course_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not course_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "دوره یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if course.is_deleted:
                return Response({"message": "دوره از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            course.is_deleted = True
            course.save()
            return Response({"message": "دوره به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if course.is_deleted:
                return Response({"message": "دوره از قبل حذف نرم شده است."},
                                status=status.HTTP_400_BAD_REQUEST)
            if course.photo:
                course.photo.is_deleted = True
                course.photo.save()

            if course.content:
                course.content.is_deleted = True
                course.content.save()

            if course.content_category:
                course.content_category.is_deleted = True
                course.content_category.save()

            # Soft delete the cms itself
            course.is_deleted = True
            course.save()

            # Add any other related models here

            return Response({"message": "دوره و تمام وابستگی‌های آن به صورت نرم پاک شدند."},
                            status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                course.delete()
                return Response({"message": "دوره به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # Manually delete the associated photo, content, and category if they exist
                if course.photo:
                    course.photo.delete()

                if course.content:
                    course.content.delete()

                if course.content_category:
                    course.content_category.delete()

                # Finally, delete the cms itself
                course.delete()
                return Response({"message": "دوره و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class CourseUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Course by ID"
    )
    @role_decorator
    def post(self, request):
        course_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not course_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "دوره یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if course.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                course.is_deleted = False
                course.save()
                return Response({"message": "دوره به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:

                if course.photo:
                    course.photo.is_deleted = False
                    course.photo.save()

                if course.content:
                    course.content.is_deleted = False
                    course.content.save()

                if course.content_category:
                    course.content_category.is_deleted = False
                    course.content_category.save()

                # Soft delete the cms itself
                course.is_deleted = False
                course.save()

                # Add any other related models here

                return Response({"message": "دوره و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "دوره مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
