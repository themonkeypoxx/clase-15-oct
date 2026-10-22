from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('catalogo/', include('apps.catalogo.urls', namespace='catalogo')),
    path('pedidos/', include('apps.pedidos.urls', namespace='pedidos')),
]

# Servir archivos multimedia durante el desarrollo local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)