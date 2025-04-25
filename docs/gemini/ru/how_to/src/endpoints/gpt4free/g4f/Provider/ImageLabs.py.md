## Как использовать класс `ImageLabs` для генерации изображений 

=========================================================================================

### Описание
-------------------------
Класс `ImageLabs` реализует асинхронный генератор для создания изображений с использованием модели Stable Diffusion XL от ImageLabs. Он предоставляет функции для отправки запросов на генерацию изображений, проверки прогресса и получения результата.

### Шаги выполнения
-------------------------
1. **Инициализация**: 
    - Создайте экземпляр класса `ImageLabs`.
    - Укажите модель Stable Diffusion XL, которую хотите использовать, при помощи аргумента `model`.
    - Укажите текст подсказки для генерации изображения в аргументе `prompt`.
    - Дополнительно можно указать `negative_prompt`, `width`, `height` и другие параметры для управления процессом генерации.
    - Получите асинхронный генератор с помощью метода `create_async_generator`.

2. **Запуск генерации**:
    - Используйте цикл `async for` для итерации по асинхронному генератору.
    - Внутри цикла `async for` получите объект `ImageResponse`, который содержит сгенерированное изображение.

3. **Обработка результата**:
    - Доступ к URL изображения можно получить из свойства `images` объекта `ImageResponse`.
    - Используйте полученный URL для загрузки изображения или для других целей.

### Пример использования
-------------------------
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.ImageLabs import ImageLabs

async def generate_image():
    # Создаем экземпляр класса ImageLabs с моделью sdxl-turbo
    image_generator = ImageLabs(model='sdxl-turbo')

    # Задаем текст подсказки и дополнительные параметры
    prompt = "A photorealistic image of a cat wearing a hat"
    width = 512
    height = 512

    # Получаем асинхронный генератор
    async_generator = await image_generator.create_async_generator(
        prompt=prompt,
        width=width,
        height=height
    )

    # Итерируемся по генератору и обрабатываем результат
    async for image_response in async_generator:
        # Получаем URL сгенерированного изображения
        image_url = image_response.images[0]

        # Выводим URL изображения в консоль
        print(f"Generated image URL: {image_url}")

# Запускаем асинхронную функцию
asyncio.run(generate_image())

```