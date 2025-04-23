### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой класс `ImageLabs`, который является асинхронным провайдером для генерации изображений на основе текстовых запросов через API `editor.imagelabs.net`. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов.

Шаги выполнения
-------------------------
1. **Инициализация класса**:
   - Определяется класс `ImageLabs`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Устанавливаются базовые атрибуты, такие как `url`, `api_endpoint`, `working`, `supports_stream`, `supports_system_message`, `supports_message_history`, `default_model`, `default_image_model`, `image_models` и `models`.

2. **Метод `create_async_generator`**:
   - Этот метод является асинхронным генератором, который принимает параметры, такие как `model`, `messages`, `proxy`, `prompt`, `negative_prompt`, `width` и `height`.
   - Формируются заголовки HTTP-запроса, необходимые для взаимодействия с API `editor.imagelabs.net`.
   - Создается асинхронная сессия `aiohttp.ClientSession` с заданными заголовками.
   - Извлекается или устанавливается `prompt` из входящих `messages`.
   - Формируется полезная нагрузка (`payload`) для запроса к API, включающая параметры, такие как `prompt`, `seed`, `subseed`, `attention`, `width`, `height`, `tiling`, `negative_prompt`, `reference_image` и `reference_strength`.
   - Выполняется POST-запрос к `f'{cls.url}/txt2img'` с `payload` и прокси (если указан) для запуска генерации изображения.
   - Полученный `task_id` используется для последующего опроса состояния задачи.

3. **Опрос состояния задачи**:
   - Запускается бесконечный цикл, в котором происходит опрос API для получения прогресса выполнения задачи генерации изображения.
   - Выполняется POST-запрос к `f'{cls.url}/progress'` с `task_id` и прокси (если указан).
   - Анализируется ответ, чтобы определить, завершена ли задача или произошла ошибка.
   - Если задача завершена (`status` == `'Done'` или получен `final_image_url`), возвращается объект `ImageResponse` с URL-адресом сгенерированного изображения и `alt` текстом (prompt).
   - Если в статусе задачи содержится ошибка (`'error' in status.lower()`), выбрасывается исключение с сообщением об ошибке.
   - Если задача еще не завершена, поток приостанавливается на 1 секунду перед следующей попыткой опроса.

4. **Метод `get_model`**:
   - Этот метод возвращает модель по умолчанию (`cls.default_model`).

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.ImageLabs import ImageLabs
from src.endpoints.gpt4free.g4f.typing import Message

async def main():
    messages: list[Message] = [{"role": "user", "content": "A cat in space"}]
    
    # Использование create_async_generator для генерации изображений
    result = ImageLabs.create_async_generator(
        model='sdxl-turbo',
        messages=messages,
        width=512,
        height=512
    )
    
    # Получение и отображение результатов генерации
    async for item in result:
        print(item.images[0])  # Вывод URL первого сгенерированного изображения

if __name__ == "__main__":
    asyncio.run(main())
```