from django.db import models


class Transaction(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    user = models.ForeignKey('security.User', on_delete=models.PROTECT, null=True, related_name='transaction_user')
    pay_time = models.DateTimeField(null=True, blank=True)
    pay_price = models.BigIntegerField(null=True, blank=True)
    authority = models.CharField(max_length=300, blank=True, null=True)
    ref_id = models.CharField(max_length=300, blank=True, null=True)
    pay_status = models.CharField(max_length=50, blank=True, null=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'payment_transaction'


# {
#     "status": true,
#     "url": "https://www.zarinpal.com/pg/StartPay/A000000000000000000000000000jjoxjoo6",
#     "authority": "A000000000000000000000000000jjoxjoo6"
# }