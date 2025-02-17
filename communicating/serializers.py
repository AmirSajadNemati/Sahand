from rest_framework import serializers
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer
from communicating.models import Consult, AnswerConsult, RequestConsult

# region Consult
class ConsultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Consult
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value

class ConsultGetSerializer(serializers.Serializer):
    data = ConsultSerializer()  
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class ConsultListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  
    next = serializers.CharField(allow_null=True)  
    previous = serializers.CharField(allow_null=True)  
    data = ConsultSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
    
# endregion

#region AnswerConsult  
class AnswerConsultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = AnswerConsult
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value

class AnswerConsultGetSerializer(serializers.Serializer):
    data = AnswerConsultSerializer() 
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class AnswerConsultListSerializer(serializers.Serializer):
    count = serializers.IntegerField() 
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)  
    data = AnswerConsultSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
    
 #region RequestConsult   
class RequestConsultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = RequestConsult
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class RequestConsultGetSerializer(serializers.Serializer):
    data = RequestConsultSerializer()  
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class RequestConsultListSerializer(serializers.Serializer):
    count = serializers.IntegerField()  
    next = serializers.CharField(allow_null=True)  
    previous = serializers.CharField(allow_null=True) 
    data = RequestConsultSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
    
# endregion
