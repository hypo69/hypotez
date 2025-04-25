## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот фрагмент кода представляет собой класс `BlackForestLabs_Flux1Dev`, который реализует асинхронный генератор для модели Flux-1-Dev от BlackForestLabs, размещенной на платформе Hugging Face Spaces.

Шаги выполнения
-------------------------
1. **Импорт библиотек:** Импортируются необходимые библиотеки, включая `json`, `uuid`, `StreamSession` и другие, для работы с асинхронным API, обработкой сообщений, изображениями и ошибками.
2. **Объявление класса:** Определяется класс `BlackForestLabs_Flux1Dev`, наследующий от `AsyncGeneratorProvider` и `ProviderModelMixin`.
3. **Атрибуты класса:** Задаются основные атрибуты, такие как:
    - `label`: Метка модели (BlackForestLabs Flux-1-Dev).
    - `url`: URL-адрес сервиса.
    - `space`: Имя пространства Hugging Face.
    - `referer`: URL-адрес для запросов.
    - `working`: Флаг, указывающий на доступность модели (True).
    - `default_model`: Имя модели по умолчанию.
    - `default_image_model`:  Имя модели по умолчанию для изображений.
    - `model_aliases`: Словарь алиасов для модели.
    - `image_models`: Список поддерживаемых моделей для изображений.
    - `models`: Список всех моделей.
4. **Метод `run`:** Реализует отправку HTTP-запросов к модели, используя метод `POST` для отправки запроса на очередь и метод `GET` для получения данных из очереди.
    - Обрабатывает заголовки запросов, включая `zerogpu_token`, `zerogpu_uuid`, `referer` и другие.
5. **Метод `create_async_generator`:** Создает асинхронный генератор, который:
    - Инициализирует сеанс `StreamSession`.
    - Форматирует запрос для модели, используя информацию из `messages` и `prompt`.
    - Создает объект `JsonConversation`, который содержит информацию о сессии, `zerogpu_token` и `zerogpu_uuid`.
    - Запускает асинхронный цикл для обработки ответов от модели:
        - Отправляет POST-запрос к модели с запросом.
        - Проверяет статус ответа.
        - Выполняет GET-запрос для получения данных.
        - Обрабатывает данные, полученные из очереди:
            - Если данные - сообщение о статусе (log, progress), отправляет его в генератор.
            - Если данные - изображения, отправляет их в генератор как `ImagePreview` или `ImageResponse`.
        - В случае успешного завершения отправляет сообщение о завершении в генератор.
6. **Обработка ошибок:** В блоке `try-except` обрабатываются ошибки, возникающие при обработке ответов от модели (JSONDecodeError, KeyError, TypeError), и отправляются в генератор как исключение `RuntimeError`.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev import BlackForestLabs_Flux1Dev
from hypotez.src.endpoints.gpt4free.g4f.requests import StreamSession
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
from hypotez.src.endpoints.gpt4free.g4f.providers.response import ImageResponse

async def main():
    messages: Messages = [
        {"role": "user", "content": "Нарисуй мне изображение кота, сидящего на диване."},
    ]
    async with StreamSession(impersonate="chrome") as session:
        async for result in BlackForestLabs_Flux1Dev.create_async_generator(
            model="flux", messages=messages, session=session
        ):
            if isinstance(result, ImageResponse):
                print(f"Generated image URL: {result.url}")
                # Обрабатывайте изображение, используя URL

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```