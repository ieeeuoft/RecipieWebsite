from django.urls import path
from .views import recipe_list

app_name = 'core'
urlpatterns = [
    path('', recipe_list, name='recipe-list')
]
