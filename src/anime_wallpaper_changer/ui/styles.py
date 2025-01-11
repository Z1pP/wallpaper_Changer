import sys
from pathlib import Path
from typing import Dict

# Добавляем путь к директории src в PYTHONPATH
src_path = str(Path(__file__).parent.parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from anime_wallpaper_changer.utils.constants import THEMES, DEFAULT_THEME


class StyleManager:
    """Менеджер стилей приложения"""

    def __init__(self) -> None:
        self._current_theme = DEFAULT_THEME

    @property
    def current_theme(self) -> str:
        return self._current_theme

    @current_theme.setter
    def current_theme(self, theme: str) -> None:
        if theme in THEMES:
            self._current_theme = theme

    @property
    def colors(self) -> Dict[str, str]:
        return THEMES[self.current_theme]

    def get_styles(self) -> str:
        """Получение всех стилей для текущей темы"""
        return "\n".join(
            [
                self._get_main_window_style(),
                self._get_button_style(),
                self._get_label_style(),
                self._get_progress_bar_style(),
                self._get_combo_box_style(),
            ]
        )

    def _get_main_window_style(self) -> str:
        return f"""
            QMainWindow {{
                background-color: {self.colors["background"]};
            }}
            QWidget {{
                background-color: {self.colors["background"]};
                color: {self.colors["text"]};
            }}
            QWidget#central {{
                border-radius: 10px;
                background-color: {self.colors["secondary_background"]};
                margin: 10px;
            }}
        """

    def _get_button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {self.colors["primary"]};
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 200px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.colors["hover"]};
                transform: translateY(-2px);
                transition: all 0.3s ease;
            }}
            QPushButton:pressed {{
                background-color: {self.colors["primary_dark"]};
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background-color: {self.colors["disabled"]};
                color: {self.colors["secondary_text"]};
            }}
            QPushButton#success {{
                background-color: {self.colors["success"]};
            }}
            QPushButton#success:hover {{
                background-color: {self.colors["success"]};
                opacity: 0.9;
            }}
            QPushButton#error {{
                background-color: {self.colors["error"]};
            }}
            QPushButton#error:hover {{
                background-color: {self.colors["error"]};
                opacity: 0.9;
            }}
        """

    def _get_label_style(self) -> str:
        return f"""
            QLabel {{
                font-size: 14px;
                color: {self.colors["text"]};
                background-color: transparent;
                padding: 5px;
                margin: 2px;
            }}
            QLabel#title {{
                font-size: 18px;
                font-weight: bold;
                color: {self.colors["accent"]};
                margin-bottom: 10px;
            }}
            QLabel#status {{
                font-size: 12px;
                color: {self.colors["secondary_text"]};
                font-style: italic;
            }}
        """

    def _get_progress_bar_style(self) -> str:
        return f"""
            QProgressBar {{
                border: none;
                border-radius: 10px;
                text-align: center;
                color: {self.colors["text"]};
                background-color: {self.colors["secondary_background"]};
                font-size: 12px;
                font-weight: bold;
                margin: 10px 5px;
            }}
            QProgressBar::chunk {{
                background-color: {self.colors["accent"]};
                border-radius: 10px;
            }}
        """

    def _get_combo_box_style(self) -> str:
        return f"""
            QComboBox {{
                padding: 8px 15px;
                border: 2px solid {self.colors["border"]};
                border-radius: 20px;
                background-color: {self.colors["secondary_background"]};
                color: {self.colors["text"]};
                font-size: 14px;
                min-width: 200px;
                margin: 5px;
            }}
            QComboBox:hover {{
                border-color: {self.colors["primary"]};
            }}
            QComboBox:focus {{
                border-color: {self.colors["accent"]};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {self.colors["primary"]};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.colors["secondary_background"]};
                color: {self.colors["text"]};
                selection-background-color: {self.colors["primary"]};
                selection-color: white;
                border: 1px solid {self.colors["border"]};
                border-radius: 5px;
            }}
        """

    def get_current_theme(self) -> str:
        """Получение текущей темы в виде строки стилей"""
        return self.get_styles()


# Создаем глобальный экземпляр менеджера стилей
style_manager = StyleManager()
