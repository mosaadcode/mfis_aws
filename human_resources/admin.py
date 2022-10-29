from django.contrib import admin
from .models import School,Department,Job, Employee, Month,SalaryItem,Permission,Vacation
from import_export.admin import ImportExportModelAdmin
from .resources import SalaryItemResource,PermResource,EmployeeResource
from django.utils.translation import ngettext
from django.contrib import admin, messages
from student.models import Student,Manager

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


class PermissionAdmin(ImportExportModelAdmin):
    list_display = ('employee','type', 'date','reason', 'month','ok1','ok2')
    # list_display_links = ('employee',)
    autocomplete_fields = ['employee']
    readonly_fields = ('school','created','reason','ok1','ok2')
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
    resource_class = PermResource

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
                return True
            return False

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
    def has_module_permission(self, request):
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
    list_display = ('name','mobile_number' ,'participation_date','is_educational','is_active'   )
    # autocomplete_fields = ['job']
    raw_id_fields = ('job',)
    readonly_fields = ('birth_date',)
    search_fields = ('code','name','na_id')
    filter_horizontal = ()
    list_filter = ('school','is_educational')
    fieldsets = (
    ('بيانات الموظف', { 'fields': ('name',('code','birth_date'),('na_id','school'),('mobile_number','phone_number'),('emergency_phone','email'),'address',('basic_certificate','is_educational'),('notes','is_active'))}),
    ('بيانات التعاقد', {'fields': (('attendance_date','insurance_date'),('participation_date','contract_date'),'insurance_no',('job', 'salary'),('salary_parameter'),'message')}),
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
    actions = ['activate','publish']
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','hrboys','hrgirls'):
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