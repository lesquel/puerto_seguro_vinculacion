"""
Formularios del Sistema de Seguridad Portuaria
===============================================
Define los formularios para la captura de datos.
"""

from django import forms
from .models import Barco


class BarcoForm(forms.ModelForm):
    """
    Formulario para crear y editar barcos.
    
    Usa ModelForm para generar automáticamente los campos
    basándose en el modelo Barco.
    """
    
    class Meta:
        model = Barco
        fields = ['nombre', 'imo', 'bandera', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: MSC Esperanza'
            }),
            'imo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 9484525'
            }),
            'bandera': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Panamá'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        help_texts = {
            'imo': 'Número único de 7 dígitos asignado por la OMI',
        }
