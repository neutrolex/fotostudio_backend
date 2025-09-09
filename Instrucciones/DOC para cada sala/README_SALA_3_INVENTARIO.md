# 🏭 SALA 3: INVENTARIO Y PRODUCCIÓN

## 👥 **EQUIPO RESPONSABLE**
- **Líder**: Desarrollador Senior Backend
- **Miembros**: 2 desarrolladores especializados en operaciones
- **Rol**: Equipo de Operaciones

## 🎯 **OBJETIVOS PRINCIPALES**
- Implementar gestión completa de inventario (7 categorías)
- Desarrollar sistema de órdenes de producción
- Crear gestión de productos terminados
- Implementar sistema de alertas automáticas
- Desarrollar trazabilidad completa de movimientos

## 📋 **MÓDULOS A DESARROLLAR**

### **1. App `inventory` - Gestión de Inventario**
- **7 categorías de materiales**:
    - Varillas y molduras (enmarcado)
    - Pinturas y acabados (enmarcado)
    - Materiales de impresión (minilab)
    - Materiales de recordatorio (escolares)
    - Software y equipos (restauración digital)
    - Materiales de pintura (pintura al óleo)
    - Materiales de diseño (edición gráfica)
    - Control de stock actual y mínimo
    - Alertas automáticas de stock bajo
    - Movimientos de inventario con historial
    - Gestión de mermas y pérdidas

### **2. App `production` - Gestión de Producción**
- Órdenes de producción con detalles
- Control de materiales utilizados
- Registro de mermas por proceso
- Estados de producción (Abierta, En Proceso, Cerrada, Cancelada)
- Trazabilidad desde materia prima hasta producto final
- Cálculo de eficiencia de producción

### **3. App `products` - Productos Terminados**
- Gestión de productos finales
- Estados del producto (En Producción, En Almacén, En Tienda, Vendido)
- Control de ubicación y precios
- Integración con órdenes de producción
- Historial de movimientos

## ✅ **CHECKLIST DE ENTREGABLES**

### **Día 1 - Configuración y Modelos**
- [ ] Configurar estructura de carpetas
- [ ] Crear modelos de inventario (7 tipos)
- [ ] Crear modelo Production con detalles
- [ ] Crear modelo Product (productos terminados)
- [ ] Crear modelo Movement (movimientos de inventario)
- [ ] Configurar migraciones iniciales
- [ ] Tests básicos de modelos

### **Día 2 - Serializers y Validaciones**
- [ ] Serializers para 7 tipos de inventario
- [ ] ProductionSerializer con validaciones
- [ ] ProductSerializer con estados
- [ ] MovementSerializer con historial
- [ ] Validaciones de stock y cantidades
- [ ] Validaciones de mermas
- [ ] Tests unitarios de serializers

### **Día 3 - Views y Endpoints**
- [ ] Views CRUD para inventario (7 tipos)
- [ ] ProductionListCreateView con estados
- [ ] ProductListCreateView con ubicaciones
- [ ] MovementListCreateView con historial
- [ ] AlertView para stock bajo
- [ ] StockView para consultas de stock
- [ ] Tests de views con APITestCase

### **Día 4 - Servicios y Lógica de Negocio**
- [ ] InventoryService para gestión de stock
- [ ] ProductionService para órdenes de producción
- [ ] ProductService para productos terminados
- [ ] MovementService para movimientos
- [ ] AlertService para notificaciones
- [ ] Tests de servicios

### **Día 5 - Integración y Testing**
- [ ] Integrar con sistema de autenticación
- [ ] Integrar con modelos de pedidos
- [ ] Configurar URLs principales
- [ ] Tests de integración completos
- [ ] Tests con Postman
- [ ] Coverage mínimo 90%

### **Día 6 - Documentación**
- [ ] Documentación Swagger/OpenAPI
- [ ] Ejemplos de uso de APIs
- [ ] Guías de instalación
- [ ] README de cada app

### **Día 7 - Presentación**
- [ ] Demo del sistema de inventario
- [ ] Presentación de funcionalidades
- [ ] Entrega de documentación

## 🔧 **ESTRUCTURA DE CARPETAS**

```
apps/inventory/
├── __init__.py
├── models.py              # 7 tipos de inventario
├── serializers.py         # Serializers de inventario
├── views.py              # Views de inventario
├── urls.py               # URLs de inventario
├── admin.py              # Admin de inventario
├── services.py           # InventoryService
├── signals.py            # Signals para alertas
└── tests/

apps/production/
├── __init__.py
├── models.py              # Modelo Production
├── serializers.py         # ProductionSerializer
├── views.py              # Views de producción
├── urls.py               # URLs de producción
├── admin.py              # Admin de producción
├── services.py           # ProductionService
└── tests/

apps/products/
├── __init__.py
├── models.py              # Modelo Product
├── serializers.py         # ProductSerializer
├── views.py              # Views de productos
├── urls.py               # URLs de productos
├── admin.py              # Admin de productos
├── services.py           # ProductService
└── tests/
```

## 📊 **MODELOS DE DATOS**

### **Varilla Model (Ejemplo de Inventario)**
```python
class Varilla(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=20)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.model}"
    
    @property
    def is_low_stock(self):
        return self.stock_actual <= self.stock_minimo
```
## 🌐 **ENDPOINTS A IMPLEMENTAR**

