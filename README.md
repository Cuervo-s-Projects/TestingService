# Pruebas y Tests del Proyecto

Este documento describe las pruebas realizadas sobre los servicios principales del sistema, los cuales se comunican con el frontend mediante solicitudes HTTP (`GET` y `POST`). Las pruebas se ejecutan en entorno local y están automatizadas utilizando **Selenium**. Además, se utiliza **Swagger** para la documentación y validación manual de los servicios.

Cada conjunto de pruebas genera automáticamente una carpeta que contiene los resultados en formato **PDF**, organizados por servicio.

---

## Servicios Probados

### 1. Servicio de Login

**Método utilizado:** `POST`

#### Pruebas realizadas:
- Verificación de autenticación con credenciales válidas e inválidas
- Respuesta ante envío de campos vacíos o con formato incorrecto
- Validación del inicio y cierre de sesión
- Comprobación del manejo de sesiones en el navegador

---

### 2. Servicio de Videos

**Métodos utilizados:** `POST`, `GET`

#### Pruebas realizadas:
- Subida de videos en distintos formatos válidos (ej. MP4)
- Visualización de videos desde el navegador
- Verificación del listado de videos accesibles por el usuario
- Comprobación de restricciones de tamaño y acceso

---

### 3. Servicio de Cuestionarios

**Métodos utilizados:** `POST`, `GET`

#### Pruebas realizadas:
- Subida de nuevos cuestionarios desde el frontend
- Visualización y navegación por las preguntas
- Resolución completa del cuestionario y envío de respuestas
- Validación de campos requeridos y lógica condicional (si aplica)

---

### 4. Servicio de Guardado en Perfil

**Métodos utilizados:** `POST`, `GET`

#### Pruebas realizadas:
- Almacenamiento correcto de respuestas luego de completar un cuestionario
- Recuperación y visualización del historial en el perfil del usuario
- Validación de acceso solo al perfil propio (control de sesión y permisos)

---

## Herramientas utilizadas

- **Selenium**: Automatización de pruebas de interacción desde el navegador
- **Swagger**: Validación y documentación de los servicios HTTP

---

## Generación de Resultados

- Cada ejecución de pruebas crea una carpeta específica por servicio.
- Los resultados de cada prueba se exportan en archivos **PDF**, los cuales incluyen:
  - Escenario probado
  - Pasos realizados
  - Resultado esperado vs. obtenido
  - Capturas de pantalla (si aplica)

---

## Entorno de Pruebas

- Todas las pruebas se ejecutan en entorno **local de desarrollo**
- Los servicios deben estar corriendo antes de iniciar la suite de pruebas
- Se recomienda tener el navegador actualizado y habilitado para la automatización por Selenium

---

