from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=500, null=True, blank=True)
    value = models.CharField(max_length=1000, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_setting'

