from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from fees.models import Fee
from .models import Student
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_text
from import_export.results import RowResult

class FeesResource(resources.ModelResource):
    student = fields.Field(column_name='student',
                      attribute='student',
                      widget=ForeignKeyWidget(Student, 'code'))

    class Meta:
        model = Fee
        import_id_fields = ('id',)
        fields = ('id', 'student', 'student__username', 'school', 'student__grade', 'value', 'kind', 'bank_account','created','payment_date')
        export_order = ('id','student', 'student__username', 'school', 'student__grade', 'value', 'kind','bank_account','created','payment_date')

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
        fields = ('code','username', 'password','school', 'grade', 'study_payment1', 'study_payment3', 'bus_payment2','message','total_paid','is_active', 'can_pay','father_mobile', 'mother_mobile', 'phone_number', 'email', 'living_area', 'address', 'old_bus')
        export_order = ('code','username', 'password','school', 'grade', 'study_payment1', 'study_payment3', 'bus_payment2','message','total_paid','is_active', 'can_pay','father_mobile', 'mother_mobile', 'phone_number', 'email', 'living_area', 'address', 'old_bus')
