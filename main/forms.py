from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from .models import *
from django.forms import widgets
class UserCreationForm(UserCreationForm):
    # role = forms.CharField()
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2","role"]
        widgets = {
            'roles':forms.Select(choices=User.role,attrs={'empty_label': 'Select a genre'})
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['roles'].empty_label = "Select genre"
class InventorForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ["username","first_name","email","last_name"]

class IdForm(forms.ModelForm):
    class Meta:
        model = Classfication
        fields = ["name"]     
class SelectWithPlaceholder(widgets.Select):
    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs=attrs, **kwargs)
        self.attrs['placeholder'] = kwargs.pop('placeholder', 'Select a genre')
  
class ManscriptForm(forms.ModelForm):
    # mansuscript_name = forms.CharField(label="Name:", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    class Meta:
        model = Manuscript
        fields ="__all__"
        exclude = ["inventor","index"]
        widgets ={
            'language': forms.SelectMultiple(attrs={'class':' form-control'}),
             'genere' : forms.SelectMultiple(attrs={'class':'form-control multiselect'}),
        }
    def __init__(self,*args, **kwargs):
        super(ManscriptForm,self).__init__(*args,**kwargs)
        # self.fields['genere'].empty_label = "select gener"
        # self.fields['repository'].empty_label = "Repository"
        # self.fields['uid'].empty_label = "select code"
        self.fields['repositoryLocation'].empty_label = "select location"
        

    #     widgets = {
    #         'genere':  forms.Select(choices=Genre.objects.all(),attrs={'empty_label': 'Select a genre'}),
    #         'language':  forms.Select(choices=Language.objects.all(),attrs={'empty_label': 'Select a language'}),
    #         'repository':  forms.Select(choices=Repository.objects.all(),attrs={'empty_label': 'Select a repository'}),
    #         'repositoryOwner':  forms.Select(choices=RepositoryOwner.objects.all(),attrs={'empty_label': 'Select a owner'}),
    #         'repositoryLocation':  forms.Select(choices=RepositoryLocation.objects.all(),attrs={'empty_label': 'Select a location'}),
    #         'uid':  forms.Select(choices=Classfication.objects.all(),attrs={'empty_label': 'Select a location'}),

    #     }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['genere'].empty_label = "Select genre"
    #     self.fields['language'].empty_label = "Select language"
    #     self.fields['repository'].empty_label = "Select repository"
    #     self.fields['repositoryOwner'].empty_label = "Select repository owner"
    #     self.fields['repositoryLocation'].empty_label = "Select repository location"
    #     self.fields['uid'].empty_label = "select id prefix"

class RepositoryOwnerForm(forms.ModelForm):
    class Meta:
        model = RepositoryOwner
        fields = "__all__"
        exclude = ["inventor","index"]

class RepositoryLocationForm(forms.ModelForm):
    class Meta:
        model = RepositoryLocation
        fields="__all__"
        exclude = ["inventor"]
class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = "__all__"
        exclude = ["inventor","index"]
class GenerForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields="__all__"
        exclude = ["inventor"] 
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields="__all__" 
        exclude = ["inventor"]

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']
              