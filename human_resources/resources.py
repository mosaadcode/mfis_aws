from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, BooleanWidget
from .models import Month,SalaryItem,Employee,Permission,School,Job,Employee_month,Time_setting
from import_export.results import RowResult
from operator import attrgetter

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

    def get_row_result_class(self):
        """
        Returns the class used to store the result of a row import.
        """
        return RowResult

    def before_import_row(self,row, **kwargs):
        if not row['code']:
            code_gen = []
            code_gen.append(row['na_id'][1:3])
            if row['school'] == "بنين":
                code_gen.append('b')
            else:
                code_gen.append('g')
            myschool = School.objects.get(school=row['school'])
            myschool.count +=1
            code_gen.append(format(myschool.count,'04'))
            myschool.save()
            row['code'] = ''.join(code_gen)

    class Meta:
        model = Employee
        import_id_fields = ('code',)
        fields = ('code','school','name','na_id','birth_date','mobile_number','phone_number','emergency_phone','email','address','basic_certificate','is_educational','attendance_date','insurance_date','participation_date','contract_date','insurance_no','notes','job','job_code','is_active','salary_parameter','salary','message','time_in','time_out','time_in_perm','time_out_perm','time_code')
        export_order = ('code','school','name','na_id','birth_date','mobile_number','phone_number','emergency_phone','email','address','basic_certificate','is_educational','attendance_date','insurance_date','participation_date','contract_date','insurance_no','notes','job','job_code','is_active','salary_parameter','salary','message','time_in','time_out','time_in_perm','time_out_perm','time_code')


class PermResource(resources.ModelResource):
    employee = fields.Field(column_name='employee',
                      attribute='employee',
                      widget=ForeignKeyWidget(Employee, 'code'))
    
    month = fields.Field(column_name='month',
                    attribute='month',
                    widget=ForeignKeyWidget(Month, 'code'))

    def before_import_row(self,row, **kwargs):
        if row['month']==None:
            row['month'] = active_month
        return row

    class Meta:
        model = Permission
        import_id_fields = ('id',)
        fields = ('id','school','employee','date','type','ok1','ok2','month')
        export_order = ('id','school','employee','date','type','ok1','ok2','month')

class Employee_monthResource(resources.ModelResource):
    employee = fields.Field(column_name='employee',
                      attribute='employee',
                      widget=ForeignKeyWidget(Employee, 'code'))
    
    month = fields.Field(column_name='month',
                      attribute='month',
                      widget=ForeignKeyWidget(Month, 'code'))
    
    # print(employee)
    # print(month)

    def before_import_row(self,row, **kwargs):
        if row['month']==None:
            row['month'] = active_month
        return row

    class Meta:
        model = Employee_month
        import_id_fields = ('id',)
        fields = ('id','school','employee','permissions','vacations','salary_value','is_active','month')
        export_order = ('id','school','employee','permissions','vacations','salary_value','is_active','month')

class Time_settingResource(resources.ModelResource):

    month = fields.Field(column_name='month',
                      attribute='month',
                      widget=ForeignKeyWidget(Month, 'code'))
    
    class Meta:
        model = Time_setting
        import_id_fields = ('id',)      
        fields = ('id','name','month','date','time_in','time_in_perm','time_out', 'time_out_perm','school')
        export_order = ('id','name','month','date','time_in','time_in_perm','time_out', 'time_out_perm','school')
    
    def export(self, queryset=None, *args, **kwargs):
        queryset = self.get_queryset() if queryset is None else queryset
        sorted_queryset = sorted(queryset, key=attrgetter('date'))
        return super().export(sorted_queryset, *args, **kwargs)