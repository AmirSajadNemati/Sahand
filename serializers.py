from rest_framework import serializers


class SearchFilterSerializer(serializers.Serializer):
    column = serializers.CharField()
    value = serializers.CharField()


class ListRequestSerializer(serializers.Serializer):
    sort = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    searches = SearchFilterSerializer(many=True, required=False)
    filters = SearchFilterSerializer(many=True, required=False)


class MessageAndIdSerializer(serializers.Serializer):
    message = serializers.CharField()
    id = serializers.IntegerField()


class GetModelSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    prentId = serializers.IntegerField(required=False)
    enName = serializers.CharField(required=False)


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class AttrSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.CharField()
    message = serializers.CharField()


class PropertyAttributeSerializer(serializers.Serializer):
    order = serializers.IntegerField()
    propertyName = serializers.CharField()
    propertyType = serializers.CharField()
    enumsSelect = serializers.ListField(child=serializers.CharField())
    isEnum = serializers.BooleanField()
    isEnumList = serializers.BooleanField()
    isFK = serializers.BooleanField()
    fkUrl = serializers.CharField()
    fknLevel = serializers.BooleanField()
    fkLevelEnd = serializers.BooleanField()
    fkParent = serializers.CharField()
    fkShow = serializers.CharField()
    fkMultiple = serializers.BooleanField()
    isFile = serializers.BooleanField()
    fileTypes = serializers.ListField(child=serializers.CharField())
    fileUrl = serializers.CharField()
    fileMultiple = serializers.BooleanField()
    isReadOnly = serializers.BooleanField()
    isNotShow = serializers.BooleanField()
    isHidden = serializers.BooleanField()
    dateType = serializers.CharField()
    isDate = serializers.BooleanField()
    isColor = serializers.BooleanField()
    isPrice = serializers.BooleanField()
    priceType = serializers.CharField(allow_null=True)
    isTag = serializers.BooleanField()
    isEditor = serializers.BooleanField()
    editorType = serializers.CharField(allow_null=True)
    isLocation = serializers.BooleanField()
    isList = serializers.BooleanField()
    listProperty = serializers.ListField(child=serializers.CharField())
    listError = serializers.ListField(child=serializers.CharField())
    locationType = serializers.CharField(allow_null=True)
    attribute = serializers.ListField(child=AttrSerializer())


class ListPropertiesAttributeSerializer(serializers.Serializer):
    propertyName = serializers.CharField()
    propertyType = serializers.CharField()
    isSearch = serializers.BooleanField()
    isFilter = serializers.BooleanField()
    isShow = serializers.BooleanField()
    isPrice = serializers.BooleanField()
    enumsSelect = serializers.ListField(child=serializers.CharField())
    isEnum = serializers.BooleanField()
    isFK = serializers.BooleanField()
    fkUrl = serializers.CharField()
    fkShow = serializers.CharField()
    fkMultiple = serializers.BooleanField()
    fkLevelEnd = serializers.BooleanField()
    fknLevel = serializers.BooleanField()
    fkParent = serializers.BooleanField()
    isDate = serializers.BooleanField()
    isRangeDate = serializers.BooleanField()
    showType = serializers.CharField()
    otherFieldName = serializers.CharField()
    propertyPersianName = serializers.CharField()
    isSort = serializers.BooleanField()
    isUrl = serializers.BooleanField()
    isCopy = serializers.BooleanField()
    statusFieldData = serializers.ListField(child=serializers.CharField())


class DeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.IntegerField()


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class UrlSerializer(serializers.Serializer):
    url = serializers.CharField()

