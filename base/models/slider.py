from django.db import models


class Slider(models.Model):
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='slider_photo')
    order_num = models.IntegerField()
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_slider'