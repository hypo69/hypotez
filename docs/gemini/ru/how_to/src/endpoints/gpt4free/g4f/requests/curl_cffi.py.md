### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код предоставляет инструменты для работы с асинхронными HTTP-запросами и WebSocket-соединениями, используя библиотеку `curl_cffi`. Он включает классы для управления потоковыми ответами (`StreamResponse`), асинхронными сессиями (`StreamSession`), формирования данных для отправки (`FormData`) и работы с WebSocket (`WebSocket`).

Шаги выполнения
-------------------------
1. **Инициализация `StreamResponse`**:
   - Класс `StreamResponse` оборачивает объект `Response` из `curl_cffi` и предоставляет методы для асинхронного получения текста, JSON-данных, итерации по строкам и содержимому ответа.
   - Для создания экземпляра `StreamResponse` необходимо передать объект `Response` в конструктор.

2. **Использование `StreamSession`**:
   - Класс `StreamSession` наследуется от `AsyncSession` и предоставляет методы для выполнения HTTP-запросов с потоковой передачей данных.
   - Для выполнения запроса необходимо вызвать один из методов HTTP (например, `get`, `post`, `put`, `delete`) с указанием URL и параметров запроса.
   - Метод `request` возвращает объект `StreamResponse`, который можно использовать для получения данных из ответа.

3. **Формирование данных с использованием `FormData`**:
   - Класс `FormData` используется для создания данных в формате multipart/form-data.
   - Для добавления полей в форму необходимо использовать метод `add_field`, указывая имя поля, данные и тип содержимого.

4. **Работа с WebSocket через класс `WebSocket`**:
   - Класс `WebSocket` предназначен для установления и управления WebSocket-соединениями.
   - Для подключения к WebSocket необходимо создать экземпляр класса `WebSocket`, указав URL и параметры подключения.
   - Методы `receive_str` и `send_str` используются для получения и отправки текстовых сообщений через WebSocket.

Пример использования
-------------------------

```python
from curl_cffi.requests import AsyncSession
from g4f.requests import StreamSession

async def main():
    # Использование StreamSession для выполнения GET-запроса
    async with StreamSession() as session:
        response = await session.get("https://example.com")
        print(f"Status code: {response.status}")
        content = await response.text()
        print(f"Content: {content[:100]}...")

    # Использование StreamSession для выполнения POST-запроса с данными
    async with StreamSession() as session:
        data = {"key": "value"}
        response = await session.post("https://example.com/post", json=data)
        print(f"Status code: {response.status}")
        content = await response.json()
        print(f"Content: {content}")
        
    # Использование StreamSession для работы с FormData
    async with StreamSession() as session:
        form_data = FormData()
        form_data.add_field("field1", "value1")
        form_data.add_field("file1", data=b"file content", filename="test.txt", content_type="text/plain")
        response = await session.post("https://example.com/upload", data=form_data)
        print(f"Status code: {response.status}")
        print(await response.text())

    # Использование StreamSession для подключения к WebSocket
    async with StreamSession() as session:
        async with session.ws_connect("wss://example.com/ws", autoping=False) as ws:
            await ws.send_str("Hello, WebSocket!")
            message = await ws.receive_str()
            print(f"Received message: {message}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())