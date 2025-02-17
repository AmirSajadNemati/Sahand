from rest_framework import serializers

from activity.serializers import CommentSerializer
from cms.models import Blog
from cms.serializers import ServiceSerializer, StorySerializer, PostSerializer, BlogSerializer, WorkSampleSerializer
from course.serializers import CourseSerializer, CourseUserSerializer


# from course.serializers import CourseUserSerializer
from payment.serializers import TransactionSerializer


class DashboardCommentSerializer(serializers.Serializer):
    all_comments = serializers.IntegerField()
    true_comments = serializers.IntegerField()
    false_comments = serializers.IntegerField()
    courses = CommentSerializer(many=True)
    blogs = CommentSerializer(many=True)
    work_samples = CommentSerializer(many=True)
    posts = CommentSerializer(many=True)
    stories = CommentSerializer(many=True)
    services = CommentSerializer(many=True)

class SavedItemsSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    blogs = BlogSerializer(many=True)
    work_samples = WorkSampleSerializer(many=True)
    posts = PostSerializer(many=True)
    stories = StorySerializer(many=True)
    services = ServiceSerializer(many=True)

class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=250)
    sex = serializers.CharField(max_length=250)
    photo = serializers.IntegerField()




class UserDashboardSerializer(serializers.Serializer):
    profile = UserProfileSerializer()
    saved = serializers.DictField()
    comments = DashboardCommentSerializer()
    courses = CourseUserSerializer(many=True)
    transactions = TransactionSerializer(many=True)
    # saved = SavedItemSerializer(many=True)
    # comments = CommentSerializer(many=True)
    # purchased_courses = PurchasedCourseSerializer(many=True)