RPG Daily Quests API

API REST de misiones estilo RPG para estudiantes universitarios.

Instalacion Local

1. Clonar repositorio:
git clone <tu-repo>
cd apimisiones

2. Crear entorno virtual:
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias:
pip install -r requirements.txt

4. Ejecutar:
python -m uvicorn APIMisiones:app --reload

5. Acceder a:
API: http://localhost:8000
Docs: http://localhost:8000/docs

Desplegar en Render

1. Crear cuenta en https://render.com
2. Conectar repositorio de GitHub
3. Crear nuevo servicio web
4. Seleccionar Docker
5. Render usara render.yaml automaticamente
6. La URL se generara automaticamente

Estructura del Proyecto

apimisiones/
  APIMisiones.py          - Archivo principal de la API
  requirements.txt        - Dependencias Python
  Dockerfile              - Configuracion de contenedor
  docker-compose.yml      - Orquestacion local
  render.yaml             - Configuracion para Render
  .gitignore              - Archivos a ignorar en Git
  runtime.txt             - Version de Python
  readme_api.md           - Documentacion de endpoints
  test_endpoints.py       - Script de pruebas
  rpg.db                  - Base de datos SQLite (auto-generada)

Variables de Entorno

Actualmente la API no necesita variables de entorno.

Documentacion

Ver readme_api.md para documentacion completa de endpoints.

Testing

Ejecutar pruebas locales:
python test_endpoints.py

Necesita que la API este corriendo en http://localhost:8000


Integracion con render 

# Guía de Integración - RPG Daily Quests API

Base URL: https://apimisiones.onrender.com

## Documentación Interactiva
https://apimisiones.onrender.com/docs

## Health Check
GET https://apimisiones.onrender.com/

Respuesta esperada:
{
  "titulo": "RPG Daily Quests API",
  "version": "1.0",
  "status": "online"
}

## Crear Misión (Recomendado)
POST https://apimisiones.onrender.com/misiones/auto

Body:
{
  "descripcion": "Tu misión aquí",
  "xp": 100
}

Respuesta:
{
  "mensaje": "Misión creada automáticamente",
  "id": 1,
  "mision": {...}
}

## Obtener Misiones
GET https://apimisiones.onrender.com/misiones

## Completar Misión
PUT https://apimisiones.onrender.com/misiones/{id}/completar

Respuesta:
{
  "mensaje": "Misión completada",
  "xp_ganada": 100
}

## Ver Estadísticas
GET https://apimisiones.onrender.com/estadisticas

Respuesta:
{
  "misiones_pendientes": 3,
  "misiones_completadas": 5,
  "xp_total_ganada": 750
}