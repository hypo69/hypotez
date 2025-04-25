## Как использовать класс Prodia для генерации изображений
=========================================================================================

Описание
-------------------------
Класс `Prodia` предоставляет функционал для генерации изображений с использованием API Prodia. 

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
    - Импортируй класс `Prodia` из модуля `hypotez/src/endpoints/gpt4free/g4f/Provider/not_working/Prodia.py`.
2. **Инициализация класса**:
    - Создай экземпляр класса `Prodia`.
3. **Генерация изображения**:
    - Вызови метод `create_async_generator` класса `Prodia`. 
    - Передай необходимые параметры, такие как `model` (модель, которую нужно использовать), `messages` (текстовые подсказки для генерации), `seed` (случайное число для инициализации генератора). 
    - Метод `create_async_generator` возвращает асинхронный генератор, который генерирует объекты `ImageResponse` с URL-адресом полученного изображения. 
4. **Обработка результатов**:
    - Используй цикл `async for` для получения каждого `ImageResponse` из генератора.
    - Доступ к URL-адресу изображения можно получить с помощью свойства `image_url` объекта `ImageResponse`.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Prodia import Prodia
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def generate_image():
    """
    Пример использования класса Prodia для генерации изображения.
    """
    provider = Prodia()

    # Текстовые подсказки для генерации изображения
    messages: Messages = [
        {
            'role': 'user',
            'content': 'Котик сидит на столе, смотрит на камеру, кружок свежий',
        }
    ]

    # Запуск асинхронного генератора
    async for image_response in provider.create_async_generator(model='absolutereality_v181.safetensors [3d9d4d2b]', messages=messages):
        # Получение URL-адреса изображения
        image_url = image_response.image_url
        # Обработка изображения (сохранение, отображение и т.д.)
        print(f'Image generated: {image_url}')

# Запуск асинхронной функции
asyncio.run(generate_image())
```