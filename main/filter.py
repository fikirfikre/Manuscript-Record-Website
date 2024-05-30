import django_filters
from django import forms
from django_filters import DateFilter, CharFilter
from .models import *
class ManuscriptFilter(django_filters.FilterSet):
    title = CharFilter(field_name="manuscript_name", lookup_expr = 'icontains')
    
    class Meta:
        model = Manuscript
        fields = ["genere","language","repository","repositoryLocation"]
    def __init__(self,*args,**kwargs):
        super(ManuscriptFilter,self).__init__(*args,**kwargs)
        # self.filters['genere'].extra.update({'empty_label': "select genre"})
        self.filters['repository'].extra.update({'empty_label':'Repositories'})
        # self.fields['uid'].empty_label = "select code"
        self.filters['repositoryLocation'].extra.update({'empty_label':"Locations"})
      

    def has_active_filters(self):
        # Check if any filter options are selected (excluding "all_manuscripts")
        print(self.data.items())
        for name, value in self.data.items():
            if value and name != 'all_manuscripts':
                return True
        return False

    def has_results(self):
        # Return True only if the filter QuerySet contains results
        return self.qs.exists()
