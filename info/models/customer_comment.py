from django.db import models


class CustomerComment(models.Model):
    COMMENT_TYPE_CHOICES = [
        (1, 'متن'),  # Text
        (2, 'صوت'),  # Audio
        (3, 'Video'),  # Video
    ]

    title = models.CharField(max_length=250, null=True, blank=True)
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='customer_photo')
    comment_type = models.IntegerField(choices=COMMENT_TYPE_CHOICES)
    file = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='customer_file')
    text = models.TextField(max_length=3000, null=True, blank=True)
    comment_date = models.DateTimeField()
    page = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField()
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'info_customer_comment'
        ordering = ['id']
