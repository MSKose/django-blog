from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# creating a form to add some more fields to django's default registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # required is True by default

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']