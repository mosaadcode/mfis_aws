from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ngettext
from .models import Fee
import csv
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from student.resources import FeesResource




class FeesInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = Fee
    can_delete = False
    # exclude = ('school',)
    # readonly_fields = [
    #     'verified'
    # ]
    extra = 0
    def has_change_permission(self, request, obj=None):
        return False
    # def has_add_permission(self, request, obj=None):
    # return False


class FeeAdmin(ImportExportModelAdmin):
    list_display = ('student', 'value', 'school', 'kind', 'bank_account', 'payment_date' , 'created','verified')
    # search_fields = ('student',)
    readonly_fields = ('created',)

    filter_horizontal = ()
    list_filter = ('verified','school', 'kind', 'payment_date','bank_account', 'created', )
    fieldsets = ()
    resource_class = FeesResource


    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        # field_names = ['value',]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    def verified(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, ngettext(
            '%d fee was successfully verified.',
            '%d fees were successfully verified.',
            updated,
        ) % updated, messages.SUCCESS)
    verified.short_description = "Ok Verified"

    def unverified(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(request, ngettext(
            '%d fee was successfully unverified.',
            '%d fees were successfully unverified.',
            updated,
        ) % updated, messages.SUCCESS)


    actions = ['export_as_csv','verified','unverified']



# class XeesAdmin(ImportExportModelAdmin):
#     pass
admin.site.register(Fee, FeeAdmin)
