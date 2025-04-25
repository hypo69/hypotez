# Модуль Local
## Обзор
Модуль предоставляет класс `Local`, который является провайдером для работы с локальными моделями GPT4All.
## Подробнее
Класс `Local` реализует интерфейс `AbstractProvider` и предоставляет функциональность для взаимодействия с локальными моделями GPT4All, установленными с помощью пакета `gpt4all`. 
## Классы
### `class Local`
**Описание**: Класс `Local` - это провайдер для работы с локальными моделями GPT4All.
**Наследует**:
- `AbstractProvider`
- `ProviderModelMixin`
**Атрибуты**:
- `label` (str): Метка провайдера, равна "GPT4All".
- `working` (bool): Флаг, указывающий, доступен ли провайдер.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу ответов.
**Методы**:
- `get_models()`: Возвращает список доступных локальных моделей GPT4All.
- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: Создает завершение с помощью выбранной модели, сообщениями и потоковой передачей.
## Методы класса
### `get_models`
```python
    @classmethod
    def get_models(cls):
        """
        Возвращает список доступных локальных моделей GPT4All.

        Если список моделей пуст, он заполняется из модуля `locals.models` с помощью функции `get_models`.
        По умолчанию используется первая модель из списка доступных моделей.

        Returns:
            list: Список доступных локальных моделей GPT4All.

        Example:
            >>> Local.get_models()
            ['gpt4all-lora', 'gpt4all-j', 'gpt4all-l2']
        """
        if not cls.models:
            cls.models = list(get_models())
            cls.default_model = cls.models[0]
        return cls.models
```

### `create_completion`
```python
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs
    ) -> CreateResult:
        """
        Создает завершение с помощью выбранной модели, сообщениями и потоковой передачей.

        Проверяет наличие необходимых зависимостей (`gpt4all`). 
        Если зависимость отсутствует, вызывается исключение `MissingRequirementsError`.
        Использует локальный провайдер `LocalProvider` для создания завершения.

        Args:
            model (str): Имя модели, используемой для создания завершения.
            messages (Messages): Список сообщений для обработки.
            stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
            **kwargs: Дополнительные аргументы для модели.

        Returns:
            CreateResult: Результат создания завершения, включающий текст ответа и информацию о потоковой передаче.

        Raises:
            MissingRequirementsError: Если отсутствует необходимая зависимость.

        Example:
            >>> messages = [
            ...    {"role": "user", "content": "Привет, как дела?"},
            ... ]
            >>> create_completion(model="gpt4all-lora", messages=messages, stream=False)
            CreateResult(content='Хорошо, спасибо, а у тебя?', stream=False)
        """
        if not has_requirements:
            raise MissingRequirementsError('Install "gpt4all" package | pip install -U g4f[local]')
        return LocalProvider.create_completion(
            cls.get_model(model),
            messages,
            stream,
            **kwargs
        )
```
## Параметры класса
- `models` (list): Список доступных локальных моделей GPT4All.
- `default_model` (str): Имя модели по умолчанию, используемой для создания завершения.
## Примеры
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.local.Local import Local

# Получить список доступных локальных моделей GPT4All
models = Local.get_models()
print(f"Доступные модели: {models}")

# Создать завершение с помощью модели "gpt4all-lora"
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]
result = Local.create_completion(model="gpt4all-lora", messages=messages, stream=False)
print(f"Результат: {result.content}")
```
```markdown