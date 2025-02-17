from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from course.models import CourseCategory, Course, Episode
from course.serializers import CourseCategorySerializer, CourseSerializer, EpisodeSerializer
from frontend_api.serializers import CourseSearchRequestSerializer, CourseListPaginationResponseSerializer, \
    CourseDetailSerializer, EpisodeDetailSerializer
from frontend_api.views.cms_page_api import BlogPagination
from serializers import UrlSerializer


class CourseFilterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Retrieve orders and categories data",
        description="Returns a list of orders and categories with their respective details.",
        responses=OpenApiResponse(
            description="Response with orders and categories data.",
            response={
                "type": "object",
                "properties": {
                    "ordersList": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "string", "description": "Key of the order item"},
                                "value": {"type": "string", "description": "Value of the order item"},
                            }
                        }
                    },
                    "categories": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "description": "Category ID"},
                                "title": {"type": "string", "description": "Title of the category"},
                                "englishTitle": {"type": "string", "description": "English title of the category"},
                                "photo": {"type": "string", "description": "URL to the category photo"},
                                "photoId": {"type": "string", "description": "ID of the category photo"},
                            }
                        }
                    }
                }
            }
        )
    )
    def post(self, request):
        categories = CourseCategory.objects.filter(is_deleted=False)
        # Serialize the ContentCategory objects
        category_serializer = CourseCategorySerializer(categories, many=True)
        # Define the orders list
        orders_list = [
            {"key": "new", "value": "جدیدترین"},
            {"key": "view", "value": "بیشترین بازدید"},
            {"key": "popular", "value": "محبوب ترین"},
        ]
        # Prepare the final response
        response_data = {
            "ordersList": orders_list,
            "categories": category_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CourseListPagination(APIView):
    pagination_class = BlogPagination  # Use your existing pagination class
    permission_classes = [AllowAny]

    @extend_schema(
        request=CourseSearchRequestSerializer,
        responses={
            200: OpenApiResponse(response=CourseListPaginationResponseSerializer),
        },
        description="Course List with Pagination"
    )
    def post(self, request):
        category = request.data.get('category')
        search = request.data.get('search')
        page = request.data.get('page', 1)  # Default to 1 for one-based indexing
        page_count = request.data.get('pageCount', 10)  # Default to 10 per page
        order = request.data.get('order', 'id')  # Default order by id
        is_free = request.data.get('is_free', False)

        # Filtering and searching
        courses = Course.objects.filter(is_deleted=False)

        if category:
            courses = courses.filter(category_id=category)

        if search:
            courses = courses.filter(
                Q(title__icontains=search) |
                Q(abstract__icontains=search) |
                Q(keywords__icontains=search)
            )
        if is_free:
            courses = courses.filter(price=0)
        elif not is_free:
            courses = courses.filter(price__gt=0)

        # Ordering the results
        if order == 'new':
            courses = courses.order_by('-create_row_date')
        elif order == 'view':
            courses = courses.order_by('-count_view')
        elif order == 'popular':
            courses = courses.order_by('-count_like')
        else:
            courses = courses.order_by(order)

        # Calculate the correct pagination
        paginator = self.pagination_class()

        # Adjust for one-based page indexing
        start = (page - 1) * page_count
        end = start + page_count

        # Use the paginator to get the paginated courses
        paginated_courses = courses[start:end]

        # Serialize paginated courses
        course_serializer = CourseSerializer(paginated_courses, many=True)

        # Get the total count and total pages
        total_count = courses.count()  # Total count without pagination
        total_page = (total_count // page_count) + (1 if total_count % page_count > 0 else 0)

        # Determine if there is a next page
        has_next_page = page < total_page

        # Construct the response
        response_data = {
            "courses": course_serializer.data,
            "totalPage": total_page,
            "totalCount": total_count,
            "currentPage": page,
            "hasNextPage": has_next_page,  # Correctly determine if there is a next page
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CourseDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(CourseDetailSerializer),
        },
    )
    def post(self, request):
        url = request.data.get('url')  # Get the 'url' parameter from query params
        if not url:
            return Response({"error": "URL parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(english_title=url)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseDetailSerializer(course, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class EpisodeDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(EpisodeDetailSerializer),
        },
    )
    def post(self, request):
        url = request.data.get('url')  # Get the 'url' parameter from query params
        if not url:
            return Response({"error": "URL parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            episode = Episode.objects.get(english_title=url)
        except Episode.DoesNotExist:
            return Response({"error": "Episode not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the episode data
        serializer = EpisodeDetailSerializer(episode)
        return Response(serializer.data, status=status.HTTP_200_OK)