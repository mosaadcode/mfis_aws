from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import Student,Bus,BusStudent,Teacher,SchoolFee,Manager,Program, Archive
from fees.admin import FeesInline
from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from .resources import StudentResource,BusStudentResource
from django.contrib.auth.models import Group
from django.utils.translation import ngettext
from django.contrib.auth.hashers import make_password
from human_resources.models import Employee

admin.site.unregister(Group)

current_year = '23-22'

class AccAdmin:
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

class ArchivesInline(admin.TabularInline):
    model = Archive
    can_delete = False
    exclude = ('code','school')
    readonly_fields = [
        'study_year','grade','study','bus','discount','total','old_fee','old_paid','year_status'
    ]
    extra = 0
    ordering = ('-study_year',)
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    
class StudentAdmin(ImportExportMixin, UserAdmin):
    list_display = ('code', 'username', 'total_paid', 'payment_status','total_books')
    search_fields = ('code', 'username')
    readonly_fields = ('code','username','year','school','grade','living_area', 'address','bus_number','old_bus','total_paid', 'old_fee', 'old_paid','study_payment1', 'study_payment2', 'study_payment3','study_payment3', 'payment_status','last_login','bus_order','books','total_books','father_mobile','mother_mobile','phone_number', 'email','lms_code')

    # filter_horizontal = ()
    list_filter = ('school','year','grade','bus_active','books','is_active','can_pay')
    fieldsets = (
        (None, { 'fields': (('code', 'year'), 'username', ('school', 'grade'),'password', ('is_active', 'can_pay', 'bus_active'))}),
        # (None, { 'fields': (('is_staff','is_admin'),)}),
        ('الأقساط والسداد', {'fields': (('study_payment1', 'study_payment2', 'study_payment3'),('bus_payment1', 'bus_payment2'), ('old_fee','old_paid'),'discount', ('total_paid','payment_status'))}),
        ('الكتب الدراسية', {'fields': (('books','total_books'),)}),
        ('التواصل', {'fields': ('message', ('father_mobile','mother_mobile'),('phone_number', 'email'),'lms_code','last_login')}),
        ('السيارة', {'fields': ('bus_notes','living_area', 'address','bus_number','old_bus','bus_order')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
                 )
    resource_class = StudentResource

    # def payment_status(self,obj):
    #     return obj.payment_status()
    # payment_status.short_description = "مستحق سداد "
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "mfisb" or request.user.code[:3]=="acb":
            return qs.filter(school__in = ('بنين',),is_employ=False)
        elif request.user.code == "mfisg" or request.user.code[:3]=="acg":
            # return qs.filter(Q(school='.بنات.')| Q(school='بنات'))
            return qs.filter(school__in = ('.بنات.', 'بنات',),is_employ=False)
        return qs

    inlines = [ArchivesInline,FeesInline]

    def deactivate(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if  obj.is_active :
                obj.is_active = False
                obj.can_pay = False
                obj.study_payment1 = 0
                obj.study_payment2 = 0
                obj.study_payment3 = 0
                obj.bus_active = False
                obj.bus_payment1 = 0
                obj.bus_payment2 = 0
                obj.old_fee = 0
                self.log_change(request, obj, 'طالب منقطع - تم إلغاء المصروفات المستحقة')
                obj.save()
                updated +=1
            else:
                notupdated +=1

        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم تحويل الطالب الى طالب منقطع لعدد',
                '%d تم تحويل الطالب الى طالب منقطع لعدد',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d طالب منقطع بالفعل',
                '%d طالب منقطع بالفعل',
                notupdated,
            ) % notupdated, messages.ERROR)
            
    deactivate.short_description = "طالب منقطع"

    actions = ['deactivate',]

    # Adjust User Access ''''''''''''''''''''''''''''''''''''''''''
    def has_module_permission(self, request):
        return self.has_permission(request)

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_add_permission(self, request, obj=None):
        return request.user.code == "mosaad"

    def has_permission(self, request, obj=None):
        if request.user.is_authenticated:
            user_code = request.user.code
            return user_code in ('mosaad', 'mfisb', 'mfisg') or user_code[0] == 'a' and user_code[1] == 'c'
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.code == "mosaad"
        
class BusAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('number','supervisor_name','supervisor_mobile','driver_name','driver_mobile')
    search_fields = ('number','area')
    readonly_fields = ('school','bus_count')
    filter_horizontal = ()
    list_filter = ('school','area')
    fieldsets = (
        (None, {'fields': ('bus_count','number','area','sub_area','supervisor_name','supervisor_mobile','supervisor_address','supervisor_time' ,'driver_name' ,'driver_mobile','school')}),
                 )
    def bus_count(self, obj):
        return obj.bus_count()
    bus_count.short_description = 'مشتركين '
    def save_model(self, request, obj, form, change):
        if obj.school =="":
            if request.user.code == "busb":
                obj.school = "بنين"
            elif request.user.code == "busg":
                obj.school = "بنات"
            else:
                obj.school = ""
        super().save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.code == "busg":
    #         return qs.filter(school='بنات')
    #     elif request.user.code =="busb":
    #         return qs.filter(school="بنين")
    #     return qs
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','busb','busg'):
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False

class BusStudentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('username','father_mobile' ,'mother_mobile','bus_number','bus_order','bus_notes')
    ordering = ('bus_number','bus_order')
    autocomplete_fields = ['bus_number']
    search_fields = ('username','bus_number__number','bus_number__area')
    readonly_fields = ('code', 'school','username','grade','father_mobile' ,'mother_mobile','phone_number', 'email', 'old_bus')

    filter_horizontal = ()
    list_filter = ('school','grade', 'living_area')
    fieldsets = (
        ('بيانات الطالب', {'fields': (('father_mobile','mother_mobile'),('phone_number','code'),'username','grade','old_bus')}),
        ('إشتراك السيارة ', {'fields': ('bus_number','bus_order','living_area', 'address','bus_notes' )}),
                 )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code in ('busg','busb'):
        #     return qs.filter(bus_active=True,school__in = ('.بنات.', 'بنات','Ig'))
            return qs.filter(bus_active=True)
        # elif request.user.code =="busb":
        #     return qs.filter(bus_active=True,school="بنين")
        return qs
        
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','busb','busg'):
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False
    def has_add_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False

    resource_class = BusStudentResource

class TeacherAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'job','phone_number','bus_number','bus_order','bus_notes')
    ordering = ('bus_number','bus_order')
    autocomplete_fields = ['bus_number']
    search_fields = ('name','bus_number__number','bus_number__area')
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ('school','living_area')
    fieldsets = (
        (None, {'fields': ('name', 'school','job','phone_number','living_area', 'address','bus_number','bus_order','bus_notes')}),
                 )
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','busb','busg'):
                return True
            return False

class SchoolFeeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('grade' , 'study_fee', 'activity_fee', 'computer_fee','study_payment1','study_payment2','study_payment3','bus_payment1','bus_payment2')
    ordering = ('id',)
    readonly_fields = ('school', 'grade','year')

    filter_horizontal = ()
    list_filter = ('school','year')
    fieldsets = (
        # ('None', {'fields': ('grade',)}),
        ('المصروفات الرسمية ', {'fields': (('grade','year'),'study_fee', 'activity_fee', 'computer_fee','bus_fee','books_fee' )}),
        ('المصروفات', {'fields': (('study_payment1','study_payment2','study_payment3'),('bus_payment1','bus_payment2'),('books_all','books_books','books_booklet','books_a_level'))}),
                 )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "mfisg" or request.user.code[:3]=="acg":
            return qs.filter(school__in = ('.بنات.', 'بنات'))
        elif request.user.code =="mfisb" or request.user.code[:3]=="acb":
            return qs.filter(school="بنين")
        return qs
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','mfisb','mfisg') or request.user.code[:2]=="ac":
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False
    def has_add_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False

    def update(self, request, queryset):
        count = 0
        for obj in queryset:
            count +=1
        if count > 1 :
            self.message_user(request,'لا يمكن تحديث اكثر من مرحلة في نفس الوقت', messages.ERROR)
        else:
            school = obj.school
            grade = obj.grade
            study1 = obj.study_payment1
            study2 = obj.study_payment2
            study3 = obj.study_payment3
            bus1 = obj.bus_payment1
            bus2 = obj.bus_payment2
            if school == 'بنين':
                students = Student.objects.filter(year=obj.year,school=school,grade=grade)
            else:
                students = Student.objects.filter(year=obj.year,school__in = ('.بنات.', 'بنات'),grade=grade)
            students.update(
                study_payment1 = study1,
                study_payment2 = study2,
                study_payment3 = study3,
                bus_payment1 = bus1,
                bus_payment2 = bus2,
            )
            self.log_change(request, obj, 'تم تحديث مصروفات جميع الطلاب')
            count = students.count()
            if count != 0:
                self.message_user(request, ngettext(
                'تم تحديث مصروفات %d طالب ',
                'تم تحديث مصروفات %d طالب ',
                count,
                ) % count, messages.SUCCESS)
    update.short_description='تحديث مصروفات المرحلة'
    actions = ['update']

