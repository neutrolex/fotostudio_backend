
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación y usuarios
    path('api/auth/', include('apps.users.urls')),
    path('api/tenants/', include('apps.tenants.urls')),
    
    # Módulo 2 - Gestión de Negocio
    path('api/orders/', include('apps.orders.urls')),
    path('api/clients/', include('apps.clients.urls')),
    path('api/contracts/', include('apps.contracts.urls')),
    path('api/agenda/', include('apps.agenda.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    
    # Módulo 3 - Inventario y Producción
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/materials/', include('apps.materials.urls')),
    path('api/production/', include('apps.production.urls')),

    # Módulo 4 - Reportes y Métricas
    path('api/reports/', include('apps.reports.urls')),
    path('api/metrics/', include('apps.metrics.urls')),
]
