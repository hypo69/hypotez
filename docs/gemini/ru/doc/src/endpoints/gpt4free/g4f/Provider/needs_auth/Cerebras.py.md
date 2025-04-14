# Модуль Cerebras

## Обзор

Модуль `Cerebras` представляет собой класс для взаимодействия с API Cerebras Inference, который предоставляет доступ к различным моделям, таким как `llama3.1-70b` и `deepseek-r1-distill-llama-70b`. Он наследуется от класса `OpenaiAPI` и предназначен для асинхронного создания генераторов текста на основе предоставленных сообщений.

## Подробнее

Этот модуль обеспечивает возможность использования моделей Cerebras Inference для генерации текста. Он проверяет наличие API-ключа и, если он отсутствует, пытается получить его из cookies или через API. Модуль также определяет список доступных моделей и их псевдонимы.

## Классы

### `Cerebras`

**Описание**: Класс для взаимодействия с API Cerebras Inference.

**Наследует**:
- `OpenaiAPI`: Этот класс наследует функциональность от `OpenaiAPI`, предоставляя базовые методы для взаимодействия с API OpenAI.

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера как "Cerebras Inference".
- `url` (str): URL главной страницы Cerebras Inference.
- `login_url` (str): URL страницы логина Cerebras Cloud.
- `api_base` (str): Базовый URL для API Cerebras.
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `default_model` (str): Модель, используемая по умолчанию ("llama3.1-70b").
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator()`: Асинхронный метод для создания генератора текста на основе предоставленных сообщений.

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
    """Асинхронно создает генератор текста на основе предоставленных сообщений, используя API Cerebras Inference.

    Args:
        cls (Type[Cerebras]): Класс `Cerebras`.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для генерации текста.
        api_key (Optional[str]): API-ключ для доступа к API Cerebras. По умолчанию `None`.
        cookies (Optional[Cookies]): Cookies для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, передаваемые в базовый метод `create_async_generator`.

    Returns:
        AsyncResult: Асинхронный генератор текста.

    Raises:
        Exception: Если не удается получить API-ключ.

    Как работает функция:
    - Проверяет наличие API-ключа. Если он не предоставлен, пытается получить его из cookies.
    - Если cookies также не предоставлены, пытается получить их для домена ".cerebras.ai".
    - Если API-ключ по-прежнему отсутствует, выполняет запрос к "https://inference.cerebras.ai/api/auth/session" для получения API-ключа.
    - Вызывает метод `create_async_generator` родительского класса `OpenaiAPI` с необходимыми параметрами.
    - Передает полученные чанки текста через yield.
    """
    ...
```

#### Параметры:
- `model` (str): Название модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений, используемых для генерации текста.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, передаваемые в функцию генерации.

#### Возвращает:
- `AsyncResult`: Асинхронный генератор текста.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
model = "llama3.1-70b"

# Предположим, что api_key и cookies уже получены
api_key = "your_api_key"
cookies = {"cookie_name": "cookie_value"}

async def generate_text():
    async for chunk in Cerebras.create_async_generator(model=model, messages=messages, api_key=api_key, cookies=cookies):
        print(chunk, end="")

# Запуск асинхронной функции
# await generate_text()