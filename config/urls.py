"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    # Panel de Administración de Django
    path('admin/', admin.site.urls),
    
    # Sistema de Autenticación de Django (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Páginas Públicas
    path('', views.home, name='home'),
    
    # Panel de Control
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestión de Barcos (CRUD)
    path('barcos/', views.lista_barcos, name='lista_barcos'),
    path('barcos/nuevo/', views.crear_barco, name='crear_barco'),
    path('barcos/<int:pk>/', views.detalle_barco, name='detalle_barco'),
    path('barcos/<int:pk>/editar/', views.editar_barco, name='editar_barco'),
    path('barcos/<int:pk>/eliminar/', views.eliminar_barco, name='eliminar_barco'),
]
