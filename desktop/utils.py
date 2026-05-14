import os
from pathlib import Path

class Assets:
    """Gestor de rutas de assets"""
    
    BASE_DIR = Path(__file__).parent
    ASSETS_DIR = BASE_DIR / "assets"
    STYLES_DIR = ASSETS_DIR / "styles"
    ICONS_DIR = ASSETS_DIR / "icons"
    
    @classmethod
    def get_style_sheet(cls):
        """Carga el archivo de estilos QSS"""
        qss_path = cls.ASSETS_DIR / "styles.qss"
        if qss_path.exists():
            with open(qss_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    @classmethod
    def get_icon(cls, icon_name):
        """Obtiene la ruta completa de un icono"""
        icon_path = cls.ICONS_DIR / f"{icon_name}.png"
        if icon_path.exists():
            return str(icon_path)
        return None


class Colors:
    """Colores para la aplicación"""
    
    PRIMARY = "#00d4ff"      # Cian
    SECONDARY = "#0099cc"    # Azul oscuro
    SUCCESS = "#00ff00"      # Verde
    DANGER = "#ff6b6b"       # Rojo
    WARNING = "#ffff00"      # Amarillo
    TEXT = "#eee"            # Blanco claro
    BG_DARK = "#0f3460"      # Fondo oscuro
    BG_DARKER = "#1a1a2e"    # Fondo más oscuro


class Constants:
    """Constantes de la aplicación"""
    
    API_BASE_URL = "https://apimisiones.onrender.com"
    MAX_MISIONES = 10
    XP_PER_LEVEL = 500
    APP_TITLE = "⚔️ RPG Daily Quests"
    APP_VERSION = "1.0"