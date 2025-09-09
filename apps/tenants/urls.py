"""
URLs para la app de tenants.
"""

from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    path('', views.TenantListView.as_view(), name='tenant-list'),
    path('<int:pk>/', views.TenantDetailView.as_view(), name='tenant-detail'),
    path('current/', views.current_tenant, name='current-tenant'),
]

