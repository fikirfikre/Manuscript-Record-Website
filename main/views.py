from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

from main.decorators import allowed_users, onlyAdmin
from .forms import *
from .models import User,Reader,User
from .filter import ManuscriptFilter
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError

# Create your views here.
def register(request):
    if request.method == "POST" :
        
        form = UserCreationForm(request.POST)
    
        if form.is_valid():
            user_data = form.cleaned_data
            selectedRole = user_data['role']
            print(selectedRole)
            user = User.objects.create_user(
                username=user_data['username'],
                first_name = user_data['first_name'],
                last_name = user_data['last_name'],
                email = user_data['email'],
                password = user_data['password1'],
                role = selectedRole
            )
            user.save()
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
            return redirect('view')
        else:
            messages.info(request,'Invalid username or password')
    return render(request,'main/login.html',{})

@login_required(login_url="login")
def logoutPage(request):
    logout(request)
    return redirect("login")

# def home(request):
#     return render(request,'main/login.html')

@login_required(login_url="login")
def editProfile(request):
    user = request.user
    form = InventorForm(instance=user)
    if (request.method == "POST"):
        form = InventorForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    context={'form':form}
    return render(request,'main/edit-form.html',context)
def profile(request):
       user = request.user
       context= {'user':user}
       return render(request,'main/user-profile.html',context) 
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def manuscriptFormPage(request):
    inventor = request.user
    print(request.user.role)
    if request.method == "POST":
        form =ManscriptForm(request.POST)
        print(form)
        if form.is_valid():
            mansucript=form.save(commit=False)
            mansucript.inventor=inventor
            print(mansucript)
            mansucript.save()
            return redirect("home")
    else:
        form = ManscriptForm()
    context ={'form':form}
    return render(request,"main/form-manuscript.html",context)

