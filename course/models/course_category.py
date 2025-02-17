
from django.db import models
from django.core.validators import RegexValidator

class CourseCategory(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True, unique=True,
                                     validators=[
                                         RegexValidator(
                                             regex=r'^[^_]*$',
                                             message="Underscores are not allowed in the title."
                                         )
                                     ]
                                     )
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True, related_name='course_category_photo')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'course_category'