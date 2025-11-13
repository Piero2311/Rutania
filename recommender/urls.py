from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('', views.index, name='index'),
    path('recomendar/', views.recomendar, name='recomendar'),
    path('rutinas/', views.catalogo_rutinas, name='rutinas'),
    path('acerca-de/', views.acerca_de, name='acerca'),
]
