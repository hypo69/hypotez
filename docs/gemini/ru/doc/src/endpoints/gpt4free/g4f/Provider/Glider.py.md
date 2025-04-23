# Документация модуля Glider

## Обзор

Модуль `Glider` предоставляет класс для взаимодействия с сервисом Glider.so, использующим API, совместимое с OpenAI. Он наследуется от класса `OpenaiTemplate` и предназначен для работы с различными моделями, предоставляемыми Glider.

## Подробней

Модуль определяет основные параметры, такие как URL, endpoint API и список поддерживаемых моделей, а также их алиасы. Это позволяет унифицировать взаимодействие с Glider.so через общий интерфейс, предоставляемый классом `OpenaiTemplate`.

## Классы

### `Glider`

**Описание**: Класс для работы с сервисом Glider.so.

**Наследует**:

- `OpenaiTemplate`: Обеспечивает базовую функциональность для работы с API, совместимыми с OpenAI.

**Атрибуты**:

- `label` (str): Метка провайдера, в данном случае "Glider".
- `url` (str): URL сервиса Glider.so.
- `api_endpoint` (str): URL API endpoint для взаимодействия с Glider.so.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию, в данном случае 'chat-llama-3-1-70b'.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Словарь алиасов моделей для удобства использования.

**Принцип работы**:

Класс `Glider` наследует от `OpenaiTemplate`, что позволяет ему использовать общую логику для взаимодействия с API, совместимыми с OpenAI. Он определяет специфичные для Glider.so параметры, такие как URL, endpoint API и список поддерживаемых моделей. Это позволяет унифицировать взаимодействие с Glider.so через общий интерфейс.

## Методы класса

### `__init__`

```python
    def __init__(self):
        """
        Инициализирует экземпляр класса Glider.

        Args:
            Нет.

        Returns:
            None.

        Raises:
            Нет.
        """
        ...
```
### `create_payload`
```python
    def create_payload(self, messages: list[dict], model: str):
        """
        Создает payload для запроса к API Glider.

        Args:
            messages (list[dict]): Список сообщений для отправки.
            model (str): Имя используемой модели.

        Returns:
            dict: Payload для запроса.

        Raises:
            Нет.
        """
        ...
```

### `get_header`
```python
    def get_header(self):
        """
        Возвращает заголовок запроса к API Glider.

        Args:
            Нет.

        Returns:
            dict: Заголовок запроса.

        Raises:
            Нет.
        """
        ...
```

## Параметры класса

- `label` (str): Метка провайдера, всегда "Glider".
- `url` (str): URL сервиса Glider.so.
- `api_endpoint` (str): URL API endpoint для взаимодействия с Glider.so.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Словарь алиасов моделей для удобства использования.

## Примеры

Пример создания экземпляра класса `Glider`:

```python
from src.endpoints.gpt4free.g4f.Provider.Glider import Glider

glider_provider = Glider()
print(f"Провайдер: {glider_provider.label}, URL: {glider_provider.url}")
```

Пример использования алиаса модели:

```python
from src.endpoints.gpt4free.g4f.Provider.Glider import Glider

glider_provider = Glider()
model_name = glider_provider.model_aliases.get("llama-3.1-70b")
print(f"Имя модели: {model_name}")
```