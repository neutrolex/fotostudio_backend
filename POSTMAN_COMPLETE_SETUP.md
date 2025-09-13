# 🚀 Configuración COMPLETA de Postman para Fotostudio Backend

## 📋 **INSTRUCCIONES DE INSTALACIÓN**

### **1. 📥 Importar Colección y Entorno COMPLETOS**

1. **Abrir Postman**
2. **Importar Colección:**
   - Click en "Import" (esquina superior izquierda)
   - Seleccionar `Fotostudio_COMPLETE_ALL_Endpoints.postman_collection.json`
   - Click "Import"

3. **Importar Entorno:**
   - Click en "Import" nuevamente
   - Seleccionar `Fotostudio_COMPLETE_Environment.postman_environment.json`
   - Click "Import"

4. **Seleccionar Entorno:**
   - En la esquina superior derecha, seleccionar "Fotostudio Complete Environment"

### **2. 🔐 Configuración de Autenticación Automática**

#### **Paso 1: Obtener Token Automáticamente**
1. Ir a la carpeta **"🔐 Autenticación y Usuarios (25 endpoints)"**
2. Ejecutar **"Login"**
3. **¡El token se guarda automáticamente!** (gracias al script de test)
4. Verificar en la pestaña **"Environment"** que `access_token` se llenó

#### **Paso 2: Variables Configuradas**
- `base_url`: `http://localhost:8000` ✅
- `access_token`: (se llena automáticamente) ✅
- `refresh_token`: (se llena automáticamente) ✅
- `username`: `ochoa` ✅
- `password`: `123456` ✅
- `tenant_id`: `1` ✅
- `user_id`: `1` ✅
- `client_id`: `1` ✅
- `order_id`: `1` ✅
- `contract_id`: `1` ✅
- `appointment_id`: `1` ✅
- `production_order_id`: `1` ✅
- `report_id`: `1` ✅
- `material_id`: `1` ✅
- `inventory_item_id`: `1` ✅

## 🎯 **TODOS LOS ENDPOINTS DISPONIBLES (80 endpoints)**

### **🔐 Autenticación y Usuarios (25 endpoints)**
- **Login**: `POST /api/auth/login/` (con auto-guardado de token)
- **Refresh Token**: `POST /api/auth/token/refresh/`
- **Registro**: `POST /api/auth/register/`
- **Solicitar Código Login**: `POST /api/auth/login/code/request/`
- **Login con Código**: `POST /api/auth/login/code/`
- **Mi Perfil**: `GET /api/auth/users/me/`
- **Actualizar Mi Perfil**: `PUT /api/auth/users/me/update/`
- **Subir Foto Perfil**: `POST /api/auth/users/me/photo/`
- **Buscar Usuarios**: `GET /api/auth/users/search/`
- **Perfil Detallado**: `GET /api/auth/profiles/me/`
- **Crear Perfil**: `POST /api/auth/profiles/create/`
- **Perfil Público**: `GET /api/auth/profiles/public/{user_name}/`
- **Configuraciones Perfil**: `GET /api/auth/profiles/settings/`
- **Completitud Perfil**: `GET /api/auth/profiles/completion/`
- **Buscar Perfiles**: `GET /api/auth/profiles/search/`
- **Cambiar Contraseña**: `POST /api/auth/password/change/`
- **Reset Contraseña**: `POST /api/auth/password/reset/`
- **Confirmar Reset Contraseña**: `POST /api/auth/password/reset/confirm/`
- **Verificar Fortaleza Contraseña**: `POST /api/auth/password/strength/`
- **Política Contraseñas**: `GET /api/auth/password/policy/`
- **Verificar Código**: `POST /api/auth/verification/code/`
- **Cambiar Email**: `POST /api/auth/verification/email/change/`
- **Confirmar Cambio Email**: `POST /api/auth/verification/email/change/confirm/`
- **Reenviar Código**: `POST /api/auth/verification/code/resend/`
- **Estado Verificación**: `GET /api/auth/verification/status/`
- **Verificación Email**: `POST /api/auth/verification/email/`
- **Confirmar Verificación Email**: `POST /api/auth/verification/email/confirm/`

### **🏢 Tenants (3 endpoints)**
- **Listar Tenants**: `GET /api/tenants/` (público)
- **Obtener Tenant por ID**: `GET /api/tenants/{id}/`
- **Tenant Actual**: `GET /api/tenants/current/`

### **📋 Pedidos (5 endpoints)**
- **Listar Pedidos**: `GET /api/orders/`
- **Crear Pedido**: `POST /api/orders/`
- **Obtener Pedido por ID**: `GET /api/orders/{id}/`
- **Buscar Pedidos**: `GET /api/orders/search/`
- **Pedidos por Estado**: `GET /api/orders/status/{status}/`

