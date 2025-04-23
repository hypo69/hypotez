### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `OpenaiTemplate`, который является асинхронным генератором для взаимодействия с API OpenAI. Он поддерживает текстовые и графические запросы, обрабатывает потоковую передачу данных и ошибки, а также предоставляет гибкие настройки для запросов.

Шаги выполнения
-------------------------
1. **Инициализация класса**:
   - Класс `OpenaiTemplate` наследуется от `AsyncGeneratorProvider`, `ProviderModelMixin` и `RaiseErrorMixin`, что обеспечивает асинхронную генерацию, поддержку моделей и обработку ошибок.
   - Определяются атрибуты класса, такие как `api_base`, `api_key`, `api_endpoint`, `supports_message_history`, `supports_system_message`, `default_model`, `fallback_models`, `sort_models` и `ssl`.

2. **Получение списка моделей**:
   - Метод `get_models` извлекает список доступных моделей из API OpenAI.
   - Он выполняет HTTP-запрос к `api_base/models`, используя `requests.get`.
   - Заголовки запроса включают авторизацию с использованием API-ключа, если он предоставлен.
   - В случае успеха, извлекаются `image_models` и `models` из JSON-ответа.
   - Если происходит ошибка, возвращается `fallback_models`.

3. **Создание асинхронного генератора**:
   - Метод `create_async_generator` создает асинхронный генератор для отправки запросов к API OpenAI и получения ответов.
   - Он принимает параметры, такие как `model`, `messages`, `proxy`, `timeout`, `media`, `api_key`, `api_endpoint`, `api_base`, `temperature`, `max_tokens`, `top_p`, `stop`, `stream`, `prompt`, `headers`, `impersonate`, `extra_parameters` и `extra_data`.
   - Если `api_key` не предоставлен, используется `cls.api_key`.
   - Если требуется аутентификация и `api_key` отсутствует, выбрасывается исключение `MissingAuthError`.

4. **Обработка запросов генерации изображений**:
   - Если модель указана в `cls.image_models`, формируется запрос на генерацию изображения.
   - Используется метод `format_image_prompt` для подготовки промпта на основе сообщений.
   - Отправляется POST-запрос к `api_base/images/generations` с использованием `session.post`.
   - Результат возвращается как `ImageResponse`.

5. **Обработка запросов завершения чата**:
   - Формируется запрос на завершение чата с использованием параметров, таких как `messages`, `model`, `temperature`, `max_tokens`, `top_p` и `stop`.
   - Отправляется POST-запрос к `api_endpoint` (или `api_base/chat/completions`, если `api_endpoint` не указан) с использованием `session.post`.
   - Обрабатываются ответы в формате JSON или text/event-stream.
   - Для JSON-ответов извлекается содержимое сообщения, вызовы инструментов и информация об использовании.
   - Для text/event-stream ответов обрабатываются потоковые данные и извлекаются дельты содержимого.
   - В случае ошибок выбрасывается исключение `ResponseError`.

6. **Получение заголовков запроса**:
   - Метод `get_headers` формирует заголовки для HTTP-запроса.
   - Заголовки включают `Accept` (application/json или text/event-stream в зависимости от `stream`), `Content-Type` (application/json) и авторизацию с использованием API-ключа, если он предоставлен.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.template import OpenaiTemplate
from src.endpoints.gpt4free.g4f.typing import Messages

# Пример использования для получения списка моделей
api_key = "YOUR_API_KEY"
models = OpenaiTemplate.get_models(api_key=api_key)
print(f"Доступные модели: {models}")

# Пример использования для создания асинхронного генератора
async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for response in OpenaiTemplate.create_async_generator(
        model="gpt-3.5-turbo",
        messages=messages,
        api_key=api_key,
        stream=True
    ):
        print(response, end="")

import asyncio
asyncio.run(main())