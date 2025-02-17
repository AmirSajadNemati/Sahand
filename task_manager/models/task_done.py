from django.core.validators import RegexValidator
from django.db import models


class TaskDone(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    is_done = models.BooleanField(default=False)
    done_at = models.DateTimeField(blank=True, null=True)
    done_by = models.JSONField(default=dict)
    task_request = models.ForeignKey('task_manager.TaskRequest', on_delete=models.SET_NULL,
                                     related_name='task_done_request', null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'task_manager_done'
