# 📱 RPG Daily Quests - Aplicación Móvil Flutter

Aplicación móvil para gestionar misiones diarias tipo RPG con experiencia y niveles.

## 🚀 Requisitos Previos

- **Flutter SDK**: 3.0.0 o superior
- **Dart SDK**: Incluido con Flutter
- **Android Studio** o **Xcode** (para emuladores)
- **Git** (opcional)

## 📥 Instalación de Flutter

### En Windows:

1. Descarga Flutter desde: https://flutter.dev/docs/get-started/install/windows

2. Extrae en una carpeta (ej: `C:\flutter`)

3. Agrega Flutter al PATH:
   - Abre PowerShell como administrador
   - Ejecuta:
   ```powershell
   $env:Path += ";C:\flutter\bin"
   ```

4. Verifica la instalación:
   ```bash
   flutter --version
   ```

### En macOS:

```bash
brew install flutter
```

### En Linux:

```bash
sudo apt-get install flutter
```

## 🏗️ Configuración del Proyecto

### 1. Clona o descarga el proyecto

```bash
cd c:\Users\tu_usuario\Desktop\DSFD\apimisiones\movil
```

### 2. Obtén las dependencias

```bash
flutter pub get
```

### 3. Verifica que todo esté correcto

```bash
flutter doctor
```

Debería verse algo como:
```
Doctor summary (to see all details, run flutter doctor -v):
[✓] Flutter (Channel stable, 3.x.x)
[✓] Android toolchain
[✓] Xcode (para macOS/iOS)
[✓] VS Code
```

## 📱 Emulación en PC

### Emulador Android (recomendado)

#### Opción 1: Android Studio

1. Abre Android Studio
2. Ve a **Tools → Device Manager → Create Device**
3. Selecciona un dispositivo (ej: Pixel 5)
4. Selecciona una API (ej: API 33)
5. Crea el emulador

#### Opción 2: Línea de comandos

```bash
# Ver emuladores disponibles
emulator -list-avds

# Iniciar emulador (reemplaza PIXEL_5_API_33 con tu emulador)
emulator -avd PIXEL_5_API_33
```

### Emulador iOS (solo macOS)

```bash
# Ver simuladores disponibles
xcrun simctl list devices

# Iniciar simulador
xcrun simctl boot <device-udid>

# O simplemente:
open -a Simulator
```

## ▶️ Ejecución de la App

### Opción 1: Ejecutar en emulador conectado

```bash
flutter run
```

### Opción 2: Ejecutar en dispositivo específico

```bash
# Ver dispositivos conectados
flutter devices

# Ejecutar en dispositivo específico
flutter run -d <device-id>
```

### Opción 3: Ejecutar con más opciones

```bash
# En modo debug
flutter run -d emulator-5554

# En modo release
flutter run -d emulator-5554 --release

# Con logs
flutter run -d emulator-5554 -v
```

## 🔨 Compilar APK (Android)

### APK Debug

```bash
flutter build apk --debug
```

Ubicación: `build/app/outputs/flutter-apk/app-debug.apk`

### APK Release (para distribuir)

```bash
flutter build apk --release
```

Ubicación: `build/app/outputs/flutter-apk/app-release.apk`

### APK Split (optimizado por arquitectura)

```bash
flutter build apk --split-per-abi
```

Ubicación: `build/app/outputs/flutter-apk/app-*.apk`

## 📦 Compilar APK Bundle (Google Play)

```bash
flutter build appbundle --release
```

Ubicación: `build/app/outputs/bundle/release/app-release.aab`

## 🏠 Compilar iOS (solo macOS)

### Simulator

```bash
flutter build ios --simulator
```

### Device

```bash
flutter build ios --release
```

## 🧪 Pruebas

### Ejecutar tests

```bash
flutter test
```

### Test con cobertura

```bash
flutter test --coverage
```

## 📋 Estructura del Proyecto