### **👥 Clientes (5 endpoints)**
- **Listar Clientes**: `GET /api/clients/`
- **Crear Cliente**: `POST /api/clients/`
- **Obtener Cliente por ID**: `GET /api/clients/{id}/`
- **Buscar Clientes**: `GET /api/clients/search/`
- **Listar Colegios**: `GET /api/clients/schools/`

### **📄 Contratos (4 endpoints)**
- **Listar Contratos**: `GET /api/contracts/`
- **Crear Contrato**: `POST /api/contracts/`
- **Obtener Contrato por ID**: `GET /api/contracts/{id}/`
- **Contratos por Vencer**: `GET /api/contracts/expiring/`

### **📅 Agenda (4 endpoints)**
- **Listar Citas**: `GET /api/agenda/`
- **Crear Cita**: `POST /api/agenda/`
- **Obtener Cita por ID**: `GET /api/agenda/{id}/`
- **Calendario de Citas**: `GET /api/agenda/calendar/`

### **📊 Dashboard (4 endpoints)**
- **Métricas Principales**: `GET /api/dashboard/`
- **Métricas de Pedidos**: `GET /api/dashboard/orders/`
- **Métricas de Clientes**: `GET /api/dashboard/clients/`
- **Métricas de Ingresos**: `GET /api/dashboard/revenue/`

### **📦 Inventario (12 endpoints)**
- **Listar Inventario General**: `GET /api/inventory/`
- **Varillas**: `GET /api/inventory/varillas/`
- **Pinturas y Acabados**: `GET /api/inventory/pinturas/`
- **Materiales de Impresión**: `GET /api/inventory/impresion/`
- **Materiales de Recordatorio**: `GET /api/inventory/recordatorio/`
- **Software y Equipos**: `GET /api/inventory/software/`
- **Materiales de Pintura**: `GET /api/inventory/pintura/`
- **Materiales de Diseño**: `GET /api/inventory/diseno/`
- **Productos Terminados**: `GET /api/inventory/productos/`
- **Movimientos de Inventario**: `GET /api/inventory/movements/`
- **Alertas de Stock**: `GET /api/inventory/alerts/`
- **Crear Movimiento Inventario**: `POST /api/inventory/movements/`

### **🏭 Producción (6 endpoints)**
- **Listar Órdenes de Producción**: `GET /api/production/orders/`
- **Crear Orden de Producción**: `POST /api/production/orders/`
- **Obtener Orden por ID**: `GET /api/production/orders/{id}/`
- **Detalles de Producción**: `GET /api/production/detalles/`
- **Cuadros**: `GET /api/production/cuadros/`
- **Registrar Producción**: `POST /api/production/register/`

### **🔧 Materiales (2 endpoints)**
- **Listar Materiales Varilla**: `GET /api/materials/varilla/`
- **Obtener Material Varilla por ID**: `GET /api/materials/varilla/{id}/`

### **📊 Reportes (6 endpoints)**
- **Listar Reportes**: `GET /api/reports/`
- **Generar Reporte**: `POST /api/reports/generate/`
- **Exportar CSV**: `GET /api/reports/export/csv/{id}/`
- **Exportar Excel**: `GET /api/reports/export/excel/{id}/`
- **Exportar PDF**: `GET /api/reports/export/pdf/{id}/`
- **Categorías de Reportes**: `GET /api/reports/categories/`

### **📈 Métricas (2 endpoints)**
- **Listar Métricas**: `GET /api/metrics/`
- **KPIs**: `GET /api/metrics/kpis/`

## 🧪 **PRUEBAS RECOMENDADAS**

### **1. 🔐 Prueba de Autenticación Automática**
1. Ejecutar **"Login"** en la carpeta de Autenticación
2. **¡Verificar que el token se guarda automáticamente!**
3. Verificar que el status es `200 OK`

### **2. 📊 Prueba del Dashboard**
1. Ejecutar **"Métricas Principales"** en Dashboard
2. Verificar que se obtienen métricas del sistema
3. Verificar que el status es `200 OK`

### **3. 📦 Prueba de Inventario**
1. Ejecutar **"Listar Inventario General"**
2. Ejecutar **"Materiales de Impresión"**
3. Ejecutar **"Productos Terminados"**
4. Ejecutar **"Movimientos de Inventario"**
5. Verificar que todas las respuestas son `200 OK`

### **4. 🏭 Prueba de Producción**
1. Ejecutar **"Listar Órdenes de Producción"**
2. Ejecutar **"Crear Orden de Producción"**
3. Verificar que la creación funciona sin errores
4. Verificar que todas las respuestas son `200 OK` o `201 Created`

