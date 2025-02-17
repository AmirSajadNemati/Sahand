from rest_framework import serializers
from menu.serializers import MenuSerializer

class GetSiteInfoRequestSerializer(serializers.Serializer):
    url = serializers.CharField()
class ServerTimeSerializer(serializers.Serializer):
    time = serializers.TimeField()
    date = serializers.DateField()

class AppInfoSerializer(serializers.Serializer):
    logo = serializers.IntegerField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, required=False)
    slogan = serializers.CharField(allow_null=True, required=False)
    footerLogo = serializers.IntegerField(allow_null=True, required=False)
    englishTitle = serializers.CharField(allow_null=True, required=False)
    smallLogo = serializers.IntegerField(allow_null=True, required=False)
    whiteLogo = serializers.IntegerField(allow_null=True, required=False)

class DLListSerializer(serializers.Serializer):
    photo = serializers.IntegerField(allow_null=True, required=False)
    title = serializers.CharField(allow_null=True, required=False)
    url = serializers.CharField(allow_null=True, required=False)

class AppVersionSerializer(serializers.Serializer):
    year = serializers.IntegerField(allow_null=True, required=False)
    version = serializers.IntegerField(allow_null=True, required=False)
    versionShow = serializers.CharField(allow_null=True, required=False)
    requiredUpdate = serializers.BooleanField(allow_null=True, required=False)
    downloadList = DLListSerializer(many=True, allow_empty=True)

class AppColorSerializer(serializers.Serializer):
    lightBaseColor = serializers.CharField(allow_null=True, required=False)
    lightSecoundColor = serializers.CharField(allow_null=True, required=False)
    lightTextColor = serializers.CharField(allow_null=True, required=False)
    lightBoxColor = serializers.CharField(allow_null=True, required=False)
    lightBgColor = serializers.CharField(allow_null=True, required=False)
    lightThirdColor = serializers.CharField(allow_null=True, required=False)
    darkBaseColor = serializers.CharField(allow_null=True, required=False)
    darkSecoundColor = serializers.CharField(allow_null=True, required=False)
    darkTextColor = serializers.CharField(allow_null=True, required=False)
    darkBoxColor = serializers.CharField(allow_null=True, required=False)
    darkBgColor = serializers.CharField(allow_null=True, required=False)
    darkThirdColor = serializers.CharField(allow_null=True, required=False)

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    userName = serializers.CharField(allow_blank=True, required=False)
    fullName = serializers.CharField(allow_null=True, required=False)
    fullNameWithSex = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    phoneNumber = serializers.CharField(allow_null=True, required=False)
    photo = serializers.IntegerField(allow_null=True, required=False)
    balance = serializers.IntegerField(allow_null=True, required=False)
    inviteCount = serializers.IntegerField(allow_null=True, required=False)

class DeveloperSerializer(serializers.Serializer):
    logo = serializers.IntegerField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    englishTitle = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    url = serializers.URLField(allow_null=True, allow_blank=True, required=False)

class PanelInfoResponseSerializer(serializers.Serializer):
    isAuthorize = serializers.BooleanField(default=False)
    appInfo = AppInfoSerializer(allow_null=True)
    appVersion = AppVersionSerializer(allow_null=True)
    appColor = AppColorSerializer(allow_null=True)
    profile = ProfileSerializer(allow_null=True)
    features_selected = serializers.JSONField()
    developer = DeveloperSerializer(allow_null=True)
    serverTime = ServerTimeSerializer(allow_null=True)
    countNotReadMessage = serializers.IntegerField(default=0)  # ✅ مقدار جدید برای تعداد پیام‌های خوانده‌نشده

class AppInfoResponseSerializer(serializers.Serializer):
    isAuthorize = serializers.BooleanField(default=False)
    appInfo = AppInfoSerializer(allow_null=True)
    appVersion = AppVersionSerializer(allow_null=True)
    appColor = AppColorSerializer(allow_null=True)
    profile = ProfileSerializer(allow_null=True)

class AppAuthorizeResponseSerializer(serializers.Serializer):
    isAuthorize = serializers.BooleanField(default=False)
    appInfo = AppInfoSerializer(allow_null=True)
    appVersion = AppVersionSerializer(allow_null=True)
    appColor = AppColorSerializer(allow_null=True)
    loginText = serializers.CharField(allow_null=True, required=False)
    loginPhotoLight = serializers.IntegerField(allow_null=True, required=False)
    loginPhotoDark = serializers.IntegerField(allow_null=True, required=False)

class SearchPanelRequestSerializer(serializers.Serializer):
    title = serializers.CharField()