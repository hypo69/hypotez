# Модуль для взаимодействия с API Copilot через completions

## Обзор

Этот модуль демонстрирует пример взаимодействия с API Copilot через endpoint completions. Он отправляет запросы к локальному серверу и обрабатывает потоковые ответы для получения информации от модели Copilot.

## Подробней

Модуль предназначен для отправки текстовых запросов к API Copilot и получения ответов в реальном времени. Он использует библиотеку `requests` для отправки POST-запросов и обрабатывает потоковые ответы, декодируя JSON-данные и извлекая текстовое содержимое. `conversation_id` используется для отслеживания диалога.

## Функции

### Отправка запроса и обработка ответа

Основная логика модуля заключается в отправке POST-запросов к endpoint `/v1/chat/completions` и обработке потоковых ответов. Каждый ответ проверяется на наличие ошибок, и извлекается текстовое содержимое.

**Как работает функция:**

1.  Формируется тело запроса (`body`) с указанием модели, провайдера (`Copilot`), включенным режимом потоковой передачи (`stream`), списком сообщений (`messages`) и идентификатором разговора (`conversation_id`).
2.  Отправляется POST-запрос к указанному URL (`url`) с телом запроса в формате JSON и включенным режимом потоковой передачи.
3.  Полученный ответ обрабатывается построчно. Каждая строка, начинающаяся с `b"data: "`, считается JSON-данными.
4.  JSON-данные декодируются, и проверяется наличие ошибок. Если ошибка обнаружена, она выводится в консоль, и обработка прекращается.
5.  Извлекается текстовое содержимое из поля `content`, которое находится в структуре `choices[0].delta`.
6.  Извлеченное содержимое выводится в консоль без добавления новой строки (`end=""`), чтобы обеспечить потоковый вывод.
7.  В случае ошибки декодирования JSON, она игнорируется.

**Примеры:**

```python
import requests
import json
import uuid

url = "http://localhost:1337/v1/chat/completions"
conversation_id = str(uuid.uuid4())
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
## Переменные
- `url` (str): URL-адрес endpoint completions.
- `conversation_id` (str): Уникальный идентификатор разговора, генерируемый с помощью `uuid.uuid4()`.
- `body` (dict): Тело запроса, содержащее модель, провайдера, режим потоковой передачи, сообщения и идентификатор разговора.
- `response` (requests.Response): Объект ответа, полученный от сервера.
- `line` (bytes): Строка данных, полученная из потокового ответа.
- `json_data` (dict): Декодированные JSON-данные из строки ответа.
- `content` (str): Текстовое содержимое, извлеченное из JSON-данных.