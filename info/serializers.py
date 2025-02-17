from rest_framework import serializers

from info.models import Colleague, CustomerComment, Honor, SiteFeature, Statistic, Team, TimeLine, WhyUs
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer

#Colleague
class ColleagueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    

    class Meta:
        model = Colleague
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class ColleagueGetSerializer(serializers.Serializer):
    data = ColleagueSerializer()  # This includes the fields from the ColleagueSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class ColleagueListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = ColleagueSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# category
class CustomerCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = CustomerComment
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class CustomerCommentGetSerializer(serializers.Serializer):
    data = CustomerCommentSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class CustomerCommentListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = CustomerCommentSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# event
class HonorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Honor
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class HonorGetSerializer(serializers.Serializer):
    data = HonorSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class HonorListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = HonorSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# story
class SiteFeatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SiteFeature
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class SiteFeatureGetSerializer(serializers.Serializer):
    data = SiteFeatureSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class SiteFeatureListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = SiteFeatureSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# survey
class StatisticSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Statistic
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class StatisticGetSerializer(serializers.Serializer):
    data = StatisticSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class StatisticListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = StatisticSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# video
class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Team
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class TeamGetSerializer(serializers.Serializer):
    data = TeamSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class TeamListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = TeamSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# voice
class TimeLineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TimeLine
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class TimeLineGetSerializer(serializers.Serializer):
    data = TimeLineSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class TimeLineListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = TimeLineSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# topic
class WhyUsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = WhyUs
        fields = '__all__'

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class WhyUsGetSerializer(serializers.Serializer):
    data = WhyUsSerializer()  # This includes the fields from the BlogSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class WhyUsListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = WhyUsSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())