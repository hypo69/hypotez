# Документация для `text_completions_demo_sync.py`

## Обзор

Этот файл демонстрирует пример синхронного запроса к модели GPT-4o с использованием библиотеки `g4f`. Он показывает, как создать клиента, отправить запрос с системным и пользовательским сообщением, и напечатать полученный ответ.

## Подробнее

Этот код используется для демонстрации базового функционала библиотеки `g4f` для отправки запросов к моделям GPT. Он показывает, как создать простой диалог с моделью и получить ответ.

## Функции

### `Client`

```python
from g4f.client import Client

client = Client()
```

**Описание**: Создает экземпляр класса `Client` из библиотеки `g4f`.

### `chat.completions.create`

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "how does a court case get to the Supreme Court?"}
    ],
)
```

**Назначение**: Отправляет запрос к модели GPT-4o с заданными сообщениями.

**Параметры**:
- `model` (str): Имя модели, используемой для генерации ответа. В данном случае "gpt-4o".
- `messages` (List[dict]): Список сообщений, формирующих контекст диалога. Каждое сообщение содержит роль (`role`) и содержание (`content`).

**Возвращает**:
- `response` (объект): Объект ответа, содержащий сгенерированный моделью текст.

**Как работает функция**:
- Функция создает запрос к указанной модели (`gpt-4o`) с заданным списком сообщений.
- Сообщения содержат системное сообщение, определяющее роль модели, и пользовательское сообщение с вопросом.
- Функция отправляет запрос и получает ответ от модели.

### `print`

```python
print(response.choices[0].message.content)
```

**Назначение**: Выводит содержание ответа модели в консоль.

**Параметры**:
- `response.choices[0].message.content` (str): Текст ответа, сгенерированный моделью.

**Как работает функция**:
- Функция извлекает текст ответа из объекта `response`.
- Выводит текст в консоль.

## Примеры

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