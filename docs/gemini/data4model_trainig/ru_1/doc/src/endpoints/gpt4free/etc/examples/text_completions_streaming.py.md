# Модуль для демонстрации потоковой передачи текста с использованием g4f

## Обзор

Этот модуль демонстрирует, как использовать библиотеки `g4f` для создания потоковых текстовых завершений как в синхронном, так и в асинхронном режимах. Он включает в себя примеры использования `Client` и `AsyncClient` для взаимодействия с моделью `gpt-4` и вывода результатов в режиме реального времени.

## Подробнее

Этот код демонстрирует, как использовать библиотеку `g4f` для создания потоковых текстовых завершений. Он включает в себя примеры использования `Client` и `AsyncClient` для взаимодействия с моделью `gpt-4` и вывода результатов в режиме реального времени. Код содержит две основные функции: `sync_stream` и `async_stream`, которые демонстрируют синхронную и асинхронную потоковую передачу соответственно. Функция `main` запускает обе функции и обрабатывает любые возникающие исключения.

## Функции

### `sync_stream`

```python
def sync_stream():
    """
    Выполняет синхронную потоковую передачу текста с использованием g4f.

    Функция создает экземпляр `Client`, отправляет запрос на завершение чата к модели "gpt-4" и выводит
    полученные фрагменты текста в режиме реального времени.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Пример:
        >>> sync_stream()
        Привет! Вот как можно рекурсивно перечислить все файлы в каталоге в Python:
        ...
    """
    client = Client()
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": question}
        ],
        stream=True,
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content or "", end="")

### `async_stream`

```python
async def async_stream():
    """
    Выполняет асинхронную потоковую передачу текста с использованием g4f.

    Функция создает экземпляр `AsyncClient`, отправляет асинхронный запрос на завершение чата к модели "gpt-4" и
    выводит полученные фрагменты текста в режиме реального времени.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Пример:
        >>> asyncio.run(async_stream())
        Привет! Вот как можно рекурсивно перечислить все файлы в каталоге в Python:
        ...
    """
    client = AsyncClient()
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": question}
        ],
        stream=True,
    )
    
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")

### `main`

```python
def main():
    """
    Запускает синхронную и асинхронную потоковую передачу и обрабатывает исключения.

    Функция выводит заголовки для каждого потока, запускает функции `sync_stream` и `async_stream`
    и обрабатывает любые исключения, которые могут возникнуть в процессе.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: Если в процессе выполнения возникает необработанное исключение.

    Пример:
        >>> main()
        Synchronous Stream:
        Привет! Вот как можно рекурсивно перечислить все файлы в каталоге в Python:
        ...

        Asynchronous Stream:
        Привет! Вот как можно рекурсивно перечислить все файлы в каталоге в Python:
        ...
    """
    print("Synchronous Stream:")
    sync_stream()
    print("\n\nAsynchronous Stream:")
    asyncio.run(async_stream())
```

### Внутренние функции

Внутри функций `sync_stream` и `async_stream` нет внутренних функций.

## Переменные

- `question` (str): Вопрос, используемый для запроса к модели.
- `client` (Client | AsyncClient): Клиент для взаимодействия с API g4f.
- `stream` (Generator): Генератор, возвращающий фрагменты ответа модели.
- `chunk` (object): Фрагмент ответа, полученный от модели.

## Примеры

```python
import asyncio
from g4f.client import Client, AsyncClient

question = """
Hey! How can I recursively list all files in a directory in Python?
"""

# Пример использования sync_stream
client = Client()
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": question}
    ],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content or "", end="")

# Пример использования async_stream
async def main():
    client = AsyncClient()
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": question}
        ],
        stream=True,
    )
    
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")

asyncio.run(main())