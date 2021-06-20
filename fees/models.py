from django.db import models
# from account.models import Account

class Fee(models.Model):
    BankA_CHOICES = (
        ('نقدي بالمدرسة', 'نقدي بالمدرسة'),
        ('نقدي سلفيات', 'نقدي سلفيات'),
        ('تسوية مصروفات', 'تسوية مصروفات'),
        ('تحويل', 'تحويل'),
        ('1903530354880500015', '1903530354880500015'),
        ('1903530635939400011', '1903530635939400011'),
        ('1903530776181400019', '1903530776181400019'),
        ('1903530635939300017', '1903530635939300017'),
        ('1903530709961400015', '1903530709961400015'),
    )

    KIND_CHOICES = (
        ('دراسية', 'دراسية'),
        ('سيارة', 'سيارة'),
    )

    SCHOOL_CHOICES = (
        (None, ""),
        ('بنين', 'بنين'),
        ('بنات', 'بنات'),
        ('.بنات.', '.بنات.'),
    )

    YEAR_CHOICES = (
         ('21-20' , '21-20'),
         ('22-21' , '22-21'),
    )
    payment_date = models.DateField(null=True, blank=True,verbose_name='تاريخ الدفع ')
    bank_account = models.CharField(max_length=19, choices=BankA_CHOICES,verbose_name='حساب ')
    value = models.SmallIntegerField(null=True,verbose_name='قيمة ')
    created = models.DateTimeField(auto_now_add=True,verbose_name='تارخ تسجيل ')
    kind = models.CharField(max_length=6, choices=KIND_CHOICES,verbose_name='مصروفات ')
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES, blank=True,verbose_name='مدرسة ')
    student = models.ForeignKey(to='student.Student', on_delete=models.CASCADE, null=True,verbose_name='طالب ')
    verified = models.BooleanField(default=False,verbose_name='تحقق ')
    year = models.CharField( max_length=5,choices=YEAR_CHOICES, default='21-20',verbose_name='عام دراسي ')

    class Meta:
        verbose_name='fee'
        verbose_name_plural ='عمليات السداد '

    def __str__(self):
        return self.student.username
