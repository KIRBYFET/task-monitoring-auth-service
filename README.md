# task-monitoring-auth-service

Servicio backend en **Python** orientado a **autenticación y autorización**, desarrollado con **FastAPI** y **SQLite**.  
Este proyecto provee mecanismos de seguridad para **usuarios humanos** y **clientes máquina**, y está diseñado para integrarse con otros sistemas backend (por ejemplo, un sistema de monitoreo de tareas).

---

## 📌 Estado del proyecto

### 🟡 **En diseño y documentación avanzada**  

Arquitectura y modelo de datos definidos y documentados.  
Implementación prevista como siguiente etapa.

---

## 🧠 Descripción general

Este proyecto implementa un **servicio de autenticación centralizado**, con el objetivo de:

- Autenticar **usuarios humanos** mediante JWT
- Autenticar **clientes máquina** mediante API Keys
- Autorizar accesos usando:
  - **Roles (RBAC)** para usuarios
  - **Scopes** para integraciones
- Servir como proveedor de seguridad para otros servicios backend
- Demostrar buenas prácticas de **seguridad**, **arquitectura desacoplada** y **diseño modular**

El proyecto fue desarrollado con **fines educativos y de portafolio profesional**.

---

## 🎯 Alcance y no-alcance del proyecto

Este servicio fue diseñado con un **alcance claramente delimitado**, priorizando claridad arquitectónica y buenas prácticas, **no como un sistema productivo completo**.

### ✅ Alcance del proyecto

- API REST para autenticación y autorización
- Autenticación de usuarios humanos mediante JWT
- Autenticación de clientes máquina mediante API Keys
- Control de acceso basado en:
  - Roles (`ADMIN`, `USER`)
  - Scopes (permisos granulares)
- Persistencia de usuarios y clientes
- Diseño preparado para integración con otros servicios

### 🚫 No-alcance del proyecto

De forma intencional, este proyecto **no incluye**:

- ❌ OAuth externo (Google, GitHub, etc.)
- ❌ Autenticación multifactor (MFA)
- ❌ Refresh tokens
- ❌ Gestión de sesiones
- ❌ Rate limiting o WAF
- ❌ Auditoría avanzada
- ❌ Despliegue en cloud o contenedores
- ❌ Configuración orientada a producción

Estas decisiones permiten mantener el foco en el objetivo principal del proyecto.

---

## 🧩 Componentes del sistema

### 🔹 API REST (FastAPI)

- Endpoints de autenticación
- Emisión y validación de JWT
- Administración de usuarios y roles (solo ADMIN)
- Administración de clientes máquina y API Keys (solo ADMIN)
- Documentación interactiva con Swagger UI

---

### 🔹 Capa de seguridad

- Hashing seguro de contraseñas
- Generación y validación de JWT
- Validación de API Keys
- Evaluación de roles y scopes
- Dependencias reutilizables para protección de endpoints

---

### 🔹 Persistencia de datos

- Base de datos **SQLite**
- Modelos separados para:
  - Usuarios humanos
  - Clientes máquina
- Enfoque simple y claro para facilitar el análisis y la extensión futura

---

## 📁 Estructura del proyecto

```

```

---

## 📚 Documentación del proyecto
La documentación técnica del proyecto se encuentra en la carpeta Documentación/.

## 🏗️ **[Arquitectura del Sistema](Documentación/Architecture.md)**  
Describe en detalle:

- Visión general de la arquitectura
- Componentes principales
- Flujos de autenticación (JWT y API Key)
- Modelo de autorización (roles y scopes)
- Integración futura con otros servicios
- Limitaciones conocidas

---

## 🗃️ **[Modelo de Datos](Documentación/Data_model.md)**  

Documenta el modelo de datos del servicio, incluyendo:

- Entidad User
- Entidad Client
- Roles y scopes
- Reglas de seguridad
- Decisiones de diseño
- Elementos fuera de alcance

Documento clave para comprender la seguridad y persistencia del sistema.

## 🔗 Integración con otros proyectos

Este servicio está diseñado para integrarse con:
- Automated Task Monitoring System
- Otros servicios backend que requieran autenticación centralizada

En una arquitectura completa:
- Este servicio emite tokens y valida accesos
- Los servicios consumidores confían en él para autorización

---

## 📝 Notas finales
Este proyecto demuestra:

- Diseño de servicios de autenticación
- Separación clara de responsabilidades
- Buenas prácticas de seguridad backend
- Pensamiento arquitectónico modular
- Preparación para sistemas distribuidos

Forma parte de una serie de proyectos de portafolio enfocados en backend, automatización y arquitectura.
