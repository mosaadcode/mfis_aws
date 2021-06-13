from django.db import models
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db.models import Sum
from datetime import date

class Grade(models.Model):
    name = models.CharField(max_length=24, blank=True)
    def __str__(self):
        return self.name

AREA_CHOICES = (
    (None, ""),
    ('النزهة الجديدة','النزهة الجديدة'),
    ('شيراتون','شيراتون'),
    ('مصر الجديدة','مصر الجديدة'),
    ('الزيتون','الزيتون'),
    ('حدائق القبة','حدائق القبة'),
    ('العباسية','العباسية'),
    ('مدينة نصر','مدينة نصر'),
    ('إمتداد رمسيس','إمتداد رمسيس'),
    ('المعادى','المعادى'),
    ('المقطم','المقطم'),
    ('مدينتى','مدينتى'),
    ('الرحاب','الرحاب'),
    ('التجمع الاول','التجمع الاول'),
    ('التجمع الثالث','التجمع الثالث'),
    ('التجمع الخامس','التجمع الخامس'),
)

class Bus(models.Model):
    SCHOOL_CHOICES1 = (
        (None, ""),
        ('بنين', 'بنين'),
        ('بنات', 'بنات'),
    )

    number = models.CharField(unique=True,max_length=4,verbose_name='رقم السيارة')
    area = models.CharField( max_length=16, choices=AREA_CHOICES, blank=True,null=True,verbose_name='المنطقة')
    sub_area = models.CharField(max_length=24,blank=True,null=True,verbose_name='المنطقة الفرعية')
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES1,verbose_name='المدرسة')
    driver_name = models.CharField(max_length=24,blank=True,null=True,verbose_name='اسم السائق')
    driver_mobile = models.CharField(max_length=11,blank=True,null=True,verbose_name='تليفون السائق')
    supervisor_name = models.CharField(max_length=24,blank=True,null=True,verbose_name='اسم المشرف')
    supervisor_mobile = models.CharField(max_length=11,blank=True,null=True,verbose_name='تليفون المشرف')

    def students(self):
        return Student.objects.filter(bus_number=self.id).count()
    students

    def __str__(self):
        return self.number 

class StudentManager(BaseUserManager):
    def create_user(self, code, username, password=None):
        if not code:
            raise ValueError("Users must have a code")
        if not username:
            raise ValueError("Users must have a name")
        user = self.model(
               code = code,
               username = username,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, code, username, password):
        user = self.create_user(
               code = code,
               password = password,
               username = username,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Student(AbstractBaseUser, PermissionsMixin):
    SCHOOL_CHOICES = (
        (None, ""),
        ('بنين', 'بنين'),
        ('بنات', 'بنات'),
        ('.بنات.', '.بنات.'),
    )
    GRADE_CHOICES = (
        (None, ""),
        ('تمهيدى حضانة', 'تمهيدى حضانة'),
        ('اولى حضانة', 'اولى حضانة'),
        ('ثانية حضانة', 'ثانية حضانة'),
        ('الاول الابتدائى','الاول الابتدائى'),
        ('الثانى الابتدائى','الثانى الابتدائى'),
        ('الثالث الابتدائى','الثالث الابتدائى'),
        ('الرابع الابتدائى','الرابع الابتدائى'),
        ('الخامس الابتدائى','الخامس الابتدائى'),
        ('السادس الابتدائى','السادس الابتدائى'),
        ('الاول الاعدادى','الاول الاعدادى'),
        ('الثانى الاعدادى','الثانى الاعدادى'),
        ('الثالث الاعدادى','الثالث الاعدادى'),
        ('الاول الثانوى','الاول الثانوى'),
        ('الثانى الثانوى','الثانى الثانوى'),
        ('الثالث الثانوى','الثالث الثانوى'),
    )

    YEAR_CHOICES = (
         ('21-20' , '21-20'),
         ('22-21' , '22-21'),
    )

    code = models.CharField(max_length=7, unique=True)
    username = models.CharField(max_length=60,verbose_name='student name')
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES, blank=True)
    grade = models.CharField( max_length=16, choices=GRADE_CHOICES, blank=True)
    father_mobile = models.CharField(max_length=11, null=True, blank=True)
    mother_mobile = models.CharField(max_length=11, null=True, blank=True)
    phone_number = models.CharField(max_length=8, null=True, blank=True)
    email = models.EmailField(max_length=60, null=True, blank=True)

    year = models.CharField( max_length=5,choices=YEAR_CHOICES, default='22-21')

    study_payment1 = models.PositiveSmallIntegerField(default=0,verbose_name='Study 1')
    study_payment2 = models.PositiveSmallIntegerField(default=0,verbose_name='Study 2')
    study_payment3 = models.PositiveSmallIntegerField(default=0,verbose_name='Study 3')
    discount = models.PositiveSmallIntegerField(default=0)
    old_fee = models.SmallIntegerField(default=0)

    bus_active = models.BooleanField( default=False)
    bus_payment1 = models.PositiveSmallIntegerField( default=10000,verbose_name='Bus 1')
    bus_payment2 = models.PositiveSmallIntegerField( default=0,verbose_name='Bus 2')
    total_paid = models.IntegerField(default=0)
    old_paid = models.SmallIntegerField( verbose_name='Old Fee paid', default=0)
    def payment_status(self):
