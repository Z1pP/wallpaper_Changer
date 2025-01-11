# Anime Wallpaper Changer

Автоматическая смена обоев рабочего стола аниме-артами с сайта wallpaperscraft.ru

## Особенности

- Асинхронная загрузка изображений
- Поддержка Windows и Linux
- Автоматическое определение системы и путей сохранения
- Поддержка различных окружений рабочего стола в Linux (GNOME, KDE, XFCE)
- Логирование всех операций


## Использование с Docker

1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Соберите образ Docker:
   ```bash
   docker build -t anime-wallpaper-changer .
   ```
3. Запустите контейнер:
   ```bash
   docker run --rm -it anime-wallpaper-changer
   ```
4. Приложение будет запущено внутри контейнера.

## Использование с Docker Compose

1. Запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
2. Приложение будет доступно в контейнере `anime_wallpaper_changer`.

## Использование без Docker

```bash
# Активируйте виртуальное окружение
poetry shell

# Запустите программу
python -m anime_wallpaper_changer
```

## Зависимости

- aiohttp: Асинхронные HTTP-запросы
- beautifulsoup4: Парсинг HTML
- aiofiles: Асинхронная работа с файлами
- lxml: Быстрый HTML-парсер
- PyQt6: GUI библиотека
- qasync: Асинхронная интеграция с PyQt
- pillow: Работа с изображениями
