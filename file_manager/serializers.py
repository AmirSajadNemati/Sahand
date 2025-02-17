from rest_framework import serializers

from Sahand import settings
from .models import FileManager

class FileTypeSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    label = serializers.CharField()
    extension = serializers.CharField()

class FileManagerBaseDataSerializer(serializers.Serializer):
    totalSize = serializers.IntegerField()
    totalSizeValue = serializers.CharField()
    usedSize = serializers.IntegerField()
    usedSizeValue = serializers.CharField()
    totalFile = serializers.IntegerField()
    totalFolder = serializers.IntegerField()
    fileTypes = FileTypeSerializer(many=True)

class FileAndFolderSerializer(serializers.ModelSerializer):
    # parentUrl = serializers.CharField(source='parentUrl', read_only=True)
    sizeValue = serializers.SerializerMethodField()
    updateRowDateValue = serializers.DateTimeField(source='updated_at', format="%Y-%m-%d %H:%M:%S")
    extension = serializers.SerializerMethodField()
    nameWithoutExtension = serializers.SerializerMethodField()
    iconUrl = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    typeValue = serializers.SerializerMethodField()
    previewType = serializers.SerializerMethodField()

    class Meta:
        model = FileManager
        fields = [
            'id', 'parentUrl', 'name', 'size', 'sizeValue', 'updateRowDateValue',
            'extension', 'nameWithoutExtension', 'iconUrl', 'type', 'typeValue', 'previewType'
        ]

    def get_sizeValue(self, obj):
        size_in_bytes = obj.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024

    def get_extension(self, obj):
        return obj.name.split('.')[-1].lower() if not obj.is_folder and '.' in obj.name else ''

    def get_nameWithoutExtension(self, obj):
        return obj.name.rsplit('.', 1)[0] if not obj.is_folder and '.' in obj.name else obj.name

    def get_iconUrl(self, obj):
        if obj.is_folder:
            return "/static/icons/folder-icon.png"
        ext = self.get_extension(obj)
        if ext in ['jpg', 'png', 'gif']:
            return "/static/icons/image-icon.png"
        elif ext in ['mp4', 'avi']:
            return "/static/icons/video-icon.png"
        return "/static/icons/file-icon.png"

    def get_type(self, obj):
        return 2 if obj.is_folder else 1

    def get_typeValue(self, obj):
        return "Folder" if obj.is_folder else "File"

    def get_previewType(self, obj):
        if obj.is_folder:
            return "folder"
        ext = self.get_extension(obj)
        if ext in ['jpg', 'png', 'gif']:
            return "image"
        elif ext in ['mp4', 'avi']:
            return "video"
        return "file"


class FileManagerSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)  # Optional for updates
    parentUrl = serializers.CharField(max_length=500, required=False, allow_null=True)  # Parent folder path
    name = serializers.CharField(max_length=255)  # Folder/File name


class FileManagerSearchSerializer(serializers.Serializer):
    """Serializer for searching FileManager entries."""
    search = serializers.CharField(required=False, allow_blank=True, max_length=255)
    url = serializers.URLField(required=False, allow_null=True)
    file_type = serializers.IntegerField(default=1)

class BreadCrumbSerializer(serializers.Serializer):
    """Serializer for breadcrumb navigation."""
    id = serializers.IntegerField()
    name = serializers.CharField()

class ResponseDataSerializer(serializers.Serializer):
    """Main response serializer containing various data."""
    url = serializers.URLField(allow_null=True, required=False)
    breadCrumbs = BreadCrumbSerializer(many=True, required=False)
    fileAndFolders = FileAndFolderSerializer(many=True)
    baseData = FileManagerBaseDataSerializer()

class MessageResponseSerializer(serializers.Serializer):
    """Generic response serializer for messages."""
    message = serializers.CharField()
    id = serializers.IntegerField()

class TowerCommandMessageSerializer(serializers.Serializer):
    """Serializer for tower command messages."""
    message = serializers.CharField()

class IdRequestSerializer(serializers.Serializer):
    """Serializer for requests containing an ID."""
    id = serializers.IntegerField()

class UrlResponseSerializer(serializers.Serializer):
    """Serializer for URL response."""
    file_url = serializers.URLField()
