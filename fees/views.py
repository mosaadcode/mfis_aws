from django.shortcuts import render, redirect
from .forms import FeesForm
from .models import Fee
from student.forms import StudentForm, StudentArea
from student_affairs.models import Student as StudentAff
from student.models import Archive

last_year = '24-23'

def dashboard(request):
    try:
        OldVale = Archive.objects.get(code=request.user.code,study_year=last_year).year_status()
        OldVale=int(OldVale)
        if OldVale < 0 :
            OldVale = OldVale *-1
            oldSign = -1
        elif OldVale > 0 :
            oldSign = 1
        elif OldVale == 0 :
            oldSign = 0
         
    except Archive.DoesNotExist:
        oldSign = 0
        OldVale = 0

    studentaff = StudentAff.objects.get(code=request.user.code)
    if studentaff.grade not in ('الاول الابتدائى','الاول الاعدادى','الاول الثانوى') and studentaff.contact_status == False:
        request.session['error'] ='برجاء تحديث بيانات التواصل'
        return redirect('contact')
    else:
        student=request.user
        if len(str(request.user.living_area)) > 4 :
            bus = True
        else :
            bus = False
        msg = request.session.get('msg')
        error = request.session.get('error')
        request.session['msg'] = ''
        request.session['error'] = ''
        context = {
            'bus':bus,
            'msg':msg,
            'error':error,
            'oldSign':oldSign,
            'OldVale':OldVale,
        }
        return render(request, 'fees/dashboard.html',context)

def addfees(request):
    if request.method == 'GET':   
        msg = request.session.get('msg')
        return render(request, 'fees/addfees.html', {'form':FeesForm(),'msg':msg})     
    else:
        try:
            LYFee = Archive.objects.get(code=request.user.code,study_year=last_year).year_status()
            LYFee=int(LYFee)
            if LYFee < 0 :
                LYFee = LYFee *-1
            else:
                LYFee = 0
          
        except Archive.DoesNotExist:
            LYFee = 0

        if request.user.can_pay == True:
            if request.POST['kind'] == "دراسية":
                # add try: except to solve value Error
                try:
                    form = FeesForm(request.POST)
                    newfee = form.save(commit=False)
                    newfee.student = request.user
                    newfee.school = request.user.school

                    SYear=request.user.year
                    if LYFee >0:
                        if int(request.POST['value']) <= LYFee:
                            newfee.year = last_year
                            newfee.save()
                        else:
                            newfee.value = LYFee
                            newfee.year = last_year
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
                        # if LYFee >0:
                        #     if int(request.POST['value']) <= LYFee:
                        #         newfee.year = '22-21'
                        #         newfee.save()
                        #     else:
                        #         newfee.value = LYFee
                        #         newfee.year ='22-21'
                        #         newfee.save()
                        #         form2 = FeesForm(request.POST)
                        #         newfee2 = form2.save(commit=False)
                        #         newfee2.student = request.user
                        #         newfee2.school = request.user.school
                        #         newfee2.value = int(request.POST['value']) - LYFee
                        #         newfee2.year = SYear
                        #         newfee2.save()
                        # else:        
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
    fees = Fee.objects.filter(student=request.user.id,year=request.user.year,kind__in = ('دراسية','سيارة',)).exclude(school__in=('Out-b', 'Out-g')).order_by('payment_date')
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
