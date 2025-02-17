from django.db import models


class Message(models.Model):
    MESSAGE_STATUS_CHOICES = [
        (1, 'Send'),
        (2, 'Receive'),
        (3, 'Failed'),
    ]
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    text = models.TextField(null=True, blank=True)
    send_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('security.User', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='message_user')
    task_project = models.ForeignKey('task_manager.TaskProject', on_delete=models.CASCADE,
                                     related_name='message_task_project')
    message_status = models.PositiveIntegerField(choices=MESSAGE_STATUS_CHOICES)
    file = models.ForeignKey('file_manager.FileManager', null=True, blank=True, related_name='message_file',
                             on_delete=models.SET_NULL)
    voice = models.ForeignKey('file_manager.FileManager', null=True, blank=True, related_name='message_voice',
                              on_delete=models.SET_NULL)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'chat_message'
