"""
URLs para la app de inventario.
"""

from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # URLs legacy para compatibilidad
    path('', views.InventoryListView.as_view(), name='inventory-list'),
    path('<int:pk>/', views.InventoryDetailView.as_view(), name='inventory-detail'),
    
    # URLs para Varillas
    path('varillas/', views.VarillaListView.as_view(), name='varilla-list'),
    path('varillas/<int:pk>/', views.VarillaDetailView.as_view(), name='varilla-detail'),
    
    # URLs para Pinturas y Acabados
    path('pinturas/', views.PinturaAcabadoListView.as_view(), name='pintura-acabado-list'),
    path('pinturas/<int:pk>/', views.PinturaAcabadoDetailView.as_view(), name='pintura-acabado-detail'),
    
    # URLs para Materiales de Impresión
    path('impresion/', views.MaterialImpresionListView.as_view(), name='material-impresion-list'),
    path('impresion/<int:pk>/', views.MaterialImpresionDetailView.as_view(), name='material-impresion-detail'),
    
    # URLs para Materiales de Recordatorio
    path('recordatorio/', views.MaterialRecordatorioListView.as_view(), name='material-recordatorio-list'),
    path('recordatorio/<int:pk>/', views.MaterialRecordatorioDetailView.as_view(), name='material-recordatorio-detail'),
    
    # URLs para Software y Equipos
    path('software/', views.SoftwareEquipoListView.as_view(), name='software-equipo-list'),
    path('software/<int:pk>/', views.SoftwareEquipoDetailView.as_view(), name='software-equipo-detail'),
    
    # URLs para Materiales de Pintura
    path('pintura/', views.MaterialPinturaListView.as_view(), name='material-pintura-list'),
    path('pintura/<int:pk>/', views.MaterialPinturaDetailView.as_view(), name='material-pintura-detail'),
    
    # URLs para Materiales de Diseño
    path('diseno/', views.MaterialDisenoListView.as_view(), name='material-diseno-list'),
    path('diseno/<int:pk>/', views.MaterialDisenoDetailView.as_view(), name='material-diseno-detail'),
    
    # URLs para Productos Terminados
    path('productos/', views.ProductoTerminadoListView.as_view(), name='producto-terminado-list'),
    path('productos/<int:pk>/', views.ProductoTerminadoDetailView.as_view(), name='producto-terminado-detail'),
    
    # URLs para Movimientos de Inventario
    path('movements/', views.MovimientoInventarioListView.as_view(), name='movimiento-inventario-list'),
    path('movements/<int:pk>/', views.MovimientoInventarioDetailView.as_view(), name='movimiento-inventario-detail'),
    
    # URLs especiales para alertas y reportes
    path('alerts/', views.stock_alerts, name='stock-alerts'),
    path('report/', views.stock_report, name='stock-report'),
    path('adjust-stock/', views.adjust_stock, name='adjust-stock'),
]
