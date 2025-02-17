from django.db import models

class SpecialGroupCategory(models.Model):
    special_category = models.ForeignKey('base.SpecialCategory', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='special_cat_gp_photo')
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_special_group_category'