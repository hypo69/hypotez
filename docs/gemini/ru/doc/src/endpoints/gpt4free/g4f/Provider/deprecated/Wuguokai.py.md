# Модуль Wuguokai

## Обзор

Модуль `Wuguokai` предоставляет реализацию класса `Wuguokai`, который является провайдером для взаимодействия с API-сервисом `wuguokai.xyz`.

## Классы

### `class Wuguokai`

**Описание**: Класс `Wuguokai` реализует провайдера для взаимодействия с API-сервисом `wuguokai.xyz`. 

**Атрибуты**:
- `url (str)`: Базовый URL API-сервиса `wuguokai.xyz`.
- `supports_gpt_35_turbo (bool)`: Указывает, поддерживает ли данный провайдер модель GPT-3.5 Turbo.
- `working (bool)`: Флаг, показывающий, работает ли провайдер.

**Методы**:
- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

#### `create_completion`

**Назначение**: Функция отправляет запрос на API-сервис `wuguokai.xyz` для получения завершения текста.

**Параметры**:
- `model (str)`: Идентификатор модели (например, `gpt-3.5-turbo`).
- `messages (list[dict[str, str]])`: Список сообщений, которые используются как контекст для генерации.
- `stream (bool)`: Флаг, указывающий, нужно ли получать ответ в потоковом режиме.
- `**kwargs (Any)`: Дополнительные аргументы, которые могут быть переданы в запрос.

**Возвращает**:
- `CreateResult`: Объект `CreateResult` с информацией об успешном или неудачном запросе.

**Как работает**:
- Формируется JSON-запрос с необходимыми данными (prompt, options, userId, usingContext).
- Отправляется POST-запрос на URL `https://ai-api20.wuguokai.xyz/api/chat-process`.
- Обрабатывается ответ от сервера.
- В случае успешного ответа возвращается генератор, который последовательно выдает части текста.
- В случае ошибки, поднимается исключение `Exception`.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Wuguokai import Wuguokai
from hypotez.src.endpoints.gpt4free.g4f.typing import CreateResult

provider = Wuguokai()

# Пример вызова create_completion
messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Хорошо, а у тебя?"},
]
response: CreateResult = provider.create_completion(
    model="gpt-3.5-turbo",
    messages=messages,
    stream=False,
)
print(response)
```

## Параметры класса

- `url (str)`: Базовый URL API-сервиса `wuguokai.xyz`.
- `supports_gpt_35_turbo (bool)`: Указывает, поддерживает ли данный провайдер модель GPT-3.5 Turbo.
- `working (bool)`: Флаг, показывающий, работает ли провайдер.


**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Wuguokai import Wuguokai

provider = Wuguokai()

print(provider.url)
print(provider.supports_gpt_35_turbo)
print(provider.working)
```