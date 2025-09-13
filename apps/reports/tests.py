"""
Tests para el sistema de reportes.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Report, ReportTemplate

User = get_user_model()


class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            tenant_id=1
        )
    
    def test_create_report(self):
        report = Report.objects.create(
            tenant_id=1,
            name='Test Report',
            report_type='financial',
            created_by='testuser'
        )
        self.assertEqual(report.name, 'Test Report')
        self.assertEqual(report.report_type, 'financial')
        self.assertEqual(report.status, 'pending')


class ReportAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            tenant_id=1
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_report(self):
        data = {
            'name': 'Test Report',
            'report_type': 'financial',
            'description': 'Test description'
        }
        response = self.client.post('/api/reports/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)
    
    def test_generate_report(self):
        data = {
            'report_type': 'financial',
            'export_format': 'pdf'
        }
        response = self.client.post('/api/reports/generate/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)