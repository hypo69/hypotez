Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует асинхронный генератор для взаимодействия с моделью CohereForAI C4AI Command через API. Он поддерживает создание и ведение бесед, отправку сообщений и получение ответов в реальном времени.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Функция `create_async_generator` принимает параметры, такие как модель, сообщения, API-ключ, прокси и существующую беседу (если есть).
   - Извлекает модель с помощью `cls.get_model(model)`, чтобы убедиться, что используется правильный псевдоним модели.

2. **Подготовка заголовков**:
   - Создает заголовки HTTP-запроса, включая `Origin`, `User-Agent`, `Accept` и другие необходимые параметры.
   - Если предоставлен `api_key`, добавляет его в заголовок `Authorization`.

3. **Создание сессии**:
   - Использует `ClientSession` из библиотеки `aiohttp` для управления HTTP-соединением.
   - Если предоставлена существующая беседа (`conversation`), использует её cookies.

4. **Обработка сообщений**:
   - Разделяет сообщения на системные и пользовательские.
   - Форматирует входные данные (`inputs`) на основе того, является ли это началом новой беседы или продолжением существующей.

5. **Создание или обновление беседы**:
   - Если беседа не существует или модель/системный промпт отличаются от текущих, создает новую беседу, отправляя POST-запрос на `cls.conversation_url`.
   - Сохраняет полученные cookies и данные беседы в объекте `JsonConversation`.

6. **Получение ID сообщения**:
   - Отправляет GET-запрос для получения ID последнего сообщения в беседе.
   - Извлекает данные из JSON, полученного из ответа.

7. **Отправка данных**:
   - Создает объект `FormData` и добавляет входные данные, ID сообщения и другие параметры в формате JSON.
   - Отправляет POST-запрос с данными на URL беседы.

8. **Получение и обработка ответов**:
   - Получает ответы от сервера в виде чанков.
   - Преобразует каждый чанк в JSON и обрабатывает его в зависимости от типа (`stream`, `title`, `finalAnswer`).
   - Для типа `stream` возвращает текст токена, заменяя `\u0000` на пустую строку.
   - Для типа `title` возвращает заголовок.
   - Завершает обработку при получении типа `finalAnswer`.

9. **Обработка ошибок**:
   - Проверяет наличие ошибок в ответе и вызывает исключение `RuntimeError` в случае их обнаружения.
   - Обрабатывает ошибки JSON при декодировании чанков ответа и вызывает исключение `RuntimeError`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.CohereForAI_C4AI_Command import CohereForAI_C4AI_Command
from src.endpoints.gpt4free.g4f.providers.response import JsonConversation

async def main():
    model = "command-r-plus"
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Как дела?"}
    ]
    api_key = "YOUR_API_KEY"
    proxy = None
    conversation = None  # Может быть передан существующий JsonConversation

    async for response in CohereForAI_C4AI_Command.create_async_generator(
        model=model, 
        messages=messages, 
        api_key=api_key, 
        proxy=proxy,
        conversation=conversation,
        return_conversation=True
    ):
        if isinstance(response, JsonConversation):
            print(f"New conversation: {response.conversationId}")
        else:
            print(response, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())