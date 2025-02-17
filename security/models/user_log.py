from django.db import models

class UserLog(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("security.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='security_log_user')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    headers = models.TextField()
    operation = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'security_user_log'
        ordering = ['id']
