from django.db import models


class CourseUser(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    course = models.ForeignKey('course.Course', on_delete=models.PROTECT, related_name='course_user_course')
    user = models.ForeignKey('security.User', on_delete=models.PROTECT, related_name='course_user_user')
    is_full = models.BooleanField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    transactions = models.JSONField(default=list)
    course_price = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    course_installment_count = models.PositiveIntegerField(null=True, blank=True)
    paid_installments = models.PositiveIntegerField(default=0)  # Track how many installments have been paid
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'course_user'
