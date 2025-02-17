from django.db import models


class SiteInfo(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    english_title = models.CharField(max_length=150, null=True, blank=True)
    site_url = models.CharField(max_length=150, null=True, blank=True)
    slogan = models.CharField(max_length=350, null=True, blank=True)
    developer_title = models.CharField(max_length=150, null=True, blank=True)
    developer_english_title = models.CharField(max_length=150, null=True, blank=True)
    developer_url = models.CharField(max_length=150, null=True, blank=True)
    logo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='setting_logo')
    fav_icon = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='fav_icon')
    small_logo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='small_logo')
    developer_logo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='dev_logo')
    white_logo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='white_logo')
    light_base_color = models.CharField(max_length=16, null=True, blank=True)
    light_second_color = models.CharField(max_length=16, null=True, blank=True)
    light_text_color = models.CharField(max_length=16, null=True, blank=True)
    light_box_color = models.CharField(max_length=16, null=True, blank=True)
    light_bg_color = models.CharField(max_length=16, null=True, blank=True)
    light_third_color = models.CharField(max_length=16, null=True, blank=True)
    dark_base_color = models.CharField(max_length=16, null=True, blank=True)
    dark_second_color = models.CharField(max_length=16, null=True, blank=True)
    dark_text_color = models.CharField(max_length=16, null=True, blank=True)
    dark_box_color = models.CharField(max_length=16, null=True, blank=True)
    dark_bg_color = models.CharField(max_length=16, null=True, blank=True)
    dark_third_color = models.CharField(max_length=16, null=True, blank=True)
    keywords = models.CharField(max_length=1500, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    robot_txt = models.CharField(max_length=1000, null=True, blank=True)
    video = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='setting_video')
    catalog_id = models.CharField(max_length=100, null=True, blank=True)
    features_selected = models.TextField(null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_site_info'
