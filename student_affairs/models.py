from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from student.models import Student as StudentAcc, SchoolFee
from datetime import date,timedelta
from django.contrib.auth.hashers import make_password

current_year = '22-21'

class School(models.Model):
    school = models.CharField(max_length=5)
    count = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.school+" "+str(self.count)

class Governorate(models.Model):
    name = models.CharField(max_length=36)
    # class Meta:
    #     verbose_name='governorate'
    #     verbose_name_plural ='المحافظات والاقسام والمراكز '
    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=11)
    # class Meta:
    #     verbose_name='nationality'
    #     verbose_name_plural ='الجنسيات '
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=6)
    class Meta:
        verbose_name='class'
        verbose_name_plural =' B -  الفصول الدراسية'
    def __str__(self):
        return self.name

class Class_group(models.Model):
    name = models.CharField(max_length=6)
    class Meta:
        verbose_name='group'
        verbose_name_plural =' C -  مجموعات الفصول'
    def __str__(self):
        return self.name


class Student(models.Model):

    SCHOOL_CHOICES = (
        ('بنين', 'بنين'),
        ('بنات', 'بنات'),
        ('.بنات.', '.بنات.'),
    )
    STATUS_CHOICES = (
        # (None, ""),
        ('مستجد', 'مستجد'),
        ('منقول', 'منقول'),
        ('باقي', 'باقي للإعادة'),
        ('محول', 'محول'),
        ('محول من', 'محول من'),
        ('عائد','عائد'),
        ('وافد','وافد'),
    )
    GRADE_CHOICES = (
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
        ('خريج','خريج'),
    )

    RELIGION_CHOICES = (
        ('مسلم','مسلم'),
        ('مسيحي','مسيحي'),
    )

    RESPONSIBILITY_CHOICES = (
        ('الاب','الاب'),
        ('الام','الام'),
        ('الاب والام','الاب والام'),
    )    

    OVER_CHOICES =(
        ('No',''),
        ('ضابط','ضابط'),
        ('وزير','وزير'),
        ('بعثات','بعثات'),
    )   

    KIND_CHOICES = (
        ('ذكر','ذكر'),
        ('اُنثى','اُنثى'),
    )
    code = models.CharField(max_length=7, unique=True,blank=True,verbose_name='الكود ')
    global_code = models.CharField(max_length=9,blank=True,null=True,verbose_name='كود الوزارة ')
    name = models.CharField(max_length=60,verbose_name='إسم الطالب ')
    en_name = models.CharField(max_length=60, blank=True, null=True,verbose_name='الإسم بالانجلزية ')
    kind = models.CharField(max_length=5,choices=KIND_CHOICES,blank=True,null=True,verbose_name='النوع ')
    student_id = models.CharField(max_length=14, blank=True, null=True,verbose_name='رقم قومي ')
    status = models.CharField( max_length=7, choices=STATUS_CHOICES,default='مستجد',verbose_name='حالة القيد ')
    status_no = models.CharField(max_length=7, blank=True, null=True,verbose_name='رقم القيد ')
    from_to = models.CharField(max_length=32,blank=True,null=True,verbose_name='')
    study_year = models.CharField( max_length=5, default = current_year,verbose_name='العام الدراسي ')
    start_year = models.CharField( max_length=5,blank=True,verbose_name='سنة الالتحاق ')
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES,verbose_name='المدرسة ')
    grade = models.CharField( max_length=16, choices=GRADE_CHOICES,verbose_name='الصف ')
    Class = models.ForeignKey(Class,on_delete=models.SET_NULL, null=True,blank=True,verbose_name='الفصل ')
    group = models.ForeignKey(Class_group,on_delete=models.SET_NULL, null=True,blank=True,verbose_name='المجموعة ')
    religion = models.CharField(max_length=5,choices=RELIGION_CHOICES,default='مسلم',blank=True,null=True,verbose_name='الديانة ')
    nationality = models.ForeignKey(Nationality,on_delete=SET_NULL, blank=True,null=True,verbose_name='الجنسية ')
    is_over = models.CharField( max_length=5, choices=OVER_CHOICES,default='',verbose_name='فوق الكثافة ')
    birth_date = models.DateField(null=True,blank=True, verbose_name='تاريخ الميلاد ')
    birth_gov = models.ForeignKey(Governorate,on_delete=SET_NULL, null=True,blank=True,verbose_name='محل الميلاد ')
    age1oct = models.CharField(default="",max_length=8,null=True,blank=True,verbose_name='(يوم- شهر- سنة) العمر اول اكتوبر ')
    father_name = models.CharField(max_length=46,null=True, blank=True,verbose_name='إسم الاب ')
    father_job = models.CharField(max_length=60,null=True, blank=True,verbose_name='الوظيفة ')
    father_id = models.CharField(max_length=14, null=True,blank=True,verbose_name='رقم قومي ')
    mother_name = models.CharField(max_length=46, null=True,blank=True,verbose_name='إسم الام ')
    mother_job = models.CharField(max_length=60,null=True, blank=True,verbose_name='الوظيفة ')
    responsibility = models.CharField(max_length=11,choices=RESPONSIBILITY_CHOICES,default='الاب والام',blank=True,null=True,verbose_name='الولاية التعليمية ')    
    father_mobile = models.CharField(max_length=14, null=True,blank=True,verbose_name='هاتف الاب ')
    mother_mobile = models.CharField(max_length=11, null=True,blank=True,verbose_name='هاتف الام ')
    phone_number = models.CharField(max_length=11, null=True,blank=True,verbose_name='هاتف المنزل ')
    phone_number2 = models.CharField(max_length=11, null=True,blank=True,verbose_name='هاتف بديل ')
    address_1 = models.CharField( max_length=86,null=True,blank=True,verbose_name='العنوان ')
    # address_2 = models.CharField( max_length=64,null=True,blank=True,verbose_name='العنوان البديل ')
    email = models.EmailField(max_length=60, blank=True,null=True)
    notes = models.TextField( max_length=250,null=True,blank=True,verbose_name='ملاحظات ')
    payment_status = models.BooleanField(default=False,verbose_name='حالة السداد ')


    def __str__(self):
        return self.name + " " + self.code

    def get_code(self):
        if self.code == "":
            code_gen = []
            if self.school == "بنين":
                code_gen.append('2')
            else:
                code_gen.append('3')
            code_gen.append(self.study_year[3:])
            if self.school == ".بنات.":
                myschool = School.objects.get(school="بنات")
            else:
                myschool = School.objects.get(school=self.school)
            myschool.count +=1
            code_gen.append(format(myschool.count,'04'))
            myschool.save()
            return ''.join(code_gen)


    def myage(self):
        if self.birth_date !=None:
            ret = []
            age = date(2021,10,1) - self.birth_date
            num_years = int(age.days / 365.2425)
            if num_years >= 0:
                age -= timedelta(days=num_years * 365.2425)
                num_years = format(num_years,'02')
                ret.append(num_years)
            num_months = int(age.days / 30.436875)
            if num_months >= 0:
                age -= timedelta(days=num_months * 30.436875)
                num_months = format(num_months,'02')
                ret.append(num_months)
            if age.days >= 0:
                days = format(age.days,'02')
                ret.append(days)
            return '-'.join(ret)
        return ""
    
    # def brothers(self):
    #     return Student.objects.filter(father_id=self.father_id).count()-1


    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = self.get_code()
        self.age1oct = self.myage()
        if self.start_year == "":
            self.start_year = self.study_year
        super().save(*args, **kwargs)

    class Meta:
        verbose_name='student'
        verbose_name_plural =' A -  سجلات الطلاب'



def create_student(sender, instance, created, **kwargs):
    if created:
        GradeFee = SchoolFee.objects.get(school=instance.school,grade=instance.grade)
        StudentAcc.objects.create(
            code=instance.code,
            username=instance.name,
            password=make_password(instance.code),
            school=instance.school,
            grade=instance.grade,
            year=instance.study_year,
            study_payment1=GradeFee.study_payment1,
            study_payment2=GradeFee.study_payment2,
            study_payment3=GradeFee.study_payment3,
            bus_payment1=GradeFee.bus_payment1,
            bus_payment2=GradeFee.bus_payment2,
            )
post_save.connect(create_student, sender=Student)


def update_student(sender, instance, created, **kwargs):
    if created ==False:
        GradeFee = SchoolFee.objects.get(school=instance.school,grade=instance.grade)
        StudentAcc.objects.filter(code=instance.code).update(
            username=instance.name,
            school=instance.school,
            grade=instance.grade,
            year=instance.study_year,
            study_payment1=GradeFee.study_payment1,
            study_payment2=GradeFee.study_payment2,
            study_payment3=GradeFee.study_payment3,
            bus_payment1=GradeFee.bus_payment1,
            bus_payment2=GradeFee.bus_payment2,
        )
post_save.connect(update_student, Student)