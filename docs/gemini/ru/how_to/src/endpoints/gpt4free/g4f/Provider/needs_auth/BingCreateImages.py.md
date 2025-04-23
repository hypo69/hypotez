### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `BingCreateImages`, который является асинхронным генератором изображений с использованием Microsoft Designer в Bing. Он позволяет создавать изображения на основе текстового запроса (prompt) и возвращает результат в виде markdown-форматированной строки со ссылками на сгенерированные изображения.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются классы и функции из других модулей, таких как `get_cookies`, `ImageResponse`, `MissingAuthError`, `AsyncResult`, `Messages`, `Cookies`, `AsyncGeneratorProvider`, `ProviderModelMixin`, `create_images`, `create_session`, и `format_image_prompt`.
2. **Определение класса `BingCreateImages`**: Класс наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Указываются атрибуты класса, такие как `label`, `url`, `working`, `needs_auth`, `image_models`, и `models`.
3. **Инициализация класса `__init__`**: Конструктор класса принимает параметры `cookies`, `proxy` и `api_key`. Если передан `api_key`, он добавляется в cookies с ключом "_U".
4. **Создание асинхронного генератора `create_async_generator`**: Метод класса, который создает экземпляр класса `BingCreateImages` и вызывает метод `generate` для генерации изображений. Возвращает асинхронный генератор, который выдает результаты генерации изображений.
5. **Генерация изображений `generate`**: Асинхронный метод, который принимает текстовый запрос `prompt` и использует cookies для создания сессии с Bing. Если cookies отсутствуют или не содержат ключ "_U", выбрасывается исключение `MissingAuthError`. Далее, метод вызывает функцию `create_images` для генерации изображений на основе запроса и возвращает объект `ImageResponse` с результатами.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth import BingCreateImages

async def main():
    # Пример использования BingCreateImages для генерации изображений

    # Укажите ваш API ключ и/или cookies для аутентификации
    api_key = "YOUR_API_KEY"
    cookies = {"_U": "YOUR_COOKIE_U"}

    # Создайте экземпляр BingCreateImages с API ключом и/или cookies
    bing_images = BingCreateImages(cookies=cookies)

    # Определите текстовый запрос для генерации изображений
    prompt = "A futuristic cityscape at sunset"

    try:
        # Сгенерируйте изображения асинхронно
        image_response = await bing_images.generate(prompt)

        # Проверьте, успешно ли сгенерированы изображения
        if image_response and image_response.images:
            print("Images generated successfully:")
            for image in image_response.images:
                print(image)  # Вывод ссылок на изображения
        else:
            print("Failed to generate images.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())