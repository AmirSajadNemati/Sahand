from rest_framework import serializers

from security.models import User
from serializers import PropertyAttributeSerializer, ListPropertiesAttributeSerializer
from task_manager.models import TaskRequest, TaskProject, TaskDone, Notification


# region TaskRequest
class TaskRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    todo_users_detail = serializers.SerializerMethodField()

    class Meta:
        model = TaskRequest
        exclude = ['note_list']

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value

    def get_todo_users_detail(self, obj):
        todo_users = []
        for todo_user in obj.todo_users:
            try:
                user = User.objects.get(id=todo_user)
                todo_users.append(
                    {'id': user.id, 'full_name': user.full_name, 'photo': user.photo.id if user.photo else None})
            except User.DoesNotExist:
                pass
        return todo_users

    def update(self, instance, validated_data):
        """
        `note_list` را مستقیماً از `request.data` دریافت کرده و به‌روزرسانی می‌کنیم.
        """
        request_data = self.context['request'].data  # دریافت داده‌های خام از request

        # اگر `note_list` در درخواست وجود دارد، مقدار جدید را تنظیم کن
        if 'note_list' in request_data:
            instance.note_list = request_data['note_list']
            instance.save(update_fields=['note_list'])  # فقط این فیلد ذخیره شود

        # سایر فیلدها را طبق داده‌های تایید شده ذخیره کن
        return super().update(instance, validated_data)


class TaskRequestGetSerializer(serializers.Serializer):
    data = TaskRequestSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class TaskRequestListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = TaskRequestSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# endregion

# region TaskProject  
class TaskProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    members_detail = serializers.SerializerMethodField()
    managers_detail = serializers.SerializerMethodField()
    all_task_requests = serializers.SerializerMethodField()
    done_task_requests = serializers.SerializerMethodField()

    class Meta:
        model = TaskProject
        fields = "__all__"

    def get_members_detail(self, obj):
        members = []
        for member in obj.project_members:
            try:
                user = User.objects.get(id=member)
                members.append(
                    {'id': user.id, 'full_name': user.full_name, 'photo': user.photo.id if user.photo else None})
            except User.DoesNotExist:
                pass
        return members

    def get_managers_detail(self, obj):
        managers = []
        for manager in obj.project_managers:
            try:
                user = User.objects.get(id=manager)
                managers.append(
                    {'id': user.id, 'full_name': user.full_name, 'photo': user.photo.id if user.photo else None})
            except User.DoesNotExist:
                pass
        return managers

    def get_all_task_requests(self, obj):
        # Get the count of all task requests related to this TaskProject
        return TaskRequest.objects.filter(task_project=obj, is_deleted=False).count()

    def get_done_task_requests(self, obj):
        # Get the count of task requests with status '5' (Done) related to this TaskProject
        return TaskRequest.objects.filter(task_project=obj, status=5, is_deleted=False).count()

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class TaskProjectGetSerializer(serializers.Serializer):
    data = TaskProjectSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class TaskProjectListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = TaskProjectSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# region TaskDone   
class TaskDoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TaskDone
        fields = "__all__"

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class TaskDoneGetSerializer(serializers.Serializer):
    data = TaskDoneSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class TaskDoneListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = TaskDoneSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# endregion
# region

class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    send_to_detail = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_send_to_detail(self, obj):
        members = []
        for member in obj.send_to:
            try:
                user = User.objects.get(id=member)
                members.append(
                    {'id': user.id, 'full_name': user.full_name, 'photo': user.photo.id if user.photo else None})
            except User.DoesNotExist:
                pass
        return members

    def validate_id(self, value):
        if value == 0:
            # Treat id=0 as if the id wasn't provided
            return None
        return value


class NotificationGetSerializer(serializers.Serializer):
    data = NotificationSerializer()
    propertiesAttribute = serializers.ListField(child=PropertyAttributeSerializer())


class NotificationListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    data = NotificationSerializer()
    propertiesAttribute = serializers.ListField(child=ListPropertiesAttributeSerializer())


# endregion
class TaskProjectIdSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False)
    id = serializers.IntegerField(label="TaskProject ID",
                                  help_text="can be empty to retrieve all task requests of the user", required=False)


class TaskRequestNoteListSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False)
    id = serializers.IntegerField()