from setuptools import setup, find_packages

setup(
    name="anime-wallpaper-changer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiohttp>=3.11.0",
        "aiofiles>=24.1.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=5.3.0",
        "PyQt6>=6.6.0",
        "qasync>=0.27.0",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "anime-wallpaper=anime_wallpaper_changer.__main__:main",
        ],
    },
)
