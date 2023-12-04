from django.contrib import admin,messages
from .models import School,Department,Job, Employee, MonthN as Month,SalaryItem,Permission,Vacation,Permission_setting,Employee_month,Time_setting,Vacation_setting
from import_export.admin import ImportExportModelAdmin
from .resources import SalaryItemResource,PermResource,EmployeeResource,Employee_monthResource,Time_settingResource,JobResource
from django.utils.translation import ngettext
from django.contrib import admin, messages
from student.models import Student,Manager
from django.db.models import F,Count
from django.db.models import Min
from datetime import date,datetime,timedelta
from django.contrib.auth.hashers import make_password
from django.utils import formats
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect

try:
    active_month = Month.objects.get(active=True)
except Month.DoesNotExist:
    pass

# Adjust User Access ''''''''''''''''''''''''''''''''''''''''''
class HrEmployeesAndApprover:
    def has_module_permission(self, request):
        return self.has_permission(request)
    
    def has_view_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_add_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_permission(self, request, obj=None):
        if request.user.is_authenticated:
            user_code = request.user.code
            return user_code == 'mosaad' or user_code.startswith('hr') or user_code.startswith('m1') or user_code.startswith('m2')
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.code == "mosaad"

class HrEmployees:
    def has_module_permission(self, request):
        return self.has_permission(request)
    
    def has_view_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_add_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_permission(self, request, obj=None):
        if request.user.is_authenticated:
            user_code = request.user.code
            return user_code == 'mosaad' or user_code.startswith('hr')
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.code == "mosaad"
    
class HrAdmin:
    def has_module_permission(self, request):
        return self.has_permission(request)
    
    def has_view_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_add_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_permission(self, request, obj=None):
        if request.user.is_authenticated:
            user_code = request.user.code
            return user_code == 'mosaad'
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.code == "mosaad"

# FILTER All QUERYSETS
def get_filtered_queryset(request, model_class):
    qs = model_class.objects.all().order_by('-id')
    if request.user.code != 'mosaad':
        user_code = request.user.code[:4]
        employee = Employee.objects.get(code=request.user.code)

        code_filters = {
            'hrb0': dict(school='بنين'),
            'hrg0': dict(school__in=('بنات', 'Ig')),
            'm1b0': dict(school='بنين', dep_code=employee.dep_code,grade_code=employee.grade_code),
            'm1bd': dict(school='بنين', dep_code=employee.dep_code),
            'm2b0': dict(school='بنين', grade_code=employee.grade_code),
            'm1g0': dict(school__in=('بنات', 'Ig'), dep_code=employee.dep_code,grade_code=employee.grade_code),
            'm1gd': dict(school__in=('بنات', 'Ig'), dep_code=employee.dep_code),
            'm2g0': dict(school__in=('بنات', 'Ig'), grade_code=employee.grade_code),
            'm1s0': dict( dep_code=employee.dep_code,grade_code=employee.grade_code),
            'm1sd': dict( dep_code=employee.dep_code),
        }
        if user_code in code_filters:
            return qs.filter(**code_filters[user_code])
        else:
            # Handle default case when user code doesn't match any condition
            return qs.none()
    else:
        return qs

def get_restricted_actions(user_code):
    if user_code == 'mosaad':
        return []
    if user_code.startswith('hr'):
        return ['ok1', 'ok2', 'ok']
    if user_code.startswith('m1'):
        return ['ok2', 'ok', 'refused']
    if user_code.startswith('m2'):
        return ['ok1']
    return None

class SchoolAdmin(HrAdmin,ImportExportModelAdmin):
    list_display = ('school','count')

class JobAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('__str__','employee_count','grade','department','title')
    filter_horizontal = ()
    search_fields = ('title',)
    list_filter = ('type','grade','department')

    resource_class = JobResource

    def employee_count(self, obj):
        return obj.employee_set.count()

    # Customize the column name in the admin
    employee_count.short_description = 'عدد الموظفين'

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(employee_count=Count('employee')).order_by('-employee_count')
        return qs

    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)
    
class DepartmentAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('name',)
    filter_horizontal = ()
    search_fields = ('name',)
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls') or request.user.code[:2] in ('hr',):
                return True
            return False

    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)
    
class SalaryItemAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('employee','item','value', 'month')
    autocomplete_fields = ['employee'] 
    readonly_fields = ('created',)
    filter_horizontal = ()
    search_fields = ('employee__code','employee__name','item')
    list_filter = ('school','month',)

    list_per_page = 30

    def get_queryset(self, request):
        qs = get_filtered_queryset(request, SalaryItem)
        return qs
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('month',) + self.readonly_fields
        return self.readonly_fields

    resource_class = SalaryItemResource

    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)

