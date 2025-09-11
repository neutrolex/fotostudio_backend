"""
URLs para la app de producción.
"""

from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.ProductionListView.as_view(), name='production-list'),
    path('<int:pk>/', views.ProductionDetailView.as_view(), name='production-detail'),
]
