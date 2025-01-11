from typing import Dict, Callable, Optional
from pathlib import Path
import io

from PIL import Image, ImageEnhance, ImageFilter

from anime_wallpaper_changer.utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageEffect:
    """Class for applying effects to images."""

    # Constants
    PREVIEW_SIZE = (600, 300)
    JPEG_QUALITY = 95

    EFFECTS: Dict[str, Callable[[Image.Image, float], Image.Image]] = {
        "Яркость": lambda img, value: ImageEnhance.Brightness(img).enhance(value),
        "Контраст": lambda img, value: ImageEnhance.Contrast(img).enhance(value),
        "Размытие": lambda img, value: img.filter(
            ImageFilter.GaussianBlur(radius=value)
        ),
        "Резкость": lambda img, value: ImageEnhance.Sharpness(img).enhance(value),
        "Насыщенность": lambda img, value: ImageEnhance.Color(img).enhance(value),
    }

    @staticmethod
    def apply_effect(
        image_path: Path,
        effect_name: str,
        intensity: float = 1.0,
        output_path: Optional[Path] = None,
    ) -> Optional[Path]:
        """Apply effect to an image.

        Args:
            image_path: Path to source image
            effect_name: Name of the effect to apply
            intensity: Effect intensity (0.0 - 2.0)
            output_path: Path to save result (if None, overwrites source)

        Returns:
            Path: Path to processed image or None if error occurs
        """
        try:
            if effect_name not in ImageEffect.EFFECTS:
                logger.error(f"Unknown effect: {effect_name}")
                return None

            with Image.open(image_path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")

                effect_func = ImageEffect.EFFECTS[effect_name]
                processed_img = effect_func(img, intensity)

                save_path = output_path or image_path
                processed_img.save(save_path, "JPEG", quality=ImageEffect.JPEG_QUALITY)

                logger.info(f"Effect {effect_name} successfully applied")
                return save_path

        except Exception as e:
            logger.error(f"Error applying effect {effect_name}: {e}")
            return None

    @staticmethod
    def get_available_effects() -> list[str]:
        """Get list of available effects."""
        return list(ImageEffect.EFFECTS.keys())

    @staticmethod
    def preview_effect(
        image_path: Path, effect_name: str, intensity: float = 1.0
    ) -> Optional[bytes]:
        """Create effect preview without saving.

        Args:
            image_path: Path to source image
            effect_name: Name of the effect
            intensity: Effect intensity (0.0 - 2.0)

        Returns:
            bytes: Preview binary data or None if error occurs
        """
        try:
            if effect_name not in ImageEffect.EFFECTS:
                logger.error(f"Unknown effect: {effect_name}")
                return None

            with Image.open(image_path) as img:
                img.thumbnail(ImageEffect.PREVIEW_SIZE, Image.Resampling.LANCZOS)

                if img.mode != "RGB":
                    img = img.convert("RGB")

                effect_func = ImageEffect.EFFECTS[effect_name]
                processed_img = effect_func(img, intensity)

                buffer = io.BytesIO()
                processed_img.save(buffer, format="JPEG")
                return buffer.getvalue()

        except Exception as e:
            logger.error(f"Error creating preview for effect {effect_name}: {e}")
            return None
