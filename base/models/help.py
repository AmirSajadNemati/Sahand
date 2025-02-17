from django.db import models


class Help(models.Model):
    help_category = models.ForeignKey('base.HelpCategory', on_delete=models.CASCADE, related_name='helps')
    title = models.CharField(max_length=250, null=True, blank=True)
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='help_content')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_help'
