import sys
from pathlib import Path
from typing import List, Optional

# Добавляем путь к директории src в PYTHONPATH
src_path = str(Path(__file__).parent.parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QWidget,
    QSlider,
    QVBoxLayout,
)


class StyledLabel(QLabel):
    """Стилизованная метка"""

    def __init__(self, text: str, centered: bool = False) -> None:
        super().__init__(text)
        if centered:
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                font-size: 13px;
                padding: 2px;
            }
        """)


class StyledComboBox(QComboBox):
    """Стилизованный выпадающий список"""

    def __init__(self, items: Optional[List[str]] = None, width: int = 350) -> None:
        super().__init__()
        if items:
            self.addItems(items)
        self.setFixedWidth(width)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QComboBox {
                padding: 5px 15px;
                border: 2px solid #404040;
                border-radius: 12px;
                background-color: #2D2D2D;
                color: white;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7C4DFF;
                margin-right: 10px;
            }
            QComboBox:hover {
                border-color: #7C4DFF;
            }
            QComboBox QAbstractItemView {
                background-color: #2D2D2D;
                border: 2px solid #404040;
                border-radius: 12px;
                selection-background-color: #7C4DFF;
                color: white;
            }
        """)


class PreviewLabel(QLabel):
    """Метка для предпросмотра изображения"""

    def __init__(self) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px solid #404040;
                border-radius: 15px;
                padding: 5px;
                background-color: #2D2D2D;
                color: #808080;
            }
        """)
        self.setText("Здесь появится превью обоев")
        self.setWordWrap(True)


class StyledButton(QPushButton):
    """Стилизованная кнопка"""

    def __init__(self, text: str, width: int = 350, height: int = 40) -> None:
        super().__init__(text)
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 15px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C4DFF, stop:1 #651FFF
                );
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9575FF, stop:1 #7C4DFF
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #651FFF, stop:1 #5E35B1
                );
            }
            QPushButton:disabled {
                background: #404040;
                color: #808080;
            }
        """)


class StyledProgressBar(QProgressBar):
    """Стилизованный прогресс-бар"""

    def __init__(self, width: int = 350, height: int = 25) -> None:
        super().__init__()
        self.setFixedSize(width, height)
        self.setTextVisible(True)
        self.setFormat("%p%")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 12px;
                background-color: #2D2D2D;
                color: white;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #7C4DFF;
                border-radius: 10px;
            }
        """)
        self.hide()


class WindowButton(QPushButton):
    """Кнопка управления окном"""

    def __init__(self, text: str, hover_color: str) -> None:
        super().__init__(text)
        self._hover_color = hover_color
        self.setFixedSize(5, 20)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-radius: 2px;
                background: transparent;
                color: white;
                font-size: 10px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                background: {hover_color};
            }}
        """)


class EffectSlider(QWidget):
    """Слайдер для настройки интенсивности эффекта"""

    def __init__(
        self,
        min_value: float = 0.0,
        max_value: float = 2.0,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Создаем слайдер
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)  # 1.0 по умолчанию
        self.slider.setFixedWidth(150)

        # Значение
        self.value_label = QLabel("1.0")
        self.value_label.setFixedWidth(40)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Настраиваем стили
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #404040;
                height: 4px;
                background: #2D2D2D;
                margin: 2px 0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #7C4DFF;
                border: none;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::handle:horizontal:hover {
                background: #9575FF;
            }
        """)
        self.value_label.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                font-size: 12px;
                padding: 2px;
            }
        """)

        # Добавляем компоненты в layout
        layout.addWidget(self.slider)
        layout.addWidget(self.value_label)

        # Подключаем сигнал
        self.slider.valueChanged.connect(self._update_value)

        # Сохраняем диапазон значений
        self._min_value = min_value
        self._max_value = max_value

    def _update_value(self) -> None:
        """Обновление отображаемого значения"""
        value = self._get_normalized_value()
        self.value_label.setText(f"{value:.1f}")

    def _get_normalized_value(self) -> float:
        """Получение нормализованного значения слайдера"""
        slider_value = self.slider.value()
        range_size = self._max_value - self._min_value
        normalized = self._min_value + (slider_value / 100.0) * range_size
        return normalized

    def get_value(self) -> float:
        """Получение текущего значения"""
        return self._get_normalized_value()

    def set_value(self, value: float) -> None:
        """Установка значения слайдера"""
        normalized = (
            (value - self._min_value) / (self._max_value - self._min_value)
        ) * 100
        self.slider.setValue(int(normalized))


class EffectPanel(QWidget):
    """Панель управления эффектами"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Заголовок
        title = StyledLabel("Эффекты", centered=True)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title)

        # Выбор эффекта
        effect_label = StyledLabel("Выберите эффект:", centered=False)
        layout.addWidget(effect_label)

        self.effect_combo = StyledComboBox(width=300)
        layout.addWidget(self.effect_combo)

        # Настройка интенсивности
        intensity_label = StyledLabel("Интенсивность:", centered=False)
        layout.addWidget(intensity_label)

        self.intensity_slider = EffectSlider()
        layout.addWidget(self.intensity_slider)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.preview_button = StyledButton("👁 Предпросмотр", width=90, height=30)
        self.apply_button = StyledButton("✨ Применить", width=90, height=30)
        self.reset_button = StyledButton("↺ Сбросить", width=90, height=30)

        buttons_layout.addWidget(self.preview_button)
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.addWidget(self.reset_button)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Стилизация
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                border-radius: 10px;
            }
        """)


class TitleBar(QWidget):
    """Панель заголовка окна"""

    def __init__(self, parent: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(40)
        self._window = parent
        self._old_pos: Optional[QPoint] = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 0, 0)
        layout.setSpacing(0)

        # Заголовок
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)

        self.title_label = QLabel("Anime Wallpaper Changer")
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            font-weight: bold;
        """)
        title_layout.addWidget(self.title_label)

        # Подсказки с горячими клавишами
        shortcuts_label = QLabel(
            "[Ctrl+D] Скачать\n[Ctrl+S] Установить\n[Ctrl+O] Папка\n[Esc] Выход"
        )
        shortcuts_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
        """)
        title_layout.addWidget(shortcuts_label)

        layout.addLayout(title_layout)
        layout.addStretch()

        # Кнопки управления окном в отдельном контейнере
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)

        self.minimize_button = WindowButton("─", "#FFB300")
        if isinstance(self._window, QMainWindow):
            self.minimize_button.clicked.connect(self._window.showMinimized)
            self.minimize_button.setToolTip("Свернуть")

        self.close_button = WindowButton("×", "#FF5252")
        if isinstance(self._window, QMainWindow):
            self.close_button.clicked.connect(self._window.close)
            self.close_button.setToolTip("Закрыть [Esc]")

        buttons_layout.addWidget(self.minimize_button)
        buttons_layout.addWidget(self.close_button)
        layout.addWidget(buttons_container)

        self.setStyleSheet("""
            TitleBar {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C4DFF, stop:1 #651FFF
                );
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)

    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: Optional[QMouseEvent]) -> None:
        if (
            event
            and self._old_pos is not None
            and isinstance(self._window, QMainWindow)
        ):
            delta = event.globalPosition().toPoint() - self._old_pos
            self._window.move(self._window.pos() + delta)
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: Optional[QMouseEvent]) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = None
