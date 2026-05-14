import 'package:http/http.dart' as http;
import 'dart:convert';

const String BASE_URL = 'https://apimisiones.onrender.com';

// Crear misión
Future<void> crearMision() async {
  final response = await http.post(
    Uri.parse('$BASE_URL/misiones/auto'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'descripcion': 'Estudiar programación',
      'xp': 100
    }),
  );
  
  if (response.statusCode == 200) {
    print(jsonDecode(response.body));
  }
}

// Obtener misiones
Future<List> obtenerMisiones() async {
  final response = await http.get(
    Uri.parse('$BASE_URL/misiones'),
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  }
  return [];
}