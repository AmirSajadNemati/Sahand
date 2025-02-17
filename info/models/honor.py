from django.db import models


class Honor(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='honor_photo')
    order = models.IntegerField()
    text = models.TextField(max_length=3000, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'info_honor'
        ordering = ['id']
