"""
Anime Wallpaper Changer - приложение для автоматической смены обоев рабочего стола
"""

__version__ = "0.1.0"

from .core.config import Config
from .core.parser import WallpapersCraftParser, ParsingError
from .core.saver import ImageSaver
from .core.wallpaper import WallpaperSetter
from .ui.main_window import MainWindow

__all__ = [
    "Config",
    "WallpapersCraftParser",
    "ParsingError",
    "ImageSaver",
    "WallpaperSetter",
    "MainWindow",
]
