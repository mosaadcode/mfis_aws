from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ngettext
from .models import Fee
from student.models import Student
from import_export.admin import ImportExportModelAdmin
from student.resources import FeesResource
from django.db.models import F

class FeesInline(admin.TabularInline):
    model = Fee
    can_delete = False
    # exclude = ('school',)
    readonly_fields = [
        'verified'
    ]
    extra = 0
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
        if obj.verified == True:
            return ('year','student','school','kind', 'value','bank_account','payment_date',) + self.readonly_fields
        return self.readonly_fields

    def verified(self, request, queryset):
        # updated = queryset.update(verified=True)
        updated = 0
        notupdated = 0
        for obj in queryset:
            if obj.verified == False:
                mystudent = Student.objects.get(id=obj.student_id)
                mystudent.total_paid=F('total_paid') + obj.value
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
                mystudent.total_paid=F('total_paid') - obj.value
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
                mystudent.total_paid=F('total_paid') - obj.value
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
            mystudent.total_paid=F('total_paid') - obj.value
            mystudent.save()
            obj.delete()
        else:
            obj.delete()
        """
        you can do anything here AFTER deleting the object
        """

        print('============================delete_model============================')

    actions = ['verified','unverified']



# class XeesAdmin(ImportExportModelAdmin):
#     pass
admin.site.register(Fee, FeeAdmin)
