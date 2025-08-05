## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код демонстрирует два способа использования потоковой передачи ответов от модели GPT-4 через API `gpt4free`: синхронный и асинхронный. 

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек:**
   -  `asyncio` используется для асинхронного программирования.
   -  `g4f.client` предоставляет API-клиент для взаимодействия с `gpt4free`.
2. **Определение вопроса:**
   -  `question` содержит строку с текстом вопроса, который будет задан модели.
3. **Функция `sync_stream()`:**
   -  Создает экземпляр клиента `Client`.
   -  Использует метод `chat.completions.create` для отправки запроса с вопросом и включенной потоковой передачей (`stream=True`).
   -  Итерирует по частям ответа (`chunk`) из потока.
   -  Если в части ответа присутствует текст (`chunk.choices[0].delta.content`), выводит его на консоль.
4. **Функция `async_stream()`:**
   -  Создает экземпляр асинхронного клиента `AsyncClient`.
   -  Использует метод `chat.completions.create` для отправки запроса с вопросом и включенной потоковой передачей (`stream=True`).
   -  Итерирует асинхронно по частям ответа (`chunk`) из потока.
   -  Если в части ответа присутствует текст (`chunk.choices[0].delta.content`), выводит его на консоль.
5. **Функция `main()`:**
   -  Выводит заголовок для синхронного потока.
   -  Вызывает `sync_stream()` для демонстрации синхронной потоковой передачи.
   -  Выводит заголовок для асинхронного потока.
   -  Использует `asyncio.run(async_stream())` для запуска асинхронного потока.
6. **Блок `if __name__ == "__main__":`:**
   -  Вызывает функцию `main()`, чтобы запустить код.
   -  Обрабатывает исключения, возникающие во время выполнения.

Пример использования
-------------------------

```python
import asyncio
from g4f.client import Client, AsyncClient

question = """
Hey! How can I recursively list all files in a directory in Python?\n
"""

# Synchronous streaming function
def sync_stream():
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

# Asynchronous streaming function
async def async_stream():
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

# Main function to run both streams
def main():
    print("Synchronous Stream:")
    sync_stream()
    print("\n\nAsynchronous Stream:")
    asyncio.run(async_stream())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
```