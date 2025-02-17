from django.db import models


class SiteFeature(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='site_feature_photo')
    icon = models.CharField(max_length=300, null=True, blank=True)
    text = models.TextField(max_length=3000, null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'info_site_features'
        ordering = ['id']
