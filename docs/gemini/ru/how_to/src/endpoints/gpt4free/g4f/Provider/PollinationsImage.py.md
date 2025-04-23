### Как использовать блок кода PollinationsImage
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `PollinationsImage`, который наследуется от `PollinationsAI`. Он предназначен для генерации изображений с использованием моделей Pollinations AI. Класс управляет списком доступных моделей изображений, загружает их и предоставляет асинхронный генератор для создания изображений на основе заданных параметров.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются `from __future__ import annotations`, `Optional` из `typing`, `format_image_prompt` из `helper`, `AsyncResult` и `Messages` из `..typing`, и `PollinationsAI` из `.PollinationsAI`.

2. **Определение класса `PollinationsImage`**:
   - Класс `PollinationsImage` наследуется от `PollinationsAI`.
   - Определяются атрибуты класса:
     - `label`: Строка, определяющая название провайдера изображений ("PollinationsImage").
     - `default_model`: Строка, определяющая модель по умолчанию ("flux").
     - `default_vision_model`: Модель для обработки изображений (в данном случае `None`).
     - `default_image_model`: Модель для генерации изображений по умолчанию (`default_model`).
     - `image_models`: Список моделей изображений, используемых по умолчанию (`[default_image_model]`).
     - `_models_loaded`: Флаг, указывающий, были ли загружены модели (изначально `False`).

3. **Метод `get_models`**:
   - Функция `get_models` извлекает и обновляет список доступных моделей изображений.
   - Проверяет, загружены ли модели, используя флаг `_models_loaded`. Если модели не загружены:
     - Функция вызывает метод `get_models` родительского класса (`super().get_models()`) для загрузки базовых моделей.
     - Объединяет модели из `cls.image_models`, `PollinationsAI.image_models` и `cls.extra_image_models`, чтобы получить полный список моделей.
     - Удаляет дубликаты из объединенного списка с помощью `dict.fromkeys`.
     - Обновляет атрибут `cls.image_models` полным списком моделей.
     - Устанавливает флаг `_models_loaded` в `True`, чтобы указать, что модели были загружены.
   - Возвращает список доступных моделей изображений.

4. **Метод `create_async_generator`**:
   - Функция `create_async_generator` создает асинхронный генератор для генерации изображений.
   - Принимает параметры:
     - `model` (str): Модель для генерации.
     - `messages` (Messages): Сообщения для генерации изображения.
     - `proxy` (str, optional): Прокси-сервер. По умолчанию `None`.
     - `prompt` (str, optional): Текстовое описание для генерации. По умолчанию `None`.
     - `aspect_ratio` (str): Соотношение сторон изображения. По умолчанию "1:1".
     - `width` (int, optional): Ширина изображения. По умолчанию `None`.
     - `height` (int, optional): Высота изображения. По умолчанию `None`.
     - `seed` (Optional[int], optional): Зерно для случайной генерации. По умолчанию `None`.
     - `cache` (bool): Флаг для использования кэша. По умолчанию `False`.
     - `nologo` (bool): Флаг для удаления логотипа. По умолчанию `True`.
     - `private` (bool): Флаг для приватности. По умолчанию `False`.
     - `enhance` (bool): Флаг для улучшения изображения. По умолчанию `False`.
     - `safe` (bool): Флаг для безопасного контента. По умолчанию `False`.
     - `n` (int): Количество изображений для генерации. По умолчанию 4.
     - `**kwargs`: Дополнительные параметры.
   - Функция вызывает `cls.get_models()` для обновления списка моделей.
   - Запускает асинхронный генератор `cls._generate_image` с переданными параметрами, форматируя prompt с помощью `format_image_prompt`.
   - Передает каждый чанк, сгенерированный `cls._generate_image`, через `yield`, делая `create_async_generator` асинхронным генератором.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    # Пример использования create_async_generator
    messages: Messages = [{"role": "user", "content": "A beautiful cat"}]
    model = "flux"
    aspect_ratio = "16:9"
    n = 2

    generator = PollinationsImage.create_async_generator(
        model=model,
        messages=messages,
        aspect_ratio=aspect_ratio,
        n=n
    )

    async for chunk in generator:
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())
```