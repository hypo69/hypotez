## Как использовать модуль `webp2png`
=========================================================================================

### Описание
-------------------------
Модуль `webp2png` предоставляет функцию `webp2png` для преобразования изображений в формате WebP в PNG. Он также включает функцию `convert_images`, которая обрабатывает пакетное преобразование всех WebP-файлов в указанном каталоге.

### Шаги выполнения
-------------------------
1. **Импорт модулей:**
    - Импортируйте модуль `webp2png` из `src.utils.convertors.webp2png`.
    - Импортируйте необходимые модули, такие как `Path` из `pathlib`, `gs` для доступа к путям к файлам и `get_filenames` для получения списка файлов в каталоге.
2. **Определение каталогов:**
    - Укажите директорию, содержащую исходные WebP-файлы (`webp_dir`).
    - Укажите директорию, куда будут сохраняться преобразованные PNG-файлы (`png_dir`).
3. **Запуск преобразования:**
    - Вызовите функцию `convert_images` с `webp_dir` и `png_dir` в качестве аргументов.
    - Функция `convert_images` ищет WebP-файлы в `webp_dir`, преобразует их в PNG с помощью `webp2png` и сохраняет полученные изображения в `png_dir`.

### Пример использования
-------------------------

```python
from src.utils.convertors.webp2png import webp2png
from pathlib import Path
from src import gs
from src.utils.file import get_filenames

def convert_images(webp_dir: Path, png_dir: Path) -> None:
    """ Преобразует все WebP-изображения в указанном каталоге в формат PNG.

    Args:
        webp_dir (Path): Каталог, содержащий исходные WebP-изображения.
        png_dir (Path): Каталог для сохранения преобразованных PNG-изображений.

    Example:
        convert_images(
            gs.path.google_drive / 'emil' / 'raw_images_from_openai',
            gs.path.google_drive / 'emil' / 'converted_images'
        )
    """
    webp_files: list = get_filenames(webp_dir)

    for webp in webp_files:
        png = png_dir / f"{Path(webp).stem}.png"  # Используйте `stem` для получения имени файла без расширения
        webp_path = webp_dir / webp
        result = webp2png(webp_path, png)
        print(result)

if __name__ == '__main__':
    # Определите каталоги для WebP и PNG-изображений
    webp_dir = gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai'
    png_dir = gs.path.google_drive / 'kazarinov' / 'converted_images'
    print(f"from: {webp_dir=}\nto:{png_dir=}")
    # Запустите преобразование
    convert_images(webp_dir, png_dir)
```

**Заметка:**
-  `gs`  - это модуль проекта `hypotez`, который предоставляет доступ к путям к файлам.
-  `get_filenames`  - это функция, которая получает список файлов в указанном каталоге.
-  `stem`  - это атрибут `Path`, который возвращает имя файла без расширения.