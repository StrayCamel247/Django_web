from django.contrib import admin
from .models import FriendLink
# Register your models here.
# # 自定义管理站点的名称和URL标题

admin.site.site_header = '网站管理'
admin.site.site_title = '博客后台管理'

@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
        list_display = ('name', 'description', 'link', 'create_date', 'is_active', 'is_show')
        date_hierarchy = 'create_date'
        list_filter = ('is_active', 'is_show')