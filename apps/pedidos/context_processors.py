def carrito_context(request):
    """Permite acceder al número de figuras en el carrito de cualquier plantilla"""
    carrito = request.session.get('carrito',{})
    total_items = sum(item.get('cantidad',0) for item in carrito.values())
    return{
        'carrito_total_items': total_items
    }