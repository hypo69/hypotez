# Модуль API

## Обзор

Модуль `api.py` содержит классы и функции для обработки запросов к различным моделям и провайдерам,
включая управление разговорами, подготовку аргументов для запросов и создание потоков ответов.
Он также обеспечивает доступ к информации о моделях, провайдерах и версиях, а также обработку изображений.

## Более подробная информация

Этот модуль является частью веб-сервера `g4f` и предоставляет API для взаимодействия с различными
AI-моделями и провайдерами. Он включает в себя функции для получения списка доступных моделей и
провайдеров, управления разговорами, подготовки аргументов для запросов и создания потоков ответов.

## Классы

### `Api`

**Описание**: Класс `Api` содержит статические методы и методы экземпляра для обработки API-запросов.

**Методы**:

- `get_models()`: Возвращает список доступных моделей.
- `get_provider_models(provider: str, api_key: str = None, api_base: str = None)`: Возвращает список моделей, поддерживаемых указанным провайдером.
- `get_providers()`: Возвращает список доступных провайдеров.
- `get_version()`: Возвращает информацию о версии.
- `serve_images(name)`: Обслуживает запросы на изображения.
- `_prepare_conversation_kwargs(self, json_data: dict)`: Подготавливает аргументы для создания или продолжения разговора.
- `_create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True)`: Создает поток ответов на основе переданных аргументов.
- `_yield_logs(self)`: Генерирует логи отладки.
- `_format_json(self, response_type: str, content = None, **kwargs)`: Форматирует JSON-ответ.
- `handle_provider(self, provider_handler, model)`: Обрабатывает информацию о провайдере.

## Методы класса

### `get_models`

```python
@staticmethod
def get_models() -> list[dict]:
    """
    Возвращает список доступных моделей с информацией о каждой модели.

    Returns:
        list[dict]: Список словарей, где каждый словарь содержит информацию о модели, включая ее имя,
                    поддержку изображений и видео, а также список провайдеров, поддерживающих эту модель.
    """
    ...
```

### `get_provider_models`

```python
@staticmethod
def get_provider_models(provider: str, api_key: str = None, api_base: str = None) -> list[dict]:
    """
    Возвращает список моделей, поддерживаемых указанным провайдером.

    Args:
        provider (str): Имя провайдера.
        api_key (str, optional): API-ключ для провайдера. Defaults to `None`.
        api_base (str, optional): Базовый URL API для провайдера. Defaults to `None`.

    Returns:
        list[dict]: Список словарей, где каждый словарь содержит информацию о модели, включая ее имя,
                    является ли она моделью по умолчанию, поддерживает ли она изображения и видео,
                    а также задачу, которую она выполняет.
    """
    ...
```

### `get_providers`

```python
@staticmethod
def get_providers() -> list[dict]:
    """
    Возвращает список доступных провайдеров с информацией о каждом провайдере.

    Returns:
        list[dict]: Список словарей, где каждый словарь содержит информацию о провайдере, включая его имя,
                    отображаемое имя, родительский провайдер (если есть), поддержку изображений и видео,
                    требуется ли аутентификация и URL для входа.
    """
    ...
```

### `get_version`

```python
@staticmethod
def get_version() -> dict:
    """
    Возвращает информацию о текущей и последней доступной версии.

    Returns:
        dict: Словарь, содержащий информацию о текущей и последней доступной версии.
              Если информация о версии недоступна, возвращает `None` для обеих версий.

    Raises:
        VersionNotFoundError: Если не удается получить информацию о версии.
    """
    ...
```

## Методы экземпляра класса

### `serve_images`

```python
def serve_images(self, name: str) -> Response:
    """
    Обслуживает запросы на изображения из каталога изображений.

    Args:
        name (str): Имя файла изображения.

    Returns:
        Response: Объект ответа Flask, содержащий запрошенное изображение.
    """
    ...
```

### `_prepare_conversation_kwargs`

```python
def _prepare_conversation_kwargs(self, json_data: dict) -> dict:
    """
    Подготавливает аргументы для создания или продолжения разговора на основе JSON-данных.

    Args:
        json_data (dict): JSON-данные, содержащие параметры разговора, такие как модель, провайдер,
                           сообщения и идентификатор разговора.

    Returns:
        dict: Словарь с подготовленными аргументами для создания или продолжения разговора.
    """
    ...
```

### `_create_response_stream`

```python
def _create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator:
    """
    Создает поток ответов на основе переданных аргументов.

    Args:
        kwargs (dict): Аргументы для создания потока ответов, такие как модель, провайдер и сообщения.
        conversation_id (str): Идентификатор разговора.
        provider (str): Имя провайдера.
        download_media (bool, optional): Флаг, указывающий, нужно ли загружать медиафайлы. Defaults to `True`.

    Yields:
        Iterator: Поток ответов, который может содержать информацию о провайдере, сообщения, изображения,
                  аудио и другие данные.
    """
    ...
```

### `_yield_logs`

```python
def _yield_logs(self) -> Iterator:
    """
    Генерирует логи отладки, если они есть, и очищает список логов.

    Yields:
        Iterator: Поток логов отладки.
    """
    ...
```

### `_format_json`

```python
def _format_json(self, response_type: str, content = None, **kwargs) -> dict:
    """
    Форматирует JSON-ответ.

    Args:
        response_type (str): Тип ответа.
        content (Any, optional): Содержимое ответа. Defaults to `None`.
        **kwargs: Дополнительные аргументы для включения в JSON-ответ.

    Returns:
        dict: Словарь, представляющий JSON-ответ.
    """
    ...
```

### `handle_provider`

```python
def handle_provider(self, provider_handler, model) -> dict:
    """
    Обрабатывает информацию о провайдере.

    Args:
        provider_handler: Обработчик провайдера.
        model: Модель, используемая провайдером.

    Returns:
        dict: Словарь, содержащий информацию о провайдере.
    """
    ...
```

## Функции

### `get_error_message`

```python
def get_error_message(exception: Exception) -> str:
    """
    Форматирует сообщение об ошибке на основе переданного исключения.

    Args:
        exception (Exception): Объект исключения.

    Returns:
        str: Отформатированное сообщение об ошибке, содержащее имя типа исключения и сообщение.
    """
    return f"{type(exception).__name__}: {exception}"
```