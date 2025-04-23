# Module website.py

## Обзор

Модуль `website.py` отвечает за настройку маршрутов и обработку запросов для веб-интерфейса приложения. Он использует Flask для определения эндпоинтов, отображения шаблонов и перенаправления пользователей.

## Более подробно

Модуль определяет класс `Website`, который инициализирует Flask-приложение и настраивает маршруты для различных страниц веб-интерфейса, таких как чат, настройки и фоновые изображения. Он также обрабатывает запросы, связанные с идентификаторами общих ресурсов и идентификаторами бесед.

## Классы

### `Website`

**Описание**: Класс `Website` управляет маршрутами и отображением веб-страниц для приложения.

**Атрибуты**:

-   `app`: Flask-приложение, с которым связан класс.
-   `routes` (dict): Словарь, содержащий маршруты и связанные с ними функции и методы.

**Методы**:

-   `__init__(self, app)`: Инициализирует экземпляр класса `Website`, связывая его с Flask-приложением и определяя маршруты.
-   `_chat(self, conversation_id)`: Отображает шаблон `index.html` для чата с указанным `conversation_id`.
-   `_share_id(self, share_id, conversation_id: str = "")`: Отображает шаблон `index.html` с информацией об общем ресурсе (`share_url`, `share_id` и `conversation_id`).
-   `_index(self)`: Отображает шаблон `index.html` для главной страницы чата с новым `conversation_id`.
-   `_settings(self)`: Отображает шаблон `index.html` для страницы настроек с новым `conversation_id`.
-   `_background(self)`: Отображает шаблон `background.html` для страницы с фоном.

## Методы класса

### `__init__`

```python
def __init__(self, app) -> None:
    """Инициализирует экземпляр класса Website.

    Args:
        app: Flask-приложение, с которым будет связан класс.
    """
```

### `_chat`

```python
def _chat(self, conversation_id):
    """Отображает шаблон index.html для чата с указанным conversation_id.

    Args:
        conversation_id: Идентификатор беседы.
    """
```

### `_share_id`

```python
def _share_id(self, share_id, conversation_id: str = ""):
    """Отображает шаблон index.html с информацией об общем ресурсе.

    Args:
        share_id: Идентификатор общего ресурса.
        conversation_id (str, optional): Идентификатор беседы. Defaults to "".
    """
```

### `_index`

```python
def _index(self):
    """Отображает шаблон index.html для главной страницы чата с новым conversation_id."""
```

### `_settings`

```python
def _settings(self):
    """Отображает шаблон index.html для страницы настроек с новым conversation_id."""
```

### `_background`

```python
def _background(self):
    """Отображает шаблон background.html для страницы с фоном."""