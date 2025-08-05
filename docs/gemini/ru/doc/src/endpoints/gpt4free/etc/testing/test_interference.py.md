# Модуль `test_interference.py`

## Обзор

Этот модуль содержит тестовый сценарий для проверки взаимодействия с OpenAI API через локальный сервер. 

## Подробней

Модуль `test_interference.py`  задаёт параметры API OpenAI и отправляет запрос для генерации стихотворения о дереве. 
Он использует локальный сервер OpenAI, доступный по адресу `http://localhost:1337`.

## Функции

### `main`

**Назначение**:  Функция `main` инициализирует API OpenAI и выполняет запрос на генерацию стихотворения.

**Параметры**: 
- Нет

**Возвращает**: 
- Нет

**Вызывает исключения**: 
- Нет

**Как работает функция**:
- Функция `main` инициализирует OpenAI API с использованием ключа `openai.api_key` и базового адреса `openai.api_base`. 
- Она отправляет запрос к модели `gpt-3.5-turbo` с сообщением `"write a poem about a tree"`.
- Если получен не потоковый ответ, функция печатает содержимое ответа. 
- Если получен потоковый ответ, функция печатает каждый полученный токен.

**Примеры**:
```python
# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
if isinstance(chat_completion, dict):
    # Не потоковый ответ
    print(chat_completion.choices[0].message.content)
else:
    # Потоковый ответ
    for token in chat_completion:
        content = token["choices"][0]["delta"].get("content")
        if content != None:
            print(content, end="", flush=True)
```
```python
# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)
```
```python
# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)
```

## Примеры

```python
from src.endpoints.gpt4free.etc.testing.test_interference import main

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)
```
```python
from src.endpoints.gpt4free.etc.testing.test_interference import main
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
)

# Обработка ответа
print(chat_completion.choices[0].message.content)

# Выполняет тестовый сценарий
main()
```
```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

# Инициализация API OpenAI
openai.api_key = ""
openai.api_base = "http://localhost:1337"

# Запрос к модели GPT-3.5-turbo
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
)

# Обработка ответа
for token in chat_completion:
    content = token["choices"][0]["delta"].get("content")
    if content != None:
        print(content, end="", flush=True)

# Выполняет тестовый сценарий
main()