"""
Tests para el sistema de métricas.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Metric, KPIDefinition
from django.utils import timezone

User = get_user_model()


class MetricModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            tenant_id=1
        )
    
    def test_create_metric(self):
        metric = Metric.objects.create(
            tenant_id=1,
            name='Test Metric',
            metric_type='financial',
            value=100.50,
            period_start=timezone.now(),
            period_end=timezone.now()
        )
        self.assertEqual(metric.name, 'Test Metric')
        self.assertEqual(metric.value, 100.50)


class MetricAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            tenant_id=1
        )
        self.client.force_authenticate(user=self.user)
    
    def test_dashboard_metrics(self):
        response = self.client.get('/api/metrics/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('financial', response.data)
        self.assertIn('operational', response.data)