# Modelo de Datos — Task Monitoring Auth Service

Este documento describe el **modelo de datos** utilizado por el servicio **Task Monitoring Auth Service**, responsable de la **autenticación y autorización** de usuarios humanos y clientes máquina.

El diseño del modelo está orientado a:

- Separar claramente autenticación humana y autenticación de sistemas
- Facilitar el control de acceso por roles y permisos
- Permitir una futura integración con otros servicios backend (por ejemplo, el sistema de monitoreo de tareas)

---

## 🧠 Enfoque del modelo de datos

El sistema maneja **dos tipos de identidades**, con responsabilidades y mecanismos de autenticación distintos:

1. **Usuarios humanos** → autenticación mediante **JWT**
2. **Clientes máquina** (integraciones) → autenticación mediante **API Keys**

Esta separación es **intencional** y responde a buenas prácticas de diseño de sistemas seguros.

---

## 🧑 Entidad `User`

Representa a los **usuarios humanos** que acceden al sistema, como administradores o usuarios finales.

### 📌 Campos

- id (int, PK)

- email (string, requerido, único): correo utilizado para autenticación

- hashed_password (string, requerido): contraseña hasheada

- role (enum): ADMIN | USER

- is_active (boolean): indica si el usuario está habilitado

- created_at (datetime ISO)

- updated_at (datetime ISO)

### 🔐 Consideraciones de seguridad

- Las contraseñas **nunca** se almacenan en texto plano.
- Se utiliza hashing seguro (por ejemplo, bcrypt).
- El campo `is_active` permite revocar acceso sin eliminar registros.
- El control de acceso se basa en **roles (RBAC)** simples y claros.

---

## 🤖 Entidad `Client`

Representa a **clientes máquina** o sistemas externos que se autentican sin intervención humana  
(por ejemplo, simuladores o servicios automatizados).

### 📌 Campos


- id (int, PK)

- name (string, requerido): nombre descriptivo del cliente

- api_key_hash (string, requerido): hash de la API Key

- scopes (string / lista, requerido): permisos asignados al cliente
Ejemplo: tasks:create,tasks:close

- is_active (boolean): indica si la API Key está habilitada

- created_at (datetime ISO)

- updated_at (datetime ISO)


### 🔐 Consideraciones de seguridad

- Las API Keys **no se almacenan en texto plano**.
- Se almacena únicamente el hash de la clave.
- El campo `is_active` permite revocar el acceso inmediatamente.
- Los permisos se gestionan mediante **scopes**.

---

## 🔑 Scopes (permisos de clientes máquina)

Los **scopes** definen qué acciones puede realizar un cliente máquina.

### 📌 Ejemplos de scopes

```
tasks:create

tasks:read

tasks:close

tasks:report
```

## 📌 Implementación actual
- Los scopes se almacenan como una cadena delimitada o estructura simple.

- En versiones futuras podrían normalizarse o gestionarse en una tabla separada.

## 🔗 Relación con otros servicios
Este servicio está diseñado para integrarse con otros sistemas backend.

Ejemplo de integración futura:

## Task Monitoring Auth Service

- Emite tokens JWT

- Valida API Keys

- Define roles y scopes

## Automated Task Monitoring System

- Protege endpoints usando JWT o API Keys

- Confía en este servicio para la autenticación y autorización

Esta separación permite una arquitectura modular y escalable.

---

## 🧩 Diagrama lógico simplificado

```
┌────────────┐        JWT          ┌──────────────────────┐
│   User     │ ────────────────▶  │  Protected Endpoints │
└────────────┘                     └──────────────────────┘
      ▲
      │
      │ API Key
      │
┌────────────┐
│   Client   │
└────────────┘

 ```
## 🧑 Entidad: User
Usuarios humanos autenticados mediante JWT, con control de acceso por roles (RBAC).
## 🔐 Reglas de negocio

Solo usuarios ADMIN pueden:

- listar usuarios

- cambiar roles

- administrar clientes máquina

Usuarios USER solo acceden a endpoints permitidos

## 🤖 Entidad: Client (Machine Client)
Clientes máquina que se autentican mediante API Key, sin login humano.

## 🔐 Reglas de negocio

- Las API Keys nunca se almacenan en texto plano

- Si is_active = false, la key queda invalidada

- El acceso se controla por scopes, no por roles

---

No existen relaciones directas entre User y Client, ya que representan tipos de identidad distintos.

---
## 🔗 Relación entre entidades
| Origen   | Relación | Destino   | Tipo      |
| -------- | -------- | --------- | --------- |
| `User`   | —        | `Client`  | ❌ Ninguna |
| `User`   | Auth     | Endpoints | JWT       |
| `Client` | Auth     | Endpoints | API Key   |

📌 Decisión de diseño:
Separar User y Client evita mezclar modelos de seguridad humana y automática.

---

## 🚫 Elementos fuera de alcance
De forma intencional, este modelo no incluye:

- Refresh tokens

- Gestión de sesiones

- Logs de auditoría

- Autenticación multifactor (MFA)

- Proveedores OAuth externos

- Gestión avanzada de permisos (ABAC)

Estas decisiones permiten mantener el modelo simple y enfocado en los objetivos del proyecto.

---

## 📝 Notas finales
Este modelo de datos fue diseñado con fines educativos y de portafolio, priorizando:

- Claridad

- Buenas prácticas de seguridad

- Separación de responsabilidades

- Facilidad de integración futura

El modelo es extensible y puede evolucionar hacia escenarios más complejos si el proyecto lo requiere.
