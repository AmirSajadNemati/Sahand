from rest_framework import serializers

from chat.models import Message
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Message
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class MessageGetSerializer(serializers.Serializer):
    data = MessageSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class MessageListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = MessageSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
