from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import *
from .models import Inventor
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == "POST" :
        form = UserCreationForm(request.POST)
        if form.is_valid():
          user = form.save()
          Inventor.objects.create(user=user,name=user.username,email= user.email)
          return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {'form':form}
    return render(request,'main/register.html',context)
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid username or password')
    return render(request,'main/login.html',{})
@login_required
def logoutPage(request):
    logout(request)
    return redirect("login")
def home(request):
    return render(request,'main/home.html')
@login_required
def setting(request):
    user = request.user.inventor
    form = InventorForm(instance=user)
    if (request.method == "POST"):
        form = InventorForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.info(request,"Your Profile is Updated")
    context={'form':form}
    return render(request,'main/settings.html',context)
@login_required
def manuscriptFormPage(request):
    inventor = Inventor.objects.filter(user=request.user).first()
    if request.method == "POST":
        form =ManscriptForm(request.POST)
        if form.is_valid():
            mansucript=form.save(commit=False)
            mansucript.inventor=inventor
            mansucript.save()
            return redirect("home")
    else:
        form = ManscriptForm()
    context ={'form':form}
    return render(request,"main/manuscript.html",context)
@login_required
def LanguageFormPage(request):
    if request.method == "POST":
        form = Language(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manuscriptform')
    else:
        form = Language()
    context ={'form':form}
    return render(request,"main/language.html",context)
@login_required
def GenerFormPage(request):
    if request.method == "POST":
        form = GenerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manuscriptform')
    else:
        form = GenerForm()
    context ={'form':form}
    return render(request,"main/gener.html",context)
@login_required
def RepositoryFormPage(request):
    form = RepositoryForm()
    context ={'form':form}
    return render(request,"main/repository.html",context)
@login_required
def RepositoryLocationFormPage(request):
    form = RepositoryLocationForm()
    context ={'form':form}
    return render (request,"main/repositoryLocation.html",context)
@login_required
def RepositoryOwnerFormpage(request):
    form = RepositoryOwnerForm()
    context = {'form':form}
    return render(request,"main/repositoryOwner.html",context)

def home(request):
    manuscripts = Manuscript.objects.all()
    context = {'manuscripts':manuscripts}
    return render(request,"main/home.html",context)

def detail(request,pk):
    print(pk)
    return render (request,'main/detail.html')