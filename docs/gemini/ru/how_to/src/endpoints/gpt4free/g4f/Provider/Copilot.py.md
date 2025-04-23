### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой реализацию провайдера Microsoft Copilot для библиотеки `g4f`. Он позволяет взаимодействовать с Copilot через WebSocket для отправки запросов и получения ответов, включая текст и изображения. Код также включает функции для аутентификации и получения access token, а также для работы с медиафайлами.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Проверяется наличие необходимых библиотек `curl_cffi` и `nodriver`. Если `curl_cffi` отсутствует, выбрасывается исключение `MissingRequirementsError`.
   - Определяются параметры модели, URL WebSocket и URL для conversation API.

2. **Аутентификация**:
   - Проверяется наличие access token. Если он отсутствует, происходит попытка чтения из HAR-файла.
   - Если HAR-файл не найден или access token не получен, используется `nodriver` для получения access token и cookies через браузер.

3. **Создание сессии**:
   - Создается сессия `curl_cffi.requests.Session` с использованием прокси, timeout и заголовков.
   - Если access token был получен, он добавляется в заголовок `Authorization`.

4. **Получение информации о пользователе**:
   - Отправляется запрос к API для получения информации о пользователе.
   - В случае ошибки 401 (Invalid access token), выбрасывается исключение `MissingAuthError`.

5. **Создание или использование существующей conversation**:
   - Если conversation не предоставлен, создается новая conversation через POST-запрос к conversation API.
   - Если conversation предоставлен, используется существующий ID conversation.

6. **Обработка медиафайлов**:
   - Медиафайлы (изображения) объединяются с сообщениями и отправляются на сервер.
   - Изображения кодируются в байты и отправляются через POST-запрос к API attachments.

7. **Взаимодействие через WebSocket**:
   - Устанавливается WebSocket-соединение с сервером Copilot.
   - Отправляются сообщения для установки опций и отправки контента (текст и изображения) в conversation.

8. **Получение и обработка ответов**:
   - В цикле ожидаются сообщения от сервера.
   - Обрабатываются различные типы сообщений:
     - `appendText`: добавляет текст к ответу.
     - `generatingImage`: указывает на генерацию изображения.
     - `imageGenerated`: содержит URL сгенерированного изображения.
     - `done`: завершает conversation.
     - `suggestedFollowups`: предлагает варианты продолжения conversation.
     - `replaceText`: заменяет текст в ответе.
     - `error`: выбрасывает исключение `RuntimeError` с информацией об ошибке.

9. **Завершение**:
   - WebSocket-соединение закрывается.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.Copilot import Copilot
from src.endpoints.gpt4free.g4f.typing import Messages, MediaListType
from src.endpoints.gpt4free.g4f.providers.response import BaseConversation

async def main():
    model = "Copilot"
    messages: Messages = [{"role": "user", "content": "Напиши короткий стих о весне."}]
    stream = True
    proxy = None
    timeout = 900
    media: MediaListType = None
    conversation: BaseConversation = None
    return_conversation = False
    api_key = None

    try:
        result = Copilot.create_completion(
            model=model,
            messages=messages,
            stream=stream,
            proxy=proxy,
            timeout=timeout,
            media=media,
            conversation=conversation,
            return_conversation=return_conversation,
            api_key=api_key
        )

        async for response in result:
            print(response, end="")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())