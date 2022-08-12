from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student,Bus,BusStudent,Teacher,SchoolFee
from fees.admin import FeesInline
# from django.http import HttpResponse
# import csv
from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from .resources import StudentResource,BusStudentResource
from django.contrib.auth.models import Group
# from django.db.models import Q

admin.site.unregister(Group)

class StudentAdmin(ImportExportMixin, UserAdmin):
    list_display = ('code', 'username', 'total_paid', 'payment_status','total_books')
    search_fields = ('code', 'username')
    readonly_fields = ('code','username','year','school','grade','living_area', 'address','bus_number','old_bus','total_paid', 'old_fee', 'old_paid','study_payment3', 'bus_payment2', 'payment_status','last_login','bus_order','books','total_books')

    # filter_horizontal = ()
    list_filter = ('school','year','grade','bus_active','books','is_active','can_pay')
    fieldsets = (
        (None, { 'fields': (('code', 'year'), 'username', ('school', 'grade'),'password', ('is_active', 'can_pay', 'bus_active'))}),
        # (None, { 'fields': (('is_staff','is_admin'),)}),
        ('الأقساط والسداد', {'fields': (('study_payment1', 'study_payment2', 'study_payment3'),('bus_payment1', 'bus_payment2'), ('old_fee','old_paid'),'discount', ('total_paid','payment_status'))}),
        ('الكتب الدراسية', {'fields': (('books','total_books'),)}),
        ('التواصل', {'fields': ('message', ('father_mobile','mother_mobile'),('phone_number', 'email'),'last_login')}),
        ('السيارة', {'fields': ('bus_notes','living_area', 'address','bus_number','old_bus','bus_order')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
                 )
    resource_class = StudentResource

    # def payment_status(self,obj):
    #     return obj.payment_status()
    # payment_status.short_description = "مستحق سداد "
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "mfisb":
            return qs.filter(school="بنين")
        elif request.user.code == "mfisg":
            # return qs.filter(Q(school='.بنات.')| Q(school='بنات'))
            return qs.filter(school__in = ('.بنات.', 'بنات'))
        return qs

    # def export_bus(self, request, queryset):

    #     meta = self.model._meta
    #     # field_names = [field.name for field in meta.fields]
    #     field_names = ['code', 'username', 'school', 'grade', 'old_bus', 'living_area', 'address']
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename=bus.csv'.format(meta)
    #     writer = csv.writer(response)

    #     writer.writerow(field_names)
    #     for obj in queryset:
    #         row = writer.writerow([getattr(obj, field) for field in field_names])

    #     return response

    # export_bus.short_description = "Bus Data"



    # def export_student(self, request, queryset):

    #     meta = self.model._meta
    #     # field_names = [field.name for field in meta.fields]
    #     field_names = ['code', 'username', 'school', 'grade']
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename=Students.csv'.format(meta)
    #     writer = csv.writer(response)

    #     writer.writerow(field_names)
    #     for obj in queryset:
    #         row = writer.writerow([getattr(obj, field) for field in field_names])

    #     return response

    # export_student.short_description = "تصدير بيانات الطلبة"



    # actions = ["export_bus", "export_student"]

    inlines = [FeesInline]

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','mfisb','mfisg'):
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False
        
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
    list_display = ('grade' , 'study_fee', 'activity_fee', 'computer_fee','study_payment1','study_payment2','study_payment3','bus_payment1','bus_payment1')
    ordering = ('id',)
    readonly_fields = ('school', 'grade',)

    filter_horizontal = ()
    list_filter = ('school',)
    fieldsets = (
        # ('None', {'fields': ('grade',)}),
        ('المصروفات الرسمية ', {'fields': ('grade','study_fee', 'activity_fee', 'computer_fee','bus_fee','books_fee' )}),
        ('المصروفات', {'fields': (('study_payment1','study_payment2','study_payment3'),('bus_payment1','bus_payment2'),('books_all','books_books','books_booklet','books_a_level'))}),
                 )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "mfisg":
            return qs.filter(school__in = ('.بنات.', 'بنات'))
        elif request.user.code =="mfisb":
            return qs.filter(school="بنين")
        return qs
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','mfisb','mfisg'):
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

admin.site.register(Student, StudentAdmin)
admin.site.register(Bus,BusAdmin)
admin.site.register(BusStudent,BusStudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(SchoolFee,SchoolFeeAdmin)
