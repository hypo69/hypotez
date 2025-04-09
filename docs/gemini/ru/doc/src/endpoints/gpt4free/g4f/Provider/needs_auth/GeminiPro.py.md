# Модуль для работы с Google Gemini API (GeminiPro)

## Обзор

Модуль `GeminiPro.py` предназначен для взаимодействия с API Google Gemini, в частности с моделью Gemini Pro. Он обеспечивает асинхронную генерацию текста, поддержку истории сообщений, системных сообщений и аутентификацию через API-ключ. Модуль позволяет использовать как потоковую, так и не потоковую генерацию контента, а также поддерживает отправку медиа-файлов.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими частями проекта, требующими взаимодействия с Google Gemini API. Он предоставляет удобный интерфейс для отправки запросов к API и получения ответов, а также обрабатывает ошибки и возвращает результаты в нужном формате.

## Классы

### `GeminiPro`

**Описание**: Класс `GeminiPro` предоставляет функциональность для взаимодействия с Google Gemini API.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, значение "Google Gemini API".
- `url` (str): URL документации Google AI.
- `login_url` (str): URL для получения API-ключа Google AI Studio.
- `api_base` (str): Базовый URL API Google Generative Language.
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (True).
- `default_model` (str): Модель по умолчанию ("gemini-1.5-pro").
- `default_vision_model` (str): Модель для обработки изображений (совпадает с `default_model`).
- `fallback_models` (list[str]): Список резервных моделей.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `get_models()`: Получает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с API.

## Функции

### `get_models`

```python
    @classmethod
    def get_models(cls, api_key: str = None, api_base: str = api_base) -> list[str]:
        """
        Возвращает список доступных моделей Gemini API.

        Args:
            api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
            api_base (str, optional): Базовый URL API. По умолчанию `api_base` класса.

        Returns:
            list[str]: Список имен моделей.

        Raises:
            MissingAuthError: Если `api_key` не указан и не удалось получить список моделей.

        Как работает функция:
        1. Проверяет, если список моделей уже был получен ранее. Если да, возвращает его.
        2. Если список моделей пуст, пытается получить его из API.
        3. Формирует URL для запроса списка моделей.
        4. Отправляет GET-запрос к API с использованием `requests`.
        5. Проверяет статус ответа и вызывает исключение, если произошла ошибка.
        6. Извлекает имена моделей из JSON-ответа и сохраняет их в `cls.models`.
        7. В случае ошибки логирует её и возвращает список резервных моделей.
        """
        ...
```

**Назначение**: Получение списка доступных моделей Gemini API.

**Параметры**:
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL API. По умолчанию `api_base` класса.

**Возвращает**:
- `list[str]`: Список имен моделей.

**Вызывает исключения**:
- `MissingAuthError`: Если `api_key` не указан и не удалось получить список моделей.

**Как работает функция**:
```
A[Проверка наличия моделей в cls.models]
│
├─── True ───> B[Возврат cls.models]
│
└─── False ───> C[Попытка получения моделей из API]
│
D[Формирование URL для запроса списка моделей]
│
E[Отправка GET-запроса к API]
│
F[Проверка статуса ответа]
│
├─── Успешно ───> G[Извлечение имен моделей из JSON-ответа]
│   │
│   H[Сохранение имен моделей в cls.models]
│   │
│   I[Возврат cls.models]
│
└─── Ошибка ───> J[Логирование ошибки]
│
K[Возврат списка резервных моделей fallback_models]
```

**Примеры**:

```python
models = GeminiPro.get_models(api_key="your_api_key")
print(models)
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = False,
        proxy: str = None,
        api_key: str = None,
        api_base: str = api_base,
        use_auth_header: bool = False,
        media: MediaListType = None,
        tools: Optional[list] = None,
        connector: BaseConnector = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с Gemini API.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки в API.
            stream (bool, optional): Флаг, указывающий на использование потоковой генерации. По умолчанию `False`.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
            api_base (str, optional): Базовый URL API. По умолчанию `api_base` класса.
            use_auth_header (bool, optional): Флаг, указывающий на использование заголовка авторизации. По умолчанию `False`.
            media (MediaListType, optional): Список медиа-файлов для отправки. По умолчанию `None`.
            tools (Optional[list], optional): Список инструментов, которые будут использоваться. По умолчанию `None`.
            connector (BaseConnector, optional): HTTP-коннектор aiohttp. По умолчанию `None`.
            **kwargs: Дополнительные параметры для конфигурации генерации.

        Returns:
            AsyncResult: Асинхронный генератор для получения ответов от API.

        Raises:
            MissingAuthError: Если `api_key` не указан.

        Как работает функция:
        1. Проверяет наличие API-ключа и вызывает исключение, если он не указан.
        2. Получает имя модели, используя `cls.get_model`.
        3. Формирует заголовки и параметры запроса в зависимости от способа аутентификации.
        4. Определяет метод API в зависимости от флага `stream`.
        5. Формирует URL для запроса.
        6. Создает `ClientSession` aiohttp для выполнения запросов.
        7. Преобразует сообщения в формат, требуемый API.
        8. Добавляет медиа-файлы в запрос, если они указаны.
        9. Формирует тело запроса с сообщениями, конфигурацией генерации и инструментами.
        10. Отправляет POST-запрос к API.
        11. Обрабатывает ответ API:
            - Если `stream` равен `True`, обрабатывает потоковые ответы.
            - Если `stream` равен `False`, обрабатывает не потоковые ответы.
        12. Возвращает асинхронный генератор для получения ответов.
        """
        ...
```

**Назначение**: Создание асинхронного генератора для взаимодействия с Gemini API.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `stream` (bool, optional): Флаг, указывающий на использование потоковой генерации. По умолчанию `False`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL API. По умолчанию `api_base` класса.
- `use_auth_header` (bool, optional): Флаг, указывающий на использование заголовка авторизации. По умолчанию `False`.
- `media` (MediaListType, optional): Список медиа-файлов для отправки. По умолчанию `None`.
- `tools` (Optional[list], optional): Список инструментов, которые будут использоваться. По умолчанию `None`.
- `connector` (BaseConnector, optional): HTTP-коннектор aiohttp. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для конфигурации генерации.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от API.

**Вызывает исключения**:
- `MissingAuthError`: Если `api_key` не указан.

**Как работает функция**:

```
A[Проверка наличия API-ключа]
│
├─── Нет API-ключа ───> B[Выброс исключения MissingAuthError]
│
└─── Есть API-ключ ───> C[Получение имени модели]
│
D[Формирование заголовков и параметров запроса]
│
E[Определение метода API (streamGenerateContent или generateContent)]
│
F[Формирование URL для запроса]
│
G[Создание ClientSession aiohttp]
│
H[Преобразование сообщений в формат API]
│
I[Добавление медиа-файлов (если есть)]
│
J[Формирование тела запроса (сообщения, конфигурация, инструменты)]
│
K[Отправка POST-запроса к API]
│
L[Обработка ответа API]
│
├─── stream = True ───> M[Обработка потоковых ответов]
│
└─── stream = False ───> N[Обработка не потоковых ответов]
│
O[Возврат асинхронного генератора]
```

**Примеры**:

```python
async def main():
    messages = [{"role": "user", "content": "Hello, Gemini!"}]
    async for response in GeminiPro.create_async_generator(model="gemini-1.5-pro", messages=messages, api_key="your_api_key"):
        print(response)

import asyncio
asyncio.run(main())