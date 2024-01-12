from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import UserCreationForm, InventorForm
from .models import Inventor

# Create your views here.
def register(request):
    if request.method == "POST" :
        form = UserCreationForm(request.POST)
        if form.is_valid():
          user =   form.save()
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

def home(request):
    return render(request,'main/home.html')

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