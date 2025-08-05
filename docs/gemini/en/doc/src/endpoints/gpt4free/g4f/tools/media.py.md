# Модуль для обработки медиафайлов
=================================================

Модуль `media.py` предоставляет функции для работы с медиафайлами, такими как изображения и аудио. Он позволяет рендерить медиафайлы в различных форматах, объединять их с сообщениями и рендерить сообщения с медиафайлами.

## Содержание
  - [Функции](#Функции)
    - [render_media](#render_media)
    - [render_part](#render_part)
    - [merge_media](#merge_media)
    - [render_messages](#render_messages)

## Функции

### `render_media`
```python
def render_media(bucket_id: str, name: str, url: str, as_path: bool = False, as_base64: bool = False) -> Union[str, Path]:
    """
    Функция рендерит медиафайл в различных форматах.

    Args:
        bucket_id (str): ID корзины, в которой хранится медиафайл.
        name (str): Имя медиафайла.
        url (str): URL медиафайла.
        as_path (bool, optional): Если `True`, возвращает путь к файлу. По умолчанию `False`.
        as_base64 (bool, optional): Если `True`, возвращает медиафайл в кодировке Base64. По умолчанию `False`.

    Returns:
        Union[str, Path]: Путь к файлу, медиафайл в кодировке Base64 или URL медиафайла.

    Raises:
        Exception: Если возникает ошибка при обработке медиафайла.
    """
```

### `render_part`
```python
def render_part(part: dict) -> dict:
    """
    Функция рендерит часть сообщения, которая может содержать медиафайл.

    Args:
        part (dict): Часть сообщения, содержащая информацию о медиафайле.

    Returns:
        dict: Отформатированная часть сообщения с медиафайлом.

    Raises:
        Exception: Если возникает ошибка при обработке сообщения.
    """
```

### `merge_media`
```python
def merge_media(media: list, messages: list) -> Iterator:
    """
    Функция объединяет медиафайлы с сообщениями.

    Args:
        media (list): Список медиафайлов.
        messages (list): Список сообщений.

    Returns:
        Iterator: Итератор, который возвращает пары (путь к файлу, имя файла) или (URL, None) для каждого медиафайла в сообщении.

    Raises:
        Exception: Если возникает ошибка при обработке медиафайла или сообщения.
    """
```

### `render_messages`
```python
def render_messages(messages: Messages, media: list = None) -> Iterator:
    """
    Функция рендерит сообщения с медиафайлами.

    Args:
        messages (Messages): Список сообщений.
        media (list, optional): Список медиафайлов. По умолчанию `None`.

    Returns:
        Iterator: Итератор, который возвращает отформатированные сообщения с медиафайлами.

    Raises:
        Exception: Если возникает ошибка при обработке медиафайла или сообщения.
    """