from django.db import models
from django.contrib.auth.models import Permission, Group,AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        READER = "READER", "reader"
        INVENTOR= "INVENTOR", "inventor"
        ADMIN="ADMIN","admin"
    base_role = Role.READER
    role = models.CharField(max_length=10,choices = Role.choices,default=base_role)

    
class Reader(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="reader")
    name = models.CharField(max_length=150)
    address =models.CharField( max_length=50)
    email = models.EmailField( max_length=254) 
    def __str__(self):
        return self.name 
class Genre(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank=True, null=True)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
class RepositoryOwner(models.Model):
    name = models.CharField(max_length = 255)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class RepositoryLocation(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.city
    
class Repository(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank=True, null=True)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.name



    
class Language(models.Model):
    name = models.CharField(max_length=100,unique=True)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
    

   
class Manuscript(models.Model):

    mansucript_name = models.CharField(max_length = 100,blank=False,null=False)
    repository = models.ForeignKey(Repository,on_delete = models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    genere = models.ForeignKey(Genre, on_delete=models.PROTECT)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    repositoryOwner = models.ForeignKey(RepositoryOwner,on_delete=models.PROTECT)
    repositoryLocation = models.ForeignKey(RepositoryLocation,on_delete = models.PROTECT)
    shelf_mark = models.CharField(max_length=50,null=False,blank=False)
    resp_statement = models.CharField( max_length=50,null=False,blank=False)
    inventory_date = models.DateField(auto_now_add=True,null=False,blank=False)
    measurement =models.CharField(max_length=50,null=False,blank=False)
    follos_number = models.IntegerField(null=False,blank=False)
    binding = models.CharField(max_length=100,null=False,blank=False)
    main_content = models.CharField(null=False,blank=False,max_length=500)
    dating = models.CharField(max_length=50,null=False,blank=False)
    other_provenance = models.CharField(max_length=50,blank=True, null=True)
    scripe = models.CharField(max_length=50,blank=True, null=True)
    no_of_cols = models.IntegerField(null=False,blank=False )
    notes_cur_use = models.TextField(blank=True, null=True)    
    no_of_lines = models.IntegerField(null=False,blank=False)
    decoration = models.CharField(max_length=255,null=False,blank=False)
    colophones = models.CharField( max_length=50,null=False,blank=False)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.mansucript_name
    
    