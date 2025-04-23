### Как использовать клиент xAI API
=========================================================================================

Описание
-------------------------
Этот документ описывает, как использовать Python клиент для взаимодействия с xAI API. Клиент упрощает процесс отправки запросов к API, включая как стандартные, так и потоковые запросы.

Шаги выполнения
-------------------------
1. **Установка**: Установите необходимые зависимости, используя `pip`.
2. **Инициализация**: Инициализируйте класс `XAI` с вашим API ключом.
3. **Chat Completion**: Используйте метод `chat_completion` для генерации ответов от моделей xAI.
4. **Streaming Chat Completion**: Используйте метод `stream_chat_completion` для получения потоковых ответов от моделей xAI.

Пример использования
-------------------------

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш фактический API ключ
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

# Non-streaming request
completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)

# Streaming request
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

1.  **Установка**:
    -   Код устанавливает библиотеку `requests`, которая необходима для выполнения HTTP-запросов к xAI API.
    -   Выполните команду `pip install requests` в вашем терминале.

2.  **Инициализация**:
    -   Код импортирует класс `XAI` из модуля `xai`.
    -   Создает экземпляр класса `XAI`, передавая ваш API ключ в качестве аргумента.
    -   Функция `XAI` инициализируется с вашим ключом API, который функция использует для аутентификации запросов.

3.  **Chat Completion**:
    -   Код создает список сообщений, где каждое сообщение представляет собой словарь с ключами `role` и `content`.
    -   `role` определяет роль отправителя сообщения (`system` или `user`).
    -   `content` содержит текст сообщения.
    -   Код вызывает метод `chat_completion` объекта `xai`, передавая список сообщений.
    -   Метод отправляет запрос к xAI API и возвращает ответ.
    -   Код отображает полученный ответ.
    -   Функция `chat_completion` выполняет запрос к API xAI, отправляет данные и возвращает результат запроса.

4.  **Streaming Chat Completion**:
    -   Код вызывает метод `stream_chat_completion` объекта `xai`, передавая список сообщений.
    -   Метод отправляет потоковый запрос к xAI API и возвращает генератор.
    -   Код итерируется по строкам в потоковом ответе.
    -   Если строка не пустая, код преобразует её в JSON объект и отображает.
    -   Функция `stream_chat_completion` отправляет запрос потоковой передачи в API xAI и обрабатывает каждый ответ в режиме реального времени.