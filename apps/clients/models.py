from django.db import models
from django.contrib.auth.models import User
from apps.tenants.models import Tenant


class Client(models.Model):
    """
    Modelo actualizado para gestionar clientes del estudio fotográfico.
    
    COMPATIBLE CON EL FRONTEND - Campos coinciden exactamente.
    """
    
    CLIENT_TYPE_CHOICES = [
        ('individual', 'Particular'),
        ('school', 'Colegio'),
        ('business', 'Empresa'),
    ]
    
    # ID personalizado para compatibilidad con frontend
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID Cliente")
    
    # Información básica - COMPATIBLE CON FRONTEND
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    contacto = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Contacto"
    )
    tipo = models.CharField(
        max_length=20, 
        choices=CLIENT_TYPE_CHOICES, 
        default='individual',
        verbose_name="Tipo de Cliente"
    )
    
    # Información adicional - COMPATIBLE CON FRONTEND
    direccion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Dirección"
    )
    ie = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Institución Educativa"
    )
    detalles = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Notas Adicionales"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Registro"
    )
    ultimo_pedido = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Último Pedido"
    )
    total_pedidos = models.IntegerField(
        default=0, 
        verbose_name="Total de Pedidos"
    )
    monto_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="Monto Total"
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relaciones
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='clients')
    created_by = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_registro']
        unique_together = ['id', 'tenant']
        db_table = 'client'
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generar ID automático si no se proporciona
            last_client = Client.objects.filter(tenant=self.tenant).order_by('-id').first()
            if last_client and last_client.id.startswith('C'):
                try:
                    last_num = int(last_client.id[1:])
                    self.id = f"C{str(last_num + 1).zfill(3)}"
                except ValueError:
                    self.id = "C001"
            else:
                self.id = "C001"
        super().save(*args, **kwargs)
    
    def update_pedido_stats(self):
        """Actualizar estadísticas de pedidos del cliente."""
        from apps.orders.models import Pedido
        
        pedidos = Pedido.objects.filter(cliente=self.nombre, tenant=self.tenant)
        
        # Actualizar total de pedidos
        self.total_pedidos = pedidos.count()
        
        # Actualizar monto total
        from django.db.models import Sum
        total = pedidos.aggregate(total=Sum('precio'))['total'] or 0
        self.monto_total = total
        
        # Actualizar último pedido
        ultimo = pedidos.order_by('-fechaPedido').first()
        if ultimo:
            self.ultimo_pedido = ultimo.fechaPedido.date()
        
        self.save(update_fields=['total_pedidos', 'monto_total', 'ultimo_pedido'])
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del cliente."""
        return self.nombre