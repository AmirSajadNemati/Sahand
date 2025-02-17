# cms/views.py
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from base.models import Faq, Slider, BasePage, AbstractContent, StaticContent
from base.serializers import FaqSerializer, SliderSerializer, BasePageSerializer, AbstractContentSerializer
from cms.models import Blog, ContentCategory, Gallery, Story, Service, Event, Banner, Post, WorkSample, Brand
from cms.serializers import BlogSerializer, ContentCategorySerializer, GallerySerializer, StorySerializer, \
    ServiceSerializer, EventSerializer, BannerSerializer, PostSerializer, WorkSampleSerializer, BrandSerializer
from django.db.models import Q

from course.models import Course, CourseCategory
from course.serializers import CourseSerializer, CourseCategorySerializer
from frontend_api.models import AboutUs
from frontend_api.serializers import BlogResponseSerializer, BlogSearchRequestSerializer, \
    BlogListPaginationResponseSerializer, BlogDetailSerializer, ServiceContentSerializer, BasePageContentSerializer, \
    BlogContentSerializer, FaqContentSerializer, CourseListPaginationResponseSerializer, PostContentSerializer, \
    WorkSampleContentSerializer, PostSearchRequestSerializer, PostListPaginationResponseSerializer, \
    WorkSampleSearchRequestSerializer, WorkSampleListPaginationResponseSerializer, AboutUsContentSerializer, \
    BlogDetailWithUserSerializer, ServiceSearchRequestSerializer, ServiceListPaginationResponseSerializer, \
    WhyUsContentSerializer, StorySearchRequestSerializer, StoryListPaginationResponseSerializer, StoryFrontSerializer, \
    AbstractContentContentSerializer, StaticContentContentSerializer, CourseWriterSerializer
from info.models import WhyUs, Colleague, Statistic, CustomerComment, Team
from info.serializers import WhyUsSerializer, ColleagueSerializer, StatisticSerializer, CustomerCommentSerializer, \
    TeamSerializer
from serializers import GetModelSerializer, UrlSerializer


class BlogPagination(PageNumberPagination):
    permission_classes = [AllowAny]
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get('page', 1)

    def get_page_size(self, request):
        return request.data.get('pageSize', self.page_size)


class BlogSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=BlogSearchRequestSerializer,
        responses={
            200: OpenApiResponse(response=BlogResponseSerializer),
        },
        description="BlogList cmsPage"
    )
    def post(self, request):
        category = request.data.get('category')
        search = request.data.get('search')
        page = request.data.get('page', 0)
        page_count = request.data.get('pageCount', 10)  # Default to 10 per page
        order = request.data.get('order', 'id')  # Default order by id

        # Filtering and searching
        blogs = Blog.objects.filter(is_deleted=False)

        if category:
            blogs = blogs.filter(
                Q(content_category__title__icontains=category) |
                Q(content_category__english_title__icontains=category)
            )

        if search:
            blogs = blogs.filter(
                Q(title__icontains=search) |
                Q(abstract__icontains=search) |
                Q(keywords__icontains=search)
            )

        # Ordering the results
        order_mapping = {
            "new": "-create_row_date",  # Newest first
            "view": "-count_view",  # Most views first
            "popular": "-count_like",
        }

        # Determine the order field
        order_field = order_mapping.get(order, 'id')  # Fallback to 'id' if order is invalid
        blogs = blogs.order_by(order_field)

        # Pagination
        total_count = blogs.count()
        total_page = (total_count // page_count) + (1 if total_count % page_count > 0 else 0)
        start = page * page_count
        end = start + page_count
        paginated_blogs = blogs[start:end]

        # Serialize paginated blogs
        blog_serializer = BlogDetailWithUserSerializer(paginated_blogs, many=True)

        # Get latest and best blogs (you might want to implement your own logic here)
        latest_blogs = Blog.objects.filter(is_deleted=False).order_by('-create_row_date')[:5]  # Get the latest 5
        best_blogs = Blog.objects.filter(is_deleted=False).order_by('-count_view')[:5]  # Get the most viewed 5

        latest_blog_serializer = BlogDetailWithUserSerializer(latest_blogs, many=True)
        best_blog_serializer = BlogDetailWithUserSerializer(best_blogs, many=True)

        # Fetch all content categories
        content_categories = ContentCategory.objects.filter(is_deleted=False)
        content_category_serializer = ContentCategorySerializer(content_categories, many=True)

        # Construct the response
        response_data = {
            "blogPaginationData": {
                "blogs": blog_serializer.data,
                "totalPage": total_page,
                "totalCount": total_count,
                "currentPage": page,
                "hasNextPage": page + 1 < total_page,
            },
            "latestBlog": latest_blog_serializer.data,
            "bestBlog": best_blog_serializer.data,
            "orders": [
                {"key": "new", "value": "جدیدترین"},
                {"key": "view", "value": "بیشترین بازدید"},
                {"key": "popular", "value": "محبوب ترین"}
            ],
            "contentCategorys": content_category_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


# cms/views.py
class BlogListPagination(APIView):
    pagination_class = BlogPagination  # Use your existing pagination class
    permission_classes = [AllowAny]

    @extend_schema(
        request=BlogSearchRequestSerializer,
        responses={
            200: OpenApiResponse(response=BlogListPaginationResponseSerializer),
        },
        description="Blog List with Pagination"
    )
    def post(self, request):
        category = request.data.get('category')
        search = request.data.get('search')
        page = request.data.get('page', 1)  # Default to 1 for one-based indexing
        page_count = request.data.get('pageCount', 10)  # Default to 10 per page
        order = request.data.get('order', 'id')  # Default order by id

        # Filtering and searching
        blogs = Blog.objects.filter(is_deleted=False)

        if category:
            blogs = blogs.filter(content_category__title__icontains=category)

        if search:
            blogs = blogs.filter(
                Q(title__icontains=search) |
                Q(abstract__icontains=search) |
                Q(keywords__icontains=search)
            )

        # Ordering the results
        if order == 'new':
            blogs = blogs.order_by('-create_row_date')
        elif order == 'view':
            blogs = blogs.order_by('-count_view')
        elif order == 'popular':
            blogs = blogs.order_by('-count_like')
        else:
            blogs = blogs.order_by(order)

        # Calculate the correct pagination
        paginator = self.pagination_class()

        # Adjust for one-based page indexing
        start = (page - 1) * page_count
        end = start + page_count

        # Use the paginator to get the paginated blogs
        paginated_blogs = blogs[start:end]

        # Serialize paginated blogs
        blog_serializer = BlogSerializer(paginated_blogs, many=True)

        # Get the total count and total pages
        total_count = blogs.count()  # Total count without pagination
        total_page = (total_count // page_count) + (1 if total_count % page_count > 0 else 0)

        # Determine if there is a next page
        has_next_page = page < total_page

        # Construct the response
        response_data = {
            "blogs": blog_serializer.data,
            "totalPage": total_page,
            "totalCount": total_count,
            "currentPage": page,
            "hasNextPage": has_next_page,  # Correctly determine if there is a next page
        }

        return Response(response_data, status=status.HTTP_200_OK)


# views.py
class BlogDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(BlogDetailSerializer),
        },
    )
    def post(self, request):
        en_name = request.data.get('url')  # This can be used for filtering or other logic
        try:
            blog = Blog.objects.get(english_title=en_name, is_deleted=False)
            # Assume `content` field is also serialized properly
            serializer = BlogDetailSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'message': 'بلاگ یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)


class BlogFilterView(APIView):
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
        categories = ContentCategory.objects.filter(is_deleted=False)

        # Serialize the ContentCategory objects
        category_serializer = ContentCategorySerializer(categories, many=True)

        # Define the orders list
        orders_list = [
            {"key": "new", "value": "جدیدترین"},
            {"key": "view", "value": "بیشترین بازدید"},
            {"key": "popular", "value": "محبوب ترین"}
        ]

        # Prepare the final response
        response_data = {
            "ordersList": orders_list,
            "categories": category_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class IndexAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Retrieve latest 10 items for each content type",
        description="Returns the 10 most recently created items from each content model.",
        responses=OpenApiResponse(
            description="Response with the 10 latest objects for each model.",
            response={
                "type": "object",
                "properties": {
                    "blogs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "abstract": {"type": "string"},
                                "count_share": {"type": "integer"},
                                "count_comment": {"type": "integer"},
                                "count_like": {"type": "integer"},
                                "count_view": {"type": "integer"},
                                "rate": {"type": "number"}
                            }
                        }
                    },
                    "faqs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "content": {"type": "string"},
                                "status": {"type": "integer"}
                            }
                        }
                    },
                    "galleries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "tags": {"type": "string"},
                                "count_view": {"type": "integer"},
                                "rate": {"type": "number"}
                            }
                        }
                    },
                    "stories": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "story_details": {"type": "string"},
                                "status": {"type": "integer"}
                            }
                        }
                    },
                    "services": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "price": {"type": "string"},
                                "status": {"type": "integer"}
                            }
                        }
                    },
                    "sliders": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "order_num": {"type": "integer"}
                            }
                        }
                    },
                    "whyus": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "text": {"type": "string"},
                                "order": {"type": "integer"},
                                "status": {"type": "integer"}
                            }
                        }
                    },
                    "colleagues": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "order": {"type": "integer"},
                                "status": {"type": "integer"}
                            }
                        }
                    },
                    "events": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "event_date": {"type": "string", "format": "date"},
                                "is_holiday": {"type": "boolean"},
                                "description": {"type": "string"},
                                "photos": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "status": {"type": "integer"}
                            }
                        }
                    },
                    "courses": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string"},
                                "english_title": {"type": "string"},
                                "photo_id": {"type": "integer", "nullable": True},
                                "video_id": {"type": "integer", "nullable": True},
                                "category_id": {"type": "integer", "nullable": True},
                                "count_share": {"type": "integer", "default": 0},
                                "count_comment": {"type": "integer", "default": 0},
                                "count_like": {"type": "integer", "default": 0},
                                "count_dislike": {"type": "integer", "default": 0},
                                "count_view": {"type": "integer", "default": 0},
                                "count_sale": {"type": "integer", "default": 0},
                                "count_session": {"type": "integer", "nullable": True},
                                "minutes": {"type": "integer", "nullable": True},
                                "progress": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "maximum": 100
                                },
                                "rate": {"type": "number", "default": 0},
                                "abstract": {"type": "string", "maxLength": 3000},
                                "description": {"type": "string", "maxLength": 3000},
                                "features": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "tags": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "price": {
                                    "type": "number",
                                    "maximum": 999999999999999.999,
                                    "nullable": True
                                },
                                "is_discount": {"type": "boolean", "default": False},
                                "discount": {
                                    "type": "number",
                                    "maximum": 999999999999999.999,
                                    "nullable": True
                                },
                                "discount_type": {
                                    "type": "integer",
                                    "enum": [1, 2],
                                    "nullable": True
                                },
                                "discount_end": {"type": "string", "format": "date-time", "nullable": True},
                                "is_discount_time": {"type": "boolean", "default": False},
                                "consultant_id": {"type": "integer", "nullable": True},
                                "writer_id": {"type": "integer", "nullable": True},
                                "question_value": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "is_published": {"type": "boolean", "default": False},
                                "create_row_date": {"type": "string", "format": "date-time"},
                                "update_row_date": {"type": "string", "format": "date-time"},
                                "is_deleted": {"type": "boolean", "default": False},
                                "status": {
                                    "type": "integer",
                                    "enum": [1, 2],
                                    "nullable": True
                                }
                            }
                        }
                    }
                }
            }
        )
    )
    def post(self, request):
        # Fetch the 10 latest objects from each model
        latest_blogs = Blog.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_faqs = Faq.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')
        latest_galleries = Gallery.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_stories = Story.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_services = Service.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_sliders = Slider.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')
        latest_whyus = WhyUs.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')
        latest_colleagues = Colleague.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_events = Event.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_courses = Course.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_banners = Banner.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_statistics = Statistic.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_posts = Post.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_customer_comments = CustomerComment.objects.filter(is_deleted=False, status=1).order_by(
            '-create_row_date')[:10]
        latest_work_samples = WorkSample.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_brands = Brand.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_abstract_contents = AbstractContent.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        latest_static_contents = StaticContent.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        about_us = AboutUs.objects.first()
        latest_teams = Team.objects.filter(is_deleted=False, status=1).order_by('-create_row_date')[:10]
        # Serialize each queryset
        response_data = {
            "blogs": BlogDetailWithUserSerializer(latest_blogs, many=True).data,
            "faqs": FaqContentSerializer(latest_faqs, many=True).data,
            "galleries": GallerySerializer(latest_galleries, many=True).data,
            "stories": StoryFrontSerializer(latest_stories, many=True).data,
            "services": ServiceSerializer(latest_services, many=True).data,
            "sliders": SliderSerializer(latest_sliders, many=True).data,
            "whyus": WhyUsSerializer(latest_whyus, many=True).data,
            "colleagues": ColleagueSerializer(latest_colleagues, many=True).data,
            "events": EventSerializer(latest_events, many=True).data,
            "courses": CourseWriterSerializer(latest_courses, many=True).data,
            "banners": BannerSerializer(latest_banners, many=True).data,
            "statistics": StatisticSerializer(latest_statistics, many=True).data,
            "posts": PostSerializer(latest_posts, many=True).data,
            "customer_comments": CustomerCommentSerializer(latest_customer_comments, many=True).data,
            "work_samples": WorkSampleSerializer(latest_work_samples, many=True).data,
            "about_us": AboutUsContentSerializer(about_us).data,
            "brands": BrandSerializer(latest_brands, many=True).data,
            "abstract_contents": AbstractContentContentSerializer(latest_abstract_contents, many=True).data,
            "static_contents": StaticContentContentSerializer(latest_static_contents, many=True).data,
            "teams": TeamSerializer(latest_teams, many=True).data,
        }

        return Response(response_data)


