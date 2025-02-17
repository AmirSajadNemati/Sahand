from django.db import models


class Branch(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    country = models.ForeignKey('base.Country', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='branch_country')
    province = models.ForeignKey('base.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='branch_province')
    city = models.ForeignKey('base.City', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='branch_city')
    hour = models.TextField(null=True, blank=True)
    manager = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    branch_contact_details = models.TextField(null=True, blank=True)
    is_base = models.BooleanField(default=False)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_branch'
