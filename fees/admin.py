from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.db.models import F
from import_export.admin import ImportExportModelAdmin
from .models import Fee
from student.models import Student,Archive
from student.resources import FeesResource
from student_affairs.models import Student as StudentAff

CURRENT_YEAR = '24-23'

def get_allowed_schools(user_code):
    if user_code == "mfisb" or user_code[:3] == "acb":
        return ('بنين',)
    elif user_code == "mfisg" or user_code[:3] == "acg":
        return ('.بنات.', 'بنات',)
    return ()

class FeesInline(admin.TabularInline):
    model = Fee
    can_delete = False
    # exclude = ('school',)
    readonly_fields = [
        'verified'
    ]
    extra = 0
    ordering = ('-year','-created')

    # Adjust School Access ''''''''''''''''''''''''''''
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code != 'mosaad':
            allowed_schools = get_allowed_schools(request.user.code)
            return qs.filter(school__in=allowed_schools)
        return qs
    
    def has_change_permission(self, request, obj=None):
        return False
    # def has_add_permission(self, request, obj=None):
    # return False


class FeeAdmin(ImportExportModelAdmin):
    list_display = ('student', 'value', 'school', 'kind', 'bank_account', 'payment_date' , 'created','year','verified')
    autocomplete_fields = ['student']
    search_fields = ('student__code','student__username')
    readonly_fields = ('created','verified')

    filter_horizontal = ()
    list_filter = ('school', 'year', 'verified', 'kind','bank_account', 'payment_date', 'created', )
    fieldsets = ()
    resource_class = FeesResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.verified == True:
                return ('year','student','school','kind', 'value','bank_account','payment_date',) + self.readonly_fields
            return self.readonly_fields
        return self.readonly_fields

    # Adjust School Access ''''''''''''''''''''''''''''
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code != 'mosaad':
            allowed_schools = get_allowed_schools(request.user.code)
            return qs.filter(school__in=allowed_schools)
        return qs

    
    def out(self, request, queryset):
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.verified == True or obj.school[0] =='O':
                notupdated +=1
            else:
                if request.user.code == 'mfisb':
                    school = 'Out-b'
                else:
                    school = 'Out-g'
                obj.school = school
                self.log_change(request, obj, 'delete to out')
                obj.save()
                updated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d fee was successfully deleted.',
                '%d fees were successfully deleted.',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d fee can not be deleted.',
                '%d fees can not be deleted.',
                notupdated,
            ) % notupdated, messages.ERROR)
            
    out.short_description = "Delete fee"
            
    def verified(self, request, queryset):
        # updated = queryset.update(verified=True)
        updated = 0
        notupdated = 0
        cannot = 0
        for obj in queryset:
            if obj.verified == False:
                mystudent = Student.objects.get(id=obj.student_id)
                SYear=mystudent.year
                if obj.year == SYear:

                    #for book and book
                    if obj.kind[:3] == 'Boo':
                        mystudent.total_books = F('total_books')+obj.value
                        if obj.value > 0 :
                            mystudent.books = True
                        else:
                            mystudent.books = False
                    elif obj.kind[:3] == 'Bok':
                        mystudent.total_books = F('total_books')+obj.value
                    elif obj.kind == 'دراسية':
                        mystudent.total_paid=F('total_paid') + obj.value
                    #update student Affiars
                        try:
                            mystudentAff = StudentAff.objects.get(code=mystudent.code)
                            mystudentAff.payment_status = True
                            mystudentAff.save()
                        except StudentAff.DoesNotExist:
                            pass
                    elif obj.kind == 'سيارة':
                        mystudent.total_paid=F('total_paid') + obj.value                                                                     
                        mystudent.bus_active = True

                    mystudent.save()
                    obj.verified = True
                    obj.save()
                    self.log_change(request, obj, 'verified')
                    updated += 1                    
                else:
                    try:
                        archive = Archive.objects.get(code=mystudent.code,study_year=obj.year)
                        archive.total = F('total')+obj.value
                        archive.save()
                        obj.verified = True
                        obj.save()
                        self.log_change(request, obj, 'verified')
                        updated += 1                        
                    except Archive.DoesNotExist:
                        cannot +=1
            else:
                notupdated +=1
        if updated != 0:
            self.message_user(request, ngettext(
                '%d fee was successfully verified.',
                '%d fees were successfully verified.',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d fee was already verified before.',
                '%d fees were already verified before.',
                notupdated,
            ) % notupdated, messages.ERROR)
        if cannot != 0:
            self.message_user(request, ngettext(
                '%d fee needs year check.',
                '%d fees need year check.',
                cannot,
            ) % cannot, messages.ERROR)
        
    verified.short_description = "Ok Verified"

    def unverified(self, request, queryset):
        # updated = queryset.update(verified=False)
        updated = 0
        notupdated = 0
        cannot = 0
        for obj in queryset:
            if obj.verified == True:
                # if obj.year == current_year:
                mystudent = Student.objects.get(id=obj.student_id)
                StudentYear = mystudent.year
                if obj.year == StudentYear:
                    #for book and book
                    if obj.kind[:3] == 'Boo':
                        mystudent.total_books = F('total_books')-obj.value
                        mystudent.books = False
                    elif obj.kind[:3] == 'Bok':
                        mystudent.total_books = F('total_books')-obj.value
                    elif obj.kind == 'دراسية':
                        mystudent.total_paid=F('total_paid') - obj.value
                        if Fee.objects.filter(student=obj.student_id,kind='دراسية',year=StudentYear,verified=True).count()==1:
                            try:
                                mystudentAff = StudentAff.objects.get(code=mystudent.code)
                                mystudentAff.payment_status = False
                                mystudentAff.save()
                            except StudentAff.DoesNotExist:
                                pass
                    elif obj.kind == 'سيارة':
                        mystudent.total_paid=F('total_paid') - obj.value                                                                     
                        if Fee.objects.filter(student=obj.student_id,kind="سيارة",year=StudentYear,verified=True).count()==1:
                            mystudent.bus_active = False
                    mystudent.save()
                    obj.verified = False
                    obj.save()
                    self.log_change(request, obj, 'unverified')
                    updated += 1                   
                else:
                    try:
                        archive = Archive.objects.get(code=mystudent.code,study_year=obj.year)
                        archive.total = F('total')-obj.value
                        archive.save()
                        obj.verified = False
                        obj.save()
                        self.log_change(request, obj, 'unverified')
                        updated += 1                        
                    except Archive.DoesNotExist:
                        cannot +=1
                # else:
                #     cannot +=1
            else:
                notupdated +=1

        if updated != 0:
            self.message_user(request, ngettext(
                '%d fee was successfully unverified.',
                '%d fees were successfully unverified.',
                updated,
            ) % updated, messages.SUCCESS)
        if notupdated != 0:
            self.message_user(request, ngettext(
                '%d fee was already unverified.',
                '%d fees were already unverified.',
                notupdated,
            ) % notupdated, messages.ERROR)
        if cannot != 0:
            self.message_user(request, ngettext(
                '%d fee can not unverified.',
                '%d fee can not unverified.',
                cannot,
            ) % cannot, messages.ERROR)

    def delete_queryset(self, request, queryset):

        for obj in queryset:
            if obj.verified == True:
                mystudent = Student.objects.get(id=obj.student_id)
                StudentYear = mystudent.year
                if obj.year == StudentYear:
                    #for book and book
                    if obj.kind[:3] == 'Boo':
                        mystudent.total_books = F('total_books')-obj.value
                        mystudent.books = False
                    elif obj.kind[:3] == 'Bok':
                        mystudent.total_books = F('total_books')-obj.value
                    elif obj.kind == 'دراسية':
                        mystudent.total_paid=F('total_paid') - obj.value
                        if Fee.objects.filter(student=obj.student_id,kind='دراسية',year=StudentYear,verified=True).count()==1:
                            try:
                                mystudentAff = StudentAff.objects.get(code=mystudent.code)
                                mystudentAff.payment_status = False
                                mystudentAff.save()
                            except StudentAff.DoesNotExist:
                                pass
                    elif obj.kind == 'سيارة':
                        mystudent.total_paid=F('total_paid') - obj.value                                                                     
                        if Fee.objects.filter(student=obj.student_id,kind="سيارة",year=StudentYear,verified=True).count()==1:
                            mystudent.bus_active = False
                    mystudent.save()
                else:
                    try:
                        archive = Archive.objects.get(code=mystudent.code,study_year=obj.year)
                        archive.total = F('total')-obj.value
                        archive.save()
                    except Archive.DoesNotExist:
                        pass
                obj.delete()
            else:
                obj.delete()

    def delete_model(self, request, obj):

        if obj.verified == True:
            mystudent = Student.objects.get(id=obj.student_id)
            StudentYear = mystudent.year
            if obj.year == StudentYear:
                #for book and book
                if obj.kind[:3] == 'Boo':
                    mystudent.total_books = F('total_books')-obj.value
                    mystudent.books = False
                elif obj.kind[:3] == 'Bok':
                    mystudent.total_books = F('total_books')-obj.value
                elif obj.kind == 'دراسية':
                    mystudent.total_paid=F('total_paid') - obj.value
                    if Fee.objects.filter(student=obj.student_id,kind='دراسية',year=StudentYear,verified=True).count()==1:
                        try:
                            mystudentAff = StudentAff.objects.get(code=mystudent.code)
                            mystudentAff.payment_status = False
                            mystudentAff.save()
                        except StudentAff.DoesNotExist:
                            pass
                elif obj.kind == 'سيارة':
                    mystudent.total_paid=F('total_paid') - obj.value                                                                     
                    if Fee.objects.filter(student=obj.student_id,kind="سيارة",year=StudentYear,verified=True).count()==1:
                        mystudent.bus_active = False
                    mystudent.save()
            else:
                try:
                    archive = Archive.objects.get(code=mystudent.code,study_year=obj.year)
                    archive.total = F('total')-obj.value
                    archive.save()
                except Archive.DoesNotExist:
                    pass
            obj.delete()
        else:
            obj.delete()

    actions = ['verified','unverified','out']

    # Adjust User Access ''''''''''''''''''''''''''''''''''''''''''
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
            return user_code in ('mosaad', 'mfisb', 'mfisg') or user_code[0] == 'a' and user_code[1] == 'c'
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.code == "mosaad"

admin.site.register(Fee, FeeAdmin)
