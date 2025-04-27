## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует, как инициализировать и использовать класс `XAI`, который позволяет взаимодействовать с xAI API, чтобы получить ответы от моделей xAI, как в стандартном, так и в режиме потоковой передачи.

Шаги выполнения
-------------------------
1. **Инициализация:** Создаем объект класса `XAI`, передавая в качестве аргумента свой API ключ.
2. **Создание запроса:**  Создаем список `messages`, представляющий диалог с моделью. Каждый элемент списка — словарь с ключами `role` (роль отправителя — `system`, `user`, `assistant`) и `content` (текст сообщения).
3. **Выполнение запроса:** 
    - **Стандартный запрос:** Вызываем метод `chat_completion` с созданным списком `messages`. Получаем полный ответ от модели.
    - **Потоковый запрос:**  Вызываем метод `stream_chat_completion` с созданным списком `messages`. Получаем ответ от модели частями (строками), которые можно обрабатывать в режиме реального времени.

Пример использования
-------------------------

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш реальный API ключ
xai = XAI(api_key)

messages = [
    {
        "role": "system",
        "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
    },
    {
        "role": "user",
        "content": "What is the answer to life and universe?"
    }
]

# Стандартный запрос
completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)

# Потоковый запрос
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```