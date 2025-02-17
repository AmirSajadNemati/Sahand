from rest_framework import serializers
from base.models import (BasePage, Branch, City, ContactInfo, Country, Faq, FaqCategory, Help, HelpCategory,
                         LayoutTag, Menu, PageSeo, Province, Setting, Slider, SpecialCategory,
                         SpecialGroupCategory, StaticContent, StaticPage, StaticForm, SiteInfo, Photo, AbstractContent)


# BasePage
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer


class BasePageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = BasePage
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class BasePageGetSerializer(serializers.Serializer):
    data = BasePageSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class BasePageListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = BasePageSerializer(many=True)
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# photo
class PhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Photo
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class PhotoGetSerializer(serializers.Serializer):
    data = PhotoSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class PhotoListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = PhotoSerializer(many=True)
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())
# Branch
class BranchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Branch
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class BranchGetSerializer(serializers.Serializer):
    data = BranchSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class BranchListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = BranchSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# City
class CitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    country_title = serializers.SerializerMethodField()  # Dynamically add the country title
    province_title = serializers.SerializerMethodField()  # Dynamically add the country title

    class Meta:
        model = City
        fields = "__all__"

    def get_country_title(self, obj):
        return obj.country.title if obj.country else None

    def get_province_title(self, obj):
        return obj.province.title if obj.province else None

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class CityGetSerializer(serializers.Serializer):
    data = CitySerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class CityListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = CitySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# ContactInfo
class ContactInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ContactInfo
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class ContactInfoGetSerializer(serializers.Serializer):
    data = ContactInfoSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class ContactInfoListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = ContactInfoSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Country
class CountrySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Country
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class CountryGetSerializer(serializers.Serializer):
    data = CountrySerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class CountryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = CountrySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Faq
class FaqSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Faq
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class FaqGetSerializer(serializers.Serializer):
    data = FaqSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class FaqListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = FaqSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# FaqCategory
class FaqCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = FaqCategory
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class FaqCategoryGetSerializer(serializers.Serializer):
    data = FaqCategorySerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class FaqCategoryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = FaqCategorySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Help
class HelpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Help
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class HelpGetSerializer(serializers.Serializer):
    data = HelpSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class HelpListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = HelpSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# HelpCategory
class HelpCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = HelpCategory
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class HelpCategoryGetSerializer(serializers.Serializer):
    data = HelpCategorySerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class HelpCategoryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = HelpCategorySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# LayoutTag
class LayoutTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = LayoutTag
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class LayoutTagGetSerializer(serializers.Serializer):
    data = LayoutTagSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class LayoutTagListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = LayoutTagSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Menu
class MenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Menu
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value

    def to_representation(self, instance):
        # Get the original serialized data
        data = super().to_representation(instance)

        # Replace `menu_type` integer with its corresponding label
        menu_type_display = dict(Menu.MENU_TYPE_CHOICES).get(instance.menu_type, None)
        data['menu_type'] = menu_type_display

        return data

class MenuGetSerializer(serializers.Serializer):
    data = MenuSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class MenuListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = MenuSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# PageSeo
class PageSeoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = PageSeo
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class PageSeoGetSerializer(serializers.Serializer):
    data = PageSeoSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class PageSeoListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = PageSeoSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Province
class ProvinceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    country_title = serializers.SerializerMethodField()

    class Meta:
        model = Province
        fields = "__all__"

    def get_country_name(self, obj):
        return obj.country.title if obj.country else None

    def validate_id(self, value):
        if value == 0:
            return None
        return value

    def to_representation(self, instance):
        # Get the original data
        data = super().to_representation(instance)

        # Replace the country ID with the country title, if country is not None
        if instance.country:
            data['country'] = instance.country.title
        else:
            data['country'] = None

        return data


class ProvinceGetSerializer(serializers.Serializer):
    data = ProvinceSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class ProvinceListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = ProvinceSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Setting
class SettingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Setting
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class SettingGetSerializer(serializers.Serializer):
    data = SettingSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class SettingListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = SettingSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# Slider
class SliderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Slider
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class SliderGetSerializer(serializers.Serializer):
    data = SliderSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class SliderListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = SliderSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# SpecialCategory
class SpecialCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SpecialCategory
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class SpecialCategoryGetSerializer(serializers.Serializer):
    data = SpecialCategorySerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class SpecialCategoryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = SpecialCategorySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# SpecialGroupCategory
class SpecialGroupCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SpecialGroupCategory
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class SpecialGroupCategoryGetSerializer(serializers.Serializer):
    data = SpecialGroupCategorySerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class SpecialGroupCategoryListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = SpecialGroupCategorySerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# StaticContent
class StaticContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = StaticContent
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class StaticContentGetSerializer(serializers.Serializer):
    data = StaticContentSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class StaticContentListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = StaticContentSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# StaticPage
class StaticPageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = StaticPage
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class StaticPageGetSerializer(serializers.Serializer):
    data = StaticPageSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class StaticPageListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = StaticPageSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# StaticForm
class StaticFormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = StaticForm
        fields = "__all__"

    def get_username(self, obj):
        return obj.user.full_name if obj.user else None

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class StaticFormGetSerializer(serializers.Serializer):
    data = StaticFormSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class StaticFormListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = StaticFormSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# SiteInfo
class SiteInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SiteInfo
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class SiteInfoGetSerializer(serializers.Serializer):
    data = SiteInfoSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class SiteInfoListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = SiteInfoSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())

# AbstractContent
class AbstractContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = AbstractContent
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            return None
        return value


class AbstractContentGetSerializer(serializers.Serializer):
    data = AbstractContentSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())

class AbstractContentListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = AbstractContentSerializer(many=True)
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())