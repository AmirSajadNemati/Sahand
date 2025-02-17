from django.db import models
from django.core.validators import RegexValidator


class Consult(models.Model):
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
    file = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='consult_file')
    count_view = models.IntegerField(default=0)
    form_fields = models.JSONField(default=dict)
    page_link = models.JSONField(default=dict)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(blank=True, null=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'communicating_consult'
