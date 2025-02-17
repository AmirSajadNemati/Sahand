from django.contrib import admin

from .models import User, Operation, StaticOperation


class OperationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent', 'icon_lib', 'icon_name', 'status', 'order_num')
    search_fields = ['title', 'url']
    list_editable = ['parent', 'status']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number']

    search_fields = ['username', 'phone_number']


class StaticOperationAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'operation_type', 'data_type']


admin.site.register(Operation, OperationAdmin)
admin.site.register(StaticOperation, StaticOperationAdmin)
admin.site.register(User, UserAdmin)
