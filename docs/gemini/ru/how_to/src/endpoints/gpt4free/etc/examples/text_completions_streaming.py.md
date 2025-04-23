Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код демонстрирует, как использовать потоковую передачу данных (streaming) для получения ответов от модели GPT-4 как синхронно, так и асинхронно. Это особенно полезно для задач, требующих длительных ответов, так как позволяет получать и обрабатывать части ответа по мере их генерации, а не ждать завершения всего ответа.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `asyncio` для поддержки асинхронного выполнения.
   - Импортируются классы `Client` и `AsyncClient` из библиотеки `g4f.client` для создания клиентов для взаимодействия с моделью GPT-4.

2. **Определение вопроса**:
   - Определяется переменная `question`, содержащая текст вопроса, который будет отправлен модели GPT-4.

3. **Синхронная потоковая функция (`sync_stream`)**:
   - Создается экземпляр класса `Client`.
   - Вызывается метод `client.chat.completions.create` для отправки запроса к модели GPT-4.
     - `model="gpt-4"`: Указывается используемая модель.
     - `messages`: Список сообщений, содержащих вопрос пользователя.
     - `stream=True`: Включается режим потоковой передачи данных.
   - Итерируется по потоку `stream`, получая чанки (фрагменты) ответа.
   - Из каждого чанка извлекается содержимое (`chunk.choices[0].delta.content`) и выводится в консоль без символа новой строки (`end=""`), чтобы сформировать непрерывный ответ.

4. **Асинхронная потоковая функция (`async_stream`)**:
   - Создается экземпляр класса `AsyncClient`.
   - Вызывается метод `client.chat.completions.create` для отправки асинхронного запроса к модели GPT-4 (аналогично синхронному варианту).
   - Асинхронно итерируется по потоку `stream`, получая чанки ответа.
   - Из каждого чанка извлекается содержимое и выводится в консоль.

5. **Главная функция (`main`)**:
   - Выводит заголовок "Synchronous Stream:".
   - Вызывает функцию `sync_stream()` для запуска синхронного потока.
   - Выводит заголовок "Asynchronous Stream:".
   - Использует `asyncio.run(async_stream())` для запуска асинхронного потока.

6. **Запуск кода**:
   - Проверяется, является ли скрипт главным запускаемым файлом (`if __name__ == "__main__":`).
   - Вызывается функция `main()` для запуска основного процесса.
   - Обрабатывается возможное исключение, которое может возникнуть в процессе выполнения, и выводится сообщение об ошибке.

Пример использования
-------------------------

```python
import asyncio
from g4f.client import Client, AsyncClient

question = """
Hey! How can I recursively list all files in a directory in Python?
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