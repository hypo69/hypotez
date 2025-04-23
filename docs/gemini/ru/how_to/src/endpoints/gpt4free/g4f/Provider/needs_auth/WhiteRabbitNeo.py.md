### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет асинхронный провайдер `WhiteRabbitNeo` для взаимодействия с API `www.whiterabbitneo.com`. Он предназначен для генерации ответов на основе предоставленных сообщений, используя асинхронные запросы. Класс `WhiteRabbitNeo` наследуется от `AsyncGeneratorProvider` и предоставляет метод `create_async_generator` для создания асинхронного генератора, который отправляет запросы к API и возвращает чанки данных.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `__future__`, `ClientSession`, `BaseConnector`, `AsyncResult`, `Messages`, `Cookies`, `raise_for_status`, `AsyncGeneratorProvider`, `get_cookies`, `get_connector`, `get_random_string`.
2. **Определение класса `WhiteRabbitNeo`**:
   - Определяется класс `WhiteRabbitNeo`, который наследуется от `AsyncGeneratorProvider`.
   - Устанавливаются атрибуты класса:
     - `url`: URL API (`https://www.whiterabbitneo.com`).
     - `working`: Флаг, указывающий, что провайдер работает (`True`).
     - `supports_message_history`: Флаг, указывающий, что провайдер поддерживает историю сообщений (`True`).
     - `needs_auth`: Флаг, указывающий, что провайдер требует аутентификацию (`True`).
3. **Определение метода `create_async_generator`**:
   - Определяется асинхронный метод `create_async_generator`, который принимает следующие аргументы:
     - `model` (str): Модель для генерации ответов.
     - `messages` (Messages): Список сообщений для отправки.
     - `cookies` (Cookies, optional): Куки для аутентификации. По умолчанию `None`.
     - `connector` (BaseConnector, optional): Коннектор для асинхронных запросов. По умолчанию `None`.
     - `proxy` (str, optional): Прокси-сервер для запросов. По умолчанию `None`.
     - `**kwargs`: Дополнительные аргументы.
4. **Получение или установка куки**:
   - Если `cookies` не предоставлены, они получаются с помощью `get_cookies("www.whiterabbitneo.com")`.
5. **Определение заголовков**:
   - Определяются заголовки для HTTP-запроса, включая `User-Agent`, `Accept`, `Accept-Language`, `Accept-Encoding`, `Referer`, `Content-Type`, `Origin`, `Connection`, `Sec-Fetch-Dest`, `Sec-Fetch-Mode`, `Sec-Fetch-Site`, `TE`.
6. **Создание асинхронной сессии**:
   - Создается асинхронная сессия `ClientSession` с использованием предоставленных заголовков, куки и коннектора.
7. **Формирование данных для отправки**:
   - Формируются данные для отправки в формате JSON, включая `messages`, `id` (случайная строка), `enhancePrompt` (False) и `useFunctions` (False).
8. **Отправка POST-запроса**:
   - Отправляется POST-запрос к API (`f"{cls.url}/api/chat"`) с использованием асинхронной сессии, JSON-данных и прокси.
9. **Обработка ответа**:
   - Проверяется статус ответа с помощью `raise_for_status(response)`.
   - Асинхронно итерируются чанки данных из ответа и декодируются, после чего возвращаются через `yield`.

Пример использования
-------------------------

```python
from aiohttp import ClientSession
from src.endpoints.gpt4free.g4f.Provider.needs_auth import WhiteRabbitNeo
from src.endpoints.gpt4free.g4f import Messages

async def main():
    model = "default"
    messages: Messages = [{"role": "user", "content": "Hello, World!"}]
    cookies = {"cookie_name": "cookie_value"}  # Замените на реальные куки

    async for chunk in WhiteRabbitNeo.create_async_generator(model=model, messages=messages, cookies=cookies):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())