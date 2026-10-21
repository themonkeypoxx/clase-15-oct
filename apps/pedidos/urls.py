from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('carrito/', views.carrito_ver, name='ver'),
    path('carrito/agregar/<int:id>/', views.carrito_agregar, name='agregar'),
    path('carrito/restar/<int:id>/', views.carrito_restar, name='restar'),
    path('carrito/eliminar/<int:id>/', views.carrito_eliminar, name='eliminar'),
    path('carrito/limpiar/', views.carrito_limpiar, name='limpiar'),
    path('checkout/', views.checkout_simulado, name='checkout'),
]