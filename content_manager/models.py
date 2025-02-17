from django.db import models

# Create your models here.


class ContentManager(models.Model):
    content = models.TextField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'content_manager'  # Specify the table name here
        verbose_name = 'Content Manager'
        verbose_name_plural = 'Content Manager'
