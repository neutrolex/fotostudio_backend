"""
URLs para la app de pedidos.
"""

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('search/', views.OrderSearchView.as_view(), name='order-search'),
    path('status/<str:status>/', views.OrderStatusView.as_view(), name='order-status'),
    path('<str:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('<str:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]
