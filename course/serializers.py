from datetime import timedelta

from rest_framework import serializers
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer
from course.models import Course, CourseCategory, Episode, EpisodeQA, CourseUser


# region course
class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Course
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class CourseGetSerializer(serializers.Serializer):
    data = CourseSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class CourseListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = CourseSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# endregion

# region CourseCategory
class CourseCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = CourseCategory
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class CourseCategoryGetSerializer(serializers.Serializer):
    data = CourseCategorySerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class CourseCategoryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = CourseCategorySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# region Episode
class EpisodeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Episode
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.time:
            total_seconds = int(instance.time.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            representation['time'] = f"{hours:02}:{minutes:02}:{seconds:02}"
        return representation


class EpisodeGetSerializer(serializers.Serializer):
    data = EpisodeSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class EpisodeListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = EpisodeSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# endregion

# region episode_qa
class EpisodeQASerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = EpisodeQA
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class EpisodeQAGetSerializer(serializers.Serializer):
    data = EpisodeQASerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class EpisodeQAListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = EpisodeQASerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# endregion
class CourseUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    course_photo = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    course_english_title = serializers.SerializerMethodField()
    course_rate = serializers.SerializerMethodField()

    class Meta:
        model = CourseUser
        fields = "__all__"

    def get_course_photo(self, obj):
        return obj.course.photo.id if obj.course.photo else None

    def get_course_title(self, obj):
        course = obj.course
        return course.title if course.title else None

    def get_course_english_title(self, obj):
        course = obj.course
        return course.english_title if course.english_title else None

    def get_course_rate(self, obj):
        course = obj.course
        return course.rate if course.rate else None

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class CourseUserGetSerializer(serializers.Serializer):
    data = CourseUserSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class CourseUserListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = CourseUserSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())