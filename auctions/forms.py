from django import forms
from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Products

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CreateNewProduct(ModelForm): 
    class Meta: 
        model = Products
        fields = ["title", "description", "initial_offer", "img_url", "category"]