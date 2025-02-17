from rest_framework import serializers

from cms.models import Blog, ContentCategory, Event, Story, Survey, Video, Voice, Topic, TopicPost, Gallery, Service, \
    Banner, Post, WorkSample, Brand
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer


# blog
class BlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    rate = serializers.FloatField(required=False)
    content_category_title = serializers.SerializerMethodField()


    class Meta:
        model = Blog
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value

    def get_content_category_title(self, obj):
        # Check if we're dealing with a model instance or a serialized dictionary
        if hasattr(obj, 'content_category'):
            # obj is a Blog model instance
            return obj.content_category.title if obj.content_category else None
        elif isinstance(obj, dict):
            # obj is already a serialized dict (ReturnDict)
            # You can either return an existing key, or simply return None
            # If you want to compute it manually, you'll need to have the raw data available.
            return obj.get("content_category_title", None)
        return None


class BlogGetSerializer(serializers.Serializer):
    data = BlogSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class BlogListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = BlogSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# service

class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Service
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class ServiceGetSerializer(serializers.Serializer):
    data = ServiceSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class ServiceListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = ServiceSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# category
class ContentCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ContentCategory
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class ConetntCategoryGetSerializer(serializers.Serializer):
    data = ContentCategorySerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class ContentCategoryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = ContentCategorySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# event
class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Event
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class EventGetSerializer(serializers.Serializer):
    data = EventSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class EventListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = EventSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# story
class StorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Story
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class StoryGetSerializer(serializers.Serializer):
    data = StorySerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class StoryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = StorySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# survey
class SurveySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Survey
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class SurveyGetSerializer(serializers.Serializer):
    data = SurveySerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class SurveyListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = SurveySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# video
class VideoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Video
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class VideoGetSerializer(serializers.Serializer):
    data = SurveySerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class VideoListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = VideoSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# voice
class VoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Voice
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class VoiceGetSerializer(serializers.Serializer):
    data = VoiceSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class VoiceListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = VoiceSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# topic
class TopicSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Topic
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class TopicGetSerializer(serializers.Serializer):
    data = TopicSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class TopicListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = TopicSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# topic post
class TopicPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TopicPost
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class TopicPostGetSerializer(serializers.Serializer):
    data = TopicPostSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class TopicPostListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = TopicPostSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# gallery

class GallerySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Gallery
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class GalleryGetSerializer(serializers.Serializer):
    data = GallerySerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class GalleryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = GallerySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Banner

class BannerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Banner
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class BannerGetSerializer(serializers.Serializer):
    data = BannerSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class BannerListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = BannerSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())



# Post

class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class PostGetSerializer(serializers.Serializer):
    data = PostSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class PostListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = PostSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# service

class WorkSampleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = WorkSample
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class WorkSampleGetSerializer(serializers.Serializer):
    data = WorkSampleSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class WorkSampleListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = WorkSampleSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# brand

class BrandSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Brand
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class BrandGetSerializer(serializers.Serializer):
    data = BrandSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class BrandListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = BrandSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())