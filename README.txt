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
En futuro puedes agregar:
- DATABASE_URL
- SECRET_KEY
- LOG_LEVEL

Documentacion

Ver readme_api.md para documentacion completa de endpoints.

Testing

Ejecutar pruebas locales:
python test_endpoints.py

Necesita que la API este corriendo en http://localhost:8000