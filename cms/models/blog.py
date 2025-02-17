from django.core.validators import RegexValidator
from django.db import models

from content_manager.models import ContentManager


class Blog(models.Model):
    BLOG_TYPE_CHOICES = [
        (1, 'مقاله متنی'),
        (2, 'مقاله ویدیویی')
    ]
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    content_category = models.ForeignKey('cms.ContentCategory', on_delete=models.SET_NULL, null=True,
                                         related_name='blog_category')
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True, unique=True,
                                     validators=[
                                         RegexValidator(
                                             regex=r'^[^_]*$',
                                             message="Underscores are not allowed in the title."
                                         )
                                     ]
                                     )
    user = models.ForeignKey('security.User', blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='blog_user')
    blog_type = models.PositiveIntegerField(choices=BLOG_TYPE_CHOICES, null=True, blank=True)
    abstract = models.TextField(max_length=3000, null=True, blank=True)
    features = models.TextField(max_length=3000, null=True, blank=True)
    time = models.IntegerField()  # Can be used to store time in seconds/minutes (as per your requirement)
    content = models.ForeignKey(ContentManager, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='blog_content')
    keywords = models.JSONField(null=True, blank=True, default=list)
    count_share = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='blog_photo')
    video = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='blog_video')
    publish_date = models.DateTimeField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'cms_blog'
        ordering = ['id']

    def __str__(self):
        return self.title
