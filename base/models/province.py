from django.db import models

class Province(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    country = models.ForeignKey('base.Country', on_delete=models.SET_NULL, blank=True, null=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_province'