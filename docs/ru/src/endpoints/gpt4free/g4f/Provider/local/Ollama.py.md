# Модуль для работы с Ollama

## Обзор

Модуль `Ollama.py` предоставляет класс `Ollama`, который является подклассом `OpenaiAPI`. Он предназначен для взаимодействия с локально запущенными моделями Ollama. Модуль позволяет получать список доступных моделей и создавать асинхронный генератор для взаимодействия с выбранной моделью.

## Подробнее

Этот модуль обеспечивает интеграцию с Ollama, позволяя использовать локальные модели машинного обучения для генерации текста. Он использует переменные окружения `OLLAMA_HOST` и `OLLAMA_PORT` для определения адреса и порта сервера Ollama.
Модуль автоматически получает список доступных моделей при первом обращении и использует первую модель из списка в качестве модели по умолчанию.

## Классы

### `Ollama`

**Описание**: Класс `Ollama` предназначен для взаимодействия с локально запущенными моделями Ollama.

**Наследует**:

- `OpenaiAPI`: Класс наследуется от `OpenaiAPI`, что позволяет использовать общую логику для работы с API OpenAI.

**Атрибуты**:

- `label` (str): Метка провайдера, в данном случае "Ollama".
- `url` (str): URL для Ollama.
- `login_url` (str | None): URL для логина (отсутствует, так как не требует аутентификации).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (в данном случае `False`).
- `working` (bool): Флаг, указывающий, работает ли провайдер (в данном случае `True`).
- `models` (List[str] | None): Список доступных моделей.
- `default_model` (str | None): Модель, используемая по умолчанию.

**Методы**:

- `get_models()`: Получает список доступных моделей Ollama.
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с моделью.

## Функции

### `get_models`

```python
@classmethod
def get_models(cls, api_base: str = None, **kwargs):
    """
    Получает список доступных моделей Ollama.

    Args:
        cls (Ollama): Класс Ollama.
        api_base (str, optional): Базовый URL API. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        List[str]: Список доступных моделей.

    Как работает функция:
    1. Проверяет, был ли уже получен список моделей (cls.models).
    2. Если список моделей не был получен, определяет URL для запроса списка моделей. Если передан api_base, то использует его, иначе использует переменные окружения OLLAMA_HOST и OLLAMA_PORT для формирования URL.
    3. Отправляет GET-запрос к API Ollama для получения списка моделей.
    4. Извлекает имена моделей из JSON-ответа и сохраняет их в cls.models.
    5. Устанавливает первую модель из списка в качестве модели по умолчанию (cls.default_model).
    6. Возвращает список доступных моделей.
    """
    ...
```

**Назначение**: Получение списка доступных моделей Ollama.

**Параметры**:

- `cls` (Ollama): Класс `Ollama`.
- `api_base` (str, optional): Базовый URL API. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `List[str]`: Список доступных моделей.

```
   A
   │
   │ api_base is None?
   ├─── Нет: B
   │   │
   │   B
   │   │ url = api_base.replace("/v1", "/api/tags")
   │   │
   └─── Да: C
       │
       C
       │ host = os.getenv("OLLAMA_HOST", "127.0.0.1")
       │ port = os.getenv("OLLAMA_PORT", "11434")
       │ url = f"http://{host}:{port}/api/tags"
       │
   │
   D
   │ models = requests.get(url).json()["models"]
   │ cls.models = [model["name"] for model in models]
   │ cls.default_model = cls.models[0]
   │
   E
   │ return cls.models
   │
   Конец
```

**Примеры**:

```python
# Пример вызова функции
models = Ollama.get_models()
print(models)
```

### `create_async_generator`

```python
    @classmethod
    def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_base: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с моделью Ollama.

        Args:
            cls (Ollama): Класс Ollama.
            model (str): Имя модели.
            messages (Messages): Список сообщений.
            api_base (str, optional): Базовый URL API. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор.

        Как работает функция:
        1. Определяет базовый URL API. Если передан api_base, использует его, иначе использует переменные окружения OLLAMA_HOST и OLLAMA_PORT для формирования URL.
        2. Вызывает метод create_async_generator родительского класса (super().create_async_generator) для создания асинхронного генератора.
        """
        ...
```

**Назначение**: Создание асинхронного генератора для взаимодействия с моделью Ollama.

**Параметры**:

- `cls` (Ollama): Класс `Ollama`.
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений.
- `api_base` (str, optional): Базовый URL API. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор.

```
   A
   │
   │ api_base is None?
   ├─── Нет: B
   │   │
   │   B
   │   │ super().create_async_generator(model, messages, api_base=api_base, **kwargs)
   │   │
   └─── Да: C
       │
       C
       │ host = os.getenv("OLLAMA_HOST", "localhost")
       │ port = os.getenv("OLLAMA_PORT", "11434")
       │ api_base: str = f"http://{host}:{port}/v1"
       │ super().create_async_generator(model, messages, api_base=api_base, **kwargs)
       │
   Конец
```

**Примеры**:

```python
# Пример вызова функции
messages = [{"role": "user", "content": "Hello"}]
generator = Ollama.create_async_generator(model="llama2", messages=messages)