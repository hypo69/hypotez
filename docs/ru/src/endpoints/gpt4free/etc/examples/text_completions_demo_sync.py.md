# Документация для примера text_completions_demo_sync.py

## Обзор

Этот файл демонстрирует синхронный вызов API для получения текстовых завершений с использованием библиотеки `g4f`. Он создает клиент, отправляет запрос на завершение текста и выводит полученный результат.

## Подробнее

Этот код предназначен для демонстрации простого способа взаимодействия с моделью GPT-4o через библиотеку `g4f`. Он показывает, как создать клиент, сформировать запрос с системным и пользовательским сообщениями, и получить ответ от модели.

## Переменные

- `client`: Объект класса `Client` из модуля `g4f.client`, используемый для отправки запросов к API.
- `response`: Объект, содержащий ответ от API с завершением текста.

## Код

```python
from g4f.client import Client

client = Client()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "how does a court case get to the Supreme Court?"}
    ],
)

print(response.choices[0].message.content)
```

## Функции

Здесь нет явно определенных функций, но используется метод `create` объекта `client.chat.completions`.

### `client.chat.completions.create`

**Назначение**: Отправляет запрос на завершение текста к API.

**Параметры**:
- `model` (str): Идентификатор используемой модели, в данном случае "gpt-4o".
- `messages` (list): Список сообщений, содержащих роль и контент для модели.

**Возвращает**:
- Объект, содержащий ответ от API.

**Как работает функция**:
- Создает запрос к API с указанной моделью и сообщениями.
- Получает ответ от API с завершением текста.

**Примеры**:

```python
from g4f.client import Client

client = Client()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "how does a court case get to the Supreme Court?"}
    ],
)

print(response.choices[0].message.content)
```

В этом примере создается запрос к модели "gpt-4o" с системным сообщением, указывающим, что модель должна быть полезным ассистентом, и пользовательским сообщением, спрашивающим, как судебное дело попадает в Верховный суд.