@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def LanguageFormPage(request):
    inventor = request.user
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
    return render(request,"main/form-language.html",context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def GenerFormPage(request):
    inventor = request.user
    print(User.objects.all())
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
    return render(request,"main/form-genre.html",context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def RepositoryFormPage(request):
    inventor = request.user
    form = RepositoryForm()
    context ={'form':form}
    if (request.method == "POST"):
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.inventor = inventor
            repo.save()
            return redirect('repo')
    return render(request,"main/form-repository.html",context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def RepositoryLocationFormPage(request):
    inventor = request.user
    form = RepositoryLocationForm()
    context ={'form':form}
    if (request.method == "POST"):
        form = RepositoryLocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.inventor = inventor
            location.save()
            return redirect('locations')
    return render (request,"main/form-location.html",context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def RepositoryOwnerFormpage(request):
    inventor = request.user
    form = RepositoryOwnerForm()
    context = {'form':form}
    if (request.method == "POST"):
        form = RepositoryOwnerForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.inventor = inventor
            owner.save()
            return redirect('owners')
    return render(request,"main/form-owner.html",context)
@login_required(login_url="login")
def home(request):
    all_manuscripts = Manuscript.objects.all()
    manuscriptFilter = ManuscriptFilter(request.POST,queryset=all_manuscripts)
    manuscripts = []
    
    count = 1
    for key,value in request.POST.items():
        print(key)
        if(key != "csrfmiddlewaretoken"):
            print(value)
            if(value != ''):
                count = count + 1
                manuscripts = manuscriptFilter.qs
                print(manuscripts)
                print(count)
            else:
                if count == 1:
                    manuscripts = []
                

    if (request.POST.get('all_manuscripts')):
         manuscripts = all_manuscripts
    print(manuscripts)
    context = {'manuscripts':manuscripts,"filter":manuscriptFilter}
    return render(request,"main/manuscript-list.html",context)

        #  request.session['selected_checkboxes'] = True
    # elif manuscriptFilter.has_active_filters():
    #     manuscripts = manuscriptFilter.qs
    
    # else:
    #     # manuscripts=[]
    #     request.session.pop('selected_checkboxes', None)
    # stored_checkbox = request.session.get('selected_checkboxes', False)
    
    # if not request.GET.get('all_manuscripts') or  request.GET:
    #     manuscripts = []



@login_required(login_url="login")
def detail(request,pk):

    manuscript = Manuscript.objects.get(id=pk)
    context={"manuscript":manuscript}
    return render (request,'main/manuscript-detail.html',context)

@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def edit(request,pk):
    manuscript = Manuscript.objects.get(id=pk)
    if(manuscript.inventor != request.user and request.user.role != "ADMIN" ):
        return render(request,'main/notAllowed.html')
    form= ManscriptForm(instance=manuscript)
    if (request.method == "POST"):
        form = ManscriptForm(request.POST,instance=manuscript)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {"form":form,'title':'Manuscript'}
    return render(request,'main/edit-manuscript.html',context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def delete(request,pk):
    manuscript = Manuscript.objects.get(id=pk)
    if(manuscript.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            manuscript.delete()
            return redirect('home')
        except ProtectedError:
            return redirect('main/notAllowed.html')
    return render(request,'main/delete.html',{"name":manuscript.mansucript_name,"return_url":"home"})
@login_required(login_url="login")
def repositoryList(request):

    repositories = Repository.objects.all()
    context = {'objects' : repositories,'title':'Repositories','deleteUrl':"deleteRepo","editUrl":"editRepo"}
    return render(request,'main/object-list.html',context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def deleteRepo(request,pk):
    reposiotry = Repository.objects.get(id=pk)
    if(reposiotry.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            reposiotry.delete()
            return redirect('repo')
        except ProtectedError:
            return redirect('notAllowed')
        
    return render(request,'main/delete.html',{"name":reposiotry.name,"return_url":"repo"})
@login_required(login_url="login")
def genreList(request):
    genres = Genre.objects.all()
    context = {'objects':genres,'title':"Genres",'deleteUrl':"deleteGenre","editUrl":"editGener"}
    return render(request,'main/object-list.html',context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def deleteGenre(request,pk):
    genre = Genre.objects.get(id=pk)

    if(genre.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            genre.delete()
            return redirect('genres')
        except ProtectedError:
            return redirect('notAllowed')
    return render(request,'main/delete.html',{"name":genre.name,"return_url":"genres"})
@login_required(login_url="login")

def OwnerList(request):
    owners = RepositoryOwner.objects.all()
    context = {'objects':owners,'title':"Owners",'deleteUrl':"deleteOwner","editUrl":"editOwner"}
    return render(request,'main/object-list.html',context)

@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def deleteOwner(request,pk):
    owners = RepositoryOwner.objects.get(id=pk)
    if(owners.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            owners.delete()
            return redirect('owners')
        except ProtectedError:
            return redirect('notAllowed')
    return render(request,'main/delete.html',{"name":owners.name,"return_url":"owners"})
@login_required(login_url="login")

def LocationList(request):
    locations = RepositoryLocation.objects.all()
    context = {'objects':locations,'title':"Locations",'deleteUrl':"deleteLocation","editUrl":"editLocation"}
    return render(request,'main/object-list.html',context)

@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def deleteLocation(request,pk):
    location = RepositoryLocation.objects.get(id=pk)

    if(location.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            location.delete()
            return redirect('locations')
        except ProtectedError:
            return redirect('notAllowed')
    return render(request,'main/delete.html',{"name":location.city,"return_url":"locations"})
@login_required(login_url="login")
def LanguageList(request):  
    languages = Language.objects.all()
    context = {'objects':languages,'title':"Languages",'deleteUrl':"deleteLanguage","editUrl":"editLanguage"}
    return render(request,'main/object-list.html',context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def deleteLanguage(request,pk):
    language = Language.objects.get(id=pk)

    if(language.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    if(request.method == "POST"):
        try:
            language.delete()
            return redirect('languages')
        except ProtectedError:
            return redirect('notAllowed')
    return render(request,'main/delete.html',{"name":language.name,"return_url":"languages"})
@login_required(login_url="login")
def notAllowed(request):
    return render(request,'main/notAllowed.html')
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def editGener(request,pk):
    genre = Genre.objects.get(id=pk)
    if(genre.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    form = GenerForm(instance=genre)
    if request.method == "POST":
        form = GenerForm(request.POST,instance=genre)
        if form.is_valid():
            form.save()
            return redirect("genres")
    context={"form":form,"title":"Genre"}
    return render(request,'main/edit-form.html',context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def editOwner(request,pk):
    owner = RepositoryOwner.objects.get(id=pk)
    if(owner.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    
    form = RepositoryOwnerForm(instance=owner)
    if request.method == "POST":
        form = RepositoryOwnerForm(request.POST,instance=owner)
        if form.is_valid():
            form.save()
            return redirect("owners")
    context={"form":form,"title":"Repository Owner"}
    return render(request,'main/edit-form.html',context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def editLocation(request,pk ):
    location = RepositoryLocation.objects.get(id=pk)
    if(location.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    form = RepositoryLocationForm(instance=location)
    if request.method == "POST":
        form = RepositoryLocationForm(request.POST,instance=location)
        if form.is_valid():
            form.save()
            return redirect("locations")
    context={"form":form,"title":"Repository Location"}
    return render(request,'main/edit-form.html',context)
@login_required
@allowed_users(['INVENTOR'])
def editLanguage(request,pk):
    language = Language.objects.get(id=pk)
    if(language.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    form = LanguageForm(instance=language)
    if request.method == "POST":
        form = LanguageForm(request.POST,instance=language)
        if form.is_valid():
            form.save()
            return redirect("languages")
    context={"form":form,"title":" Language"}
    return render(request,'main/edit-form.html',context)
@login_required(login_url="login")
@allowed_users(['INVENTOR'])
def editRepository(request,pk):
    repository = Repository.objects.get(id=pk)
    if(repository.inventor != request.user and request.user.role != "ADMIN"):
        return render(request,'main/notAllowed.html')
    form = RepositoryForm(instance=repository)
    if request.method == "POST":
        form = RepositoryForm(request.POST,instance=repository)
        if form.is_valid():
            form.save()
            return redirect("repo")
    context={"form":form,"title":"Repository"}
    return render(request,'main/edit-form.html',context)
@login_required(login_url="login")
@onlyAdmin()
def users(request):
    users = User.objects.all()
    page_number = request.GET.get('page',1)
    paginator = Paginator(users,10)
    page_obj = paginator.get_page(page_number)
    context ={'page_obj':page_obj,'paginator':paginator,'page_range':range(1,paginator.num_pages+1)}
    return render(request,'main/users-list.html',context)
def usersEdit(request,pk):
    user = User.objects.get(id=pk)
    form = UserEditForm(request.POST,instance=user)
    if (request.method == 'POST'):
        if form.is_valid():
            user.role = form.cleaned_data['role']
            user.save()
            return  redirect('users')
    context = {'form':form,'user':user,'title':user.username}
    return render(request,'main/edit-form.html',context)
@login_required(login_url="login")
def view(request):
    return render(request,"main/view.html")
@login_required(login_url="login")
@allowed_users()
def entry(request):
    return render(request,"main/entry.html")
@login_required(login_url="login")
def setting(request):
    user = request.user
    context = {'user':user}
    return render(request,'main/profile.html',context)
@login_required(login_url="login")
def statistics(request):
    manuscripts = Manuscript.objects.count()
    locations = RepositoryLocation.objects.count()
    geners = Genre.objects.count()
    owners = RepositoryOwner.objects.count()
    repository = Repository.objects.count()
    language = Language.objects.count()
    context ={
        "manuscripts":manuscripts,
        "locations":locations,
        "genres": geners,
        "owners":owners,
        "repository":repository,
        "languages":language
    }
    return render(request,'main/statistics-list.html',context)