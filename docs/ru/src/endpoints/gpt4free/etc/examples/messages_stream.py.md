# Модуль для демонстрации асинхронного стриминга ответов от gpt4free

## Обзор

Этот модуль демонстрирует, как использовать асинхронный клиент `gpt4free` для получения потоковых ответов от модели `gpt-4`. Он показывает, как накапливать и выводить текст по мере его поступления, а также обрабатывать возможные ошибки.

## Подробней

Модуль использует `AsyncClient` из библиотеки `g4f` для взаимодействия с моделью `gpt-4`. Он отправляет запрос с сообщением "Say hello there!" и получает ответ в виде потока чанков. Каждый чанк содержит часть текста ответа, который накапливается и выводится в консоль. В случае возникновения ошибки, она логируется, и выводится сообщение об ошибке. В конце выводится весь накопленный текст.

## Функции

### `main`

```python
async def main():
    """ Асинхронная функция для демонстрации стриминга ответов от gpt4free.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при получении или обработке ответа от gpt4free.
    
    Example:
        >>> asyncio.run(main())
        Hello there!

        Final accumulated text: Hello there!
    """
```

**Как работает функция**:

1. **Создание асинхронного клиента**: Создается экземпляр `AsyncClient` для взаимодействия с gpt4free.
2. **Отправка запроса на получение потокового ответа**: Используется метод `client.chat.completions.create` для отправки запроса к модели `gpt-4` с сообщением "Say hello there!". Указание `stream=True` включает режим потоковой передачи.
3. **Обработка потока чанков**: Асинхронно перебираются чанки, поступающие из потока.
   - Если чанк содержит текст ответа (`chunk.choices[0].delta.content`), этот текст добавляется к накопительной строке `accumulated_text` и выводится в консоль.
4. **Обработка ошибок**: Если в процессе получения или обработки ответа возникает исключение, оно перехватывается, и выводится сообщение об ошибке.
5. **Вывод накопленного текста**: После завершения потока (или в случае возникновения ошибки) выводится весь накопленный текст из `accumulated_text`.

```ascii
Создание асинхронного клиента    
│
│
Отправка запроса на стриминг ответа
│
│
Начало асинхронного цикла по чанкам
│
│
Обработка чанка ->  Извлечение контента чанка
│
│
Добавление контента к accumulated_text и вывод в консоль
│
│
Завершение цикла или обработка исключения
│
│
Вывод accumulated_text
```

**Примеры**:

```python
import asyncio
from g4f.client import AsyncClient

async def main():
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
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())