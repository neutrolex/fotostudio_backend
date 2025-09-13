from django.db import models

# Create your models here.

class Agenda(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, db_column='user_id', default=1)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'pendiente'), ('confirmada', 'confirmada'), ('completada', 'completada'), ('cancelada', 'cancelada')], default='pendiente')
    
    # CAMPOS COMPATIBLES CON FRONTEND
    client = models.CharField(max_length=200, blank=True, null=True, verbose_name="Cliente")
    date = models.DateField(blank=True, null=True, verbose_name="Fecha")
    time = models.TimeField(blank=True, null=True, verbose_name="Hora")
    duration = models.CharField(max_length=50, blank=True, null=True, verbose_name="Duración")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ubicación")
    type = models.CharField(max_length=20, choices=[('reunion', 'Reunión'), ('sesion', 'Sesión'), ('entrega', 'Entrega')], default='sesion', verbose_name="Tipo")
    status = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado'), ('completado', 'Completado'), ('cancelado', 'Cancelado')], default='pendiente', verbose_name="Estado")
    participants = models.PositiveIntegerField(default=0, verbose_name="Participantes")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas")
    tasks = models.JSONField(default=list, blank=True, verbose_name="Tareas")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'agenda'

    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio}"