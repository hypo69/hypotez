## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот фрагмент кода представляет собой пример взаимодействия с API  gpt4free, используя библиотеку `requests` и отправляя POST запросы с JSON-данными, чтобы получить ответы от модели  Copilot.

Шаги выполнения
-------------------------
1. Импортирует необходимые библиотеки: `requests` для работы с HTTP запросами, `json` для обработки JSON данных, и `uuid` для генерации уникальных идентификаторов.
2. Задаёт URL для отправки запросов - "http://localhost:1337/v1/chat/completions".
3. Создаёт уникальный идентификатор  `conversation_id` для каждой сессии общения.
4.  Создаёт словарь `body` с JSON-данными, которые отправляются в API.  Он включает:
    -  `model`: указывает модель, которая должна быть использована (в данном случае Copilot),
    - `provider`: указывает, что используется Copilot,
    - `stream`:  определяет, должен ли ответ от сервера передаваться потоком (True - да, False - нет),
    - `messages`:  содержит список сообщений, которые отправляются в API. В данном случае это одно сообщение от пользователя.
    - `conversation_id`: уникальный идентификатор сессии.
5. Отправляет POST запрос на указанный URL, используя библиотеку `requests.post` и передаёт JSON-данные в `body`. 
6. Проверяет статус ответа, вызывая `response.raise_for_status()`.
7.  Обрабатывает ответ, получая данные по частям:
    -  Использует `response.iter_lines()` для итерации по каждой строке ответа,
    -  Проверяет, начинается ли строка с "data: ", 
    -  Если да, то преобразует JSON данные из строки в объект  и проверяет наличие ошибок. 
    -  Выводит содержимое ответа на консоль.
8.  Повторяет шаги 4-7 для отправки другого сообщения.

Пример использования
-------------------------

```python
import requests
import json
import uuid

url = "http://localhost:1337/v1/chat/completions"
conversation_id = str(uuid.uuid4())

# Отправляем первое сообщение
body = {
    "model": "",
    "provider": "Copilot",
    "stream": True,
    "messages": [
        {"role": "user", "content": "Hello, i am Heiner. How are you?"}
    ],
    "conversation_id": conversation_id
}
response = requests.post(url, json=body, stream=True)
response.raise_for_status()
for line in response.iter_lines():
    # Обработка ответа, как описано выше
    if line.startswith(b"data: "):
        try:
            json_data = json.loads(line[6:])
            if json_data.get("error"):
                print(json_data)
                break
            content = json_data.get("choices", [{"delta": {}}])[0]["delta"].get("content", "")
            if content:
                print(content, end="")
        except json.JSONDecodeError:
            pass
print()
print()
print()

# Отправляем второе сообщение
body = {
    "model": "",
    "provider": "Copilot",
    "stream": True,
    "messages": [
        {"role": "user", "content": "Tell me somethings about my name"}
    ],
    "conversation_id": conversation_id
}
response = requests.post(url, json=body, stream=True)
response.raise_for_status()
for line in response.iter_lines():
    # Обработка ответа, как описано выше
    if line.startswith(b"data: "):
        try:
            json_data = json.loads(line[6:])
            if json_data.get("error"):
                print(json_data)
                break
            content = json_data.get("choices", [{"delta": {}}])[0]["delta"].get("content", "")
            if content:
                print(content, end="")
        except json.JSONDecodeError:
            pass

```