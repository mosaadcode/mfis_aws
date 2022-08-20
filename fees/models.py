from django.db import models
# from account.models import Account

class Fee(models.Model):
    BankA_CHOICES = (
        ('نقدي بالمدرسة', 'نقدي بالمدرسة'),
        ('نقدي سلفيات', 'نقدي سلفيات'),
        ('تسوية مصروفات', 'تسوية مصروفات'),
        ('تحويل', 'تحويل'),
        ('Ig تحويل', 'Ig تحويل'),
        ('تحويل الفاروق', 'تحويل الفاروق'),
        ('سحب', 'سحب'),
        ('خصم', 'خصم'),
        ('خصم سحب', 'خصم سحب'),
        ('تقسيط', 'تقسيط'),
        ('1903530354880500015', '1903530354880500015'),
        ('1903530635939400011', '1903530635939400011'),
        ('1903530776181400019', '1903530776181400019'),
        ('1903530635939300017', '1903530635939300017'),
        ('1903530709961400015', '1903530709961400015'),
    )

    KIND_CHOICES = (
        ('دراسية', 'دراسية'),
        ('سيارة', 'سيارة'),
        ('Books','Books-All'),
        ('Book','Books-Books'),
        ('Boklet','Books-Booklet'),
        ('BokAlv','Books-A_level'),
    )

    SCHOOL_CHOICES = (
        (None, ""),
        ('بنين', 'بنين'),
        ('بنات', 'بنات'),
        ('.بنات.', '.بنات.'),
        ('Out-b','Out-b'),
        ('Out-g','Out-g'),
    )

    YEAR_CHOICES = (
         ('21-20' , '21-20'),
         ('22-21' , '22-21'),
         ('23-22' , '23-22'),
    )
    payment_date = models.DateField(null=True, blank=True)
    bank_account = models.CharField(max_length=19, choices=BankA_CHOICES)
    value = models.SmallIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=6, choices=KIND_CHOICES)
    school = models.CharField( max_length=6, choices=SCHOOL_CHOICES, blank=True)
    student = models.ForeignKey(to='student.Student', on_delete=models.CASCADE, null=True)
    verified = models.BooleanField(default=False)
    year = models.CharField( max_length=5,choices=YEAR_CHOICES, default='23-22')

    # class Meta:
    #     verbose_name='fee'
    #     verbose_name_plural ='عمليات السداد '
    def __str__(self):
        return self.student.username
