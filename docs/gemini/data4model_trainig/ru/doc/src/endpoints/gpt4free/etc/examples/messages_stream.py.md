# Модуль для демонстрации стриминга сообщений от GPT-4 через g4f.client

## Обзор

Этот модуль демонстрирует, как использовать асинхронный клиент `AsyncClient` из библиотеки `g4f` для получения потоковых ответов от модели GPT-4. Он показывает, как создать запрос к модели, обрабатывать входящие чанки данных и собирать их в единый текст.

## Подробней

Модуль предназначен для демонстрации асинхронного взаимодействия с GPT-4 API через библиотеку `g4f`. Он создает асинхронный клиент, отправляет запрос на генерацию текста и обрабатывает поток данных, выводя каждый чанк в консоль и собирая их в итоговый текст.  Этот код полезен для понимания того, как работают стриминговые API и как можно обрабатывать большие объемы данных, получаемые по частям.

## Функции

### `main`

```python
async def main():
    """
    Асинхронная функция, демонстрирующая потоковое получение ответа от GPT-4.

    Функция создает асинхронный клиент, отправляет запрос к GPT-4 и обрабатывает
    поток чанков данных, выводя их в консоль и собирая в итоговый текст.

    Raises:
        Exception: Если во время обработки потока возникает ошибка.

    Пример:
        >>> asyncio.run(main())
        Hello there!
        
        Final accumulated text: Hello there!
    """
    client = AsyncClient()

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say hello there!"}],
        stream=True,
    )

    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as ex:
        print(f"\nError occurred: {ex}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

## Внутренние функции

В данной функции нет внутренних функций

## Параметры
- `client` (`AsyncClient`): Асинхронный клиент для взаимодействия с API.
- `stream` (AsyncGenerator): Асинхронный генератор, предоставляющий чанки данных от API.
- `chunk` (Any): Отдельный чанк данных, полученный из потока.
 - `content` (str): Содержимое текущего чанка.
- `accumulated_text` (str): Строка, накапливающая все полученные чанки текста.

### Как работает функция `main`

1. **Создание асинхронного клиента**:
   - Создается экземпляр класса `AsyncClient`, который используется для взаимодействия с API.
2. **Создание запроса к GPT-4**:
   - Вызывается метод `client.chat.completions.create` для создания запроса к модели GPT-4.
   - В запросе указывается модель (`gpt-4`), сообщение (`{"role": "user", "content": "Say hello there!"}`) и режим стриминга (`stream=True`).
3. **Обработка потока данных**:
   - Организуется асинхронный цикл `async for chunk in stream` для обработки каждого чанка данных, поступающего из API.
   - Внутри цикла проверяется наличие данных в чанке (`chunk.choices and chunk.choices[0].delta.content`).
   - Если данные присутствуют, они извлекаются (`content = chunk.choices[0].delta.content`), добавляются к переменной `accumulated_text` и выводятся в консоль (`print(content, end="", flush=True)`).
4. **Обработка ошибок**:
   - Блок `try...except` используется для перехвата возможных исключений, возникающих во время обработки потока данных.
   - В случае возникновения ошибки, информация об ошибке выводится в консоль (`print(f"\nError occurred: {ex}")`).
5. **Завершение и вывод итогового текста**:
   - Блок `finally` выполняется после завершения цикла обработки данных, независимо от того, произошла ошибка или нет.
   - В блоке `finally` выводится итоговый накопленный текст (`print("\n\nFinal accumulated text:", accumulated_text)`).

## Примеры
```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Как дела?"}],
        stream=True,
    )
    
    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())
```

```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Напиши небольшой стих про осень"}],
        stream=True,
    )
    
    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())
```
```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Кто ты?"}],
        stream=True,
    )
    
    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())
```

```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Что такое машинное обучение?"}],
        stream=True,
    )
    
    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())
```
```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Переведи на английский: Привет мир!"}],
        stream=True,
    )
    
    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())
```
```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Напиши код на Python, который выводит 'Hello, world!'"}],
        stream=True,
    )
    
    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())
```

## Дополнительная информация

Этот модуль демонстрирует базовый пример использования асинхронного клиента `g4f` для потоковой передачи данных от GPT-4. Он может быть расширен для обработки более сложных запросов и интеграции с другими частями проекта.