from django.db import models
from django.db.models import Sum
from rest_framework import serializers
from django.db.models import Case, When, Value, F

from activity.models import Comment
from activity.serializers import CommentSerializer
from base.models import FaqCategory, Faq, Help, HelpCategory, BasePage, AbstractContent, StaticContent
from base.serializers import ContactInfoSerializer, BranchSerializer
from cms.models import ContentCategory, Blog, Service, Post, WorkSample, Story
from cms.serializers import ContentCategorySerializer, BlogSerializer, PostSerializer, WorkSampleSerializer, \
    ServiceSerializer, StorySerializer
from content_manager.models import ContentManager
from course.models import Course, Episode, EpisodeQA, CourseUser
from course.serializers import CourseSerializer, EpisodeSerializer
from file_manager.models import FileManager
from frontend_api.models import Rule, ContactUs, AboutUs, Privacy, Bug, Criticism, Suggestion, Complaint
from info.models import WhyUs
from info.serializers import CustomerCommentSerializer, WhyUsSerializer, SiteFeatureSerializer, HonorSerializer, \
    StatisticSerializer, TeamSerializer, TimeLineSerializer, ColleagueSerializer
from security.models import User
from task_manager.models import TaskRequest
from utils import duration_maker


class PostSearchRequestSerializer(serializers.Serializer):
    # category = serializers.CharField(required=False, allow_blank=True)
    search = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(default=0)
    pageCount = serializers.IntegerField(default=10)
    order = serializers.CharField(default='id')


class PostListPaginationResponseSerializer(serializers.Serializer):
    posts = PostSerializer(many=True)
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    hasNextPage = serializers.BooleanField()


class WorkSampleSearchRequestSerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_blank=True)
    search = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(default=0)
    pageCount = serializers.IntegerField(default=10)
    order = serializers.CharField(default='id')


class WorkSampleListPaginationResponseSerializer(serializers.Serializer):
    work_samples = WorkSampleSerializer(many=True)
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    hasNextPage = serializers.BooleanField()


class BlogSearchRequestSerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_blank=True)
    search = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(default=0)
    pageCount = serializers.IntegerField(default=0)
    order = serializers.CharField(default='id')


class BlogPaginationDataSerializer(serializers.Serializer):
    blogs = BlogSerializer(many=True)
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    hasNextPage = serializers.BooleanField()


class BlogListSerializer(serializers.Serializer):
    latestBlog = BlogSerializer(many=True)
    bestBlog = BlogSerializer(many=True)


class OrderSerializer(serializers.Serializer):
    title = serializers.CharField()
    value = serializers.CharField()


class ContentCategoryWithChildSerializer(serializers.ModelSerializer):
    childs = ContentCategorySerializer(many=True, source='contentcategory_set')

    class Meta:
        model = ContentCategory
        fields = ['id', 'title', 'english_title', 'photo', 'childs']


class BlogResponseSerializer(serializers.Serializer):
    blogPaginationData = BlogPaginationDataSerializer()
    latestBlog = BlogListSerializer()
    bestBlog = BlogListSerializer()
    orders = OrderSerializer(many=True)
    contentCategorys = ContentCategoryWithChildSerializer(many=True)


# cms/serializers.py

class BlogListPaginationResponseSerializer(serializers.Serializer):
    blogs = BlogSerializer(many=True)
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    hasNextPage = serializers.BooleanField()


class CourseListPaginationResponseSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    hasNextPage = serializers.BooleanField()


class CourseSearchRequestSerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_blank=True)
    search = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(default=0)
    pageCount = serializers.IntegerField(default=0)
    order = serializers.CharField(default='id')
    is_free = serializers.BooleanField(default=False)

class CommentUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_user(self, obj):
        return {
            "full_name": obj.user.full_name,
            "photo": obj.user.photo.id if obj.user.photo else None,
            "about": obj.user.about
        } if obj.user else None

class CourseDetailSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    comment_responses = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    paid_percentage = serializers.SerializerMethodField()  # New field
    has_course = serializers.SerializerMethodField()  # ✅ New field

    class Meta:
        model = Course
        fields = '__all__'

    def get_paid_percentage(self, obj):
        """
        Calculates the paid_percentage for the course_user.
        """
        user = self.context.get('request').user
        if not user.is_authenticated:
            return None

        try:
            course_user = CourseUser.objects.get(course=obj, user=user)
            if course_user.course_installment_count and course_user.paid_installments:
                return f"{course_user.paid_installments}/{course_user.course_installment_count}"
        except CourseUser.DoesNotExist:
            return None

        return None

    def get_episodes(self, obj):
        """
        Modifies the `video_link` field in the episodes based on the user's paid percentage.
        """
        request = self.context.get('request')
        user = request.user if request else None
        episodes = obj.episode_course.all().order_by('order')  # Get all episodes for the course

        if user and user.is_authenticated:
            try:
                course_user = CourseUser.objects.get(course=obj, user=user)

                # Calculate unlocked episodes
                if course_user.course_installment_count and course_user.paid_installments:
                    paid_fraction = course_user.paid_installments / course_user.course_installment_count
                    total_episodes = episodes.count()
                    unlocked_episodes_count = int(paid_fraction * total_episodes)
                else:
                    # No installments paid, no episodes unlocked
                    unlocked_episodes_count = 0
            except CourseUser.DoesNotExist:
                # No `CourseUser` entry for this user, no episodes unlocked
                unlocked_episodes_count = 0
        else:
            # User not authenticated, only free episodes are unlocked
            unlocked_episodes_count = 0

        serialized_episodes = []
        for i, episode in enumerate(episodes):
            # Set `video_link` based on unlocking logic
            if user and user.is_authenticated:
                if i < unlocked_episodes_count:
                    video_link = episode.video_link
                else:
                    video_link = None
            else:
                # For unauthenticated users, only free episodes have `video_link`
                video_link = episode.video_link if episode.is_free else None

            # Serialize the episode with the modified `video_link`
            serialized_episodes.append({
                "id": episode.id,
                "title": episode.title,
                "english_title": episode.english_title,
                "description": episode.description,
                "video_link": video_link,
                "is_video": episode.is_video,
                "is_test": episode.is_test,
                "is_project": episode.is_project,
                "is_free": episode.is_free,
                "order": episode.order,
                "time": duration_maker(episode.time) if episode.time else None,
                "create_row_date": episode.create_row_date,
                "update_row_date": episode.update_row_date,
                "is_deleted": episode.is_deleted,
                "status": episode.status,
                "photo": episode.photo.id if episode.photo else None,
                "file": episode.file.id if episode.file else None,
                "content": episode.content.id if episode.content else None,
                "course": episode.course.id,
                "parent": episode.parent.id if episode.parent else None,
            })

        return serialized_episodes

    def get_content(self, obj):
        return obj.content.content if obj.content else None

    def get_writer(self, obj):
        return {
            "full_name": obj.writer.full_name,
            "photo": obj.writer.photo.id if obj.writer.photo else None,
            "about": obj.writer.about
        } if obj.writer else None

    def get_comment_responses(self, obj):
        comments = Comment.objects.filter(related_id=obj.id, object_type=1, status=1)
        return CommentUserSerializer(comments, many=True).data  # Serialize the queryset

    def get_has_course(self, obj):
        request = self.context.get('request')  # ✅ Get request from context
        if not request or not request.user.is_authenticated:
            return False  # User must be logged in

        user = request.user  # ✅ Now we have the user!

        return CourseUser.objects.filter(
            course=obj, user=user
        ).filter(
            models.Q(paid_installments__gt=0) | models.Q(is_completed=True)
        ).exists()  # ✅ Returns True if conditions are met, else False

class EpisodeDetailSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()
    episode_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    qa = serializers.SerializerMethodField()  # Added field for QA data
    content = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = '__all__'
    def get_content(self, obj):
        return obj.content.content if obj.content else None

    def get_course_name(self, obj):
        return obj.course.title if obj.course.title else None

    def get_episodes(self, obj):
        episodes = Episode.objects.filter(course=obj.course)
        return EpisodeSerializer(episodes, many=True).data

    def get_episode_count(self, obj):
        return obj.course.count_session

    def get_student_count(self, obj):
        return obj.course.student_count

    def get_total_time(self, obj):
        total_duration = Episode.objects.filter(course=obj.course).aggregate(
            total=Sum('time')
        )['total']

        if total_duration:
            total_seconds = int(total_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        return "00:00:00"

    def get_writer(self, obj):
        return {
            "full_name": obj.course.writer.full_name,
            "photo": obj.course.writer.photo.id if obj.course.writer.photo else None,
            "about": obj.course.writer.about
        } if obj.course.writer else None

    def get_qa(self, obj):
        # Retrieve QA data where parent is null for the current episode
        qas = EpisodeQA.objects.filter(episode=obj, parent__isnull=True, is_deleted=False)
        return [self._get_qa_data(qa) for qa in qas]

    def _get_qa_data(self, qa):
        # Recursively get data for each QA and its children
        children = EpisodeQA.objects.filter(parent=qa, is_deleted=False)
        children_data = [self._get_qa_data(child) for child in children] if children else []

        return {
            "id": qa.id,
            "question": qa.content.content if qa.content else None,
            "user": {
                "id": qa.user.id if qa.user else None,
                "sex": qa.user.sex if qa.user else None,
                "full_name": qa.user.full_name if qa.user else None,
                "photo": qa.user.photo.id if qa.user and qa.user.photo else None
            } if qa.user else None,
            "author": {
                "id": qa.author.id if qa.author else None,
                "sex": qa.author.sex if qa.author else None,
                "full_name": qa.author.full_name if qa.author else None,
                "photo": qa.author.photo.id if qa.author and qa.author.photo else None
            } if qa.author else None,
            "course": {
                "id": qa.course.id if qa.course else None,
                "title": qa.course.title if qa.course else None,
                "english_title": qa.course.english_title if qa.course else None
            } if qa.course else None,
            "episode": {
                "id": qa.episode.id if qa.episode else None
            } if qa.episode else None,
            "file": {
                "id": qa.file.id if qa.file else None
            } if qa.file else None,
            "parent": qa.parent.id if qa.parent else None,
            "children": children_data  # Nested children data
        }


class ExtendedResponseSerializer(serializers.Serializer):
    contactInfos = ContactInfoSerializer(many=True)
    contactBranchs = BranchSerializer(many=True)
    content = serializers.CharField()


class ContactUsContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        # Return the content from the related ContentManager, or None if it doesn't exist
        return obj.content.content if obj.content else None

    class Meta:
        model = ContactUs
        fields = ['content']  # We only want to return the 'content' field


class RuleContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return obj.content.content if obj.content else None

    class Meta:
        model = Rule
        fields = ['content']  # We only want to return the 'content' field


class AboutUsContentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', allow_null=True)

    class Meta:
        model = AboutUs
        fields = ['content']


class AboutUsResponseSerializer(serializers.Serializer):
    content = serializers.CharField()
    customerCommentPageResponses = CustomerCommentSerializer(many=True)
    whyUSPageResponses = WhyUsSerializer(many=True)
    siteFeaturePageResponses = SiteFeatureSerializer(many=True)
    honorPageResponses = HonorSerializer(many=True)
    statisticPageResponses = StatisticSerializer(many=True)
    teamPageResponses = TeamSerializer(many=True)
    timeLinePageResponses = TimeLineSerializer(many=True)
    colleaguePageResponses = ColleagueSerializer(many=True)


class PrivacyContentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', allow_null=True)

    class Meta:
        model = Privacy
        fields = ['content']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentManager
        fields = ['content']


# FAQ
class FaqPageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', default=None)

    class Meta:
        model = Faq
        fields = ['title', 'content']


class FaqCategoryPageSerializer(serializers.ModelSerializer):
    rows = FaqPageSerializer(many=True, source='faqs')

    class Meta:
        model = FaqCategory
        fields = ['title', 'photo', 'rows']


# HelpCategory
class HelpPageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', default=None)

    class Meta:
        model = Help
        fields = ['title', 'content']


class HelpCategoryPageSerializer(serializers.ModelSerializer):
    rows = HelpPageSerializer(many=True, source='helps')

    class Meta:
        model = HelpCategory
        fields = ['title', 'photo', 'rows']


# bug
class BugContentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', allow_null=True)

    class Meta:
        model = Bug
        fields = ['content']


# Criticism

class CriticismContentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', allow_null=True)

    class Meta:
        model = Criticism
        fields = ['content']


# Suggestion
class SuggestionContentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', allow_null=True)

    class Meta:
        model = Suggestion
        fields = ['content']


# Complaint
class ComplaintContentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='content.content', allow_null=True)

    class Meta:
        model = Complaint
        fields = ['content']


# إBlogDetail

class UserProfileDataSerializer(serializers.ModelSerializer):
    has_image = serializers.BooleanField(source='photo', default=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'full_name', 'image_url', 'has_image']

    def get_image_url(self, obj):
        if obj.photo:
            return obj.photo.url  # Assuming 'photo' is an instance of FileManager that has a URL attribute
        return None


class CommentCMSSerializer(serializers.ModelSerializer):
    user_profile_data = UserProfileDataSerializer(source='user')  # Fetch user details

    class Meta:
        model = Comment
        fields = [
            'id',
            'user_profile_data',  # Now we have detailed user profile data
            'comment_date',  # Make sure this is formatted as needed in the view or here
            'comment_type',
            'rate',
            'comment_text',
            'positives',  # Adjust if necessary
            'negatives',  # Adjust if necessary
        ]

    def to_representation(self, instance):
        """Customize the output format for the Comment"""
        representation = super().to_representation(instance)
        # Adjust field names as per your requirements
        representation['commentDateValue'] = representation.pop('comment_date')
        representation['possitivesValue'] = representation.pop('positives')
        representation['negativesValue'] = representation.pop('negatives')
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCategory
        fields = ['id', 'title', 'english_title', 'photo']  # Adjust as per your model


class BlogDetailWithUserSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='content_category')  # Reference to the category
    user = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_user(self, obj):
        return {
            "full_name": obj.user.full_name,
            "photo": obj.user.photo.id if obj.user.photo else None,
            "about": obj.user.about
        } if obj.user else None


class BlogDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='content_category')  # Reference to the category
    keywords = serializers.ListField(child=serializers.CharField())
    features = serializers.ListField(child=serializers.CharField())
    comment_responses = serializers.SerializerMethodField()
    related_blogs = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_user(self, obj):
        return {
            "full_name": obj.user.full_name,
            "photo": obj.user.photo.id if obj.user.photo else None,
            "about": obj.user.about
        } if obj.user else None

    def get_comment_responses(self, obj):
        comments = Comment.objects.filter(related_id=obj.id, object_type=2, status=1)
        return CommentUserSerializer(comments, many=True).data  # Serialize the queryset

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None

    def get_related_blogs(self, obj):
        # Fetch the latest 10 blogs with the same category, excluding the current blog
        related_blogs = Blog.objects.filter(
            content_category=obj.content_category,
            is_deleted=False
        ).exclude(id=obj.id).order_by('-create_row_date')[:10]

        # Use BlogDetailSerializer to serialize related blogs or define a simpler serializer
        return BlogContentSerializer(related_blogs, many=True).data


class FaqContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Faq
        fields = '__all__'

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None

class AbstractContentContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = AbstractContent
        fields = '__all__'

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None

class StaticContentContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = StaticContent
        fields = '__all__'

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None

class ServiceContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    comment_responses = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_comment_responses(self, obj):
        comments = Comment.objects.filter(related_id=obj.id, object_type=6)
        return CommentUserSerializer(comments, many=True).data

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None


class ServiceSearchRequestSerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(default=0)
    pageCount = serializers.IntegerField(default=10)
    order = serializers.CharField(default='id')


class ServiceListPaginationResponseSerializer(serializers.Serializer):
    services = ServiceSerializer(many=True)
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    hasNextPage = serializers.BooleanField()


class PostContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'


    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None


class WorkSampleContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    comment_responses = serializers.SerializerMethodField()

    class Meta:
        model = WorkSample
        fields = '__all__'

    def get_comment_responses(self, obj):
        comments = Comment.objects.filter(related_id=obj.id, object_type=3)
        return CommentUserSerializer(comments, many=True).data

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None


class BlogContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    category = CategorySerializer(source='content_category')  # Reference to the category
    user = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None

    def get_user(self, obj):
        return {
            "full_name": obj.user.full_name,
            "photo": obj.user.photo.id if obj.user.photo else None,
            "about": obj.user.about
        } if obj.user else None


class BasePageContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = BasePage
        fields = '__all__'

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None


# Task Manager
class TaskRequestContentSerializer(serializers.ModelSerializer):
    project_members = serializers.SerializerMethodField()
    project_managers = serializers.SerializerMethodField()
    members_detail = serializers.SerializerMethodField()
    managers_detail = serializers.SerializerMethodField()

    class Meta:
        model = TaskRequest
        fields = '__all__'

    def get_project_members(self, obj):
        if obj.task_project.project_members:
            return obj.task_project.project_members
        return None

    def get_project_managers(self, obj):
        if obj.task_project.project_managers:
            return obj.task_project.project_managers
        return None

    def get_members_detail(self, obj):
        members = []
        for member in obj.project_members:
            try:
                user = User.objects.get(id=member)
                members.append(
                    {'id': user.id, 'full_name': user.full_name, 'photo': user.photo.id if user.photo else None})
            except User.DoesNotExist:
                pass
        return members

    def get_managers_detail(self, obj):
        managers = []
        for manager in obj.project_managers:
            try:
                user = User.objects.get(id=manager)
                managers.append(
                    {'id': user.id, 'full_name': user.full_name, 'photo': user.photo.id if user.photo else None})
            except User.DoesNotExist:
                pass
        return managers


# why us
class WhyUsContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = WhyUs
        fields = '__all__'

    def get_content(self, obj):
        if obj.content:
            return obj.content.content
        return None


# story
class StoryFrontSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = "__all__"

    def get_files(self, obj):
        # Retrieve file details from FileManager based on file IDs in the JSONField
        file_ids = obj.files if isinstance(obj.files, list) else []
        files = FileManager.objects.filter(id__in=file_ids)
        return [{'id': file.id, 'file_extension': file.file_extension} for file in files]


class StorySearchRequestSerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_blank=True)
    search = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(default=0)
    pageCount = serializers.IntegerField(default=10)
    order = serializers.CharField(default='id')


class StoryListPaginationResponseSerializer(serializers.Serializer):
    stories = StoryFrontSerializer(many=True)
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    hasNextPage = serializers.BooleanField()


class CourseWriterSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_writer(self, obj):
        return {
            "full_name": obj.writer.full_name,
            "photo": obj.writer.photo.id if obj.writer.photo else None,
            "about": obj.writer.about
        } if obj.writer else None