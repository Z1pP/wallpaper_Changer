import PyInstaller.__main__
from pathlib import Path

# Получаем абсолютный путь к директории проекта
project_path = Path(__file__).parent
main_path = project_path / "src" / "anime_wallpaper_changer" / "__main__.py"

PyInstaller.__main__.run(
    [
        str(main_path),
        "--name=anime-wallpaper-prog",
        "--onefile",
        "--noconsole",
        "--add-data=README.md:.",
        "--clean",
    ]
)
