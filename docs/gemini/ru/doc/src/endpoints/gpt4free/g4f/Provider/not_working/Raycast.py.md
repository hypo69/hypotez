# Модуль `Raycast`

## Обзор

Этот модуль предоставляет реализацию класса `Raycast`, который является провайдером для генерации текста с использованием модели GPT-4 от Raycast. Он реализует интерфейс `AbstractProvider` и обеспечивает функциональность для отправки запросов к API Raycast.

## Классы

### `class Raycast`

**Описание**: Класс `Raycast` является провайдером для генерации текста с использованием модели GPT-4 от Raycast.

**Наследует**: `AbstractProvider`

**Атрибуты**:

- `url (str)`: Базовый URL API Raycast.
- `supports_stream (bool)`: Флаг, указывающий, поддерживает ли провайдер потоковую передачу.
- `needs_auth (bool)`: Флаг, указывающий, требуется ли авторизация для использования провайдера.
- `working (bool)`: Флаг, указывающий, работает ли провайдер.
- `models (list[str])`: Список поддерживаемых моделей.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, **kwargs) -> CreateResult`

#### `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, **kwargs) -> CreateResult`

**Назначение**: Функция отправляет запрос к API Raycast для генерации текста.

**Параметры**:

- `model (str)`: Имя модели GPT, используемой для генерации текста.
- `messages (Messages)`: Список сообщений, используемых в качестве контекста для генерации текста.
- `stream (bool)`: Флаг, указывающий, требуется ли потоковая передача.
- `proxy (str, optional)`: Прокси-сервер для использования при отправке запроса.
- `**kwargs`: Дополнительные параметры, включая токен авторизации (`auth`).

**Возвращает**:

- `CreateResult`: Результат создания текста.

**Вызывает исключения**:

- `ValueError`: Если не предоставлен токен авторизации (`auth`).

**Как работает функция**:

1. Проверяет, предоставлен ли токен авторизации (`auth`).
2. Формирует заголовки запроса, включая токен авторизации, тип контента и агент пользователя.
3. Парсит список сообщений для соответствия формату API Raycast.
4. Создает данные запроса, включая модель, сообщения, системные инструкции, язык и температуру.
5. Отправляет POST-запрос к API Raycast с использованием библиотеки `requests`.
6. Если параметр `stream` установлен в `True`, функция итерирует по строкам ответа и выводит текст по частям. 
7. Если параметр `stream` установлен в `False`, функция возвращает весь сгенерированный текст.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Raycast import Raycast
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание объекта провайдера Raycast с токеном авторизации
raycast = Raycast(auth="YOUR_AUTH_TOKEN")

# Создание запроса с использованием модели GPT-4
messages = Messages(
    [
        {"role": "user", "content": "Привет! Как дела?"},
        {"role": "assistant", "content": "Хорошо, а у тебя?"},
    ]
)
result = raycast.create_completion(model="gpt-4", messages=messages, stream=False)

# Вывод сгенерированного текста
print(result.content)
```