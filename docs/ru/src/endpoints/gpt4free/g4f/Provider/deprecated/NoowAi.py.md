# Модуль `NoowAi`

## Обзор

Модуль `NoowAi` предоставляет асинхронный генератор для взаимодействия с сервисом NoowAi.com. Он поддерживает использование истории сообщений и модель `gpt-3.5-turbo`. Модуль предназначен для интеграции с `gpt4free` для предоставления доступа к ответам, сгенерированным NoowAi.

## Подробнее

Этот модуль реализует класс `NoowAi`, который является асинхронным провайдером генератора. Он отправляет запросы к API NoowAi и возвращает сгенерированные ответы.  Для отправки запросов используется `aiohttp`, для работы с асинхронностью.

## Классы

### `NoowAi`

**Описание**: Класс `NoowAi` предназначен для асинхронного взаимодействия с API NoowAi.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL сервиса NoowAi (`https://noowai.com`).
- `supports_message_history` (bool): Указывает, поддерживается ли история сообщений (значение `True`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживается ли модель `gpt-3.5-turbo` (значение `True`).
- `working` (bool): Указывает, находится ли провайдер в рабочем состоянии (значение `False`).

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
    """Создает асинхронный генератор для взаимодействия с NoowAi.

    Args:
        model (str): Используемая модель (например, `gpt-3.5-turbo`).
        messages (Messages): Список сообщений для отправки в NoowAi.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от NoowAi.

    Raises:
        RuntimeError: Если получен некорректный ответ от NoowAi.
    """
```

**Назначение**: Создает и возвращает асинхронный генератор, который отправляет сообщения в NoowAi и выдает результаты по мере их поступления.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от NoowAi.

**Вызывает исключения**:
- `RuntimeError`: Если получен поврежденный ответ от NoowAi или если в ответе указана ошибка.

**Как работает функция**:

1. **Определение заголовков**: Функция определяет заголовки HTTP-запроса, включая User-Agent, Accept, Referer, Content-Type и Origin.
2. **Создание сессии `aiohttp`**: Создается асинхронная HTTP-сессия с заданными заголовками.
3. **Формирование данных запроса**: Создается словарь `data`, содержащий информацию о запросе, включая идентификаторы бота, сессии, чата и контекста, а также список сообщений и новое сообщение.
4. **Отправка POST-запроса**: Отправляется POST-запрос к API NoowAi (`{cls.url}/wp-json/mwai-ui/v1/chats/submit`) с данными запроса и прокси-сервером (если указан).
5. **Обработка ответа**: Функция асинхронно перебирает строки в ответе. Если строка начинается с `b"data: "`, она пытается распарсить JSON из этой строки.
6. **Извлечение данных**: Если распарсинг успешен и в JSON есть ключ `"type"`, функция проверяет значение этого ключа.
   - Если `"type" == "live"`, функция выдает значение ключа `"data"`.
   - Если `"type" == "end"`, функция завершает генератор.
   - Если `"type" == "error"`, функция вызывает исключение `RuntimeError` с сообщением об ошибке из ключа `"data"`.
7. **Обработка ошибок**: Если при распарсинге JSON возникает ошибка, функция вызывает исключение `RuntimeError` с сообщением о поврежденной строке.

```
     Определение заголовков HTTP-запроса
     ↓
     Создание сессии aiohttp
     ↓
     Формирование данных запроса
     ↓
     Отправка POST-запроса к API NoowAi
     ↓
     Обработка ответа (перебор строк)
     │
     ├── Строка начинается с "data: "?
     │   └── Да:
     │       │
     │       └── Попытка распарсить JSON
     │           │
     │           └── Успешно?
     │               ├── Да:
     │               │   │
     │               │   └── Проверка значения "type"
     │               │       │
     │               │       ├── "type" == "live"?
     │               │       │   └── Да: Выдача значения "data"
     │               │       │
     │               │       ├── "type" == "end"?
     │               │       │   └── Да: Завершение генератора
     │               │       │
     │               │       ├── "type" == "error"?
     │               │       │   └── Да: Вызов исключения RuntimeError с сообщением об ошибке
     │               │       │
     │               │       └── Нет: Продолжение обработки
     │               │
     │               └── Нет: Вызов исключения RuntimeError с сообщением о поврежденной строке
     │
     └── Нет: Продолжение обработки
```

**Примеры**:

```python
# Пример использования асинхронного генератора NoowAi
async def example():
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "user", "content": "Привет, как дела?"}
    ]
    async for message in NoowAi.create_async_generator(model=model, messages=messages):
        print(message)

# Запуск примера
# import asyncio
# asyncio.run(example())