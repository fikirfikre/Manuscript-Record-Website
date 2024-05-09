from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Manuscript)
admin.site.register(Repository)
admin.site.register(RepositoryOwner)
admin.site.register(RepositoryLocation)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(User)
admin.site.register(Reader)
admin.site.register(Classfication)

