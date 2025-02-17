from django.db import models


class TimeLine(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    year = models.IntegerField()
    month = models.IntegerField()
    photos = models.JSONField(default=list, blank=True, null=True)
    video = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='time_line_video')
    voice = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='time_line_voice')
    text = models.TextField(max_length=3000, null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'info_time_line'
        ordering = ['id']
