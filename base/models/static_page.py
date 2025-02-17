from django.db import models


class StaticPage(models.Model):
    STATIC_PAGE_TYPE_CHOICES = [
        (1, 'درباره ما'),  # About Us
        (2, 'تماس با ما'),  # Contact Us
        (3, 'قوانین'),  # Rules
        (4, 'حفظ حریم خصوصی'),  # Privacy Policy
        (5, 'شکایت'),  # Complaint
        (6, 'انتقاد'),  # Criticism
        (7, 'اعلام خطا'),  # Report Error
        (8, 'پیشنهاد'),  # Suggestion
    ]

    static_page_type = models.IntegerField(choices=STATIC_PAGE_TYPE_CHOICES, null=True, blank=True)
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='static_page_content')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_static_page'
