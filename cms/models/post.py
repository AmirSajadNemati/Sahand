from django.core.validators import RegexValidator
from django.db import models

class Post(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True, unique=True,
                                     validators=[
                                         RegexValidator(
                                             regex=r'^[^_]*$',
                                             message="Underscores are not allowed in the title."
                                         )
                                     ]
                                     )
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    user = models.ForeignKey('security.User', blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='post_user')
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='post_photo')
    video = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='post_video')
    other_photos = models.JSONField(default=list, blank=True, null=True)
    hashtag = models.TextField(blank=True, null=True)
    content = models.ForeignKey('content_manager.ContentManager', blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='post_user')
    post_type = models.PositiveIntegerField(default=1)
    count_share = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    publish_date = models.DateTimeField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'cms_post'