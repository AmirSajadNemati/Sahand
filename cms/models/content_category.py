from django.db import models

from file_manager.models import FileManager


class ContentCategory(models.Model):
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    title = models.CharField(max_length=300, null=True, blank=True)
    english_title = models.CharField(max_length=300, null=True, blank=True)
    photo = models.ForeignKey(FileManager, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='content_category_photo')
    count_blog = models.IntegerField(null=True, blank=True)
    count_video = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=3000, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'cms_content_category'
        ordering = ['id']

    def __str__(self):
        return self.title
