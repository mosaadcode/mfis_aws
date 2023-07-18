from django.contrib import admin
from .models import School,Department,Job, Employee, Month,SalaryItem,Permission,Vacation,Permission_setting,Employee_month,Time_setting
from import_export.admin import ImportExportModelAdmin
from .resources import SalaryItemResource,PermResource,EmployeeResource,Employee_monthResource,Time_settingResource
from django.utils.translation import ngettext
from django.contrib import admin, messages
from student.models import Student,Manager
from django.db.models import F

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
    # list_display = ('title','department')
    filter_horizontal = ()
    search_fields = ('title',)
    list_filter = ('type','grade','department')
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
            return qs.filter(school__in = ('بنات',))
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
    list_filter = ('school',)
    fieldsets = (
    ('', { 'fields': ('name','is_perms','is_over',('is_evening','is_between','is_morning'),( 'perms'))}),
                )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "hrgirls":
            return qs.filter(school__in = ('بنات',))
        elif request.user.code =="hrboys":
            return qs.filter(school__in = ('بنين',))
        return qs

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            if request.user.code == "hrboys":
                obj.school = "بنين"
            elif request.user.code == "hrgirls":
                obj.school = "بنات"
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

class Time_settingAdmin(ImportExportModelAdmin):
    list_display = ('name','date','time_in','time_in_perm','time_out', 'time_out_perm','school')
    # list_display_links = ('employee',)
    # autocomplete_fields = ['employee']
    readonly_fields = ()
    filter_horizontal = ()
    search_fields = ('name',)
    list_filter = ('school','name','month')
    fieldsets = (
    ('', { 'fields': ('name','month','date','time_in','time_in_perm','time_out', 'time_out_perm')}),
                )
    resource_class=Time_settingResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('name', 'date')
        if request.user.code == "hrgirls":
            return qs.filter(school__in = ('بنات',))
        elif request.user.code =="hrboys":
            return qs.filter(school__in = ('بنين',))
        return qs

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            if request.user.code == "hrboys":
                obj.school = "بنين"
            elif request.user.code == "hrgirls":
                obj.school = "بنات"
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

class PermissionAdmin(ImportExportModelAdmin):
    list_display = ('employee','type', 'date','reason', 'month','ok1','ok2')
    # list_display_links = ('employee',)
    autocomplete_fields = ['employee']
    readonly_fields = ('school','created','reason','ok1','ok2','start_time','end_time')
    filter_horizontal = ()
    search_fields = ('employee__code','employee__name')
    list_filter = ('school','month','type')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.ok2==True:
                return ('employee','type', 'date','month') + self.readonly_fields
            return self.readonly_fields
        return self.readonly_fields
    
    # def get_list_display_links(self, request, obj=None):
        # users = Manager.objects.filter(level__gte=10).values_list('user',flat=True)
        # if request.user.id in Manager.objects.filter(level__gte=10).values_list('user',flat=True):
        #     return self.list_display_links
        # self.list_display_links = None
        # return self.list_display_links

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

    resource_class = PermResource

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
    list_display = ('name','code','mobile_number' ,'participation_date','job','is_active')
    autocomplete_fields = ['perms','times']
    raw_id_fields = ('job',)
    readonly_fields = ('birth_date','job_code','time_in','time_in_perm','time_out','time_out_perm')
    search_fields = ('code','name','na_id','insurance_no')
    filter_horizontal = ()
    list_filter = ('school','job__type','job__grade','is_educational','job__department')
    fieldsets = (
    ('بيانات الموظف', { 'fields': (('name','job'),('code','job_code','birth_date'),('na_id','school'),('mobile_number','phone_number'),('emergency_phone','email'),'address',('basic_certificate','is_educational'),('notes','is_active'))}),
    ('بيانات التعاقد', {'fields': (('attendance_date','insurance_date'),('participation_date','contract_date'),'insurance_no',('salary_parameter','salary'),'message','time_code','perms','times')}),
                )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code','na_id','school') + self.readonly_fields
        return self.readonly_fields

    inlines = [PermissionInline,SalaryItemInline]
    resource_class = EmployeeResource
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

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