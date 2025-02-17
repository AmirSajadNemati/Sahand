from django.utils import timezone
from rest_framework import serializers
import persian

# User
from security.models import User, Role, Operation, StaticOperation, UserLog
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    password = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class UserGetSerializer(serializers.Serializer):
    data = UserSerializer()  # This includes the fields from the UserSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class UserListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = UserSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# region role
class RoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Role
        exclude = ['features_selected']

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class RoleGetWithFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class RoleGetSerializer(serializers.Serializer):
    data = RoleGetWithFeatureSerializer()  # This includes the fields from the RoleSerializer
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class RoleListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  # Total number of items
    next = serializers.CharField(allow_null=True)  # URL for the next page, can be null
    previous = serializers.CharField(allow_null=True)  # URL for the previous page, can be null
    data = RoleSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# endregion


# Operation
class OperationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Operation
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class OperationGetSerializer(serializers.Serializer):
    data = OperationSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class OperationListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = OperationSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# StaticOp
class StaticOperationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = StaticOperation
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class StaticOperationGetSerializer(serializers.Serializer):
    data = StaticOperationSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class StaticOperationListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = OperationSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


class UserLogRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False)
    from_date = serializers.CharField(required=True)
    to_date = serializers.CharField(required=True)
    user_id = serializers.IntegerField(required=False)


class UserLogResponseSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()  # Override timestamp

    class Meta:
        model = UserLog
        fields = '__all__'

    def get_timestamp(self, obj):
        """ Convert Gregorian timestamp to Hijri format """
        if obj.timestamp:
            local_time = timezone.localtime(obj.timestamp)  # Convert to local timezone
            hijri_date = persian.from_gregorian(local_time.year, local_time.month, local_time.day)
            hijri_time = local_time.strftime("%H:%M:%S")  # Keep time format

            return f"{hijri_date[0]}-{hijri_date[1]:02d}-{hijri_date[2]:02d} {hijri_time}"
        return None
