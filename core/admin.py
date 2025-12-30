"""
Configuración del Panel de Administración
==========================================
Personaliza la interfaz de admin para gestionar usuarios y barcos.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Barco


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Admin personalizado para el modelo Usuario.
    Extiende UserAdmin para mantener la funcionalidad de gestión de contraseñas.
    """
    list_display = ('username', 'email', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    # Añadir el campo 'rol' al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en el Sistema', {'fields': ('rol',)}),
    )
    
    # Añadir el campo 'rol' al formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol en el Sistema', {'fields': ('rol',)}),
    )


@admin.register(Barco)
class BarcoAdmin(admin.ModelAdmin):
    """
    Admin para gestionar los registros de barcos.
    """
    list_display = ('nombre', 'imo', 'bandera', 'tipo', 'fecha_llegada', 'registrado_por')
    list_filter = ('tipo', 'bandera', 'fecha_llegada')
    search_fields = ('nombre', 'imo')
    readonly_fields = ('fecha_llegada', 'registrado_por')
    ordering = ('-fecha_llegada',)
    
    def save_model(self, request, obj, form, change):
        """Guarda automáticamente quién registró el barco desde el admin."""
        if not change:  # Solo en creación
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)
