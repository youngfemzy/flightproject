
# import django forms 
from django import forms


# import all models in our models.py
from .models import *



from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from django.contrib.auth.models import User


    
class checkoutForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'country', 'state']




class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget= TextInput)
    password = forms.CharField(widget= PasswordInput)


    
class customerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'country', 'state']