class Employee_monthAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('employee','month','salary_value','permissions','vacations','vacations_s','absent_ok','absent','is_active')
    autocomplete_fields = ['employee']
    readonly_fields = ('school','employee','salary_value','permissions','vacations','vacations_s','month','absent','absent_ok','is_active')
    filter_horizontal = ()
    search_fields = ('employee__name','employee__code')
    list_filter = ('school','month','is_active')

    list_per_page = 30

    resource_class = Employee_monthResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user.code in ('mosaad'):
                return self.readonly_fields
            return self.readonly_fields
        return ('is_active',)

    def save_model(self, request, obj, form, change):
        try:
            # Check for duplicates
            existing_record = Employee_month.objects.filter(employee=obj.employee, month=obj.month).exclude(pk=obj.pk).first()
            if existing_record:
                raise ValidationError("السجل الشهري موجود بالفعل")
        except ValidationError as e:
            self.message_user(request, str(e), level=messages.ERROR)
            return
        super().save_model(request, obj, form, change)
                
    def get_queryset(self, request):
        qs = get_filtered_queryset(request, Employee_month)
        return qs

    def has_add_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.code in ('mosaad')
    
    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)
        
class Permission_settingAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('name','is_perms','is_morning','is_evening','is_between', 'perms','is_over')
    readonly_fields = ()
    filter_horizontal = ()
    search_fields = ('name',)
    list_filter = ()
    fieldsets = (
    ('', { 'fields': ('name','is_perms','is_over',('is_evening','is_between','is_morning'),( 'perms'))}),
                )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return tuple(readonly_fields) + ('name',) if obj is not None else tuple(readonly_fields)
       
    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)
        
class Vacation_settingAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('name','is_vacation','is_vacation_s','is_absent','time_in','time_in_perm','time_out', 'time_out_perm','saturday')
    readonly_fields = ()
    filter_horizontal = ()
    search_fields = ('name',)
    list_filter = ()
    fieldsets = (
    ('', { 'fields': ('name',('vacations','is_vacation'),('vacations_s','is_vacation_s'),('absents','is_absent','saturday'),('time_in','time_in_perm'),('time_out', 'time_out_perm'))}),
                )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return tuple(readonly_fields) + ('name',) if obj is not None else tuple(readonly_fields)
     
    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)

class Time_settingAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('name','date','time_in','time_in_perm','time_out', 'time_out_perm','dayoff')
    readonly_fields = ()
    filter_horizontal = ()
    search_fields = ('name__name',)
    list_filter = ('name','month','dayoff')
    fieldsets = (
    ('', { 'fields': ('name','month',('date','dayoff'),'time_in','time_in_perm','time_out', 'time_out_perm')}),
                )
    list_per_page = 30
    list_editable = ('dayoff',)
    resource_class=Time_settingResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('name', 'date')
        return qs
    
    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)

