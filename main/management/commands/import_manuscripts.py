import os
import django
import pandas as pd
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manuscript.settings')
django.setup()

from main.models import Manuscript, Classfication, Repository, Language, Genre, RepositoryLocation, User

# Define a function to get or create foreign key objects
def get_or_create_fk(model, **kwargs):
    instance, created = model.objects.get_or_create(**kwargs)
    instance.save()
    return instance

# Read data from Excel file
file_path = 'main/static/Excel Worksheet_TR_Written Heritage March_a_2023.xlsx'
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# Handle NaN values for numerical fields with a default value
def handle_nan(value, default=0):
    return value if pd.notna(value) else default

# Iterate over the rows of the dataframe and insert into the database
for index, row in df.iterrows():
    
        # Retrieve or create the repository
        inventor = User.objects.first()
        repository, created = Repository.objects.get_or_create(name=row['Name of the current repository'], defaults={'inventor': inventor})
        if not created:
            print(f"Repository already exists: {repository.name}")
        
        # Retrieve or create the repository location
        repository_location, created = RepositoryLocation.objects.get_or_create(location=row['Physical address'], defaults={'inventor': inventor})
        
        # Process languages
        languages = []
        if pd.notna(row['Language(s)']):
            languages = [Language.objects.get_or_create(name=lang.strip(), defaults={'inventor': inventor})[0] for lang in row['Language(s)'].split(',')]
        
        # Process genres
        genres = []
        genre_key = 'Genre keywords (Bib - Biblical; Hag. - Hagiography; Hom. - Homily; Lit. - Liturgical;  )'
        if pd.notna(row[genre_key]):
            genres = [Genre.objects.get_or_create(name=gen.strip(), defaults={'inventor': inventor})[0] for gen in row[genre_key].split(',')]

        # Handle NaN values for numerical fields
        folios_number = handle_nan(row['Folios number'])
        no_of_cols = handle_nan(row['Number of columns'])
        no_of_lines = handle_nan(row['Number of lines'])

        # Create the manuscript instance
        manuscript = Manuscript(
            repository=repository,
            repositoryLocation=repository_location,
            manuscript_name=row['Name of the current repository'],
            repositoryOwner=row['Owner(s):'],
            shelf_mark_By_Instutition=row['Shelfmark(s) given by the repository'],
            shelf_mark_By_author=row['Scribe:'],
            responsiblit_statement=row['Responsibility Statement'],
            inventor_date=row['Dating (with explanation)'],
            measurement=row['Measurements (height x width + thickness, mm)'],
            folios_number=folios_number,
            binding=row['Binding'],
            main_content=row['Main content:'],
            dating=row.get('Dating (with explanation)', ''),
            other_provenance=row.get('Other provenance details:', ''),
            scripe=row.get('Scribe:', ''),
            no_of_cols=no_of_cols,
            notes_cur_use=row.get('Notes on current use:', ''),
            no_of_lines=no_of_lines,
            decoration=row.get('Decorations', ''),
            colophones=row.get('Colophon(s)', ''),
            additional_notes=row.get('Additional notes:', ''),
            inventor=inventor  # Assuming the first user is the inventor
        )
        manuscript.save()
        
        # Add many-to-many relationships
        manuscript.language.add(*languages)
        manuscript.genere.add(*genres)

        print(f'Inserted manuscript: {manuscript.manuscript_title}')
    
