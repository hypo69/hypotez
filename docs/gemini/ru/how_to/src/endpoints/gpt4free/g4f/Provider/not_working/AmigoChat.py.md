## Как использовать блок кода AmigoChat
=========================================================================================

Описание
-------------------------
Блок кода `AmigoChat` представляет собой класс, реализующий провайдера для взаимодействия с сервисом AmigoChat.  Он позволяет генерировать текст и изображения с использованием различных моделей. 

Шаги выполнения
-------------------------
1. **Инициализация провайдера**: Создайте экземпляр класса `AmigoChat`.
2. **Выбор модели**:  
    -  Используйте `chat_models` для получения списка доступных моделей для генерации текста. 
    - Используйте `image_models` для получения списка доступных моделей для генерации изображений.
    -  Используйте `model_aliases` для получения  альтернативных названий моделей.
3. **Генерация текста**: 
    -  Используйте метод `create_async_generator` для запуска генерации текста.
    -  Передайте необходимые параметры:
        - `model`: название модели для генерации.
        - `messages`: список сообщений в формате  `Messages`  (массив словарей с ключами `role` и `content`).
        -  Дополнительно можете указать другие параметры для настройки генерации, такие как `temperature`, `top_p`, `frequency_penalty`, `presence_penalty`, `max_tokens` и др.
4. **Обработка результатов**: 
    -  Метод `create_async_generator` возвращает асинхронный генератор, который можно использовать для  получения ответов от модели.
    -  Проходите по результатам с помощью цикла `async for` и обрабатывайте полученные ответы.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AmigoChat import AmigoChat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра провайдера
provider = AmigoChat()

# Получение списка доступных моделей
chat_models = provider.chat_models
print(f"Доступные модели для чата: {chat_models}")

# Генерация текста с помощью модели "gpt-4o-mini"
messages = Messages([
    {"role": "user", "content": "Расскажи мне анекдот."}
])
async for response in provider.create_async_generator(model="gpt-4o-mini", messages=messages):
    print(f"Ответ: {response}") 

# Генерация изображения с помощью модели "flux-pro"
messages = Messages([
    {"role": "user", "content": "Сгенерируй изображение кота, сидящего на диване."}
])
async for response in provider.create_async_generator(model="flux-pro", messages=messages):
    print(f"URL изображения: {response.image_urls}")
```