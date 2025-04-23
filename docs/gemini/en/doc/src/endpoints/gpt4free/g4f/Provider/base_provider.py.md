# Документация для `base_provider.py`

## Обзор

Этот файл содержит базовые классы и типы, используемые другими провайдерами. Он включает в себя `BaseProvider`, `Streaming`, `BaseConversation`, `Sources` и `FinishReason`, а также вспомогательные функции для работы с провайдерами.

## Детали

Файл `base_provider.py` предоставляет абстрактные классы и типы, которые служат основой для реализации различных провайдеров, используемых в проекте. Это обеспечивает единообразие и упрощает добавление новых провайдеров.

## Классы

### `BaseProvider`

**Описание**: Базовый класс для всех провайдеров.

**Наследует**:
- Нет.

**Атрибуты**:
- `name` (str): Название провайдера.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
- `needs_key` (bool): Указывает, требуется ли ключ API для работы с провайдером.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `url` (str): URL провайдера.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `BaseProvider`.
- `_create_completion`: Абстрактный метод для создания завершения.
- `create_completion`: Метод для создания завершения с обработкой ошибок.

### `BaseProvider.__init__`

```python
def __init__(
        self,
        name: str,
        supports_gpt_35_turbo: bool = True,
        supports_stream: bool = True,
        needs_key: bool = False,
        working: bool = True,
        url: str = "",
    ):
        """
        Инициализирует экземпляр класса `BaseProvider`.
        
        Args:
            name (str): Название провайдера.
            supports_gpt_35_turbo (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo. По умолчанию `True`.
            supports_stream (bool): Указывает, поддерживает ли провайдер потоковую передачу. По умолчанию `True`.
            needs_key (bool): Указывает, требуется ли ключ API для работы с провайдером. По умолчанию `False`.
            working (bool): Указывает, работает ли провайдер в данный момент. По умолчанию `True`.
            url (str): URL провайдера. По умолчанию пустая строка.
        """
```

### `BaseProvider._create_completion`

```python
@abstractmethod
def _create_completion(
    self,
    model: str,
    prompt: str,
    **kwargs
):
    """
    Абстрактный метод для создания завершения.

    Args:
        model (str): Название модели.
        prompt (str): Входной запрос.
        **kwargs: Дополнительные параметры.
    """
```

### `BaseProvider.create_completion`

```python
def create_completion(
    self,
    model: str,
    prompt: str,
    **kwargs
):
    """
    Метод для создания завершения с обработкой ошибок.

    Args:
        model (str): Название модели.
        prompt (str): Входной запрос.
        **kwargs: Дополнительные параметры.

    Returns:
        str: Результат завершения.

    Raises:
        Exception: Если происходит ошибка при создании завершения.
    """
```

## Переменные

### `Streaming`
- Тип: `typing.Any`
- Описание: Тип для потоковой передачи данных.

### `BaseConversation`
- Тип: `typing.Any`
- Описание: Тип для представления базового разговора.

### `Sources`
- Тип: `typing.Any`
- Описание: Тип для представления источников.

### `FinishReason`
- Тип: `typing.Any`
- Описание: Тип для представления причины завершения.

## Функции

### `get_cookies`

```python
def get_cookies(url: str) -> dict:
    """
    Извлекает куки из указанного URL.

    Args:
        url (str): URL для извлечения куки.

    Returns:
        dict: Словарь с куками.
    """
```

### `format_prompt`

```python
def format_prompt(prompt: str, model: str) -> str:
    """
    Форматирует входной запрос для конкретной модели.

    Args:
        prompt (str): Входной запрос.
        model (str): Название модели.

    Returns:
        str: Отформатированный запрос.
    """