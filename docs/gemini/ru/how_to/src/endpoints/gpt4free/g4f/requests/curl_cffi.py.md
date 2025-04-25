## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода реализует асинхронную сессию для HTTP-запросов с поддержкой потоковой передачи данных (streaming). Он обеспечивает:

- **Асинхронное выполнение**:  Позволяет  отправлять и получать данные HTTP-запросов без блокировки  основного потока.
- **Потоковая обработка данных**:  Предоставляет возможность получать данные частями, не загружая весь  отклик целиком в память.
- **Поддержка  JSON, Server-Sent Events (SSE):**  Включает в себя методы для работы с JSON-ответами и событиями SSE.
- **WebSocket**:  Поддерживает подключение к WebSocket-серверам для двусторонней связи.
- **Удобный интерфейс**:  Предоставляет методы для выполнения различных HTTP-запросов (GET, POST, PUT, DELETE и т.д.),  а также  методы  для  работы с данными  SSE и WebSocket.

Шаги выполнения
-------------------------
1. **Импорт модулей**:  Импортируются необходимые модули для работы с HTTP-запросами, потоковой передачей данных и  WebSocket.
2. **Определение класса StreamResponse**:  Этот класс обертывает объект `Response`  и предоставляет дополнительные  методы  для  работы  с  асинхронной  потоковой  передачей  данных.
    -  `text()`:  Возвращает  текст  ответа.
    -  `raise_for_status()`:  Поднимает  исключение  `HTTPError`,  если  возникла  ошибка.
    -  `json()`:  Парсит  JSON-отклик.
    -  `iter_lines()`:  Итерирует  строки  ответа.
    -  `iter_content()`:  Итерирует  содержимое  ответа.
    -  `sse()`:  Итерирует  события  SSE  в  ответе.
3. **Определение класса StreamSession**:  Этот класс  представляет  собой  асинхронную  сессию  для  HTTP-запросов.
    -  `request()`:  Создает  и  возвращает  объект  `StreamResponse`  для  заданного  HTTP-запроса.
    -  `ws_connect()`:  Создает  соединение  с  WebSocket-сервером.
    -  `_ws_connect()`:  Приватный  метод  для  установления  соединения  с  WebSocket.
    -  `head`, `get`, `post`, `put`, `patch`, `delete`, `options`:  Partial  методы  для  выполнения  различных  HTTP-запросов.
4. **Определение класса FormData**:  Этот класс  предоставляет  возможность  создать  multipart/form-data  запрос.
5. **Определение класса WebSocket**:  Этот класс  представляет  собой  WebSocket-соединение.
    -  `__aenter__`:  Входит  в  контекст  соединения.
    -  `__aexit__`:  Выходит  из  контекста  соединения.
    -  `receive_str()`:  Получает  строку  данных  с  WebSocket-сервера.
    -  `send_str()`:  Отправляет  строку  данных  на  WebSocket-сервер.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.requests.curl_cffi import StreamSession, FormData

async def main():
    async with StreamSession() as session:
        # Отправляем POST-запрос с multipart/form-data
        form_data = FormData()
        form_data.add_field("file", open("file.txt", "rb"), content_type="text/plain", filename="file.txt")
        response = await session.post("https://example.com/upload", data=form_data)

        # Проверяем статус ответа
        response.raise_for_status()

        # Получаем текст ответа
        text = await response.text()
        print(text)

        # Итерируем строчки ответа
        async for line in response.iter_lines():
            print(line.decode())

        # Итерируем содержимое ответа
        async for chunk in response.iter_content():
            print(chunk.decode())

        # Итерируем события SSE
        async for event in response.sse():
            print(event)

        # Создаем WebSocket-соединение
        async with session.ws_connect("wss://example.com/ws") as ws:
            # Отправляем сообщение на WebSocket
            await ws.send_str("Hello, world!")

            # Получаем сообщение с WebSocket
            message = await ws.receive_str()
            print(message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```