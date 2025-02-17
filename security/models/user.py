from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        (3, 'Suspended'),
        (4, 'Pending')
    ]
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField(choices=USER_STATUS_CHOICES, blank=True, null=True)
    about = models.TextField(max_length=1000, null=True, blank=True)
    concurrency_stamp = models.CharField(max_length=500, blank=True, null=True)
    security_stamp = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    sex = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    password_text = models.CharField(max_length=50, blank=True, null=True)
    phone_number_code = models.CharField(max_length=8, blank=True, null=True)
    count_send_sms = models.IntegerField(default=0)
    last_send_sms = models.DateTimeField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    job = models.CharField(max_length=150, blank=True, null=True)
    education = models.CharField(max_length=150, blank=True, null=True)
    national_code = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    has_login = models.BooleanField(default=False)
    balance = models.BigIntegerField(default=0)
    invited_user = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='invited_users')
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    phone_number_confirmed = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    lockout_end = models.DateTimeField(blank=True, null=True)
    lockout_enabled = models.BooleanField(default=False)
    access_failed_count = models.IntegerField(default=0)
    postal_code = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    is_support = models.BooleanField(null=True, blank=True)
    is_consult = models.BooleanField(null=True, blank=True)
    is_developer = models.BooleanField(null=True, blank=True)
    url_name = models.TextField(null=True, blank=True)
    roles = models.JSONField(default=dict)

    class Meta:
        db_table = 'security_user'

    def __str__(self):
        return self.username or self.full_name