### **Inventario**
```
GET    /api/inventory/varillas/        # Varillas
POST   /api/inventory/varillas/        # Crear varilla
GET    /api/inventory/varillas/{id}/   # Detalle varilla
PUT    /api/inventory/varillas/{id}/   # Actualizar varilla
DELETE /api/inventory/varillas/{id}/   # Eliminar varilla

GET    /api/inventory/pinturas/        # Pinturas y acabados
GET    /api/inventory/impresion/       # Materiales impresión
GET    /api/inventory/recordatorio/    # Materiales recordatorio
GET    /api/inventory/software/        # Software y equipos
GET    /api/inventory/pintura/         # Materiales pintura
GET    /api/inventory/diseno/          # Materiales diseño

GET    /api/inventory/alerts/          # Alertas de stock bajo
GET    /api/inventory/movements/       # Movimientos de inventario
POST   /api/inventory/movements/       # Registrar movimiento
```

### **Producción**
```
GET    /api/production/orders/         # Órdenes de producción
POST   /api/production/orders/         # Crear orden
GET    /api/production/orders/{id}/    # Detalle orden
PUT    /api/production/orders/{id}/    # Actualizar orden
DELETE /api/production/orders/{id}/    # Eliminar orden

POST   /api/production/register/       # Registrar producción
GET    /api/production/efficiency/     # Eficiencia de producción
GET    /api/production/waste/          # Reporte de mermas
```

### **Productos Terminados**
```
GET    /api/products/                  # Productos terminados
POST   /api/products/                  # Crear producto
GET    /api/products/{id}/             # Detalle producto
PUT    /api/products/{id}/             # Actualizar producto
DELETE /api/products/{id}/             # Eliminar producto

GET    /api/products/status/{status}/  # Productos por estado
GET    /api/products/location/{location}/ # Productos por ubicación
POST   /api/products/sell/{id}/        # Marcar como vendido
```

## 🧪 **TESTS OBLIGATORIOS**

### **Tests Unitarios**
- [ ] Tests de modelos de inventario (7 tipos)
- [ ] Tests de modelo Production y ProductionDetail
- [ ] Tests de modelo Product
- [ ] Tests de modelo Movement
- [ ] Tests de serializers con validaciones
- [ ] Tests de views con operaciones CRUD
- [ ] Tests de servicios de negocio

### **Tests de Integración**
- [ ] Tests de flujo completo de producción
- [ ] Tests de movimientos de inventario
- [ ] Tests de alertas automáticas
- [ ] Tests de cálculo de eficiencia
- [ ] Tests de control de stock

### **Cobertura Mínima**
- **90%** en código de producción
- **100%** en lógica de inventario crítica
- **100%** en cálculos de producción

## 📚 **DOCUMENTACIÓN REQUERIDA**

### **Swagger/OpenAPI**
- [ ] Documentación automática de todas las APIs
- [ ] Ejemplos de uso para cada endpoint
- [ ] Esquemas de datos detallados
- [ ] Códigos de error documentados
- [ ] Filtros y búsquedas documentadas

### **Documentación Técnica**
- [ ] README de cada app
- [ ] Guías de instalación
- [ ] Ejemplos de uso
- [ ] Documentación de lógica de negocio

## 🔄 **DEPENDENCIAS**

### **Hacia Otros Equipos**
- **Proporciona**: Modelos de inventario y producción
- **Proporciona**: APIs de gestión de stock
- **Proporciona**: Sistema de alertas
- **Proporciona**: Trazabilidad de movimientos

### **De Otros Equipos**
- **Requiere**: Sistema de autenticación (Sala 1)
- **Requiere**: Modelos de pedidos (Sala 2)
- **Nota**: Depende del trabajo de Sala 1 y Sala 2

## 🚨 **SISTEMA DE ALERTAS**

### **Alertas Automáticas**
- [ ] Stock bajo por material
- [ ] Mermas excesivas en producción
- [ ] Productos sin movimiento
- [ ] Órdenes de producción atrasadas
- [ ] Materiales próximos a vencer

### **Notificaciones**
- [ ] Email automático para alertas críticas
- [ ] Dashboard con alertas visuales
- [ ] API para consultar alertas
- [ ] Sistema de prioridades

## 📊 **MÉTRICAS Y REPORTES**

### **Métricas de Inventario**
- [ ] Valor total del inventario
- [ ] Rotación de materiales
- [ ] Stock promedio por categoría
- [ ] Tiempo de reposición
- [ ] Costo de almacenamiento

### **Métricas de Producción**
- [ ] Eficiencia por proceso
- [ ] Mermas por tipo de material
- [ ] Tiempo promedio de producción
- [ ] Productos terminados por día
- [ ] Costo de producción

## 📞 **CONTACTO Y SOPORTE**

- **Líder del equipo**: [Nombre del líder]
- **Email**: [email@empresa.com]
- **Slack**: #sala-3-inventario
- **Horario de trabajo**: 8:00 AM - 6:00 PM

## 🎯 **CRITERIOS DE ACEPTACIÓN**

### **Funcionalidad**
- [ ] CRUD completo de inventario (7 tipos)
- [ ] Sistema de producción funcional
- [ ] Gestión de productos terminados
- [ ] Alertas automáticas operativas
- [ ] Trazabilidad completa de movimientos

### **Calidad**
- [ ] Tests con 90% coverage
- [ ] Documentación completa
- [ ] Código limpio y documentado
- [ ] APIs documentadas con Swagger
- [ ] Lógica de negocio validada

### **Performance**
- [ ] Consultas de stock rápidas (< 200ms)
- [ ] Alertas en tiempo real
- [ ] Cálculos de eficiencia precisos
- [ ] Queries optimizadas
- [ ] Sistema escalable

---
**Responsable**: Sala 3 - Inventario y Producción
