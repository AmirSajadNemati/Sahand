from django.core.validators import RegexValidator
from django.db import models


class TaskRequest(models.Model):
    STATUS_CHOICES = [
        (1, 'Ready to start'),
        (2, 'In progress'),
        (3, 'Waiting for review'),
        (4, 'Pending deploy'),
        (5, 'Done'),
        (6, 'Stuck'),
    ]
    PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
        (4, 'No Priority'),
    ]
    title = models.CharField(max_length=250)
    code = models.IntegerField(null=True, blank=True)
    pre_tasks = models.JSONField(default=dict)
    description = models.TextField(null=True, blank=True)
    todo_users = models.JSONField(default=dict)
    is_scheduled = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    file = models.ForeignKey('file_manager.FileManager', null=True, blank=True, related_name='task_req_file',
                             on_delete=models.SET_NULL)
    task_project = models.ForeignKey('task_manager.TaskProject', related_name='task_req_task_project',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    requires_sms = models.BooleanField(default=False)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, blank=True, null=True)
    note_list = models.JSONField(default=list)
    is_done = models.BooleanField(default=False)
    done_at = models.DateTimeField(blank=True, null=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'task_manager_request'
