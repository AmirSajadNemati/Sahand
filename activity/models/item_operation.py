from django.db import models

from security.models import User


class ItemOperation(models.Model):
    OBJECT_TYPE_CHOICES = [
        (1, 'Course'),
        (2, 'Blog'),
        (3, 'WorkSample'),
        (4, 'Post'),
        (5, 'Story'),
        (6, 'Service')

    ]
    ITEM_OPERATION_TYPE_CHOICES = [
        (1, 'Like'),
        (2, 'DisLike'),
        (3, 'Save'),

    ]
    object_type = models.IntegerField(choices=OBJECT_TYPE_CHOICES)  # Equivalent to int NOT NULL
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # bigInt NOT NULL
    related_id = models.BigIntegerField()  # bigInt NOT NULL
    operation_date = models.DateTimeField(auto_now=True)  # datetime2(7) NOT NULL
    item_operation_type = models.IntegerField(choices=ITEM_OPERATION_TYPE_CHOICES)
    create_row_date = models.DateTimeField(auto_now_add=True)  # datetime2(7) NOT NULL
    update_row_date = models.DateTimeField(auto_now=True)  # datetime2(7) NOT NULL
    is_deleted = models.BooleanField(default=False)  # bit NOT NULL
    status = models.IntegerField()

    class Meta:
        db_table = 'activity_item_operation'  # Specify the database table name
        verbose_name_plural = 'ItemOperations'  # Optional: For admin display