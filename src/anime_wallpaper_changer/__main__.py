import argparse
import asyncio
import sys
from pathlib import Path

import aiohttp
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

# Добавляем путь к директории src в PYTHONPATH
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from anime_wallpaper_changer.core.config import Config
from anime_wallpaper_changer.core.parser import ParsingError, WallpapersCraftParser
from anime_wallpaper_changer.core.saver import ImageSaver
from anime_wallpaper_changer.core.wallpaper import WallpaperSetter
from anime_wallpaper_changer.ui.main_window import MainWindow
from anime_wallpaper_changer.utils.logger import setup_logger

logger = setup_logger(__name__)


async def run_cli(args: argparse.Namespace) -> None:
    """Запуск в режиме командной строки"""
    config = Config()
    parser = WallpapersCraftParser(config)
    saver = ImageSaver(config.OUTPUT_DIR)
    wallpaper_setter = WallpaperSetter()

    try:
        # Обновляем путь каталога с учетом аргументов
        parser.catalog_path = config.get_catalog_path(args.category, args.resolution)

        async with aiohttp.ClientSession() as session:
            # Получаем URL случайного изображения
            image_url = await parser.get_random_image_url()
            logger.info(f"Получен URL изображения: {image_url}")

            # Загружаем изображение
            image_data = await parser.download_image(image_url, session)

            # Генерируем имя файла из URL
            filename = image_url.split("/")[-1]

            # Сохраняем изображение
            image_path = await saver.save_image(image_data, filename)

            # Устанавливаем обои
            if wallpaper_setter.set_wallpaper(image_path):
                logger.info("Обои успешно установлены")
            else:
                logger.error("Не удалось установить обои")

    except ParsingError as e:
        logger.error(f"Ошибка парсинга: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")


def run_gui() -> None:
    """Запуск в режиме GUI"""
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()


def main() -> None:
    """Основная функция"""
    parser = argparse.ArgumentParser(description="Anime Wallpaper Changer")
    parser.add_argument(
        "--cli", action="store_true", help="Запуск в режиме командной строки"
    )
    parser.add_argument("--category", help="Категория обоев", default="anime")
    parser.add_argument("--resolution", help="Разрешение обоев", default="1920x1080")

    args = parser.parse_args()

    if args.cli:
        # Запуск в режиме командной строки
        asyncio.run(run_cli(args))
    else:
        # Запуск в режиме GUI
        run_gui()


if __name__ == "__main__":
    main()
