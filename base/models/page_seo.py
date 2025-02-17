from django.db import models


class PageSeo(models.Model):
    FREQUENCY_CHANGE_TYPE_CHOICES = [
        (1, 'یک روز'),  # One Day
        (2, 'یک ماه'),  # One Month
        (3, 'یک سال'),  # One Year
        (4, 'یک ساعت'),  # One Hour
    ]
    url = models.CharField(max_length=300, null=True, blank=True, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    robot = models.CharField(max_length=500, null=True, blank=True)
    frequency_change_type = models.IntegerField(choices=FREQUENCY_CHANGE_TYPE_CHOICES)
    priority = models.FloatField()
    description = models.CharField(max_length=500, null=True, blank=True)
    is_changed = models.BooleanField(default=False)
    last_check_date = models.DateTimeField()
    related_id = models.BigIntegerField()
    short_link = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=500, null=True, blank=True)
    category_show = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_page_seo'