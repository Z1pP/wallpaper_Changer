from dataclasses import dataclass
from pathlib import Path
import platform
import os
from typing import Final, Optional

from anime_wallpaper_changer.utils.constants import DEFAULT_RESOLUTION, DEFAULT_CATEGORY
from anime_wallpaper_changer.utils.logger import setup_logger

logger = setup_logger(__name__)


def get_platform_specific_path(folder_name: str) -> Path:
    """
    Get platform-specific path for saving wallpapers.

    Args:
        folder_name: Name of the folder to create

    Returns:
        Path object with platform-specific wallpaper directory
    """
    system = platform.system().lower()
    user = os.getenv("USER") or os.getenv("USERNAME")

    if system == "windows":
        return Path(os.path.expanduser("~")) / "Pictures" / folder_name
    elif system == "linux":
        return Path(f"/home/{user}/Downloads/{folder_name}")
    return Path(folder_name)


@dataclass
class Config:
    """
    Configuration class for wallpaper parser settings.

    Contains base URL, paths, and download settings for the wallpaper service.
    """

    BASE_URL: Final[str] = "https://wallpaperscraft.ru"
    WALLPAPER_BASE_URL: Final[str] = "https://wallpaperscraft.ru"
    WALLPAPER_CATALOG_PATH: Final[str] = "/catalog"
    WALLPAPER_FOLDER_NAME: Final[str] = "Wallpapers"
    MAX_PAGE_LIMIT: Final[int] = 254
    MAX_CONCURRENT_DOWNLOADS: Final[int] = 3
    DEFAULT_RESOLUTION: Final[str] = DEFAULT_RESOLUTION
    DEFAULT_CATEGORY: Final[str] = DEFAULT_CATEGORY
    MAX_PAGES: Final[int] = 254

    def __init__(self) -> None:
        self._output_dir: Path = get_platform_specific_path(
            folder_name=self.WALLPAPER_FOLDER_NAME
        )

    @property
    def OUTPUT_DIR(self) -> Path:
        """Get the directory path for saving wallpapers."""
        return self._output_dir

    @OUTPUT_DIR.setter
    def OUTPUT_DIR(self, path: Path) -> None:
        """
        Set a new directory path for saving wallpapers.

        Args:
            path: New Path object for wallpaper directory
        """
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        self._output_dir = path

    def get_catalog_path(
        self, category: Optional[str] = None, resolution: Optional[str] = None
    ) -> str:
        """
        Get the full catalog path with category and resolution.

        Args:
            category: Wallpaper category (optional)
            resolution: Wallpaper resolution (optional)

        Returns:
            Full catalog path as a string
        """
        cat = category or self.DEFAULT_CATEGORY
        res = resolution or self.DEFAULT_RESOLUTION
        return f"{self.WALLPAPER_CATALOG_PATH}/{cat}/{res}"
