# Модуль WhiteRabbitNeo

## Обзор

Модуль `WhiteRabbitNeo` предоставляет асинхронный генератор для взаимодействия с провайдером WhiteRabbitNeo. Он поддерживает использование истории сообщений и требует аутентификации. Этот модуль предназначен для интеграции с gpt4free, обеспечивая возможность общаться с моделями, предоставляемыми WhiteRabbitNeo.

## Подробней

Модуль `WhiteRabbitNeo` является частью проекта `hypotez` и предназначен для работы с асинхронными запросами к API WhiteRabbitNeo. Он использует `aiohttp` для асинхронных HTTP-запросов и предоставляет функциональность для создания генератора, который возвращает чанки данных из ответов API. Модуль требует аутентификации, что подразумевает необходимость передачи cookies для успешного выполнения запросов.

## Классы

### `WhiteRabbitNeo`

**Описание**: Класс `WhiteRabbitNeo` является асинхронным провайдером, который взаимодействует с API WhiteRabbitNeo. Он наследуется от `AsyncGeneratorProvider` и предоставляет метод для создания асинхронного генератора, который возвращает чанки данных из ответов API.

**Наследует**:

- `AsyncGeneratorProvider`: базовый класс для асинхронных провайдеров, использующих генераторы.

**Атрибуты**:

- `url` (str): URL-адрес API WhiteRabbitNeo.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация для использования провайдера.

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API WhiteRabbitNeo.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        cookies: Cookies = None,
        connector: BaseConnector = None,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с API WhiteRabbitNeo.

        Args:
            model (str): Модель, используемая для генерации ответов.
            messages (Messages): Список сообщений для отправки в API.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            connector (BaseConnector, optional): Aiohttp коннектор для переиспользования соединений. По умолчанию `None`.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий чанки данных из ответов API.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.
        """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API WhiteRabbitNeo. Этот генератор отправляет сообщения в API и возвращает чанки данных из ответов.

**Параметры**:

- `model` (str): Модель, используемая для генерации ответов.
- `messages` (Messages): Список сообщений для отправки в API.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `connector` (BaseConnector, optional): Aiohttp коннектор для переиспользования соединений. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, возвращающий чанки данных из ответов API.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при выполнении запроса.

**Как работает функция**:

1. **Проверка и установка Cookies**: Если `cookies` не переданы, функция пытается получить их с домена `"www.whiterabbitneo.com"` с помощью функции `get_cookies`.
2. **Формирование заголовков**: Определяются HTTP-заголовки, включая `User-Agent`, `Accept`, `Referer`, `Content-Type` и другие, необходимые для запроса к API.
3. **Создание сессии**: Создается асинхронная сессия `aiohttp` с заданными заголовками, cookies и коннектором. Коннектор используется для переиспользования соединений, что может улучшить производительность. Если коннектор не передан, он создается с помощью функции `get_connector`.
4. **Формирование данных**: Создается словарь `data` с сообщениями (`messages`), случайным идентификатором (`id`), а также флагами `enhancePrompt` и `useFunctions`.
5. **Выполнение POST-запроса**: Выполняется асинхронный POST-запрос к API `f"{cls.url}/api/chat"` с данными `data` в формате JSON и установленным прокси (если он передан).
6. **Обработка ответа**: Для каждого чанка данных, полученного из ответа, выполняется декодирование (`chunk.decode(errors="ignore")`), и чанк возвращается через `yield`.
7. **Обработка ошибок**: Функция `raise_for_status` проверяет статус ответа и вызывает исключение в случае ошибки.

```
    Проверка Cookies
    │
    └──► Формирование заголовков HTTP
        │
        └──► Создание асинхронной сессии aiohttp
            │
            └──► Формирование данных для POST-запроса (JSON)
                │
                └──► Выполнение асинхронного POST-запроса к API
                    │
                    └──► Итерация по чанкам данных из ответа
                        │
                        └──► Декодирование чанка данных
                            │
                            └──► Генерация чанка данных (yield)
```

**Примеры**:

Пример 1: Использование `create_async_generator` с минимальными параметрами.

```python
messages = [{"role": "user", "content": "Hello, WhiteRabbitNeo!"}]
async for chunk in WhiteRabbitNeo.create_async_generator(model="default", messages=messages):
    print(chunk, end="")
```

Пример 2: Использование `create_async_generator` с cookies и прокси.

```python
messages = [{"role": "user", "content": "Hello, WhiteRabbitNeo!"}]
cookies = {"session_id": "1234567890"}
proxy = "http://proxy.example.com:8080"
async for chunk in WhiteRabbitNeo.create_async_generator(model="default", messages=messages, cookies=cookies, proxy=proxy):
    print(chunk, end="")
```