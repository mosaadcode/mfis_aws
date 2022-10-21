from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, BooleanWidget
from .models import Month,SalaryItem,Employee,Permission,Job

try:
    active_month = Month.objects.get(active=True)
except Month.DoesNotExist:
    pass

class SalaryItemResource(resources.ModelResource):
    employee = fields.Field(column_name='employee',
                      attribute='employee',
                      widget=ForeignKeyWidget(Employee, 'code'))

    def before_import_row(self,row, **kwargs):
        if row['month']==None:
            row['month'] = active_month
        return row

    class Meta:
        model = SalaryItem
        import_id_fields = ('id',)
        fields = ('id','school','employee','item','value','month')
        export_order = ('id','school','employee','item','value','month')

class EmployeeResource(resources.ModelResource):

    # job = fields.Field(column_name='job',
    #                   attribute='job',
    #                   widget=ForeignKeyWidget(Job, 'title'))

    # def before_import_row(self,row, **kwargs):
    #     if row['month']==None:
    #         row['month'] = active_month
    #     return row

    class Meta:
        model = Employee
        import_id_fields = ('code',)
        fields = ('code','school','name','na_id','birth_date','mobile_number','phone_number','emergency_phone','email','address','basic_certificate','is_educational','attendance_date','insurance_date','participation_date','contract_date','insurance_no','notes','job','is_active','salary_parameter','salary','message')
        export_order = ('code','school','name','na_id','birth_date','mobile_number','phone_number','emergency_phone','email','address','basic_certificate','is_educational','attendance_date','insurance_date','participation_date','contract_date','insurance_no','notes','job','is_active','salary_parameter','salary','message')


class PermResource(resources.ModelResource):
    employee = fields.Field(column_name='employee',
                      attribute='employee',
                      widget=ForeignKeyWidget(Employee, 'code'))

    def before_import_row(self,row, **kwargs):
        if row['month']==None:
            row['month'] = active_month
        return row

    class Meta:
        model = Permission
        import_id_fields = ('id',)
        fields = ('id','school','employee','date','type','verified','month')
        export_order = ('id','school','employee','date','type','verified','month')