```
movil/
├── lib/
│   ├── main.dart                    # Punto de entrada
│   ├── config/
│   │   ├── colors.dart              # Colores de la app
│   │   ├── constants.dart           # Constantes (API URL, etc)
│   │   └── themes.dart              # Temas (Material 3)
│   ├── models/
│   │   ├── mision.dart              # Modelo de Misión
│   │   └── estadisticas.dart        # Modelo de Estadísticas
│   ├── services/
│   │   ├── api_service.dart         # Cliente HTTP
│   │   └── mission_service.dart     # Lógica de misiones
│   ├── providers/
│   │   └── mission_provider.dart    # State Management (Provider)
│   ├── screens/
│   │   ├── home_screen.dart         # Pantalla principal
│   │   ├── crear_mision_screen.dart # Crear misión
│   │   └── estadisticas_screen.dart # Ver estadísticas
│   └── widgets/
│       ├── header_widget.dart       # Header con nivel/XP
│       ├── mision_card.dart         # Card de misión
│       └── xp_progress_widget.dart  # Barra de progreso XP
│
├── assets/
│   ├── images/                      # Imágenes (agregar aquí)
│   └── fonts/                       # Fuentes personalizadas
│
├── pubspec.yaml                     # Dependencias
└── README.md                        # Este archivo
```

## 🎨 Personalización

### Cambiar URL de la API

Edita `lib/config/constants.dart`:

```dart
static const String API_BASE_URL = 'https://tu-api.com';
```

### Cambiar colores

Edita `lib/config/colors.dart`:

```dart
static const Color PRIMARY = Color(0xFF00ff00); // Verde en lugar de cian
```

### Cambiar tema

Edita `lib/config/themes.dart` para personalizar Material 3.

## 🐛 Troubleshooting

### "Flutter command not found"

Agrega Flutter al PATH:

```powershell
# Windows PowerShell
$env:Path += ";C:\flutter\bin"
```

### "No device connected"

```bash
# Ver dispositivos
flutter devices

# Si no hay emuladores, créalos en Android Studio
# o inicia uno desde emulator -avd <name>
```

### "Build failed: Gradle error"

```bash
flutter clean
flutter pub get
flutter run
```

### "API connection error"

- Verifica que `API_BASE_URL` en `constants.dart` es correcto
- Comprueba que la API está corriendo en Render
- Prueba con `flutter run -v` para ver logs detallados

### "Emulator is slow"

```bash
# Ejecuta el emulador con aceleración
emulator -avd <name> -accel auto
```

## 📊 Monitoreo de Performance

```bash
# Ver árboles de widgets
flutter run --track-widget-creation

# DevTools (herramienta de debugging)
flutter pub global activate devtools
devtools
```

## 🚀 Despliegue en Google Play

1. Crea una cuenta en [Google Play Console](https://play.google.com/console)

2. Crea una aplicación nueva

3. Sube el `.aab`:
   ```bash
   flutter build appbundle --release
   ```

4. Sube a Google Play Console

5. Rellena la información de la app y publica

## 🍎 Despliegue en Apple App Store (solo macOS)

1. Crea una cuenta en [Apple Developer](https://developer.apple.com/)

2. Configura certificados y provisioning profiles

3. Compila para iOS:
   ```bash
   flutter build ios --release
   ```

4. Abre en Xcode y sube a App Store Connect

## 📚 Documentación Útil

- [Flutter Docs](https://flutter.dev/docs)
- [Dart Language](https://dart.dev/guides)
- [Provider Package](https://pub.dev/packages/provider)
- [HTTP Package](https://pub.dev/packages/http)
- [Material Design 3](https://m3.material.io/)

## 🎯 Características Implementadas

✅ Crear misiones con XP personalizado  
✅ Completar misiones y ganar XP  
✅ Sistema de niveles (500 XP por nivel)  
✅ Historial de misiones completadas  
✅ Estadísticas en tiempo real  
✅ Interfaz tipo RPG con tema cyberpunk  
✅ Provider para state management  
✅ Integración con API REST  
✅ Manejo de errores de red  
✅ Interfaz responsive  

## 📝 Notas

- La app usa **Provider** para gestión de estado (igual que React Context)
- Todas las API calls se hacen en **threads separados** (no bloquea la UI)
- Los **colores y tema** son consistentes con la versión desktop
- La app es **completamente offline-ready** (con algunos ajustes)

## 🤝 Contribuciones

Si encuentras bugs o quieres agregar features, ¡crea un issue o PR!

---

**¿Listo para empezar?** 🎮

```bash
cd movil
flutter run
```