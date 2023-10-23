from django.contrib import admin
from .models import School,Department,Job, Employee, Month,SalaryItem,Permission,Vacation,Permission_setting,Employee_month,Time_setting,Vacation_setting,Time_template
from import_export.admin import ImportExportModelAdmin
from .resources import SalaryItemResource,PermResource,EmployeeResource,Employee_monthResource,Time_settingResource,JobResource
from django.utils.translation import ngettext
from django.contrib import admin, messages
from student.models import Student,Manager
from django.db.models import F
from django.db.models import Min
from datetime import date,datetime
from django.contrib.auth.hashers import make_password
from django.utils import formats

try:
    active_month = Month.objects.get(active=True)
except Month.DoesNotExist:
    pass

class SchoolAdmin(ImportExportModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad',):
                return True
            return False

class JobAdmin(ImportExportModelAdmin):
    # list_display = ('__str__','title','department')
    filter_horizontal = ()
    search_fields = ('title',)
    list_filter = ('type','grade','department')

    resource_class = JobResource
    
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    filter_horizontal = ()
    search_fields = ('name',)
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

class SalaryItemAdmin(ImportExportModelAdmin):
    list_display = ('employee','item','value', 'month')
    autocomplete_fields = ['employee'] 
    readonly_fields = ('created',)
    filter_horizontal = ()
    search_fields = ('employee__code','employee__name','item')
    list_filter = ('school','month',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "hrgirls":
            return qs.filter(school__in = ('بنات','Ig'))
        elif request.user.code =="hrboys":
            return qs.filter(school__in = ('بنين',))
        return qs
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('month',) + self.readonly_fields
        return self.readonly_fields

    resource_class = SalaryItemResource

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

class Employee_monthAdmin(ImportExportModelAdmin):
    list_display = ('employee','month','salary_value','permissions','vacations','is_active')
    # list_display_links = ('employee',)
    autocomplete_fields = ['employee']
    readonly_fields = ('school','employee','salary_value','permissions','vacations','month','is_active')
    filter_horizontal = ()
    search_fields = ('employee__name','employee__code')
    list_filter = ('school','month','is_active')
    # fieldsets = (
    # ('', { 'fields': ('employee','is_perms','is_over',('is_evening','is_between','is_morning'),( 'perms',))}),
    #             )

    resource_class = Employee_monthResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "hrgirls":
            return qs.filter(school__in = ('بنات','Ig'))
        elif request.user.code =="hrboys":
            return qs.filter(school__in = ('بنين',))
        return qs

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False
    def has_add_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad'):
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad'):
                return True
            return False
        
class Permission_settingAdmin(ImportExportModelAdmin):
    list_display = ('name','is_perms','is_morning','is_evening','is_between', 'perms','is_over')
    # list_display_links = ('employee',)
    # autocomplete_fields = ['employee']
    readonly_fields = ()
    filter_horizontal = ()
    search_fields = ('name',)
    list_filter = ()
    fieldsets = (
    ('', { 'fields': ('name','is_perms','is_over',('is_evening','is_between','is_morning'),( 'perms'))}),
                )


    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False
        
class Vacation_settingAdmin(ImportExportModelAdmin):
    list_display = ('name','is_vacation', 'vacations','vacations_s')
    # list_display_links = ('employee',)
    # autocomplete_fields = ['employee']
    readonly_fields = ()
    filter_horizontal = ()
    search_fields = ('name',)
    list_filter = ()
    fieldsets = (
    ('', { 'fields': ('name','is_vacation', 'vacations','vacations_s')}),
                )

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False
        
class Time_settingAdmin(ImportExportModelAdmin):
    list_display = ('name','date','time_in','time_in_perm','time_out', 'time_out_perm')
    # list_display_links = ('employee',)
    # autocomplete_fields = ['employee']
    readonly_fields = ()
    filter_horizontal = ()
    search_fields = ('name__name',)
    list_filter = ('name','month')
    fieldsets = (
    ('', { 'fields': ('name','month','date','time_in','time_in_perm','time_out', 'time_out_perm')}),
                )
    resource_class=Time_settingResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('name', 'date')
        return qs

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

class Time_templateAdmin(ImportExportModelAdmin):
    # list_display = ('__str__','title','department')
    filter_horizontal = ()
    search_fields = ()
    list_filter = ()
    
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False
    def has_add_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad'):
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad'):
                return True
            return False

class PermissionAdmin(ImportExportModelAdmin):
    list_display = ('employee','type', 'formatted_date','reason','count','total','ok1','ok2','job_code')
    # list_display_links = ('employee',)
    autocomplete_fields = ['employee']
    readonly_fields = ('school','created','reason','ok1','ok2','start_time','end_time','count','total')
    filter_horizontal = ()
    search_fields = ('employee__code','employee__name')
    list_filter = ('school','month','type')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.ok2==True:
                return ('employee','type', 'date','month') + self.readonly_fields
            return self.readonly_fields
        return self.readonly_fields
    
    def formatted_date(self, obj):
        # Use the formats.date_format function to format the date as "M.dd"
        return formats.date_format(obj.date, "M-d")

    formatted_date.short_description = 'التاريخ'  # Set a custom column header name

    def ok1(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.ok1 == False:
                obj.ok1 = True
                obj.save()
                self.log_change(request, obj, 'تم موافقة الرئيس المباشر')
                updated += 1
            else:
                notupdated +=1
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

    def ok2(self, request, queryset):
            updated = 0
            notupdated = 0
            for obj in queryset:
                if obj.ok1 == True:
                    obj.ok2 = True
                    obj.save()
                    employee_month = Employee_month.objects.get(employee=obj.employee,month=active_month)
                    employee_month.permissions=F('permissions') + 1
                    employee_month.save(update_fields=['permissions'])
                    self.log_change(request, obj, 'تم موافقة الرئيس الأعلى')
                    updated += 1
                else:
                    notupdated +=1
            if updated != 0:
                self.message_user(request, ngettext(
                    '%d تم الموافقة على',
                    '%d تم الموافقة على',
                    updated,
                ) % updated, messages.SUCCESS)
            if notupdated != 0:
                self.message_user(request, ngettext(
                    '%d لم يتم موافقة الرئيس المباشر',
                    '%d لم يتم موافقة الرئيس المباشر',
                    notupdated,
                ) % notupdated, messages.ERROR)

    def ok(self, request, queryset):
            updated = 0
            notupdated = 0
            for obj in queryset:
                if obj.ok2 == False:
                    obj.ok2 = True
                    obj.save()
                    employee_month = Employee_month.objects.get(employee=obj.employee,month=active_month)
                    employee_month.permissions=F('permissions') + 1
                    employee_month.save(update_fields=['permissions'])
                    self.log_change(request, obj, ' موافقة مباشرة')
                    updated += 1
                else:
                    notupdated +=1
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

    def refused(self, request, queryset):
            updated = 0
            notupdated = 0
            for obj in queryset:
                if obj.ok1 == False and obj.ok2== False:
                    obj.delete()
                    updated += 1
                else:
                    notupdated +=1
            if updated != 0:
                self.message_user(request, ngettext(
                    '%d تم رفض ',
                    '%d تم رفض',
                    updated,
                ) % updated, messages.SUCCESS)
            if notupdated != 0:
                self.message_user(request, ngettext(
                    '%d لا يمكن رفض ',
                    '%d لا يمكن رفض ',
                    notupdated,
                ) % notupdated, messages.ERROR)

    ok1.short_description = "موافقة الرئيس المباشر"
    ok2.short_description = "موافقة الرئيس الأعلى"
    ok.short_description = "موافقة مباشرة"
    refused.short_description = "رفض الإذن"

    actions = ['ok1','ok2','ok','refused']

    def get_actions(self, request):
        actions= super().get_actions(request)
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls') or request.user.code[:2] in ('hr',):
                return actions
            elif  request.user.code[:2] in ('m1',):
                del actions['ok2']
                del actions['ok']
                del actions['refused']
                return actions
            elif request.user.code[:2] in ('m2',):          
                del actions['ok1']
                return actions
                
    resource_class = PermResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code!='mosaad':           
            user_code = request.user.code[:3]
            employee = Employee.objects.get(code=request.user.code)

            code_filters = {
                'hrb': dict(school='بنين'),
                'hrg': dict(school__in=('بنات', 'Ig')),
                'm1b': dict(school='بنين', ok1=False, ok2=False, job_code=employee.job_code),
                'm2b': dict(school='بنين', ok2=False, job_code__startswith=employee.job_code),
                'm1g': dict(school__in=('بنات', 'Ig'), ok1=False, ok2=False, job_code=employee.job_code),
                'm2g': dict(school__in=('بنات', 'Ig'), ok2=False, job_code__startswith=employee.job_code)
            }
            if user_code in code_filters:
                return qs.filter(**code_filters[user_code])
            else:
                # Handle default case when user code doesn't match any condition
                return qs.none()
        else:
            return qs

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls') or request.user.code[:2] in ('hr','m1','m2'):
                return True
            return False

    def get_list_display_links(self, request, obj=None):
        if request.user.code in ('mosaad','hrboys','hrgirls') or request.user.code[:2] in ('hr',):
            self.list_display_links = ('employee',)
            return self.list_display_links
        else:
            self.list_display_links = None
            return self.list_display_links

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls') or request.user.code[:2] in ('hr',):
                return True
            return False
    def delete_queryset(self, request, queryset):
        print('==========================delete_queryset==========================')
        print(queryset)

        """
        you can do anything here BEFORE deleting the object(s)
        """
        for obj in queryset:
            if obj.ok2 == True and obj.month == active_month:
                employee_month = Employee_month.objects.get(employee=obj.employee,month=active_month)
                employee_month.permissions=F('permissions') - 1
                employee_month.save(update_fields=['permissions'])

                obj.delete()
            else:
                obj.delete()
        # queryset.delete()

        """
        you can do anything here AFTER deleting the object(s)
        """

        print('==========================delete_queryset==========================')

    def delete_model(self, request, obj):
        print('============================delete_model============================')
        print(obj)

        """
        you can do anything here BEFORE deleting the object
        """
        if obj.ok2 == True and obj.month == active_month:
            employee_month = Employee_month.objects.get(employee=obj.employee,month=active_month)
            employee_month.permissions=F('permissions') - 1
            employee_month.save(update_fields=['permissions'])

            obj.delete()
        else:
            obj.delete()
        """
        you can do anything here AFTER deleting the object
        """

        print('============================delete_model============================')

class VacationAdmin(ImportExportModelAdmin):
    list_display = ('employee','date_from','date_to','reason', 'month','ok1','ok2')
    # list_display_links = None
    autocomplete_fields = ['employee'] 
    readonly_fields = ('created','reason','ok1','ok2')
    filter_horizontal = ()
    search_fields = ('employee__code','employee__name')
    list_filter = ('school','month','type')
    fieldsets =(
        ('-----------', { 'fields': (('employee','month'),'type',('date_from','date_to'),'reason',('ok1','ok2'),'created','school')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.ok2==True:
                return ('employee','date_from','date_to','type','month') + self.readonly_fields
            return self.readonly_fields
        return self.readonly_fields


    def ok1(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.ok1 == False:
                obj.ok1 = True
                obj.save()
                self.log_change(request, obj, 'تم موافقة الرئيس المباشر')
                updated += 1
            else:
                notupdated +=1
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

    def ok2(self, request, queryset):
            updated = 0
            notupdated = 0
            for obj in queryset:
                if obj.ok1 == True:
                    obj.ok2 = True
                    obj.save()
                    self.log_change(request, obj, 'تم موافقة الرئيس الأعلى')
                    updated += 1
                else:
                    notupdated +=1
            if updated != 0:
                self.message_user(request, ngettext(
                    '%d تم الموافقة على',
                    '%d تم الموافقة على',
                    updated,
                ) % updated, messages.SUCCESS)
            if notupdated != 0:
                self.message_user(request, ngettext(
                    '%d لم يتم موافقة الرئيس المباشر',
                    '%d لم يتم موافقة الرئيس المباشر',
                    notupdated,
                ) % notupdated, messages.ERROR)

    def ok(self, request, queryset):
            updated = 0
            notupdated = 0
            for obj in queryset:
                if obj.ok2 == False:
                    obj.ok2 = True
                    obj.save()
                    self.log_change(request, obj, ' موافقة مباشرة')
                    updated += 1
                else:
                    notupdated +=1
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

    ok1.short_description = "موافقة الرئيس المباشر"
    ok2.short_description = "موافقة الرئيس الأعلى"
    ok.short_description = "موافقة مباشرة"
    
    actions = ['ok1','ok2','ok']
    def get_actions(self, request):
        actions= super().get_actions(request)
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return actions
            elif request.user.id in Manager.objects.filter(level=2).values_list('user',flat=True):
                del actions['ok']
                return actions
            else:          
                del actions['ok']
                del actions['ok2']
                return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code !="mosaad":
            qs.filter(school=request.user.school)
            if request.user.id in Manager.objects.filter(level=1).values_list('user',flat=True):
                employee = Employee.objects.get(code=request.user.code)
                return qs.filter(employee__job_code=employee.job_code,ok1=False,ok2=False)
            elif request.user.id in Manager.objects.filter(level=2).values_list('user',flat=True):
                employee = Employee.objects.get(code=request.user.code)
                return qs.filter(employee__job_code__startswith=employee.job_code[:2],ok2=False)
        return qs

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            elif request.user.id in Manager.objects.filter(level__in=(1,2)).values_list('user',flat=True):
                return True
            return False

    def get_list_display_links(self, request, obj=None):
        if request.user.code in ('mosaad','hrboys','hrgirls'):
            self.list_display_links = ('employee',)
            return self.list_display_links
        else:
            self.list_display_links = None
            return self.list_display_links

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

class SalaryItemInline(admin.TabularInline):
    model = SalaryItem
    # can_delete = False
    exclude = ('month',)
    # readonly_fields = [
    #     'month'
    # ]
    extra = 0
    # ordering = ('-month',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            return qs.filter(month=active_month)
        except Month.DoesNotExist:
            return qs

class PermissionInline(admin.TabularInline):
    model = Permission
    can_delete = False
    # exclude = ('month',)
    readonly_fields = ['ok1','ok2']
    extra = 0
    ordering = ('-date',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            return qs.filter(month=active_month)
        except Month.DoesNotExist:
            return qs


    def has_change_permission(self, request, obj=None):
        return False

class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('name','job','perms','vecation_role','times','code','job_code','time_code','is_active')
    # autocomplete_fields = ['perms','vecation_role']
    raw_id_fields = ('job',)
    readonly_fields = ('birth_date','job_code','vacations','vacations_s')
    search_fields = ('code','name','na_id','insurance_no')
    filter_horizontal = ()
    list_filter = ('school','job__type','job__grade','is_educational','job__title','job__department')
    fieldsets = (
    ('بيانات الموظف', { 'fields': (('name','code'),('job_code','job'),('na_id','birth_date','school'),('mobile_number','phone_number'),('emergency_phone','email'),'address',('basic_certificate','is_educational'),('notes','is_active'))}),
    ('بيانات التعاقد', {'fields': (('attendance_date','insurance_date'),('participation_date','contract_date'),'insurance_no',('salary_parameter','salary'),'message','time_code','perms','vecation_role','times',('vacations','vacations_s'))}),
                )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code =="hrboys":
            return qs.filter(school__in = ('بنين',))
        elif request.user.code == "hrgirls":
            # return qs.filter(Q(school='.بنات.')| Q(school='بنات'))
            return qs.filter(school__in = ('بنات','Ig'))
        return qs
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code','na_id','school') + self.readonly_fields
        return self.readonly_fields

    inlines = [PermissionInline,SalaryItemInline]
    resource_class = EmployeeResource

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
                self.log_change(request, obj, 'إعطاء صلاحية الرئيس المباشر')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم إعطاء صلاحية الرئيس المباشر الى',
                '%d تم إعطاء صلاحية الرئيس المباشر الى',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d بالفعل يمتلك صلاحية الرئيس المباشر ',
                '%d بالفعل يمتلك صلاحية الرئيس المباشر ',
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
                self.log_change(request, obj, 'إعطاء صلاحية الرئيس الأعلى')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم إعطاء صلاحية الرئيس الأعلى الى',
                '%d تم إعطاء صلاحية الرئيس الأعلى الى',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d بالفعل يمتلك صلاحية الرئيس الأعلى ',
                '%d بالفعل يمتلك صلاحية الرئيس الأعلى ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def manager_out(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.code[:2] == "m1" or obj.code[:2] == "m2":
                new_code = obj.na_id[1:3] + obj.code[2:]
                employee_acc = Student.objects.get(code=obj.code)
                employee_acc.code = new_code
                employee_acc.password=make_password(new_code)
                employee_acc.is_admin = False
                employee_acc.is_staff = False
                obj.code = new_code
                obj.save(update_fields=["code",])
                employee_acc.save(update_fields=["code", "password", "is_staff", "is_admin"])
                self.log_change(request, obj, 'سحب صلاحية الرئيس ')
                updated += 1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم سحب صلاحية الرئيس من',
                '%d تم سحب صلاحية الرئيس من',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d لا يمتلك صلاحية الرئيس من الاساس ',
                '%d لا يمتلك صلاحية الرئيس من الاساس ',
                notupdated,
            ) % notupdated, messages.ERROR)

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad',):
                return True
            return False
        
    def Fix_job_code(self, request, queryset):
        # updated = queryset.update(verified=True)
        updated = 0
        notupdated = 0

        for obj in queryset:
            if obj.job is not None:
                school=obj.school
                if school=="بنين":
                    school="b"
                elif school=="بنات":
                    school="g"         
                job_dep = str(obj.job.department.id)
                job_grade = obj.job.grade
                if obj.job.department.name == "المرحلة":
                    code = school+job_grade
                elif obj.job.department.name == "المدرسة":
                    code = school
                else:
                    if job_grade !=None:
                        code = school+job_grade + job_dep
                    else:
                        code = school+job_dep
                obj.job_code=code
                obj.save(update_fields=["job_code",])

                # Update related permissions
                related_permissions = Permission.objects.filter(employee=obj,month=active_month)
                related_permissions.update(job_code=code)

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
    manager_1.short_description = 'إعطاء صلاحية الرئيس المباشر'
    manager_2.short_description = 'إعطاء صلاحية الرئيس الأعلى'
    manager_out.short_description = 'سحب صلاحية الرئيس'

    actions = ['manager_1','manager_2','manager_out','Fix_job_code','Fix_birth_date']

    def delete_queryset(self, request, queryset):
            print('==========================delete_queryset==========================')
            print(queryset)

            """
            you can do anything here BEFORE deleting the object(s)
            """
            for obj in queryset:
                try:
                    employee = Student.objects.get(code=obj.code)
                    employee.delete()
                except Student.DoesNotExist:
                    pass
                obj.delete()
            # queryset.delete()

            """
            you can do anything here AFTER deleting the object(s)
            """

            print('==========================delete_queryset==========================')

class MonthAdmin(ImportExportModelAdmin):
    list_display = ('code','perms','active','published','status')
    filter_horizontal = ()
    readonly_fields = ('active','published',)
    fieldsets =(
        ('None', { 'fields': ('code','active','published','perms','dayoff')}),
        )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by('id')
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code',) + self.readonly_fields
        return self.readonly_fields

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
            count +=1
        if count > 1 :
            self.message_user(request,'لا يمكن فتح اكثر من شهر في نفس الفترة', messages.ERROR)
        else:
            if obj.active == False:
                self.message_user(request,'تم فتح الشهر من قبل', messages.ERROR)
            else:
                if obj.status == '3':
                    self.message_user(request,'تم إغلاق الشهر سابقاً ولا يمكن إعادة تفعيلة مرة اخرى', messages.ERROR)
                else:
                    before_count = Employee_month.objects.count()
                    # Retrieve the active employees queryset
                    employees = Employee.objects.all()
                    # Prepare a list of Employee_month objects
                    employee_months = [
                        Employee_month(
                            employee=employee,
                            school=employee.school,
                            month=active_month,
                            is_active=employee.is_active,
                            permissions=0,
                            vacations=0,
                            salary_value=0
                        )
                        for employee in employees
                    ]
                    # Bulk create the Employee_month objects
                    Employee_month.objects.bulk_create(employee_months)

                    after_count = Employee_month.objects.count()
                    created = after_count - before_count
                    self.message_user(request, ngettext(
                        '%d Monthly Record was Created',
                        '%d Monthly Records ware Created',
                        created,
                    ) % created, messages.SUCCESS)
           
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
    MonthlyRecords.short_description = 'إنشاء السجلات الشهرية'
    actions = ['activate','publish','MonthlyRecords']
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad',):
                return True
            return False

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
admin.site.register(Time_template,Time_templateAdmin)