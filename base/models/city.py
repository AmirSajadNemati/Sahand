from django.db import models


class City(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    country = models.ForeignKey('base.Country', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='city_country')
    province = models.ForeignKey('base.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='city_province')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_city'