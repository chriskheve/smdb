from django.urls import path

from . import api

urlpatterns = [
    path('create/', api.create_site, name='create_site'),
    path('import-excel/', api.import_sites_excel, name='import_sites_excel'),
    path('all/', api.get_all_sites, name='get_all_sites'),
    
]