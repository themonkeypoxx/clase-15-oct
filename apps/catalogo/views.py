from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Figura, Categoria
from .forms import FiguraForm


def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def figura_lista(request):
    query = request.GET.get('q', '').strip()
    categoria_slug = request.GET.get('categoria', '')
    orden = request.GET.get('orden', '-fecha_creacion')

    figuras = Figura.objects.filter(activo=True).select_related('categoria')

    if categoria_slug:
        figuras = figuras.filter(categoria__slug=categoria_slug)

    if query:
        figuras = figuras.filter(
            Q(nombre__icontains=query) |
            Q(fabricante__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )

    ordenes_validos = {
        'precio_asc': 'precio',
        'precio_desc': '-precio',
        'nombre_asc': 'nombre',
        'recientes': '-fecha_creacion',
    }
    figuras = figuras.order_by(ordenes_validos.get(orden, '-fecha_creacion'))

    paginador = Paginator(figuras, 6)
    pagina = paginador.get_page(request.GET.get('page'))
    categorias = Categoria.objects.filter(activo=True)

    return render(request, 'catalogo/figura_lista.html', {
        'figuras': pagina,
        'categorias': categorias,
        'categoria_seleccionada': categoria_slug,
        'query_actual': query,
        'orden_actual': orden,
        'total_resultados': figuras.count(),
    })


def figura_detalle(request, slug):
    figura = get_object_or_404(Figura.objects.select_related('categoria'), slug=slug, activo=True)
    relacionadas = Figura.objects.filter(categoria=figura.categoria, activo=True).exclude(pk=figura.pk)[:3]
    return render(request, 'catalogo/figura_detalle.html', {'figura': figura, 'relacionadas': relacionadas})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def gestion_figuras(request):
    query = request.GET.get('q', '').strip()
    figuras = Figura.objects.all().select_related('categoria')
    if query:
        figuras = figuras.filter(Q(nombre__icontains=query) | Q(fabricante__icontains=query))
    paginador = Paginator(figuras.order_by('-fecha_creacion'), 10)
    pagina = paginador.get_page(request.GET.get('page'))
    return render(request, 'catalogo/gestion_figuras.html', {'figuras': pagina, 'query': query})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def figura_crear(request):
    if request.method == 'POST':
        form = FiguraForm(request.POST, request.FILES)
        if form.is_valid():
            figura = form.save()
            messages.success(request, f"¡Figura '{figura.nombre}' creada exitosamente!")
            return redirect('catalogo:gestion')
    else:
        form = FiguraForm()
    return render(request, 'catalogo/figura_form.html', {'form': form, 'titulo_accion': 'Ingresar Nueva Figura', 'boton_texto': 'Guardar'})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def figura_editar(request, id):
    figura = get_object_or_404(Figura, id=id)
    if request.method == 'POST':
        form = FiguraForm(request.POST, request.FILES, instance=figura)
        if form.is_valid():
            form.save()
            messages.success(request, f"Figura '{figura.nombre}' actualizada.")
            return redirect('catalogo:gestion')
    else:
        form = FiguraForm(instance=figura)
    return render(request, 'catalogo/figura_form.html', {'form': form, 'figura': figura, 'titulo_accion': 'Editar Figura', 'boton_texto': 'Actualizar'})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def figura_eliminar(request, id):
    figura = get_object_or_404(Figura, id=id)
    if request.method == 'POST':
        nombre = figura.nombre
        figura.delete()
        messages.success(request, f"Figura '{nombre}' eliminada.")
        return redirect('catalogo:gestion')
    return render(request, 'catalogo/figura_confirmar_eliminar.html', {'figura': figura})