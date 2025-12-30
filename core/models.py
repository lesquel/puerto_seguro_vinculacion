"""
Modelos del Sistema de Seguridad Portuaria
==========================================
Implementa el modelo de Usuario personalizado con roles y el modelo Barco.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Usuario personalizado con sistema de roles.
    
    Extiende AbstractUser para añadir el campo 'rol' que determina
    los permisos del usuario en el sistema.
    
    Roles disponibles:
    - admin: Administrador (Jefe de Puerto) - Acceso total
    - operador: Operador - Puede registrar y gestionar barcos
    - guardia: Guardia - Solo puede ver información (lectura)
    """
    ROLES = (
        ('admin', 'Administrador (Jefe de Puerto)'),
        ('operador', 'Operador (Registra Barcos)'),
        ('guardia', 'Guardia (Solo ve accesos)'),
    )
    
    rol = models.CharField(
        max_length=20, 
        choices=ROLES, 
        default='guardia',
        verbose_name='Rol del Usuario',
        help_text='Define los permisos del usuario en el sistema'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


class Barco(models.Model):
    """
    Modelo que representa un barco registrado en el puerto.
    
    Incluye información básica del barco y datos de auditoría
    para saber quién y cuándo registró cada embarcación.
    """
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre del Barco'
    )
    imo = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name='Número IMO',
        help_text='Número de identificación marítima internacional (único)'
    )
    bandera = models.CharField(
        max_length=50,
        verbose_name='País de Bandera',
        default='Ecuador'
    )
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('carga', 'Buque de Carga'),
            ('pasajeros', 'Buque de Pasajeros'),
            ('petrolero', 'Petrolero'),
            ('pesquero', 'Pesquero'),
            ('otro', 'Otro'),
        ],
        default='carga',
        verbose_name='Tipo de Embarcación'
    )
    fecha_llegada = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    # Auditoría: Quién registró el barco (Best Practice)
    registrado_por = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Registrado por',
        related_name='barcos_registrados'
    )

    class Meta:
        verbose_name = 'Barco'
        verbose_name_plural = 'Barcos'
        ordering = ['-fecha_llegada']

    def __str__(self):
        return f"{self.nombre} (IMO: {self.imo})"
