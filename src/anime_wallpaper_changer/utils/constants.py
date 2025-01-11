from typing import Dict

# Цветовые схемы
THEMES = {
    "dark": {
        "primary": "#7C4DFF",  # Яркий фиолетовый
        "primary_dark": "#651FFF",
        "background": "#1A1A1A",  # Глубокий темный
        "secondary_background": "#2D2D2D",
        "text": "#FFFFFF",
        "secondary_text": "#B3B3B3",
        "border": "#404040",
        "disabled": "#505050",
        "accent": "#00E5FF",  # Яркий голубой для акцентов
        "success": "#00E676",  # Зеленый для успешных действий
        "error": "#FF1744",  # Красный для ошибок
        "hover": "#9575FF",  # Светлый фиолетовый для ховера
    },
    "light": {
        "primary": "#7C4DFF",  # Тот же фиолетовый для консистентности
        "primary_dark": "#651FFF",
        "background": "#F5F5F5",  # Мягкий светлый
        "secondary_background": "#FFFFFF",
        "text": "#2C2C2C",
        "secondary_text": "#757575",
        "border": "#E0E0E0",
        "disabled": "#BDBDBD",
        "accent": "#00B8D4",  # Приглушенный голубой
        "success": "#00C853",  # Приглушенный зеленый
        "error": "#D50000",  # Приглушенный красный
        "hover": "#B39DDB",  # Пастельный фиолетовый для ховера
    },
}

DEFAULT_THEME = "dark"

# Доступные разрешения
RESOLUTIONS: Dict[str, str] = {
    "HD (1366x768)": "1366x768",
    "HD+ (1600x900)": "1600x900",
    "Full HD (1920x1080)": "1920x1080",
    "2K (2560x1440)": "2560x1440",
    "4K (3840x2160)": "3840x2160",
}

# Доступные категории
CATEGORIES: Dict[str, str] = {
    "3D": "3d",
    "Абстракция": "abstract",
    "Аниме": "anime",
    "Арт": "art",
    "Векторная графика": "vector",
    "Города": "city",
    "Еда": "food",
    "Животные": "animals",
    "Космос": "space",
    "Любовь": "love",
    "Макро": "macro",
    "Машины": "cars",
    "Минимализм": "minimalism",
    "Мотоциклы": "motorcycles",
    "Музыка": "music",
    "Праздники": "holidays",
    "Природа": "nature",
    "Разное": "other",
    "Слова": "words",
    "Спорт": "sport",
    "Текстуры": "textures",
    "Темные": "dark",
    "Технологии": "hi-tech",
    "Фэнтези": "fantasy",
    "Цветы": "flowers",
    "Черно-белые": "black_and_white",
    "Черные": "black",
}

# Настройки по умолчанию
DEFAULT_RESOLUTION = "1920x1080"
DEFAULT_CATEGORY = "anime"
