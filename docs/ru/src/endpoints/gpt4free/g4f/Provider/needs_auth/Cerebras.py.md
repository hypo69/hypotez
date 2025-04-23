# Документация модуля Cerebras

## Обзор

Модуль `Cerebras.py` предназначен для взаимодействия с сервисом Cerebras Inference, предоставляющим доступ к различным моделям машинного обучения, включая llama3.1-70b, llama3.1-8b и deepseek-r1-distill-llama-70b. Модуль наследует функциональность от класса `OpenaiAPI` и предоставляет механизм для аутентификации и запросов к API Cerebras.

## Подробней

Модуль обеспечивает асинхронное взаимодействие с API Cerebras Inference, используя `aiohttp` для выполнения HTTP-запросов. Он поддерживает автоматическое получение ключа API из cookies, если он не был предоставлен явно. Также модуль определяет список поддерживаемых моделей и их псевдонимы.

## Классы

### `Cerebras`

**Описание**: Класс `Cerebras` предназначен для взаимодействия с API Cerebras Inference. Он наследуется от класса `OpenaiAPI` и реализует специфическую логику аутентификации и формирования запросов к API Cerebras.

**Наследует**:

- `OpenaiAPI`: Предоставляет базовую функциональность для работы с API OpenAI-подобных сервисов.

**Атрибуты**:

- `label` (str): Метка, идентифицирующая провайдера Cerebras Inference.
- `url` (str): URL для доступа к веб-интерфейсу Cerebras Inference.
- `login_url` (str): URL для логина в Cerebras Cloud.
- `api_base` (str): Базовый URL для API Cerebras.
- `working` (bool): Указывает, работает ли данный провайдер.
- `default_model` (str): Модель, используемая по умолчанию ("llama3.1-70b").
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:

- `create_async_generator()`: Асинхронный генератор для создания запросов к API Cerebras.

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
    Создает асинхронный генератор для взаимодействия с API Cerebras.

    Args:
        model (str): Модель для использования в запросе.
        messages (Messages): Список сообщений для отправки в API.
        api_key (str, optional): Ключ API. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки данных из API.

    Raises:
        Exception: Если не удается получить ключ API.

    
    - Функция сначала пытается получить ключ API из cookies, если он не предоставлен явно.
    - Если cookies не предоставлены, функция получает их из домена ".cerebras.ai".
    - Затем функция отправляет запрос к "https://inference.cerebras.ai/api/auth/session", чтобы получить ключ API.
    - Далее вызывается метод `create_async_generator` родительского класса `OpenaiAPI` с полученным ключом API и другими параметрами.
    - Функция переопределяет User-Agent в заголовках запроса.

    Внутренние функции:
        отсутствуют

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello, Cerebras!"}]
        >>> async for chunk in Cerebras.create_async_generator(model="llama3.1-70b", messages=messages):
        ...     print(chunk)
    """
    ...
```

## Параметры класса

- `label` (str): "Cerebras Inference" - метка, идентифицирующая провайдера.
- `url` (str): "https://inference.cerebras.ai/" - URL для доступа к веб-интерфейсу.
- `login_url` (str): "https://cloud.cerebras.ai" - URL для логина в Cerebras Cloud.
- `api_base` (str): "https://api.cerebras.ai/v1" - базовый URL для API Cerebras.
- `working` (bool): `True` - указывает, что данный провайдер работает.
- `default_model` (str): "llama3.1-70b" - модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей, включая "llama3.1-70b", "llama3.1-8b", "llama-3.3-70b" и "deepseek-r1-distill-llama-70b".
- `model_aliases` (Dict[str, str]): Псевдонимы моделей, например, {"llama-3.1-70b": "llama3.1-70b", "llama-3.1-8b": "llama3.1-8b", "deepseek-r1": "deepseek-r1-distill-llama-70b"}.

## Примеры

Пример использования класса `Cerebras` для создания асинхронного генератора:

```python
messages = [{"role": "user", "content": "Hello, Cerebras!"}]
async for chunk in Cerebras.create_async_generator(model="llama3.1-70b", messages=messages):
    print(chunk)