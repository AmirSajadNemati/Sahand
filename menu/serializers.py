from rest_framework import serializers


class MenuSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    parent = serializers.IntegerField(allow_null=True)  # Store parent ID only
    icon_lib = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    icon_name = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    status = serializers.BooleanField()
    order_num = serializers.IntegerField()
    data_type = serializers.IntegerField(allow_null=True)
    operation_type = serializers.IntegerField(allow_null=True)
    is_deleted = serializers.BooleanField()
    children = serializers.ListField(child=serializers.DictField(), required=False)
