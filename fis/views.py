from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# from fees.models import Fees
from django.db.models import Sum
# from .forms import StudentProfile
from human_resources.models import Employee
from student_affairs.models import Student as StudentAff
from django.http import JsonResponse
import json

def fis_loginuser(request):
    if request.method == 'GET':
        return render(request, 'fis/home2.html', {'form':AuthenticationForm})
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            na_id = data ['na_id']
            try:
                employee = Employee.objects.get(na_id=na_id)
                code = employee.code
            except Employee.DoesNotExist:
                 code = 0

            return JsonResponse({'code':code,})
        else:
            user = authenticate(request, code=request.POST['username'],password=request.POST['password'])
            if user is None:
                return render(request, 'fis/home2.html', {'form':AuthenticationForm, 'error':'برجاء التأكد من الكود وكلمة المرور'})
            else:
                login(request, user)
                if user.is_employ == False:
                    studentaff = StudentAff.objects.get(code=request.user.code)        
                    if studentaff.grade in ('الاول الابتدائى','الاول الاعدادى','الاول الثانوى'):
                        if studentaff.document_status == False:
                            logout(request)
                            return render(request, 'fis/home2.html', {'form':AuthenticationForm, 'error':'لا يمكن تسجيل المصروفات قبل إستيفاء كامل الأوراق المطلوبة, برجاء التواصل مع المدرسة'})
                        else:
                            if studentaff.application_status == False:
                                request.session['error'] ='برجاء تحديث البيانات التالية'
                                return redirect('application')
                            else:
                                return redirect('dashboard')
                    return redirect('dashboard')
                return redirect('home2')
