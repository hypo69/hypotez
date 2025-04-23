# Документация модуля `Opchatgpts`

## Обзор

Модуль `Opchatgpts` представляет собой асинхронный провайдер для взаимодействия с сервисом Opchatgpts.net.
Он позволяет генерировать ответы на основе предоставленных сообщений, используя GPT-3.5 Turbo. Модуль поддерживает историю сообщений.

## Более подробная информация

Модуль предназначен для интеграции с другими частями проекта, где требуется взаимодействие с Opchatgpts.net для генерации текста.
Он использует асинхронные запросы для неблокирующей работы.

## Классы

### `Opchatgpts`

**Описание**: Класс `Opchatgpts` является асинхронным провайдером.

**Наследует**:
- `AsyncGeneratorProvider`: базовый класс для асинхронных провайдеров, генерирующих данные.

**Атрибуты**:
- `url` (str): URL-адрес сервиса Opchatgpts.net.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.

**Принцип работы**:
Класс `Opchatgpts` предназначен для асинхронного взаимодействия с API Opchatgpts.net. Он отправляет сообщения и получает ответы, используя асинхронные генераторы.
Класс использует `aiohttp.ClientSession` для выполнения HTTP-запросов.

### Методы класса

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None, **kwargs) -> AsyncResult:
        """Создает асинхронный генератор для получения ответов от Opchatgpts.net.

        Args:
            cls (Opchatgpts): Ссылка на класс.
            model (str): Модель для использования (например, "gpt-3.5-turbo").
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий текстовые ответы.

        Raises:
            RuntimeError: Если получен поврежденный ответ от сервера.
            aiohttp.ClientResponseError: В случае неудачного HTTP-ответа.

        Как работает функция:
        - Функция создает заголовки для HTTP-запроса.
        - Инициализирует асинхронную сессию `ClientSession` с заданными заголовками.
        - Формирует JSON-данные для отправки, включая `botId`, `chatId`, `contextId`, `messages` и другие параметры.
        - Отправляет POST-запрос к API Opchatgpts.net.
        - Получает ответ в виде потока данных и обрабатывает его построчно.
        - Проверяет, начинается ли строка с `b"data: "`. Если да, пытается загрузить JSON из этой строки.
        - Проверяет наличие ключа `"type"` в загруженном JSON.
        - Если `line["type"] == "live"`, выдает данные (`line["data"]`).
        - Если `line["type"] == "end"`, завершает генератор.
        """
```

#### Параметры функции `create_async_generator`

- `cls` (Opchatgpts): Ссылка на класс.
- `model` (str): Модель для использования (например, "gpt-3.5-turbo").
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Примеры**:

```python
# Пример вызова create_async_generator
messages = [{"role": "user", "content": "Hello, world!"}]
async for message in Opchatgpts.create_async_generator(model="gpt-3.5-turbo", messages=messages):
    print(message)
```
```python
# Пример вызова create_async_generator c прокси
messages = [{"role": "user", "content": "Hello, world!"}]
async for message in Opchatgpts.create_async_generator(model="gpt-3.5-turbo", messages=messages, proxy="http://proxy.example.com"):
    print(message)
```
```python
# Пример обработки ошибки при вызове create_async_generator
messages = [{"role": "user", "content": "Hello, world!"}]
try:
    async for message in Opchatgpts.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message)
except RuntimeError as ex:
    logger.error("Ошибка при получении ответа от Opchatgpts", ex, exc_info=True)