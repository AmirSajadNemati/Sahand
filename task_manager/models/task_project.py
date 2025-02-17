from django.core.validators import RegexValidator
from django.db import models


class TaskProject(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    PROJECT_STATUS_CHOICES = [
        (1, 'Done'),
        (2, 'Failed'),
        (3, 'Pending'),
        (4, 'No Task'),
    ]
    title = models.CharField(max_length=250)
    project_members = models.JSONField(default=dict)
    project_managers = models.JSONField(default=dict)
    description = models.TextField(null=True, blank=True)
    project_status = models.IntegerField(choices=PROJECT_STATUS_CHOICES, null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'task_manager_project'
