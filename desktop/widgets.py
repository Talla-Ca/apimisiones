from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from utils import Colors, Constants


class UserInfoPanel(QWidget):
    """Panel con información del usuario"""
    
    def __init__(self):
        super().__init__()
        self.nivel = 1
        self.xp_actual = 0
        self.inicializar_ui()
    
    def inicializar_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Nivel
        self.label_nivel = QLabel(f"⭐ NIVEL: {self.nivel}")
        self.label_nivel.setObjectName("subtitulo")
        layout.addWidget(self.label_nivel)
        
        # Barra de XP
        self.barra_xp = QProgressBar()
        self.barra_xp.setMaximum(Constants.XP_PER_LEVEL)
        self.barra_xp.setValue(0)
        self.barra_xp.setFixedHeight(20)
        layout.addWidget(self.barra_xp)
        
        # Texto de XP
        self.label_xp = QLabel(f"XP: 0 / {Constants.XP_PER_LEVEL}")
        self.label_xp.setObjectName("info")
        layout.addWidget(self.label_xp)
        
        self.setLayout(layout)
    
    def actualizar_xp(self, xp_total):
        """Actualizar información de XP"""
        self.xp_actual = xp_total
        self.nivel = (xp_total // Constants.XP_PER_LEVEL) + 1
        xp_en_nivel = xp_total % Constants.XP_PER_LEVEL
        
        self.label_nivel.setText(f"⭐ NIVEL: {self.nivel}")
        self.barra_xp.setMaximum(Constants.XP_PER_LEVEL)
        self.barra_xp.setValue(xp_en_nivel)
        self.label_xp.setText(f"XP: {xp_total} | En este nivel: {xp_en_nivel} / {Constants.XP_PER_LEVEL}")


class HeaderPanel(QWidget):
    """Panel de encabezado con título e información del usuario"""
    
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
    
    def inicializar_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        titulo = QLabel(Constants.APP_TITLE)
        titulo.setObjectName("titulo")
        titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        
        layout.addWidget(titulo)
        layout.addStretch()
        
        # Panel de usuario
        self.user_panel = UserInfoPanel()
        self.user_panel.setFixedWidth(200)
        layout.addWidget(self.user_panel)
        
        self.setLayout(layout)
    
    def actualizar_usuario(self, xp_total):
        """Actualizar información del usuario"""
        self.user_panel.actualizar_xp(xp_total)


class MisionItem(QWidget):
    """Componente para mostrar una misión"""
    
    def __init__(self, mision_data):
        super().__init__()
        self.mision_data = mision_data
        self.inicializar_ui()
    
    def inicializar_ui(self):
        layout = QVBoxLayout()
        
        mision = self.mision_data
        texto = f"[ID: {mision['id']}] {mision['descripcion']} | ⚡ {mision['xp']} XP"
        
        label = QLabel(texto)
        label.setObjectName("info")
        
        if mision.get('estado') == 'completada':
            label.setStyleSheet("color: #00ff00;")
        else:
            label.setStyleSheet("color: #00ffff;")
        
        layout.addWidget(label)
        self.setLayout(layout)