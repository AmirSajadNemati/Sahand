from django.db import models

class Notification(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]

    title = models.CharField(max_length=250)
    link = models.CharField(max_length=250, null=True, blank=True)
    send_to = models.JSONField(default=dict)
    description = models.TextField(null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='notification_photo')
    is_read = models.BooleanField(default=False)
    related_section = models.CharField(max_length=250)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'task_manager_notification'
