# ContentManager
from rest_framework import serializers

from content_manager.models import ContentManager
from serializers import ListPropertiesAttributeSerializer, PropertyAttributeSerializer


class ContentManagerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ContentManager
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class ContentManagerGetSerializer(serializers.Serializer):
    data = ContentManagerSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class ContentManagerListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = ContentManagerSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
