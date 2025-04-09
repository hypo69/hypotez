# Модуль для работы с Perplexity Labs
## Обзор

Модуль `PerplexityLabs` предоставляет асинхронный интерфейс для взаимодействия с API Perplexity Labs. Он позволяет отправлять сообщения к различным моделям Perplexity Labs и получать ответы в виде асинхронного генератора. Модуль поддерживает различные модели, такие как `r1-1776`, `sonar-pro`, `sonar`, `sonar-reasoning`, `sonar-reasoning-pro`.
## Подробнее

Этот модуль предназначен для интеграции с Perplexity Labs и использования в асинхронных приложениях. Он предоставляет удобный способ для отправки запросов к API Perplexity Labs и обработки полученных ответов. Он использует `StreamSession` для установления соединения и обмена сообщениями через WebSocket.

## Классы

### `PerplexityLabs`

**Описание**: Класс `PerplexityLabs` является провайдером для асинхронной работы с API Perplexity Labs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL адрес `https://labs.perplexity.ai`.
- `working` (bool): Указывает, что провайдер работает.
- `default_model` (str): Модель по умолчанию (`r1-1776`).
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API Perplexity Labs.

## Функции

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
    Создает асинхронный генератор для взаимодействия с API Perplexity Labs.

    Args:
        model (str): Название модели, которую нужно использовать.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API Perplexity Labs.

    Raises:
        ResponseError: Если возникает ошибка при обработке ответа от API.
        RuntimeError: Если происходит неизвестная ошибка.

    Example:
        Пример вызова:
        ```python
        async for message in PerplexityLabs.create_async_generator(model="r1-1776", messages=[{"role": "user", "content": "Hello, world!"}]):
            print(message)
        ```
    """
```

**Назначение**: Создание асинхронного генератора для взаимодействия с API Perplexity Labs. Этот метод отвечает за установление соединения с сервером Perplexity Labs, отправку сообщений и получение ответов в асинхронном режиме.

**Параметры**:
- `cls`: Ссылка на класс `PerplexityLabs`.
- `model` (str): Название модели, которую нужно использовать.
- `messages (Messages)`: Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от API Perplexity Labs.

**Вызывает исключения**:
- `ResponseError`: Если возникает ошибка при обработке ответа от API.
- `RuntimeError`: Если происходит неизвестная ошибка.

**Как работает функция**:

1. **Формирование заголовков**:
   - Создаются заголовки `headers`, включающие `Origin` и `Referer` для имитации запроса с сайта Perplexity Labs.

2. **Установка соединения**:
   - Используется `StreamSession` для асинхронного установления соединения с API Perplexity Labs через `API_URL`.

3. **Получение SID (Session ID)**:
   - Выполняется GET-запрос к API для получения идентификатора сессии (`sid`).

4. **Авторизация**:
   - Отправляется POST-запрос с данными `post_data`, содержащими JWT для авторизации.

5. **Обновление соединения через WebSocket**:
   - Устанавливается WebSocket соединение с использованием полученного `sid`.

6. **Отправка данных**:
   - Формируется сообщение `message_data`, содержащее версию, источник, модель и сообщения для отправки.
   - Отправляется сообщение через WebSocket.

7. **Получение и обработка ответов**:
   - В цикле принимаются сообщения от WebSocket.
   - Обрабатываются различные типы сообщений:
     - `"2"`: Отправляется `"3"` в ответ.
     - Сообщения с данными: Извлекается и передается полезная нагрузка.

8. **Обработка завершения**:
   - Проверяется флаг `data["final"]` для определения окончания работы.
   - Извлекаются цитаты (`data["citations"]`) и причина завершения (`FinishReason`).

9. **Обработка ошибок**:
   - В случае ошибки при обработке сообщения вызывается исключение `ResponseError`.

**Внутренние функции**: Отсутствуют

**ASCII Flowchart**:

```
Начало
  ↓
Установка соединения (StreamSession)
  ↓
Получение SID (GET)
  ↓
Авторизация (POST)
  ↓
Установка WebSocket соединения
  ↓
Отправка данных (WebSocket)
  ↓
Получение сообщения (WebSocket)
  │
  ├── "2" ──→ Отправка "3" (WebSocket)
  │
  └── Данные ──→ Извлечение данных
       │
       ├── final=True ──→ Извлечение цитат и причины завершения → Завершение
       │
       └── final=False ──→ Выдача данных → Получение сообщения (WebSocket)
```

**Примеры**:

```python
# Пример 1: Простой запрос к модели r1-1776
messages = [{"role": "user", "content": "Hello, world!"}]
async for message in PerplexityLabs.create_async_generator(model="r1-1776", messages=messages):
    print(message)

# Пример 2: Использование прокси-сервера
messages = [{"role": "user", "content": "What is the capital of France?"}]
async for message in PerplexityLabs.create_async_generator(model="r1-1776", messages=messages, proxy="http://your_proxy:8080"):
    print(message)

# Пример 3: Отправка нескольких сообщений
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you."},
    {"role": "user", "content": "What is your name?"}
]
async for message in PerplexityLabs.create_async_generator(model="r1-1776", messages=messages):
    print(message)