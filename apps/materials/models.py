from django.db import models

# Create your models here.

class PinturaAcabado(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'pintura_acabado'

    def __str__(self):
        return self.nombre

class MaterialImpresion(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    especificaciones = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'material_impresion'

    def __str__(self):
        return self.nombre

class MaterialRecordatorio(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'material_recordatorio'

    def __str__(self):
        return self.nombre

class SoftwareEquipo(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'software_equipo'

    def __str__(self):
        return self.nombre

class MaterialPintura(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'material_pintura'

    def __str__(self):
        return self.nombre

class MaterialDiseno(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    especificaciones = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'material_diseno'

    def __str__(self):
        return self.nombre

class ProductoTerminado(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[('disponible', 'disponible'), ('reservado', 'reservado'), ('vendido', 'vendido'), ('devuelto', 'devuelto')], default='disponible')
    fecha_creacion = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'producto_terminado'

    def __str__(self):
        return self.nombre

class MaterialVarilla(models.Model):
    id = models.AutoField(primary_key=True)
    varilla_id = models.IntegerField()
    material_type = models.CharField(max_length=25, choices=[
        ('pintura_acabado', 'pintura_acabado'),
        ('material_impresion', 'material_impresion'),
        ('material_recordatorio', 'material_recordatorio'),
        ('software_equipo', 'software_equipo'),
        ('material_pintura', 'material_pintura'),
        ('material_diseno', 'material_diseno')
    ])
    material_id = models.IntegerField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'material_varilla'