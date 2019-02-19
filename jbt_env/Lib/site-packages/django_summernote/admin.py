from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.db import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.settings import summernote_config, get_attachment_model

__widget__ = SummernoteWidget if summernote_config['iframe'] \
    else SummernoteInplaceWidget


class SummernoteModelAdminMixin(object):
    summernote_fields = '__all__'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if self.summernote_fields == '__all__':
            if isinstance(db_field, models.TextField):
                kwargs['widget'] = __widget__
        else:
            if db_field.name in self.summernote_fields:
                kwargs['widget'] = __widget__

        return super(SummernoteModelAdminMixin, self).formfield_for_dbfield(db_field, **kwargs)


class SummernoteInlineModelAdmin(SummernoteModelAdminMixin, InlineModelAdmin):
    pass


class SummernoteModelAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    pass


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'uploaded']
    search_fields = ['name']
    ordering = ('-id',)

    def save_model(self, request, obj, form, change):
        obj.name = obj.file.name if (not obj.name) else obj.name
        super(AttachmentAdmin, self).save_model(request, obj, form, change)


admin.site.register(get_attachment_model(), AttachmentAdmin)
