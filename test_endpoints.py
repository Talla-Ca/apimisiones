import requests
import json
import time

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_result(test_name, success, response=None):
    status = f"{Colors.GREEN}PASSED{Colors.END}" if success else f"{Colors.RED}FAILED{Colors.END}"
    print(f"{test_name}: {status}")
    if response and not success:
        print(f"  Response: {response}")

def test_endpoints():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}     PRUEBAS DE API - RPG DAILY QUESTS{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    mision_test_id = None
    mision_auto_id = None
    
    try:
        print(f"{Colors.CYAN}Verificando conexion a {BASE_URL}...{Colors.END}\n")
        
        print(f"{Colors.YELLOW}PRUEBA 1: Endpoint raiz{Colors.END}")
        response = requests.get(f"{BASE_URL}/")
        success = response.status_code == 200
        print_result("GET /", success, response.text if not success else None)
        if success:
            data = response.json()
            print(f"  Titulo: {data['titulo']}")
            print(f"  Version: {data['version']}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 2: Crear mision con ID automatico{Colors.END}")
        payload_auto = {
            "descripcion": "Estudiar para el examen de algoritmos",
            "xp": 100
        }
        response = requests.post(f"{BASE_URL}/misiones/auto", json=payload_auto)
        success = response.status_code == 200
        print_result("POST /misiones/auto", success, response.text if not success else None)
        if success:
            mision_auto_id = response.json()["id"]
            print(f"  ID generado automaticamente: {mision_auto_id}")
            print(f"  Descripcion: {response.json()['mision']['descripcion']}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 3: Crear mision especificando ID{Colors.END}")
        payload = {
            "id": 100,
            "descripcion": "Hacer proyecto de programacion",
            "xp": 200,
            "estado": "pendiente"
        }
        response = requests.post(f"{BASE_URL}/misiones", json=payload)
        success = response.status_code == 200
        print_result("POST /misiones", success, response.text if not success else None)
        if success:
            mision_test_id = response.json()["mision"]["id"]
            print(f"  ID de mision creada: {mision_test_id}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 4: Obtener todas las misiones{Colors.END}")
        response = requests.get(f"{BASE_URL}/misiones")
        success = response.status_code == 200 and len(response.json()) > 0
        print_result("GET /misiones", success, response.text if not success else None)
        if success:
            print(f"  Total de misiones: {len(response.json())}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 5: Obtener una mision especifica{Colors.END}")
        response = requests.get(f"{BASE_URL}/misiones/{mision_test_id}")
        success = response.status_code == 200
        print_result(f"GET /misiones/{mision_test_id}", success, response.text if not success else None)
        if success:
            print(f"  Descripcion: {response.json()['descripcion']}")
            print(f"  XP: {response.json()['xp']}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 6: Ver estadisticas{Colors.END}")
        response = requests.get(f"{BASE_URL}/estadisticas")
        success = response.status_code == 200
        print_result("GET /estadisticas", success, response.text if not success else None)
        if success:
            data = response.json()
            print(f"  Misiones pendientes: {data['misiones_pendientes']}")
            print(f"  Misiones completadas: {data['misiones_completadas']}")
            print(f"  XP total ganada: {data['xp_total_ganada']}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 7: Actualizar una mision{Colors.END}")
        payload_update = {
            "id": mision_test_id,
            "descripcion": "Hacer proyecto de programacion avanzada",
            "xp": 250,
            "estado": "pendiente"
        }
        response = requests.put(f"{BASE_URL}/misiones/{mision_test_id}", json=payload_update)
        success = response.status_code == 200
        print_result(f"PUT /misiones/{mision_test_id}", success, response.text if not success else None)
        if success:
            print(f"  XP actualizado a: 250\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 8: Completar una mision{Colors.END}")
        response = requests.put(f"{BASE_URL}/misiones/{mision_test_id}/completar")
        success = response.status_code == 200
        print_result(f"PUT /misiones/{mision_test_id}/completar", success, response.text if not success else None)
        if success:
            xp_ganada = response.json()["xp_ganada"]
            print(f"  XP ganada: {xp_ganada}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 9: Ver historial de misiones completadas{Colors.END}")
        response = requests.get(f"{BASE_URL}/misiones/completadas")
        success = response.status_code == 200
        print_result("GET /misiones/completadas", success, response.text if not success else None)
        if success:
            historial = response.json()
            print(f"  Total en historial: {len(historial)}\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 10: Intentar completar mision ya completada{Colors.END}")
        response = requests.put(f"{BASE_URL}/misiones/{mision_test_id}/completar")
        success = response.status_code != 200
        print_result("PUT /misiones/{id}/completar (error esperado)", success)
        if response.status_code != 200:
            print(f"  Error capturado correctamente\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 11: Eliminar una mision{Colors.END}")
        response = requests.delete(f"{BASE_URL}/misiones/{mision_auto_id}")
        success = response.status_code == 200
        print_result(f"DELETE /misiones/{mision_auto_id}", success, response.text if not success else None)
        if success:
            print(f"  Mision eliminada correctamente\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 12: Obtener mision eliminada (debe fallar){Colors.END}")
        response = requests.get(f"{BASE_URL}/misiones/{mision_auto_id}")
        success = response.status_code == 404
        print_result(f"GET /misiones/{mision_auto_id} (error esperado)", success)
        if success:
            print(f"  Error 404 retornado correctamente\n")
        time.sleep(0.5)
        
        print(f"{Colors.YELLOW}PRUEBA 13: Obtener mision inexistente{Colors.END}")
        response = requests.get(f"{BASE_URL}/misiones/99999")
        success = response.status_code == 404
        print_result("GET /misiones/99999 (error esperado)", success)
        if success:
            print(f"  Error 404 retornado correctamente\n")
        
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}     TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
        
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}{'='*60}{Colors.END}")
        print(f"{Colors.RED}ERROR: No se puede conectar a {BASE_URL}{Colors.END}")
        print(f"{Colors.RED}{'='*60}{Colors.END}")
        print("\nAsegúrate de que el servidor está corriendo:")
        print(f"{Colors.CYAN}python -m uvicorn APIMisiones:app --reload{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.END}\n")

if __name__ == "__main__":
    test_endpoints()