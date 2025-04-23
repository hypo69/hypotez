# Модуль `PerplexityLabs`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с Perplexity Labs API. Он позволяет генерировать текст на основе предоставленных сообщений, используя различные модели, предоставляемые Perplexity Labs. Модуль поддерживает стриминг ответов и обработку источников цитирования.

## Подробнее

Модуль `PerplexityLabs` предназначен для работы с API Perplexity Labs, который предоставляет доступ к различным моделям генерации текста. Он использует вебсокеты для стриминга ответов в асинхронном режиме.

## Классы

### `PerplexityLabs`

**Описание**: Класс, предоставляющий асинхронный интерфейс для взаимодействия с Perplexity Labs API.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `url` (str): URL для Perplexity Labs.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`"r1-1776"`).
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от Perplexity Labs API.

## Методы класса

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
    """Создает асинхронный генератор для получения ответов от Perplexity Labs API.

    Args:
        cls (PerplexityLabs): Класс PerplexityLabs.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        ResponseError: Если возникает ошибка при обработке сообщения.
        RuntimeError: Если возникает неизвестная ошибка.

    Как работает функция:
    - Функция устанавливает соединение с сервером Perplexity Labs через WebSocket.
    - Происходит процесс инициализации соединения, включающий обмен данными через HTTP и WebSocket.
    - Подготавливаются данные сообщения, включая версию, источник, модель и список сообщений.
    - Функция отправляет данные сообщения на сервер Perplexity Labs через WebSocket.
    - В цикле ожидает входящие сообщения от сервера.
    - Обрабатывает каждое сообщение, извлекая и передавая содержимое ответа.
    - Если получен финальный ответ, извлекает цитаты и завершает генерацию.
    - В случае ошибок в процессе обработки сообщений, выбрасывает исключение ResponseError.

    Внутренние функции:
        Отсутствуют

    Примеры:
        # Пример вызова функции
        model = "r1-1776"
        messages = [{"role": "user", "content": "Hello, Perplexity Labs!"}]
        proxy = "http://your_proxy:8080"
        generator = PerplexityLabs.create_async_generator(model, messages, proxy=proxy)
        async for message in generator:
            print(message)
    """
```

## Параметры класса

- `url` (str): URL для Perplexity Labs.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`"r1-1776"`).
- `models` (List[str]): Список поддерживаемых моделей.

## Примеры

Пример использования класса `PerplexityLabs`:

```python
# Пример использования create_async_generator
model = "r1-1776"
messages = [{"role": "user", "content": "Hello, Perplexity Labs!"}]
proxy = "http://your_proxy:8080"

async def main():
    generator = await PerplexityLabs.create_async_generator(model, messages, proxy=proxy)
    async for message in generator:
        print(message)

# Запуск асинхронной функции
import asyncio
asyncio.run(main())