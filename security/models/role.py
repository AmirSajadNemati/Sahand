from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    persian_name = models.CharField(max_length=100, null=True, blank=True)
    normalized_name = models.CharField(max_length=300, null=True, blank=True)
    features_selected = models.JSONField(default=dict)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'security_role'