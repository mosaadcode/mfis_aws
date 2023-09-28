from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from student.models import Student as StudentAcc
from django.contrib.auth.hashers import make_password
from datetime import date,datetime
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django import forms

SCHOOL_CHOICES = (
    ('بنين','بنين'),
    ('بنات','بنات'),
    ('Ig','Ig'),
)

class School(models.Model):
    school = models.CharField(max_length=5)
    count = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.school+" "+str(self.count)

class Department(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Department'
        verbose_name_plural ='5_ اقسام وظائف'     

class Job(models.Model):

    TYPES_CHOICES = (
        ('إدارية','إدارية'),
        ('تعليمية','تعليمية'),
        ('خدمية','خدمية'),
    )
    GRADE_CHOICES = (
        ('10','رياض أطفال'),
        ('20','ابتدائى'),
        ('30','اعدادى'),
        ('40','ثانوى'),
        ('50','اعدادى وثانوى'),
    )
    type = models.CharField(max_length=7, choices=TYPES_CHOICES, verbose_name='نوع الوظيفة')
    title = models.CharField(max_length=20 ,verbose_name='المسمى الوظيفي')
    department = models.ForeignKey(Department, on_delete=SET_NULL, null=True,verbose_name='القسم')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True,blank=True,verbose_name='المرحلة الدراسية')

    def __str__(self):
        if self.department!=None:
            if self.grade != None:
                return  self.title + " " + self.department.name + ' ( ' + self.get_grade_display() + ' )'
            else:
                return  self.title + " " + self.department.name
        else:
            if self.grade != None:
                return self.title + ' ( ' + self.get_grade_display() + ' )'
            else:
                return self.title

    class Meta:
        verbose_name='job'
        verbose_name_plural ='4_ وظائف'        

class Employee(models.Model):
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES,verbose_name='المدرسة ')
    code = models.CharField(max_length=7, unique=True,blank=True)
    name = models.CharField(max_length=60,verbose_name='الإسم')
    na_id = models.CharField(max_length=14, unique=True,verbose_name='رقم قومي ')
    birth_date = models.DateField(null=True,blank=True, verbose_name='تاريخ الميلاد ')
    mobile_number = models.CharField(max_length=13, null=True,blank=True,verbose_name='هاتف محمول')
    phone_number = models.CharField(max_length=13, null=True,blank=True,verbose_name='هاتف المنزل ')
    emergency_phone = models.CharField(max_length=13, null=True,blank=True,verbose_name='هاتف طوارئ')
    email = models.EmailField(max_length=60, blank=True,null=True)
    address = models.CharField( max_length=86,null=True,blank=True,verbose_name='العنوان ')
    basic_certificate = models.CharField(max_length=96, blank=True, null=True,verbose_name='المؤهل الاساسي')
    is_educational = models.BooleanField(default=False,verbose_name='تربوي')
    attendance_date = models.DateField(null=True,blank=True,verbose_name='تاريخ الحضور')
    insurance_date = models.DateField(null=True,blank=True,verbose_name='تاريخ التأمين')
    participation_date = models.DateField(null=True,blank=True,verbose_name='تاريخ الاشتراك')
    contract_date = models.DateField(null=True,blank=True,verbose_name='تاريخ إعتماد العقد')
    insurance_no = models.CharField(max_length=10, unique=True,null=True,blank=True,verbose_name='الرقم التأميني')
    notes = models.TextField( max_length=260,null=True,blank=True,verbose_name='ملاحظات ')
    job = models.ForeignKey(Job, on_delete=SET_NULL,null=True, blank=True,verbose_name='الوظيفة')
    job_code = models.CharField(max_length=6,blank=True,null=True,verbose_name='')
    is_active = models.BooleanField(default=True,verbose_name='الحالة')
    salary_parameter = models.TextField( max_length=120,blank=True,null=True,verbose_name='عوامل تحديد الراتب ')
    salary = models.PositiveSmallIntegerField(null=True,blank=True,verbose_name='قيمة الراتب')
    message = models.CharField(max_length=260, null=True, blank=True)
    time_code = models.CharField(max_length=6,unique=True,blank=True,null=True,verbose_name='كود البصمة')
    perms = models.ForeignKey("Permission_setting", on_delete=models.SET_NULL,blank=True, null=True,verbose_name='إعدادات الاَذون ')
    vecation_role = models.ForeignKey("Vacation_setting", on_delete=models.SET_NULL,blank=True, null=True,verbose_name='إعدادات الإجازات ')
    times = models.ForeignKey("Time_setting", on_delete=models.SET_NULL,blank=True, null=True,verbose_name='الحضور والإنصراف')
    vacations = models.PositiveSmallIntegerField(default=0,verbose_name='اجازات ')
    vacations_s = models.PositiveSmallIntegerField(default=0,verbose_name='اجازات مرضي ')

    def get_code(self):
        if self.code == "":
            code_gen = []
            code_gen.append(self.na_id[1:3])
            if self.school == "بنين":
                code_gen.append('b')
            else:
                code_gen.append('g')
            myschool = School.objects.get(school=self.school)
            myschool.count +=1
            code_gen.append(format(myschool.count,'04'))
            myschool.save()
            return ''.join(code_gen)

    def get_birth_date(self):
        if self.birth_date is None:
            birth_date = datetime.strptime(self.na_id[1:3]+'-'+self.na_id[3:5]+'-'+self.na_id[5:7], '%y-%m-%d').date()
        return birth_date

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = self.get_code()
        if self.birth_date is None:
            self.birth_date = self.get_birth_date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code+" "+self.name

    class Meta:
        verbose_name='employee'
        verbose_name_plural ='1_ سجلات الموظفين'     

class ModifiedArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            **kwargs
        }
        return super(ArrayField, self).formfield(**defaults)


class Month(models.Model):
    STATUS_CHOSIES = (
        ('1','جديد'),
        ('2','قيد النشر'),
        ('3','مغلق'),
    )
    LABELS_CHOICES = (
    ("16", "16"),
    ("17", "17"),
    ("18", "18"),
    ("19", "19"),
    ("20", "20"),
    ("21", "21"),
    ("22", "22"),
    ("23", "23"),
    ("24", "24"),
    ("25", "25"),
    ("26", "26"),
    ("27", "27"),
    ("28", "28"),
    ("29", "29"),
    ("30", "30"),
    ("31", "31"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
    )
    code = models.CharField(max_length=7,verbose_name='شهر  ')
    perms = models.PositiveSmallIntegerField(default=4,verbose_name='الاُذون المتاحة  ')
    active=models.BooleanField(default=False,verbose_name='نشط  ')
    published =models.BooleanField(default=False,verbose_name='نشر  ')
    status=models.CharField(max_length=1,choices=STATUS_CHOSIES,default=1,verbose_name='الحالة  ')
    dayoff = ModifiedArrayField(
        models.CharField(
            choices=LABELS_CHOICES,
            max_length=100,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )  

    def __str__(self):
        return self.code

    class Meta:
        verbose_name='month'
        verbose_name_plural ='إعدادات الشهور'

class SalaryItem(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,verbose_name='إسم الموظف')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True,verbose_name='شهر ')
    item = models.CharField(max_length=66,verbose_name='الوصف')
    value = models.SmallIntegerField(verbose_name='القيمة')
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES,null=True,verbose_name='المدرسة ')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.month == "":
            self.month = Month.objects.get(active=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee.name

    class Meta:
        verbose_name='SalaryItem'
        verbose_name_plural ='4_ مفردات رواتب'   

class Vacation(models.Model):
    OFF_CHOICES = (
    ('إذن','إذن'),
    ('مرضي','مرضي'),
    ('من الرصيد','من الرصيد'),
)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,verbose_name='إسم الموظف')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True,verbose_name='شهر ')
    date_from = models.DateField(verbose_name='من')
    date_to = models.DateField(verbose_name='الى')
    reason = models.CharField (max_length=24,blank=True,null=True,verbose_name='السبب')
    type = models.CharField(max_length=9, choices=OFF_CHOICES,null=True,verbose_name='النوع')
    school = models.CharField(max_length=6, choices=SCHOOL_CHOICES,null=True,verbose_name='المدرسة')
    created = models.DateTimeField(auto_now_add=True)
    ok1 = models.BooleanField(default=False,verbose_name='مدير مباشر')
    ok2 = models.BooleanField(default=False,verbose_name='مدير أعلى')

    def save(self, *args, **kwargs):
        if self.month == "":
            self.month = Month.objects.last()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee.name

    class Meta:
        verbose_name='vacation'
        verbose_name_plural ='3_ إجازات سنوية'   

