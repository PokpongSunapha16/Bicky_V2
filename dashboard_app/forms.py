from django import forms
from . models import dash

class elec(forms.ModelForm):
    class Meta:
        model = dash
        fields = '__all__'
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'num_of_products': forms.TextInput(attrs={'class': 'form-control'}),
        }