from django.db import models
from django.contrib.auth.models import User
from apps.tenants.models import Tenant


class Pedido(models.Model):
    """
    Modelo actualizado para gestionar pedidos del estudio fotográfico.
    
    COMPATIBLE CON EL FRONTEND - Campos coinciden exactamente.
    """
    
    ESTADO_CHOICES = [
        ('Nuevo', 'Nuevo'),
        ('Producción', 'Producción'),
        ('Entregado', 'Entregado'),
    ]
    
    SERVICIO_CHOICES = [
        ('Impresión Minilab', 'Impresión Minilab'),
        ('Enmarcado', 'Enmarcado'),
        ('Recordatorio Escolar', 'Recordatorio Escolar'),
        ('Retoque Fotográfico', 'Retoque Fotográfico'),
    ]
    
    # ID personalizado para compatibilidad con frontend
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID Pedido")
    
    # Información básica - COMPATIBLE CON FRONTEND
    cliente = models.CharField(max_length=200, verbose_name="Cliente/Colegio")
    servicio = models.CharField(
        max_length=50, 
        choices=SERVICIO_CHOICES, 
        default='Impresión Minilab',
        verbose_name="Tipo de Servicio"
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='Nuevo',
        verbose_name="Estado"
    )
    
    # Campos de detalles - COMPATIBLE CON FRONTEND
    fotografias = models.CharField(
        max_length=200,
        blank=True, 
        null=True, 
        verbose_name="Fotografías Asociadas"
    )
    diseño = models.CharField(
        max_length=200,
        blank=True, 
        null=True, 
        verbose_name="Diseño"
    )
    detalles = models.CharField(
        max_length=200,
        blank=True, 
        null=True, 
        verbose_name="Detalles Adicionales"
    )
    
    # Información de seguimiento
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    # Multi-tenancy
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        verbose_name="Tenant",
        default=1
    )
    
    class Meta:
        managed = True
        db_table = 'pedido'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"
    
    @property
    def numero_pedido(self):
        return f"P{self.id:04d}"
    
    def save(self, *args, **kwargs):
        """Override save para actualizar estadísticas del cliente."""
        super().save(*args, **kwargs)
        
        # Actualizar estadísticas del cliente
        try:
            from apps.clients.models import Client
            client = Client.objects.filter(nombre=self.cliente, tenant=self.tenant).first()
            if client:
                client.update_pedido_stats()
        except Exception:
            # Si hay error, continuar sin actualizar estadísticas
            pass


class Proyecto(models.Model):
    """
    Modelo para gestionar proyectos del estudio fotográfico.
    
    COMPATIBLE CON EL FRONTEND - Campos coinciden exactamente.
    """
    
    ESTADO_CHOICES = [
        ('Planificación', 'Planificación'),
        ('En Progreso', 'En Progreso'),
        ('Revision', 'Revisión'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    TIPO_CHOICES = [
        ('Fotografía Escolar', 'Fotografía Escolar'),
        ('Promoción Escolar', 'Promoción Escolar'),
        ('Evento Social', 'Evento Social'),
        ('Sesión Familiar', 'Sesión Familiar'),
        ('Fotografía Comercial', 'Fotografía Comercial'),
        ('Enmarcado', 'Enmarcado'),
        ('Impresión Digital', 'Impresión Digital'),
        ('Retoque Fotográfico', 'Retoque Fotográfico'),
    ]
    
    # ID personalizado para compatibilidad con frontend
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID Proyecto")
    
    # Información básica - COMPATIBLE CON FRONTEND
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Proyecto")
    cliente = models.CharField(max_length=200, verbose_name="Cliente")
    tipo = models.CharField(
        max_length=50, 
        choices=TIPO_CHOICES, 
        default='Fotografía Escolar',
        verbose_name="Tipo de Proyecto"
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='Planificación',
        verbose_name="Estado"
    )
    
    # Campos de fechas - COMPATIBLE CON FRONTEND
    fechaInicio = models.DateField(verbose_name="Fecha de Inicio")
    fechaEntrega = models.DateField(verbose_name="Fecha de Entrega")
    
    # Campos financieros - COMPATIBLE CON FRONTEND
    presupuesto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Presupuesto"
    )
    
    # Campos de detalles - COMPATIBLE CON FRONTEND
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción"
    )
    
    # Información de seguimiento
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    # Multi-tenancy
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        verbose_name="Tenant",
        default=1
    )
    
    class Meta:
        managed = True
        db_table = 'proyecto'
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Proyecto {self.id} - {self.nombre}"
    
    @property
    def numero_proyecto(self):
        return f"PRJ{self.id:04d}"