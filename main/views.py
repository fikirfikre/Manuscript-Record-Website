from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import *
from .models import Inventor
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError

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
    return redirect("home")
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
    inventor = Inventor.objects.filter(user =request.user).first()
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            language= form.save(commit=False)
            language.inventor = inventor
            language.save()
            return redirect('languages')
    else:
        form = LanguageForm()
    context ={'form':form}
    return render(request,"main/language.html",context)
@login_required
def GenerFormPage(request):
    inventor = Inventor.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = GenerForm(request.POST)
        if form.is_valid():
            genre = form.save(commit=False)
            genre.inventor = inventor
            genre.save()
            return redirect('genres')
    else:
        form = GenerForm()
    context ={'form':form}
    return render(request,"main/gener.html",context)
@login_required
def RepositoryFormPage(request):
    inventor = Inventor.objects.filter(user =request.user).first()
    form = RepositoryForm()
    context ={'form':form}
    if (request.method == "POST"):
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.inventor = inventor
            repo.save()
            return redirect('repo')
    return render(request,"main/repository.html",context)
@login_required
def RepositoryLocationFormPage(request):
    inventor = Inventor.objects.filter(user =request.user).first()
    form = RepositoryLocationForm()
    context ={'form':form}
    if (request.method == "POST"):
        form = RepositoryLocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.inventor = inventor
            location.save()
            return redirect('locations')
    return render (request,"main/repositoryLocation.html",context)
@login_required
def RepositoryOwnerFormpage(request):
    inventor = Inventor.objects.filter(user =request.user).first()
    form = RepositoryOwnerForm()
    context = {'form':form}
    if (request.method == "POST"):
        form = RepositoryOwnerForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.inventor = inventor
            owner.save()
            return redirect('owners')
    return render(request,"main/repositoryOwner.html",context)

