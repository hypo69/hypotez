# Модуль `WhiteRabbitNeo.py`

## Обзор

Модуль `WhiteRabbitNeo.py` предназначен для работы с провайдером WhiteRabbitNeo, который требует аутентификацию. Он использует асинхронные запросы для взаимодействия с API WhiteRabbitNeo и предоставляет функциональность для генерации текста на основе предоставленных сообщений.

## Более детально

Этот модуль реализует класс `WhiteRabbitNeo`, который является подклассом `AsyncGeneratorProvider`. Он отвечает за создание асинхронного генератора для получения ответов от API WhiteRabbitNeo. Модуль использует библиотеки `aiohttp` для выполнения асинхронных HTTP-запросов и включает механизмы для обработки cookies, установки заголовков и прокси.

## Классы

### `WhiteRabbitNeo`

**Описание**:
Класс `WhiteRabbitNeo` представляет собой асинхронный провайдер, взаимодействующий с API WhiteRabbitNeo.

**Наследует**:
- `AsyncGeneratorProvider`: Этот класс наследует функциональность асинхронного генератора от `AsyncGeneratorProvider`.

**Атрибуты**:
- `url` (str): URL-адрес сервиса WhiteRabbitNeo (`"https://www.whiterabbitneo.com"`).
- `working` (bool): Указывает, работает ли провайдер (`True`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (`True`).
- `needs_auth` (bool): Указывает, требуется ли аутенентификация(`True`).

**Принцип работы**:
Класс использует асинхронные запросы для отправки сообщений к API WhiteRabbitNeo и получения ответов в виде асинхронного генератора. Он также обрабатывает cookies и заголовки для обеспечения правильного взаимодействия с API.

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
        """ Создает асинхронный генератор для взаимодействия с API WhiteRabbitNeo.

        Args:
            model (str): Модель, используемая для генерации текста.
            messages (Messages): Список сообщений для отправки в API.
            cookies (Cookies, optional): Cookies для использования в запросах. По умолчанию `None`.
            connector (BaseConnector, optional): Aiohttp connector. Defaults to None.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.

        Raises:
            Exception: Если возникает ошибка при взаимодействии с API.

        Пример:
            Примеры вызовов с полным набором параметров, которые можно передать в функцию.
        """
```

#### Параметры:
- `model` (str): Модель, используемая для генерации текста.
- `messages` (Messages): Список сообщений для отправки в API.
- `cookies` (Cookies, optional): Cookies для использования в запросах. Defaults to `None`.
- `connector` (BaseConnector, optional): Aiohttp connector. Defaults to None.
- `proxy` (str, optional): Прокси-сервер для использования. Defaults to `None`.
- `**kwargs`: Дополнительные параметры.

#### Как работает функция:
1. **Проверка и установка cookies**: Если cookies не предоставлены, они получаются с домена `"www.whiterabbitneo.com"`.
2. **Формирование заголовков**: Создаются заголовки HTTP-запроса, включая User-Agent, Accept, Referer и Content-Type.
3. **Создание асинхронной сессии**: Используется `aiohttp.ClientSession` для выполнения асинхронных запросов с заданными заголовками, cookies и прокси.
4. **Формирование данных запроса**: Создается словарь `data`, включающий сообщения, случайный идентификатор, а также флаги `enhancePrompt` и `useFunctions`.
5. **Выполнение POST-запроса**: Отправляется POST-запрос к API (`f"{cls.url}/api/chat"`) с данными в формате JSON.
6. **Обработка ответа**:
   - Вызывается функция `raise_for_status` для проверки статуса ответа.
   - Ответ обрабатывается по частям (chunks) с использованием асинхронного итератора `response.content.iter_any()`.
   - Каждая часть декодируется и передается через генератор.

#### Примеры:

```python
# Пример вызова функции create_async_generator
model = "default"
messages = [{"role": "user", "content": "Hello, world!"}]
cookies = {"session_id": "12345"}
proxy = "http://proxy.example.com"

async def main():
    generator = await WhiteRabbitNeo.create_async_generator(
        model=model,
        messages=messages,
        cookies=cookies,
        proxy=proxy
    )
    async for chunk in generator:
        print(chunk)

# Запуск примера (необходимо находиться внутри асинхронной функции)
# import asyncio
# asyncio.run(main())
```