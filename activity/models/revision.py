from django.db import models

from security.models import User


class Revision(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # bigInt NOT NULL
    user_push_token_id = models.BigIntegerField(null=True, blank=True)  # bigInt NOT NULL
    type = models.IntegerField()  # int NOT NULL
    table_name = models.CharField(max_length=100, null=True, blank=True)  # nvarchar(100) NULL
    record_id = models.BigIntegerField()  # bigInt NOT NULL
    data = models.TextField(null=True, blank=True)  # nvarchar(max) NULL
    base_data = models.CharField(max_length=500, null=True, blank=True)  # nvarchar(500) NULL
    create_row_date = models.DateTimeField(auto_now_add=True)  # datetime2(7) NOT NULL
    update_row_date = models.DateTimeField(auto_now=True)  # datetime2(7) NOT NULL
    is_deleted = models.BooleanField(default=False)  # bit NOT NULL
    status = models.IntegerField(default=1)  # int NOT NULL

    class Meta:
        db_table = 'activity_revision'
        verbose_name_plural = 'Revisions'

    def __str__(self):
        return f'Revision {self.id}'