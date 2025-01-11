import asyncio
from pathlib import Path
from typing import Optional

import aiohttp
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QPixmap, QShortcut, QImage
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from anime_wallpaper_changer.core.config import Config
from anime_wallpaper_changer.core.parser import ParsingError, WallpapersCraftParser
from anime_wallpaper_changer.core.saver import ImageSaver
from anime_wallpaper_changer.core.wallpaper import WallpaperSetter
from anime_wallpaper_changer.core.effects import ImageEffect
from anime_wallpaper_changer.ui.components import (
    PreviewLabel,
    StyledButton,
    StyledComboBox,
    StyledLabel,
    StyledProgressBar,
    TitleBar,
    EffectPanel,
)
from anime_wallpaper_changer.ui.styles import style_manager
from anime_wallpaper_changer.utils.constants import CATEGORIES, RESOLUTIONS
from anime_wallpaper_changer.utils.logger import setup_logger

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(800, 600)

        # Инициализация компонентов
        self.config = Config()
        self.parser = WallpapersCraftParser(self.config)
        self.saver = ImageSaver(self.config.OUTPUT_DIR)
        self.wallpaper_setter = WallpaperSetter()
        self.current_wallpaper: Optional[Path] = None

        # Создаем центральный виджет
        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Добавляем TitleBar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Контейнер для контента
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)  # Горизонтальное расположение
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Инициализация левой и правой частей
        self._init_left_panel(content_layout)
        self._init_right_panel(content_layout)

        main_layout.addWidget(content_widget)

        # Применяем стили
        self.setStyleSheet(style_manager.get_styles())

    def _init_left_panel(self, parent_layout: QHBoxLayout) -> None:
        """Инициализация левой панели с превью и кнопками"""
        left_container = QWidget()
        left_container.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(15)

        # Превью
        preview_label = StyledLabel("Предпросмотр:", centered=True)
        left_layout.addWidget(preview_label)

        self.preview_label = PreviewLabel()
        self.preview_label.setFixedSize(350, 200)
        left_layout.addWidget(
            self.preview_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Кнопки под превью
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)

        self.download_button = StyledButton("🔄 Скачать обои", width=200)
        self.download_button.clicked.connect(self.handle_download)
        buttons_layout.addWidget(
            self.download_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.set_wallpaper_button = StyledButton("🖼 Установить как обои", width=200)
        self.set_wallpaper_button.clicked.connect(self.set_wallpaper)
        self.set_wallpaper_button.setEnabled(False)
        buttons_layout.addWidget(
            self.set_wallpaper_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        left_layout.addLayout(buttons_layout)

        # Прогресс и статус
        self.progress_bar = StyledProgressBar(width=300)
        left_layout.addWidget(self.progress_bar)

        self.status_label = StyledLabel("", centered=True)
        left_layout.addWidget(self.status_label)

        parent_layout.addWidget(left_container)

    def _init_right_panel(self, parent_layout: QHBoxLayout) -> None:
        """Инициализация правой панели с настройками и эффектами"""
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(20)

        # Настройки
        settings_container = QWidget()
        settings_container.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setSpacing(10)

        settings_title = StyledLabel("Настройки", centered=True)
        settings_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        settings_layout.addWidget(settings_title)

        # Категория
        category_label = StyledLabel("Категория:", centered=False)
        settings_layout.addWidget(category_label)
        self.category_combo = StyledComboBox(list(CATEGORIES.keys()), width=300)
        settings_layout.addWidget(self.category_combo)

        # Разрешение
        resolution_label = StyledLabel("Разрешение:", centered=False)
        settings_layout.addWidget(resolution_label)
        self.resolution_combo = StyledComboBox(list(RESOLUTIONS.keys()), width=300)
        settings_layout.addWidget(self.resolution_combo)

        right_layout.addWidget(settings_container)

        # Панель эффектов
        self.effect_panel = EffectPanel()
        self.effect_panel.effect_combo.addItems(ImageEffect.get_available_effects())
        self.effect_panel.preview_button.clicked.connect(self._preview_effect)
        self.effect_panel.apply_button.clicked.connect(self._apply_effect)
        self.effect_panel.reset_button.clicked.connect(self._reset_effect)
        self.effect_panel.intensity_slider.slider.valueChanged.connect(
            self._preview_effect
        )
        right_layout.addWidget(self.effect_panel)

        parent_layout.addWidget(right_container)

    def _setup_shortcuts(self) -> None:
        """Настройка горячих клавиш"""
        # Ctrl+D - Скачать новые обои
        download_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        download_shortcut.activated.connect(self.handle_download)
        self.download_button.setToolTip("Скачать новые обои (Ctrl+D)")

        # Ctrl+S - Установить как обои
        set_wallpaper_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        set_wallpaper_shortcut.activated.connect(self.set_wallpaper)
        self.set_wallpaper_button.setToolTip("Установить как обои (Ctrl+S)")

        # Ctrl+O - Выбрать папку
        choose_dir_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        choose_dir_shortcut.activated.connect(self.choose_output_directory)
        self.choose_dir_button.setToolTip("Выбрать папку для сохранения (Ctrl+O)")

        # Esc - Закрыть приложение
        close_shortcut = QShortcut(QKeySequence("Esc"), self)
        close_shortcut.activated.connect(self.close)

    def choose_output_directory(self) -> None:
        """Выбор директории для сохранения изображений"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для сохранения",
            str(self.config.OUTPUT_DIR),
            QFileDialog.Option.ShowDirsOnly,
        )

        if directory:
            new_path = Path(directory)
            self.config.OUTPUT_DIR = new_path
            self.saver = ImageSaver(self.config.OUTPUT_DIR)
            self.output_dir_label.setText(str(new_path))
            logger.info(f"Изменена директория сохранения: {new_path}")

    def on_category_changed(self, category_text: str) -> None:
        """Обработчик изменения категории"""
        self.status_label.setText(f"Выбрана категория: {category_text}")

    def on_resolution_changed(self, resolution_text: str) -> None:
        """Обработчик изменения разрешения"""
        self.status_label.setText(f"Выбрано разрешение: {resolution_text}")

    def update_preview(self) -> None:
        """Обновить превью изображения"""
        if self.current_wallpaper and self.current_wallpaper.exists():
            pixmap = QPixmap(str(self.current_wallpaper))
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.preview_label.setPixmap(scaled_pixmap)

    def set_wallpaper(self) -> None:
        """Установка текущего изображения как обоев"""
        if not self.current_wallpaper:
            self.status_label.setText("❌ Сначала скачайте изображение")
            return

        # Применяем эффект перед установкой
        effect_name = self.effect_panel.effect_combo.currentText()
        intensity = self.effect_panel.intensity_slider.get_value()

        result = ImageEffect.apply_effect(
            self.current_wallpaper,
            effect_name,
            intensity,
            output_path=self.current_wallpaper,
        )

        if result:
            if self.wallpaper_setter.set_wallpaper(self.current_wallpaper):
                self.status_label.setText("✅ Обои успешно установлены")
            else:
                self.status_label.setText("❌ Не удалось установить обои")
        else:
            self.status_label.setText(
                "❌ Ошибка при применении эффекта перед установкой"
            )

    def handle_download(self) -> None:
        """Обработчик нажатия кнопки скачивания"""
        if not self.download_button.isEnabled():
            return
        asyncio.create_task(self._start_download())

    async def _start_download(self) -> None:
        """Асинхронная загрузка обоев"""
        self.download_button.setEnabled(False)
        self.set_wallpaper_button.setEnabled(False)
        self.progress_bar.show()
        self.status_label.setText("⏳ Загрузка...")

        try:
            category = self.category_combo.currentText()
            resolution = self.resolution_combo.currentText()

            async with aiohttp.ClientSession() as session:
                # Обновляем путь каталога
                self.parser.catalog_path = self.config.get_catalog_path(
                    CATEGORIES[category], RESOLUTIONS[resolution]
                )

                # Получаем URL изображения
                self.status_label.setText("🔍 Получение ссылки на изображение...")
                image_url = await self.parser.get_random_image_url()
                self.progress_bar.setValue(30)

                if not image_url:
                    raise ParsingError("Не удалось получить URL изображения")

                # Загружаем изображение
                self.status_label.setText("📥 Загрузка изображения...")
                image_data = await self.parser.download_image(image_url, session)
                self.progress_bar.setValue(60)

                # Сохраняем изображение
                self.status_label.setText("💾 Сохранение изображения...")
                filename = image_url.split("/")[-1]
                self.current_wallpaper = await self.saver.save_image(
                    image_data, filename
                )
                self.progress_bar.setValue(90)

                if not self.current_wallpaper:
                    raise ParsingError("Не удалось сохранить изображение")

                self.update_preview()
                self.progress_bar.setValue(100)
                self.set_wallpaper_button.setEnabled(True)
                self.status_label.setText("✨ Загрузка завершена")

        except Exception as e:
            logger.error(f"Ошибка при загрузке: {e}")
            self.status_label.setText(f"❌ Ошибка: {str(e)}")
        finally:
            self.download_button.setEnabled(True)
            QTimer.singleShot(2000, self.progress_bar.hide)

    def apply_theme(self) -> None:
        """Применение текущей темы"""
        self.setStyleSheet(style_manager.get_styles())

    def _preview_effect(self) -> None:
        """Предпросмотр эффекта"""
        if not self.current_wallpaper:
            self.status_label.setText("❌ Сначала скачайте изображение")
            return

        effect_name = self.effect_panel.effect_combo.currentText()
        intensity = self.effect_panel.intensity_slider.get_value()

        preview_data = ImageEffect.preview_effect(
            self.current_wallpaper, effect_name, intensity
        )

        if preview_data:
            # Создаем QImage из байтов
            image = QImage.fromData(preview_data)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                self.preview_label.setPixmap(
                    pixmap.scaled(
                        self.preview_label.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                self.status_label.setText("✨ Предпросмотр эффекта применен")
            else:
                self.status_label.setText("❌ Ошибка при создании превью")
        else:
            self.status_label.setText("❌ Ошибка при применении эффекта")

    def _apply_effect(self) -> None:
        """Применение эффекта"""
        if not self.current_wallpaper:
            self.status_label.setText("❌ Сначала скачайте изображение")
            return

        effect_name = self.effect_panel.effect_combo.currentText()
        intensity = self.effect_panel.intensity_slider.get_value()

        result = ImageEffect.apply_effect(
            self.current_wallpaper, effect_name, intensity
        )

        if result:
            self.status_label.setText("✅ Эффект успешно применен")
            # Обновляем превью
            self.update_preview()
        else:
            self.status_label.setText("❌ Ошибка при применении эффекта")

    def _reset_effect(self) -> None:
        """Сброс эффектов"""
        if not self.current_wallpaper:
            self.status_label.setText("❌ Сначала скачайте изображение")
            return

        # Просто обновляем превью исходного изображения
        self.update_preview()
        self.status_label.setText("↺ Эффекты сброшены")
