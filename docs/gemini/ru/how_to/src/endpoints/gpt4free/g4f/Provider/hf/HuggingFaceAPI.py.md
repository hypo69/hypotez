### Как использовать блок кода HuggingFaceAPI
=========================================================================================

Описание
-------------------------
Этот код определяет класс `HuggingFaceAPI`, который наследуется от `OpenaiTemplate` и предназначен для взаимодействия с API Hugging Face для генерации текста. Класс поддерживает различные модели, включая модели для работы с изображениями, и обеспечивает гибкий механизм для выбора и конфигурации моделей через API Hugging Face.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются необходимые классы и типы из других модулей, включая `requests`, `StreamSession`, `ProviderInfo`, `OpenaiTemplate`, а также специфичные для Hugging Face модели и обработку ошибок.

2. **Определение класса `HuggingFaceAPI`**:
   - Класс `HuggingFaceAPI` наследуется от `OpenaiTemplate`.
   - Устанавливаются основные атрибуты класса, такие как `label`, `parent`, `url`, `api_base`, `working`, `needs_auth`, `default_model`, `default_vision_model`, `vision_models`, `model_aliases` и `fallback_models`.
   - Определяется словарь `provider_mapping`, который связывает модели с их конфигурациями на стороне Hugging Face.

3. **Метод `get_model`**:
   - Переопределяет метод `get_model` для получения имени модели.
   - В случае, если модель не поддерживается, возвращает исходное имя модели.

4. **Метод `get_models`**:
   - Получает список доступных моделей с API Hugging Face.
   - Если запрос успешен, извлекает идентификаторы моделей, поддерживающих "conversational" задачу.
   - Если запрос не успешен, использует `fallback_models` в качестве списка моделей.

5. **Метод `get_mapping`**:
   - Получает конфигурацию модели из `provider_mapping`.
   - Если конфигурация не найдена, запрашивает её с API Hugging Face и сохраняет в `provider_mapping`.

6. **Метод `create_async_generator`**:
   - Создает асинхронный генератор для получения чанков текста от API Hugging Face.
   - Выбирает модель, получает её конфигурацию, и настраивает параметры запроса.
   - Обрабатывает ошибки, такие как `ModelNotSupportedError` и `PaymentRequiredError`.
   - Использует `super().create_async_generator` для фактического запроса к API и генерации чанков.

7. **Функция `calculate_lenght`**:
   - Вычисляет длину сообщений.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf.HuggingFaceAPI import HuggingFaceAPI
from src.providers.types import Messages

async def main():
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    model = "google/gemma-3-27b-it"
    api_key = "YOUR_API_KEY"

    try:
        async for provider in HuggingFaceAPI.create_async_generator(model=model, messages=messages, api_key=api_key):
            print(f"Provider: {provider}")
        
        async for chunk in HuggingFaceAPI.create_async_generator(model=model, messages=messages, api_key=api_key):
            print(f"Chunk: {chunk}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```