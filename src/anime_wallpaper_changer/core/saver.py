from pathlib import Path
from typing import Optional
import aiofiles
from anime_wallpaper_changer.utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageSaver:
    """
    Класс для сохранения изображений на диск.

    Обеспечивает асинхронное сохранение изображений в указанную директорию
    с обработкой ошибок и логированием.
    """

    def __init__(self, output_dir: Path) -> None:
        """
        Инициализация сохранятеля изображений.

        Args:
            output_dir (Path): Директория для сохранения изображений.
                             Будет создана, если не существует.
        """
        self.output_dir: Path = output_dir
        self._ensure_output_dir_exists()

    def _ensure_output_dir_exists(self) -> None:
        """Создает директорию для сохранения, если она не существует."""
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)

    async def save_image(self, image_data: bytes, filename: str) -> Optional[Path]:
        """
        Асинхронное сохранение изображения на диск.

        Args:
            image_data (bytes): Бинарные данные изображения для сохранения
            filename (str): Имя файла для сохраняемого изображения

        Returns:
            Optional[Path]: Путь к сохраненному файлу или None в случае ошибки

        Raises:
            IOError: При ошибках записи файла
            OSError: При системных ошибках работы с файлами
        """
        try:
            image_path = self.output_dir / filename
            async with aiofiles.open(image_path, mode="wb") as file:
                await file.write(image_data)
            logger.info(f"Изображение успешно сохранено: {image_path}")
            return image_path
        except (IOError, OSError) as e:
            logger.error(f"Ошибка при сохранении изображения {filename}: {e}")
            return None
