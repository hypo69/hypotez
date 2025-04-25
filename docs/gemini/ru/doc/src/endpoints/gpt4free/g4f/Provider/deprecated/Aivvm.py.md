# Модуль Aivvm 
## Обзор

Модуль `Aivvm` предоставляет класс `Aivvm`, который реализует интерфейс `AbstractProvider` для взаимодействия с API сервиса `Aivvm` (https://chat.aivvm.com). Сервис позволяет получить доступ к моделям машинного обучения, таким как GPT-3.5 и GPT-4, для генерации текста.

## Классы

### `class Aivvm`

**Описание**: Класс `Aivvm` реализует интерфейс `AbstractProvider` для работы с API сервиса `Aivvm`. 

**Атрибуты**:

 - `url (str)`: Базовый URL API `Aivvm` (https://chat.aivvm.com). 
 - `supports_stream (bool)`: Указывает, поддерживает ли API потоковую передачу данных (True).
 - `working (bool)`: Флаг, указывающий на работоспособность API (по умолчанию False).
 - `supports_gpt_35_turbo (bool)`: Указывает, поддерживает ли API модель `gpt-3.5-turbo` (True).
 - `supports_gpt_4 (bool)`: Указывает, поддерживает ли API модель `gpt-4` (True).

**Методы**:

 - `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: 
   - Функция отправляет запрос к API `Aivvm` для генерации текста.
   - **Параметры**:
     - `model (str)`: Идентификатор модели, например, `gpt-3.5-turbo`.
     - `messages (Messages)`: Список сообщений, которые передаются в качестве контекста для модели.
     - `stream (bool)`: Флаг, указывающий на то, должна ли функция использовать потоковую передачу данных (True).
   - **Возвращает**: 
     - `CreateResult`: Объект `CreateResult`, который содержит результат генерации текста.

## Функции

### `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`

**Назначение**: Функция отправляет запрос к API `Aivvm` для генерации текста.

**Параметры**:

 - `model (str)`: Идентификатор модели, например, `gpt-3.5-turbo`.
 - `messages (Messages)`: Список сообщений, которые передаются в качестве контекста для модели.
 - `stream (bool)`: Флаг, указывающий на то, должна ли функция использовать потоковую передачу данных (True).

**Возвращает**:

 - `CreateResult`: Объект `CreateResult`, который содержит результат генерации текста.

**Как работает функция**:

1.  Функция проверяет, был ли передан идентификатор модели. Если нет, то по умолчанию устанавливается `gpt-3.5-turbo`.
2.  Проверяет, поддерживается ли переданная модель API. 
3.  Формирует JSON-данные для запроса к API. Включает идентификатор модели, сообщения, ключ API (ожидается, что ключ будет предоставлен в контексте), системное сообщение и температуру.
4.  Устанавливает заголовки для запроса, включая тип контента, языковые настройки и информацию о браузере.
5.  Отправляет POST-запрос к API `Aivvm` по адресу `https://chat.aivvm.com/api/chat`.
6.  Обрабатывает ответ API. 
7.  Если включена потоковая передача данных, то функция генерирует итератор, который поочередно возвращает декодированные части ответа API.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aivvm import Aivvm
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса Aivvm
provider = Aivvm()

# Создание списка сообщений для передачи в качестве контекста модели
messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"}
]

# Вызов функции `create_completion` для генерации текста
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)

# Печать результата (в данном случае текст будет выводиться по частям)
for chunk in response:
    print(chunk)

```

## Параметры класса

- `url (str)`: Базовый URL API `Aivvm` (https://chat.aivvm.com). 
- `supports_stream (bool)`: Указывает, поддерживает ли API потоковую передачу данных (True).
- `working (bool)`: Флаг, указывающий на работоспособность API (по умолчанию False).
- `supports_gpt_35_turbo (bool)`: Указывает, поддерживает ли API модель `gpt-3.5-turbo` (True).
- `supports_gpt_4 (bool)`: Указывает, поддерживает ли API модель `gpt-4` (True).

## Примеры

```python
# Импортируем необходимые модули
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aivvm import Aivvm
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создаем инстанс класса Aivvm
provider = Aivvm()

# Определяем список сообщений для передачи в качестве контекста модели
messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"}
]

# Вызываем функцию `create_completion` для генерации текста
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)

# Печать результата (в данном случае текст будет выводиться по частям)
for chunk in response:
    print(chunk)
```
```markdown