from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=256, required=True)
    email = forms.CharField(max_length=256, required=True)
    password = forms.CharField(max_length=256)
    confirm_password = forms.CharField(max_length=256, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
