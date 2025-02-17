from django.db import models


class Banner(models.Model):
    BANNER_TYPE_CHOICES = [
        (1, 'Banner Pop-up'),
        (2, 'Big Banner'),
        (3, 'Wide Small Banner'),
        (4, 'Square Small Banner'),
        (5, 'Site Top Whole Banner'),
        (6, 'Wide Low Hight Banner'),
    ]
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    photo = models.ForeignKey('file_manager.FileManager', null=True, blank=True, on_delete=models.CASCADE)
    banner_type = models.PositiveIntegerField(choices=BANNER_TYPE_CHOICES, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=255, null=True, blank=True)
    content = models.ForeignKey('content_manager.ContentManager', null=True, blank=True, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title  # Display title in the Django admin or shell

    class Meta:
        db_table = 'cms_banner'