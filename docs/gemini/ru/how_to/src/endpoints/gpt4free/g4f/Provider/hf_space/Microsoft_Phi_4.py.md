### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный код определяет класс `Microsoft_Phi_4`, который является асинхронным провайдером для взаимодействия с моделью Microsoft Phi-4 Multimodal через Hugging Face Spaces. Он поддерживает потоковую передачу данных, системные сообщения и историю сообщений. Код содержит методы для отправки запросов к API, загрузки медиафайлов и создания асинхронного генератора для получения ответов от модели.

Шаги выполнения
-------------------------
1. **Определение класса `Microsoft_Phi_4`**:
   - Класс наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Определяются атрибуты класса, такие как `label`, `space`, `url`, `api_url`, `referer`, `working`, `supports_stream`, `supports_system_message`, `supports_message_history`, `default_model`, `default_vision_model`, `model_aliases`, `vision_models` и `models`.

2. **Метод `run`**:
   - Функция выполняет HTTP-запросы к API в зависимости от переданного метода (`predict`, `post`, `get`).
   - Формирует заголовки запроса, включая `content-type`, `x-zerogpu-token`, `x-zerogpu-uuid` и `referer`.
   - Для метода `predict` отправляет POST-запрос с текстом и медиафайлами.
   - Для метода `post` отправляет POST-запрос с сообщениями пользователя и медиафайлами.
   - Для метода `get` отправляет GET-запрос для получения данных в формате `text/event-stream`.

3. **Метод `create_async_generator`**:
   - Функция создает асинхронный генератор для взаимодействия с моделью.
   - Форматирует промпт, используя `format_prompt` и `format_image_prompt`.
   - Создает или использует существующий `JsonConversation` для хранения состояния сессии.
   - Загружает медиафайлы на сервер, если они предоставлены.
   - Вызывает методы `run` для отправки запросов и получения ответов от модели.
   - Обрабатывает ответы в формате `text/event-stream`, извлекая данные JSON и возвращая их через генератор.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.Microsoft_Phi_4 import Microsoft_Phi_4
from src.endpoints.gpt4free.g4f.typing import Messages, MediaListType
from src.endpoints.gpt4free.g4f.providers.response import JsonConversation

async def main():
    model = "phi-4-multimodal"
    messages: Messages = [{"role": "user", "content": "Напиши стихотворение о весне."}]
    media: MediaListType = []
    prompt = None
    proxy = None
    cookies = None
    api_key = None
    zerogpu_uuid = "[object Object]"
    return_conversation = False
    conversation = JsonConversation(session_hash="test_session")

    async for response in Microsoft_Phi_4.create_async_generator(
        model=model,
        messages=messages,
        media=media,
        prompt=prompt,
        proxy=proxy,
        cookies=cookies,
        api_key=api_key,
        zerogpu_uuid=zerogpu_uuid,
        return_conversation=return_conversation,
        conversation=conversation
    ):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())