# Модуль для работы с видео (video.py)

## Обзор

Этот модуль предоставляет асинхронные функции для скачивания и сохранения видеофайлов, а также для получения данных видео. Он включает обработку ошибок и логирование для обеспечения надежной работы.

## Подробней

Модуль `src.utils.video` предоставляет утилиты для работы с видеофайлами, такие как асинхронное скачивание видео по URL и чтение бинарных данных видео. Модуль использует библиотеки `aiohttp`, `aiofiles` и модуль логирования `src.logger.logger`.

## Функции

### `save_video_from_url`

**Назначение**: Асинхронно скачивает видео по URL и сохраняет его локально.

```python
async def save_video_from_url(
    url: str,
    save_path: str
) -> Optional[Path]:
    """Download a video from a URL and save it locally asynchronously.

    Args:
        url (str): The URL from which to download the video.
        save_path (str): The path to save the downloaded video.

    Returns:
        Optional[Path]: The path to the saved file, or `None` if the operation failed.  Returns None on errors and if file is 0 bytes.

    Raises:
        aiohttp.ClientError: on network issues during the download.
    """
    ...
```

**Параметры**:

-   `url` (str): URL для скачивания видео.
-   `save_path` (str): Путь для сохранения скачанного видео.

**Возвращает**:

-   `Optional[Path]`: Путь к сохраненному файлу или `None`, если операция не удалась. Возвращает `None` при ошибках и если размер файла равен 0 байт.

**Вызывает исключения**:

-   `aiohttp.ClientError`: При сетевых проблемах во время скачивания.

**Как работает функция**:

1.  Преобразует путь для сохранения в объект `Path`.
2.  Использует `aiohttp.ClientSession` для асинхронного выполнения HTTP-запроса к указанному URL.
3.  Проверяет статус ответа (код 200 означает успех).
4.  Создает родительские директории, если они не существуют.
5.  Асинхронно открывает файл для записи в бинарном режиме.
6.  Читает содержимое файла частями (чанками) и записывает их в файл.
7.  После сохранения проверяет, был ли файл создан и не является ли он пустым.
8.  Логирует информацию об ошибках, используя `logger.error`.

### `get_video_data`

**Назначение**: Извлекает бинарные данные видеофайла, если он существует.

```python
def get_video_data(file_name: str) -> Optional[bytes]:
    """Retrieve binary data of a video file if it exists.

    Args:
        file_name (str): The path to the video file to read.

    Returns:
        Optional[bytes]: The binary data of the file if it exists, or `None` if the file is not found or an error occurred.
    """
    ...
```

**Параметры**:

-   `file_name` (str): Путь к видеофайлу для чтения.

**Возвращает**:

-   `Optional[bytes]`: Бинарные данные файла, если он существует, или `None`, если файл не найден или произошла ошибка.

**Как работает функция**:

1.  Преобразует имя файла в объект `Path`.
2.  Проверяет, существует ли указанный файл.
3.  Открывает файл в бинарном режиме (`"rb"`) и считывает его содержимое.
4.  Логирует информацию об ошибках, используя `logger.error`.

## Переменные модуля

-   В этом модуле отсутствуют глобальные переменные, за исключением констант, определенных внутри функций.

## Пример использования

**Скачивание видеофайла:**

```python
import asyncio
from src.utils import video

async def main():
    url = "https://example.com/video.mp4"  # Замените на реальный URL!
    save_path = "local_video.mp4"
    result = await video.save_video_from_url(url, save_path)
    if result:
        print(f"Video saved to {result}")
    else:
        print("Failed to save video.")

if __name__ == "__main__":
    asyncio.run(main())
```

**Получение данных видеофайла:**

```python
from src.utils import video

data = video.get_video_data("local_video.mp4")
if data:
    print(f"Video data: {data[:10]}...")  # Вывод первых 10 байт
else:
    print("Failed to retrieve video data.")
```

## Взаимосвязь с другими частями проекта

-   Модуль `src.utils.video` используется другими модулями проекта для скачивания и обработки видеофайлов.
-   Для логирования ошибок используется модуль `src.logger.logger`.
-   Для асинхронных операций используется модуль `aiohttp` и `aiofiles`.