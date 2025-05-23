## Как использовать класс `GizAI`
=========================================================================================

Описание
-------------------------
Класс `GizAI`  предоставляет функциональность для взаимодействия с моделью искусственного интеллекта от GizAI через API. 
Он наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, обеспечивая асинхронную генерацию текста и поддержку различных моделей.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Создайте экземпляр класса `GizAI`.
   - Укажите модель, с которой хотите взаимодействовать (например, `chat-gemini-flash`).
   - Предоставьте список сообщений (`messages`) для отправки в модель.
   - Опционально, задайте прокси-сервер (`proxy`) для анонимности.
2. **Получение асинхронного генератора**:
   - Вызовите метод `create_async_generator` для получения асинхронного генератора, который будет производить ответы модели.
3. **Обработка ответа**:
   - Перебирайте элементы генератора с помощью цикла `async for`.
   - Обработайте полученные ответы модели.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.GizAI import GizAI
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Инициализация экземпляра класса GizAI
provider = GizAI(model="chat-gemini-flash")

# Создание списка сообщений
messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "Хорошо, а у тебя?"},
]

# Получение асинхронного генератора
async_generator = await provider.create_async_generator(messages=messages)

# Обработка ответа
async for response in async_generator:
    print(f"Ответ модели: {response}")

```