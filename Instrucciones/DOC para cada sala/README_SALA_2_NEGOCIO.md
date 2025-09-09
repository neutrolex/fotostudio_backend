# 📋 SALA 2: GESTIÓN DE NEGOCIO

## 👥 **EQUIPO RESPONSABLE**
- **Líder**: Desarrollador Senior Backend
- **Miembros**: 2 desarrolladores especializados en lógica de negocio
- **Rol**: Equipo de Lógica de Negocio

## 🎯 **OBJETIVOS PRINCIPALES**
- Implementar gestión completa de pedidos
- Desarrollar sistema de clientes y colegios
- Crear gestión de contratos
- Implementar agenda de citas
- Desarrollar dashboard con métricas

## 📋 **MÓDULOS A DESARROLLAR**

### **1. App `orders` - Gestión de Pedidos**
- CRUD completo de pedidos
- Estados de pedido (Nuevo, En Producción, Entregado)
- Cálculo automático de tiempos y costos
- Filtrado y búsqueda avanzada
- Integración con inventario y producción

### **2. App `clients` - Gestión de Clientes**
- Clientes particulares y colegios
- Historial completo de pedidos
- Información de contacto y preferencias
- Sistema de búsqueda y filtrado
- Integración con contratos

### **3. App `contracts` - Gestión de Contratos**
- Contratos con colegios
- Términos y condiciones
- Fechas de vigencia
- Integración con clientes y pedidos
- Sistema de renovación

### **4. App `agenda` - Gestión de Agenda**
- Programación de citas
- Gestión de calendario
- Recordatorios automáticos
- Coordinación entre servicios
- Integración con clientes

### **5. App `dashboard` - Dashboard y Métricas**
- Panel de control centralizado
- Métricas en tiempo real
- KPIs principales
- Gráficos interactivos
- Alertas visuales

## ✅ **CHECKLIST DE ENTREGABLES**

### **Día 1 - Configuración y Modelos**
- [ ] Configurar estructura de carpetas
- [ ] Crear modelos Order, Client, School, Contract, Appointment
- [ ] Definir relaciones entre modelos
- [ ] Configurar migraciones iniciales
- [ ] Tests básicos de modelos

### **Día 2 - Serializers y Validaciones**
- [ ] OrderSerializer con validaciones de negocio
- [ ] ClientSerializer y SchoolSerializer
- [ ] ContractSerializer con validaciones de fechas
- [ ] AppointmentSerializer
- [ ] Validaciones de negocio (fechas, montos, estados)
- [ ] Tests unitarios de serializers

### **Día 3 - Views y Endpoints**
- [ ] OrderListCreateView con filtros
- [ ] OrderDetailView con estados
- [ ] ClientListCreateView con búsqueda
- [ ] ContractListCreateView con fechas
- [ ] AppointmentListCreateView con calendario
- [ ] DashboardView con métricas
- [ ] Tests de views con APITestCase

### **Día 4 - Servicios y Lógica de Negocio**
- [ ] OrderService para cálculos y estados
- [ ] ClientService para gestión de clientes
- [ ] ContractService para renovaciones
- [ ] AppointmentService para programación
- [ ] DashboardService para métricas
- [ ] Tests de servicios

### **Día 5 - Integración y Testing**
- [ ] Integrar con sistema de autenticación
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
- [ ] Demo del sistema de gestión
- [ ] Presentación de funcionalidades
- [ ] Entrega de documentación

## 🔧 **ESTRUCTURA DE CARPETAS**

```
apps/orders/
├── __init__.py
├── models.py              # Modelo Order
├── serializers.py         # OrderSerializer
├── views.py              # Views de pedidos
├── urls.py               # URLs de pedidos
├── admin.py              # Admin de pedidos
├── services.py           # OrderService
└── tests/

apps/clients/
├── __init__.py
├── models.py              # Modelos Client, School
├── serializers.py         # ClientSerializer, SchoolSerializer
├── views.py              # Views de clientes
├── urls.py               # URLs de clientes
├── admin.py              # Admin de clientes
├── services.py           # ClientService
└── tests/

apps/contracts/
├── __init__.py
├── models.py              # Modelo Contract
├── serializers.py         # ContractSerializer
├── views.py              # Views de contratos
├── urls.py               # URLs de contratos
├── admin.py              # Admin de contratos
├── services.py           # ContractService
└── tests/

apps/agenda/
├── __init__.py
├── models.py              # Modelo Appointment
├── serializers.py         # AppointmentSerializer
├── views.py              # Views de agenda
├── urls.py               # URLs de agenda
├── admin.py              # Admin de agenda
├── services.py           # AppointmentService
└── tests/

apps/dashboard/
├── __init__.py
├── views.py              # DashboardView
├── urls.py               # URLs de dashboard
├── services.py           # DashboardService
└── tests/
```
## 🌐 **ENDPOINTS A IMPLEMENTAR**

