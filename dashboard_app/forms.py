from django import forms
from .models import CustomUser  # หรือโมเดลที่มีอยู่จริง


class elec(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'num_of_products': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("seller", "Seller"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Register as")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]
