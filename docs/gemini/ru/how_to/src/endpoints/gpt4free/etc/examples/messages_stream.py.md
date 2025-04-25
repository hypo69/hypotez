## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код демонстрирует пример асинхронного взаимодействия с моделью GPT-4 через библиотеку g4f. Он показывает, как получить текстовый ответ от модели по частям (streaming) и собрать его в единый текст.

Шаги выполнения
-------------------------
1. **Импортирование необходимых модулей:**
   - Импортируется модуль `asyncio` для асинхронного программирования.
   - Импортируется класс `AsyncClient` из библиотеки `g4f.client` для создания асинхронного клиента.

2. **Создание асинхронной функции `main()`:**
   - Функция `main()` является асинхронной, что позволяет ей работать с `asyncio`.
   - Внутри функции создается объект `client` класса `AsyncClient` для взаимодействия с API.

3. **Вызов метода `chat.completions.create()` для отправки запроса:**
   - Метод `chat.completions.create()` используется для отправки запроса к модели GPT-4.
   - Параметры запроса:
     - `model="gpt-4"` - указывает на использование модели GPT-4.
     - `messages=[{"role": "user", "content": "Say hello there!"}]` - задает сообщение для модели.
     - `stream=True` - включает потоковый режим, то есть ответ будет возвращаться по частям.

4. **Обработка ответа от модели по частям:**
   - Используется цикл `async for chunk in stream:` для перебора частей ответа.
   - Проверяется, доступна ли часть текста в `chunk.choices[0].delta.content`.
   - Если часть текста доступна, она добавляется к переменной `accumulated_text` и выводится на экран.

5. **Обработка ошибок:**
   - Блок `try...except` позволяет перехватить ошибки, которые могут возникнуть при работе с API.
   - В случае ошибки выводится сообщение об ошибке.

6. **Вывод финального текста:**
   - Блок `finally` гарантирует выполнение кода независимо от того, произошла ли ошибка или нет.
   - В блоке `finally` выводится накопленный текст `accumulated_text`.

7. **Запуск асинхронной функции:**
   - Используется функция `asyncio.run(main())` для запуска асинхронной функции `main()`.

Пример использования
-------------------------

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
```