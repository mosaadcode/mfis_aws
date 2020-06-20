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
    )
    GRADE_CHOICES = (
        (None, ""),
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

    code = models.CharField(max_length=7, unique=True)
    username = models.CharField(max_length=36,verbose_name='student name')
    school = models.CharField( max_length=4, choices=SCHOOL_CHOICES, blank=True)
    grade = models.CharField( max_length=16, choices=GRADE_CHOICES, blank=True)
    father_mobile = models.CharField(max_length=11, blank=True)
    mother_mobile = models.CharField(max_length=11, blank=True)
    phone_number = models.CharField(max_length=8, blank=True)
    email = models.EmailField(max_length=60, blank=True)

    study_payment1 = models.PositiveSmallIntegerField(default=0)
    study_payment3 = models.PositiveSmallIntegerField(default=0)

    bus_active = models.BooleanField( default=False)
    bus_payment2 = models.PositiveSmallIntegerField( default=0)
    total_paid = models.PositiveSmallIntegerField( default=0)
    def payment_status(self):
#due date 1st study and 1st bus
        if date.today() <= date(2020,9,30):
            if self.bus_active == True:
                return self.study_payment1 + 5000 - self.total_paid
            else:
                return self.study_payment1 - self.total_paid
#due date 1st study and ( 1st ,2nd ) bus payemnts
        elif date.today() <= date(2020,10,31):
            if self.bus_active == True:
                return self.study_payment1 + 5000 + self.bus_payment2 - self.total_paid
            else:
                return self.study_payment1 - self.total_paid
#due date (1st , 2nd) study and ( 1st ,2nd ) bus payemnts
        elif date.today() <= date(2020,12,31):
            if self.bus_active == True:
                return self.study_payment1 + 7000 + 5000 + self.bus_payment2 - self.total_paid
            else:
                return self.study_payment1 + 7000 - self.total_paid
#due date (1st , 2nd ,3rd) study and ( 1st ,2nd ) bus payemnts
        elif date.today() >= date(2021,1,1):
            if self.bus_active == True:
                return self.study_payment1 + 7000 + self.study_payment3 + 5000 + self.bus_payment2 - self.total_paid
            else:
                return self.study_payment1 + 7000 + self.study_payment3 - self.total_paid

    payment_status

    living_area = models.CharField( max_length=16, choices=AREA_CHOICES, blank=True)
    address = models.CharField( max_length=50, blank=True)
    old_bus = models.CharField( max_length=4, blank=True)
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
