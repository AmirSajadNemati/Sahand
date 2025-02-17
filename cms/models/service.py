from django.core.validators import RegexValidator
from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True, unique=True, validators=[
        RegexValidator(
            regex=r'^[^_]*$',
            message="Underscores are not allowed in the title."
        )
    ])
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='service_content')
    description = models.TextField(max_length=3000, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='service_photo')
    icon = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='service_icon')
    order = models.IntegerField(null=True, blank=True)
    count_share = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=18, decimal_places=3, null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'cms_service'
        ordering = ['id']
