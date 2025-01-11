from pathlib import Path
import platform
import os
import ctypes
import subprocess
from typing import Optional

from anime_wallpaper_changer.utils.logger import setup_logger

logger = setup_logger(__name__)


class WallpaperSetter:
    """
    Класс для управления обоями рабочего стола.

    Поддерживает установку обоев на различных операционных системах
    и окружениях рабочего стола.
    """

    @staticmethod
    def set_wallpaper(image_path: Path) -> bool:
        """
        Установка изображения в качестве обоев рабочего стола.

        Args:
            image_path (Path): Путь к файлу изображения для установки

        Returns:
            bool: True в случае успешной установки, False при возникновении ошибки

        Raises:
            OSError: При проблемах с доступом к файлу
            ValueError: При некорректном пути к файлу
        """
        try:
            if not image_path.exists():
                logger.error(f"Файл не существует: {image_path}")
                return False

            system = platform.system().lower()
            abs_path = str(image_path.absolute())

            wallpaper_setters = {
                "windows": WallpaperSetter._set_windows_wallpaper,
                "linux": WallpaperSetter._set_linux_wallpaper,
            }

            if system not in wallpaper_setters:
                logger.warning(f"Неподдерживаемая операционная система: {system}")
                return False

            return wallpaper_setters[system](abs_path)

        except Exception as e:
            logger.error(f"Критическая ошибка при установке обоев: {str(e)}")
            return False

    @staticmethod
    def _set_windows_wallpaper(abs_path: str) -> bool:
        """
        Установка обоев в системе Windows.

        Args:
            abs_path (str): Абсолютный путь к файлу изображения

        Returns:
            bool: Результат установки обоев
        """
        try:
            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDCHANGE = 0x02

            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                abs_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
            )

            if result:
                logger.info("Обои успешно установлены в Windows")
                return True
            else:
                logger.error("Не удалось установить обои в Windows")
                return False

        except Exception as e:
            logger.error(f"Ошибка при установке обоев в Windows: {str(e)}")
            return False

    @staticmethod
    def _set_linux_wallpaper(abs_path: str) -> bool:
        """Установка обоев в Linux"""
        try:
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

            if "gnome" in desktop or "unity" in desktop:
                return WallpaperSetter._set_gnome_wallpaper(abs_path)
            elif "kde" in desktop:
                return WallpaperSetter._set_kde_wallpaper(abs_path)
            elif "xfce" in desktop:
                return WallpaperSetter._set_xfce_wallpaper(abs_path)
            else:
                logger.warning(f"Неподдерживаемое окружение рабочего стола: {desktop}")
                return False

        except Exception as e:
            logger.error(f"Ошибка при установке обоев в Linux: {e}")
            return False

    @staticmethod
    def _set_gnome_wallpaper(abs_path: str) -> bool:
        """Установка обоев в GNOME/Unity"""
        try:
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    "picture-uri",
                    f"file://{abs_path}",
                ]
            )
            logger.info("Обои успешно установлены в GNOME/Unity")
            return True
        except Exception as e:
            logger.error(f"Ошибка при установке обоев в GNOME/Unity: {e}")
            return False

    @staticmethod
    def _set_kde_wallpaper(abs_path: str) -> bool:
        """Установка обоев в KDE Plasma"""
        try:
            script = (
                "var allDesktops = desktops();"
                "for (i=0; i<allDesktops.length; i++) {"
                f"    d = allDesktops[i]; d.wallpaperPlugin = 'org.kde.image';"
                f"    d.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');"
                f"    d.writeConfig('Image', 'file://{abs_path}')"
                "}"
            )
            subprocess.run(
                [
                    "qdbus",
                    "org.kde.plasmashell",
                    "/PlasmaShell",
                    "org.kde.PlasmaShell.evaluateScript",
                    script,
                ]
            )
            logger.info("Обои успешно установлены в KDE Plasma")
            return True
        except Exception as e:
            logger.error(f"Ошибка при установке обоев в KDE Plasma: {e}")
            return False

    @staticmethod
    def _set_xfce_wallpaper(abs_path: str) -> bool:
        """Установка обоев в XFCE"""
        try:
            subprocess.run(
                [
                    "xfconf-query",
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor0/workspace0/last-image",
                    "-s",
                    abs_path,
                ]
            )
            logger.info("Обои успешно установлены в XFCE")
            return True
        except Exception as e:
            logger.error(f"Ошибка при установке обоев в XFCE: {e}")
            return False
