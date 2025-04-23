### Как использовать блок кода HuggingFaceInference
=========================================================================================

Описание
-------------------------
Этот код определяет класс `HuggingFaceInference`, который является асинхронным генератором для взаимодействия с моделями Hugging Face Inference API. Он поддерживает как текстовые, так и графические модели, а также предоставляет методы для получения списка доступных моделей и их метаданных.

Шаги выполнения
-------------------------
1. **Инициализация класса**:
   - Класс `HuggingFaceInference` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Определяются основные атрибуты, такие как `url`, `parent`, `working`, `default_model`, `default_image_model` и `model_aliases`.

2. **Получение списка моделей**:
   - Метод `get_models` получает список поддерживаемых моделей.
   - Он запрашивает список моделей для генерации текста и преобразования текста в изображение с API Hugging Face.
   - Объединяет полученные списки и возвращает общий список моделей.

3. **Получение метаданных модели**:
   - Метод `get_model_data` получает метаданные для конкретной модели.
   - Если метаданные уже закэшированы, они возвращаются из `cls.model_data`.
   - В противном случае выполняется запрос к API Hugging Face для получения метаданных и сохранения их в кэше.

4. **Создание асинхронного генератора**:
   - Метод `create_async_generator` создает асинхронный генератор для взаимодействия с моделью.
   - Он принимает параметры, такие как `model`, `messages`, `stream`, `proxy`, `timeout`, `api_base`, `api_key`, `max_tokens`, `temperature`, `prompt`, `action`, `extra_data`, `seed`, `aspect_ratio`, `width` и `height`.
   - В зависимости от типа модели (текстовая или графическая) формируется соответствующий запрос к API Hugging Face.
   - Для графических моделей используется `provider_together_urls`, если модель поддерживается.
   - Для текстовых моделей формируется полезная нагрузка (`payload`) с входными данными и параметрами.
   - Ответ от API обрабатывается потоково, если `stream=True`, или целиком, если `stream=False`.

5. **Форматирование входных данных**:
   - Используются различные методы форматирования входных данных (`format_prompt_*`) в зависимости от типа модели.
   - Метод `get_inputs` выбирает правильный метод форматирования на основе метаданных модели.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf.HuggingFaceInference import HuggingFaceInference
from src.requests import StreamSession

async def main():
    # Пример использования текстовой модели
    model = "google/gemma-7b-it"
    messages = [
        {"role": "user", "content": "Напиши короткое стихотворение о весне."}
    ]
    async for chunk in HuggingFaceInference.create_async_generator(model=model, messages=messages):
        print(chunk, end="")

    # Пример использования графической модели
    model = "stabilityai/stable-diffusion-2-1"
    messages = [
        {"role": "user", "content": "A beautiful landscape."}
    ]
    async for chunk in HuggingFaceInference.create_async_generator(model=model, messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())