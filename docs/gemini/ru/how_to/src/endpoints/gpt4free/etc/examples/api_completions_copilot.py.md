### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код отправляет запросы к локальному серверу для генерации текста с использованием модели Copilot. Он включает в себя отправку двух сообщений с разными запросами и обработку потоковых ответов от сервера.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
   - Импортируется `requests` для выполнения HTTP-запросов.
   - Импортируется `json` для работы с данными в формате JSON.
   - Импортируется `uuid` для генерации уникальных идентификаторов.

2. **Определение URL и ID разговора**:
   - Устанавливается `url` для отправки запросов (http://localhost:1337/v1/chat/completions).
   - Генерируется уникальный `conversation_id` с использованием `uuid.uuid4()`.

3. **Формирование тела запроса (первое сообщение)**:
   - Создается словарь `body` с параметрами запроса:
     - `model`: остается пустым.
     - `provider`: устанавливается как "Copilot".
     - `stream`: устанавливается как `True` для получения потоковых ответов.
     - `messages`: список, содержащий одно сообщение с ролью "user" и содержанием "Hello, i am Heiner. How are you?".
     - `conversation_id`: устанавливается как сгенерированный UUID.

4. **Отправка POST-запроса (первое сообщение)**:
   - Отправляется POST-запрос к указанному `url` с телом запроса `body` и параметром `stream=True`.
   - Обрабатывается статус ответа с помощью `response.raise_for_status()`.

5. **Обработка потокового ответа (первое сообщение)**:
   - Итерируется по строкам в потоковом ответе с помощью `response.iter_lines()`.
   - Проверяется, начинается ли строка с `b"data: "`.
   - Извлекаются данные JSON из строки, удаляя префикс `b"data: "`.
   - Обрабатываются ошибки JSON-декодирования.
   - Проверяется наличие поля "error" в JSON-данных и выводится сообщение об ошибке, если оно есть.
   - Извлекается содержимое из поля "content" в структуре `json_data["choices"][0]["delta"]`.
   - Выводится извлеченное содержимое без символа новой строки (`end=""`).

6. **Формирование тела запроса (второе сообщение)**:
   - Создается новый словарь `body` с аналогичными параметрами запроса, но с другим сообщением:
     - `messages`: список, содержащий одно сообщение с ролью "user" и содержанием "Tell me somethings about my name".
     - `conversation_id`: остается прежним.

7. **Отправка POST-запроса (второе сообщение)**:
   - Отправляется POST-запрос к указанному `url` с новым телом запроса `body` и параметром `stream=True`.
   - Обрабатывается статус ответа с помощью `response.raise_for_status()`.

8. **Обработка потокового ответа (второе сообщение)**:
   - Аналогично первому сообщению, итерируется по строкам в потоковом ответе.
   - Проверяется, начинается ли строка с `b"data: "`.
   - Извлекаются данные JSON из строки, удаляя префикс `b"data: "`.
   - Обрабатываются ошибки JSON-декодирования.
   - Проверяется наличие поля "error" в JSON-данных и выводится сообщение об ошибке, если оно есть.
   - Извлекается содержимое из поля "content" в структуре `json_data["choices"][0]["delta"]`.
   - Выводится извлеченное содержимое без символа новой строки (`end=""`).

Пример использования
-------------------------

```python
import requests
import json
import uuid

def get_copilot_response(message: str, conversation_id: str | None = None) -> None:
    """
    Отправляет сообщение Copilot и обрабатывает потоковый ответ.

    Args:
        message (str): Сообщение для отправки.
        conversation_id (str, optional): ID разговора. Defaults to None.
    """
    url = "http://localhost:1337/v1/chat/completions"
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())
    body = {
        "model": "",
        "provider": "Copilot",
        "stream": True,
        "messages": [
            {"role": "user", "content": message}
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

# Пример использования
get_copilot_response("Hello, i am Heiner. How are you?")
get_copilot_response("Tell me somethings about my name")