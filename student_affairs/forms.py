from django.forms import ModelForm
from .models import Student,Contact

class ContactData(ModelForm):
    class Meta:
        model = Student
        fields = ['father_mobile', 'mother_mobile', 'phone_number', 'email','address_1']

class ContactContact(ModelForm):
    class Meta:
        model = Contact
        fields = ['father_mobile', 'mother_mobile', 'phone_number', 'email','address_1']