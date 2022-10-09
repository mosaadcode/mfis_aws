from django.shortcuts import render,redirect
from .models import Student,Contact
from .forms import ContactData,ContactContact

def contact(request):
        if request.method == 'GET':
            msg = request.session.get('msg')
            request.session['msg'] = ''
            error = request.session.get('error')
            request.session['error'] = ''

            student = Student.objects.get(code=request.user.code)
            try:
                contact = Contact.objects.get(student=student)
                context = {
                'msg':msg,
                'error':error,
                'form':ContactContact(instance=contact),
                 }
            except Contact.DoesNotExist:
                context = {
                    'msg':msg,
                    'error':error,
                    'form':ContactData(instance=student),
                }
            return render(request, 'student_affairs/contact.html',context)

        else:
            try:
                student = Student.objects.get(code=request.user.code)
                if student.father_mobile != request.POST['father_mobile'] or student.mother_mobile != request.POST['mother_mobile'] :
                    phone_update = True
                else:
                    phone_update = False
                if student.address_1 != request.POST['address']:
                    address_update = True
                else:
                    address_update = False
                try:
                    contact = Contact.objects.get(student=student)
                    contact.father_mobile = request.POST['father_mobile']
                    contact.mother_mobile = request.POST['mother_mobile']
                    contact.phone_number = request.POST['phone_number']
                    contact.email = request.POST['email']
                    contact.address_1 = request.POST['address']
                    contact.phone_update = phone_update
                    contact.address_update = address_update
                    contact.save()
                except Contact.DoesNotExist:
                    contact = Contact(
                        student=student,
                        father_mobile = request.POST['father_mobile'],
                        mother_mobile = request.POST['mother_mobile'],
                        phone_number = request.POST['phone_number'],
                        email = request.POST['email'],
                        address_1 = request.POST['address'],
                        school = request.user.school,
                        phone_update = phone_update,
                        address_update = address_update,
                    )
                    contact.save()
                student.contact_status = True
                student.save()
                request.session['msg'] = 'تم استلام البيانات وسيتم التعديل بعد المراجعة'
                return redirect('dashboard')
            except ValueError:
                    request.session['error'] = 'برجاء إدخال البيانات بشكل صحيح'
                    return redirect('contact')
