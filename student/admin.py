from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student
from fees.admin import FeesInline
from django.http import HttpResponse
import csv
from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from .resources import StudentResource
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class StudentAdmin(ImportExportMixin, UserAdmin):
    list_display = ('code', 'username', 'total_paid', 'payment_status')
    search_fields = ('code', 'username')
    readonly_fields = ( 'payment_status','last_login')

    # filter_horizontal = ()
    list_filter = ('school','grade', 'is_active','can_pay', 'bus_active')
    fieldsets = (
        (None, { 'fields': ('code', 'username', ('school', 'grade'),'password')}),
        # (None, { 'fields': (('is_staff','is_admin'),)}),
        ('المصروفات', {'fields': (('is_active', 'can_pay', 'bus_active'),('study_payment1', 'study_payment3', 'bus_payment2'),('total_paid','payment_status'), 'message')}),
        ('بيانات', {'fields': (('father_mobile','mother_mobile'),('phone_number', 'email'),('living_area', 'address', 'old_bus'), 'last_login')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
                 )
    resource_class = StudentResource

    def export_bus(self, request, queryset):

        meta = self.model._meta
        # field_names = [field.name for field in meta.fields]
        field_names = ['code', 'username', 'school', 'grade', 'old_bus', 'living_area', 'address']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=bus.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_bus.short_description = "Bus Data"



    def export_student(self, request, queryset):

        meta = self.model._meta
        # field_names = [field.name for field in meta.fields]
        field_names = ['code', 'username', 'school', 'grade']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Students.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_student.short_description = "تصدير بيانات الطلبة"



    actions = ["export_bus", "export_student"]

    inlines = [FeesInline]


admin.site.register(Student, StudentAdmin)

admin.site.site_header = "Manarat Al Farouk Islamic Language School"
