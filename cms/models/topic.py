from django.db import models

from security.models import User
from .content_category import ContentCategory
from file_manager.models import FileManager


class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_user = models.BooleanField()
    is_verify = models.BooleanField()
    content_category = models.ForeignKey(ContentCategory, on_delete=models.SET_NULL, null=True,
                                         related_name='topic_category')
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True)
    count_share = models.IntegerField(null=True, blank=True)
    count_comment = models.IntegerField(null=True, blank=True)
    count_like = models.IntegerField(null=True, blank=True)
    count_dislike = models.IntegerField(null=True, blank=True)
    count_view = models.IntegerField(null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    abstract = models.TextField(max_length=3000, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='topic_photo')
    last_update_date = models.DateTimeField()
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'cms_topic'
