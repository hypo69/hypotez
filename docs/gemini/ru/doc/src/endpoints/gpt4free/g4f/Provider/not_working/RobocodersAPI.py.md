# Модуль `RobocodersAPI.py`

## Обзор

Модуль `RobocodersAPI.py` предоставляет асинхронный интерфейс для взаимодействия с API Robocoders AI. Он позволяет генерировать ответы на основе предоставленных сообщений, используя различные модели агентов, такие как `GeneralCodingAgent`, `RepoAgent` и `FrontEndAgent`. Модуль поддерживает сохранение и обновление токенов доступа и идентификаторов сессий в кэше для повторного использования.

## Подробней

Этот модуль предназначен для интеграции с AI-сервисами Robocoders, предоставляя возможность программного взаимодействия с их API. Он включает в себя функции для получения токена доступа, создания сессии и отправки запросов на генерацию ответов. В модуле реализована логика обработки ошибок и повторных запросов, а также механизм автоматического продолжения диалога при достижении лимита ресурсов. Кэширование данных помогает избежать повторных запросов и ускоряет процесс взаимодействия с API.

## Классы

### `RobocodersAPI`

**Описание**: Класс `RobocodersAPI` является асинхронным провайдером и миксином моделей, предоставляющим интерфейс для взаимодействия с API Robocoders AI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера "API Robocoders AI".
- `url` (str): URL документации API Robocoders AI ("https://api.robocoders.ai/docs").
- `api_endpoint` (str): URL конечной точки API для чата ("https://api.robocoders.ai/chat").
- `working` (bool): Флаг, указывающий на работоспособность API (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (в данном случае `True`).
- `default_model` (str): Модель агента по умолчанию ('GeneralCodingAgent').
- `agent` (list): Список доступных моделей агентов, включая `default_model`, "RepoAgent" и "FrontEndAgent".
- `models` (list): Список доступных моделей, идентичный `agent`.
- `CACHE_DIR` (Path): Путь к директории для кэширования.
- `CACHE_FILE` (Path): Путь к файлу кэша (`robocoders.json`).

**Принцип работы**:
Класс использует асинхронные запросы к API Robocoders AI для генерации ответов на основе предоставленных сообщений. Он управляет токенами доступа и идентификаторами сессий, сохраняя их в кэше для повторного использования. Класс также обрабатывает ошибки и автоматически продолжает диалог при достижении лимита ресурсов.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.
- `_get_or_create_access_and_session`: Получает или создает токен доступа и идентификатор сессии.
- `_fetch_and_cache_access_token`: Получает и кэширует токен доступа.
- `_create_and_cache_session`: Создает и кэширует идентификатор сессии.
- `_save_cached_data`: Сохраняет новые данные в файл кэша.
- `_update_cached_data`: Обновляет существующие данные в файле кэша.
- `_clear_cached_data`: Удаляет файл кэша.
- `_get_cached_data`: Получает все закэшированные данные.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от API Robocoders AI.

    Args:
        cls (RobocodersAPI): Ссылка на класс `RobocodersAPI`.
        model (str): Модель агента для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API.

    Raises:
        Exception: Если не удается инициализировать взаимодействие с API, если возникает ошибка аутентификации,
                   ошибка валидации входных данных, серверная ошибка или неожиданная ошибка.
    """
```
**Как работает функция**:
1. Устанавливает таймаут для клиентской сессии aiohttp.
2. Создает асинхронную клиентскую сессию.
3. Получает или создает токен доступа и идентификатор сессии, вызывая метод `_get_or_create_access_and_session`.
4. Формирует заголовки запроса, включая токен доступа.
5. Форматирует запрос, подготавливая данные для отправки в API.
6. Отправляет POST-запрос к API с использованием предоставленных данных и заголовков.
7. Обрабатывает различные статусы ответа, такие как 401 (неавторизованный), 422 (ошибка валидации) и ошибки 5xx.
8. Итерируется по каждой строке ответа, декодирует JSON, извлекает сообщение и выдает его через генератор.
9. Обрабатывает ситуации, когда достигнут лимит ресурсов, и автоматически продолжает диалог.
10. Логирует любые ошибки декодирования JSON или другие исключения, возникающие в процессе.

### `_get_or_create_access_and_session`

```python
@staticmethod
async def _get_or_create_access_and_session(session: aiohttp.ClientSession):
    """
    Получает существующий токен доступа и идентификатор сессии из кэша или создает новые, если они не найдены или недействительны.

    Args:
        session (aiohttp.ClientSession): Асинхронная клиентская сессия.

    Returns:
        tuple[str, str]: Кортеж, содержащий токен доступа и идентификатор сессии.

    Raises:
        Exception: Если не удается получить токен доступа или создать сессию.
    """
```

**Как работает функция**:
1.  Создает директорию для кэширования, если она не существует.
2.  Проверяет наличие файла кэша.
3.  Если файл кэша существует, пытается загрузить из него токен доступа и идентификатор сессии.
4.  Если токен доступа и идентификатор сессии успешно загружены и валидны, возвращает их.
5.  Если файл кэша не существует или данные в нем невалидны, получает новый токен доступа, вызывая метод `_fetch_and_cache_access_token`.
6.  Создает новый идентификатор сессии, вызывая метод `_create_and_cache_session`.
7.  Возвращает полученные токен доступа и идентификатор сессии.

### `_fetch_and_cache_access_token`

```python
@staticmethod
async def _fetch_and_cache_access_token(session: aiohttp.ClientSession) -> str:
    """
    Получает токен доступа с использованием BeautifulSoup для парсинга HTML и кэширует его.

    Args:
        session (aiohttp.ClientSession): Асинхронная клиентская сессия.

    Returns:
        str: Токен доступа.

    Raises:
        MissingRequirementsError: Если библиотека `beautifulsoup4` не установлена.
    """
```

**Как работает функция**:
1.  Проверяет, установлена ли библиотека `beautifulsoup4`. Если нет, вызывает исключение `MissingRequirementsError`.
2.  Определяет URL для аутентификации и заголовки запроса.
3.  Выполняет GET-запрос к URL аутентификации.
4.  Если запрос успешен (status code 200), извлекает HTML из ответа.
5.  Использует BeautifulSoup для парсинга HTML и поиска элемента `<pre>` с id `token`.
6.  Извлекает текст из найденного элемента, удаляет пробелы и кэширует токен, вызывая метод `_save_cached_data`.
7.  Возвращает полученный токен.

### `_create_and_cache_session`

```python
@staticmethod
async def _create_and_cache_session(session: aiohttp.ClientSession, access_token: str) -> str:
    """
    Создает идентификатор сессии, используя предоставленный токен доступа, и кэширует его.

    Args:
        session (aiohttp.ClientSession): Асинхронная клиентская сессия.
        access_token (str): Токен доступа.

    Returns:
        str: Идентификатор сессии.

    Raises:
        Exception: Если возникает ошибка аутентификации или ошибка валидации входных данных.
    """
```

**Как работает функция**:
1. Определяет URL для создания сессии и заголовки запроса, включая токен доступа.
2. Выполняет GET-запрос к URL создания сессии.
3. Если запрос успешен (status code 200), извлекает JSON из ответа.
4. Извлекает идентификатор сессии из JSON-данных.
5. Кэширует идентификатор сессии, вызывая метод `_update_cached_data`.
6. Возвращает полученный идентификатор сессии.
7. Если запрос не успешен, обрабатывает ошибки аутентификации (401) и ошибки валидации (422), вызывая исключения.

### `_save_cached_data`

```python
@staticmethod
def _save_cached_data(new_data: dict):
    """
    Сохраняет новые данные в файл кэша.

    Args:
        new_data (dict): Словарь с данными для сохранения.
    """
```

**Как работает функция**:
1.  Создает директорию для кэширования, если она не существует.
2.  Создает файл кэша, если он не существует.
3.  Открывает файл кэша для записи.
4.  Сохраняет предоставленные данные в файл кэша в формате JSON.

### `_update_cached_data`

```python
@staticmethod
def _update_cached_data(updated_data: dict):
    """
    Обновляет существующие данные в файле кэша новыми значениями.

    Args:
        updated_data (dict): Словарь с данными для обновления.
    """
```

**Как работает функция**:
1.  Инициализирует пустой словарь для хранения данных.
2.  Проверяет наличие файла кэша.
3.  Если файл кэша существует, пытается загрузить из него существующие данные.
4.  Если при загрузке данных возникает ошибка JSONDecodeError, начинает с пустого словаря.
5.  Обновляет загруженные данные данными из параметра `updated_data`.
6.  Открывает файл кэша для записи.
7.  Сохраняет обновленные данные в файл кэша в формате JSON.

### `_clear_cached_data`

```python
@staticmethod
def _clear_cached_data():
    """
    Удаляет файл кэша.
    """
```

**Как работает функция**:
1.  Пытается удалить файл кэша, если он существует.
2.  Логирует любые исключения, возникающие в процессе удаления файла.

### `_get_cached_data`

```python
@staticmethod
def _get_cached_data() -> dict:
    """
    Получает все закэшированные данные.

    Returns:
        dict: Словарь с закэшированными данными.
    """
```

**Как работает функция**:
1.  Проверяет наличие файла кэша.
2.  Если файл кэша существует, пытается загрузить из него данные.
3.  Если при загрузке данных возникает ошибка JSONDecodeError, возвращает пустой словарь.
4.  Возвращает загруженные данные. Если файл кэша не существует, возвращает пустой словарь.

## Параметры класса

- `label` (str): Метка провайдера "API Robocoders AI".
- `url` (str): URL документации API Robocoders AI ("https://api.robocoders.ai/docs").
- `api_endpoint` (str): URL конечной точки API для чата ("https://api.robocoders.ai/chat").
- `working` (bool): Флаг, указывающий на работоспособность API (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (в данном случае `True`).
- `default_model` (str): Модель агента по умолчанию ('GeneralCodingAgent').
- `agent` (list): Список доступных моделей агентов, включая `default_model`, "RepoAgent" и "FrontEndAgent".
- `models` (list): Список доступных моделей, идентичный `agent`.
- `CACHE_DIR` (Path): Путь к директории для кэширования.
- `CACHE_FILE` (Path): Путь к файлу кэша (`robocoders.json`).

## Примеры

Пример использования класса `RobocodersAPI` для создания асинхронного генератора и получения ответов от API:

```python
import asyncio
from typing import AsyncGenerator, List

from g4f.models import Model, GENERAL
from g4f.providers.RobocodersAPI import RobocodersAPI

async def generate_responses(model: str, messages: List[dict]) -> AsyncGenerator[str, None]:
    """
    Генерирует ответы с использованием RobocodersAPI.

    Args:
        model (str): Модель для использования.
        messages (List[dict]): Список сообщений для отправки.

    Yields:
        str: Ответы от API.
    """
    async for response in RobocodersAPI.create_async_generator(model=model, messages=messages):
        yield response

async def main():
    """
    Пример асинхронного использования RobocodersAPI.
    """
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    model = 'GeneralCodingAgent'  # or any other supported model

    async for message in generate_responses(model, messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

Пример получения токена доступа и идентификатора сессии:

```python
import asyncio
import aiohttp

from g4f.providers.RobocodersAPI import RobocodersAPI

async def get_access_and_session():
    """
    Пример получения токена доступа и идентификатора сессии.
    """
    async with aiohttp.ClientSession() as session:
        access_token, session_id = await RobocodersAPI._get_or_create_access_and_session(session)
        print(f"Access Token: {access_token}")
        print(f"Session ID: {session_id}")

if __name__ == "__main__":
    asyncio.run(get_access_and_session())