## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода представляет класс `MicrosoftDesigner`, реализующий  асинхронный генератор изображений с помощью Microsoft Designer.  Класс наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, предоставляя функционал для асинхронной генерации и управления моделями.

Шаги выполнения
-------------------------
1. **Инициализация класса:** Создается экземпляр класса `MicrosoftDesigner`, используя класс `AsyncGeneratorProvider`.
2. **Вызов метода `create_async_generator`:**  Метод запускает асинхронный генератор, принимая модель, сообщения и опциональные параметры.
3. **Вызов метода `generate`:** Метод `generate` формирует запрос к API Microsoft Designer с использованием доступа к токену и user agent, а также полученному промт (текстовому описанию), и возвращает объект `ImageResponse` c результатом.
4. **Обработка результата:**  Полученный объект `ImageResponse` содержит список сгенерированных изображений и промт.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MicrosoftDesigner import MicrosoftDesigner

async def generate_image_with_microsoft_designer():
    # Инициализация класса
    designer = MicrosoftDesigner()

    # Текстовый промт для генерации изображения
    prompt = "A beautiful cat sitting on a window sill"

    # Запуск асинхронного генератора
    async for image_response in designer.create_async_generator(model="dall-e-3", messages=[{"role": "user", "content": prompt}]):
        # Обработка результата
        images = image_response.images
        print(f"Generated images: {images}")

# Вызов асинхронной функции
asyncio.run(generate_image_with_microsoft_designer())
```