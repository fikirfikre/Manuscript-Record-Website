from django.db import models
from django.contrib.auth.models import Permission, Group,AbstractUser
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    class Role(models.TextChoices):
        READER = "READER", "reader"
        INVENTOR= "INVENTOR", "inventor"
        ADMIN="ADMIN","admin"
    base_role = Role.READER
    role = models.CharField(max_length=10,choices = Role.choices,default=base_role)
class Classfication(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Reader(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="reader")
    name = models.CharField(max_length=150)
    address =models.CharField( max_length=50)
    email = models.EmailField( max_length=254) 
    def __str__(self):
        return self.name 
class Genre(models.Model):
    name = models.CharField(max_length = 100)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
class RepositoryOwner(models.Model):
    # index = models.CharField(unique=True,max_length=255)
    # uid = models.ForeignKey(Classfication,on_delete=models.PROTECT)
    name = models.CharField(max_length = 255)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class RepositoryLocation(models.Model):
    location = models.CharField(max_length=255)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.location
    
class Repository(models.Model):
    # index = models.CharField(unique=True,max_length=255)
    # uid = models.ForeignKey(Classfication,on_delete=models.PROTECT)
    name = models.CharField(max_length = 255)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.name



    
class Language(models.Model):
    name = models.CharField(max_length=100,unique=True)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
        
class Inventor(models.Model):
    name = models.CharField(max_length=255)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
  

   
class Manuscript(models.Model):
    # index = models.CharField(unique=True,max_length=255)
    # uid = models.ForeignKey(Classfication,on_delete=models.PROTECT)
    # repository = models.ForeignKey(Repository,on_delete = models.PROTECT)

    language = models.ManyToManyField(Language)
    genere = models.ManyToManyField(Genre)
    repositoryLocation = models.ForeignKey(RepositoryLocation,on_delete = models.PROTECT)
    repository = models.CharField(max_length=255,null=False,blank=False)
    manuscript_title = models.CharField(max_length = 100,null=False,blank=False)
    inventor = models.ForeignKey(User, on_delete=models.PROTECT)
    
    # inventor = models.ForeignKey(Inventor, on_delete=models.PROTECT)
    repository_owner = models.CharField(max_length=255)
    
    shelf_mark_By_Instutition = models.CharField(max_length=255,null=False,blank=False)
    shelf_mark_By_author  = models.CharField(max_length=255,null=False,blank=False)
    responsibility_statement = models.CharField( max_length=255,null=False,blank=False)
    upload_date = models.DateField(auto_now_add=True,null=False,blank=False)
    inventor_date = models.CharField(max_length=255)
    measurement =models.CharField(max_length=255,null=False,blank=False)
    folios_number = models.CharField(max_length=255,null=False,blank=False)
    binding = models.CharField(max_length=100,null=False,blank=False)
    main_content = models.TextField(null=False,blank=False)
    dating = models.CharField(max_length=255,blank=True, null=True)
    other_provenance = models.CharField(max_length=255,blank=True, null=True)
    scripe = models.CharField(max_length=255,blank=True, null=True)
    no_of_cols = models.CharField(max_length=255,null=False,blank=False )
    notes_cur_use = models.TextField(blank=True, null=True)    
    no_of_lines = models.CharField(max_length=255,null=False,blank=False)
    decoration = models.CharField(max_length=255,null=True,blank=True)
    colophones = models.CharField( max_length=255,null=True,blank=True)
    additional_notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='book_images/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],blank=True, null=True)

    def __str__(self):
        return self.manuscript_title
    

