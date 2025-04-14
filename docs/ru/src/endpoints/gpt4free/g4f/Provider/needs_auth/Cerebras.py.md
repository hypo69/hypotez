# Модуль Cerebras

## Обзор

Модуль `Cerebras` предоставляет класс для взаимодействия с API Cerebras Inference, который предоставляет доступ к различным моделям, таким как `llama3.1-70b`, `llama3.1-8b` и `deepseek-r1-distill-llama-70b`. Этот модуль расширяет функциональность класса `OpenaiAPI` и предназначен для асинхронного создания генератора ответов от моделей Cerebras.

## Подробней

Модуль предназначен для интеграции с API Cerebras Inference, обеспечивая удобный интерфейс для отправки запросов к моделям и получения ответов в асинхронном режиме. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и автоматически управляет получением `api_key` через `cookies`.

## Классы

### `Cerebras`

**Описание**: Класс `Cerebras` предназначен для взаимодействия с API Cerebras Inference. Он наследует функциональность от класса `OpenaiAPI` и предоставляет методы для аутентификации и создания асинхронного генератора ответов.

**Наследует**:

- `OpenaiAPI`: Класс, предоставляющий базовую функциональность для взаимодействия с OpenAI-подобными API.

**Атрибуты**:

- `label` (str): Метка провайдера, `"Cerebras Inference"`.
- `url` (str): URL главной страницы Cerebras Inference, `"https://inference.cerebras.ai/"`.
- `login_url` (str): URL страницы входа в Cerebras Cloud, `"https://cloud.cerebras.ai"`.
- `api_base` (str): Базовый URL API Cerebras, `"https://api.cerebras.ai/v1"`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
- `default_model` (str): Модель, используемая по умолчанию, `"llama3.1-70b"`.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:

- `create_async_generator`: Асинхронный метод для создания генератора ответов от моделей Cerebras.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    api_key: str = None,
    cookies: Cookies = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от API Cerebras Inference.

    Args:
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        api_key (str, optional): API ключ. Если не указан, пытается получить его из cookies. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, передаваемые в базовый генератор.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки ответов от API.

    Как работает функция:
    1. Проверяется наличие `api_key`. Если он не предоставлен, функция пытается получить его из cookies.
    2. Если `cookies` не предоставлены, функция пытается получить их для домена `.cerebras.ai`.
    3. Используется `ClientSession` из `aiohttp` для выполнения HTTP-запросов с использованием полученных cookies.
    4. Если `api_key` не был предоставлен, выполняется запрос к `"https://inference.cerebras.ai/api/auth/session"` для его получения.
    5. Вызывается метод `create_async_generator` родительского класса `OpenaiAPI` с необходимыми параметрами, включая полученный `api_key` и заголовки.
    6. Возвращается генератор, который предоставляет чанки ответов от API.

    Внутренние функции:
    - Отсутствуют

    """
    ...
```

**Параметры**:

- `cls` (Type[Cerebras]): Ссылка на класс `Cerebras`.
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `api_key` (str, optional): API ключ. Если не указан, пытается получить его из cookies. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в базовый генератор.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, возвращающий чанки ответов от API.

**Как работает функция**:

```
    Проверка наличия api_key и cookies
    │
    ├── Нет api_key:
    │   │
    │   └── Нет cookies:
    │       │
    │       └── Получение cookies для .cerebras.ai
    │
    │
    └── Получение api_key из "https://inference.cerebras.ai/api/auth/session"
    │
    │
    Вызов create_async_generator родительского класса OpenaiAPI
    │
    │
    Возврат генератора чанков ответов
```

**Примеры**:

```python
# Пример использования create_async_generator с указанием model и messages
model = "llama3.1-70b"
messages = [{"role": "user", "content": "Hello, Cerebras!"}]

# Допустим, что api_key и cookies уже установлены или будут получены автоматически
async def main():
    async for chunk in Cerebras.create_async_generator(model=model, messages=messages):
        print(chunk)

# Пример использования create_async_generator с указанием api_key и cookies
model = "llama3.1-70b"
messages = [{"role": "user", "content": "Hello, Cerebras!"}]
api_key = "YOUR_API_KEY"
cookies = {"cookie_name": "cookie_value"}

async def main():
    async for chunk in Cerebras.create_async_generator(model=model, messages=messages, api_key=api_key, cookies=cookies):
        print(chunk)