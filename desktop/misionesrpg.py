import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox, QListWidget, QListWidgetItem,
    QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from utils import Assets, Constants
from api_client import ApiClient
from widgets import HeaderPanel

class MisionRPG(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(Constants.APP_TITLE)
        self.setWindowIcon(QIcon(Assets.get_icon("icono_app")))
        self.setGeometry(100, 100, 1200, 700)
        
        # Cargar estilos
        stylesheet = Assets.get_style_sheet()
        self.setStyleSheet(stylesheet)
        
        self.usuario_xp = 0
        self.misiones = []
        self.worker = None
        
        self.inicializar_ui()
        self.verificar_api()
        self.cargar_datos()
    
    def inicializar_ui(self):
        """Crear la interfaz principal"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(10, 10, 10, 10)
        
        # ==================== HEADER ====================
        self.header = HeaderPanel()
        layout_principal.addWidget(self.header)
        
        layout_principal.addSpacing(10)
        
        # ==================== TABS ====================
        self.tabs = QTabWidget()
        
        # TAB 1: MISIONES DISPONIBLES
        tab_misiones = self.crear_tab_misiones()
        self.tabs.addTab(tab_misiones, "📜 MISIONES ACTIVAS")
        
        # TAB 2: CREAR MISIÓN
        tab_crear = self.crear_tab_crear_mision()
        self.tabs.addTab(tab_crear, "➕ NUEVA MISIÓN")
        
        # TAB 3: ESTADÍSTICAS
        tab_stats = self.crear_tab_estadisticas()
        self.tabs.addTab(tab_stats, "📊 ESTADÍSTICAS")
        
        layout_principal.addWidget(self.tabs)
        central_widget.setLayout(layout_principal)
    
    def crear_tab_misiones(self):
        """Tab de misiones disponibles"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("🎯 TUS MISIONES:"))
        
        self.lista_misiones = QListWidget()
        layout.addWidget(self.lista_misiones)
        
        # Botones de acción
        layout_botones = QHBoxLayout()
        
        self.btn_recargar = QPushButton("🔄 RECARGAR MISIONES")
        self.btn_recargar.clicked.connect(self.cargar_misiones)
        
        self.btn_completar = QPushButton("✅ COMPLETAR MISIÓN")
        self.btn_completar.clicked.connect(self.completar_mision)
        
        self.btn_eliminar = QPushButton("🗑️ ELIMINAR MISIÓN")
        self.btn_eliminar.clicked.connect(self.eliminar_mision)
        
        layout_botones.addWidget(self.btn_recargar)
        layout_botones.addWidget(self.btn_completar)
        layout_botones.addWidget(self.btn_eliminar)
        
        layout.addLayout(layout_botones)
        widget.setLayout(layout)
        
        return widget
    
    def crear_tab_crear_mision(self):
        """Tab para crear nuevas misiones"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("📝 DESCRIPCIÓN:"))
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setPlaceholderText("Ej: Estudiar programación...")
        layout.addWidget(self.input_descripcion)
        
        layout.addWidget(QLabel("⚡ EXPERIENCIA (XP):"))
        layout_xp = QHBoxLayout()
        self.spin_xp = QSpinBox()
        self.spin_xp.setMinimum(10)
        self.spin_xp.setMaximum(500)
        self.spin_xp.setValue(100)
        layout_xp.addWidget(self.spin_xp)
        layout_xp.addStretch()
        layout.addLayout(layout_xp)
        
        layout.addSpacing(20)
        
        self.btn_crear = QPushButton("🚀 CREAR MISIÓN")
        self.btn_crear.setObjectName("btnCrear")
        self.btn_crear.setFixedHeight(50)
        self.btn_crear.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.btn_crear.clicked.connect(self.crear_mision)
        layout.addWidget(self.btn_crear)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        return widget
    
    def crear_tab_estadisticas(self):
        """Tab de estadísticas"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("📈 TUS ESTADÍSTICAS:"))
        
        self.label_pendientes = QLabel("📌 Misiones Pendientes: --")
        layout.addWidget(self.label_pendientes)
        
        self.label_completadas = QLabel("✅ Misiones Completadas: --")
        layout.addWidget(self.label_completadas)
        
        self.label_xp_total = QLabel("⚡ XP Total Ganada: --")
        layout.addWidget(self.label_xp_total)
        
        layout.addSpacing(20)
        layout.addWidget(QLabel("📜 HISTORIAL DE MISIONES COMPLETADAS:"))
        
        self.lista_historial = QListWidget()
        layout.addWidget(self.lista_historial)
        
        self.btn_actualizar_stats = QPushButton("🔄 ACTUALIZAR ESTADÍSTICAS")
        self.btn_actualizar_stats.clicked.connect(self.cargar_estadisticas)
        layout.addWidget(self.btn_actualizar_stats)
        
        widget.setLayout(layout)
        
        return widget
    
    def verificar_api(self):
        """Verificar que la API está disponible"""
        self.worker_api = ApiClient.check_api() 
        self.worker_api.finished.connect(lambda: self.mostrar_exito("✅ API conectada correctamente"))
        self.worker_api.error.connect(lambda e: self.mostrar_error(f"⚠️ No se pudo conectar a la API:\n{e}"))
        self.worker_api.start() 
    
    def cargar_datos(self):
        """Cargar datos iniciales"""
        self.cargar_misiones()
        self.cargar_estadisticas()
    
    def cargar_misiones(self):
        """Cargar misiones de la API"""
        self.worker_misiones = ApiClient.get_misiones() 
        self.worker_misiones.finished.connect(self.mostrar_misiones)
        self.worker_misiones.error.connect(self.mostrar_error)
        self.worker_misiones.start() 

    def mostrar_misiones(self, datos):
        """Mostrar misiones en la lista"""
        self.lista_misiones.clear()
        
        # Filtrar para mostrar SOLO las misiones pendientes
        misiones_activas = [m for m in datos if m.get('estado') != 'completada']
        self.misiones = misiones_activas
        
        if not misiones_activas:
            item = QListWidgetItem("🚫 No hay misiones activas. ¡Crea una nueva!")
            self.lista_misiones.addItem(item)
            return
        
        for mision in misiones_activas:
            # Quitamos el texto de estado porque ya sabemos que son las activas
            texto = f"[ID: {mision['id']}] {mision['descripcion']} | ⚡ {mision['xp']} XP"
            item = QListWidgetItem(texto)
            self.lista_misiones.addItem(item)
    
    def crear_mision(self):
        """Crear una nueva misión"""
        descripcion = self.input_descripcion.text().strip()
        xp = self.spin_xp.value()
        
        if not descripcion:
            self.mostrar_error("⚠️ La descripción no puede estar vacía")
            return
        
        # Cambiamos self.worker por self.worker_accion
        self.worker_accion = ApiClient.crear_mision(descripcion, xp)
        self.worker_accion.finished.connect(lambda x: self.mision_creada(x))
        self.worker_accion.error.connect(self.mostrar_error)
        self.worker_accion.start()
    
    def mision_creada(self, datos):
        """Callback después de crear misión"""
        self.mostrar_exito(f"✅ Misión '{datos['mision']['descripcion']}' creada")
        self.input_descripcion.clear()
        self.spin_xp.setValue(100)
        self.cargar_misiones()
    
    def completar_mision(self):
        """Completar misión seleccionada"""
        item_actual = self.lista_misiones.currentItem()
        if not item_actual:
            self.mostrar_error("⚠️ Selecciona una misión primero")
            return
        
        texto = item_actual.text()
        try:
            id_mision = int(texto.split('[ID: ')[1].split(']')[0])
        except:
            self.mostrar_error("⚠️ Error al procesar la misión")
            return
        
        # Cambiamos self.worker por self.worker_accion
        self.worker_accion = ApiClient.completar_mision(id_mision)
        self.worker_accion.finished.connect(lambda x: self.mision_completada(x, id_mision))
        self.worker_accion.error.connect(self.mostrar_error)
        self.worker_accion.start()
    
    def mision_completada(self, datos, id_mision):
        """Callback después de completar misión"""
        xp_ganada = datos.get('xp_ganada', 0)
        self.usuario_xp += xp_ganada
        
        self.header.actualizar_usuario(self.usuario_xp)
        self.mostrar_exito(f"✅ Ganaste {xp_ganada} XP")
        self.cargar_misiones()
        self.cargar_estadisticas()
    
    def eliminar_mision(self):
        """Eliminar misión seleccionada"""
        item_actual = self.lista_misiones.currentItem()
        if not item_actual:
            self.mostrar_error("⚠️ Selecciona una misión primero")
            return
        
        texto = item_actual.text()
        try:
            id_mision = int(texto.split('[ID: ')[1].split(']')[0])
        except:
            self.mostrar_error("⚠️ Error al procesar la misión")
            return
        
        reply = QMessageBox.question(
            self, '¿Eliminar Misión?',
            '¿Estás seguro?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Cambiamos self.worker por self.worker_accion
            self.worker_accion = ApiClient.eliminar_mision(id_mision)
            self.worker_accion.finished.connect(lambda x: self.mision_eliminada())
            self.worker_accion.error.connect(self.mostrar_error)
            self.worker_accion.start()
    
    def mision_eliminada(self):
        """Callback después de eliminar"""
        self.mostrar_exito("🗑️ Misión eliminada")
        self.cargar_misiones()
    
    def cargar_estadisticas(self):
        """Cargar estadísticas"""
        self.worker_stats = ApiClient.obtener_estadisticas() 
        self.worker_stats.finished.connect(self.mostrar_estadisticas)
        self.worker_stats.error.connect(self.mostrar_error)
        self.worker_stats.start() 
        
        self.worker_historial = ApiClient.obtener_historial() 
        self.worker_historial.finished.connect(self.mostrar_historial)
        self.worker_historial.error.connect(self.mostrar_error)
        self.worker_historial.start() 
    
    def mostrar_estadisticas(self, datos):
        """Mostrar estadísticas"""
        pendientes = datos.get('misiones_pendientes', 0)
        completadas = datos.get('misiones_completadas', 0)
        xp_total = datos.get('xp_total_ganada', 0)
        
        self.label_pendientes.setText(f"📌 Misiones Pendientes: {pendientes}")
        self.label_completadas.setText(f"✅ Misiones Completadas: {completadas}")
        self.label_xp_total.setText(f"⚡ XP Total Ganada: {xp_total}")
        
        self.usuario_xp = xp_total
        self.header.actualizar_usuario(xp_total)
    
    def mostrar_historial(self, datos):
        """Mostrar historial"""
        self.lista_historial.clear()
        
        if not datos:
            item = QListWidgetItem("Sin misiones completadas")
            self.lista_historial.addItem(item)
            return
        
        for mision in datos:
            texto = f"✅ {mision['descripcion']} | ⚡ {mision['xp']} XP | 📅 {mision['fecha_completada']}"
            item = QListWidgetItem(texto)
            self.lista_historial.addItem(item)
    
    def mostrar_error(self, mensaje):
        """Mostrar error"""
        QMessageBox.critical(self, "❌ Error", mensaje)
    
    def mostrar_exito(self, mensaje):
        """Mostrar éxito"""
        QMessageBox.information(self, "✅ Éxito", mensaje)
    
    def closeEvent(self, event):
        """Limpiar al cerrar"""
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    ventana = MisionRPG()
    ventana.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()