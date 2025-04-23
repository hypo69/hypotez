# Документация для `Cerebras.py`

## Обзор

Файл `Cerebras.py` является частью проекта `hypotez` и предназначен для обеспечения взаимодействия с API Cerebras Inference. Он содержит класс `Cerebras`, который наследуется от `OpenaiAPI` и предоставляет функциональность для генерации асинхронных ответов от моделей Cerebras. Этот модуль также отвечает за аутентификацию и управление cookies для доступа к API.

## Более подробная информация

Этот файл необходим для интеграции с сервисом Cerebras Inference, который предоставляет доступ к различным моделям, таким как `llama3.1-70b`, `llama3.1-8b` и `deepseek-r1-distill-llama-70b`. Класс `Cerebras` переопределяет метод `create_async_generator` для аутентификации и получения API-ключа, если он не был предоставлен явно.

## Классы

### `Cerebras`

**Описание**: Класс `Cerebras` предоставляет функциональность для взаимодействия с API Cerebras Inference.

**Наследует**:
- `OpenaiAPI`: Наследует методы для работы с API OpenAI.

**Атрибуты**:
- `label` (str): Метка провайдера "Cerebras Inference".
- `url` (str): URL для доступа к Cerebras Inference.
- `login_url` (str): URL для логина в Cerebras Cloud.
- `api_base` (str): Базовый URL для API Cerebras.
- `working` (bool): Указывает, что провайдер работает.
- `default_model` (str): Модель, используемая по умолчанию ("llama3.1-70b").
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator`: Асинхронный генератор для создания ответов от моделей Cerebras.

## Методы класса

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
    """
    Создает асинхронный генератор для получения ответов от моделей Cerebras.

    Args:
        cls (Cerebras): Класс `Cerebras`.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        api_key (str, optional): API-ключ для аутентификации. Defaults to `None`.
        cookies (Cookies, optional): Cookies для аутентификации. Defaults to `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий части ответа.

    Raises:
        Exception: Если возникает ошибка при получении API-ключа или при создании генератора.

    Как работает функция:
    - Функция проверяет, предоставлен ли API-ключ. Если нет, то пытается получить его из cookies.
    - Если cookies не предоставлены, функция получает их для домена ".cerebras.ai".
    - Функция выполняет GET-запрос к "https://inference.cerebras.ai/api/auth/session" для получения API-ключа.
    - Если API-ключ получен, функция вызывает метод `create_async_generator` родительского класса `OpenaiAPI` для создания асинхронного генератора.
    - Функция передает полученный API-ключ и заголовки, имитирующие браузер Chrome, в родительский метод.
    - Функция возвращает асинхронный генератор, который выдает части ответа от API Cerebras.

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello, Cerebras!"}]
        >>> async for chunk in Cerebras.create_async_generator(model="llama3.1-70b", messages=messages):
        ...     print(chunk)
    """
    ...
```

## Параметры класса

- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `api_key` (str, optional): API-ключ для аутентификации. Defaults to `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. Defaults to `None`.

**Примеры**:
```python
messages = [{"role": "user", "content": "Hello, Cerebras!"}]
async for chunk in Cerebras.create_async_generator(model="llama3.1-70b", messages=messages):
    print(chunk)