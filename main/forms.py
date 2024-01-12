from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from .models import Inventor
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

class InventorForm(forms.ModelForm):
    class Meta:
        model = Inventor
        fields= "__all__"
        exclude = ["user"]
    
