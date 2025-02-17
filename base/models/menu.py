from django.db import models


class Menu(models.Model):
    MENU_TYPE_CHOICES = [
        (1, 'Header'),
        (2, 'Responsive'),
        (3, 'Mega'),
        (4, 'Footer1'),
        (5, 'Footer2'),
        (6, 'Footer3'),
    ]
    title = models.CharField(max_length=250, null=True, blank=True)
    SITE_CHOICES = [
        (1, 'وارنا'),
        (2, 'وارناپاد'),
        (3, 'هردو')
    ]
    site = models.PositiveIntegerField(choices=SITE_CHOICES, default=1)
    url = models.CharField(max_length=300, null=True, blank=True)
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='menu_photo')
    icon = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='menu_icon')
    icon_lib = models.CharField(max_length=500, null=True, blank=True)
    icon_name = models.CharField(max_length=3000, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    menu_type = models.IntegerField(choices=MENU_TYPE_CHOICES, null=True, blank=True)
    order = models.IntegerField()
    category = models.CharField(max_length=300, null=True, blank=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField()

    class Meta:
        db_table = 'base_menu'
