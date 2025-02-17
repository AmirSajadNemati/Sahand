from django.core.validators import RegexValidator
from django.db import models


class Photo(models.Model):
    photo_type_choices = [
        (1, "slider"),  # Tags above the header
        (2, "mobile_slider"),  # Tags below the header
        (3, "square_ads"),  # Tags above the body
        (4, "wide_ads"),  # Tags below the body
        (5, "big_ads"),  # Tags below the body
    ]
    title = models.CharField(max_length=300, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True, unique=True, validators=[
        RegexValidator(
            regex=r'^[^_]*$',
            message="Underscores are not allowed in the title."
        )
    ])
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()
    file = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='base_photo')
    photo_type = models.PositiveSmallIntegerField(choices=photo_type_choices)

    class Meta:
        db_table = 'base_photo'