class PermissionAdmin(HrEmployeesAndApprover,ImportExportModelAdmin):
    list_display = ('employee','type', 'formatted_date','count','total','ok1','ok2','dep_code','grade_code')
    autocomplete_fields = ['employee']
    readonly_fields = ('school','created','ok1','ok2','start_time','end_time','count','total','dep_code','grade_code')
    filter_horizontal = ()
    search_fields = ('employee__code','employee__name')
    # list_filter = ('school','ok2','employee__job__department__name','month','type')
    list_filter = ('school','ok2','month','type')
    fieldsets = (
    ('', { 'fields': (('employee','type'),('month','date'))}),
                )
    list_per_page = 30
    resource_class = PermResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.ok2==True:
                return ('employee','type', 'date','month') + self.readonly_fields
            return self.readonly_fields
        return self.readonly_fields
    
    def get_queryset(self, request):
        qs = get_filtered_queryset(request, Permission)  # Use the function to filter the queryset
        return qs
    
    def formatted_date(self, obj):
        return formats.date_format(obj.date, "M-d")

    formatted_date.short_description = 'التاريخ'  # Set a custom column header name

    def get_list_display_links(self, request, obj=None):
        if request.user.code in ('mosaad',) or request.user.code[:2] == 'hr':
            return ('employee',)
        else:
            return None

    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)
    
    def save_model(self, request, obj, form, change):
        try:
            if not obj.month:
                obj.month = active_month

            employee = obj.employee

            try:
                employee_month = Employee_month.objects.get(employee=employee, month=obj.month)
            except Employee_month.DoesNotExist:
                raise ValidationError("لم يتم العثور على السجل الشهري للموظف")

            setting = employee.permission_setting

            if not setting:
                raise ValidationError("برجاء ضبط إعدادات اَذون الموظف")

            obj.school = employee.school
            obj.dep_code = employee.dep_code
            obj.grade_code = employee.grade_code
            obj.total = setting.perms
            obj.count = employee_month.permissions + 1

        except ValidationError as e:
            self.message_user(request, str(e), level="ERROR")
            return

        super().save_model(request, obj, form, change)

    actions = ['ok1','ok2','ok','refused']
    def get_actions(self, request):
        actions = super().get_actions(request)
        user_code = request.user.code
        restricted_actions = get_restricted_actions(user_code)
        for action in restricted_actions:
            actions.pop(action, None)
        return actions

    def process_approval(self, request, queryset, approval_type):
        updated = 0
        already_approved = 0
        not_updated = 0

        for obj in queryset:
            if approval_type == 'ok1':
                if not obj.ok2:
                    if not obj.ok1:
                        obj.ok1 = True
                        self.approve_obj(request, obj, 'تمت موافقة رئيس القسم')
                        updated += 1
                    else:
                        already_approved += 1
                else:
                    not_updated +=1

            elif approval_type == 'ok2':
                if not obj.ok2:
                    if obj.ok1:
                        obj.ok2 = True
                        self.approve_obj(request, obj, 'تمت موافقة ناظر المرحلة')
                        updated += 1
                    else:
                        not_updated += 1
                else:
                    already_approved += 1

            elif approval_type == 'ok':
                if not obj.ok2:
                    obj.ok2 = True
                    self.approve_obj(request, obj, 'تمت موافقة وكيل المدرسة')
                    updated += 1
                else:
                    already_approved += 1

        if updated > 0:
            self.message_user(request, ngettext(
                '%d تمت الموافقة على',
                '%d تمت الموافقة على',
                updated,
            ) % updated, messages.SUCCESS)

        if not_updated > 0:
            self.message_user(request, ngettext(
                '%d لا يمكن الموافقة على',
                '%d لا يمكن الموافقة على',
                not_updated,
            ) % not_updated, messages.ERROR)

        if already_approved > 0:
            self.message_user(request, ngettext(
                '%d تمت الموافقة من قبل على',
                '%d تمت الموافقة من قبل على',
                already_approved,
            ) % already_approved, messages.ERROR)

    def approve_obj(self, request, obj, message):
        obj.save()
        self.log_change(request, obj, message)
        if obj.ok2:  # Execute only if approval_type is "ok2" or "ok" and obj.ok2 is True
            employee_month = Employee_month.objects.get(employee=obj.employee,month=obj.month)
            employee_month.permissions += 1
            employee_month.save(update_fields=['permissions'])
            self.log_change(request, employee_month, f'منح إذن  {obj.type} رقم {obj.count} ')

    def ok1(self, request, queryset):
        self.process_approval(request, queryset, 'ok1')

    def ok2(self, request, queryset):
        self.process_approval(request, queryset, 'ok2')

    def ok(self, request, queryset):
        self.process_approval(request, queryset, 'ok')


    def refused(self, request, queryset):
            updated = 0
            for obj in queryset:
                if not obj.ok2:
                    obj.delete()
                else:
                    employee_month = Employee_month.objects.get(employee=obj.employee,month=obj.month)
                    employee_month.permissions -= 1
                    employee_month.save(update_fields=['permissions'])
                    self.log_change(request, employee_month, f'إلغاء إذن  {obj.type} رقم {obj.count} ')
                    obj.delete()
                updated += 1

            if updated != 0:
                self.message_user(request, ngettext(
                    '%d  تم رفض والغاء عدد ',
                    '%d  تم رفض والغاء عدد ',
                    updated,
                ) % updated, messages.SUCCESS)

    ok1.short_description = "موافقة رئيس القسم"
    ok2.short_description = "موافقة ناظر المرحلة"
    ok.short_description = "موافقة وكيل المدرسة"
    refused.short_description = "رفض والغاء الإذن"
   
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.ok2 == True and obj.month == active_month:
                employee_month = Employee_month.objects.get(employee=obj.employee,month=active_month)
                employee_month.permissions=F('permissions') - 1
                employee_month.save(update_fields=['permissions'])
                obj.delete()
            else:
                obj.delete()

    def delete_model(self, request, obj):
        if obj.ok2 == True and obj.month == active_month:
            employee_month = Employee_month.objects.get(employee=obj.employee,month=active_month)
            employee_month.permissions=F('permissions') - 1
            employee_month.save(update_fields=['permissions'])

            obj.delete()
        else:
            obj.delete()
        
