# Модуль для взаимодействия с Copilot API для completions

## Обзор

Этот модуль содержит пример кода для взаимодействия с API Copilot для получения completions. Он демонстрирует отправку запросов к API и обработку потоковых ответов.

## Подробнее

Модуль отправляет POST-запросы к локальному серверу по адресу `http://localhost:1337/v1/chat/completions` для получения ответов от модели Copilot. Код использует библиотеку `requests` для отправки запросов и обрабатывает потоковые ответы, выводя полученный контент в консоль. conversation_id используется для поддержания контекста диалога.

## Методы

### Отправка запроса на completions

Примеры отправки запроса к API Copilot и обработки потоковых ответов

**Как работает функция**:

1.  Определяется URL для отправки запросов completions: `http://localhost:1337/v1/chat/completions`.
2.  Генерируется уникальный `conversation_id` с использованием `uuid.uuid4()`. Этот ID используется для отслеживания и поддержания контекста разговора между клиентом и сервером.
3.  Формируется тело запроса `body`, которое содержит следующие параметры:
    *   `model`: Пустая строка, указывающая, что используется модель по умолчанию (или модель, определенная на стороне сервера).
    *   `provider`: `"Copilot"`, указывающий, что запросы направляются к провайдеру Copilot.
    *   `stream`: `True`, указывающий, что ожидается потоковый ответ от сервера.
    *   `messages`: Список сообщений, где каждое сообщение содержит роль (`"user"`) и контент сообщения.
    *   `conversation_id`: Уникальный идентификатор разговора, сгенерированный ранее.
4.  Отправляется POST-запрос к указанному URL с телом запроса в формате JSON и включенным потоковым режимом (`stream=True`).
5.  Проверяется статус ответа с помощью `response.raise_for_status()`, чтобы убедиться, что запрос был успешным (код 200 OK). Если возникает HTTPError, вызывается исключение.
6.  Обрабатывается потоковый ответ построчно:
    *   Каждая строка проверяется на наличие префикса `b"data: "`.
    *   Если строка начинается с `b"data: "`, извлекается JSON-данные из строки, удаляя префикс.
    *   JSON-данные десериализуются с использованием `json.loads()`.
    *   Проверяется наличие ключа `"error"` в JSON-данных. Если он есть, сообщение об ошибке выводится в консоль, и цикл прерывается.
    *   Извлекается контент сообщения из JSON-данных, используя цепочку `json_data.get("choices", [{"delta": {}}])[0]["delta"].get("content", "")`.
    *   Если контент не пустой, он выводится в консоль без добавления новой строки в конце (`end=""`), чтобы обеспечить потоковый вывод.
    *   Если происходит ошибка при десериализации JSON-данных (`json.JSONDecodeError`), она игнорируется.

**Примеры**:

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
    if line.startswith(b"data: "):\n        try:
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
        {"role": "user", "content": "Tell me somethings about my name"}
    ],
    "conversation_id": conversation_id
}
response = requests.post(url, json=body, stream=True)
response.raise_for_status()
for line in response.iter_lines():
    if line.startswith(b"data: "):\n        try:
            json_data = json.loads(line[6:])
            if json_data.get("error"):
                print(json_data)
                break
            content = json_data.get("choices", [{"delta": {}}])[0]["delta"].get("content", "")
            if content:
                print(content, end="")
        except json.JSONDecodeError:
            pass