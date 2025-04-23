# src/endpoints/freegpt-webui-ru/g4f/Provider/Providers/Vercel.py

## Обзор

Этот модуль определяет провайдера Vercel для использования с `g4f`. Он включает в себя поддержку различных моделей, таких как `claude-instant-v1`, `claude-v1` и другие, предоставляемые через платформу Vercel. Модуль содержит классы и функции для взаимодействия с API Vercel, получения токенов и генерации текста на основе предоставленных моделей.

## Более подробная информация

Этот код позволяет использовать модели Vercel в проекте `g4f`. Он включает в себя получение токена для авторизации, определение параметров моделей и создание запросов для генерации текста. Код предназначен для асинхронной работы и может быть интегрирован в другие части проекта `hypotez` для предоставления доступа к моделям Vercel.

## Содержание

1.  **Constants**:
    -   `url`: URL для API Vercel.
    -   `supports_stream`: Поддерживает ли потоковую передачу данных.
    -   `needs_auth`: Требуется ли аутентификация.
    -   `models`: Словарь, содержащий соответствия между именами моделей и их идентификаторами.
    -   `vercel_models`: Словарь, содержащий параметры различных моделей Vercel.

2.  **Classes**:
    -   `Client`: Класс для взаимодействия с API Vercel.

## Переменные

-   `url` (str): URL-адрес API Vercel.
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
-   `needs_auth` (bool): Указывает, требуется ли аутентификация для провайдера.
-   `models` (Dict[str, str]): Словарь, сопоставляющий имена моделей с их идентификаторами.
-   `vercel_models` (Dict[str, Dict]): Словарь, содержащий параметры для различных моделей Vercel.

## Классы

### `Client`

Класс для взаимодействия с API Vercel.

**Описание**:
Этот класс предоставляет методы для получения токена аутентификации, получения параметров моделей по умолчанию и генерации текста с использованием API Vercel.

**Атрибуты**:

-   `session` (requests.Session): Сессия для выполнения HTTP-запросов.
-   `headers` (Dict[str, str]): Заголовки HTTP-запросов.

**Методы**:

-   `get_token()`: Получает токен аутентификации.
-   `get_default_params(model_id: str)`: Получает параметры по умолчанию для указанной модели.
-   `generate(model_id: str, prompt: str, params: dict = {})`: Генерирует текст на основе предоставленной модели и запроса.

### Методы класса

#### `__init__`

```python
def __init__(self):
    """Инициализирует экземпляр класса Client.

    Создает HTTP-сессию и устанавливает заголовки по умолчанию для запросов.
    """
```

#### `get_token`

```python
def get_token(self):
    """Получает токен аутентификации с API Vercel.

    Извлекает данные из `https://sdk.vercel.ai/openai.jpeg`, декодирует base64 и выполняет JavaScript-код для получения токена.

    Returns:
        str: Токен аутентификации.
    """
```

#### `get_default_params`

```python
def get_default_params(self, model_id: str) -> Dict:
    """Получает параметры по умолчанию для указанной модели.

    Args:
        model_id (str): Идентификатор модели.

    Returns:
        Dict: Словарь параметров по умолчанию.
    """
```

#### `generate`

```python
def generate(self, model_id: str, prompt: str, params: dict = {}) -> Generator[Dict, None, None]:
    """Генерирует текст на основе предоставленной модели и запроса.

    Args:
        model_id (str): Идентификатор модели.
        prompt (str): Текст запроса.
        params (dict): Дополнительные параметры.

    Yields:
        Generator[Dict, None, None]: Генератор словарей, содержащих сгенерированный текст.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса.
    """
```

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """Создает завершение для модели на основе предоставленных сообщений.

    Args:
        model (str): Идентификатор модели.
        messages (list): Список сообщений в формате [{"role": "user" or "assistant", "content": "message text"}].
        stream (bool): Указывает, следует ли использовать потоковую передачу.
        **kwargs: Дополнительные параметры.

    Yields:
        str: Сгенерированный текст.
    """
```

## Примеры

### Использование класса `Client`

```python
client = Client()
token = client.get_token()
print(f"Токен: {token}")

model_id = 'openai:gpt-3.5-turbo'
default_params = client.get_default_params(model_id)
print(f"Параметры по умолчанию для {model_id}: {default_params}")

prompt = "Напиши короткий рассказ о коте."
completion = client.generate(model_id, prompt)
for token in completion:
    print(token)
```

### Использование функции `_create_completion`

```python
model = 'openai:gpt-3.5-turbo'
messages = [
    {"role": "user", "content": "Напиши короткий рассказ о коте."},
]
stream = True

for token in _create_completion(model, messages, stream):
    print(token)
```

## Параметры

-   `model` (str): Идентификатор модели.
-   `messages` (list): Список сообщений.
-   `stream` (bool): Указывает, следует ли использовать потоковую передачу.

## Как работает функция `_create_completion`

1.  Формирует строку `conversation` из списка сообщений, объединяя `role` и `content` каждого сообщения.
2.  Создает экземпляр класса `Client`.
3.  Вызывает метод `generate` класса `Client` для генерации текста на основе `model` и `conversation`.
4.  Перебирает токены, возвращаемые генератором `completion`, и передает их в вызывающий код.

## Переменная `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: \' + \\\n    \'(%s)\' % \', \'.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

Эта строка кода создает строку, описывающую параметры, поддерживаемые функцией `_create_completion`. Она использует `os.path.basename(__file__)[:-3]` для получения имени текущего файла без расширения `.py` и `get_type_hints` для получения аннотаций типов параметров функции `_create_completion`. Затем она форматирует эту информацию в строку, которая указывает, какие параметры поддерживает провайдер Vercel.