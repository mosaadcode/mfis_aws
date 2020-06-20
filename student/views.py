from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# from fees.models import Fees
from django.db.models import Sum
from .forms import StudentProfile

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'student/home.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, code=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'student/home.html', {'form':AuthenticationForm, 'error':'برجاء التأكد من الكود وكلمة المرور'})
        else:
            login(request, user)
            if user.father_mobile == "":
                return redirect('profile')
            else:
                return redirect('dashboard')

# def home(request):
#     return render(request, 'student/home.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def profile(request):
        if request.method == 'GET':
            if request.user.father_mobile == "":
                return render(request, 'student/profile.html', {'form':StudentProfile(), 'error':'برجاء تحديث بيانات التواصل'})
            else:
                return render(request, 'student/profile.html', {'form':StudentProfile()})

        else:
            # add try: except to solve value Error
            try:
                # get the information from the post request and connect it with our form
                # form = StudentProfile(request.POST)
                # Create newtodo but dont't save it yet to the database
                # profile = form.save(commit=False)
                # set the user to newtodo
                # profile.student = request.user
                # newfee.grade = request.user.grade
                # newfee.school = request.user.school
                # save newtodo
                # newfee.save()
                # update student data
                request.user.father_mobile = request.POST['father_mobile']
                request.user.mother_mobile = request.POST['mother_mobile']
                request.user.phone_number = request.POST['phone_number']
                request.user.email = request.POST['email']
                request.user.save(update_fields=["father_mobile", "mother_mobile", "phone_number", "email"])
                # redirect user to currenttodos page
                return redirect('dashboard')
            except ValueError:
                    # tell user when error hapen
                    return render(request, 'student/profile.html', {'form':StudentProfile(),'error':'برجاء مراجعة البيانات'})
