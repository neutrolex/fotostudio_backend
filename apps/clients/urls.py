"""
URLs para la app de clientes.
"""

from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='client-list'),
    path('<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('search/', views.ClientSearchView.as_view(), name='client-search'),
    path('schools/', views.SchoolListView.as_view(), name='school-list'),
]
