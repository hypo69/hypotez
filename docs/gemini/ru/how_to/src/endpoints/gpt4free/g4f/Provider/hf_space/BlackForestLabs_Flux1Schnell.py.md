Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `BlackForestLabs_Flux1Schnell`, который является асинхронным провайдером для генерации изображений с использованием API Black Forest Labs Flux-1-Schnell. Он позволяет генерировать изображения на основе текстового запроса, используя API endpoints для отправки запросов и получения результатов.

Шаги выполнения
-------------------------
1. **Подготовка параметров**:
   - Функция `create_async_generator` принимает параметры, такие как `model` (модель для генерации), `messages` (сообщения для формирования запроса), `width` и `height` (размеры изображения), `num_inference_steps` (количество шагов для генерации), `seed` (начальное значение для генерации) и другие.
   - Размеры изображения `width` и `height` корректируются, чтобы быть кратными 8 и не менее 32.
   - Формируется `prompt` (текстовый запрос) для генерации изображения на основе входных `messages`.

2. **Формирование payload**:
   - Создается словарь `payload`, содержащий данные для отправки в API, включая `prompt`, `seed`, `randomize_seed`, `width`, `height` и `num_inference_steps`.

3. **Отправка запроса к API**:
   - Используется `ClientSession` из библиотеки `aiohttp` для выполнения асинхронных HTTP-запросов.
   - Отправляется `POST` запрос к API endpoint (`cls.api_endpoint`) с сформированным `payload` в формате JSON.
   - Проверяется статус ответа с помощью `raise_for_status`, чтобы убедиться, что запрос выполнен успешно.

4. **Получение и обработка event_id**:
   - Извлекается `event_id` из JSON-ответа, который используется для получения статуса генерации изображения.

5. **Цикл ожидания и обработки статуса**:
   - Организуется бесконечный цикл (`while True`) для опроса статуса генерации изображения.
   - В цикле отправляется `GET` запрос к API endpoint статуса (`f"{cls.api_endpoint}/{event_id}"`).
   - Читаются данные из ответа по частям (events) до тех пор, пока не будет получен полный ответ.
   - Каждая часть ответа проверяется на наличие `event:`, чтобы определить тип события (error или complete).

6. **Обработка событий**:
   - Если `event_type` равен `error`, выбрасывается исключение `ResponseError` с сообщением об ошибке.
   - Если `event_type` равен `complete`, извлекается URL изображения из JSON-данных и генерируется объект `ImageResponse`, который содержит URL изображения и альтернативный текст (`prompt`).
   - Объект `ImageResponse` возвращается через `yield`, что делает функцию асинхронным генератором.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Schnell import BlackForestLabs_Flux1Schnell
import asyncio

async def main():
    model = "black-forest-labs-flux-1-schnell"
    messages = [{"role": "user", "content": "A beautiful landscape"}]
    
    generator = BlackForestLabs_Flux1Schnell.create_async_generator(
        model=model,
        messages=messages,
        width=512,
        height=512,
        num_inference_steps=2
    )
    
    async for response in generator:
        if response and response.images:
            print(f"Image URL: {response.images[0]}")
            break

if __name__ == "__main__":
    asyncio.run(main())