class Employee_month(models.Model):   
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,verbose_name='إسم الموظف')
    school = models.CharField(max_length=6, choices=SCHOOL_CHOICES,null=True,verbose_name='المدرسة')    
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True,verbose_name='شهر')
    is_active = models.BooleanField(default=True,verbose_name='نشط')
    permissions = models.PositiveSmallIntegerField(default=0,verbose_name='اَذون')
    vacations = models.PositiveSmallIntegerField(default=0,verbose_name='إجازات')
    salary_value =models.PositiveSmallIntegerField(default=0,verbose_name='الراتب')

    def __str__(self):
        return self.employee.code
    
    class Meta:
        # Add a unique constraint on employee and month fields
        unique_together = ('employee', 'month')

    class Meta:
        verbose_name='Employee Month'
        verbose_name_plural ='السجلات الشهرية' 

class Permission_setting(models.Model):
    school = models.CharField(max_length=6, choices=SCHOOL_CHOICES,blank=True,null=True,verbose_name='المدرسة') 
    name = models.CharField(max_length=26,verbose_name='الإسم')
    is_perms = models.BooleanField(default=False,verbose_name='السماح بالاَذون')
    is_morning = models.BooleanField(default=False,verbose_name='صباحي')
    is_evening = models.BooleanField(default=False,verbose_name='مسائي')
    is_between = models.BooleanField(default=False,verbose_name='داخلي')
    is_over = models.BooleanField(default=False,verbose_name='السماح بتجاوز عدد الاَذون')
    perms = models.PositiveSmallIntegerField(default=4,verbose_name='عدد الاّذون المتاحة خلال الشهر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='permation setting'
        verbose_name_plural ='إعدادات الاَذون'

class Vacation_setting(models.Model):
    school = models.CharField(max_length=6, choices=SCHOOL_CHOICES,blank=True,null=True,verbose_name='المدرسة') 
    name = models.CharField(max_length=26,verbose_name='الإسم')
    is_vacation = models.BooleanField(default=False,verbose_name='اجازة من الرصيد ')
    vacations = models.PositiveSmallIntegerField(default=0,verbose_name='رصيد اجازات ')
    vacations_s = models.PositiveSmallIntegerField(default=0,verbose_name='رصيد اجازات مرضي ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='vacation setting'
        verbose_name_plural ='إعدادات الاجازات'

class Time_setting(models.Model):
    name = models.CharField(max_length=26,verbose_name='مواعيد فئة')
    date = models.DateField(verbose_name='يوم')
    time_in = models.CharField(max_length=5,verbose_name='موعد الحضور')
    time_out = models.CharField(max_length=5,verbose_name='موعد الإنصراف')
    time_in_perm = models.CharField(max_length=5,verbose_name='حضور بإذن')
    time_out_perm = models.CharField(max_length=5,verbose_name='إنصراف بإذن')
    month = models.ForeignKey(Month, on_delete=SET_NULL, null=True,verbose_name='شهر ')
    school = models.CharField(max_length=6, choices=SCHOOL_CHOICES,blank=True,null=True,verbose_name='المدرسة') 
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Time setting'
        verbose_name_plural ='مواعيد الحضور والإنصراف'

class Permission(models.Model):
    PERM_CHOICES = (
    ('صباحي','صباحي'),
    ('داخلي','داخلي'),
    ('مسائي','مسائي'),
)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,verbose_name='إسم الموظف')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True,verbose_name='شهر ')
    date = models.DateField(verbose_name='تاريخ الإذن')
    reason = models.CharField (max_length=24,blank=True,null=True,verbose_name='السبب')
    type = models.CharField( max_length=5, choices=PERM_CHOICES,null=True,verbose_name='النوع ')
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES,null=True,verbose_name='المدرسة ')
    created = models.DateTimeField(auto_now_add=True)
    ok1 = models.BooleanField(default=False,verbose_name='مدير مباشر')
    ok2 = models.BooleanField(default=False,verbose_name='مدير أعلى')
    start_time = models.CharField(max_length=5,blank=True,null=True,verbose_name='من ساعة')
    end_time = models.CharField(max_length=5,blank=True,null=True,verbose_name='الى ساعة')

    def save(self, *args, **kwargs):
        if self.month == "":
            self.month = Month.objects.last()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee.name

    class Meta:
        verbose_name='permission'
        verbose_name_plural ='2_ اُذون يومية'   


def create_employ(sender, instance, created, **kwargs):
    if created:
        StudentAcc.objects.create(
            code=instance.code,
            username=instance.name,
            password=make_password(instance.code),
            school=instance.school,
            year='emp22',
            is_employ=True,
            )
post_save.connect(create_employ, sender=Employee)