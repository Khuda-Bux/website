from django import forms
from .models import Customer,Cart
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class Registrationform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'        


class My_Cart(forms.ModelForm):
    class Meta:
        model = Cart
        fields=['id','quantity','product']

class MyCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
        exclude=['id','user','state']
        widgets = {
            'user': forms.HiddenInput(),# Hide the user field in the form
            # 'name':forms.TextInput(attrs={'class': 'form-control'}),
            # 'locality':forms.TextInput(attrs={'class': 'form-control'}),
            # 'city':forms.TextInput(attrs={'class': 'form-control'}),
            # 'zipcode':forms.IntegerField(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'        