#due date 1st study and 1st bus
        if date.today() <= date(2020,9,30):
            if self.bus_active == True:
                return self.study_payment1 + self.bus_payment1 - self.total_paid - self.discount + self.old_fee - self.old_paid
            else:
                return self.study_payment1 - self.total_paid - self.discount + self.old_fee - self.old_paid
#due date 1st study and ( 1st ,2nd ) bus payemnts
        elif date.today() <= date(2020,10,31):
            if self.bus_active == True:
                return self.study_payment1 + self.bus_payment1 + self.bus_payment2 - self.total_paid - self.discount + self.old_fee - self.old_paid
            else:
                return self.study_payment1 - self.total_paid - self.discount + self.old_fee - self.old_paid
#due date (1st , 2nd) study and ( 1st ,2nd ) bus payemnts
        elif date.today() <= date(2020,12,31):
            if self.bus_active == True:
                return self.study_payment1 + self.study_payment2 + self.bus_payment1 + self.bus_payment2 - self.total_paid - self.discount + self.old_fee - self.old_paid
            else:
                return self.study_payment1 + self.study_payment2 - self.total_paid - self.discount + self.old_fee - self.old_paid
#due date (1st , 2nd ,3rd) study and ( 1st ,2nd ) bus payemnts
        elif date.today() >= date(2021,1,1):
            if self.bus_active == True:
                return self.study_payment1 + self.study_payment2 + self.study_payment3 + self.bus_payment1 + self.bus_payment2 - self.total_paid - self.discount + self.old_fee - self.old_paid
            else:
                return self.study_payment1 + self.study_payment2 + self.study_payment3 - self.total_paid - self.discount + self.old_fee - self.old_paid

    payment_status

    living_area = models.CharField( max_length=16, choices=AREA_CHOICES,null=True,blank=True,verbose_name='المنطقة السكنية ')
    address = models.CharField( max_length=50,null=True,blank=True,verbose_name='العنوان ')
    old_bus = models.CharField( max_length=4,null=True,blank=True,verbose_name='رقم سيارة العام السابق ')
    bus_number = models.ForeignKey(Bus, on_delete=models.CASCADE,null=True, blank=True,verbose_name='رقم السيارة ')
    message = models.CharField(max_length=260, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    can_pay = models.BooleanField(default=True)
    is_admin  = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    objects = StudentManager()

    USERNAME_FIELD = 'code'
    REQUIRED_FIELDS = ['username',]


    def __str__(self):
        return self.username + " " + self.code
    # # def __str__(self):
    # #     return self.code
    #
    #
    def has_perm(self, perm, obj=None):
        return self.is_admin
        # return True

    def has_module_perms(self, app_label):
        return True

class BusStudent(Student):
    class Meta:
        proxy = True
