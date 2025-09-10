from django.db import models

# Create your models here.

class Agenda(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    user_id = models.IntegerField()
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'pendiente'), ('confirmada', 'confirmada'), ('completada', 'completada'), ('cancelada', 'cancelada')], default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'agenda'

    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio}"