"""
URLs para la app de materiales.
"""

from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('varilla/', views.MaterialVarillaListView.as_view(), name='material-varilla-list'),
    path('varilla/<int:pk>/', views.MaterialVarillaDetailView.as_view(), name='material-varilla-detail'),
]
