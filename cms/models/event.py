from django.db import models

from file_manager.models import FileManager


class Event(models.Model):
    title = models.CharField(max_length=300, null=True)
    event_date = models.DateTimeField()
    is_holiday = models.BooleanField(null=True, blank=True, default=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    photos = models.JSONField(default=list, blank=True, null=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'cms_event'
        ordering = ['id']