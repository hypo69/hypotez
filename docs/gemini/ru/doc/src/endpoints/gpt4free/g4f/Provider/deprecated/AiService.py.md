# Модуль `AiService` 

## Обзор

Модуль `AiService` предоставляет реализацию класса `AiService` - провайдера AI-услуг, который использует API-интерфейс `aiservice.vercel.app` для генерации ответов.  Данный модуль является устаревшим и не рекомендуется к использованию. 

## Подробней

Модуль реализует `AiService` - класс, который наследуется от базового провайдера `AbstractProvider`. Он использует API-интерфейс `aiservice.vercel.app` для генерации ответов от AI-модели. 

## Классы

### `class AiService`

**Описание**:  Класс `AiService` - это провайдер AI-услуг, который использует API-интерфейс `aiservice.vercel.app` для генерации ответов.

**Наследует**: `AbstractProvider`

**Атрибуты**:

- `url`: URL-адрес API-интерфейса `aiservice.vercel.app`.
- `working`:  Флаг, указывающий на работоспособность провайдера.
- `supports_gpt_35_turbo`: Флаг, указывающий на поддержку модели GPT-3.5 Turbo.

**Методы**:

#### `create_completion()`

**Назначение**:  Генерирует ответ от AI-модели с использованием API-интерфейса `aiservice.vercel.app`.

**Параметры**:

- `model`:  Название модели AI.
- `messages`:  Список сообщений для модели AI.
- `stream`: Флаг, указывающий на то, нужно ли использовать потоковый режим.
- `**kwargs`:  Дополнительные параметры.

**Возвращает**:  Генератор JSON-данных с ответом от AI-модели.

**Вызывает исключения**:

- `requests.exceptions.HTTPError`:  Если API-запрос завершился с ошибкой.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.AiService import AiService
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {'role': 'user', 'content': 'Привет! Как дела?'},
]

ai_service = AiService()
for response in ai_service.create_completion(model='gpt-3.5-turbo', messages=messages, stream=False):
    print(response)
```

**Как работает функция**:

- Формирует строку с историей сообщений, используя  `messages`.
- Собирает заголовки HTTP-запроса.
- Отправляет POST-запрос на `https://aiservice.vercel.app/api/chat/answer`.
- Обрабатывает ответ от API-интерфейса и возвращает JSON-данные.
- Возвращает генератор, позволяющий получать данные ответа по частям.

**Внутренние функции**:  Нет.