class VacationAdmin(ImportExportModelAdmin):
    list_display = ('employee','type','DateFrom','DateTo','count','total','ok1','ok2','dep_code','grade_code')
    autocomplete_fields = ['employee'] 
    readonly_fields = ('created','ok1','ok2','count','total','days','dep_code','grade_code')
    filter_horizontal = ()
    search_fields = ('employee__code','employee__name')
    list_filter = ('school','ok2','month','type')
    fieldsets = (
    ('', { 'fields': (('employee','days'),('type','month'),('date_from','date_to'))}),
                )
    list_per_page = 30

    def DateFrom(self, obj):
        return formats.date_format(obj.date_from, "M-d")   
    def DateTo(self, obj):
        return formats.date_format(obj.date_to, "M-d")
    DateFrom.short_description = 'من'  # Set a custom column header name
    DateTo.short_description = 'إلى'  # Set a custom column header name

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.ok2==True:
                return ('employee','date_from','date_to','type','month',) + self.readonly_fields
            return self.readonly_fields
        return self.readonly_fields
    
    def get_queryset(self, request):
        qs = get_filtered_queryset(request, Vacation)  # Use the function to filter the queryset
        return qs

    # def view_photo_link(self, obj):
    #     if obj.photo:
    #         photo_url = obj.photo.url
    #         return format_html('<a href="{}" target="_blank">صورة</a>', photo_url)
    #     return ""

    # view_photo_link.short_description = "مرفق"

    def get_list_display_links(self, request, obj=None):
        if request.user.code in ('mosaad','hrboys','hrgirls') or request.user.code[:2] in ('hr',):
            self.list_display_links = ('employee',)
            return self.list_display_links
        else:
            self.list_display_links = None
            return self.list_display_links

    def save_model(self, request, obj, form, change):
        try:
            if not obj.month:
                obj.month = active_month
            employee = obj.employee

            try:
                employee_month = Employee_month.objects.get(employee=employee, month=obj.month)
            except Employee_month.DoesNotExist:
                raise ValidationError("لم يتم العثور على السجل الشهري للموظف")

            settings = employee.vacation_setting

            if not settings:
                raise ValidationError("برجاء ضبط إعدادات اجازات الموظف")

            obj.school = employee.school
            obj.dep_code = employee.dep_code
            obj.grade_code = employee.grade_code

            dayoff_settings = Time_setting.objects.filter(month=active_month, name=settings, dayoff=True)
            dayoffs = [setting.date for setting in dayoff_settings]
            days_count = 0
            days = []
            current_date = obj.date_from
            while current_date <= obj.date_to:
                # Check if the current date is not a day-off
                if current_date not in dayoffs:
                    days_count += 1
                    days.append(current_date.day)  # Add the day component to the 'days' list
                current_date += timedelta(days=1)

            obj.days = days
            obj.count = days_count

            if obj.type == 'إذن غياب':
                obj.total = settings.absents - employee_month.absent_ok
            elif obj.type == 'من الرصيد':
                obj.total = settings.vacations - employee.used_vacations
            else:
                obj.total = settings.vacations_s - employee.used_vacations_s

            super().save_model(request, obj, form, change)

        except ValidationError as e:
            self.message_user(request, str(e), level="ERROR")

    actions = ['ok1', 'ok2', 'ok', 'refused']   
    def get_actions(self, request):
        actions = super().get_actions(request)
        user_code = request.user.code
        restricted_actions = get_restricted_actions(user_code)
        for action in restricted_actions:
            actions.pop(action, None)
        return actions
    
    def ok1(self, request, queryset):
        updated = 0
        notupdated = 0
        useless = 0
        for obj in queryset:
            if not obj.ok2:
                if obj.ok1 == False:
                    obj.ok1 = True
                    obj.save()
                    self.log_change(request, obj, 'تمت موافقة رئيس القسم')
                    updated += 1
                else:
                    notupdated +=1
            else:
                useless +=1

        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم الموافقة على',
                '%d تم الموافقة على',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d تم الموافقة من قبل على',
                '%d تم الموافقة من قبل على',
                notupdated,
            ) % notupdated, messages.ERROR)
        if useless != 0:
            self.message_user(request, ngettext(
                '%d لا اهمية لموافقتك الان على',
                '%d لا اهمية لموافقتك الان على',
                useless,
            ) % useless, messages.ERROR)


    def ok2(self, request, queryset):
        updated = 0
        notupdated = 0
        already = 0

        for obj in queryset:
            if not obj.ok2:
                if obj.ok1:
                    dayoffs = int(obj.count)
                    employee = Employee.objects.get(id=obj.employee.id)
                    employee_month = Employee_month.objects.get(employee=employee, month=obj.month)

                    if obj.type == 'من الرصيد':
                        employee.used_vacations = F('used_vacations') + dayoffs
                        employee_month.vacations = F('vacations') + dayoffs
                    elif obj.type == 'مرضي':
                        employee.used_vacations_s = F('used_vacations_s') + dayoffs
                        employee_month.vacations_s = F('vacations_s') + dayoffs
                    elif obj.type == 'إذن غياب':
                        employee_month.absent_ok = F('absent_ok') + dayoffs

                    obj.ok2 = True
                    obj.save()  # Save changes to the 'Vacation' model
                    self.log_change(request, obj, 'تمت موافقة ناظر المرحلة')
                    
                    # Log the same message to 'employee_month'
                    self.log_change(request, employee_month, f'منح اجازة  {obj.type} {obj.count} يوم')

                    employee.save()  # Save changes to the 'Employee' model
                    employee_month.save()  # Save changes to the 'Employee_month' model
                    updated += 1
                else:
                    notupdated += 1
            else:
                already += 1

        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم الموافقة على',
                '%d تم الموافقة على',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d لم يتم موافقة رئيس القسم',
                '%d لم يتم موافقة رئيس القسم',
                notupdated,
            ) % notupdated, messages.ERROR)
        if already != 0:
            self.message_user(request, ngettext(
                '%d  تمت الموافقة من قبل',
                '%d  تمت الموافقة من قبل',
                already,
            ) % already, messages.ERROR)

    def ok(self, request, queryset):
        updated = 0
        already = 0

        for obj in queryset:
            if not obj.ok2:
                dayoffs = int(obj.count)
                employee = Employee.objects.get(id=obj.employee.id)
                employee_month = Employee_month.objects.get(employee=employee, month=obj.month)

                if obj.type == 'من الرصيد':
                    employee.used_vacations = F('used_vacations') + dayoffs
                    employee_month.vacations = F('vacations') + dayoffs
                elif obj.type == 'مرضي':
                    employee.used_vacations_s = F('used_vacations_s') + dayoffs
                    employee_month.vacations_s = F('vacations_s') + dayoffs
                elif obj.type == 'إذن غياب':
                    employee_month.absent_ok = F('absent_ok') + dayoffs

                obj.ok2 = True
                obj.save()  # Save changes to the 'Vacation' model
                self.log_change(request, obj, 'تمت موافقة وكيل المدرسة ')
                self.log_change(request, employee_month, f'منح اجازة  {obj.type} {obj.count} يوم')
                employee.save()  # Save changes to the 'Employee' model
                employee_month.save()  # Save changes to the 'Employee_month' model
                updated += 1
            else:
                already +=1

        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم الموافقة على',
                '%d تم الموافقة على',
                updated,
            ) % updated, messages.SUCCESS)
        if already != 0:
            self.message_user(request, ngettext(
                '%d  تمت الموافقة من قبل',
                '%d  تمت الموافقة من قبل',
                already,
            ) % already, messages.ERROR)

    def refused(self, request, queryset):
        deleted = 0
        for obj in queryset:
            if not obj.ok2:
                obj.delete()
            else:

                dayoffs = int(obj.count)
                employee = Employee.objects.get(id=obj.employee.id)
                employee_month = Employee_month.objects.get(employee=employee, month=obj.month)

                if obj.type == 'من الرصيد':
                    employee.used_vacations = F('used_vacations') - dayoffs
                    employee_month.vacations = F('vacations') - dayoffs
                elif obj.type == 'مرضي':
                    employee.used_vacations_s = F('used_vacations_s') - dayoffs
                    employee_month.vacations_s = F('vacations_s') - dayoffs
                elif obj.type == 'إذن غياب':
                    employee_month.absent_ok = F('absent_ok') - dayoffs

                obj.delete()
                self.log_change(request, employee_month, f'إلغاء اجازة  {obj.type} {obj.count} يوم')
                employee.save()  # Save changes to the 'Employee' model
                employee_month.save()  # Save changes to the 'Employee_month' model
            deleted += 1
     
        if deleted != 0:
            self.message_user(request, ngettext(
                '%d تم رفض وإلغاء عدد ',
                '%d تم رفض وإلغاء عدد',
                deleted,
            ) % deleted, messages.SUCCESS)


    ok1.short_description = "موافقة رئيس القسم"
    ok2.short_description = "موافقة ناظر المرحلة"
    ok.short_description = "موافقة وكيل المدرسة"
    refused.short_description = " رفض وإلغاء الاجازة"

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls') or request.user.code[:2] in ('hr','m1','m2'):
                return True
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False
        
    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)

