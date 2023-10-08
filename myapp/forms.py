
from django import forms
from .models import Customer

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
