from django.db import models


class StaticForm(models.Model):
    STATIC_USER_TYPE_CHOICES = [
        (1, 'کاربر'),  # User
        (2, 'مهمان'),  # Guest
    ]

    # Choices for static_frm_type
    STATIC_FRM_TYPE_CHOICES = [
        (1, 'تماس با ما'),  # Contact Us
        (2, 'شکایت'),  # Complaint
        (3, 'پیشنهاد'),  # Suggestion
        (4, 'اعلام خطا'),  # Report Error
        (5, 'انتقاد'),  # Criticism
    ]

    static_user_type = models.IntegerField(choices=STATIC_USER_TYPE_CHOICES)
    static_frm_type = models.IntegerField(choices=STATIC_FRM_TYPE_CHOICES)
    user = models.ForeignKey('security.User', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='static_form_user')
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=3000, null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_static_form'