class EmployeeAdmin(HrEmployees,ImportExportModelAdmin):
    list_display = ('name','job','permission_setting','vacation_setting','code','dep_code','grade_code','time_code','is_active')
    # autocomplete_fields = ['perms','vecation_role']
    raw_id_fields = ('job',)
    readonly_fields = ('birth_date','dep_code','grade_code','used_vacations','used_vacations_s')
    search_fields = ('code','name','na_id','insurance_no')
    filter_horizontal = ()
    list_filter = ('school','job__type','job__grade','is_educational','job__department','job__title')
    fieldsets = (
    ('بيانات الموظف', { 'fields': (('name','code'),'job',('na_id','birth_date','school'),('mobile_number','phone_number'),('emergency_phone','email'),'address',('basic_certificate','is_educational'),('notes','is_active'))}),
    ('بيانات التعاقد', {'fields': (('attendance_date','insurance_date'),('participation_date','contract_date'),'insurance_no',('salary_parameter','salary'),'message','time_code',('dep_code','grade_code'),'permission_setting','vacation_setting',('used_vacations','used_vacations_s'))}),
                )
    list_per_page = 50

    def get_queryset(self, request):
        qs = get_filtered_queryset(request, Employee)  # Use the function to filter the queryset
        return qs
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code','school') + self.readonly_fields
        return self.readonly_fields

    resource_class = EmployeeResource

    def has_import_permission(self, request):
        return request.user.code in ('mosaad',)

    def has_export_permission(self, request):
        return request.user.code in ('mosaad',)

    def manager_1(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[:2] != "m1":
                new_code = "m1" + obj.code[2:]
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                employee_acc.is_admin = True
                employee_acc.is_staff = True
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password", "is_staff", "is_admin"])
                self.log_change(request, obj, 'منح صلاحيات رئيس القسم')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم منح صلاحيات رئيس القسم الى',
                '%d تم منح صلاحيات رئيس القسم الى',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d بالفعل يمتلك منح صلاحيات رئيس القسم ',
                '%d بالفعل يمتلك منح صلاحيات رئيس القسم ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def manager_2(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[:2] != "m2":
                new_code = "m2" + obj.code[2:]
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                employee_acc.is_admin = True
                employee_acc.is_staff = True
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password", "is_staff", "is_admin"])
                self.log_change(request, obj, 'منح صلاحيات ناظر المرحلة')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم منح صلاحيات ناظر المرحلة الى',
                '%d تم منح صلاحيات ناظر المرحلة الى',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d بالفعل يمتلك صلاحيات ناظر المرحلة ',
                '%d بالفعل يمتلك صلاحيات ناظر المرحلة ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def manager_out(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[:2] == "m1" or obj.code[:2] == "m2":
                school = 'b' if obj.school == "بنين" else 'g'
                new_code = obj.na_id[1:3] + school + '0' + obj.code[4:]
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                employee_acc.is_admin = False
                employee_acc.is_staff = False
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password", "is_staff", "is_admin"])
                self.log_change(request, obj, 'سحب جميع صلاحيات الإدارة ')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم سحب جميع الصلاحيات من',
                '%d تم سحب جميع الصلاحيات من',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d لا يمتلك صلاحية الرئيس من الاساس ',
                '%d لا يمتلك صلاحية الرئيس من الاساس ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def general_manager(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[:2] == "m1":
                new_code = "m1s" + obj.code[3:]
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password"])
                self.log_change(request, obj, 'منح صلاحية إدارة المدرستين')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم منح صلاحية إدارة المدرستين الى',
                '%d تم منح صلاحية إدارة المدرستين الى',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d لا يمتلك صلاحية رئيس القسم ',
                '%d لا يمتلك صلاحية رئيس القسم ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def local_manager(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[:3] == "m1s":
                school = 'b' if obj.school == "بنين" else 'g'
                new_code = "m1" + school + obj.code[3:]
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password"])
                self.log_change(request, obj, 'سحب صلاحية إدارة المدرستين')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم سحب صلاحية إدارة المدرستين من',
                '%d تم سحب صلاحية إدارة المدرستين من',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d لا يمتلك صلاحية إدارة المدرستين ',
                '%d لا يمتلك صلاحية إدارة المدرستين ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def department_manager(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[:2] == "m1":
                new_code = obj.code[:3] + 'd' + obj.code[4:]
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password"])
                self.log_change(request, obj, 'منح صلاحية إدارة القسم')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم منح صلاحية إدارة القسم الى',
                '%d تم منح صلاحية إدارة القسم الى',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d لا يمتلك صلاحية رئيس القسم ',
                '%d لا يمتلك صلاحية رئيس القسم ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def normal_manager(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[3:4] == "d":
                new_code = obj.code[:3] + '0' + obj.code[4:]
                print(new_code)
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password"])
                self.log_change(request, obj, 'سحب صلاحية إدارة القسم')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم سحب صلاحية إدارة القسم من',
                '%d تم سحب صلاحية إدارة القسم من',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d لا يمتلك صلاحية إدارة القسم ',
                '%d لا يمتلك صلاحية إدارة القسم ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def Fix_job_code(self, request, queryset):
        # updated = queryset.update(verified=True)
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.job is not None:
                # school=obj.school
                # if school=="بنين":
                #     school="b"
                # elif school=="بنات":
                #     school="g"         
                job_dep = str(obj.job.department.id)
                job_grade = obj.job.grade
                # if obj.job.department.name == "المرحلة":
                #     code = school+job_grade
                # elif obj.job.department.name == "المدرسة":
                #     code = school
                # else:
                #     if job_grade !=None:
                #         code = school+job_grade + job_dep
                #     else:
                #         code = school+job_dep
                obj.dep_code=job_dep
                obj.grade_code=job_grade
                obj.save(update_fields=["dep_code","grade_code"])

                # Update related permissions
                related_permissions = Permission.objects.filter(employee=obj,month=active_month)
                related_permissions.update(dep_code=job_dep,grade_code=job_grade)

                # Update related vacations
                related_vacations= Vacation.objects.filter(employee=obj,month=active_month)
                related_vacations.update(dep_code=job_dep,grade_code=job_grade)

                updated +=1
            else:
                notupdated +=1

        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم التحقق من الكود الوظيفي',
                '%d تم التحقق من الكود الوظيفي',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d يجب تحديد الوظيفة أولاً',
                '%d يجب تحديد الوظيفة أولاً',
                notupdated,
            ) % notupdated, messages.ERROR)

    def Fix_birth_date(self, request, queryset):
        # updated = queryset.update(verified=True)
        updated = 0
        notupdated = 0

        for obj in queryset:
            na_id = obj.na_id
            if na_id[0] == "2" or na_id[0] =="3":
                if na_id[0] =="2":
                    year_prefix = '19'
                elif na_id[0] == "3":
                    year_prefix ='20'
                birth_date = datetime.strptime(year_prefix + na_id[1:3] + '-' + na_id[3:5] + '-' + na_id[5:7], '%Y-%m-%d').date()
                obj.birth_date = birth_date
                obj.save(update_fields=["birth_date"])
                updated +=1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d birth date was successfully update.',
                '%d birth date ware successfully update.',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d birth date not set.',
                '%d birth date not set.',
                notupdated,
            ) % notupdated, messages.ERROR)
    
    Fix_birth_date.short_description = 'ضبط  تاريخ الميلاد'    
    Fix_job_code.short_description = 'التحقق  من الكود الوظيفي'
    manager_1.short_description = 'منح صلاحيات رئيس قسم'
    manager_2.short_description = 'منح صلاحيات ناظر مرحلة'
    manager_out.short_description = 'سحب جميع صلاحيات الإدارة'
    general_manager.short_description = 'منح صلاحية إدارة المدرستين'
    local_manager.short_description = 'سحب صلاحية إدارة المدرستين'
    department_manager.short_description = 'منح صلاحية إدارة القسم'
    normal_manager.short_description = 'سحب صلاحية إدارة القسم'

    actions = ['manager_1','manager_2','department_manager','normal_manager','general_manager','local_manager','manager_out','Fix_job_code','Fix_birth_date']

    def delete_queryset(self, request, queryset):

            for obj in queryset:
                try:
                    employee = Student.objects.get(code=obj.code)
                    employee.delete()
                except Student.DoesNotExist:
                    pass
                obj.delete()
    # TO GRANT ACCESS FOR HR AND M1 AND M2 USERS IN PERMISION AND VACATIONS
    def has_view_permission(self, request, obj=None):
        return request.user.code in ('mosaad',) or request.user.code[:2] in ('hr','m1','m2')
 

