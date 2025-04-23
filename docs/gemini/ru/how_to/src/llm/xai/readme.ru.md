## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой документацию для Python-клиента, предназначенного для взаимодействия с API xAI. Клиент позволяет отправлять запросы к API xAI, включая как стандартные, так и потоковые запросы, упрощая процесс интеграции с моделями xAI.

Шаги выполнения
-------------------------
1. **Установка зависимостей**:
   - Установите Python на вашей системе.
   - Установите необходимые зависимости с помощью pip:
     ```bash
     pip install requests
     ```

2. **Инициализация клиента**:
   - Импортируйте класс `XAI` из модуля `xai`.
   - Инициализируйте класс `XAI` с вашим ключом API:
     ```python
     from xai import XAI

     api_key = "your_api_key_here"  # Функция изменяет значение переменной на ваш реальный ключ API
     xai = XAI(api_key)
     ```

3. **Отправка запроса на завершение чата (непотоковый)**:
   - Подготовьте список сообщений для отправки в API.
   - Вызовите метод `chat_completion` для получения ответа:
     ```python
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

     completion_response = xai.chat_completion(messages)
     print("Non-streaming response:", completion_response)
     ```

4. **Отправка запроса на завершение чата (потоковый)**:
   - Подготовьте список сообщений для отправки в API.
   - Вызовите метод `stream_chat_completion` для получения потокового ответа:
     ```python
     stream_response = xai.stream_chat_completion(messages)
     print("Streaming response:")
     for line in stream_response:
         if line.strip():
             print(json.loads(line))
     ```

Пример использования
-------------------------

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Функция изменяет значение переменной на ваш реальный ключ API
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

# Непотоковый запрос
completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)

# Потоковый запрос
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))