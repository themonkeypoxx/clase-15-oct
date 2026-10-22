from django.shortcuts import render
from apps.catalogo.models import Figura, Categoria


def inicio(request):
    """
    Portada de Mundo Figuras con figuras destacadas, categorías principales
    y promociones vigentes.
    """
    destacadas = Figura.objects.filter(
        activo=True,
        destacado=True
    ).select_related('categoria')[:4]

    categorias = Categoria.objects.filter(activo=True)[:6]

    return render(request, 'core/index.html', {
        'destacadas': destacadas,
        'categorias': categorias,
        'total_figuras': Figura.objects.filter(activo=True).count(),
        'total_categorias': Categoria.objects.filter(activo=True).count(),
    })


def nosotros(request):
    """
    Información institucional sobre la tienda Mundo Figuras,
    garantía de originalidad, envíos a todo Chile y atención al coleccionista.
    """
    return render(request, 'core/nosotros.html')