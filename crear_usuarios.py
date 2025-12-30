"""
Script para crear usuarios de prueba en el sistema.
Ejecutar con: uv run python manage.py shell < crear_usuarios.py
O mejor: uv run python crear_usuarios.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Usuario, Barco

def crear_usuarios_demo():
    """Crea los usuarios de demostración para probar el sistema."""
    
    print("=" * 50)
    print("🚀 Creando usuarios de demostración...")
    print("=" * 50)
    
    usuarios_demo = [
        {
            'username': 'admin',
            'email': 'admin@puerto.com',
            'password': 'admin123',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'rol': 'admin',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'ana_operadora',
            'email': 'ana@puerto.com',
            'password': 'operador123',
            'first_name': 'Ana',
            'last_name': 'García',
            'rol': 'operador',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'username': 'pepe_guardia',
            'email': 'pepe@puerto.com',
            'password': 'guardia123',
            'first_name': 'José',
            'last_name': 'Pérez',
            'rol': 'guardia',
            'is_staff': False,
            'is_superuser': False,
        },
    ]
    
    for datos in usuarios_demo:
        username = datos.pop('username')
        password = datos.pop('password')
        
        usuario, creado = Usuario.objects.get_or_create(
            username=username,
            defaults=datos
        )
        
        if creado:
            usuario.set_password(password)
            usuario.save()
            print(f"✅ Usuario '{username}' creado con rol '{usuario.rol}'")
        else:
            print(f"ℹ️  Usuario '{username}' ya existe")
    
    print()
    print("=" * 50)
    print("📋 Usuarios disponibles para login:")
    print("=" * 50)
    print()
    print("┌──────────────────┬─────────────┬──────────────────┐")
    print("│ Usuario          │ Contraseña  │ Rol              │")
    print("├──────────────────┼─────────────┼──────────────────┤")
    print("│ admin            │ admin123    │ Administrador    │")
    print("│ ana_operadora    │ operador123 │ Operador         │")
    print("│ pepe_guardia     │ guardia123  │ Guardia          │")
    print("└──────────────────┴─────────────┴──────────────────┘")
    print()


def crear_barcos_demo():
    """Crea algunos barcos de ejemplo para demostración."""
    
    print("🚢 Creando barcos de demostración...")
    print()
    
    # Obtener el usuario operador para asignar como registrador
    try:
        operador = Usuario.objects.get(username='ana_operadora')
    except Usuario.DoesNotExist:
        operador = None
    
    barcos_demo = [
        {
            'nombre': 'MSC Esperanza',
            'imo': '9484525',
            'bandera': 'Panamá',
            'tipo': 'carga',
        },
        {
            'nombre': 'Costa Pacífica',
            'imo': '9378498',
            'bandera': 'Italia',
            'tipo': 'pasajeros',
        },
        {
            'nombre': 'Tanker Ecuador',
            'imo': '9156778',
            'bandera': 'Ecuador',
            'tipo': 'petrolero',
        },
    ]
    
    for datos in barcos_demo:
        imo = datos['imo']
        barco, creado = Barco.objects.get_or_create(
            imo=imo,
            defaults={**datos, 'registrado_por': operador}
        )
        
        if creado:
            print(f"✅ Barco '{barco.nombre}' registrado (IMO: {barco.imo})")
        else:
            print(f"ℹ️  Barco con IMO '{imo}' ya existe")
    
    print()


if __name__ == '__main__':
    crear_usuarios_demo()
    crear_barcos_demo()
    print("🎉 ¡Datos de demostración creados exitosamente!")
    print()
    print("Ejecuta el servidor con:")
    print("  uv run python manage.py runserver")
    print()
    print("Luego accede a: http://127.0.0.1:8000/")
    print()
