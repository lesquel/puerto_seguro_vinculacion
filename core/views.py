"""
Vistas del Sistema de Seguridad Portuaria
==========================================
Implementa autenticación y autorización basada en roles.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Barco
from .forms import BarcoForm


# ============================================================================
# FUNCIONES DE VERIFICACIÓN DE ROLES (Autorización)
# ============================================================================

def es_admin(user):
    """Verifica si el usuario es administrador."""
    return user.rol == 'admin' or user.is_superuser


def es_operador(user):
    """Verifica si el usuario es operador o tiene permisos superiores."""
    return user.rol in ('operador', 'admin') or user.is_superuser


def es_guardia_o_superior(user):
    """Verifica si el usuario tiene al menos rol de guardia (cualquier rol)."""
    return user.rol in ('guardia', 'operador', 'admin') or user.is_superuser


# ============================================================================
# VISTAS PÚBLICAS
# ============================================================================

def home(request):
    """
    Página principal del sistema.
    Muestra información diferente según el estado de autenticación.
    """
    context = {
        'total_barcos': Barco.objects.count(),
    }
    return render(request, 'home.html', context)


# ============================================================================
# VISTAS PROTEGIDAS (Requieren Login)
# ============================================================================

@login_required
def lista_barcos(request):
    """
    Lista todos los barcos registrados.
    Requiere: Usuario autenticado (cualquier rol).
    """
    barcos = Barco.objects.all().select_related('registrado_por')
    return render(request, 'lista_barcos.html', {'barcos': barcos})


@login_required
def detalle_barco(request, pk):
    """
    Muestra el detalle de un barco específico.
    Requiere: Usuario autenticado (cualquier rol).
    """
    from django.shortcuts import get_object_or_404
    barco = get_object_or_404(Barco, pk=pk)
    return render(request, 'detalle_barco.html', {'barco': barco})


# ============================================================================
# VISTAS RESTRINGIDAS (Requieren Login + Rol Específico)
# ============================================================================

@login_required
@user_passes_test(es_operador, login_url='home')
def crear_barco(request):
    """
    Formulario para registrar un nuevo barco.
    Requiere: Usuario autenticado con rol 'operador' o 'admin'.
    
    El decorador @user_passes_test verifica el rol antes de permitir acceso.
    Si el usuario no tiene permisos, es redirigido a 'home'.
    """
    if request.method == 'POST':
        form = BarcoForm(request.POST)
        if form.is_valid():
            barco = form.save(commit=False)
            barco.registrado_por = request.user  # Auditoría: guardamos quién creó
            barco.save()
            messages.success(request, f'✅ Barco "{barco.nombre}" registrado exitosamente.')
            return redirect('lista_barcos')
    else:
        form = BarcoForm()
    
    return render(request, 'crear_barco.html', {'form': form})


@login_required
@user_passes_test(es_operador, login_url='home')
def editar_barco(request, pk):
    """
    Formulario para editar un barco existente.
    Requiere: Usuario autenticado con rol 'operador' o 'admin'.
    """
    from django.shortcuts import get_object_or_404
    barco = get_object_or_404(Barco, pk=pk)
    
    if request.method == 'POST':
        form = BarcoForm(request.POST, instance=barco)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Barco "{barco.nombre}" actualizado.')
            return redirect('lista_barcos')
    else:
        form = BarcoForm(instance=barco)
    
    return render(request, 'editar_barco.html', {'form': form, 'barco': barco})


@login_required
@user_passes_test(es_admin, login_url='home')
def eliminar_barco(request, pk):
    """
    Elimina un barco del sistema.
    Requiere: Usuario autenticado con rol 'admin' únicamente.
    """
    from django.shortcuts import get_object_or_404
    barco = get_object_or_404(Barco, pk=pk)
    
    if request.method == 'POST':
        nombre = barco.nombre
        barco.delete()
        messages.warning(request, f'🗑️ Barco "{nombre}" eliminado del sistema.')
        return redirect('lista_barcos')
    
    return render(request, 'eliminar_barco.html', {'barco': barco})


# ============================================================================
# VISTA DEL PANEL DE CONTROL (Dashboard)
# ============================================================================

@login_required
def dashboard(request):
    """
    Panel de control con estadísticas del sistema.
    Muestra información según el rol del usuario.
    """
    from django.db.models import Count
    
    context = {
        'total_barcos': Barco.objects.count(),
        'barcos_por_tipo': Barco.objects.values('tipo').annotate(total=Count('tipo')),
    }
    
    # Los operadores/admins ven sus propios registros
    if es_operador(request.user):
        context['mis_registros'] = Barco.objects.filter(
            registrado_por=request.user
        ).count()
    
    return render(request, 'dashboard.html', context)
