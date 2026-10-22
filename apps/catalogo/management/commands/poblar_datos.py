from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.catalogo.models import Categoria, Figura


class Command(BaseCommand):
    help = "Pobla la base de datos con categorías y figuras de prueba."

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@mundofiguras.cl", "admin")
            self.stdout.write(self.style.SUCCESS("✓ Superusuario 'admin' creado."))

        categorias = {
            "Anime y Manga": "Series animadas japonesas.",
            "Cómics y Superhéroes": "Universo Marvel y DC Comics.",
            "Videojuegos": "Franquicias de consolas y PC.",
            "Cine y Televisión": "Películas de culto y sagas."
        }
        cat_map = {}
        for nombre, desc in categorias.items():
            cat, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
            cat_map[nombre] = cat

        figuras = [
            ("Figura Son Goku Super Saiyan", cat_map["Anime y Manga"], "Bandai Spirits", 34990, 10, True),
            ("Figura Monkey D. Luffy Gear 5", cat_map["Anime y Manga"], "Banpresto", 39990, 8, True),
            ("Estatua Batman The Dark Knight", cat_map["Cómics y Superhéroes"], "Kotobukiya", 189990, 3, True),
            ("Figura Link Tears of the Kingdom", cat_map["Videojuegos"], "Good Smile", 69990, 6, True),
        ]
        for nom, cat, fab, pre, stk, dest in figuras:
            Figura.objects.get_or_create(nombre=nom, defaults={
                'categoria': cat, 'fabricante': fab, 'precio': pre, 'stock': stk, 'destacado': dest, 'activo': True
            })

        self.stdout.write(self.style.SUCCESS("✓ Catálogo poblado exitosamente."))