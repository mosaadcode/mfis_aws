from django.forms import ModelForm
from django import forms
from .models import Employee,Permission,Vacation

class DateInput(forms.DateInput):
    input_type = 'date'

class EmployeeContact(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('mobile_number','phone_number','emergency_phone','email')

class PermForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('date','type','reason','start_time','end_time')
        start_time = forms.TimeInput(format='%H:%M'),
        end_time = forms.TimeInput(format='%H:%M'),
        # exclude = ('date','type')

    date = forms.DateField(widget=DateInput,)

class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ('date_from','date_to','type','reason')
        # exclude = ('date','type')

    date_from = forms.DateField(widget=DateInput,)
    date_to = forms.DateField(widget=DateInput,)