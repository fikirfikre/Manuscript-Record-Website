import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manuscript.settings')
django.setup()

from main.models import User, Reader, Genre, RepositoryOwner, RepositoryLocation, Repository, Language, Inventor, Manuscript

# Read the Excel file
df = pd.read_excel('main\static\Excel Worksheet_TR_Written Heritage March_a_2023.xlsx')

# Example: Insert data into Classification model
# for _, row in df.iterrows():
    # classification, created = Classification.objects.get_or_create(name=row['Classification'])
    # Assuming the DataFrame has a column named 'Classification'

# Example: Insert data into Manuscript model
for _, row in df.iterrows():
    # classification = Classification.objects.get(name=row['Classification'])
    repository = Repository.objects.get(name=row['Repository'])
    language = Language.objects.get(name=row['Language'])
    genre = Genre.objects.get(name=row['Genre'])
    repository_location = RepositoryLocation.objects.get(location=row['RepositoryLocation'])
    inventor = User.objects.get(username=row['Inventor'])
    
    manuscript = Manuscript(
        index=row['Index'],
        # uid=classification,
        repository=repository,
        manuscript_name=row['ManuscriptName'],
        repositoryOwner=row['RepositoryOwner'],
        shelf_mark_By_Instutition=row['ShelfMarkByInstitution'],
        shelf_mark_By_author=row['ShelfMarkByAuthor'],
        responsiblit_statement=row['ResponsibilityStatement'],
        inventor_date=row['InventorDate'],
        measurement=row['Measurement'],
        folios_number=row['FoliosNumber'],
        binding=row['Binding'],
        main_content=row['MainContent'],
        dating=row['Dating'],
        other_provenance=row['OtherProvenance'],
        scripe=row['Scribe'],
        no_of_cols=row['NoOfCols'],
        notes_cur_use=row['NotesCurrentUse'],
        no_of_lines=row['NoOfLines'],
        decoration=row['Decoration'],
        colophones=row['Colophones'],
        additional_notes=row['AdditionalNotes'],
        inventor=inventor,
        repositoryLocation=repository_location
    )
    manuscript.save()
    manuscript.language.set([language])
    manuscript.genere.set([genre])

print("Data inserted successfully!")
