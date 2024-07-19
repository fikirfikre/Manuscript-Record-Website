from django.core.management.base import BaseCommand
import pandas as pd 
import datetime
from main.models import *
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manuscript.settings')
django.setup()

df = pd.read_excel('main\static\Excel Worksheet_TR_Written Heritage March_a_2023.xlsx')
for index, row in df.iterrows():
    inventor = User.objects.get(username = "admin")
#    classfication,_ = Classfication.objects.get_or_create(name=row['uid'])
    genre,_  = Genre.objects.get_or_create(name=row["Genre keywords (Bib - Biblical; Hag. - Hagiography; Hom. - Homily; Lit. - Liturgical;  )"],inventor = inventor)
    language,_ = Language.objects.get_or_create(name=row['Language(s)'],inventor=inventor)
    location,_ = RepositoryLocation.objects.get_or_create(location=row["Physical address"],inventor= inventor)

class Command(BaseCommand):
  def handle(self, *args, **kwargs):

    inventor = User.objects.get(user_name = "admin")
    df = pd.read_excel('main\static\Excel Worksheet_TR_Written Heritage March_a_2023.xlsx')
    for index, row in df.iterrows():
        print(row)