class MonthAdmin(HrAdmin,ImportExportModelAdmin):
    list_display = ('code','active','published','status')
    filter_horizontal = ()
    readonly_fields = ('code','active','published',)
    fieldsets =(
        ('None', { 'fields': ('code','start_date','end_date','dayoff',('active','published'))}),
        )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by('id')
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code','start_date','end_date') + self.readonly_fields
        return self.readonly_fields

    actions = ['activate','MonthlyRecords','Create_Time_setting','publish']

    def get_actions(self, request):
        actions= super().get_actions(request)
        if request.user.is_authenticated:
            if request.user.code in ('mosaad',):
                return actions
            else:          
                return None

    def activate(self, request, queryset):
        count = 0
        for obj in queryset:
            count +=1
        if count > 1 :
            self.message_user(request,'لا يمكن فتح اكثر من شهر في نفس الفترة', messages.ERROR)
        else:
            if obj.active == True:
                self.message_user(request,'تم فتح الشهر من قبل', messages.ERROR)
            else:
                if obj.status == '3':
                    self.message_user(request,'تم إغلاق الشهر سابقاً ولا يمكن إعادة تفعيلة مرة اخرى', messages.ERROR)
                else:
                    old_month = True
                    try:
                        closed_month = Month.objects.get(active=True)
                        closed_month.active = False
                        closed_month.status= '2'
                        closed_month.save(update_fields=['active','status'])
                        self.log_change(request, closed_month, ' تم إنهاء الشهر ')
                    except Month.DoesNotExist:
                        old_month = False
                    obj.active = True
                    self.log_change(request, obj, ' تم فتح الشهر للتسجيل ')
                    obj.save(update_fields=['active'])
                    if old_month == True :
                        self.message_user(request,obj.code  + ' تم إنهاء شهر ' + closed_month.code +' وفتح  شهر  ', messages.SUCCESS)
                    else:
                        self.message_user(request,obj.code  + ' تم فتح شهر ', messages.SUCCESS)

    def MonthlyRecords(self, request, queryset):
        count = 0
        for obj in queryset:
            count += 1
            if count > 1:
                self.message_user(request, 'لا يمكن فتح اكثر من شهر في نفس الفترة', messages.ERROR)
            else:
                if obj.active == False:
                    self.message_user(request, 'تم فتح الشهر من قبل', messages.ERROR)
                else:
                    if obj.status == '3':
                        self.message_user(request, 'تم إغلاق الشهر سابقاً ولا يمكن إعادة تفعيله مرة أخرى', messages.ERROR)
                    else:
                        # Retrieve the active employees queryset
                        employees = Employee.objects.all()
                        new_records = []
                        existing_records_count = 0

                        for employee in employees:
                            # Check if an Employee_month record already exists for this employee and month
                            existing_record = Employee_month.objects.filter(employee=employee, month=obj).first()

                            if not existing_record:
                                # Create a new Employee_month object and add it to the list for bulk_create
                                new_record = Employee_month(
                                    employee=employee,
                                    school=employee.school,
                                    month=obj,
                                    is_active=employee.is_active,
                                )
                                new_records.append(new_record)
                            else:
                                existing_records_count += 1

                        # Bulk create the new Employee_month objects
                        Employee_month.objects.bulk_create(new_records)

                        created = len(new_records)
                        self.message_user(
                            request,
                            ngettext(
                                '%d Monthly Record was Created',
                                '%d Monthly Records were Created',
                                created,
                            ) % created,
                            messages.SUCCESS
                        )

                        if existing_records_count > 0:
                            self.message_user(
                                request,
                                f'{existing_records_count} existing Monthly Records were found and skipped.',
                                messages.WARNING
                            )

    def Create_Time_setting(self, request, queryset):
        count = 0
        vacation_names = set()  # To store the names of processed vacation settings

        for obj in queryset:
            count += 1

        if count > 1:
            self.message_user(request, 'لا يمكن انشاء مواعيد الحضور والانصراف لاكثر من شهر في نفس الوقت', messages.ERROR)
        else:
            for obj in queryset:
                if obj.start_date and obj.end_date:
                    # Loop through all vacation settings
                    vacation_settings = Vacation_setting.objects.all()
                    for vacation_setting in vacation_settings:
                        saturday = vacation_setting.saturday

                        # Loop through dates within the start_date and end_date of the selected Month
                        current_date = obj.start_date
                        while current_date <= obj.end_date:
                            # Create time_setting for the current vacation_setting
                            time_setting, created = Time_setting.objects.get_or_create(
                                name=vacation_setting,
                                date=current_date,
                                defaults={
                                    'time_in': vacation_setting.time_in,
                                    'time_out': vacation_setting.time_out,
                                    'time_in_perm': vacation_setting.time_in_perm,
                                    'time_out_perm': vacation_setting.time_out_perm,
                                    'month': obj,
                                    'dayoff': False,  # Default to False
                                }
                            )

                            if saturday:
                                if current_date.weekday() == 4 or current_date.weekday() == 5:  # Friday and Saturday
                                    time_setting.dayoff = True
                                    time_setting.save()
                            else:
                                if current_date.weekday() == 4:  # Friday
                                    time_setting.dayoff = True
                                    time_setting.save()

                            # Add the name to the set of vacation names
                            vacation_names.add(f'"{vacation_setting.name}"')

                            # Move to the next date
                            current_date += timedelta(days=1)

            # Convert the set of vacation names to a string
            vacation_names_str = ' و '.join(vacation_names)

            message = f'تم انشاء جداول الحضور والانصراف الافتراضية لفئات {vacation_names_str}'
            self.message_user(request, message)

    def publish(self, request, queryset):
        count = 0
        for obj in queryset:
            count +=1
        if count > 1 :
            self.message_user(request,'لا يمكن نشر اكثر من شهر في نفس الفترة', messages.ERROR)
        else:
            if obj.status != '2' :
                self.message_user(request,'يجب إنهاء الشهر اولاً قبل النشر', messages.ERROR)
            else:
                if obj.published == True:
                    self.message_user(request,'تم نشر الشهر من قبل', messages.ERROR)
                else:
                    try:
                        published_month = Month.objects.get(published=True)
                        published_month.published = False
                        published_month.status = '3'
                        published_month.save(update_fields=['published','status'])
                        self.log_change(request, published_month, ' تم إيقاف النشر ')
                    except Month.DoesNotExist:
                        pass
                    obj.published = True
                    self.log_change(request, obj, 'تم النشر')
                    obj.save(update_fields=['published'])
                    self.message_user(request,obj.code  + 'تم عرض بيانات الشهر للموظفين', messages.SUCCESS)

    activate.short_description = 'إعداد الشهر لبداية التسجيل'
    publish.short_description = 'عرض بيانات شهر للموظفين'
    MonthlyRecords.short_description = 'إنشاء السجلات الشهرية للموظفين'
    Create_Time_setting.short_description = 'انشاء جداول الحضور والانصراف الافتراضية'



admin.site.register(School,SchoolAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Month,MonthAdmin)
admin.site.register(SalaryItem,SalaryItemAdmin)
admin.site.register(Permission,PermissionAdmin)
admin.site.register(Vacation,VacationAdmin)
admin.site.register(Permission_setting,Permission_settingAdmin)
admin.site.register(Employee_month,Employee_monthAdmin)
admin.site.register(Time_setting,Time_settingAdmin)
admin.site.register(Vacation_setting,Vacation_settingAdmin)