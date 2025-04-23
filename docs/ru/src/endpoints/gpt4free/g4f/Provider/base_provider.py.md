# Документация для разработчика: `base_provider.py`

## Обзор

Модуль `base_provider.py` содержит базовые классы и типы, используемые для работы с различными провайдерами (providers) в проекте `hypotez`. Он определяет абстрактный класс `BaseProvider`, который служит основой для всех конкретных реализаций провайдеров, а также включает вспомогательные классы для управления потоковой передачей данных, ответами и источниками информации.

## Подробнее

Этот модуль предоставляет структуру для создания и управления различными поставщиками (провайдерами) ответов, такими как GPT4Free. Он содержит абстрактный класс `BaseProvider`, который определяет интерфейс для всех провайдеров, включая методы для получения имени провайдера, выполнения запросов и обработки ответов. Кроме того, модуль включает классы для поддержки потоковой передачи данных (`Streaming`), представления ответов (`BaseConversation`), источников информации (`Sources`) и причин завершения (`FinishReason`).

## Классы

### `BaseProvider`

**Описание**:
Абстрактный базовый класс для всех провайдеров. Предоставляет интерфейс для взаимодействия с различными API.

**Атрибуты**:
- `working: bool`: Указывает, работает ли провайдер в данный момент. По умолчанию `True`.
- `supports_stream: bool`: Указывает, поддерживает ли провайдер потоковую передачу данных. По умолчанию `True`.
- `name: str`: Имя провайдера. Должно быть задано в подклассах.
- `ai_prefix: str`: Префикс для ответов AI. Должно быть задано в подклассах.
- `url: str`: URL-адрес провайдера. Должно быть задано в подклассах.
- `needs_auth: bool`: Указывает, требуется ли аутентификация для использования провайдера. По умолчанию `False`.

**Методы**:
- `__init__(self)`: Инициализирует экземпляр класса `BaseProvider`.
- `_create_completion(self, model: str, prompt: str, system_message: str, temperature: float, top_p: float, max_tokens: int, stream: bool, **kwargs) -> str | None | Generator[str, None, None]`: Абстрактный метод для создания завершения (completion). Должен быть реализован в подклассах.
- `get_name(self) -> str`: Возвращает имя провайдера.
- `supports_gpt_35(self) -> bool`: Возвращает `True`, если провайдер поддерживает GPT-3.5. По умолчанию `False`.
- `supports_stream(self) -> bool`: Возвращает `True`, если провайдер поддерживает потоковую передачу данных.
- `get_model_names(self) -> List[str]`: Возвращает список поддерживаемых моделей. По умолчанию возвращает пустой список.

## Методы класса

### `__init__`

```python
def __init__(self):
    """
    Инициализирует экземпляр класса `BaseProvider`.
    """
    ...
```

### `_create_completion`

```python
def _create_completion(self, model: str, prompt: str, system_message: str, temperature: float, top_p: float, max_tokens: int, stream: bool, **kwargs) -> str | None | Generator[str, None, None]:
    """
    Абстрактный метод для создания завершения (completion).
    Должен быть реализован в подклассах.

    Args:
        model (str): Модель для использования.
        prompt (str): Входной запрос.
        system_message (str): Системное сообщение.
        temperature (float): Температура для генерации.
        top_p (float): Top-p значение для генерации.
        max_tokens (int): Максимальное количество токенов в ответе.
        stream (bool): Указывает, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные аргументы.

    Returns:
        str | None | Generator[str, None, None]: Сгенерированный текст или генератор для потоковой передачи.
    """
    ...
```

### `get_name`

```python
def get_name(self) -> str:
    """
    Возвращает имя провайдера.

    Returns:
        str: Имя провайдера.
    """
    ...
```

### `supports_gpt_35`

```python
def supports_gpt_35(self) -> bool:
    """
    Возвращает `True`, если провайдер поддерживает GPT-3.5.

    Returns:
        bool: `True`, если провайдер поддерживает GPT-3.5, иначе `False`.
    """
    ...
```

### `supports_stream`

```python
def supports_stream(self) -> bool:
    """
    Возвращает `True`, если провайдер поддерживает потоковую передачу данных.

    Returns:
        bool: `True`, если провайдер поддерживает потоковую передачу данных, иначе `False`.
    """
    ...
```

### `get_model_names`

```python
def get_model_names(self) -> List[str]:
    """
    Возвращает список поддерживаемых моделей.

    Returns:
        List[str]: Список поддерживаемых моделей.
    """
    ...
```

## Параметры класса

- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `name` (str): Имя провайдера.
- `ai_prefix` (str): Префикс для ответов AI.
- `url` (str): URL-адрес провайдера.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера.

## Примеры

Пример создания подкласса `BaseProvider`:

```python
from ..providers.base_provider import BaseProvider

class MyProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.name = "MyProvider"
        self.ai_prefix = "AI:"
        self.url = "https://example.com"

    def _create_completion(self, model: str, prompt: str, system_message: str, temperature: float, top_p: float, max_tokens: int, stream: bool, **kwargs) -> str | None | Generator[str, None, None]:
        # Здесь должна быть реализация метода
        pass