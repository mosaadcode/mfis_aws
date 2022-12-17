from django.shortcuts import render,redirect
from .models import Employee,SalaryItem,Month,Permission,Vacation
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
    context = {
       'emp':Employee.objects.get(code=request.user.code),
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
    if request.method == 'GET':
        msg = request.session.get('msg')
        request.session['msg'] = ''
        error = request.session.get('error')
        request.session['error'] = ''
        context = {
            'form':PermForm(),
            'msg':msg,
            'error':error,
            'month':active_month,
            'month_start':month_start,
            'month_end':month_end,
            'perms':Permission.objects.filter(employee__code=request.user.code,month=active_month).order_by('-date'),
        }        
        return render( request, "human_resources/perm.html", context)
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            employee = Employee.objects.get(code=request.user.code)
            data = json.loads(request.body)
            type = data ['type']
            if type == 'صباحي':
                start_time = employee.time_in
                end_time = employee.time_in_perm
            elif type == 'مسائي':
                start_time = employee.time_out_perm
                end_time = employee.time_out
            return JsonResponse({'start_time':start_time,'end_time': end_time })
        else:
            if active_month != None:
                if datetime.strptime((request.POST['date']), '%Y-%m-%d').date()< month_start or datetime.strptime((request.POST['date']), '%Y-%m-%d').date() > month_end:
                    request.session['error'] = 'يرجى تحديد تاريخ إذن صحيح'
                    return redirect('perm')
                else:
                    form = PermForm(request.POST)
                    permission = form.save(commit=False)
                    permission.employee = Employee.objects.get(code=request.user.code)
                    permission.school = request.user.school
                    permission.month=active_month
                    permission.save()
                    if Permission.objects.filter(employee__code=request.user.code,month=active_month,ok2=True).count() >= active_month.perms:
                        request.session['msg'] = ' ( تم تسجيل الإذن زائد ( سيتم الخصم من الراتب'
                    else:
                        request.session['msg'] = '( تم تسجيل الإذن ( قيد الموافقة'
                    return redirect('perm')
            else:
                request.session['error'] = 'لا توجد شهور مفعلة'
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