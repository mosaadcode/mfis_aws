from django.forms import ModelForm
from django import forms
from .models import Student



class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['old_bus', 'living_area','address']

#
class StudentProfile(ModelForm):
    class Meta:
        model = Student
        fields = ['father_mobile', 'mother_mobile', 'phone_number', 'email']
#
class StudentArea(ModelForm):
    class Meta:
        model = Student
        fields = ['old_bus', 'living_area', 'address']
