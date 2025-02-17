# Comment
from rest_framework import serializers

from activity.models import Comment, ItemOperation, Revision, UserLog, UserSurvey
from course.models import Course
from serializers import ListPropertiesAttributeSerializer, PropertyAttributeSerializer
from cms.models import Blog, WorkSample, Post, Story, Service


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    object_type_title = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value

    def get_object_type_title(self, obj):
        """
        Helper method to get the title of the object_type.
        Handles both model instances and serialized data (dictionaries).
        """
        object_type_titles = {
            1: "Course",
            2: "Blog",
            3: "WorkSample",
            4: "Post",
            5: "Story",
            6: "Service",
        }

        # Check if obj is a dictionary (serialized data)
        if isinstance(obj, dict):
            object_type = obj.get('object_type')  # Use dictionary key access
        else:
            object_type = getattr(obj, 'object_type', None)  # Use attribute access for model instances

        return object_type_titles.get(object_type, "Unknown")


    def to_representation(self, instance):
        """
        Customize the serialized representation of the Comment model.
        Adds the 'english_title' field based on the object_type and related_id.
        """
        # Standard representation
        data = super().to_representation(instance)

        # Extract related_id and object_type from the serialized data
        related_id = data.get('related_id')
        object_type = data.get('object_type')

        # Determine 'english_title' based on object_type and related_id
        english_title = None

        if object_type == 1:  # Course
            related_object = Course.objects.filter(id=related_id).first()
            english_title = getattr(related_object, 'english_title', None)

        elif object_type == 2:  # Blog
            related_object = Blog.objects.filter(id=related_id).first()
            english_title = getattr(related_object, 'english_title', None)

        elif object_type == 3:  # WorkSample
            related_object = WorkSample.objects.filter(id=related_id).first()
            english_title = getattr(related_object, 'title', None)

        elif object_type == 4:  # Post
            related_object = Post.objects.filter(id=related_id).first()
            english_title = getattr(related_object, 'english_title', None)

        elif object_type == 5:  # Story
            related_object = Story.objects.filter(id=related_id).first()
            english_title = getattr(related_object, 'title', None)

        elif object_type == 6:  # Service
            related_object = Service.objects.filter(id=related_id).first()
            english_title = getattr(related_object, 'title', None)

        # Add 'english_title' to the serialized data
        data['english_title'] = english_title

        return data


class CommentGetSerializer(serializers.Serializer):
    data = CommentSerializer(required=False)  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class CommentListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = CommentSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# category
class ItemOperationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user_title = serializers.SerializerMethodField

    class Meta:
        model = ItemOperation
        fields = "__all__"

    def get_user_title(self, obj):
        return obj.user.full_name if obj.user.full_name else None

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class ItemOperationGetSerializer(serializers.Serializer):
    data = ItemOperationSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class ItemOperationListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = ItemOperationSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# event
class RevisionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Revision
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class RevisionGetSerializer(serializers.Serializer):
    data = RevisionSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class RevisionListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = RevisionSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# story
class UserSurveySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user_title = serializers.SerializerMethodField()
    survey_title = serializers.SerializerMethodField()

    class Meta:
        model = UserSurvey
        fields = '__all__'

    def get_user_title(self, obj):
        return obj.user.full_name if obj.user.full_name else None

    def get_survey_title(self, obj):
        return obj.survey.title if obj.survey else None

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class UserSurveyGetSerializer(serializers.Serializer):
    data = UserSurveySerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class UserSurveyListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = UserSurveySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# survey
class UserLogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user_title = serializers.SerializerMethodField()

    class Meta:
        model = UserLog
        fields = '__all__'

    def get_user_title(self, obj):
        return obj.user.full_name if obj.user.full_name else None

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class UserLogGetSerializer(serializers.Serializer):
    data = UserLogSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class UserLogListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = UserLogSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
