# Модуль WhiteRabbitNeo

## Обзор

Модуль `WhiteRabbitNeo` предоставляет асинхронный генератор для взаимодействия с провайдером WhiteRabbitNeo. Он поддерживает сохранение истории сообщений и требует аутентификацию.

## Подробнее

Этот модуль предназначен для асинхронного взаимодействия с API WhiteRabbitNeo. Он использует `aiohttp` для выполнения HTTP-запросов и предоставляет метод `create_async_generator` для создания асинхронного генератора, который возвращает чанки данных из API. Модуль также включает вспомогательные функции для получения cookies и создания коннектора.

## Классы

### `WhiteRabbitNeo`

**Описание**: Класс `WhiteRabbitNeo` является асинхронным провайдером генератора, предназначенным для взаимодействия с API WhiteRabbitNeo.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует от базового класса асинхронных провайдеров генераторов.

**Атрибуты**:
- `url` (str): URL-адрес WhiteRabbitNeo ("https://www.whiterabbitneo.com").
- `working` (bool): Флаг, указывающий, работает ли провайдер (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (True).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация для использования провайдера (True).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения данных от WhiteRabbitNeo.

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
        Создает асинхронный генератор для получения данных от WhiteRabbitNeo.

        Args:
            model (str): Модель, используемая для генерации ответа.
            messages (Messages): Список сообщений для отправки.
            cookies (Cookies, optional): Cookies для использования в запросе. По умолчанию `None`.
            connector (BaseConnector, optional): Коннектор для использования в сессии aiohttp. По умолчанию `None`.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий чанки данных.

        Raises:
            Exception: В случае ошибки при выполнении запроса.
        """
```

**Назначение**: Создает асинхронный генератор для получения данных от WhiteRabbitNeo.

**Параметры**:
- `model` (str): Модель, используемая для генерации ответа.
- `messages` (Messages): Список сообщений для отправки.
- `cookies` (Cookies, optional): Cookies для использования в запросе. По умолчанию `None`.
- `connector` (BaseConnector, optional): Коннектор для использования в сессии aiohttp. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий чанки данных.

**Вызывает исключения**:
- `Exception`: В случае ошибки при выполнении запроса.

**Как работает функция**:

1. **Инициализация**:
   - Проверяет наличие cookies, и если их нет, получает их с помощью `get_cookies("www.whiterabbitneo.com")`.
   - Определяет заголовки (`headers`) для HTTP-запроса, включая `User-Agent`, `Accept`, `Referer` и `Content-Type`.

2. **Создание сессии**:
   - Создает асинхронную сессию `aiohttp.ClientSession` с заданными заголовками, cookies и коннектором (если предоставлен).
   - Коннектор создается с помощью `get_connector(connector, proxy)`.

3. **Подготовка данных**:
   - Формирует словарь `data`, включающий сообщения (`messages`), случайный идентификатор (`id`), флаг улучшения промпта (`enhancePrompt`) и флаг использования функций (`useFunctions`).

4. **Выполнение запроса**:
   - Отправляет POST-запрос к API (`f"{cls.url}/api/chat"`) с данными в формате JSON и прокси (если указан).
   - Использует `raise_for_status(response)` для проверки статуса ответа.

5. **Обработка ответа**:
   - Итерируется по чанкам содержимого ответа (`response.content.iter_any()`).
   - Декодирует каждый чанк в строку, игнорируя ошибки декодирования (`chunk.decode(errors="ignore")`), и возвращает его через `yield`.

```
Инициализация Cookies, Headers
│
└── Создание сессии aiohttp.ClientSession
│
└── Подготовка данных (словарь data)
│
└── POST запрос к API WhiteRabbitNeo
│
└── Обработка ответа (итерация по чанкам)
│
└── Вывод чанков данных
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from aiohttp import TCPConnector

async def main():
    model = "default"
    messages = [{"role": "user", "content": "Hello, WhiteRabbitNeo!"}]
    cookies = {"example_cookie": "value"}
    connector = TCPConnector(limit=300)
    proxy = "http://your_proxy:8080"

    async for chunk in WhiteRabbitNeo.create_async_generator(model, messages, cookies, connector, proxy):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())