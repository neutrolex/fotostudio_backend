"""
URLs para la app de contratos.
"""

from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract-list'),
    path('<int:pk>/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('expiring/', views.ContractExpiringView.as_view(), name='contract-expiring'),
]
