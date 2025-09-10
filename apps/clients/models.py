from django.db import models

# Create your models here.

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    name = models.CharField(max_length=150)
    client_type = models.CharField(max_length=10, choices=[('persona', 'persona'), ('empresa', 'empresa'), ('otro', 'otro')], default='persona')
    contact = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    additional_details = models.TextField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'cliente'

    def __str__(self):
        return self.name