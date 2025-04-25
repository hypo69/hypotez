## Как использовать класс BingCreateImages
=========================================================================================

Описание
-------------------------
Класс `BingCreateImages` предоставляет функциональность для асинхронной генерации изображений с использованием сервиса Microsoft Designer в Bing. Он наследует от классов `AsyncGeneratorProvider` и `ProviderModelMixin`, предоставляя базовую функциональность для асинхронной генерации и управления моделями.

Шаги выполнения
-------------------------
1. **Инициализация класса:** 
    - Создается экземпляр класса `BingCreateImages`, передавая в конструктор необязательные параметры:
        - `cookies`: Словарь с куки для аутентификации на Bing.
        - `proxy`: Прокси-сервер для использования при отправке запросов.
        - `api_key`: API-ключ для доступа к сервису.
2. **Генерация изображений:** 
    - Используется метод `generate` для асинхронной генерации изображения по заданному `prompt`.
    - Метод `generate` автоматически извлекает необходимые куки, если они не переданы в конструктор.
    - Проверяется наличие куки `"_U"` (API-ключ), если она отсутствует, генерируется исключение `MissingAuthError`.
    - Используется функция `create_session` для создания сессии на сайте Bing.
    - Вызывается функция `create_images` для асинхронной генерации изображений по заданному `prompt`.
    - Возвращается объект `ImageResponse`, содержащий список сгенерированных изображений, `prompt` и словарь с метаданными для изображений.
3. **Использование класса `AsyncGeneratorProvider`:** 
    - Класс `BingCreateImages` реализует интерфейс `AsyncGeneratorProvider`, что позволяет использовать его для асинхронной генерации изображений в цикле.
    - Метод `create_async_generator` возвращает асинхронный генератор, который позволяет получить доступ к результатам генерации изображений.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.BingCreateImages import BingCreateImages
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр класса BingCreateImages
bing_image_generator = BingCreateImages(api_key="YOUR_API_KEY")

# Задаем сообщение для генерации изображения
messages = Messages(
    role="user",
    content="Сгенерировать изображение кота, который сидит на стуле"
)

# Асинхронно генерируем изображение
async def generate_image():
    async for response in bing_image_generator.create_async_generator(model="dall-e-3", messages=messages):
        print(response)

# Запускаем функцию
asyncio.run(generate_image())
```

**Примечание:** 
- API-ключ для Bing можно получить на сайте Microsoft Azure.
- Для использования класса `BingCreateImages` требуется установка библиотеки `asyncio`.