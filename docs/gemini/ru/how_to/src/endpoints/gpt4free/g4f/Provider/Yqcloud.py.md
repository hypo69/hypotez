### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код определяет класс `Yqcloud`, который является асинхронным провайдером для работы с языковой моделью, размещенной на `chat9.yqcloud.top`. Он позволяет отправлять запросы к API `api.binjie.fun` для генерации текста в потоковом режиме. Класс поддерживает системные сообщения и историю сообщений, что позволяет вести контекстные диалоги.

Шаги выполнения
-------------------------
1. **Определение класса `Conversation`**:
   - Создается класс `Conversation` для хранения истории сообщений и идентификатора пользователя.
   - При инициализации класса устанавливается модель и генерируется уникальный `userId` на основе текущего времени.

2. **Определение класса `Yqcloud`**:
   - Класс `Yqcloud` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Устанавливаются базовые атрибуты, такие как `url`, `api_endpoint`, `working`, `supports_stream`, `supports_system_message`, `supports_message_history`, `default_model` и `models`.

3. **Метод `create_async_generator`**:
   - Принимает параметры: `model` (языковая модель), `messages` (список сообщений), `stream` (флаг потоковой передачи), `proxy` (прокси-сервер), `conversation` (объект `Conversation`) и `return_conversation` (флаг возврата объекта `Conversation`).
   - Извлекает модель с помощью `cls.get_model(model)`.
   - Формирует заголовки запроса (`headers`), включая `origin` и `referer` на основе `cls.url`.
   - Если объект `conversation` не передан, создает новый объект `Conversation` и инициализирует его историю сообщений. В противном случае добавляет последнее сообщение в историю.

4. **Обработка системного сообщения**:
   - Извлекает системное сообщение из истории сообщений, если оно присутствует.
   - Если первое сообщение имеет роль "system", то его содержимое сохраняется в `system_message`, и это сообщение удаляется из текущего списка сообщений.

5. **Формирование запроса и отправка данных**:
   - Использует `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.
   - Форматирует запрос с помощью `format_prompt(current_messages)`.
   - Формирует данные запроса (`data`), включая `prompt`, `userId`, `network`, `system`, `withoutContext` и `stream`.
   - Отправляет POST-запрос к `cls.api_endpoint` с использованием `session.post`.

6. **Обработка потокового ответа**:
   - Обрабатывает ответ от API в потоковом режиме.
   - Для каждого чанка данных декодирует его и передает через `yield message`.
   - Собирает все чанки в `full_message`.

7. **Возврат объекта `Conversation` и сигнала остановки**:
   - Если `return_conversation` установлен в `True`, добавляет сообщение от ассистента в историю сообщений и возвращает объект `conversation`.
   - В конце возвращает `FinishReason("stop")`, чтобы указать на завершение генерации.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.Yqcloud import Yqcloud, Conversation
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    model = "gpt-4"
    messages: Messages = [
        {"role": "user", "content": "Привет, как дела?"}
    ]
    
    async for message in Yqcloud.create_async_generator(model=model, messages=messages, stream=True, return_conversation=True):
        if isinstance(message, Conversation):
            print(f"Conversation: {message.message_history}")
        else:
            print(f"Message: {message}")

if __name__ == "__main__":
    asyncio.run(main())