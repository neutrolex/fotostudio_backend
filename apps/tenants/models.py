from django.db import models

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    subdomain = models.CharField(unique=True, max_length=100)
    status = models.CharField(max_length=10, choices=[('active', 'active'), ('inactive', 'inactive'), ('suspended', 'suspended')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Tenant'

    def str(self):
        return self.name