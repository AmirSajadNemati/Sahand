from django.db import models


class StaticContent(models.Model):
    STATIC_CONTENT_TYPE_CHOICES = [
        (1, 'هدر'),  # Header
        (2, 'فوتر'),  # Footer
        (3, 'چرا ما'),  # Why Us
        (4, 'مشاوره'),  # Consultation
        (5, 'آمار'),  # Statistics
        (6, 'درباره ما'),  # Statistics
        (7, 'Teach/Hire'),
    ]
    static_content_type = models.IntegerField(choices=STATIC_CONTENT_TYPE_CHOICES)
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='static_content_content')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.PROTECT, null=True, blank=True, related_name="static_content_photo")
    status = models.IntegerField()

    class Meta:
        db_table = 'base_static_content'