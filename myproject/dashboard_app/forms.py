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
    email = forms.EmailField(required=True)  # ✅ ไม่ต้องมี role

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = "user"  # ✅ กำหนดค่า role อัตโนมัติเป็น "user"
        if commit:
            user.save()
        return user
