from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.catalogo.models import Figura


def _obtener_carrito(request):
    return request.session.setdefault('carrito', {})


def carrito_ver(request):
    carrito = _obtener_carrito(request)
    subtotal = sum(item['subtotal'] for item in carrito.values())
    iva = int(subtotal * 0.19)
    total = subtotal + iva
    return render(request, 'pedidos/carrito.html', {
        'items_carrito': carrito.values(),
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'esta_vacio': len(carrito) == 0,
    })


def carrito_agregar(request, id):
    figura = get_object_or_404(Figura, id=id, activo=True)
    carrito = _obtener_carrito(request)
    str_id = str(figura.id)

    cantidad_actual = carrito.get(str_id, {}).get('cantidad', 0)
    nueva_cantidad = cantidad_actual + 1

    if nueva_cantidad > figura.stock:
        messages.warning(request, f"Límite de stock alcanzado ({figura.stock} unidades) para '{figura.nombre}'.")
        return redirect('pedidos:ver')

    imagen_url = figura.imagen.url if figura.imagen else ''
    carrito[str_id] = {
        'id': figura.id,
        'nombre': figura.nombre,
        'slug': figura.slug,
        'fabricante': figura.fabricante,
        'precio': int(figura.precio),
        'cantidad': nueva_cantidad,
        'subtotal': int(figura.precio) * nueva_cantidad,
        'imagen_url': imagen_url,
    }

    # Notifica a Django que la sesión fue modificada
    request.session.modified = True
    messages.success(request, f"'{figura.nombre}' añadida al carrito.")
    return redirect(request.META.get('HTTP_REFERER') or 'pedidos:ver')


def carrito_restar(request, id):
    carrito = _obtener_carrito(request)
    str_id = str(id)
    if str_id in carrito:
        carrito[str_id]['cantidad'] -= 1
        if carrito[str_id]['cantidad'] <= 0:
            del carrito[str_id]
        else:
            carrito[str_id]['subtotal'] = carrito[str_id]['precio'] * carrito[str_id]['cantidad']
        request.session.modified = True
    return redirect('pedidos:ver')


def carrito_eliminar(request, id):
    carrito = _obtener_carrito(request)
    str_id = str(id)
    if str_id in carrito:
        del carrito[str_id]
        request.session.modified = True
        messages.warning(request, "Figura eliminada del carrito.")
    return redirect('pedidos:ver')


def carrito_limpiar(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        request.session.modified = True
    return redirect('pedidos:ver')


@login_required
def checkout_simulado(request):
    carrito = _obtener_carrito(request)
    if not carrito:
        return redirect('catalogo:lista')

    subtotal = sum(item['subtotal'] for item in carrito.values())
    iva = int(subtotal * 0.19)
    total = subtotal + iva
    items_comprados = list(carrito.values())

    del request.session['carrito']
    request.session.modified = True

    return render(request, 'pedidos/checkout_exito.html', {
        'items': items_comprados,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'orden_id': f"FIG-{request.user.id}-2026",
    })