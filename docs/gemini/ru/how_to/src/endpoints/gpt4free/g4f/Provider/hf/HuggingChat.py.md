### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `HuggingChat`, который является асинхронным провайдером для взаимодействия с сервисом Hugging Face Chat. Он включает методы для аутентификации, создания бесед, отправки сообщений и обработки ответов, включая текст, изображения и результаты веб-поиска. Класс использует библиотеку `curl_cffi` для выполнения HTTP-запросов и поддерживает как текстовые, так и мультимодальные модели.

Шаги выполнения
-------------------------
1. **Инициализация класса `HuggingChat`**:
   - Определяются основные атрибуты класса, такие как домен, URL, флаги поддержки стриминга и необходимости аутентификации, а также модели по умолчанию и их псевдонимы.

2. **Аутентификация**:
   - Метод `on_auth_async` обрабатывает аутентификацию пользователя. Он проверяет наличие куки `hf-chat` и, если они есть, использует их для аутентификации. Если куки отсутствуют, запрашивается URL для логина и используются аргументы, полученные от `get_args_from_nodriver`, для завершения процесса аутентификации.

3. **Создание аутентифицированного запроса**:
   - Метод `create_authed` создает аутентифицированный запрос к Hugging Face Chat. Он принимает модель, сообщения, куки аутентификации, промпт и медиафайлы.
   - Проверяется наличие `curl_cffi`. Если библиотека отсутствует, вызывается исключение `MissingRequirementsError`.
   - Создается или используется существующая беседа (`conversation`). Если беседа новая, создается новый conversation ID и message ID.
   - Форматируется запрос с использованием `format_prompt` и `get_last_user_message`.

4. **Отправка запроса и обработка ответа**:
   - Запрос отправляется с использованием `curl_cffi.requests.Session`.
   - Ответ обрабатывается построчно. Каждая строка парсится как JSON.
   - В зависимости от типа сообщения (`stream`, `finalAnswer`, `file`, `webSearch`, `title`, `reasoning`) выполняются различные действия:
     - `stream`: извлекается и возвращается текст сообщения.
     - `finalAnswer`: завершается обработка.
     - `file`: извлекается URL изображения и возвращается `ImageResponse`.
     - `webSearch`: извлекаются источники веб-поиска и возвращаются `Sources`.
     - `title`: извлекается заголовок и возвращается `TitleGeneration`.
     - `reasoning`: извлекаются данные рассуждения и возвращаются `Reasoning`.

5. **Создание беседы**:
   - Метод `create_conversation` создает новую беседу, отправляя POST-запрос к API Hugging Face Chat. Он принимает сессию и модель в качестве аргументов и возвращает conversation ID.

6. **Получение message ID**:
   - Метод `fetch_message_id` извлекает message ID из данных ответа, полученных от API Hugging Face Chat. Он выполняет GET-запрос к API и парсит JSON-ответ для получения message ID.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf.HuggingChat import HuggingChat
from src.typing import Messages, Cookies
import asyncio

async def main():
    # Пример использования HuggingChat
    cookies: Cookies = {"hf-chat": "ваш_hf_chat_cookie"}  # Замените на ваш actual cookie
    messages: Messages = [{"role": "user", "content": "Hello, Hugging Face Chat!"}]

    # Аутентификация
    auth_result = HuggingChat.on_auth_async(cookies=cookies)
    
    # Создание аутентифицированного запроса
    async for result in auth_result:
        if result.cookies:
            response = HuggingChat.create_authed(
                model=HuggingChat.default_model,
                messages=messages,
                auth_result=result
            )

            # Обработка ответа
            async for item in response:
                print(item)

if __name__ == "__main__":
    asyncio.run(main())