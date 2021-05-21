from django.shortcuts import render, redirect, reverse
from .forms import FeesForm
from .models import Fee
from student.forms import StudentForm, StudentArea
# from django.contrib.auth import authenticate, login

def dashboard(request):
    # ddate1=DueDates.objects.get(pk=1)
    # ddate2=DueDates.objects.get(pk=2)
    # feess = Fees.objects.filter(student=request.user)
    student=request.user
    # fees = student.fee_set.all()
    #totalfees = feess.aggregate(Sum('value'))

    return render(request, 'fees/dashboard.html')

def addfees(request):
    if request.method == 'GET':
        # feess = Fees.objects.filter(student=request.user.id)
        return render(request, 'fees/addfees.html', {'form':FeesForm()})
    else:
        if request.user.can_pay == True:
            if request.POST['kind'] == "دراسية":
                # add try: except to solve value Error
                try:
                    form = FeesForm(request.POST)
                    newfee = form.save(commit=False)
                    newfee.student = request.user
                    newfee.school = request.user.school
                    LYFee = request.user.old_fee - request.user.old_paid
                    if LYFee >0:
                        if int(request.POST['value']) <= LYFee:
                            newfee.year = '21-20'
                            newfee.save()
                        else:
                            newfee.value = LYFee
                            newfee.year ='21-20'
                            newfee.save()
                            form2 = FeesForm(request.POST)
                            newfee2 = form2.save(commit=False)
                            newfee2.student = request.user
                            newfee2.school = request.user.school
                            newfee2.value = int(request.POST['value']) - LYFee
                            newfee2.year = '22-21'
                            newfee2.save()
                    else:        
                        newfee.year = '22-21'
                        newfee.save()
                    # update student data
                    # request.user.total_paid += int(request.POST['value'])
                    # request.user.save(update_fields=["total_paid"])
                    # redirect user to currenttodos page
                    return redirect('recorded')
                except ValueError:
                        # tell user when error hapen
                        return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':'برجاء مراجعة بيانات الايصال'})
            else:
                if request.user.bus_active == True:
                    # add try: except to solve value Error
                    try:
                        form = FeesForm(request.POST)
                        newfee = form.save(commit=False)
                        newfee.student = request.user
                        newfee.school = request.user.school
                        LYFee = request.user.old_fee - request.user.old_paid
                        if LYFee >0:
                            if int(request.POST['value']) <= LYFee:
                                newfee.year = '21-20'
                                newfee.save()
                            else:
                                newfee.value = LYFee
                                newfee.year ='21-20'
                                newfee.save()
                                form2 = FeesForm(request.POST)
                                newfee2 = form2.save(commit=False)
                                newfee2.student = request.user
                                newfee2.school = request.user.school
                                newfee2.value = int(request.POST['value']) - LYFee
                                newfee2.year = '22-21'
                                newfee2.save()
                        else:        
                            newfee.year = '22-21'
                            newfee.save()
                        return redirect('recorded')
                    except ValueError:
                            # tell user when error hapen
                            return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':'برجاء مراجعة البيانات'})
                else:
                    error = 'لا يمكن تسجيل الايصال قبل الموافقة على تعليمات السيارة وتحديد المنطقة السكنية في صفحة إشتراك السيارة اولاً'

                    return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':error})

        else:
            return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':'لا يمكنك التسجيل الان, برجاء مراجعة قسم الحسابات'})
def recorded(request):
    fees = Fee.objects.filter(student=request.user.id)
    return render(request, 'fees/recorded.html',{'fees':fees})


def agreement(request):
    if request.method == 'GET':
        return render(request, 'fees/agreement.html', {'form':StudentArea()})
    else:
        if request.user.bus_active == False:
            try:
                # # get the information from the post request and connect it with our form
                # form = AccountForm(request.POST)
                # # Create newtodo but dont't save it yet to the database
                # newfees = form.save(commit=False)
                # # set the user to newtodo
                # newfees.student = request.user
                # newfees.grade = request.user.grade
                # newfees.school = request.user.school
                # # save newtodo
                # newfees.save()
                # update student data
                request.user.bus_active = True
                request.user.old_bus = request.POST['old_bus']
                request.user.living_area = request.POST['living_area']
                request.user.address = request.POST['address']
                request.user.save(update_fields=["bus_active", "old_bus", "living_area", "address"])
                # redirect user to currenttodos page
                return redirect('dashboard')
            except ValueError:
                    # tell user when error hapen
                    return render(request, 'fees/agreement.html', {'form':FeesForm(),'error':'برجاء مراجعة البيانات'})
        else:
            return render(request, 'fees/agreement.html', {'form':FeesForm(),'error':'لتعديل البيانات يجب التواصل مع إدارة تشغيل السيارات'})
