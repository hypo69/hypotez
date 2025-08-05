# Модуль `src.utils.video`

## Обзор

Модуль `src.utils.video` предоставляет асинхронные функции для загрузки и сохранения видеофайлов, а также для получения видеоданных. Он включает в себя обработку ошибок и логирование для обеспечения надежной работы.

## Подробнее

Этот модуль предназначен для выполнения асинхронных операций, связанных с видеофайлами, таких как загрузка из интернета и сохранение на диск.  Он использует библиотеки `aiohttp` для асинхронных HTTP-запросов и `aiofiles` для асинхронных файловых операций, что позволяет эффективно обрабатывать видеоданные без блокировки основного потока выполнения. Модуль также предоставляет функции для чтения видеоданных с диска.

## Функции

### `save_video_from_url`

**Назначение**: Асинхронно загружает видео по URL и сохраняет его локально.

```python
async def save_video_from_url(url: str, save_path: str) -> Optional[Path]:
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
- `url` (str): URL-адрес, по которому необходимо загрузить видео.
- `save_path` (str): Путь для сохранения загруженного видео.

**Возвращает**:
- `Optional[Path]`: Путь к сохраненному файлу, если операция выполнена успешно, или `None`, если произошла ошибка. Функция возвращает `None` в случае ошибок и если размер файла равен 0 байт.

**Вызывает исключения**:
- `aiohttp.ClientError`: Возникает при проблемах с сетью во время загрузки.
- `Exception`: Возникает при других ошибках, связанных с сохранением видео.

**Как работает функция**:
1. Функция принимает URL-адрес видео и путь для сохранения.
2. Создает асинхронную HTTP-сессию с использованием `aiohttp`.
3. Выполняет GET-запрос к указанному URL.
4. Проверяет статус ответа HTTP на наличие ошибок.
5. Создает родительские директории для пути сохранения, если они не существуют.
6. Асинхронно открывает файл для записи в бинарном режиме (`wb`).
7. Читает данные из ответа чанками размером 8192 байта и записывает их в файл.
8. После завершения загрузки проверяет, был ли файл успешно сохранен и не является ли он пустым.
9. Логгирует ошибки, если файл не был сохранен или является пустым.
10. Возвращает путь к сохраненному файлу или `None` в случае ошибки.

**Примеры**:

```python
import asyncio
from pathlib import Path

# Пример успешной загрузки
url = "https://example.com/video.mp4"  # Замените на валидный URL
save_path = "local_video.mp4"
result = asyncio.run(save_video_from_url(url, save_path))
if result:
    print(f"Видео сохранено в {result}")

# Пример обработки ошибки
url = "https://example.com/nonexistent_video.mp4"
save_path = "local_video.mp4"
result = asyncio.run(save_video_from_url(url, save_path))
if result is None:
    print("Не удалось загрузить видео")
```

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
- `file_name` (str): Путь к видеофайлу для чтения.

**Возвращает**:
- `Optional[bytes]`: Бинарные данные файла, если он существует, или `None`, если файл не найден или произошла ошибка.

**Как работает функция**:
1. Функция принимает путь к видеофайлу.
2. Проверяет, существует ли файл по указанному пути.
3. Если файл не существует, функция регистрирует ошибку и возвращает `None`.
4. Открывает файл в бинарном режиме для чтения (`rb`).
5. Читает все содержимое файла в виде байтов.
6. Возвращает бинарные данные файла или `None` в случае ошибки.

**Примеры**:

```python
# Пример успешного чтения данных
file_path = "local_video.mp4"
video_data = get_video_data(file_path)
if video_data:
    print(f"Длина видеоданных: {len(video_data)} байт")

# Пример обработки ошибки
file_path = "nonexistent_video.mp4"
video_data = get_video_data(file_path)
if video_data is None:
    print("Файл не найден")
```

### `main`

**Назначение**: Главная функция для демонстрации работы модуля.

```python
def main():
    url = "https://example.com/video.mp4"  # Replace with a valid URL!
    save_path = "local_video.mp4"
    result = asyncio.run(save_video_from_url(url, save_path))
    if result:
        print(f"Video saved to {result}")
```

**Как работает функция**:

1. Определяет URL-адрес видео для загрузки и путь для сохранения.
2. Вызывает асинхронную функцию `save_video_from_url` для загрузки и сохранения видео.
3. Если загрузка прошла успешно, выводит сообщение об успешном сохранении видео.

**Примеры**:
```python
# Пример вызова main
if __name__ == "__main__":
    main()