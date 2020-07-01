from django import forms
from django.core import validators
from .models import Registration, Login


class RegisterForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ['FirstName', 'LastName', 'Address', 'Email', 'Phone', 'Image']
        widgets = {
            'FirstName': forms.TextInput(attrs={'class': 'form-control'}),
            'LastName': forms.TextInput(attrs={'class': 'form-control'}),
            'Address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 4}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control'}),
            'Image': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'FirstName': 'First Name',
            'LastName': 'Last Name',
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control','type':'password'}),
        }
        labels = {
            'username': 'Username',
            'password': 'Password',
        }

