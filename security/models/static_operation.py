from django.db import models


class StaticOperation(models.Model):
    OPERATION_TYPE_CHOICES = [
        (1, 'table'),
        (2, 'static'),
        (3, 'tree-node'),
        (4, 'tree-table')
    ]
    DATA_TYPE_CHOICES = [
        (1, 'page'),
        (2, 'modal')
    ]
    # COUNTED_TYPE_CHOICES = []
    key = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    icon_lib = models.CharField(max_length=500, null=True, blank=True)
    icon_name = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True)
    operation_type = models.PositiveIntegerField(choices=OPERATION_TYPE_CHOICES, null=True, blank=True)
    data_type = models.PositiveIntegerField(choices=DATA_TYPE_CHOICES, null=True, blank=True)
    # counted_type = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    order_num = models.IntegerField()
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_static_operation'
