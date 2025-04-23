Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `AllenAI`, который является асинхронным генератором для взаимодействия с API Ai2 Playground. Он использует multipart/form-data для отправки запросов и асинхронно обрабатывает ответы, предоставляя сгенерированный контент частями. Класс поддерживает управление историей разговоров и передачу параметров, таких как температура и top_p.

Шаги выполнения
-------------------------
1. **Инициализация разговора**: Если `conversation` не предоставлен, создается новый объект `Conversation` с указанной моделью. Если `conversation` предоставлен, используется его `x_anonymous_user_id`.
2. **Формирование данных запроса**:
   - Формируется `prompt` либо из всех сообщений (`format_prompt`), либо из последнего сообщения пользователя (`get_last_user_message`), если `conversation` уже существует.
   - Генерируется случайный `boundary` для разделения частей в multipart/form-data.
   - Создаются заголовки (`headers`) для HTTP-запроса, включая `content-type` с новым `boundary` и `x-anonymous-user-id`.
   - Формируется тело запроса (`form_data`) как список строк, представляющих различные части формы (модель, хост, контент, флаг приватности). Добавляются параметры `temperature` и `top_p`, если они указаны.
   - Тело запроса объединяется в одну строку и кодируется в байты.
3. **Отправка запроса и обработка ответа**:
   - Открывается асинхронная сессия `ClientSession` с заданными заголовками.
   - Отправляется POST-запрос на `cls.api_endpoint` с использованием `session.post()`, передавая закодированные данные и прокси, если он указан.
   - Вызывается `raise_for_status(response)` для проверки статуса ответа.
   - Асинхронно читаются чанки из ответа (`response.content`).
   - Каждый чанк декодируется и разделяется на строки. Пустые строки отбрасываются.
   - Каждая строка пытается быть распарсена как JSON.
   - Если строка успешно распарсена как JSON и является словарем:
     - Если в данных есть поле `children`, ищется первый ребенок с `role` равным "assistant", и его `id` сохраняется как `current_parent`.
     - Если в данных есть поле `message` и непустое поле `content`, содержимое (`content`) возвращается как часть генератора.
     - Если в данных есть поле `final` или `finish_reason` равно "stop":
       - Если `current_parent` существует, он устанавливается как `conversation.parent`.
       - В историю разговора (`conversation.messages`) добавляются сообщения пользователя и ассистента.
       - Если `return_conversation` равно `True`, возвращается объект `conversation`.
       - Возвращается `FinishReason("stop")` для завершения генератора.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.AllenAI import AllenAI, Conversation
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    # Пример использования AllenAI для генерации ответа на сообщение
    messages: Messages = [{"role": "user", "content": "Translate to french: Hello, how are you?"}]
    model = "tulu3-405b"
    
    # Создаем объект Conversation для хранения истории разговора (опционально)
    conversation = Conversation(model)
    
    async for response in AllenAI.create_async_generator(
        model=model,
        messages=messages,
        conversation=conversation,  # Передаем объект Conversation
        return_conversation=True  # Возвращаем объект Conversation в конце
    ):
        if isinstance(response, str):
            print(f"Response chunk: {response}")
        elif isinstance(response, Conversation):
            print(f"Conversation history: {response.messages}")
        else:
            print(f"Finish reason: {response}")

if __name__ == "__main__":
    asyncio.run(main())