
from django.db import models

from file_manager.models import FileManager


class Story(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    photo = models.ForeignKey(FileManager, on_delete=models.SET_NULL, null=True, blank=True, related_name='story_photo')
    files = models.JSONField(default=dict)
    link = models.CharField(max_length=300, null=True, blank=True)
    story_details = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    count_share = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    publish_date = models.DateTimeField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'cms_story'


# SELECT TOP (1000) [Id]
#
#       ,[Abstract]
#
#   FROM [AGENT-Varna-OROD.DB].[content].[Posts]
