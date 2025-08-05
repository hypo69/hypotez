# Демонстрация текстовых завершений GPT4Free (синхронный режим)

## Обзор

Этот файл предоставляет простой пример использования библиотеки `g4f` для синхронного получения завершений текста от модели GPT-4o.

## Подробнее

Пример демонстрирует, как использовать `g4f.client.Client` для отправки запросов к модели GPT-4o и получения завершений текста.

## Классы

### `class Client`

**Описание**: Класс `Client` - это основной класс, который обеспечивает взаимодействие с GPT4Free API.

**Атрибуты**:

- `api_key` (str): API ключ для доступа к GPT4Free API.

**Методы**:

- `chat.completions.create()`: Метод для создания запросов к GPT4Free API.

## Функции

### `main`

**Назначение**:  Функция `main`  использует `Client` для создания запроса к GPT-4o с простым текстом.

**Параметры**:

- None

**Возвращает**:

- None

**Как работает**:

- Создает инстанс `Client` для взаимодействия с GPT4Free API.
- Вызывает метод `chat.completions.create()` для создания запроса к модели GPT-4o.
- В запросе задает роль системы ("helpful assistant") и текст запроса.
- Получает ответ от GPT-4o и выводит завершение текста.

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