def home(request):
    manuscripts = Manuscript.objects.all()
    paginator = Paginator(manuscripts,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context = {'manuscripts':manuscripts,'page_obj':page_obj}
    return render(request,"main/home.html",context)

def detail(request,pk):
    inventor = ""
    if request.user.is_authenticated:
        inventor = Inventor.objects.filter(user=request.user).first()
    manuscript = Manuscript.objects.get(id=pk)
    context={"manuscript":manuscript,"inventor":inventor}
    return render (request,'main/detail.html',context)

@login_required
def edit(request,pk):
    manuscript = Manuscript.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(manuscript.inventor != inventor):
        return render(request,'main/notAllowed.html')
    form= ManscriptForm(instance=manuscript)
    if (request.method == "POST"):
        form = ManscriptForm(request.POST,instance=manuscript)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {"form":form,'title':'Manuscript'}
    return render(request,'main/edit.html',context)
@login_required
def delete(request,pk):
    manuscript = Manuscript.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(manuscript.inventor != inventor):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            manuscript.delete()
            return redirect('home')
        except ProtectedError:
            return redirect('main/notAllowed.html')
    return render(request,'main/delete.html',{"name":manuscript.mansucript_name})
@login_required
def repositoryList(request):
    inventor = ""
    if request.user.is_authenticated:
        inventor = Inventor.objects.filter(user=request.user).first()
    repositories = Repository.objects.all()
    context = {'objects' : repositories,'title':'Repositories','deleteUrl':"deleteRepo","editUrl":"editRepo","inventor":inventor}
    return render(request,'main/object_list.html',context)
@login_required
def deleteRepo(request,pk):
    reposiotry = Repository.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(reposiotry.inventor != inventor):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            reposiotry.delete()
            return redirect('repo')
        except ProtectedError:
            return redirect('notAllowed')
        
    return render(request,'main/delete.html',{"name":reposiotry.name})
@login_required
def genreList(request):
    inventor = ""
    if request.user.is_authenticated:
        inventor = Inventor.objects.filter(user=request.user).first()
    genres = Genre.objects.all()
    context = {'objects':genres,'title':"Genres",'deleteUrl':"deleteGenre","editUrl":"editGener","inventor":inventor}
    return render(request,'main/object_list.html',context)
@login_required
def deleteGenre(request,pk):
    genre = Genre.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(genre.inventor != inventor):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            genre.delete()
            return redirect('genres')
        except ProtectedError:
            return redirect('notAllowed')
    return render(request,'main/delete.html',{"name":genre.name})
@login_required
def OwnerList(request):
    inventor = ""
    if request.user.is_authenticated:
        inventor = Inventor.objects.filter(user=request.user).first()
    owners = RepositoryOwner.objects.all()
    context = {'objects':owners,'title':"Owners",'deleteUrl':"deleteOwner","editUrl":"editOwner","inventor":inventor}
    return render(request,'main/object_list.html',context)
@login_required
def deleteOwner(request,pk):
    owners = RepositoryOwner.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(owners.inventor != inventor):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            owners.delete()
            return redirect('owners')
        except ProtectedError:
            return redirect('notAllowed')
    return render(request,'main/delete.html',{"name":owners.name})
@login_required
def LocationList(request):
    inventor = ""
    if request.user.is_authenticated:
        inventor = Inventor.objects.filter(user=request.user).first()
    locations = RepositoryLocation.objects.all()
    context = {'objects':locations,'title':"Locations",'deleteUrl':"deleteLocation","editUrl":"editLocation","inventor":inventor}
    return render(request,'main/object_list.html',context)
@login_required
def deleteLocation(request,pk):
    location = RepositoryLocation.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(location.inventor != inventor):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            location.delete()
            return redirect('locations')
        except ProtectedError:
            return redirect('notAllowed')
    return render(request,'main/delete.html',{"name":location.city})
@login_required
def LanguageList(request):
    inventor = ""
    if request.user.is_authenticated:
        inventor = Inventor.objects.filter(user=request.user).first()   
    languages = Language.objects.all()
    context = {'objects':languages,'title':"Languages",'deleteUrl':"deleteLanguage","editUrl":"editLanguage","inventor":inventor}
    return render(request,'main/object_list.html',context)
@login_required
def deleteLanguage(request,pk):
    language = Language.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(language.inventor != inventor):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            language.delete()
            return redirect('languages')
        except ProtectedError:
            return redirect('notAllowed.html')
    return render(request,'main/delete.html',{"name":language.name})

def notAllowed(request):
    return render(request,'main/notAllowed.html')
@login_required
def editGener(request,pk):
    inventor = Inventor.objects.filter(user = request.user).first()
    genre = Genre.objects.get(id=pk)
    if(genre.inventor != inventor):
        return render(request,'main/notAllowed.html')
    form = GenerForm(instance=genre)
    if request.method == "POST":
        form = GenerForm(request.POST,instance=genre)
        if form.is_valid():
            form.save()
            return redirect("genres")
    context={"form":form,"title":"Genre"}
    return render(request,'main/edit.html',context)
@login_required
def editOwner(request,pk):
    owner = RepositoryOwner.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(owner.inventor != inventor):
        return render(request,'main/notAllowed.html')
    
    form = RepositoryOwnerForm(instance=owner)
    if request.method == "POST":
        form = RepositoryOwnerForm(request.POST,instance=owner)
        if form.is_valid():
            form.save()
            return redirect("owners")
    context={"form":form,"title":"Repository Owner"}
    return render(request,'main/edit.html',context)
@login_required
def editLocation(request,pk):
    location = RepositoryLocation.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(location.inventor != inventor):
        return render(request,'main/notAllowed.html')
    form = RepositoryLocationForm(instance=location)
    if request.method == "POST":
        form = RepositoryLocationForm(request.POST,instance=location)
        if form.is_valid():
            form.save()
            return redirect("locations")
    context={"form":form,"title":"Repository Location"}
    return render(request,'main/edit.html',context)
@login_required
def editLanguage(request,pk):
    language = Language.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(language.inventor != inventor):
        return render(request,'main/notAllowed.html')
    form = LanguageForm(instance=language)
    if request.method == "POST":
        form = LanguageForm(request.POST,instance=language)
        if form.is_valid():
            form.save()
            return redirect("languages")
    context={"form":form,"title":" Language"}
    return render(request,'main/edit.html',context)
@login_required
def editRepository(request,pk):
    repository = Repository.objects.get(id=pk)
    inventor = Inventor.objects.filter(user = request.user).first()
    if(repository.inventor != inventor):
        return render(request,'main/notAllowed.html')
    form = RepositoryForm(instance=repository)
    if request.method == "POST":
        form = RepositoryForm(request.POST,instance=repository)
        if form.is_valid():
            form.save()
            return redirect("repo")
    context={"form":form,"title":"Repository"}
    return render(request,'main/edit.html',context)