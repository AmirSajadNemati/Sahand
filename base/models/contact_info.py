from django.db import models

class ContactInfo(models.Model):
    CONTACT_TYPE_CHOICES = [
        (1, "Telegram"),
        (2, "Whatsapp"),
        (3, "Instagram"),
        (4, "Email"),
        (5, "Site"),
        (6, "Tell"),
        (7, "Linkedin"),
    ]
    title = models.CharField(max_length=250, null=True, blank=True)
    value = models.CharField(max_length=700, null=True, blank=True)
    icon_name = models.CharField(max_length=3000, null=True, blank=True)
    contact_type = models.PositiveSmallIntegerField(choices=CONTACT_TYPE_CHOICES)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_contact_info'