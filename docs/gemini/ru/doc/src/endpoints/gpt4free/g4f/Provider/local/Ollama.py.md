# Модуль Ollama для GPT4Free

## Обзор

Этот модуль предоставляет реализацию класса `Ollama` для работы с API Ollama в контексте проекта GPT4Free. 
`Ollama` наследует от класса `OpenaiAPI`, который реализует общий функционал для взаимодействия с различными API, 
обеспечивая единообразный подход к работе с моделями.

## Класс `Ollama`

### Описание

`Ollama` реализует интерфейс для взаимодействия с API Ollama. Он предоставляет методы для получения доступных 
моделей, создания асинхронных генераторов для выполнения запросов к API.

**Наследует**: `OpenaiAPI`

**Атрибуты**:

- `label` (str): Метка, идентифицирующая провайдера (Ollama).
- `url` (str): Базовый URL API.
- `login_url` (None):  Не используется, так как Ollama не требует авторизации.
- `needs_auth` (bool): Указывает, требуется ли авторизация для взаимодействия с API.
- `working` (bool): Указывает, работает ли провайдер.

**Методы**:

- `get_models(api_base: str = None, **kwargs)`: Получение доступных моделей. 
- `create_async_generator(model: str, messages: Messages, api_base: str = None, **kwargs) -> AsyncResult`: 
Создание асинхронного генератора для выполнения запросов к API Ollama.

### Методы класса `Ollama`

#### `get_models(api_base: str = None, **kwargs)`

**Назначение**: Метод для получения списка доступных моделей Ollama.

**Параметры**:

- `api_base` (str, optional): Базовый URL API. По умолчанию `None`, в этом случае используется `OLLAMA_HOST` и `OLLAMA_PORT` 
из переменных окружения.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `list[str]`: Список доступных моделей.

**Пример**:

```python
models = Ollama.get_models()
print(models)
```

**Как работает функция**:

- Проверяет, существует ли список доступных моделей в классе `Ollama`.
- Если список не существует, метод выполняет HTTP-запрос к API Ollama для получения списка моделей. 
- Извлекает список имен моделей из ответа API.
- Заполняет свойство `models` класса `Ollama` списком имен моделей.
- Возвращает список доступных моделей.

#### `create_async_generator(model: str, messages: Messages, api_base: str = None, **kwargs) -> AsyncResult`:

**Назначение**: Метод для создания асинхронного генератора, который используется для выполнения запросов к API Ollama.

**Параметры**:

- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений, используемых для контекста.
- `api_base` (str, optional): Базовый URL API. По умолчанию `None`, в этом случае используется `OLLAMA_HOST` и `OLLAMA_PORT` 
из переменных окружения.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который может быть использован для получения ответа от API Ollama.

**Пример**:

```python
async_generator = Ollama.create_async_generator(model="your_model", messages=[
    {"role": "user", "content": "Your message to Ollama"}
])
async for response in async_generator:
    print(response)
```

**Как работает функция**:

- Метод наследует функциональность создания асинхронного генератора от базового класса `OpenaiAPI`.
- Метод использует переданные параметры `model`, `messages` и `api_base` для создания асинхронного генератора.
- Возвращает объект `AsyncResult`, который представляет собой асинхронный генератор.

## Использование модуля

Пример использования модуля `Ollama` для получения списка доступных моделей:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.local.Ollama import Ollama

models = Ollama.get_models()
print(models)
```

Пример использования модуля `Ollama` для получения ответа от API Ollama:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.local.Ollama import Ollama
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async_generator = Ollama.create_async_generator(model="your_model", messages=[
    {"role": "user", "content": "Your message to Ollama"}
])
async for response in async_generator:
    print(response)
```