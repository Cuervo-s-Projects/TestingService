# Pruebas y Tests del Proyecto

Este documento describe las pruebas realizadas sobre los servicios principales del sistema, los cuales se comunican con el frontend mediante solicitudes HTTP (`GET` y `POST`). Las pruebas se ejecutan en un entorno **local** y están automatizadas utilizando **Selenium**. **Swagger** se utiliza para la documentación y validación manual de los servicios.

Cada conjunto de pruebas genera automáticamente una carpeta específica que contiene los resultados en formato **PDF**, organizados por servicio y por tipo de prueba.

---

## Servicios Probados

### 1. Servicio de Login

**Método utilizado:** `POST`

#### Descripción:
En el servicio de **Login**, se realiza un test completo de autenticación en el que se valida el inicio de sesión con credenciales válidas e inválidas. Los resultados del test se guardan en una carpeta específica para este servicio.

#### Ejecución de las pruebas:
- Para ejecutar las pruebas de **Login**, simplemente se ejecuta la carpeta de test correspondiente, la cual incluye todas las pruebas automatizadas de este servicio.
- Las pruebas están completamente integradas, por lo que basta con correr una vez la carpeta para validar todas las funcionalidades del login.

---

### 2. Servicio de Videos

**Métodos utilizados:** `POST`, `GET`

#### Descripción:
Para el servicio de **Videos**, existen dos pruebas individuales:
1. **Test de Subida de Video**: Valida que los videos puedan ser subidos correctamente al sistema, comprobando el formato y el tamaño permitido.
2. **Test de Descarga de Video**: Valida que los videos pueden ser descargados correctamente, verificando que el archivo se recupere sin errores.

#### Ejecución de las pruebas:
- Los tests de **Subida de Video** y **Descarga de Video** son independientes y deben ejecutarse por separado.
- Esto permite ejecutar un test a la vez, según lo que se quiera validar, sin necesidad de correr ambas pruebas juntas.
- **Nota**: Cada prueba genera un reporte PDF con los resultados de la ejecución, incluyendo pasos realizados y posibles errores encontrados.

---

### 3. Servicio de Cuestionarios

**Métodos utilizados:** `POST`, `GET`

#### Descripción:
El servicio de **Cuestionarios** se prueba mediante la subida de cuestionarios, la resolución y el envío de respuestas. Se valida el comportamiento tanto para cuestionarios con preguntas cerradas como abiertas.

#### Ejecución de las pruebas:
- Para ejecutar las pruebas de **Cuestionarios**, se puede correr cada uno de los tests de manera individual para validar funcionalidades específicas, como la subida del cuestionario, la resolución de las preguntas y el envío de respuestas.
- Cada test genera su respectiva carpeta con resultados en PDF.

---

### 4. Servicio de Guardado en Perfil

**Métodos utilizados:** `POST`, `GET`

#### Descripción:
El servicio de **Guardado en Perfil** permite que las respuestas de los cuestionarios se guarden correctamente en el perfil del usuario. Se valida la integridad de los datos al ser guardados y recuperados.

#### Ejecución de las pruebas:
- Para probar este servicio, cada test se ejecuta por separado, validando aspectos como la correcta persistencia de las respuestas y el acceso exclusivo al perfil propio.

---

## Herramientas utilizadas

- **Selenium**: Automatización de pruebas de interacción con el navegador.
- **Swagger**: Documentación y validación de los servicios HTTP.

---

## Generación de Resultados

- **Estructura de resultados**: Cada ejecución de prueba crea una carpeta específica para el servicio probado. Cada carpeta contiene un archivo **PDF** con:
  - El escenario probado.
  - Los pasos realizados.
  - El resultado esperado vs. el obtenido.
  - Capturas de pantalla si aplica.
  
---

## Ejecución de las Pruebas

### 1. Ejecutar pruebas de Login
- Navegar a la carpeta de tests correspondiente al servicio **Login**.
- Ejecutar el script de pruebas (ej. `login.test.js`).
- Verificar que todas las pruebas de login se ejecuten correctamente y revisar los reportes generados en PDF.

### 2. Ejecutar pruebas de Videos
- Para ejecutar los tests de **Subida de Video**, navegar a la carpeta `videos/upload` y ejecutar el script de pruebas (ej. `upload.test.js`).
- Para ejecutar los tests de **Descarga de Video**, navegar a la carpeta `videos/download` y ejecutar el script correspondiente (ej. `download.test.js`).
- Cada test genera su reporte en PDF, el cual puede ser consultado después de cada ejecución.

### 3. Ejecutar pruebas de Cuestionarios
- Navegar a la carpeta de tests correspondiente al servicio **Cuestionarios** y ejecutar los scripts individuales para cada escenario de prueba.
- Verificar los reportes generados por cada test en la carpeta respectiva.

### 4. Ejecutar pruebas de Guardado en Perfil
- Al igual que los otros servicios, ejecutar los tests correspondientes a la validación del guardado de respuestas en el perfil.
- Los resultados se guardan en la carpeta específica del servicio.

---

## Entorno de Pruebas

- Las pruebas se ejecutan en un entorno **local de desarrollo**.
- Los servicios deben estar en ejecución antes de iniciar cualquier prueba.
- Se recomienda tener el navegador actualizado y habilitado para la automatización con Selenium.
- **Nota**: Asegúrate de que las configuraciones locales de red permitan la correcta ejecución de los tests.

---

