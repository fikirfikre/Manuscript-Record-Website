from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from .models import *
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

class InventorForm(forms.ModelForm):
    class Meta:
        model = Inventor
        fields= "__all__"
        exclude = ["user"]
    
class ManscriptForm(forms.ModelForm):
    class Meta:
        model = Manuscript
        fields = "__all__"
        exclude = ["inventor"]

class RepositoryOwnerForm(forms.ModelForm):
    class Meta:
        model = RepositoryOwner
        fields = "__all__"

class RepositoryLocationForm(forms.ModelForm):
    class Meta:
        model = RepositoryLocation
        fields="__all__"
class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = "__all__"
class GenerForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields="__all__" 
class Language(forms.ModelForm):
    class Meta:
        model = Language
        fields="__all__" 
              
