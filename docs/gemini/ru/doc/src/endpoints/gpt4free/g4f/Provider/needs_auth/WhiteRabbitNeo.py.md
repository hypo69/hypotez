# Модуль WhiteRabbitNeo

## Обзор

Модуль `WhiteRabbitNeo` предоставляет класс `WhiteRabbitNeo`, который реализует асинхронный генератор для взаимодействия с API WhiteRabbitNeo. 

## Подробнее

Класс `WhiteRabbitNeo` наследует от класса `AsyncGeneratorProvider` и предоставляет методы для асинхронной отправки запросов к API WhiteRabbitNeo и обработки ответов. 

## Классы

### `class WhiteRabbitNeo`

**Описание**: Класс, который реализует асинхронный генератор для взаимодействия с API WhiteRabbitNeo. 

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
 - `url (str)`: Базовый URL для взаимодействия с API WhiteRabbitNeo.
 - `working (bool)`: Флаг, указывающий на работоспособность провайдера.
 - `supports_message_history (bool)`: Флаг, указывающий на поддержку истории сообщений.
 - `needs_auth (bool)`: Флаг, указывающий на необходимость авторизации.

**Методы**:
 - `create_async_generator(model: str, messages: Messages, cookies: Cookies = None, connector: BaseConnector = None, proxy: str = None, **kwargs) -> AsyncResult`: Асинхронный метод, который создает генератор для взаимодействия с API WhiteRabbitNeo.

## Методы класса

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
        if cookies is None:
            cookies = get_cookies("www.whiterabbitneo.com")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": cls.url,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        async with ClientSession(
            headers=headers,
            cookies=cookies,
            connector=get_connector(connector, proxy)
        ) as session:
            data = {
                "messages": messages,
                "id": get_random_string(6),
                "enhancePrompt": False,
                "useFunctions": False
            }
            async with session.post(f"{cls.url}/api/chat", json=data, proxy=proxy) as response:
                await raise_for_status(response)
                async for chunk in response.content.iter_any():
                    if chunk:
                        yield chunk.decode(errors="ignore")
```

**Назначение**: Асинхронный метод, который создает генератор для взаимодействия с API WhiteRabbitNeo.

**Параметры**:
- `model (str)`: Имя модели для генерации текста.
- `messages (Messages)`: Список сообщений для отправки в API WhiteRabbitNeo.
- `cookies (Cookies, optional)`: Словарь с куки для авторизации. По умолчанию `None`.
- `connector (BaseConnector, optional)`: Объект `BaseConnector` для асинхронного HTTP-запроса. По умолчанию `None`.
- `proxy (str, optional)`: Прокси-сервер для асинхронного HTTP-запроса. По умолчанию `None`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от API WhiteRabbitNeo.

**Как работает функция**:

1. Проверяет, переданы ли куки в параметрах. Если нет, то получает куки для WhiteRabbitNeo.
2. Задает заголовки запроса. 
3. Создает сессию `ClientSession` с использованием заданных куки и `connector`.
4. Формирует данные запроса с сообщениями, уникальным ID и флагами.
5. Выполняет POST-запрос к `/api/chat` с использованием сформированных данных.
6. Проверяет статус ответа.
7. Итерирует по частям ответа и выдает их по одному, декодируя в UTF-8.

**Примеры**:

```python
async def example():
    messages = [
        {"role": "user", "content": "Привет, как дела?"}
    ]
    async for chunk in await WhiteRabbitNeo.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(chunk)