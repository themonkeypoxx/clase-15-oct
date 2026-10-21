from django import forms
from .models import Figura


class FiguraForm(forms.ModelForm):
    class Meta:
        model = Figura
        fields = [
            'nombre', 'categoria', 'fabricante', 'escala', 
            'descripcion', 'precio', 'stock', 'imagen', 'destacado', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Figura Son Goku 18cm'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Bandai Spirits'}),
            'escala': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Escala 1/7 (24 cm)'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser superior a 0 CLP.")
        return precio