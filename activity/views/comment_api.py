from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from activity.models import Comment
from serializers import MessageAndIdSerializer, DeleteSerializer, ListRequestSerializer, IdSerializer
from activity.serializers import CommentSerializer, CommentListSerializer, CommentGetSerializer
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse

from utils import create_property_attribute, role_decorator


class CommentAddOrUpdateView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=CommentSerializer,
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Add or Update Comment"
    )
    def post(self, request):
        comment_id = request.data.get('id', 0)

        # Create new comment if ID is 0
        if comment_id == 0:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "نظر با موفقیت ایجاد شد!", "id": serializer.instance.id},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update an existing comment
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({'message': 'نظر مورد نظر یافت نشد.', "id": comment_id}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "نظر با موفقیت به روزرسانی شد!", "id": comment_id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class CommentGetListView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=ListRequestSerializer,
        responses={200: OpenApiResponse(response=CommentListSerializer())},
        description="Get List of Comments"
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

        comments = Comment.objects.filter(query)

        # Sorting
        if sort:
            sort_field = sort if sort.startswith('') else f'-{sort}'
            comments = comments.order_by(sort_field)
        else:
            # Apply a default ordering (e.g., by 'id' or another field)
            comments = comments.order_by('id')  # or any field you prefer

        # Pagination
        paginator = CommentPagination()
        paginated_comments = paginator.paginate_queryset(comments, request)

        # Serialize the paginated data
        serializer = CommentSerializer(paginated_comments, many=True)
        data = paginator.get_paginated_response(serializer.data)

        # Define the propertiesAttribute for the Comment model
        properties_attribute = {
            "propertyName": "Comment_text",
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
            "propertyPersianName": "متن نظر",
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

        return Response(response_data, status=status.HTTP_200_OK)


class CommentGetView(APIView):

    @extend_schema(
        request=IdSerializer,
        responses={
            200: OpenApiResponse(response=CommentGetSerializer),
            400: OpenApiResponse(description='Not Found')
        },
        description="Get a specific Comment by ID"
    )
    @role_decorator
    def post(self, request):
        comment_id = request.data.get('id', 0)
        properties_attribute = [
            {
                "order": 1000,
                "propertyName": "object_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Construction.ObjectTypeEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": "دوره",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "بلاگ",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": "نمونه کار",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": "پست",
                        "count": 0
                    },
                    {
                        "value": 5,
                        "label": "استوری",
                        "count": 0
                    },
                    {
                        "value": 4,
                        "label": "خدمات",
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
                        "value": " نوع وابستگی ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "User",
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
                        "value": "کاربر ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Related_id",
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
                        "value": "شناسه وابستگی ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "comment_date",
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
                        "value": "تاریخ دیدگاه",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "comment_type",
                "propertyType": "StructureAndDataBase.Datas.Models.Activity.CommentTypeEnum",
                "enumsSelect": [
                    {
                        "value": 1,
                        "label": "نظر",
                        "count": 0
                    },
                    {
                        "value": 2,
                        "label": "امتیاز",
                        "count": 0
                    },
                    {
                        "value": 3,
                        "label": "هردو",
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
                        "value": " نوع دیدگاه ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "Rate",
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
                        "value": "امتیاز ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "comment_text",
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
                "isEditor": True,
                "editorType": 'minipopup',
                "isLocation": False,
                "isList": False,
                "listProperty": [],
                "listError": [],
                "locationType": None,
                "attribute": [
                    {
                        "type": "MaxLengthAttribute",
                        "value": "250",
                        "message": "len of {0} cant more {1} character"
                    },
                    {
                        "type": "DisplayAttribute",
                        "value": " متن کامنت ",
                        "message": None
                    }
                ]
            },
            {
                "order": 1000,
                "propertyName": "comment_answer",
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
                "isEditor": True,
                "editorType": 'minipopup',
                "isLocation": False,
                "isList": False,
                "listProperty": [],
                "listError": [],
                "locationType": None,
                "attribute": [
                    {
                        "type": "MaxLengthAttribute",
                        "value": "250",
                        "message": "len of {0} cant more {1} character"
                    },
                    {
                        "type": "DisplayAttribute",
                        "value": " متن جواب ",
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
            }
        ]
        if comment_id == 0:
            response_data = {
                "data": {},
                "propertiesAttribute": properties_attribute
            }
            return Response(response_data, status=status.HTTP_200_OK)

        elif not comment_id:
            print(comment_id)
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comment)

        # Prepare the response structure with manual property attribute definitions for Comment fields

        response_data = {
            "data": serializer.data,
            "propertiesAttribute": properties_attribute
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CommentDeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Delete a specific Comment by ID"
    )
    @role_decorator
    def post(self, request):
        comment_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not comment_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "نظر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type == 1:
            # Soft delete: Set is_deleted to True
            if comment.is_deleted:
                return Response({"message": "نظر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            comment.is_deleted = True
            comment.save()
            return Response({"message": "نظر به صورت نرم پاک شد."}, status=status.HTTP_200_OK)
        elif delete_type == 2:
            # Soft delete the associated photo, content, and category if they exist
            if comment.is_deleted:
                return Response({"message": "نظر از قبل حذف نرم شده است."}, status=status.HTTP_400_BAD_REQUEST)
            if comment.photo:
                comment.photo.is_deleted = True
                comment.photo.save()

            if comment.content:
                comment.content.is_deleted = True
                comment.content.save()

            if comment.content_category:
                comment.content_category.is_deleted = True
                comment.content_category.save()

            # Soft delete the cms itself
            comment.is_deleted = True
            comment.save()

            # Add any other related models here

            return Response({"message": "نظر و تمام وابستگی‌های آن به صورت نرم پاک شدند."}, status=status.HTTP_200_OK)

        elif delete_type == 3:
            # Hard delete: Remove the record from the database
            try:
                comment.delete()
                return Response({"message": "نظر به صورت فیزیکی پاک شد."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_type == 4:
            # Hard delete with dependencies
            try:
                # if comment.photo:
                #     comment.photo.delete()

                comment.delete()
                return Response({"message": "نظر و تمام وابستگی‌های آن به صورت فیزیکی پاک شدند."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"حذف ناموفق: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)


class CommentUndeleteView(APIView):

    @extend_schema(
        request=DeleteSerializer,  # The request body will contain the `id` of the cms
        responses={200: OpenApiResponse(response=MessageAndIdSerializer)},
        description="Restore a soft-deleted Comment by ID"
    )
    @role_decorator
    def post(self, request):
        comment_id = request.data.get('id')
        delete_type = request.data.get('type')

        if not comment_id:
            return Response({"message": "شناسه مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "نظر یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        if comment.is_deleted:
            # If the cms is soft-deleted, restore it by setting is_deleted to False
            if delete_type == 1:
                comment.is_deleted = False
                comment.save()
                return Response({"message": "نظر به صورت نرم بازیابی شد."}, status=status.HTTP_200_OK)
            elif delete_type == 2:
                # Soft delete the cms itself
                comment.is_deleted = False
                comment.save()

                # Add any other related models here

                return Response({"message": "نظر و تمام وابستگی‌های آن به صورت نرم بازیابی شدند."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "نوع حذف نا معتبر."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cms was not soft-deleted
            return Response({"message": "نظر مورد نظر حذف نشده است."}, status=status.HTTP_400_BAD_REQUEST)
