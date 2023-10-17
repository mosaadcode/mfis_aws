from django.shortcuts import render,redirect,get_object_or_404
from .models import Employee,SalaryItem,Month,Permission,Vacation,Employee_month,Time_setting
from .forms import PermForm,VacationForm,EmployeeContact
from datetime import datetime,date
from django.http import JsonResponse
import json

try:
    published_month = Month.objects.get(published=True)
    pub_month = published_month.code[5:]
    pub_year = published_month.code[:4]
except Month.DoesNotExist:
    published_month = None
try:
    active_month = Month.objects.get(active=True)
    if int(active_month.code[5:])==1:
        month_start = date(int(active_month.code[:4])-1,12,16)
    else:
        month_start = date(int(active_month.code[:4]),int(active_month.code[5:])-1,16)
    month_end = date(int(active_month.code[:4]),int(active_month.code[5:]),15)
except Month.DoesNotExist:
    active_month = None

def home(request):
    msg = request.session.get('msg')
    request.session['msg'] = ''
    error = request.session.get('error')
    request.session['error'] = ''
    emp = Employee.objects.get(code=request.user.code)
    context = {
       'emp':emp,
       'msg':msg,
       'error':error,
    }
    return render(request, 'human_resources/home.html',context)

def salary(request):
    if published_month != None:
        context = {
        'month':pub_month,
        'year':pub_year,
        'items':SalaryItem.objects.filter(employee__code=request.user.code,month=published_month).order_by('-value'),
        }
    else:
        context = {}
    return render(request, 'human_resources/salary.html',context)

def perm(request):
    try:
        employee_month = Employee_month.objects.get(employee__code=request.user.code,month=active_month)
    except Employee_month.DoesNotExist:
        request.session['error'] = 'لم يتم العثور على السجل الشهري برجاء التواصل مع قسم شؤون العاملين'
        return redirect('home2')
    month_perms= Permission.objects.filter(employee__code=request.user.code,month=active_month).order_by('-created')
    employee = Employee.objects.get(code=request.user.code)
    settings = employee.perms
    times = employee.times
    if settings is None or times is None:
        request.session['error'] = 'إعدادات اَذون غير صحيحة برجاء التواصل مع قسم شؤون العاملين'
        return redirect('home2')       
    total = settings.perms
    used = month_perms.count()
    unused = total - used
    used_perms_percentage = (used / total) * 100
    unused_perms_percentage = 100 - used_perms_percentage
    over = employee_month.permissions - total

    # Check if there are any month_perms with ok2=False
    OpenPerm = month_perms.filter(ok2=False).exists()

    if request.method == 'GET':
        msg = request.session.get('msg')
        request.session['msg'] = ''
        error = request.session.get('error')
        request.session['error'] = ''
        if settings.is_perms == False:
            request.session['error'] = 'ليس لك الحق في إستخدام الاَذون'
            return redirect('home2')
        else:

            context = {
                'form':PermForm(),
                'msg':msg,
                'error':error,
                'settings':settings,
                'month':active_month,
                'month_start':month_start,
                'month_end':month_end,
                'month_perms':month_perms,
                'total':total,
                'used':used,
                'unused':unused,
                'used_perms_percentage' : used_perms_percentage,
                'unused_perms_percentage' :unused_perms_percentage,
                'over':over,  
                'OpenPerm' :OpenPerm,
            }
            return render( request, "human_resources/perm.html", context)

    else:       
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # employee = Employee.objects.get(code=request.user.code)
            data = json.loads(request.body)
            type = data ['type']
            date = data['date']
            work_time = Time_setting.objects.get(month=active_month,date=date,name=times)
            if type == 'صباحي':
                start_time = work_time.time_in
                end_time = work_time.time_in_perm
            elif type == 'مسائي':
                start_time = work_time.time_out_perm
                end_time = work_time.time_out
            return JsonResponse({'start_time':start_time,'end_time': end_time })
        else:
            if active_month != None:
                unused_perms = request.POST.get('unused_perms')
                if used < total :
                    form = PermForm(request.POST)
                    if form.is_valid():
                        permission = form.save(commit=False)
                        permission.employee = Employee.objects.get(code=request.user.code)
                        permission.school = request.user.school
                        permission.month=active_month
                        permission.count=employee_month.permissions+1
                        permission.total=settings.perms
                        permission.job_code=employee.job_code
                        permission.save()
                        request.session['msg'] = '( تم تسجيل الإذن ( قيد الموافقة'
                        return redirect('perm')
                    else:
                        request.session['error'] = 'حدث خطأ , رجاء إعادة المحاولة'
                        return redirect('perm')
                else:
                    if settings.is_over == False:
                        request.session['error'] = 'تم استخدام جميع اَذون هذا الشهر وغير مسموح بالتجاوز'
                        return redirect('perm')
                    else:
                        form = PermForm(request.POST)
                        permission = form.save(commit=False)
                        permission.employee = Employee.objects.get(code=request.user.code)
                        permission.school = request.user.school
                        permission.month=active_month
                        permission.count=employee_month.permissions+1
                        permission.total=settings.perms
                        permission.job_code=employee.job_code
                        permission.save()
                        request.session['msg'] = ' ( تم تسجيل الإذن زائد ( سيتم الخصم من الراتب'
                        return redirect('perm')
            else:
                request.session['error'] = 'لا توجد شهور مفعلة'
                return redirect('perm')


def delete_permission(request, permission_id):
    try:
        permission = get_object_or_404(Permission, id=permission_id)    
        # Check if both ok1 and ok2 are False
        if  not permission.ok2:
            permission.delete()
    except:
        pass
    
    return redirect('perm')




def vacation(request):
    if request.method == 'GET':
        msg = request.session.get('msg')
        request.session['msg'] = ''
        error = request.session.get('error')
        request.session['error'] = ''
        context = {
            'form':VacationForm(),
            'msg':msg,
            'error':error,
            'vacations':Vacation.objects.filter(employee__code=request.user.code).order_by('-date_from'),
        }        
        return render( request, "human_resources/vacation.html", context)
    else:
        form = VacationForm(request.POST)
        vacation = form.save(commit=False)
        vacation.employee = Employee.objects.get(code=request.user.code)
        vacation.school = request.user.school
        vacation.month = active_month
        vacation.save()

        request.session['msg'] = '( تم تسجيل الإجازة ( قيد الموافقة'
        return redirect('vacation')


def employee_contact(request):
        if request.method == 'GET':
            msg = request.session.get('msg')
            request.session['msg'] = ''
            error = request.session.get('error')
            request.session['error'] = ''

            employee = Employee.objects.get(code=request.user.code)
            context = {
                'msg':msg,
                'error':error,
                'form':EmployeeContact(instance=employee),
                }
            return render(request, 'human_resources/employee_contact.html',context)
        else:
            try:
                employee = Employee.objects.get(code=request.user.code)
                try:
                    employee.mobile_number = request.POST['mobile_number']
                    employee.phone_number = request.POST['phone_number']
                    employee.emergency_phone = request.POST['emergency_phone']
                    employee.email = request.POST['email']
                    employee.save()


                    request.session['msg'] = 'تم تعديل البيانات بنجاح'
                    return redirect('employee_contact')
                except Employee.DoesNotExist:
                    request.session['error'] = 'برجاء إدخال البيانات بشكل صحيح'
                    return redirect('employee_contact')
            except ValueError:
                    request.session['error'] = 'لا يمكن تعديل البيانات الاّن'
                    return redirect('employee_contact')