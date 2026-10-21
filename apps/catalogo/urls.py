from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.figura_lista, name='lista'),
    path('figura/<slug:slug>/', views.figura_detalle, name='detalle'),
    path('gestion/', views.gestion_figuras, name='gestion'),
    path('gestion/nueva/', views.figura_crear, name='crear'),
    path('gestion/editar/<int:id>/', views.figura_editar, name='editar'),
    path('gestion/eliminar/<int:id>/', views.figura_eliminar, name='eliminar'),
]