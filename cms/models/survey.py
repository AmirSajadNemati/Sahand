from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    options = models.JSONField(null=True, blank=True)
    count_answer = models.IntegerField(default=0, null=True, blank=True)
    survey_items = models.JSONField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)  # Set on creation
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'cms_survey'
