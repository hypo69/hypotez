# Документация модуля `Ollama.py`

## Обзор

Модуль `Ollama.py` предоставляет класс `Ollama`, который является адаптером для работы с локально развернутыми моделями Ollama. Он наследуется от класса `OpenaiAPI` и предназначен для интеграции с API Ollama, позволяя использовать модели Ollama как один из провайдеров в системе.

## Подробнее

Модуль определяет способ получения списка моделей, доступных через Ollama, а также создает асинхронный генератор для взаимодействия с API Ollama. Он использует переменные окружения `OLLAMA_HOST` и `OLLAMA_PORT` для определения адреса и порта, на котором запущен сервер Ollama.

## Классы

### `Ollama(OpenaiAPI)`

**Описание**: Класс `Ollama` предоставляет интерфейс для работы с API Ollama.

**Наследует**: `OpenaiAPI`

**Атрибуты**:
- `label` (str): Метка провайдера, "Ollama".
- `url` (str): URL веб-сайта Ollama, "https://ollama.com".
- `login_url` (None): URL для входа в систему, `None`, так как не требуется.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация, `False`.
- `working` (bool): Флаг, указывающий, работает ли провайдер, `True`.
- `models` (list): Список доступных моделей, получаемый из API Ollama.
- `default_model` (str): Модель по умолчанию, первая из списка доступных моделей.

**Методы**:
- `get_models(cls, api_base: str = None, **kwargs)`: Получает список доступных моделей из API Ollama.
- `create_async_generator(cls, model: str, messages: Messages, api_base: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API Ollama.

## Методы класса

### `get_models(cls, api_base: str = None, **kwargs)`

**Назначение**: Получает список доступных моделей из API Ollama. Если список моделей еще не был получен, он запрашивается с сервера Ollama и сохраняется в атрибуте `cls.models`.

**Параметры**:
- `cls` (type[Ollama]): Ссылка на класс `Ollama`.
- `api_base` (str, optional): Базовый URL API Ollama. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[str]`: Список доступных моделей.

**Как работает функция**:
1. Проверяет, был ли уже получен список моделей (`cls.models`).
2. Если список моделей пуст, определяет URL для запроса списка моделей. Если `api_base` не указан, используется значение из переменных окружения `OLLAMA_HOST` и `OLLAMA_PORT`. В противном случае `api_base` преобразуется в URL для получения списка моделей.
3. Выполняет GET-запрос к API Ollama для получения списка моделей.
4. Извлекает имена моделей из JSON-ответа и сохраняет их в `cls.models`.
5. Устанавливает первую модель из списка в качестве модели по умолчанию (`cls.default_model`).
6. Возвращает список моделей.

**Примеры**:

```python
models = Ollama.get_models()
print(models)
# ['llama2', 'codellama', ...]
```

### `create_async_generator(cls, model: str, messages: Messages, api_base: str = None, **kwargs) -> AsyncResult`

**Назначение**: Создает асинхронный генератор для взаимодействия с API Ollama.

**Параметры**:
- `cls` (type[Ollama]): Ссылка на класс `Ollama`.
- `model` (str): Имя модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений для отправки в API.
- `api_base` (str, optional): Базовый URL API Ollama. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от API Ollama.

**Как работает функция**:
1. Определяет базовый URL API Ollama. Если `api_base` не указан, используется значение из переменных окружения `OLLAMA_HOST` и `OLLAMA_PORT`.
2. Вызывает метод `create_async_generator` родительского класса `OpenaiAPI` для создания асинхронного генератора с указанными параметрами.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, Ollama!"}]
generator = Ollama.create_async_generator(model="llama2", messages=messages)