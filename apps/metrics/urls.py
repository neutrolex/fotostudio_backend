"""
URLs para el sistema de métricas.
"""

from django.urls import path
from .views import (
    MetricsListView, DashboardMetricsView, available_metrics,
    RevenueMetricsView, OrdersMetricsView, ClientsMetricsView,
    InventoryMetricsView, ProductionMetricsView
)

urlpatterns = [
    # Lista general de métricas
    path('', MetricsListView.as_view(), name='metrics-list'),
    
    # Métricas del dashboard
    path('dashboard/', DashboardMetricsView.as_view(), name='dashboard-metrics'),
    
    # Métricas disponibles
    path('available/', available_metrics, name='available-metrics'),

    # Métricas específicas
    path('revenue/', RevenueMetricsView.as_view(), name='metrics-revenue'),
    path('orders/', OrdersMetricsView.as_view(), name='metrics-orders'),
    path('clients/', ClientsMetricsView.as_view(), name='metrics-clients'),
    path('inventory/', InventoryMetricsView.as_view(), name='metrics-inventory'),
    path('production/', ProductionMetricsView.as_view(), name='metrics-production'),
]
