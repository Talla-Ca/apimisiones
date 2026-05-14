from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title="RPG Daily Quests API (SQLite)",
    description="API de misiones estilo RPG con base de datos SQLite",
    version="1.0"
)

conn = sqlite3.connect("rpg.db", check_same_thread=False)
conn.execute("PRAGMA foreign_keys = ON;") 
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS misiones (
    id INTEGER PRIMARY KEY,
    descripcion TEXT,
    xp INTEGER,
    estado TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mision_id INTEGER,
    descripcion TEXT,
    xp INTEGER,
    fecha_completada DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE
)
""")

conn.commit()


class Mision(BaseModel):
    id: int
    descripcion: str
    xp: int
    estado: str = "pendiente"


class MisionCrear(BaseModel):
    descripcion: str
    xp: int
    estado: str = "pendiente"


@app.get("/", tags=["Health"])
@app.head("/", tags=["Health"])
def root():
    """Endpoint raíz con información de la API - Health check"""
    return {
        "titulo": "RPG Daily Quests API",
        "version": "1.0",
        "descripcion": "API de misiones estilo RPG para estudiantes universitarios",
        "documentacion": "/docs",
        "status": "online"
    }


@app.get("/estadisticas", tags=["Estadisticas"])
def obtener_estadisticas():
    """Obtiene estadísticas de misiones y experiencia"""
    cursor.execute("SELECT COUNT(*) FROM misiones WHERE estado='pendiente'")
    pendientes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM historial")
    completadas = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(xp) FROM historial")
    xp_total = cursor.fetchone()[0] or 0
    
    return {
        "misiones_pendientes": pendientes,
        "misiones_completadas": completadas,
        "xp_total_ganada": xp_total
    }


@app.get("/misiones/completadas", tags=["Misiones"])
def ver_historial():
    """Ver historial de misiones completadas"""
    cursor.execute("SELECT * FROM historial")
    rows = cursor.fetchall()

    return [
        {"id": r[0], "mision_id": r[1], "descripcion": r[2], "xp": r[3], "fecha_completada": r[4]}
        for r in rows
    ]


@app.get("/misiones", tags=["Misiones"])
def get_misiones():
    """Obtener todas las misiones pendientes"""
    cursor.execute("SELECT * FROM misiones")
    rows = cursor.fetchall()

    return [
        {"id": r[0], "descripcion": r[1], "xp": r[2], "estado": r[3], "fecha_creacion": r[4]}
        for r in rows
    ]


@app.get("/misiones/{mision_id}", tags=["Misiones"])
def get_mision(mision_id: int):
    """Obtener una misión específica por su ID"""
    cursor.execute("SELECT * FROM misiones WHERE id=?", (mision_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    return {"id": row[0], "descripcion": row[1], "xp": row[2], "estado": row[3], "fecha_creacion": row[4]}


@app.post("/misiones", tags=["Misiones"])
def crear_mision(mision: Mision):
    """Crear una nueva misión especificando el ID"""
    cursor.execute("SELECT COUNT(*) FROM misiones")
    total = cursor.fetchone()[0]

    if total >= 10:
        raise HTTPException(status_code=400, detail="Máximo 10 misiones activas")

    cursor.execute(
        "INSERT INTO misiones (id, descripcion, xp, estado) VALUES (?, ?, ?, ?)",
        (mision.id, mision.descripcion, mision.xp, mision.estado)
    )
    conn.commit()

    return {"mensaje": "Misión creada", "mision": mision}


@app.post("/misiones/auto", tags=["Misiones"])
def crear_mision_auto(mision: MisionCrear):
    """Crear una nueva misión con ID generado automáticamente"""
    cursor.execute("SELECT MAX(id) FROM misiones")
    max_id = cursor.fetchone()[0]
    nuevo_id = (max_id or 0) + 1
    
    cursor.execute("SELECT COUNT(*) FROM misiones WHERE estado='pendiente'")
    activas = cursor.fetchone()[0]
    
    if activas >= 10:
        raise HTTPException(status_code=400, detail="Máximo 10 misiones activas")
    
    cursor.execute(
        "INSERT INTO misiones (id, descripcion, xp, estado) VALUES (?, ?, ?, ?)",
        (nuevo_id, mision.descripcion, mision.xp, mision.estado)
    )
    conn.commit()
    
    return {
        "mensaje": "Misión creada automáticamente",
        "id": nuevo_id,
        "mision": {"id": nuevo_id, "descripcion": mision.descripcion, "xp": mision.xp, "estado": mision.estado}
    }


@app.put("/misiones/{mision_id}", tags=["Misiones"])
def actualizar_mision(mision_id: int, mision: Mision):
    """Actualizar datos de una misión existente"""
    cursor.execute("SELECT * FROM misiones WHERE id=?", (mision_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    cursor.execute(
        "UPDATE misiones SET descripcion=?, xp=?, estado=? WHERE id=?",
        (mision.descripcion, mision.xp, mision.estado, mision_id)
    )
    conn.commit()

    return {"mensaje": "Misión actualizada", "mision": mision}


@app.put("/misiones/{mision_id}/completar", tags=["Misiones"])
def completar_mision(mision_id: int):
    """Marcar una misión como completada y guardar en historial"""
    cursor.execute("SELECT * FROM misiones WHERE id=?", (mision_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    if row[3] == "completada":
        raise HTTPException(status_code=400, detail="La misión ya fue completada")

    cursor.execute(
        "UPDATE misiones SET estado='completada' WHERE id=?",
        (mision_id,)
    )

    cursor.execute(
        "INSERT INTO historial (mision_id, descripcion, xp) VALUES (?, ?, ?)",
        (row[0], row[1], row[2])
    )

    conn.commit()

    return {
        "mensaje": "Misión completada",
        "xp_ganada": row[2]
    }


@app.delete("/misiones/{mision_id}", tags=["Misiones"])
def eliminar_mision(mision_id: int):
    """Eliminar una misión del sistema"""
    cursor.execute("SELECT * FROM misiones WHERE id=?", (mision_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    cursor.execute("DELETE FROM misiones WHERE id=?", (mision_id,))
    conn.commit()

    return {"mensaje": "Misión eliminada"}