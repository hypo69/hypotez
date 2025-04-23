### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `Prodia`, который является асинхронным провайдером для генерации изображений с использованием API Prodia. Он позволяет генерировать изображения на основе текстового запроса (prompt) с использованием различных моделей и параметров.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Класс `Prodia` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он определяет URL, endpoint API, список поддерживаемых моделей изображений и параметры по умолчанию.
2. **Получение модели**: Метод `get_model` проверяет, существует ли запрошенная модель в списке поддерживаемых моделей или алиасов. Если модель не найдена, возвращается модель по умолчанию.
3. **Создание асинхронного генератора**: Метод `create_async_generator` принимает текстовый запрос, модель и другие параметры генерации изображения. Он отправляет запрос к API Prodia и возвращает URL сгенерированного изображения.
4. **Опрос статуса задачи**: Метод `_poll_job` периодически проверяет статус задачи генерации изображения, отправляя запросы к API Prodia. Когда задача завершается успешно, возвращается URL изображения. Если задача завершается с ошибкой или истекает время ожидания, выбрасывается исключение.

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.Prodia import Prodia

async def main():
    # Настройка параметров
    model = "absolutereality_v181.safetensors [3d9d4d2b]"
    messages = [{"role": "user", "content": "A beautiful landscape"}]
    negative_prompt = "ugly, distorted"
    steps = 25
    cfg = 8
    seed = 42
    sampler = "DPM++ 2M Karras"
    aspect_ratio = "landscape"

    # Создание асинхронного генератора
    generator = await Prodia.create_async_generator(
        model=model,
        messages=messages,
        negative_prompt=negative_prompt,
        steps=steps,
        cfg=cfg,
        seed=seed,
        sampler=sampler,
        aspect_ratio=aspect_ratio
    )

    # Получение результата
    async for image_response in generator:
        if image_response.url:
            print(f"Image URL: {image_response.url}")
        else:
            print("Image generation failed.")

if __name__ == "__main__":
    asyncio.run(main())