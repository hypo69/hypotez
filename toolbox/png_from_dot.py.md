# Модуль для генерации ссылок на изображения в формате Markdown

## Обзор

Модуль предназначен для генерации Markdown-разметки с ссылками на изображения, находящиеся в указанной папке. Он позволяет автоматизировать процесс создания списков изображений для вставки в Markdown-документы.

## Подробнее

Модуль содержит функцию `generate_image_links`, которая принимает путь к папке с изображениями и возвращает строку с Markdown-ссылками на все изображения в этой папке. Это упрощает добавление галерей изображений в документацию или другие Markdown-файлы.

## Функции

### `generate_image_links`

**Назначение**: Генерирует Markdown-разметку с ссылками на изображения из указанной папки.

**Параметры**:

- `folder_path` (str): Путь к папке, содержащей изображения.

**Возвращает**:

- `str`: Строка с Markdown-разметкой для изображений.

**Как работает функция**:

1.  Инициализирует пустую строку `markdown_images` для хранения результата.
2.  Проходит по всем файлам в указанной папке с помощью `os.listdir(folder_path)`.
3.  Для каждого файла проверяет, является ли он изображением с помощью `filename.endswith((".png", ".jpg", ".jpeg", ".gif"))`.
4.  Если файл является изображением, формирует Markdown-ссылку в формате `![Описание {filename}]({folder_path}/{filename})\n` и добавляет её к строке `markdown_images`.
5.  Возвращает строку `markdown_images` с накопленными Markdown-ссылками.

**Примеры**:

```python
import os

def generate_image_links(folder_path: str) -> str:
    """
    Генерирует список изображений в Markdown для всех файлов из указанной папки.

    Args:
        folder_path (str): Путь к папке с изображениями.

    Returns:
        str: Строка с изображениями в формате Markdown.
    """
    markdown_images = ""
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):  # Указываем нужные расширения
            markdown_images += f"![Описание {filename}]({folder_path}/{filename})\\n"
    return markdown_images

# Пример использования:
folder_path = "images" #  Укажите путь к папке dia
# Создаем папку и несколько файлов для примера
os.makedirs(folder_path, exist_ok=True)
with open(os.path.join(folder_path, "image1.png"), "w") as f:
    f.write("")
with open(os.path.join(folder_path, "image2.jpg"), "w") as f:
    f.write("")
with open(os.path.join(folder_path, "not_image.txt"), "w") as f:
    f.write("")

markdown_output = generate_image_links(folder_path)
print(markdown_output)

#  Удаляем созданную папку и файлы
import shutil
shutil.rmtree(folder_path)
```

## Переменные модуля

-   `folder_path` (str): Путь к папке с изображениями (в данном коде `"__root__/dia"`).
-   `markdown_output` (str): Результат работы функции `generate_image_links`, содержащий Markdown-разметку.