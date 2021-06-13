from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, BooleanWidget
from fees.models import Fee
from .models import Student,Bus
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_text
from import_export.results import RowResult
from django.db.models import F

class FeesResource(resources.ModelResource):
    student = fields.Field(column_name='student',
                      attribute='student',
                      widget=ForeignKeyWidget(Student, 'code'))

    # def get_row_result_class(self):
    #     """
    #     Returns the class used to store the result of a row import.
    #     """
    #     return RowResult

    # delete = fields.Field(widget=BooleanWidget())
    # def for_delete(self, row, instance):
    #     row_result = self.get_row_result_class()
    #     row_result.object_id = instance.pk
    #     row_result.object_repr = force_text(instance)
    #     return self.fields['delete'].clean(row)

    def before_import_row(self,row, **kwargs):
        if row['verified']==True:
            mystudent = Student.objects.get(code=row['student'])
            if row['year'] == "22-21":
                mystudent.total_paid=F('total_paid') + row['value']
            else:
                mystudent.old_paid=F('old_paid') + row['value']
            mystudent.save()

    class Meta:
        model = Fee
        import_id_fields = ('id',)
        fields = ('id', 'student', 'student__username', 'school', 'student__grade', 'value', 'kind', 'bank_account','created','payment_date','year', 'verified')
        export_order = ('id', 'student', 'student__username', 'school', 'student__grade', 'value', 'kind', 'bank_account','created','payment_date','year', 'verified')

class StudentResource(resources.ModelResource):
    # if 'password' in self.fields.keys():
    def get_row_result_class(self):
        """
        Returns the class used to store the result of a row import.
        """
        return RowResult

    delete = fields.Field(widget=BooleanWidget())
    def for_delete(self, row, instance):
        row_result = self.get_row_result_class()
        row_result.object_id = instance.pk
        row_result.object_repr = force_text(instance)
        return self.fields['delete'].clean(row)

    def before_import_row(self,row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)

    class Meta:
        model = Student
        import_id_fields = ('code',)
        fields = ('year','code','username', 'password','school','grade','study_payment1','study_payment2','study_payment3','bus_payment1', 'bus_payment2','old_fee', 'old_paid', 'discount','total_paid','message','is_active', 'can_pay', 'bus_active', 'father_mobile', 'mother_mobile', 'phone_number', 'email', 'living_area', 'address', 'old_bus')
        export_order = ('year','code','username', 'password','school','grade','study_payment1','study_payment2','study_payment3','bus_payment1', 'bus_payment2','old_fee', 'old_paid', 'discount','total_paid','message','is_active', 'can_pay', 'bus_active', 'father_mobile', 'mother_mobile', 'phone_number', 'email', 'living_area', 'address', 'old_bus')

class BusStudentResource(resources.ModelResource):

    bus_number = fields.Field(column_name='bus_number',
                    attribute='bus_number',
                    widget=ForeignKeyWidget(Bus, 'number'))
    
    class Meta:
        model = Student
        import_id_fields = ('code',)
        fields = ('code','username','school','grade','bus_number','bus_active', 'father_mobile', 'mother_mobile', 'phone_number', 'email', 'living_area', 'address', 'old_bus')
        export_order = ('code','username','school','grade','bus_number','bus_active', 'father_mobile', 'mother_mobile', 'phone_number', 'email', 'living_area', 'address', 'old_bus')