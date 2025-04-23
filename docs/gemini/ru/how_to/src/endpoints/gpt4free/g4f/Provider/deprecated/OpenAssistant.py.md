### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код реализует асинхронный генератор для взаимодействия с Open Assistant API. Он отправляет запросы для создания чата, отправки сообщений пользователя и получения ответов от ассистента в режиме реального времени. Код также обрабатывает ошибки и удаляет чат после завершения.

Шаги выполнения
-------------------------
1. **Получение cookies (если необходимо)**:
   - Если `cookies` не переданы, функция `get_cookies("open-assistant.io")` извлекает их.

2. **Инициализация сессии aiohttp**:
   - Создается `ClientSession` с использованием переданных `cookies` и заголовка `User-Agent`.
   - Заголовки имитируют запрос от браузера Chrome.

3. **Создание чата**:
   - Отправляется POST-запрос на `https://open-assistant.io/api/chat` для создания нового чата.
   - `chat_id` извлекается из JSON-ответа.

4. **Отправка сообщения пользователя**:
   - Форматируется сообщение пользователя с использованием `format_prompt(messages)`.
   - Отправляется POST-запрос на `https://open-assistant.io/api/chat/prompter_message` с `chat_id` и форматированным сообщением.
   - `parent_id` извлекается из JSON-ответа.

5. **Получение ответа от ассистента**:
   - Отправляется POST-запрос на `https://open-assistant.io/api/chat/assistant_message` с `chat_id`, `parent_id` и параметрами модели.
   - В случае успеха из JSON-ответа извлекается `message_id`. Если в ответе есть поле `message`, выбрасывается исключение `RuntimeError`.

6. **Получение событий чата**:
   - Отправляется POST-запрос на `https://open-assistant.io/api/chat/events` с `chat_id` и `message_id` в параметрах запроса.
   - Асинхронно читаются строки из ответа. Если строка начинается с `data: `, она декодируется из JSON.
   - Если `event_type` равен `token`, извлекается текст и передается через `yield`.

7. **Удаление чата**:
   - Отправляется DELETE-запрос на `https://open-assistant.io/api/chat` с `chat_id` в параметрах запроса.
   - Вызывается `response.raise_for_status()` для проверки успешности запроса.

Пример использования
-------------------------

```python
import asyncio

from src.endpoints.gpt4free.g4f.Provider.deprecated import OpenAssistant
from src.endpoints.gpt4free.g4f.typing import Messages


async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    
    async for response in OpenAssistant.create_async_generator(
        model="OA_SFT_Llama_30B_6",
        messages=messages,
        proxy=None,
        cookies={}
    ):
        print(response, end="")

if __name__ == "__main__":
    asyncio.run(main())