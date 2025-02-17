from django.core.validators import RegexValidator
from django.db import models


class WorkSample(models.Model):
    order = models.IntegerField(default=0)
    categories = models.JSONField(default=list)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='work_sample_photo')
    other_photos = models.JSONField(default=list, blank=True, null=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True, unique=True,
                                     validators=[
                                         RegexValidator(
                                             regex=r'^[^_]*$',
                                             message="Underscores are not allowed in the title."
                                         )
                                     ]
                                     )
    count_share = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    has_url = models.BooleanField(default=False)
    url = models.CharField(max_length=250, null=True, blank=True)
    customer = models.CharField(max_length=250, null=True, blank=True)
    services = models.JSONField(default=list, blank=True, null=True)
    abstract = models.TextField(max_length=3000, null=True, blank=True)
    tags = models.JSONField(default=list, blank=True, null=True)
    features = models.JSONField(default=list, blank=True, null=True)
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='work_sample_content')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'cms_work_sample'
        ordering = ['id']

