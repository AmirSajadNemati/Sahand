from django.db import models


class LayoutTag(models.Model):
    LAYOUT_TAG_STATUS_CHOICES = [
        (1, "تگ های بالای هدر"),  # Tags above the header
        (2, "تگ های پایین هدر"),  # Tags below the header
        (3, "تگ های بالای بادی"),  # Tags above the body
        (4, "تگ های پایین بادی"),  # Tags below the body
    ]

    # Choices for layout_tag_location_type
    LAYOUT_TAG_LOCATION_CHOICES = [
        (1, "عمومی"),  # Public
        (2, "صفحه خاص"),  # Specific page
    ]
    title = models.CharField(max_length=300, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    layout_tag_status_type = models.PositiveSmallIntegerField(choices=LAYOUT_TAG_STATUS_CHOICES)
    layout_tag_location_type = models.PositiveSmallIntegerField(choices=LAYOUT_TAG_LOCATION_CHOICES)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_layout'
