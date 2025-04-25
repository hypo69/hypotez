#  Асинхронная демонстрация текстовых завершений с помощью GPT-4

## Обзор

Этот файл демонстрирует асинхронное использование модели GPT-4 для получения текстовых завершений с помощью библиотеки `g4f`. 

## Подробней

В этом файле мы создаем объект `AsyncClient` и используем его для отправки запроса на завершение текста в модель `gpt-4o`. 

## Классы

### `AsyncClient`

**Описание**: Класс для работы с API GPT-4 в асинхронном режиме.

**Наследует**: 
    - `g4f.client.AsyncClient`: Класс для работы с GPT-4 API.

**Атрибуты**: 
    - `chat`:  Свойство, предоставляющее доступ к методам для работы с API GPT-4, например, для  `completions`.

**Методы**:
    - `chat.completions.create()`: Метод для отправки запроса на завершение текста в модель GPT-4.

## Функции

### `main()`

**Назначение**: Асинхронная функция, которая  инициализирует `AsyncClient`,  отправляет запрос на завершение текста в модель `gpt-4o` и выводит результат.

**Параметры**:
    -  Нет

**Возвращает**: 
    -  `None`

**Вызывает исключения**:
    -  `Exception`: В случае возникновения ошибки при работе с API.

**Как работает функция**:

1. Создает объект `AsyncClient`  для работы с GPT-4 API.
2. Использует метод `chat.completions.create()` для отправки запроса на завершение текста,  устанавливая  `model="gpt-4o"` и передавая список сообщений (`messages`) для контекста.
3. Выводит в консоль ответ модели (`response.choices[0].message.content`).

**Примеры**:
```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "how does a court case get to the Supreme Court?"}
        ]
    )
    
    print(response.choices[0].message.content)

asyncio.run(main())
```

## Внутренние функции

### `chat.completions.create()`

**Назначение**: Функция  отправляет запрос на завершение текста в модель GPT-4.

**Параметры**: 

    - `model` (str): Имя модели, например, `gpt-4o`.
    - `messages` (list): Список сообщений для контекста модели.

**Возвращает**:
    -  `Response`: Объект ответа,  содержащий  результат завершения текста.

**Вызывает исключения**:
    -  `Exception`: В случае возникновения ошибки при работе с API.

**Как работает функция**: 
    - Функция `chat.completions.create()` отправляет запрос к API GPT-4 с помощью метода `request`.
    - Ответ API обрабатывается и возвращается как объект `Response`.

**Примеры**:
```python
response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "how does a court case get to the Supreme Court?"}
    ]
)
```

## Параметры

### `messages`

**Описание**:  Список сообщений (`list`) для контекста модели GPT-4.  Сообщения передаются в формате JSON.

**Пример**: 
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "how does a court case get to the Supreme Court?"}
]
```

## Примеры

**Пример 1**: Отправка запроса на завершение текста в модель `gpt-4o` с использованием базового контекста:
```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "how does a court case get to the Supreme Court?"}
        ]
    )
    
    print(response.choices[0].message.content)

asyncio.run(main())
```

**Пример 2**: Отправка запроса с более подробным контекстом:
```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a legal expert."},
            {"role": "user", "content": "Explain the process of a case reaching the Supreme Court."},
            {"role": "user", "content": "What are the requirements for a case to be heard by the Supreme Court?"}
        ]
    )
    
    print(response.choices[0].message.content)

asyncio.run(main())
```