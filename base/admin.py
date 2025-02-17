from django.contrib import admin

# Register your models here.
from .models import SiteInfo


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'english_title', 'site_url']



admin.site.register(SiteInfo, SiteInfoAdmin)