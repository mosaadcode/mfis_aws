from django.shortcuts import render, redirect
from .forms import FeesForm
from .models import Fee
from student.forms import StudentForm, StudentArea
from student_affairs.models import Student as StudentAff

def dashboard(request):
    studentaff = StudentAff.objects.get(code=request.user.code)
    if studentaff.contact_status == False:
        request.session['error'] ='برجاء تحديث بيانات التواصل'
        return redirect('contact')
    else:
        student=request.user
        oldfee = student.old_fee - student.old_paid
        if len(str(request.user.living_area)) > 4 :
            bus = True
        else :
            bus = False
        msg = request.session.get('msg')
        error = request.session.get('error')
        request.session['msg'] = ''
        request.session['error'] = ''
        return render(request, 'fees/dashboard.html',{'oldfee':oldfee,'bus':bus,'msg':msg,'error':error})

def addfees(request):
    if request.method == 'GET':
        studentaff = StudentAff.objects.get(code=request.user.code)
        if studentaff.document_status == True :
            msg = request.session.get('msg')
            return render(request, 'fees/addfees.html', {'form':FeesForm(),'msg':msg})
        else:
            request.session['error'] ='لا يمكن التسجيل قبل إستيفاء كامل الاوراق المطلوبة'
            return redirect('dashboard')
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
                    SYear=request.user.year
                    if LYFee >0:
                        if int(request.POST['value']) <= LYFee:
                            newfee.year = '22-21'
                            newfee.save()
                        else:
                            newfee.value = LYFee
                            newfee.year ='22-21'
                            newfee.save()
                            form2 = FeesForm(request.POST)
                            newfee2 = form2.save(commit=False)
                            newfee2.student = request.user
                            newfee2.school = request.user.school
                            newfee2.value = int(request.POST['value']) - LYFee
                            newfee2.year = SYear
                            newfee2.save()
                    else:        
                        newfee.year = SYear
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
                if len(str(request.user.living_area)) > 4 :
                    # add try: except to solve value Error
                    try:
                        form = FeesForm(request.POST)
                        newfee = form.save(commit=False)
                        newfee.student = request.user
                        newfee.school = request.user.school
                        LYFee = request.user.old_fee - request.user.old_paid
                        SYear=request.user.year
                        if LYFee >0:
                            if int(request.POST['value']) <= LYFee:
                                newfee.year = '22-21'
                                newfee.save()
                            else:
                                newfee.value = LYFee
                                newfee.year ='22-21'
                                newfee.save()
                                form2 = FeesForm(request.POST)
                                newfee2 = form2.save(commit=False)
                                newfee2.student = request.user
                                newfee2.school = request.user.school
                                newfee2.value = int(request.POST['value']) - LYFee
                                newfee2.year = SYear
                                newfee2.save()
                        else:        
                            newfee.year = SYear
                            newfee.save()
                        request.session['msg'] = ''
                        return redirect('recorded')
                    except ValueError:
                            # tell user when error hapen
                            return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':'برجاء مراجعة البيانات'})
                else:
                    error = ' يجب اولاً الاطلاع على تعليمات اشتراك السيارة في الاعلى ثم تحديد المنطقة السكنية والعنوان '
                    request.session['error'] = error
                    return redirect('agreement')

        else:
            return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':'لا يمكنك التسجيل الان, برجاء مراجعة قسم الحسابات'})
def recorded(request):
    fees = Fee.objects.filter(student=request.user.id,year=request.user.year)
    return render(request, 'fees/recorded.html',{'fees':fees})


def agreement(request):
    if request.method == 'GET':
        error = request.session.get('error')
        return render(request, 'fees/agreement.html', {'form':StudentArea(),'error':error})
    else:
        if len(str(request.user.living_area)) < 5 :
            try:
                request.user.old_bus = request.POST['old_bus']
                request.user.living_area = request.POST['living_area']
                request.user.address = request.POST['address']
                request.user.save(update_fields=["old_bus", "living_area", "address"])
                request.session['error'] = ''
                msg = 'يمكنكم الان تسجيل ايصالات الدفع الخاصة بإشتراك السيارة'
                request.session['msg'] = msg
                return redirect('addfees')
            except ValueError:
                    # tell user when error hapen
                    return render(request, 'fees/agreement.html', {'form':FeesForm(),'error':'برجاء مراجعة البيانات'})
        else:
            return render(request, 'fees/agreement.html', {'form':FeesForm(),'error':' لا يمكنكم تغيير العنوان المسجل قبل التواصل مباشرة مع إدارة تشغيل السيارات'})
