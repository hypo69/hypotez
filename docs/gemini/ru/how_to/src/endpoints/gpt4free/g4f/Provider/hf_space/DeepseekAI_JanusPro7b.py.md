### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой асинхронный провайдер для модели DeepseekAI Janus-Pro-7B, размещенной на Hugging Face Spaces. Он обеспечивает возможность взаимодействия с моделью для генерации текста и изображений, используя API Hugging Face.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Определяются основные атрибуты класса, такие как `label`, `space`, `url`, `api_url` и `referer`.
   - Указываются поддерживаемые функции, такие как стриминг, системные сообщения и история сообщений.
   - Устанавливаются модели по умолчанию для текста и изображений.

2. **Метод `run`**:
   - Определяет, какой HTTP-метод (POST или GET) использовать для взаимодействия с API в зависимости от типа запроса (текст или изображение).
   - Формирует заголовки запроса, включая токены авторизации и UUID.
   - Отправляет запрос к API и возвращает ответ.

3. **Метод `create_async_generator`**:
   - Подготавливает асинхронный генератор для взаимодействия с моделью.
   - Определяет метод запроса (`post` или `image`) в зависимости от типа задачи.
   - Форматирует промпт, если он не был предоставлен.
   - Генерирует случайный seed для воспроизводимости результатов, если seed не был предоставлен.
   - Создает или использует существующую сессию для взаимодействия с API.
   - Загружает медиафайлы (изображения) на сервер, если они предоставлены.
   - Отправляет запросы к API и обрабатывает ответы, возвращая результаты в виде текста или изображений.
   - Обрабатывает ошибки и исключения, возвращая соответствующие сообщения.

4. **Метод `get_zerogpu_token`**:
   - Получает токены авторизации и UUID, необходимые для доступа к API Hugging Face Spaces.
   - Использует cookies для аутентификации и получения токенов.
   - Возвращает токены для использования в последующих запросах.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.DeepseekAI_JanusPro7b import DeepseekAI_JanusPro7b
from src.requests.aiohttp import StreamSession
from src.providers.response import JsonConversation

async def main():
    # Создание сессии
    async with StreamSession() as session:
        # Пример использования модели для генерации текста
        model = "janus-pro-7b"
        messages = [{"role": "user", "content": "Напиши короткий рассказ о космосе."}]
        conversation = JsonConversation(session_hash="test_session")

        async for response in DeepseekAI_JanusPro7b.create_async_generator(
            model=model,
            messages=messages,
            conversation=conversation
        ):
            print(response)

        # Пример использования модели для генерации изображений
        model = DeepseekAI_JanusPro7b.default_image_model
        prompt = "Космический корабль в далекой галактике."
        async for response in DeepseekAI_JanusPro7b.create_async_generator(
            model=model,
            prompt=prompt,
            conversation=conversation
        ):
            print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())