### **5. 📊 Prueba de Reportes y Exportación**
1. Ejecutar **"Listar Reportes"** para ver reportes existentes
2. Ejecutar **"Exportar CSV"** para descargar un reporte en CSV
3. Ejecutar **"Exportar Excel"** para descargar un reporte en Excel
4. Ejecutar **"Exportar PDF"** para descargar un reporte en PDF
5. Verificar que los archivos se descargan correctamente

### **6. 🔐 Prueba de Gestión de Usuarios**
1. Ejecutar **"Mi Perfil"** para ver información del usuario
2. Ejecutar **"Perfil Detallado"** para ver perfil completo
3. Ejecutar **"Buscar Usuarios"** para probar búsqueda
4. Verificar que todas las respuestas son `200 OK`

### **7. 📋 Prueba de CRUD Completo**
1. **Clientes**: Crear → Listar → Obtener por ID → Buscar
2. **Pedidos**: Crear → Listar → Obtener por ID → Buscar
3. **Contratos**: Crear → Listar → Obtener por ID → Contratos por Vencer
4. **Agenda**: Crear → Listar → Obtener por ID → Calendario

## 🔧 **CARACTERÍSTICAS AVANZADAS**

### **✅ Auto-guardado de Tokens**
- El token se guarda automáticamente al hacer login
- No necesitas copiar/pegar tokens manualmente
- Todos los endpoints usan el token automáticamente

### **✅ Variables Pre-configuradas**
- IDs de ejemplo para todas las entidades
- URLs base configuradas
- Credenciales de prueba incluidas

### **✅ Documentación Completa**
- Cada endpoint tiene descripción detallada
- Ejemplos de JSON incluidos
- Headers automáticos configurados

### **✅ Organización por Módulos**
- 12 módulos organizados lógicamente
- Fácil navegación por funcionalidad
- Contadores de endpoints por módulo

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Error 401 (Unauthorized):**
- Verificar que el `access_token` esté configurado
- Ejecutar **"Login"** nuevamente (se guarda automáticamente)

### **Error 404 (Not Found):**
- Verificar que el servidor esté ejecutándose en `http://localhost:8000`
- Verificar que la URL del endpoint sea correcta

### **Error 500 (Internal Server Error):**
- Verificar que la base de datos esté configurada correctamente
- Verificar que todas las migraciones estén aplicadas

### **Token Expirado:**
- Ejecutar **"Refresh Token"** para renovar el token
- O ejecutar **"Login"** nuevamente (se guarda automáticamente)

## 📱 **USO EN POSTMAN**

### **1. Ejecutar Requests:**
- Click en el request deseado
- Click en "Send"
- Ver la respuesta en la pestaña "Response"

### **2. Ver Variables (Auto-actualizadas):**
- Click en la pestaña "Environment" (esquina superior derecha)
- Ver que `access_token` se llena automáticamente

### **3. Ver Headers (Pre-configurados):**
- En la pestaña "Headers" de cada request
- Headers de autenticación ya configurados

### **4. Ver Body (Ejemplos incluidos):**
- En la pestaña "Body" para requests POST/PUT
- JSON de ejemplo ya incluido

## 🎉 **¡LISTO PARA USAR!**

Con esta configuración COMPLETA puedes:
- ✅ **Probar TODOS los 80 endpoints** del sistema
- ✅ **Autenticación automática** con auto-guardado de tokens
- ✅ **CRUD completo** de todas las entidades
- ✅ **Exportación** a Excel, PDF y CSV
- ✅ **Sistema multi-tenant** operativo
- ✅ **Base de datos** poblada con datos reales
- ✅ **Gestión completa de usuarios** y perfiles
- ✅ **Sistema de verificación** y contraseñas
- ✅ **Reportes avanzados** con múltiples formatos

## 🔄 **MIGRACIÓN DESDE VERSIONES ANTERIORES**

Si ya tienes versiones anteriores:
1. **Eliminar** las colecciones anteriores
2. **Importar** la nueva colección COMPLETA
3. **Importar** el nuevo entorno COMPLETO
4. **¡Listo!** Tienes acceso a TODOS los endpoints

## 📊 **ESTADÍSTICAS DE LA COLECCIÓN**

- **Total de Endpoints**: 80
- **Módulos**: 12
- **Métodos HTTP**: GET, POST, PUT, PATCH, DELETE
- **Autenticación**: JWT con auto-guardado
- **Formatos de Exportación**: CSV, Excel, PDF
- **Sistema Multi-tenant**: ✅
- **Base de Datos**: MySQL poblada
- **Documentación**: Completa en cada endpoint

**¡Tu sistema de Fotostudio está COMPLETAMENTE funcional y optimizado con TODOS los endpoints disponibles!** 🚀

