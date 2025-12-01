from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    # Páginas públicas
    path('', views.index, name='index'),
    path('recomendar/', views.recomendar, name='recomendar'),
    path('rutinas/', views.catalogo_rutinas, name='rutinas'),
    path('acerca-de/', views.acerca_de, name='acerca'),
    
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    
    # Dashboard y perfil (requieren autenticación)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),
    path('generar-recomendacion/', views.generar_recomendacion, name='generar_recomendacion'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('historial-recomendaciones/', views.historial_recomendaciones, name='historial_recomendaciones'),
    path('rutina/<int:rutina_id>/semanal/', views.rutina_semanal, name='rutina_semanal'),
    
    # Chatbot API
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/marcar-ejercicio/', views.marcar_ejercicio, name='marcar_ejercicio'),
]
