# Модуль WhiteRabbitNeo

## Обзор

Модуль `WhiteRabbitNeo` представляет собой асинхронный провайдер, предназначенный для взаимодействия с сервисом WhiteRabbitNeo (www.whiterabbitneo.com).
Он поддерживает использование истории сообщений и требует аутентификации.
Модуль использует асинхронные запросы для обмена данными и предоставляет функциональность для генерации текста на основе предоставленных сообщений.

## Подробнее

Этот модуль является частью системы, которая позволяет взаимодействовать с различными поставщиками услуг генерации текста, такими как WhiteRabbitNeo.
Он обеспечивает асинхронное взаимодействие, что позволяет эффективно обрабатывать запросы, не блокируя основной поток выполнения.
Модуль предназначен для использования в системах, требующих аутентификации и поддерживающих историю сообщений.

## Классы

### `WhiteRabbitNeo`

**Описание**: Класс `WhiteRabbitNeo` является асинхронным провайдером, который взаимодействует с сервисом WhiteRabbitNeo для генерации текста.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует от этого класса функциональность асинхронного генератора.

**Атрибуты**:
- `url` (str): URL сервиса WhiteRabbitNeo (`https://www.whiterabbitneo.com`).
- `working` (bool): Указывает, работает ли данный провайдер (в данном случае `True`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (`True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера (`True`).

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с сервисом WhiteRabbitNeo.

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
    """ Создает асинхронный генератор для взаимодействия с сервисом WhiteRabbitNeo.

    Args:
        cls (WhiteRabbitNeo): Ссылка на класс `WhiteRabbitNeo`.
        model (str): Модель, используемая для генерации текста.
        messages (Messages): Список сообщений для отправки в сервис.
        cookies (Cookies, optional): Файлы cookie для аутентификации. По умолчанию `None`.
        connector (BaseConnector, optional): Асинхронный коннектор для пула соединений. По умолчанию `None`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий чанки сгенерированного текста.

    Raises:
        Exception: Если возникает ошибка при создании или использовании асинхронного генератора.

    Как работает функция:
        Функция создает асинхронный генератор, который отправляет сообщения в сервис WhiteRabbitNeo и получает сгенерированный текст.
        Она использует `aiohttp.ClientSession` для отправки запросов и получения ответов.
        Если файлы cookie не предоставлены, они извлекаются с использованием `get_cookies()`.
        Заголовки запроса устанавливаются для имитации запроса из браузера.
        Данные запроса формируются в виде словаря, содержащего сообщения, идентификатор и флаги.
        Функция итерирует по чанкам ответа и декодирует их, чтобы выдать сгенерированный текст.
    """

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
        """Создает асинхронный генератор для взаимодействия с сервисом WhiteRabbitNeo.

        Args:
            model (str): Модель для генерации текста.
            messages (Messages): Список сообщений для отправки в сервис.
            cookies (Cookies, optional): Cookie для аутентификации. Defaults to None.
            connector (BaseConnector, optional): Async коннектор для пула соединений. Defaults to None.
            proxy (str, optional): Адрес прокси-сервера. Defaults to None.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий чанки сгенерированного текста.
        """

        async def inner_function():
            """Внутренняя асинхронная функция, выполняющая запрос к API и генерирующая чанки ответа.

            Args:
                Нет явных аргументов, но использует переменные из внешней области видимости:
                `cls`, `messages`, `cookies`, `connector`, `proxy`.

            Yields:
                bytes: Декодированные чанки сгенерированного текста.

            Raises:
                Exception: Если возникает ошибка при выполнении запроса или обработке ответа.

            Как работает функция:
                1. Проверяет наличие переданных cookies, если cookies не переданы - пытается получить их, вызвав `get_cookies("www.whiterabbitneo.com")`.
                2. Определяет заголовки HTTP-запроса, включая User-Agent, Accept, Referer и Content-Type.
                3. Создаёт `ClientSession` aiohttp для управления HTTP-соединениями. Использует либо переданный `connector`, либо создает новый с помощью `get_connector(connector, proxy)`.
                4. Формирует структуру данных `data` для отправки в теле запроса, включая `messages`, случайный `id` и флаги `enhancePrompt` и `useFunctions`.
                5. Отправляет POST-запрос к API-endpoint `/api/chat` на `cls.url` (URL WhiteRabbitNeo).
                6. Обрабатывает ответ: проверяет статус код с помощью `raise_for_status(response)` (вызывает исключение, если статус код указывает на ошибку).
                7. Итерирует по содержимому ответа (`response.content.iter_any()`), декодирует каждый чанк и возвращает его через `yield`.

            """
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

    #Примеры:
    #   Примеры вызовов со всем спектром параметров. которые можно передать в функцию

## Параметры класса
- `url` (str): URL сервиса WhiteRabbitNeo (`https://www.whiterabbitneo.com`).
- `working` (bool): Указывает, работает ли данный провайдер (в данном случае `True`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (`True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера (`True`).