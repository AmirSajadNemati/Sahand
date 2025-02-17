from django.core.validators import RegexValidator
from django.db import models


class BasePage(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    headers = models.JSONField(null=True, blank=True, default=list)
    keywords = models.JSONField(null=True, blank=True, default=list)
    url = models.CharField(max_length=300, null=True, blank=True, unique=True, validators=[
            RegexValidator(
                regex=r'^[^_]*$',
                message="Underscores are not allowed in the title."
            )
        ])
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='base_content')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_base_page'