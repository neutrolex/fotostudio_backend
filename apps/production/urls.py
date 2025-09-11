"""
URLs para la app de producción.
"""

from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    # URLs para Órdenes de Producción
    path('orders/', views.ProductionListView.as_view(), name='production-list'),
    path('orders/<int:pk>/', views.ProductionDetailView.as_view(), name='production-detail'),
    
    # URLs para Cuadros
    path('cuadros/', views.CuadroListView.as_view(), name='cuadro-list'),
    path('cuadros/<int:pk>/', views.CuadroDetailView.as_view(), name='cuadro-detail'),
    
    # URLs para Detalles de Orden
    path('detalles/', views.DetalleOrdenListView.as_view(), name='detalle-orden-list'),
    path('detalles/<int:pk>/', views.DetalleOrdenDetailView.as_view(), name='detalle-orden-detail'),
    
    # URLs para Movimientos de Inventario
    path('movements/', views.MovimientoInventarioListView.as_view(), name='movimiento-inventario-list'),
    path('movements/<int:pk>/', views.MovimientoInventarioDetailView.as_view(), name='movimiento-inventario-detail'),
    
    # URLs especiales para funcionalidades de producción
    path('register/', views.register_production, name='register-production'),
    path('efficiency/', views.production_efficiency, name='production-efficiency'),
    path('waste/', views.waste_report, name='waste-report'),
    path('report/', views.production_report, name='production-report'),
    
    # URLs legacy para compatibilidad
    path('', views.ProductionListView.as_view(), name='production-list-legacy'),
    path('<int:pk>/', views.ProductionDetailView.as_view(), name='production-detail-legacy'),
]
