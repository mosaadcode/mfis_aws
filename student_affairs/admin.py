from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, School,Governorate, Nationality, Class, Class_group
from import_export.admin import ImportExportModelAdmin
from student.resources import StudentAffResource

class GovernorateAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad'):
                return True
            return False
    # def has_delete_permission(self, request, obj=None):
    #     if request.user.code == "mosaad":
    #         return True
    #     return False

class NationalityAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad'):
                return True
            return False
    # def has_delete_permission(self, request, obj=None):
    #     if request.user.code == "mosaad":
    #         return True
    #     return False

class GroupAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','affb','affg'):
                return True
            return False

class ClassAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','affb','affg'):
                return True
            return False

class StudentAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name','grade','status','age1oct','father_mobile','mother_mobile','phone_number','payment_status')
    autocomplete_fields = ['birth_gov','nationality']
    search_fields = ('code','name','father_id','notes')
    readonly_fields = ('age1oct','payment_status')

    filter_horizontal = ()
    list_filter = ('study_year','school','grade','status','is_over','payment_status')

    fieldsets = (
        ('بيانات الطالب', { 'fields': ('name','en_name',('student_id','kind'),('birth_date', 'age1oct'),'birth_gov',('nationality','religion'))}),
        ('بيانات الالتحاق', { 'fields': (('study_year','payment_status'),('start_year','start_grade'),'code','school', 'grade', ('status','from_to'),'status_no',('Class','group','is_over'),'global_code')}),
        ('بيانات ولي الامر', { 'fields': ('responsibility','father_name','father_job','father_id','mother_name','mother_job','father_mobile','mother_mobile','phone_number','phone_number2','address_1' ,'email','notes')}),

                 )
    resource_class = StudentAffResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.code != "":
                # return self.readonly_fields + ('code','study_year','school')
                return self.readonly_fields + ('code','study_year','school')
            return self.readonly_fields
        return self.readonly_fields

    # def has_delete_permission(self, request, obj=None):
    #     if request.user.code in ('mosaad','mosaad2'):
    #         return True
    #     return False
    # def has_change_permission(self, request, obj=None):
    #     if request.user.code in ('mosaad','mosaad2'):
    #         return True
    #     return False

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','affb','affg'):
                return True
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.code == "mosaad":
            return True
        return False

class SchoolAdmin(ImportExportModelAdmin):
     
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad',):
                return True
            return False

admin.site.register(Student,StudentAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Class_group,GroupAdmin)
admin.site.register(Governorate,GovernorateAdmin)
admin.site.register(Nationality,NationalityAdmin)