# region service
class ServiceDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(ServiceContentSerializer),
        },
    )
    def post(self, request):
        # Extracting the data from request
        en_name = request.data.get('url')

        try:
            # Retrieve the service based on the english_title and is_deleted fields
            service = Service.objects.get(english_title=en_name, is_deleted=False)
            # Serialize the single service object (do not use `many=True`)
            serializer = ServiceContentSerializer(service)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            # Handle case where service is not found
            return Response({'message': 'خدمات یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

class ServiceSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ServiceSearchRequestSerializer,
        responses={
            200: OpenApiResponse(response=ServiceListPaginationResponseSerializer),
        },
        description="ServiceList cmsPage"
    )
    def post(self, request):
        search = request.data.get('search')
        page = request.data.get('page', 0)
        page_count = request.data.get('pageCount', 10)  # Default to 10 per page
        order = request.data.get('order', 'id')  # Default order by id

        # Filtering and searching
        services = Service.objects.filter(is_deleted=False)

        if search:
            services = services.filter(
                Q(title__icontains=search) |
                Q(english_title__icontains=search)
            )

        # Ordering the results
        services = services.order_by(order)

        # Pagination
        total_count = services.count()
        total_page = (total_count // page_count) + (1 if total_count % page_count > 0 else 0)
        start = page * page_count
        end = start + page_count
        paginated_services = services[start:end]

        # Serialize paginated work samples
        service_serializer = ServiceSerializer(paginated_services, many=True)

        # Get latest and best work samples (implement your logic if needed)
        latest_services= Service.objects.filter(is_deleted=False).order_by('-create_row_date')[:5]
        best_services = Service.objects.filter(is_deleted=False).order_by('-count_view')[:5]

        latest_service_serializer = ServiceSerializer(latest_services, many=True)
        best_service_serializer = ServiceSerializer(best_services, many=True)

        # Construct the response
        response_data = {
            "servicePaginationData": {
                "services": service_serializer.data,
                "totalPage": total_page,
                "totalCount": total_count,
                "currentPage": page,
                "hasNextPage": page + 1 < total_page,
            },
            "latestService": latest_service_serializer.data,
            "bestService": best_service_serializer.data,
            "orders": [
                {"key": "new", "value": "جدیدترین"},
                {"key": "view", "value": "بیشترین بازدید"},
                {"key": "popular", "value": "محبوب ترین"}
            ],
        }

        return Response(response_data, status=status.HTTP_200_OK)
# endregion
# region Base Page
class BasePageDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(BasePageContentSerializer),
        },
    )
    def post(self, request):
        # Extracting the data from request
        # blog_id = request.data.get('id')
        # parent_id = request.data.get('parentId')  # This could be useful if you have a parent-child relationship
        en_name = request.data.get('url')  # This can be used for filtering or other logic

        try:
            base_page = BasePage.objects.get(url=en_name, is_deleted=False)
            # Assume `content` field is also serialized properly
            serializer = BasePageContentSerializer(base_page)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BasePage.DoesNotExist:
            return Response({'message': 'صفحه اصلی یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)


# endregion
# region post

class PostDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(PostContentSerializer),
        },
    )
    def post(self, request):
        # Extracting the data from request
        en_name = request.data.get('url')

        try:
            # Retrieve the service based on the english_title and is_deleted fields
            post = Post.objects.get(english_title=en_name, is_deleted=False)
            # Serialize the single service object (do not use `many=True`)
            serializer = PostContentSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            # Handle case where service is not found
            return Response({'message': 'پست یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)


class PostSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PostSearchRequestSerializer,
        responses={
            200: OpenApiResponse(response=PostListPaginationResponseSerializer),
        },
        description="PostList cmsPage"
    )
    def post(self, request):
        category = request.data.get('category')
        search = request.data.get('search')
        page = request.data.get('page', 0)
        page_count = request.data.get('pageCount', 10)  # Default to 10 per page
        order = request.data.get('order', 'id')  # Default order by id

        # Filtering and searching
        posts = Post.objects.filter(is_deleted=False, is_published=True)

        # if category:
        #     posts = posts.filter(content__title__icontains=category)

        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(english_title__icontains=search) |
                Q(hashtag__icontains=search)
            )
        valid_fields = {"new": "create_row_date", "view": "count_view", "popular": "count_like"}

        # Check if order starts with "-" (indicating ascending order)
        is_ascending = order.startswith("-")
        order_key = order.lstrip("-")  # Remove '-' to get the base field name

        # Get the corresponding database field, defaulting to `order` itself if not found
        field_name = valid_fields.get(order_key, order)

        # Apply ordering (prepend '-' for descending order)
        posts = posts.order_by(field_name if is_ascending else f"-{field_name}")

        # Pagination
        total_count = posts.count()
        total_page = (total_count // page_count) + (1 if total_count % page_count > 0 else 0)
        start = page * page_count
        end = start + page_count
        paginated_posts = posts[start:end]

        # Serialize paginated posts
        post_serializer = PostSerializer(paginated_posts, many=True)

        # Get latest and best posts (implement your logic if needed)
        latest_posts = Post.objects.filter(is_deleted=False, is_published=True).order_by('-create_row_date')[:5]
        best_posts = Post.objects.filter(is_deleted=False, is_published=True).order_by('-count_view')[:5]

        latest_post_serializer = PostSerializer(latest_posts, many=True)
        best_post_serializer = PostSerializer(best_posts, many=True)

        # Fetch all content categories
        content_categories = ContentCategory.objects.filter(is_deleted=False)
        content_category_serializer = ContentCategorySerializer(content_categories, many=True)

        # Construct the response
        response_data = {
            "postPaginationData": {
                "posts": post_serializer.data,
                "totalPage": total_page,
                "totalCount": total_count,
                "currentPage": page,
                "hasNextPage": page + 1 < total_page,
            },
            "latestPost": latest_post_serializer.data,
            "bestPost": best_post_serializer.data,
            "orders": [
                {"key": "new", "value": "جدیدترین"},
                {"key": "view", "value": "بیشترین بازدید"},
                {"key": "popular", "value": "محبوب ترین"}
            ],
            "contentCategorys": content_category_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

# endregion

# region WorkSample
class WorkSampleSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=WorkSampleSearchRequestSerializer,
        responses={
            200: OpenApiResponse(response=WorkSampleListPaginationResponseSerializer),
        },
        description="WorkSampleList cmsPage"
    )
    def post(self, request):
        category = request.data.get('category')
        search = request.data.get('search')
        page = request.data.get('page', 0)
        page_count = request.data.get('pageCount', 10)  # Default to 10 per page
        order = request.data.get('order', 'id')  # Default order by id

        # Filtering and searching
        work_samples = WorkSample.objects.filter(is_deleted=False)

        if category:
            work_samples = work_samples.filter(categories__icontains=category)

        if search:
            work_samples = work_samples.filter(
                Q(title__icontains=search) |
                Q(english_title__icontains=search) |
                Q(tags__icontains=search)
            )

        # Ordering the results
        order_mapping = {
            "new": "-create_row_date",  # Newest first
            "view": "-count_view",  # Most views first
            "popular": "-count_like",
        }

        # Determine the order field
        order_field = order_mapping.get(order, 'id')  # Fallback to 'id' if order is invalid
        work_samples = work_samples.order_by(order_field)

        # Pagination
        total_count = work_samples.count()
        total_page = (total_count // page_count) + (1 if total_count % page_count > 0 else 0)
        start = page * page_count
        end = start + page_count
        paginated_work_samples = work_samples[start:end]

        # Serialize paginated work samples
        work_sample_serializer = WorkSampleSerializer(paginated_work_samples, many=True)

        # Get latest and best work samples (implement your logic if needed)
        latest_work_samples = WorkSample.objects.filter(is_deleted=False).order_by('-create_row_date')[:5]
        best_work_samples = WorkSample.objects.filter(is_deleted=False).order_by('-count_view')[:5]

        latest_work_sample_serializer = WorkSampleSerializer(latest_work_samples, many=True)
        best_work_sample_serializer = WorkSampleSerializer(best_work_samples, many=True)

        # Construct the response
        response_data = {
            "workSamplePaginationData": {
                "work_samples": work_sample_serializer.data,
                "totalPage": total_page,
                "totalCount": total_count,
                "currentPage": page,
                "hasNextPage": page + 1 < total_page,
            },
            "latestWorkSample": latest_work_sample_serializer.data,
            "bestWorkSample": best_work_sample_serializer.data,
            "orders": [
                {"key": "new", "value": "جدیدترین"},
                {"key": "view", "value": "بیشترین بازدید"},
                {"key": "popular", "value": "محبوب ترین"}
            ],
        }

        return Response(response_data, status=status.HTTP_200_OK)


class WorkSampleDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UrlSerializer,
        responses={
            200: OpenApiResponse(WorkSampleContentSerializer),
        },
    )
    def post(self, request):
        # Extracting the data from request
        en_name = request.data.get('url')

        try:
            # Retrieve the service based on the english_title and is_deleted fields
            work_sample = WorkSample.objects.get(english_title=en_name, is_deleted=False)
            # Serialize the single service object (do not use `many=True`)
            serializer = WorkSampleContentSerializer(work_sample)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WorkSample.DoesNotExist:
            # Handle case where service is not found
            return Response({'message': 'نمونه کار یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)
# endregion

# region about us
class AboutUsDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(AboutUsContentSerializer),
        },
    )
    def post(self, request):
        try:
            # Retrieve the about_us object
            about_us = AboutUs.objects.first()

            # Retrieve related data
            brands = Brand.objects.filter(is_deleted=False, status=1)
            teams = Team.objects.filter(is_deleted=False, status=1)
            statistics = Statistic.objects.filter(is_deleted=False, status=1)

            # Serialize data
            about_us_serializer = AboutUsContentSerializer(about_us)
            brands_serializer = BrandSerializer(brands, many=True)
            teams_serializer = TeamSerializer(teams, many=True)
            statistics_serializer = StatisticSerializer(statistics, many=True)

            # Combine all data into response
            response_data = {
                'about_us': about_us_serializer.data,
                'brands': brands_serializer.data,
                'team': teams_serializer.data,
                'statistics': statistics_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AboutUs.DoesNotExist:
            return Response({'message': 'درباره ی ما یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)
# endregion


# region why us
class WhyUsDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(WhyUsContentSerializer),
        },
    )
    def post(self, request):
        try:
            why_us = WhyUs.objects.first()
            why_us_serializer = WhyUsContentSerializer(why_us)

            return Response(why_us_serializer.data, status=status.HTTP_200_OK)
        except WhyUs.DoesNotExist:
            return Response({'message': 'چرا ما یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)
# endregion
class WhyUsSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(WhyUsContentSerializer(many=True)),
        },
    )
    def post(self, request):
        # Query all non-deleted WhyUs objects
        why_us_objects = WhyUs.objects.filter(is_deleted=False)

        # Serialize the data
        serializer = WhyUsContentSerializer(why_us_objects, many=True)

        # Return the serialized data
        return Response(serializer.data, status=200)

# region story
class StoryListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=StorySearchRequestSerializer,
        responses={
            200: OpenApiResponse(response=StoryListPaginationResponseSerializer),
        },
        description="Story List and Search"
    )
    def post(self, request):
        category = request.data.get('category')
        search = request.data.get('search')
        page = request.data.get('page', 0)
        page_count = request.data.get('pageCount', 10)  # Default to 10 per page
        order = request.data.get('order', 'id')  # Default order by id

        # Filtering and searching
        stories = Story.objects.filter(is_deleted=False, is_published=True)

        if category:
            stories = stories.filter(story_details__icontains=category)

        if search:
            stories = stories.filter(
                Q(title__icontains=search) |
                Q(story_details__icontains=search) |
                Q(link__icontains=search)
            )

        # Ordering the results
        stories = stories.order_by(order)

        # Pagination
        total_count = stories.count()
        total_page = (total_count // page_count) + (1 if total_count % page_count > 0 else 0)
        start = page * page_count
        end = start + page_count
        paginated_stories = stories[start:end]

        # Serialize paginated stories
        story_serializer = StoryFrontSerializer(paginated_stories, many=True)

        # Get latest and best stories
        latest_stories = Story.objects.filter(is_deleted=False, is_published=True).order_by('-create_row_date')[:5]
        best_stories = Story.objects.filter(is_deleted=False, is_published=True).order_by('-count_view')[:5]

        latest_story_serializer = StoryFrontSerializer(latest_stories, many=True)
        best_story_serializer = StoryFrontSerializer(best_stories, many=True)

        # Construct the response
        response_data = {
            "storyPaginationData": {
                "stories": story_serializer.data,
                "totalPage": total_page,
                "totalCount": total_count,
                "currentPage": page,
                "hasNextPage": page + 1 < total_page,
            },
            "latestStory": latest_story_serializer.data,
            "bestStory": best_story_serializer.data,
            "orders": [
                {"key": "new", "value": "جدیدترین"},
                {"key": "view", "value": "بیشترین بازدید"},
                {"key": "popular", "value": "محبوب ترین"}
            ],
        }

        return Response(response_data, status=status.HTTP_200_OK)

# endregion