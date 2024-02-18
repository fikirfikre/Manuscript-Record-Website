from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Inventor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=150)
    address =models.CharField( max_length=50)
    email = models.EmailField( max_length=254)
    def __str__(self):
        return self.name
class RepositoryOwner(models.Model):
    name = models.CharField(max_length = 255)
    inventor = models.ForeignKey(Inventor, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class RepositoryLocation(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    inventor = models.ForeignKey(Inventor, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.city
    
class Repository(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank=True, null=True)
    inventor = models.ForeignKey(Inventor, on_delete=models.PROTECT)
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank=True, null=True)
    inventor = models.ForeignKey(Inventor, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=100)
    inventor = models.ForeignKey(Inventor, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
    

   
class Manuscript(models.Model):
    mansucript_name = models.CharField(max_length = 100)
    shelf_mark = models.CharField(max_length=50)
    resp_statement = models.CharField( max_length=50)
    inventory_date = models.DateField(auto_now_add=True)
    measurement =models.CharField(max_length=50)
    follos_number = models.IntegerField()
    binding = models.CharField(max_length=100)
    main_content = models.TextField()
    dating = models.CharField(max_length=50)
    other_provenance = models.CharField(max_length=50,blank=True, null=True)
    scripe = models.CharField(max_length=50,blank=True, null=True)
    no_of_cols = models.IntegerField(blank=True, null=True)
    notes_cur_use = models.TextField(blank=True, null=True)    
    no_of_lines = models.IntegerField()
    decoration = models.CharField(max_length=255)
    colophones = models.CharField( max_length=50)
    additional_notes = models.TextField()
    repository = models.ForeignKey(Repository,on_delete = models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    genere = models.ForeignKey(Genre, on_delete=models.PROTECT)
    inventor = models.ForeignKey(Inventor, on_delete=models.PROTECT)
    repositoryOwner = models.ForeignKey(RepositoryOwner,on_delete=models.PROTECT)
    repositoryLocation = models.ForeignKey(RepositoryLocation,on_delete = models.PROTECT)
    def __str__(self):
        return self.mansucript_name
    
    