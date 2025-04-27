## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой клиентскую библиотеку Python для взаимодействия с API xAI. Он упрощает процесс отправки запросов к API, поддерживая как стандартные, так и потоковые запросы.

Шаги выполнения
-------------------------
1. **Инициализация:** Создайте экземпляр класса `XAI` с вашим ключом API xAI:
   ```python
   from xai import XAI

   api_key = "your_api_key_here"  # Замените на ваш реальный ключ API
   xai = XAI(api_key)
   ```

2. **Завершение чата:** Используйте метод `chat_completion` для получения ответа от модели xAI:
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

3. **Потоковая передача завершения чата:** Используйте метод `stream_chat_completion` для получения ответа от модели xAI в виде потока:
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

api_key = "your_api_key_here"  # Замените на ваш реальный ключ API
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
```