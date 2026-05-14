import requests
import http 
from PyQt6.QtCore import QThread, pyqtSignal
from utils import Constants


class ApiWorker(QThread):
    """Worker thread para llamadas a la API sin bloquear la UI"""
    
    finished = pyqtSignal(object) 
    error = pyqtSignal(str)
    
    def __init__(self, method, endpoint, data=None):
        super().__init__()
        self.method = method
        self.endpoint = endpoint
        self.data = data
    
    def run(self):
        try:
            url = f'{Constants.API_BASE_URL}{self.endpoint}'
            
            if self.method == 'GET':
                response = requests.get(url, timeout=10)
            elif self.method == 'POST':
                response = requests.post(url, json=self.data, timeout=10)
            elif self.method == 'PUT':
                response = requests.put(url, json=self.data, timeout=10)
            elif self.method == 'DELETE':
                response = requests.delete(url, timeout=10)
            elif self.method == 'HEAD':
                response = requests.head(url, timeout=10)
            else:
                raise ValueError(f"Método HTTP no soportado: {self.method}")
            
            if response.status_code in [200, 201]:
                try:
                    self.finished.emit(response.json())
                except ValueError:
                    self.finished.emit({"status": "success"})
            else:
                # Obtener el nombre legible del HTTP Status
                try:
                    status_name = http.HTTPStatus(response.status_code).phrase
                except ValueError:
                    status_name = "Estado Desconocido"

                try:
                    error_detail = response.json().get("detail", response.text)
                except:
                    # Si Render devuelve HTML, evitar imprimirlo todo
                    if "<html" in response.text.lower():
                        error_detail = "El servidor está reiniciándose o no está disponible (Render)."
                    else:
                        error_detail = response.text
                        
                self.error.emit(f"Error {response.status_code} ({status_name}):\n{error_detail}")

        # Estos except cierran el bloque try principal
        except requests.exceptions.Timeout:
            self.error.emit("⏱️ Timeout: La API tardó demasiado en responder")
        except requests.exceptions.ConnectionError:
            self.error.emit("🔌 Error de conexión: No se puede conectar a la API")
        except Exception as e:
            self.error.emit(f"❌ Error interno: {str(e)}")


class ApiClient:
    """Cliente para interactuar con la API"""
    
    @staticmethod
    def get_misiones():
        """Obtener todas las misiones"""
        worker = ApiWorker('GET', '/misiones')
        return worker
    
    @staticmethod
    def get_mision(mision_id):
        """Obtener una misión específica"""
        worker = ApiWorker('GET', f'/misiones/{mision_id}')
        return worker
    
    @staticmethod
    def crear_mision(descripcion, xp):
        """Crear una nueva misión"""
        data = {"descripcion": descripcion, "xp": xp}
        worker = ApiWorker('POST', '/misiones/auto', data)
        return worker
    
    @staticmethod
    def completar_mision(mision_id):
        """Completar una misión"""
        worker = ApiWorker('PUT', f'/misiones/{mision_id}/completar')
        return worker
    
    @staticmethod
    def eliminar_mision(mision_id):
        """Eliminar una misión"""
        worker = ApiWorker('DELETE', f'/misiones/{mision_id}')
        return worker
    
    @staticmethod
    def obtener_estadisticas():
        """Obtener estadísticas"""
        worker = ApiWorker('GET', '/estadisticas')
        return worker
    
    @staticmethod
    def obtener_historial():
        """Obtener historial de misiones completadas"""
        worker = ApiWorker('GET', '/misiones/completadas')
        return worker
    
    @staticmethod
    def check_api():
        """Verificar que la API está disponible"""
        worker = ApiWorker('HEAD', '/')
        return worker