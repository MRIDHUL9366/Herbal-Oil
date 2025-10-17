from django import forms
from django.contrib.auth.models import User
from . models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email','password','first_name')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["__all__"]