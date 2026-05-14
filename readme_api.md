RPG Daily Quests API - Documentacion de Endpoints

Descripcion General
API REST para gestionar misiones estilo RPG en tu vida cotidiana como universitario.

---

ORDEN DE USO RECOMENDADO

1. Verificar que la API funciona
GET /
Obtiene informacion general de la API.

Respuesta (200):
{
  "titulo": "RPG Daily Quests API",
  "version": "1.0",
  "descripcion": "API de misiones estilo RPG para estudiantes universitarios",
  "documentacion": "/docs"
}

---

2. Crear una mision con ID automatico (RECOMENDADO)
POST /misiones/auto
Crea una nueva mision sin necesidad de especificar el ID.

Ejemplo de solicitud:
{
  "descripcion": "Estudiar para el examen de algoritmos",
  "xp": 100
}

Respuesta exitosa (200):
{
  "mensaje": "Mision creada automaticamente",
  "id": 1,
  "mision": {
    "id": 1,
    "descripcion": "Estudiar para el examen de algoritmos",
    "xp": 100,
    "estado": "pendiente"
  }
}

Error si hay 10 misiones activas (400):
{
  "detail": "Maximo 10 misiones activas"
}

---

3. Crear una mision especificando ID
POST /misiones
Crea una nueva mision con ID personalizado.

Ejemplo de solicitud:
{
  "id": 5,
  "descripcion": "Completar tarea de matematicas",
  "xp": 50,
  "estado": "pendiente"
}

Respuesta exitosa (200):
{
  "mensaje": "Mision creada",
  "mision": {
    "id": 5,
    "descripcion": "Completar tarea de matematicas",
    "xp": 50,
    "estado": "pendiente"
  }
}

Error si hay 10 misiones activas (400):
{
  "error": "Maximo 10 misiones activas"
}

---

4. Ver todas las misiones pendientes
GET /misiones
Obtiene la lista de todas las misiones activas.

Respuesta (200):
[
  {
    "id": 1,
    "descripcion": "Estudiar para el examen de algoritmos",
    "xp": 100,
    "estado": "pendiente",
    "fecha_creacion": "2024-01-15 10:30:00"
  },
  {
    "id": 2,
    "descripcion": "Hacer proyecto de programacion",
    "xp": 200,
    "estado": "pendiente",
    "fecha_creacion": "2024-01-15 11:00:00"
  }
]

---

5. Ver una mision especifica
GET /misiones/{mision_id}
Obtiene los detalles de una mision individual.

Parametro:
- mision_id: ID de la mision (entero)

Ejemplo:
GET /misiones/1

Respuesta exitosa (200):
{
  "id": 1,
  "descripcion": "Estudiar para el examen de algoritmos",
  "xp": 100,
  "estado": "pendiente",
  "fecha_creacion": "2024-01-15 10:30:00"
}

Error si no existe (404):
{
  "detail": "Mision no encontrada"
}

---

6. Ver estadisticas generales
GET /estadisticas
Obtiene informacion de misiones completadas y experiencia total ganada.

Respuesta (200):
{
  "misiones_pendientes": 3,
  "misiones_completadas": 5,
  "xp_total_ganada": 750
}

---

7. Actualizar una mision
PUT /misiones/{mision_id}
Modifica los datos de una mision existente.

Parametro:
- mision_id: ID de la mision (entero)

Ejemplo:
PUT /misiones/1

Cuerpo de solicitud:
{
  "id": 1,
  "descripcion": "Estudiar para el examen de algoritmos y estructuras de datos",
  "xp": 150,
  "estado": "pendiente"
}

Respuesta (200):
{
  "mensaje": "Mision actualizada",
  "mision": {
    "id": 1,
    "descripcion": "Estudiar para el examen de algoritmos y estructuras de datos",
    "xp": 150,
    "estado": "pendiente"
  }
}

Error si no existe (404):
{
  "detail": "Mision no encontrada"
}

---

8. Completar una mision
PUT /misiones/{mision_id}/completar
Marca una mision como completada y suma la experiencia al historial.

Parametro:
- mision_id: ID de la mision (entero)

Ejemplo:
PUT /misiones/1/completar

Respuesta exitosa (200):
{
  "mensaje": "Mision completada",
  "xp_ganada": 150
}

Error si ya fue completada (400):
{
  "error": "La mision ya fue completada"
}

Error si no existe (404):
{
  "detail": "Mision no encontrada"
}

---

9. Ver historial de misiones completadas
GET /misiones/completadas
Obtiene todas las misiones completadas con fecha y XP ganada.

Respuesta (200):
[
  {
    "id": 1,
    "mision_id": 1,
    "descripcion": "Estudiar para el examen de algoritmos",
    "xp": 100,
    "fecha_completada": "2024-01-15 15:45:00"
  },
  {
    "id": 2,
    "mision_id": 2,
    "descripcion": "Hacer proyecto de programacion",
    "xp": 200,
    "fecha_completada": "2024-01-15 16:20:00"
  }
]

---

10. Eliminar una mision
DELETE /misiones/{mision_id}
Elimina una mision del sistema.

Parametro:
- mision_id: ID de la mision (entero)

Ejemplo:
DELETE /misiones/1

Respuesta (200):
{
  "mensaje": "Mision eliminada"
}

Error si no existe (404):
{
  "detail": "Mision no encontrada"
}

---

ESTRUCTURA DE DATOS

Modelo Mision:
- id (integer): Identificador unico
- descripcion (string): Descripcion de la mision
- xp (integer): Puntos de experiencia al completar
- estado (string): "pendiente" o "completada"
- fecha_creacion (timestamp): Se genera automaticamente

Modelo MisionCrear:
- descripcion (string): Descripcion de la mision
- xp (integer): Puntos de experiencia al completar
- estado (string): "pendiente" o "completada" (opcional, por defecto "pendiente")

---

LIMITES Y RESTRICCIONES

- Maximo 10 misiones activas simultáneamente
- Las misiones completadas se guardan en el historial
- No se pueden completar misiones que ya fueron completadas
- Al eliminar una mision, se elimina automáticamente su historial asociado
- El ID se genera automaticamente cuando usas POST /misiones/auto

---

CODIGOS DE ESTADO HTTP

- 200: Solicitud exitosa
- 404: Recurso no encontrado
- 400: Solicitud invalida o limite excedido
- 500: Error interno del servidor

---

COMO EJECUTAR LA API

1. Instalar dependencias:
pip install -r requirements.txt

2. Ejecutar la API:
python -m uvicorn APIMisiones:app --reload

3. Acceder a la documentacion:
http://localhost:8000/docs

4. Acceder a la API:
http://localhost:8000

---

COMO USAR CON DOCKER

1. Compilar imagen:
docker build -t rpg-api .

2. Ejecutar contenedor:
docker run -p 8000:8000 -v $(pwd)/rpg.db:/app/rpg.db rpg-api

3. O usar docker-compose:
docker-compose up -d

4. Acceder a:
API: http://localhost:8000
Docs: http://localhost:8000/docs

---

EJEMPLO DE FLUJO COMPLETO

1. GET / -> Verificar que la API funciona
2. POST /misiones/auto -> Crear primera mision
3. POST /misiones/auto -> Crear segunda mision
4. GET /misiones -> Ver todas las misiones
5. GET /estadisticas -> Ver estadisticas
6. PUT /misiones/1/completar -> Completar primera mision
7. GET /misiones/completadas -> Ver historial
8. DELETE /misiones/2 -> Eliminar segunda mision