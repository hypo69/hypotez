# Модуль `FlowGpt`

## Обзор

Модуль `FlowGpt` предназначен для взаимодействия с сервисом FlowGPT для генерации текста на основе предоставленных сообщений. Он поддерживает различные модели, включая `gpt-3.5-turbo`, `gpt-4-turbo`, `google-gemini` и другие. Модуль использует асинхронный генератор для обработки ответов от FlowGPT и предоставляет возможность использования прокси-сервера.

## Подробней

Модуль `FlowGpt` является асинхронным провайдером, взаимодействующим с API FlowGPT для генерации текста. Он поддерживает настройку модели, передачу истории сообщений и системные сообщения. Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов.

## Классы

### `FlowGpt`

**Описание**: Класс `FlowGpt` реализует взаимодействие с FlowGPT для генерации текста.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL для взаимодействия с FlowGPT.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь с псевдонимами моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от FlowGPT.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    temperature: float = 0.7,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от FlowGPT.

    Args:
        cls (FlowGpt): Ссылка на класс.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        temperature (float, optional): Температура генерации. По умолчанию 0.7.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов.

    Raises:
        Exception: В случае ошибки при выполнении запроса.
    """
```

**Назначение**: Создает и возвращает асинхронный генератор, который отправляет запросы к FlowGPT и возвращает ответы в виде чанков текста.

**Параметры**:
- `cls` (FlowGpt): Ссылка на класс.
- `model` (str): Имя модели, которую нужно использовать для генерации ответа.
- `messages` (Messages): Список сообщений, представляющий историю разговора. Каждое сообщение содержит роль (`user` или `assistant`) и содержимое.
- `proxy` (str, optional): URL прокси-сервера, если необходимо использовать прокси для подключения к FlowGPT. По умолчанию `None`.
- `temperature` (float, optional): Параметр, определяющий случайность генерируемого текста. Значение по умолчанию - 0.7. Чем выше значение, тем более случайным будет текст.
- `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий чанки текста ответа от FlowGPT.

**Вызывает исключения**:
- `Exception`: Вызывается в случае возникновения ошибок при создании сессии, отправке запроса или обработке ответа от FlowGPT.

**Как работает функция**:

1.  **Подготовка данных**:
    *   Получает имя модели, приводит к нижнему регистру.
    *   Создает timestamp (время в секундах от начала эпохи Unix).
    *   Генерирует случайные данные для заголовков запроса: `nonce` (случайное шестнадцатеричное число) и `signature` (MD5-хеш данных, включающих timestamp, nonce и authorization token).
2.  **Формирование заголовков**:
    *   Создает словарь `headers` с необходимыми HTTP-заголовками, включая `User-Agent`, `Content-Type`, `Authorization` и другие. Заголовки включают сгенерированные `nonce`, `signature` и `timestamp`.
3.  **Создание сессии `aiohttp`**:
    *   Использует `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов. Сессия создается с заданными заголовками.
4.  **Подготовка тела запроса**:
    *   Извлекает историю сообщений из переданного списка `messages`, исключая системные сообщения.
    *   Формирует системное сообщение из содержимого всех сообщений с ролью `system`. Если системные сообщения отсутствуют, используется сообщение по умолчанию "You are helpful assistant. Follow the user's instructions carefully.".
    *   Создает словарь `data` с данными для отправки в теле запроса. Данные включают модель, флаг `nsfw`, вопрос пользователя, историю сообщений, системное сообщение, температуру и другие параметры.
5.  **Отправка POST-запроса**:
    *   Отправляет POST-запрос к API FlowGPT (`https://prod-backend-k8s.flowgpt.com/v3/chat-anonymous`) с телом запроса `data` и использованием прокси, если он указан.
6.  **Обработка ответа**:
    *   Получает ответ от сервера и проверяет его статус код. В случае ошибки вызывает исключение.
    *   Итерируется по чанкам содержимого ответа.
    *   Для каждого чанка проверяет, не является ли он пустым.
    *   Декодирует чанк как JSON.
    *   Проверяет наличие ключа `event` в JSON.
    *   Если `event` равен `"text"`, извлекает данные из ключа `data` и возвращает их через `yield`, делая функцию генератором.

```
Подготовка данных
     │
     ▼
Формирование заголовков 
     │
     ▼
Создание сессии aiohttp
     │
     ▼
  Подготовка тела запроса
     │
     ▼
    Отправка POST-запроса
     │
     ▼
       Обработка ответа
       │
       ▼
      Конец
```

**Примеры**:

```python
# Пример использования create_async_generator
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]
model = "gpt-3.5-turbo"

async def example():
    generator = await FlowGpt.create_async_generator(model=model, messages=messages)
    async for chunk in generator:
        print(chunk)

# Запуск примера
# asyncio.run(example())
```
```python
# Пример использования create_async_generator с прокси
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]
model = "gpt-3.5-turbo"
proxy = "http://your_proxy:8080"

async def example_with_proxy():
    generator = await FlowGpt.create_async_generator(model=model, messages=messages, proxy=proxy)
    async for chunk in generator:
        print(chunk)

# Запуск примера
# asyncio.run(example_with_proxy())
```
```python
# Пример использования create_async_generator с temperature
messages = [
    {"role": "user", "content": "Tell me a story."},
]
model = "gpt-3.5-turbo"
temperature = 0.9

async def example_with_temperature():
    generator = await FlowGpt.create_async_generator(model=model, messages=messages, temperature=temperature)
    async for chunk in generator:
        print(chunk)

# Запуск примера
# asyncio.run(example_with_temperature())