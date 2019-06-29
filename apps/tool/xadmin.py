from django.contrib import xadmin
from .models import  ToolLink
from django.conf import settings


# Register your models here.
if settings.TOOL_FLAG:
    @admin.register(ToolLink)
    class ToolLinkAdmin(admin.ModelAdmin):
        list_display = ('name', 'description', 'link', 'order_num','category')