class ProgramAdmin(AccAdmin,ImportExportModelAdmin):
    # list_display = ('app', 'model')
    filter_horizontal = ()
    list_filter = ('name',)
    fieldsets = ((None, {'fields':('name','code','count'),}),)

class ManagerAdmin(AccAdmin,ImportExportModelAdmin):
    list_display = ('user', 'program','level')
    autocomplete_fields = ['user']
    # raw_id_fields = ('program',)
    search_fields = ('user__username','user__code')
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ('program__name',)
    fieldsets = ((None, {'fields': ('user', ('program','level'))}),)

    def manager(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            code = obj.user.code
            if  code[:2] == "ac" or code[:2] == "hr" or code[:2] == "af" or code[:2] == "bu":
                notupdated +=1
            else:
                user = Student.objects.get(id=obj.user.pk)
                employee = Employee.objects.get(code=code)
                program = Program.objects.get(id=obj.program.pk)
                new_code = program.code + code[2:3] + format(program.count+1,'04')
                program.count+=1
                program.save()
                user.code = new_code
                user.password = make_password(new_code)
                user.is_admin = True
                user.is_staff = True
                user.save(update_fields=["code", "password", "is_staff", "is_admin"])
                employee.code=new_code
                employee.save(update_fields=["code"])
                self.log_change(request, obj, 'إعطاء صلاحيات الموظف')
                obj.save()
                updated += 1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d تم إعطاء صلاحيات الموظف الى',
                '%d تم إعطاء صلاحيات الموظف الى',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d بالفعل يمتلك صلاحيات الموظف ',
                '%d بالفعل يمتلك صلاحيات الموظف ',
                notupdated,
            ) % notupdated, messages.ERROR)

    manager.short_description = 'إعطاء صلاحيات الموظف'

    actions = ['manager',]

    def delete_queryset(self, request, queryset):

            for obj in queryset:
                employee = Student.objects.get(id=obj.user.id)
                employee.is_admin = False
                employee.is_staff = False
                employee.save(update_fields=["is_admin", "is_staff"])
                obj.delete()

class ArchiveAdmin(ImportExportModelAdmin):
    list_display = ('student','grade','study','bus','discount','total','old_fee','old_paid','year_status')
    autocomplete_fields = ['student']
    search_fields = ('code','student__username')
    readonly_fields = ('student','code','school','study_year','grade','study','bus','discount','total','old_fee','old_paid','year_status')
    filter_horizontal = ()
    list_filter = ('school','study_year', 'grade' )
    fieldsets = ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "mfisg" or request.user.code[:3]=="acg":
            return qs.filter(school__in = ('.بنات.', 'بنات'))
        elif request.user.code =="mfisb" or request.user.code[:3]=="acb":
            return qs.filter(school__in = ('بنين',))
        return qs

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','mfisb','mfisg') or request.user.code[:2]=="ac":
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False
    def has_add_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False
    def has_change_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False

admin.site.register(Student, StudentAdmin)
admin.site.register(Bus,BusAdmin)
admin.site.register(BusStudent,BusStudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(SchoolFee,SchoolFeeAdmin)
admin.site.register(Manager,ManagerAdmin)
admin.site.register(Program,ProgramAdmin)
admin.site.register(Archive,ArchiveAdmin)
