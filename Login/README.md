# Test - Login Service

Este módulo ofrece funcionalidades completas de autenticación (signup, login, JWT) y pruebas automatizadas con generación de reportes en PDF. Diseñado para integrarse en proyectos Flask + MongoDB.


## Instalación

```bash
git clone https://github.com/Cuervo-s-Projects/TestingService.git
cd Login
```

## Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```
## Pruebas Automáticas

El módulo incluye pruebas para login, registro, validación de token y roles.

Ejecuta todas las pruebas manuales vía Python:
```python
python report.py
```
Esto generará un reporte PDF en /reports/Report_X.pdf.

## Generación de PDF:

### Cada prueba registra:

- Nombre de prueba

- Resultado (PASSED / FAILED)

- Código de estado HTTP

- Tiempo de ejecución

- Respuesta de la API

