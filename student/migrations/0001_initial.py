# Generated by Django 3.0.4 on 2020-05-29 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('code', models.CharField(max_length=7, unique=True)),
                ('username', models.CharField(max_length=36, verbose_name='student name')),
                ('school', models.CharField(blank=True, choices=[(None, ''), ('بنين', 'بنين'), ('بنات', 'بنات')], max_length=4)),
                ('grade', models.CharField(blank=True, choices=[(None, ''), ('ثانية حضانة', 'ثانية حضانة'), ('الاول الابتدائى', 'الاول الابتدائى'), ('الثانى الابتدائى', 'الثانى الابتدائى'), ('الثالث الابتدائى', 'الثالث الابتدائى'), ('الرابع الابتدائى', 'الرابع الابتدائى'), ('الخامس الابتدائى', 'الخامس الابتدائى'), ('السادس الابتدائى', 'السادس الابتدائى'), ('الاول الاعدادى', 'الاول الاعدادى'), ('الثانى الاعدادى', 'الثانى الاعدادى'), ('الثالث الاعدادى', 'الثالث الاعدادى'), ('الاول الثانوى', 'الاول الثانوى'), ('الثانى الثانوى', 'الثانى الثانوى'), ('الثالث الثانوى', 'الثالث الثانوى')], max_length=16)),
                ('father_mobile', models.CharField(blank=True, max_length=11)),
                ('mother_mobile', models.CharField(blank=True, max_length=11)),
                ('phone_number', models.CharField(blank=True, max_length=8)),
                ('email', models.EmailField(blank=True, max_length=60)),
                ('study_payment1', models.PositiveSmallIntegerField(default=0)),
                ('study_payment3', models.PositiveSmallIntegerField(default=0)),
                ('bus_active', models.BooleanField(default=False)),
                ('bus_payment2', models.PositiveSmallIntegerField(default=0)),
                ('total_paid', models.PositiveSmallIntegerField(default=0)),
                ('living_area', models.CharField(blank=True, choices=[(None, ''), ('النزهة الجديدة', 'النزهة الجديدة'), ('شيراتون', 'شيراتون'), ('مصر الجديدة', 'مصر الجديدة'), ('الزيتون', 'الزيتون'), ('حدائق القبة', 'حدائق القبة'), ('العباسية', 'العباسية'), ('مدينة نصر', 'مدينة نصر'), ('إمتداد رمسيس', 'إمتداد رمسيس'), ('المعادى', 'المعادى'), ('المقطم', 'المقطم'), ('مدينتى', 'مدينتى'), ('الرحاب', 'الرحاب'), ('التجمع الاول', 'التجمع الاول'), ('التجمع الثالث', 'التجمع الثالث'), ('التجمع الخامس', 'التجمع الخامس')], max_length=16)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('old_bus', models.CharField(blank=True, max_length=4)),
                ('message', models.CharField(blank=True, max_length=260)),
                ('is_active', models.BooleanField(default=True)),
                ('can_pay', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
