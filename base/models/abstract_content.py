from django.core.validators import RegexValidator
from django.db import models


class AbstractContent(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    CONTENT_TYPE_CHOICES = [
        (1, 'AboutUs'),
        (2, 'WhyUs'),
        (3, 'Services'),
        (4, 'ّFaq'),
        (5, 'Blog'),
        (6, 'Comment'),
        (7, 'Team'),
        (8, 'WorkSample'),
        (9, 'Statistic'),
        (10, 'Header'),
        (11, 'Course'),
        (12, 'Teach/Hire'),
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
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.PROTECT, null=True, blank=True,
                                related_name='abstract_content_content')
    content_type = models.PositiveIntegerField(choices=CONTENT_TYPE_CHOICES)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'base_abstract_content'
