from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class RequestConsult(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]

    user = models.ForeignKey('security.User', on_delete=models.CASCADE, null=True, blank=True,
                             related_name="req_consult_user")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    consult = models.ForeignKey('communicating.Consult', on_delete=models.CASCADE, null=True, blank=True,
                                related_name="req_consult_consult")
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'communicating_req_consult'
