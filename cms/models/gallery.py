from django.db import models

from .content_category import ContentCategory
from file_manager.models import FileManager


class Gallery(models.Model):
    content_category = models.ForeignKey(ContentCategory, on_delete=models.SET_NULL, null=True,
                                         related_name='gallery_category')
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='gallery_photo')
    large_photo = models.ForeignKey('file_manager.FileManager', related_name='gallery_large_photo',
                                    on_delete=models.SET_NULL,
                                    null=True, blank=True)
    other_photos = models.JSONField(default=list, blank=True, null=True)
    tags = models.JSONField(null=True, blank=True)
    abstract = models.TextField(max_length=3000, null=True, blank=True)
    count_share = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'cms_gallery'
