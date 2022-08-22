from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import Student, School,Governorate, Nationality, Class, Class_group
from import_export.admin import ImportExportModelAdmin
from student.resources import StudentAffResource
from django.utils.translation import ngettext
from student.models import Student as StudentAcc
from fees.models import Fee

current_year = '23-22'

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
    list_display = ('code', 'name','grade','Class','status','age1oct','father_mobile','mother_mobile','payment_status')
    ordering = ('name',)
    autocomplete_fields = ['birth_gov','nationality']
    search_fields = ('code','name','student_id','father_id','notes')
    readonly_fields = ('payment_status',)

    filter_horizontal = ()
    list_filter = ('study_year','school','grade','Class','status','is_over','payment_status')

    fieldsets = (
        ('بيانات الطالب', { 'fields': ('name','en_name',('student_id','kind'),('birth_date', 'age1oct'),'birth_gov',('nationality','religion'))}),
        ('بيانات الالتحاق', { 'fields': (('study_year','payment_status'),('start_year','start_grade'),('school','code'), 'grade', ('status','from_to'),'status_no',('Class','group','is_over'),('global_code','document_status'))}),
        ('بيانات ولي الامر', { 'fields': ('responsibility',('father_name','father_job'),('father_id','father_mobile'),('mother_name','mother_job'),'mother_mobile',('phone_number','phone_number2'),('address_1' ,'email'),'notes')}),

                 )
    resource_class = StudentAffResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code == "affg":
            return qs.filter(school__in = ('.بنات.', 'بنات','Out-g'))
        elif request.user.code =="affb":
            return qs.filter(school__in = ('بنين','Out-b'))
        return qs
        
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.code != "":
                # return self.readonly_fields + ('code','study_year','school')
                return self.readonly_fields + ('code','study_year','school')
            return self.readonly_fields
        return self.readonly_fields

    def Transfer(self, request, queryset):
        # updated = queryset.update(verified=True)
        transferdgb = 0
        transferdbg = 0
        Passed = 0

        for obj in queryset:

            if obj.study_year != current_year :
                Passed =+1
            else:
                StudentCode = None
                NewSchool = None
                StudentFees = None
                if obj.code[0] == str(3):
                    StudentCode = obj.code
                    NewCode = 'C'+obj.code[1:7]
                    if obj.school == 'بنات':
                        NewSchool = '.بنات.'
                        obj.school = NewSchool
                        obj.status = "محول"
                        obj.from_to = "من المنارة بنات"
                        # self.log_change(request, obj, 'Transferd from Girls To Boys')
                        self.log_change(request, obj, 'تم التحويل من البنات الى البنين')
                        obj.save()

                        try:
                            CopyRecord = Student.objects.get(code=NewCode)
                            CopyRecord.delete()
                        except Student.DoesNotExist:
                            NewRecord = obj
                            NewRecord.code = NewCode
                            NewRecord.school = "بنات"
                            NewRecord.status = "محول من"
                            NewRecord.from_to = "الى المنارة بنين"
                            NewRecord.pk = None
                            NewRecord.save()      
                        transferdgb +=1
                    elif obj.school == ".بنات.":
                        NewSchool = 'بنات'
                        obj.school = NewSchool
                        obj.status = "محول"
                        obj.from_to = "من المنارة بنين"
                        self.log_change(request, obj, 'تم التحويل من البنين الى البنات')
                        obj.save() 

                        try:
                            CopyRecord = Student.objects.get(code=NewCode)
                            CopyRecord.delete()
                            obj.status = "مستجد"
                            obj.from_to = ""
                            obj.save() 
                        except Student.DoesNotExist:
                            NewRecord = obj
                            NewRecord.code = NewCode
                            NewRecord.school = ".بنات."
                            NewRecord.status = "محول من"
                            NewRecord.from_to = "الى المنارة بنات"
                            NewRecord.pk = None
                            NewRecord.save()
                        transferdbg +=1         

                    # StudentAcc.objects.filter(code=StudentCode).update(
                    # school=NewSchool)      

                    try:
                        StudentFees = Fee.objects.filter(student__code=StudentCode)
                        StudentFees.update(school = NewSchool)
                    except Student.DoesNotExist:
                        pass

                else:
                    Passed +=1
            if transferdgb != 0:
                self.message_user(request, ngettext(
                'تم تحويل عدد %d طالب من البنات الى البنين',
                'تم تحويل عدد %d طالب من البنات الى البنين',
                transferdgb,
                ) % transferdgb, messages.SUCCESS)
            if transferdbg != 0:
                self.message_user(request, ngettext(
                'تم تحويل عدد %d طالب من البنين الى البنات',
                'تم تحويل عدد %d طالب من البنين الى البنات',
                transferdbg,
                ) % transferdbg, messages.SUCCESS)
            if Passed != 0:
                self.message_user(request, ngettext(
                'لا يمكن تحويل عدد %d طالب',
                'لا يمكن تحويل عدد %d طالب',
                Passed,
                ) % Passed, messages.ERROR)
        
    Transfer.short_description = "تحويل منارة داخلي"

    def TransferOut(self, request, queryset):
        transferd = 0
        passed = 0

        for obj in queryset:
            if obj.code[0] == 'C':
                passed +=1
            else:
                if obj.study_year != current_year :
                    passed =+1
                else:
                    if obj.school[0]=='O':
                        passed +=1
                    else:
                        if obj.status == "محول من":
                            passed +=1
                        else:
                            StudentPayments = StudentAcc.objects.get(code=obj.code)
                            if StudentPayments.total_paid > 0:
                                passed +=1
                            else:    
                                StudentCode = obj.code
                                NewSchool = None
                                obj.status = "محول من"
                                if obj.code[0] == str(3):
                                    NewSchool = 'Out-g'
                                    obj.school = NewSchool
                                    # StudentAcc.objects.filter(code=obj.code).update(
                                    # school='Out-g',)
                                else:
                                    NewSchool = 'Out-b'
                                    obj.school = NewSchool
                                    # StudentAcc.objects.filter(code=obj.code).update(
                                    # school='Out-b',)
                                self.log_change(request, obj, 'تم التحويل من المدرسة')
                                transferd +=1
                                obj.save()
                                try:
                                    StudentFees = Fee.objects.filter(student__code=StudentCode)
                                    StudentFees.update(school = NewSchool)
                                except Student.DoesNotExist:
                                    pass

        if transferd != 0:
            self.message_user(request, ngettext(
            'تم تحويل عدد %d طالب من المدرسة',
            'تم تحويل عدد %d طالب من المدرسة',
            transferd,
            ) % transferd, messages.SUCCESS)

        if passed != 0:
            self.message_user(request, ngettext(
            'لا يمكن تحويل عدد %d طالب',
            'لا يمكن تحويل عدد %d طالب',
            passed,
            ) % passed, messages.ERROR)

    TransferOut.short_description = "تحويل من المدرسة"  

    actions = ['TransferOut','Transfer']
    def get_actions(self, request):
        actions= super().get_actions(request)
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','affg'):
                return actions
            else:
                del actions['Transfer']
                return actions

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
