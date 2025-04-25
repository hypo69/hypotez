# Модуль VoiGpt

## Обзор

Этот модуль реализует провайдер для VoiGpt.com.

##  Как использовать провайдер

Чтобы использовать этот провайдер, необходимо получить токен csrf/cookie с веб-сайта voigpt.com. 

##  Классы

### `class VoiGpt(AbstractProvider)`

**Описание**:  Класс, который реализует провайдер для VoiGpt.com.

**Наследует**: :class:`AbstractProvider`

**Атрибуты**:

- `url (str)`: URL-адрес API VoiGpt.
- `working (bool)`:  Признак работоспособности провайдера.
- `supports_gpt_35_turbo (bool)`: Признак поддержки модели gpt-3.5-turbo.
- `supports_message_history (bool)`: Признак поддержки истории сообщений.
- `supports_stream (bool)`: Признак поддержки потоковой передачи ответа.
- `_access_token (str)`: Токен доступа для аутентификации.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, access_token: str = None, **kwargs) -> CreateResult:`
    - **Назначение**: Создает запрос к API VoiGpt для генерации ответа.
    - **Параметры**:
        - `model (str)`:  Название модели, которую необходимо использовать.
        - `messages (Messages)`: Сообщения для отправки в API.
        - `stream (bool)`: Признак потоковой передачи ответа.
        - `proxy (str, optional)`:  Прокси-сервер, который нужно использовать. По умолчанию `None`.
        - `access_token (str, optional)`: Токен доступа для аутентификации. По умолчанию `None`.
        - `**kwargs`: Дополнительные аргументы.
    - **Возвращает**: `CreateResult`:  Объект, содержащий результат запроса.
    - **Как работает функция**: 
        - Проверяет, указаны ли в аргументах модель и токен доступа.
        - Если токен доступа не указан, извлекает его из cookies веб-сайта VoiGpt. 
        - Формирует заголовок запроса с токеном доступа и другими необходимыми параметрами. 
        - Создает тело запроса с сообщениями.
        - Отправляет POST-запрос к API VoiGpt.
        - Извлекает ответ API и преобразует его в JSON.
        - Возвращает результат в виде объекта `CreateResult`.


## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt с токеном доступа
provider = VoiGpt(access_token="your_access_token")

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt с токеном доступа
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt 
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt 
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем экземпляр VoiGpt
provider = VoiGpt()

# Сообщения для отправки
messages = Messages(
    [
        {"role": "user", "content": "Привет, как дела?"},
    ]
)

# Запускаем создание ответа
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод результата
print(response)