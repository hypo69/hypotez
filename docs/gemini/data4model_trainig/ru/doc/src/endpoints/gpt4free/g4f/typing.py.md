# Модуль typing

## Обзор

Модуль `typing` содержит определения типов, используемые в проекте `hypotez`. Он включает импорты из стандартных библиотек `sys`, `os`, `typing`, а также условный импорт класса `Image` из библиотеки `PIL`. Модуль определяет новые типы, такие как `SHA256`, `CreateResult`, `AsyncResult`, `Messages`, `Cookies`, `ImageType` и `MediaListType`, которые используются для аннотации типов в других частях проекта.

## Подробней

Этот модуль предоставляет типы, необходимые для статической проверки типов и повышения читаемости кода. Он также обрабатывает условный импорт `TypedDict` в зависимости от версии Python и определяет типы для работы с изображениями и медиа-файлами.

## Типы

### `SHA256`

**Описание**: Псевдоним типа для представления SHA256 хеша.

### `CreateResult`

**Описание**: Псевдоним типа для итератора, возвращающего строки или объекты `ResponseType`.

### `AsyncResult`

**Описание**: Псевдоним типа для асинхронного итератора, возвращающего строки или объекты `ResponseType`.

### `Messages`

**Описание**: Псевдоним типа для списка словарей, представляющих сообщения.

### `Cookies`

**Описание**: Псевдоним типа для словаря, представляющего cookies.

### `ImageType`

**Описание**: Псевдоним типа для представления изображений. Может быть строкой, байтами, файловым объектом, объектом `Image` или путем к файлу.

### `MediaListType`

**Описание**: Псевдоним типа для списка кортежей, содержащих изображения и их описания.

## Условные импорты

### `PIL.Image`

Если библиотека `PIL` (Pillow) не установлена, определяется пустой класс `Image`, чтобы избежать ошибок при аннотации типов.

### `TypedDict`

Для версий Python ниже 3.8 используется `TypedDict` из библиотеки `typing_extensions`, иначе используется встроенный `TypedDict` из модуля `typing`.

## Обзор переменных

### `__all__`

**Описание**: Список строк, содержащий имена всех типов, которые должны быть экспортированы из модуля.

## Примеры

```python
from typing import List, Dict, Union, Optional
from pathlib import Path
from io import IOBase

# Пример использования Messages
messages: List[Dict[str, Union[str, List[Dict[str, Union[str, Dict[str, str]]]]]]] = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
]

# Пример использования Cookies
cookies: Dict[str, str] = {
    "session_id": "12345",
    "user_token": "abcde"
}

# Пример использования ImageType
image_path: Path = Path("image.jpg")
image_data: bytes = b"..."  # Заглушка для данных изображения

image1: Union[str, bytes, IOBase, 'Image', Path] = str(image_path)  # Путь к изображению
image2: Union[str, bytes, IOBase, 'Image', Path] = image_data  # Байты изображения

# Пример использования MediaListType
media_list: List[Tuple[Union[str, bytes, IOBase, 'Image', Path], Optional[str]]] = [
    (image1, "Описание изображения 1"),
    (image2, None)
]