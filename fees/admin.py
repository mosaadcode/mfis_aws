from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ngettext
from .models import Fee
from student.models import Student
from import_export.admin import ImportExportModelAdmin
from student.resources import FeesResource
from django.db.models import F
from student_affairs.models import Student as StudentAff

class FeesInline(admin.TabularInline):
    model = Fee
    can_delete = False
    # exclude = ('school',)
    readonly_fields = [
        'verified'
    ]
    extra = 0
    ordering = ('-year','-created')
    def has_change_permission(self, request, obj=None):
        return False
    # def has_add_permission(self, request, obj=None):
    # return False


class FeeAdmin(ImportExportModelAdmin):
    list_display = ('student', 'value', 'school', 'kind', 'bank_account', 'payment_date' , 'created','verified')
    autocomplete_fields = ['student']
    search_fields = ('student__code','student__username')
    readonly_fields = ('created','verified')

    filter_horizontal = ()
    list_filter = ('school', 'year', 'verified', 'kind', 'payment_date','bank_account', 'created', )
    fieldsets = ()
    resource_class = FeesResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.verified == True:
                return ('year','student','school','kind', 'value','bank_account','payment_date',) + self.readonly_fields
            return self.readonly_fields
        return self.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.code =="mfisb":
            return qs.filter(school="بنين")
        elif request.user.code == "mfisg":
            # return qs.filter(Q(school='.بنات.')| Q(school='بنات'))
            return qs.filter(school__in = ('.بنات.', 'بنات'))
        return qs

    def verified(self, request, queryset):
        # updated = queryset.update(verified=True)
        updated = 0
        notupdated = 0
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
                else:
                    mystudent.old_paid=F('old_paid') + obj.value
                mystudent.save()
                obj.verified = True
                obj.save()
                self.log_change(request, obj, 'verified')
                updated += 1
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
        
    verified.short_description = "Ok Verified"

    def unverified(self, request, queryset):
        # updated = queryset.update(verified=False)
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.verified == True:
                mystudent = Student.objects.get(id=obj.student_id)
                SYear=mystudent.year
                if obj.year == SYear:
                    #for book and book
                    if obj.kind[:3] == 'Boo':
                        mystudent.total_books = F('total_books')-obj.value
                        mystudent.books = False
                    elif obj.kind[:3] == 'Bok':
                        mystudent.total_books = F('total_books')-obj.value
                    elif obj.kind == 'دراسية':
                        mystudent.total_paid=F('total_paid') - obj.value
                        try:
                            mystudentAff = StudentAff.objects.get(code=mystudent.code)
                            mystudentAff.payment_status = False
                            mystudentAff.save()
                        except StudentAff.DoesNotExist:
                            pass
                    elif obj.kind == 'سيارة':
                        mystudent.total_paid=F('total_paid') - obj.value                                                                     
                        if Fee.objects.filter(student=obj.student_id,kind="سيارة",year="22-21",verified=True).count()==1:
                            mystudent.bus_active = False
                else:
                    mystudent.old_paid=F('old_paid') - obj.value
                mystudent.save()
                obj.verified = False
                obj.save()
                self.log_change(request, obj, 'unverified')
                updated += 1
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

    def delete_queryset(self, request, queryset):
        print('==========================delete_queryset==========================')
        print(queryset)

        """
        you can do anything here BEFORE deleting the object(s)
        """
        for obj in queryset:
            if obj.verified == True:
                mystudent = Student.objects.get(id=obj.student_id)
                SYear=mystudent.year
                if obj.year == SYear:
                    #for book and book
                    if obj.kind[:3] == 'Boo':
                        mystudent.total_books = F('total_books')-obj.value
                        mystudent.books = False
                    elif obj.kind[:3] == 'Bok':
                        mystudent.total_books = F('total_books')-obj.value
                    elif obj.kind == 'دراسية':
                        mystudent.total_paid=F('total_paid') - obj.value
                        try:
                            mystudentAff = StudentAff.objects.get(code=mystudent.code)
                            mystudentAff.payment_status = False
                            mystudentAff.save()
                        except StudentAff.DoesNotExist:
                            pass
                    elif obj.kind == 'سيارة':
                        mystudent.total_paid=F('total_paid') - obj.value                                                                     
                        if Fee.objects.filter(student=obj.student_id,kind="سيارة",year="22-21",verified=True).count()==1:
                            mystudent.bus_active = False
                else:
                    mystudent.old_paid=F('old_paid') - obj.value
                mystudent.save()
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
        if obj.verified == True:
            mystudent = Student.objects.get(id=obj.student_id)
            SYear=mystudent.year
            if obj.year == SYear:
                #for book and book
                if obj.kind[:3] == 'Boo':
                    mystudent.total_books = F('total_books')-obj.value
                    mystudent.books = False
                elif obj.kind[:3] == 'Bok':
                    mystudent.total_books = F('total_books')-obj.value
                elif obj.kind == 'دراسية':
                    mystudent.total_paid=F('total_paid') - obj.value
                    try:
                        mystudentAff = StudentAff.objects.get(code=mystudent.code)
                        mystudentAff.payment_status = False
                        mystudentAff.save()
                    except StudentAff.DoesNotExist:
                        pass
                elif obj.kind == 'سيارة':
                    mystudent.total_paid=F('total_paid') - obj.value                                                                     
                    if Fee.objects.filter(student=obj.student_id,kind="سيارة",year="22-21",verified=True).count()==1:
                        mystudent.bus_active = False
            else:
                mystudent.old_paid=F('old_paid') - obj.value
            mystudent.save()
            obj.delete()
        else:
            obj.delete()
        """
        you can do anything here AFTER deleting the object
        """

        print('============================delete_model============================')

    actions = ['verified','unverified']

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.code in ('mosaad','mfisb','mfisg'):
                return True
            return False


# class XeesAdmin(ImportExportModelAdmin):
#     pass
admin.site.register(Fee, FeeAdmin)
