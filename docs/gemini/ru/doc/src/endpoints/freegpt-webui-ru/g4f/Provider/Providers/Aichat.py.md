# Провайдер Aichat

## Обзор

Этот модуль предоставляет реализацию провайдера `Aichat` для генерации ответов с помощью модели GPT-3.5-turbo. 

## Подробности

Проект `hypotez` использует этот файл для получения ответов от модели `gpt-3.5-turbo`, предоставляемой сервисом `chat-gpt.org`.

## Функции

### `_create_completion`

**Назначение**: Эта функция отправляет запрос к API `chat-gpt.org` для генерации ответа от модели `gpt-3.5-turbo`. 

**Параметры**:

- `model` (str): Имя модели (например, `gpt-3.5-turbo`).
- `messages` (list): Список сообщений в формате `[{'role': 'user', 'content': 'Текст сообщения'}, ...]`.
- `stream` (bool): Флаг, указывающий на использование потоковой передачи ответов.
- `**kwargs`: Дополнительные параметры запроса.

**Возвращает**:
- `Generator[str, None, None]`: Генератор строк с частями ответа от модели.

**Как работает функция**:

1. Создаёт строку `base`, объединяя текст всех сообщений в `messages`.
2. Добавляет префикс "assistant:" к строке `base`.
3. Формирует JSON-запрос для отправки на API, используя `base` и дополнительные параметры.
4. Отправляет POST-запрос к API `chat-gpt.org/api/text` с помощью `requests.post`.
5. Возвращает генератор строк, содержащий части ответа модели.

**Примеры**:

```python
# Пример вызова _create_completion
from ...typing import sha256, Dict, get_type_hints
from src.logger import logger

messages = [
    {'role': 'user', 'content': 'Привет, как дела?'},
    {'role': 'assistant', 'content': 'Хорошо, а у тебя?'},
]
response = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)

# Обработка ответа
for part in response:
    logger.info(f'Часть ответа: {part}')
```

## Параметры

- `url` (str): URL-адрес сервиса `chat-gpt.org`.
- `model` (list): Список поддерживаемых моделей.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации для доступа к модели.

## Примеры

```python
from ...typing import sha256, Dict, get_type_hints
from src.logger import logger

# Получение имени файла и создание объекта Aichat
from .. import Providers
provider = Providers.Aichat()
file_name = os.path.basename(__file__)[:-3]

# Вывод информации о провайдере Aichat
logger.info(f'Используемый провайдер: {file_name}')
logger.info(f'Функция _create_completion: {get_type_hints(provider._create_completion)}')
```