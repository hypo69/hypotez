### **Как использовать блок кода класса `BackendApi`**

=========================================================================================

Описание
-------------------------
Класс `BackendApi` предназначен для асинхронного взаимодействия с API, отправки запросов и получения ответов в виде асинхронного генератора. Он поддерживает отправку текстовых сообщений и медиафайлов, а также позволяет передавать дополнительные параметры и ключи API.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `json`, `Messages`, `AsyncResult`, `MediaListType`, `StreamSession`, `to_data_uri`, `AsyncGeneratorProvider`, `ProviderModelMixin`, `RawResponse` и `debug`.

2. **Определение класса `BackendApi`**:
   - Создается класс `BackendApi`, наследуемый от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Устанавливаются параметры `ssl` и `headers` класса.

3. **Метод `create_async_generator`**:
   - Определяется асинхронный метод `create_async_generator`, который принимает следующие параметры:
     - `model` (str): Название модели для запроса.
     - `messages` (Messages): Список сообщений для отправки.
     - `media` (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
     - `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
     - `**kwargs`: Дополнительные параметры для запроса.

4. **Логирование**:
   - Выполняется логирование имени класса и ключа API с использованием `debug.log`.

5. **Обработка медиафайлов**:
   - Если `media` не `None`, выполняется итерация по списку медиафайлов, и каждый файл преобразуется в формат data URI с использованием функции `to_data_uri`.

6. **Создание асинхронной сессии**:
   - Создается асинхронная сессия с использованием `StreamSession` и контекстного менеджера `async with`.
   - Устанавливаются заголовки запроса, включая `Accept: text/event-stream` и дополнительные заголовки класса.

7. **Отправка POST-запроса**:
   - Отправляется POST-запрос к API с использованием `session.post`.
   - Формируется JSON-тело запроса, включающее `model`, `messages`, `media`, `api_key` и дополнительные параметры `kwargs`.
   - Указывается параметр `ssl` для сессии.

8. **Обработка ответа**:
   - Асинхронно итерируется по строкам ответа с использованием `response.iter_lines`.
   - Каждая строка преобразуется в объект `RawResponse` с использованием `json.loads` и передается в `yield`, что делает метод асинхронным генератором.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.template.BackendApi import BackendApi
from src.endpoints.gpt4free.g4f.typing import Messages, MediaListType
import asyncio

async def main():
    # Пример использования класса BackendApi
    model = "gpt-3.5-turbo"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    media: MediaListType = None
    api_key = "your_api_key"
    kwargs = {"temperature": 0.7}

    async for response in BackendApi.create_async_generator(
        model=model,
        messages=messages,
        media=media,
        api_key=api_key,
        **kwargs
    ):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())