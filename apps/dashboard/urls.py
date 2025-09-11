"""
URLs para la app de dashboard.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('orders/', views.DashboardOrdersView.as_view(), name='dashboard-orders'),
    path('clients/', views.DashboardClientsView.as_view(), name='dashboard-clients'),
    path('revenue/', views.DashboardRevenueView.as_view(), name='dashboard-revenue'),
]