### **Pedidos**
```
GET    /api/orders/            # Listar pedidos
POST   /api/orders/            # Crear pedido
GET    /api/orders/{id}/       # Detalle pedido
PUT    /api/orders/{id}/       # Actualizar pedido
DELETE /api/orders/{id}/       # Eliminar pedido
GET    /api/orders/search/     # Buscar pedidos
GET    /api/orders/status/{status}/ # Pedidos por estado
```

### **Clientes**
```
GET    /api/clients/           # Listar clientes
POST   /api/clients/           # Crear cliente
GET    /api/clients/{id}/      # Detalle cliente
PUT    /api/clients/{id}/      # Actualizar cliente
DELETE /api/clients/{id}/      # Eliminar cliente
GET    /api/clients/search/    # Buscar clientes
GET    /api/clients/schools/   # Listar colegios
```

### **Contratos**
```
GET    /api/contracts/         # Listar contratos
POST   /api/contracts/         # Crear contrato
GET    /api/contracts/{id}/    # Detalle contrato
PUT    /api/contracts/{id}/    # Actualizar contrato
DELETE /api/contracts/{id}/    # Eliminar contrato
GET    /api/contracts/expiring/ # Contratos por vencer
```

### **Agenda**
```
GET    /api/appointments/      # Listar citas
POST   /api/appointments/      # Crear cita
GET    /api/appointments/{id}/ # Detalle cita
PUT    /api/appointments/{id}/ # Actualizar cita
DELETE /api/appointments/{id}/ # Eliminar cita
GET    /api/appointments/calendar/ # Citas por fecha
```

### **Dashboard**
```
GET    /api/dashboard/         # Métricas principales
GET    /api/dashboard/orders/  # Métricas de pedidos
GET    /api/dashboard/clients/ # Métricas de clientes
GET    /api/dashboard/revenue/ # Métricas de ingresos
```

## 🧪 **TESTS OBLIGATORIOS**

### **Tests Unitarios**
- [ ] Tests de modelos Order, Client, School, Contract, Appointment
- [ ] Tests de serializers con validaciones
- [ ] Tests de views con filtros y búsquedas
- [ ] Tests de servicios de negocio
- [ ] Tests de cálculos y métricas

### **Tests de Integración**
- [ ] Tests de flujo completo de pedidos
- [ ] Tests de gestión de clientes
- [ ] Tests de contratos y renovaciones
- [ ] Tests de agenda y citas
- [ ] Tests de dashboard y métricas

### **Cobertura Mínima**
- **90%** en código de producción
- **100%** en lógica de negocio crítica
- **100%** en cálculos y métricas

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
- **Proporciona**: Modelos de negocio (Order, Client, etc.)
- **Proporciona**: APIs de gestión de pedidos
- **Proporciona**: Sistema de clientes y colegios
- **Proporciona**: Dashboard y métricas

### **De Otros Equipos**
- **Requiere**: Sistema de autenticación (Sala 1)
- **Nota**: Depende del trabajo de Sala 1 para autenticación

## 📊 **MÉTRICAS Y KPIs**

### **Dashboard Principal**
- [ ] Total de pedidos por estado
- [ ] Ingresos por servicio
- [ ] Clientes activos vs inactivos
- [ ] Tiempo promedio de entrega
- [ ] Pedidos pendientes
- [ ] Contratos por vencer

### **Gráficos y Visualizaciones**
- [ ] Gráfico de barras para ingresos
- [ ] Gráfico de líneas para tendencias
- [ ] Gráfico de pastel para distribución
- [ ] Tablas dinámicas con filtros
- [ ] Alertas visuales

## 📞 **CONTACTO Y SOPORTE**

- **Líder del equipo**: [Nombre del líder]
- **Email**: [email@empresa.com]
- **Slack**: #sala-2-negocio
- **Horario de trabajo**: 8:00 AM - 6:00 PM

## 🎯 **CRITERIOS DE ACEPTACIÓN**

### **Funcionalidad**
- [ ] CRUD completo de pedidos
- [ ] Gestión de clientes y colegios
- [ ] Sistema de contratos funcional
- [ ] Agenda de citas operativa
- [ ] Dashboard con métricas en tiempo real

### **Calidad**
- [ ] Tests con 90% coverage
- [ ] Documentación completa
- [ ] Código limpio y documentado
- [ ] APIs documentadas con Swagger
- [ ] Lógica de negocio validada

### **Performance**
- [ ] Búsquedas rápidas (< 500ms)
- [ ] Filtros eficientes
- [ ] Paginación en listados
- [ ] Queries optimizadas
- [ ] Dashboard responsivo

---
**Responsable**: Sala 2 - Gestión de Negocio
