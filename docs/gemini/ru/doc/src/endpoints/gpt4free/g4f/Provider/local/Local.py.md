# Документация модуля `Local.py`

## Обзор

Модуль `Local.py` предоставляет интеграцию с локальными моделями GPT4All через класс `Local`. Он позволяет использовать модели GPT4All для генерации текста, поддерживая как потоковую передачу, так и управление историей сообщений и системными сообщениями.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для работы с локальными AI-моделями, в частности, GPT4All. Он обеспечивает абстракцию для взаимодействия с этими моделями, позволяя легко интегрировать их в другие части проекта. Модуль проверяет наличие необходимых зависимостей (`gpt4all`) и предоставляет метод `create_completion` для генерации текста на основе предоставленных сообщений.

## Классы

### `Local`

**Описание**: Класс `Local` предоставляет интерфейс для работы с локальными моделями GPT4All.

**Наследует**:

- `AbstractProvider`: Абстрактный базовый класс для провайдеров моделей.
- `ProviderModelMixin`: Миксин, предоставляющий утилиты для работы с моделями провайдера.

**Атрибуты**:

- `label` (str): Метка провайдера, в данном случае `"GPT4All"`.
- `working` (bool): Флаг, указывающий, работает ли провайдер, в данном случае `True`.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений, в данном случае `True`.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения, в данном случае `True`.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу, в данном случае `True`.

**Методы**:

- `get_models()`: Возвращает список доступных локальных моделей GPT4All.
- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: Создает завершение на основе предоставленных сообщений, используя указанную локальную модель.

### `Local.get_models`

**Назначение**: Получает список доступных локальных моделей GPT4All.

```python
@classmethod
def get_models(cls):
    """Возвращает список доступных локальных моделей GPT4All.

    Args:
        cls: Ссылка на класс.

    Returns:
        list: Список доступных локальных моделей GPT4All.
    """
```

**Как работает функция**:

1. Проверяет, был ли уже получен список моделей (`cls.models`).
2. Если список моделей пуст, вызывает функцию `get_models()` из модуля `...locals.models` для получения списка моделей.
3. Устанавливает первую модель в списке как модель по умолчанию (`cls.default_model`).
4. Возвращает список моделей.

### `Local.create_completion`

**Назначение**: Создает завершение (completion) на основе предоставленных сообщений, используя указанную локальную модель GPT4All.

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    **kwargs
) -> CreateResult:
    """Создает завершение на основе предоставленных сообщений, используя указанную локальную модель.

    Args:
        cls: Ссылка на класс.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для модели.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        **kwargs: Дополнительные аргументы, передаваемые в функцию `create_completion` провайдера `LocalProvider`.

    Returns:
        CreateResult: Результат создания завершения.

    Raises:
        MissingRequirementsError: Если не установлены необходимые зависимости (`gpt4all`).
    """
```

**Параметры**:

- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для модели.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу.
- `**kwargs`: Дополнительные аргументы, передаваемые в функцию `create_completion` провайдера `LocalProvider`.

**Возвращает**:

- `CreateResult`: Результат создания завершения.

**Вызывает исключения**:

- `MissingRequirementsError`: Если не установлены необходимые зависимости (`gpt4all`).

**Как работает функция**:

1. Проверяет, установлены ли необходимые зависимости (`gpt4all`). Если зависимости не установлены, вызывает исключение `MissingRequirementsError`.
2. Вызывает функцию `create_completion` из класса `LocalProvider` (из модуля `...locals.provider`) с указанием модели, сообщений, флага потоковой передачи и дополнительных аргументов.
3. Возвращает результат создания завершения.

**Примеры**:

```python
# Пример вызова функции create_completion
model_name = "ggml-model-gpt4all-falcon-q4_0.bin"  # Пример имени модели
messages_example = [{"role": "user", "content": "Hello, how are you?"}]
stream_option = False

try:
    result = Local.create_completion(model=model_name, messages=messages_example, stream=stream_option)
    print(f"Результат: {result}")
except MissingRequirementsError as ex:
    print(f"Ошибка: {ex}")
```
```python
# Пример вызова функции create_completion
model_name = "ggml-model-gpt4all-falcon-q4_0.bin"  # Пример имени модели
messages_example = [{"role": "user", "content": "Hello, how are you?"}]
stream_option = True

try:
    result = Local.create_completion(model=model_name, messages=messages_example, stream=stream_option, temperature=0.7)
    print(f"Результат: {result}")
except MissingRequirementsError as ex:
    print(f"Ошибка: {ex}")
```