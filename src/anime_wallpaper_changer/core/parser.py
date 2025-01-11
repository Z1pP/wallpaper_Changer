from abc import ABC, abstractmethod
from typing import Optional, cast
import random

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from anime_wallpaper_changer.core.config import Config
from anime_wallpaper_changer.utils.logger import setup_logger

logger = setup_logger(__name__)


class ParsingError(Exception):
    """Base exception for parsing errors"""

    pass


class AbstractImageParser(ABC):
    """Abstract base class for image parsers"""

    @abstractmethod
    async def get_random_image_url(self) -> str:
        """Get random image URL from the source"""
        pass

    @abstractmethod
    async def download_image(self, url: str, session: ClientSession) -> bytes:
        """Download image from the given URL"""
        pass


class WallpapersCraftParser(AbstractImageParser):
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self._catalog_path: Optional[str] = None

    @property
    def catalog_path(self) -> str:
        """Get current catalog path, initialize if not set"""
        if self._catalog_path is None:
            self._catalog_path = self.config.get_catalog_path()
        return self._catalog_path

    @catalog_path.setter
    def catalog_path(self, value: str) -> None:
        """Set new catalog path"""
        self._catalog_path = value

    async def get_page_content(self, url: str, session: ClientSession) -> str:
        """Fetch and return page content"""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch page: HTTP {response.status}")
                    raise ParsingError(f"Page fetch error: HTTP {response.status}")
                return await response.text()
        except Exception as e:
            logger.error(f"Network error while fetching {url}: {str(e)}")
            raise ParsingError(f"Network error: {str(e)}")

    async def get_random_image_url(self) -> str:
        """Get random wallpaper URL through multi-step parsing"""
        random_page = random.randint(1, self.config.MAX_PAGES)
        catalog_url = f"{self.config.BASE_URL}{self.catalog_path}/page{random_page}"

        async with aiohttp.ClientSession() as session:
            # Fetch preview page
            preview_content = await self.get_page_content(catalog_url, session)
            preview_soup = BeautifulSoup(preview_content, "lxml")

            # Find and select random wallpaper
            wallpaper_links = preview_soup.find_all(class_="wallpapers__link")
            if not wallpaper_links:
                logger.error("No wallpaper links found on page")
                raise ParsingError("No wallpaper links found")

            selected_wallpaper = random.choice(wallpaper_links)
            if not isinstance(selected_wallpaper, Tag):
                raise ParsingError("Invalid wallpaper element type")

            wallpaper_path = selected_wallpaper.get("href")
            if not wallpaper_path:
                raise ParsingError("Failed to get wallpaper page URL")

            # Fetch full image page
            full_page_url = f"{self.config.BASE_URL}{wallpaper_path}"
            full_page_content = await self.get_page_content(full_page_url, session)

            # Extract direct image URL
            full_page_soup = BeautifulSoup(full_page_content, "lxml")
            image_element = full_page_soup.find(class_="wallpaper__image")

            if not image_element or not isinstance(image_element, Tag):
                logger.error("Image element not found")
                raise ParsingError("Failed to locate image element")

            image_url = image_element.get("src")
            if not image_url or not isinstance(image_url, str):
                logger.error("Invalid image URL")
                raise ParsingError("Failed to extract image URL")

            return image_url

    async def download_image(self, url: str, session: ClientSession) -> bytes:
        """Загрузка изображения"""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ParsingError(
                        f"Ошибка загрузки изображения: {response.status}"
                    )
                return await response.read()
        except Exception as e:
            logger.error(f"Ошибка при загрузке изображения {url}: {e}")
            raise ParsingError(f"Ошибка загрузки: {e}")
