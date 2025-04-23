### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `StabilityAI_SD35Large`, который является асинхронным провайдером для генерации изображений с использованием модели Stability AI SD-3.5-Large. Он взаимодействует с API Stability AI через HTTP-запросы, отправляя текстовый запрос (prompt) и получая URL сгенерированного изображения. Класс поддерживает различные параметры для настройки генерации изображения, такие как соотношение сторон, размеры изображения, seed для воспроизводимости и т.д.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `json`, `ClientSession` из `aiohttp` для работы с HTTP-запросами и JSON-данными.
   - Из модуля `...typing` импортируются `AsyncResult`, `Messages` для аннотации типов.
   - Из `...providers.response` импортируются `ImageResponse` и `ImagePreview` для обработки ответов с изображениями.
   - Из `...image` импортируется `use_aspect_ratio` для корректировки соотношения сторон изображения.
   - Из `...errors` импортируется `ResponseError` для обработки ошибок при запросах.
   - Из `..base_provider` импортируются `AsyncGeneratorProvider` и `ProviderModelMixin` для создания асинхронного провайдера.
   - Из `..helper` импортируется `format_image_prompt` для форматирования запроса изображения.

2. **Определение класса `StabilityAI_SD35Large`**:
   - Класс наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет использовать его как асинхронный провайдер.
   - Устанавливаются атрибуты класса:
     - `label`: Отображаемое имя провайдера.
     - `url`: URL API Stability AI.
     - `api_endpoint`: Endpoint для вызова API.
     - `working`: Флаг, указывающий, что провайдер в рабочем состоянии.
     - `default_model`: Модель, используемая по умолчанию.
     - `model_aliases`: Алиасы для модели.
     - `image_models`: Список поддерживаемых моделей изображений.
     - `models`: Список моделей.

3. **Реализация асинхронного генератора `create_async_generator`**:
   - Метод принимает параметры:
     - `model`: Используемая модель.
     - `messages`: Список сообщений для формирования запроса (prompt).
     - `prompt`: Текстовый запрос для генерации изображения.
     - `negative_prompt`: Негативный запрос, описывающий, что не должно быть на изображении.
     - `api_key`: API-ключ для доступа к Stability AI.
     - `proxy`: Прокси-сервер для выполнения запросов.
     - `aspect_ratio`: Соотношение сторон изображения.
     - `width`: Ширина изображения.
     - `height`: Высота изображения.
     - `guidance_scale`: Масштаб соответствия запросу.
     - `num_inference_steps`: Количество шагов для генерации изображения.
     - `seed`: Seed для воспроизводимости результатов.
     - `randomize_seed`: Флаг для рандомизации seed.
   - Формируются заголовки запроса, включая API-ключ, если он предоставлен.
   - Создается асинхронная сессия `ClientSession` с установленными заголовками.
   - Форматируется запрос `prompt` с использованием `format_image_prompt`.
   - Определяются параметры изображения с использованием `use_aspect_ratio`.
   - Формируется JSON-данные для отправки в API.
   - Выполняется POST-запрос к API для запуска генерации изображения.
   - Извлекается `event_id` из ответа для последующего получения результатов.
   - Выполняется GET-запрос к API с `event_id` для получения сгенерированного изображения.
   - Читаются чанки из ответа:
     - Если чанк начинается с `event:`, извлекается тип события.
     - Если чанк начинается с `data:`, обрабатываются данные:
       - Если `event` равен "error", выбрасывается исключение `ResponseError`.
       - Если `event` равен "complete" или "generating", извлекается URL изображения из JSON-данных.
       - Если `event` равен "generating", возвращается `ImagePreview`.
       - Если `event` равен "complete", возвращается `ImageResponse` и завершается генерация.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space import StabilityAI_SD35Large
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    model = "stabilityai-stable-diffusion-3-5-large"
    messages: Messages = [{"role": "user", "content": "A cat wearing a hat"}]
    api_key = "YOUR_API_KEY"  # Замените на ваш реальный API-ключ
    aspect_ratio = "16:9"

    generator = StabilityAI_SD35Large.create_async_generator(
        model=model,
        messages=messages,
        api_key=api_key,
        aspect_ratio=aspect_ratio
    )

    try:
        async for item in generator:
            if isinstance(item, StabilityAI_SD35Large.ImagePreview):
                print(f"Preview URL: {item.url}")
            elif isinstance(item, StabilityAI_SD35Large.ImageResponse):
                print(f"Final Image URL: {item.url}")
                break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())