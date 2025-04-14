### **Анализ кода модуля `media.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и логически понятен.
    - Используются аннотации типов.
    - Присутствуют функции для обработки и рендеринга медиа-файлов.
- **Минусы**:
    - Отсутствует docstring для модуля.
    - Отсутствуют docstring для большинства функций, что затрудняет понимание их назначения и использования.
    - В некоторых местах можно улучшить читаемость кода.
    - Не используется модуль `logger` для логирования.
    - Переменные не все аннотированы.
    -  Не везде вокруг оператора `=` есть пробелы

#### **Рекомендации по улучшению**:
1.  **Добавить docstring для модуля**:
    - Описать назначение модуля и предоставить примеры использования.
2.  **Добавить docstring для каждой функции**:
    - Описать назначение функции, входные параметры, возвращаемые значения и возможные исключения.
3.  **Использовать logging**:
    - Добавить логирование для отслеживания ошибок и важной информации.
4.  **Проставить аннотации для переменных**:
    - Все переменные должны быть аннотированы
5.  **Добавить пробелы вокруг операторов присваивания**:
    - Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.

#### **Оптимизированный код**:
```python
"""
Модуль для работы с медиа-контентом
====================================

Модуль содержит функции для рендеринга медиа-файлов, обработки частей контента и объединения медиа-данных.
Он также включает функции для обработки сообщений с медиа-контентом.

Пример использования
----------------------

>>> from pathlib import Path
>>> bucket_id = "test_bucket"
>>> name = "example.jpg"
>>> url = "https://example.com/example.jpg"
>>> rendered_media = render_media(bucket_id, name, url)
>>> print(rendered_media)
data:image/jpeg;base64,...
"""

import os
import base64
from typing import Iterator, Union, Optional, List, Tuple, Dict, Any
from pathlib import Path

from src.logger import logger  # Добавлен импорт logger
from ..typing import Messages
from ..image import is_data_an_media, is_data_an_audio, to_input_audio, to_data_uri
from .files import get_bucket_dir, read_bucket


def render_media(bucket_id: str, name: str, url: str, as_path: bool = False, as_base64: bool = False) -> Union[str, Path]:
    """
    Рендерит медиа-контент в зависимости от переданных параметров.

    Args:
        bucket_id (str): ID бакета, в котором хранится медиа-файл.
        name (str): Имя медиа-файла.
        url (str): URL медиа-файла.
        as_path (bool, optional): Если True, возвращает путь к файлу. Defaults to False.
        as_base64 (bool, optional): Если True, возвращает данные в формате base64. Defaults to False.

    Returns:
        Union[str, Path]: URL медиа-файла, путь к файлу или данные в формате base64.
    
    Raises:
        FileNotFoundError: Если файл не найден и `as_path` установлен в `True`.
        Exception: Если во время обработки возникает непредвиденная ошибка.

    Example:
        >>> bucket_id = "test_bucket"
        >>> name = "example.jpg"
        >>> url = "https://example.com/example.jpg"
        >>> rendered_media = render_media(bucket_id, name, url)
        >>> print(rendered_media)
        data:image/jpeg;base64,...
    """
    try:
        if as_base64 or as_path or url.startswith("/"):
            file: Path = Path(get_bucket_dir(bucket_id, "media", name))
            if as_path:
                return file
            data: bytes = file.read_bytes()
            data_base64: str = base64.b64encode(data).decode()
            if as_base64:
                return data_base64
            return f"data:{is_data_an_media(data, name)};base64,{data_base64}"
        return url
    except FileNotFoundError as ex:
        logger.error(f"File not found: {name} in bucket {bucket_id}", ex, exc_info=True)  # Логирование ошибки
        raise
    except Exception as ex:
        logger.error(f"Error rendering media: {name} in bucket {bucket_id}", ex, exc_info=True)  # Логирование ошибки
        raise


def render_part(part: dict) -> dict:
    """
    Рендерит часть контента, определяя её тип и обрабатывая соответствующим образом.

    Args:
        part (dict): Словарь, представляющий часть контента.

    Returns:
        dict: Словарь с обработанной частью контента.
    
    Raises:
        FileNotFoundError: Если файл не найден в бакете.
        Exception: Если во время обработки возникает непредвиденная ошибка.

    Example:
        >>> part = {"bucket_id": "test_bucket", "name": "example.jpg"}
        >>> rendered_part = render_part(part)
        >>> print(rendered_part)
        {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,...'}}
    """
    try:
        if "type" in part:
            return part
        filename: Optional[str] = part.get("name")
        if filename is None:
            bucket_dir: Path = Path(get_bucket_dir(part.get("bucket_id")))
            return {
                "type": "text",
                "text": "".join(read_bucket(bucket_dir))
            }
        if is_data_an_audio(filename=filename):
            return {
                "type": "input_audio",
                "input_audio": {
                    "data": render_media(**part, as_base64=True),
                    "format": os.path.splitext(filename)[1][1:]
                }
            }
        return {
            "type": "image_url",
            "image_url": {"url": render_media(**part)}
        }
    except FileNotFoundError as ex:
        logger.error(f"File not found in bucket: {part.get('bucket_id')}", ex, exc_info=True)  # Логирование ошибки
        raise
    except Exception as ex:
        logger.error(f"Error rendering part: {part}", ex, exc_info=True)  # Логирование ошибки
        raise


def merge_media(media: list, messages: list) -> Iterator:
    """
    Объединяет медиа-данные с сообщениями, извлекая пути к медиа-файлам из сообщений пользователя.

    Args:
        media (list): Список медиа-файлов.
        messages (list): Список сообщений.

    Yields:
        Tuple[str | Path, Optional[str]]: Путь к медиа-файлу и его имя.
    
    Example:
        >>> media = [("example.mp3", "example.mp3")]
        >>> messages = [{"role": "user", "content": [{"name": "example.jpg", "bucket_id": "test_bucket"}]}]
        >>> merged_media = list(merge_media(media, messages))
        >>> print(merged_media)
        [(PosixPath('test_bucket/media/example.jpg'), 'example.jpg'), ('example.mp3', 'example.mp3')]
    """
    buffer: list = []
    for message in messages:
        if message.get("role") == "user":
            content: Any = message.get("content")
            if isinstance(content, list):
                for part in content:
                    if "type" not in part and "name" in part:
                        path: Path = render_media(**part, as_path=True)
                        buffer.append((path, os.path.basename(path)))
                    elif part.get("type") == "image_url":
                        buffer.append((part.get("image_url"), None))
        else:
            buffer = []
    yield from buffer
    if media is not None:
        yield from media


def render_messages(messages: Messages, media: list = None) -> Iterator:
    """
    Рендерит сообщения, обрабатывая медиа-контент и объединяя его с текстовыми сообщениями.

    Args:
        messages (Messages): Список сообщений.
        media (list, optional): Список медиа-файлов. Defaults to None.

    Yields:
        dict: Обработанное сообщение с медиа-контентом.
    
    Raises:
        Exception: Если во время обработки возникает непредвиденная ошибка.

    Example:
        >>> messages = [{"role": "user", "content": "Hello"}]
        >>> rendered_messages = list(render_messages(messages))
        >>> print(rendered_messages)
        [{'role': 'user', 'content': 'Hello'}]
    """
    try:
        for idx, message in enumerate(messages):
            if isinstance(message["content"], list):
                yield {
                    **message,
                    "content": [render_part(part) for part in message["content"] if part]
                }
            else:
                if media is not None and idx == len(messages) - 1:
                    yield {
                        **message,
                        "content": [
                            {
                                "type": "input_audio",
                                "input_audio": to_input_audio(media_data, filename)
                            }
                            if is_data_an_audio(media_data, filename) else {
                                "type": "image_url",
                                "image_url": {"url": to_data_uri(media_data)}
                            }
                            for media_data, filename in media
                        ] + ([{"type": "text", "text": message["content"]}] if isinstance(message["content"], str) else message["content"])
                    }
                else:
                    yield message
    except Exception as ex:
        logger.error(f"Error rendering messages: {messages}", ex, exc_info=True)  # Логирование ошибки
        raise