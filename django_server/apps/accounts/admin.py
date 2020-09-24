from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Ouser,Contacts


@admin.register(Ouser)
class OuserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        ('基础信息', {'fields': (('username', 'email'), ('link','contact', 'password'))}),
        ('权限信息', {'fields': (('is_active', 'is_staff', 'is_superuser'),
                             'groups', 'user_permissions')}),
        ('重要日期', {'fields': (('last_login', 'date_joined'),)}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')

# @admin.register(Contacts)
# class ContactsAdmin(admin.ModelAdmin):
#     list_display = ('name','description','slug')
