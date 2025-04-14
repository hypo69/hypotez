# Модуль для работы с провайдером CablyAI
## Обзор

Модуль предоставляет класс `CablyAI`, который является подклассом `OpenaiTemplate` и предназначен для взаимодействия с сервисом CablyAI. Он определяет URL, API base, флаги поддержки функциональности и метод для создания асинхронного генератора.

## Подробней

Модуль `CablyAI.py` интегрирован в проект `hypotez` для обеспечения возможности использования CablyAI в качестве одного из провайдеров для генерации текста. Он содержит необходимые настройки и заголовки для аутентификации и взаимодействия с API CablyAI.

## Классы

### `CablyAI`

**Описание**: Класс предназначен для взаимодействия с API CablyAI. Он наследует функциональность от класса `OpenaiTemplate` и предоставляет специфические настройки и методы для работы с CablyAI.

**Наследует**:

- `OpenaiTemplate`: Предоставляет базовый функционал для работы с OpenAI-подобными API.

**Атрибуты**:

- `url` (str): URL для взаимодействия с CablyAI ("https://cablyai.com/chat").
- `login_url` (str): URL для логина в CablyAI ("https://cablyai.com").
- `api_base` (str): Базовый URL для API CablyAI ("https://cablyai.com/v1").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (True).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (True).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API CablyAI.

## Методы класса

### `create_async_generator`

```python
def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    api_key: str = None,
    stream: bool = False,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с API CablyAI.

    Args:
        cls (CablyAI): Класс CablyAI.
        model (str): Название модели, которую необходимо использовать.
        messages (Messages): Список сообщений для отправки в API.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        stream (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        ModelNotSupportedError: Если указанная модель не поддерживается.

    Как работает функция:
    - Функция принимает параметры для создания асинхронного генератора.
    - Определяет заголовки запроса, включая API-ключ для авторизации.
    - Вызывает метод `create_async_generator` родительского класса `OpenaiTemplate` для фактического создания генератора.
    - Передает заголовки и другие параметры в родительский метод.
    """
```

## Параметры класса

- `cls`: Ссылка на класс `CablyAI`.
- `model` (str): Идентификатор модели, используемой для генерации ответов.
- `messages` (Messages): Список сообщений, отправляемых в API.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `stream` (bool, optional): Флаг для включения потокового режима. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры, передаваемые в API.

**Примеры**

```python
from g4f.Provider import CablyAI
from g4f.models import gpt_35_turbo

# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, CablyAI!"}]
api_key = "YOUR_API_KEY"  # Замените на ваш реальный API-ключ

async_result = CablyAI.create_async_generator(
    model=gpt_35_turbo.name,
    messages=messages,
    api_key=api_key,
    stream=True
)