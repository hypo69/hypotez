# Модуль HuggingFaceAPI

## Обзор

Модуль `HuggingFaceAPI` предназначен для взаимодействия с API Hugging Face для генерации текста. Он наследует функциональность от класса `OpenaiTemplate` и предоставляет методы для получения моделей, создания асинхронных генераторов и управления ключами API.

## Подробней

Этот модуль позволяет использовать модели Hugging Face для генерации текста, поддерживая различные типы моделей, включая текстовые и визуальные. Он также обеспечивает механизм для обработки ошибок и выбора подходящего провайдера API.

## Классы

### `HuggingFaceAPI`

**Описание**: Класс `HuggingFaceAPI` предназначен для взаимодействия с API Hugging Face для генерации текста. Он наследует функциональность от класса `OpenaiTemplate` и предоставляет методы для получения моделей, создания асинхронных генераторов и управления ключами API.

**Наследует**:
- `OpenaiTemplate`: Предоставляет базовую функциональность для работы с API OpenAI.

**Атрибуты**:
- `label` (str): Метка провайдера "HuggingFace (Text Generation)".
- `parent` (str): Родительский провайдер "HuggingFace".
- `url` (str): URL API Hugging Face "https://api-inference.huggingface.com".
- `api_base` (str): Базовый URL API Hugging Face "https://api-inference.huggingface.co/v1".
- `working` (bool): Указывает, что провайдер работает (True).
- `needs_auth` (bool): Указывает, что требуется аутентификация (True).
- `default_model` (str): Модель по умолчанию `default_llama_model`.
- `default_vision_model` (str): Визуальная модель по умолчанию `default_vision_model`.
- `vision_models` (list[str]): Список визуальных моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `fallback_models` (list[str]): Список резервных моделей.
- `provider_mapping` (dict[str, dict]): Отображение моделей провайдеров.

**Принцип работы**:

Класс `HuggingFaceAPI` предназначен для взаимодействия с API Hugging Face для генерации текста. 
Он использует `provider_mapping` для определения правильного провайдера и задачи для каждой модели. 
Если модель не найдена в `provider_mapping`, он пытается получить её отображение асинхронно. 
Он также предоставляет методы для получения списка поддерживаемых моделей и создания асинхронных генераторов для генерации текста.

**Методы**:
- `get_model`: Получает модель.
- `get_models`: Получает список доступных моделей.
- `get_mapping`: Получает отображение моделей провайдеров.
- `create_async_generator`: Создает асинхронный генератор.

## Методы класса

### `get_model`

```python
    @classmethod
    def get_model(cls, model: str, **kwargs) -> str:
        """Получает модель.

        Args:
            model (str): Имя модели.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Имя модели.
        
        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
        """
        ...
```

**Назначение**:
Этот метод используется для получения имени модели. Если модель не поддерживается, он возвращает имя модели.

**Параметры**:
- `model` (str): Имя модели, которую необходимо получить.
- `**kwargs`: Дополнительные параметры, которые могут потребоваться для получения модели.

**Возвращает**:
- `str`: Имя модели. Если модель не поддерживается, возвращается исходное имя модели.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если модель не поддерживается и возникает ошибка.

**Как работает функция**:
Функция пытается получить модель, используя родительский метод `super().get_model(model, **kwargs)`. 
Если возникает исключение `ModelNotSupportedError`, функция перехватывает его и возвращает исходное имя модели.

**Примеры**:

```python
model_name = HuggingFaceAPI.get_model("google/gemma-3-27b-it")
print(model_name)
```

### `get_models`

```python
    @classmethod
    def get_models(cls, **kwargs) -> list[str]:
        """Получает список доступных моделей.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            list[str]: Список доступных моделей.
        """
        ...
```

**Назначение**:
Этот метод используется для получения списка доступных моделей из API Hugging Face.

**Параметры**:
- `**kwargs`: Дополнительные параметры, которые могут потребоваться для получения списка моделей.

**Возвращает**:
- `list[str]`: Список доступных моделей.

**Как работает функция**:
Функция сначала проверяет, был ли уже получен список моделей. Если нет, она делает запрос к API Hugging Face для получения списка моделей, 
которые поддерживают задачу "conversational" и имеют статус "live". Затем она добавляет модели из `cls.provider_mapping.keys()` в этот список. 
Если запрос к API не удался, она использует `cls.fallback_models` в качестве резервного списка моделей.

**Примеры**:

```python
models = HuggingFaceAPI.get_models()
print(models)
```

### `get_mapping`

```python
    @classmethod
    async def get_mapping(cls, model: str, api_key: str = None):
        """Получает отображение моделей провайдеров.

        Args:
            model (str): Имя модели.
            api_key (str, optional): Ключ API. По умолчанию `None`.

        Returns:
            dict: Отображение моделей провайдеров.
        """
        ...
```

**Назначение**:
Этот метод используется для получения отображения моделей провайдеров из API Hugging Face.

**Параметры**:
- `model` (str): Имя модели, для которой необходимо получить отображение.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.

**Возвращает**:
- `dict`: Отображение моделей провайдеров.

**Как работает функция**:
Функция сначала проверяет, есть ли отображение для данной модели в `cls.provider_mapping`. 
Если да, она возвращает его. Если нет, она делает асинхронный запрос к API Hugging Face для получения отображения. 
Полученное отображение сохраняется в `cls.provider_mapping` и возвращается.

**Примеры**:

```python
import asyncio
async def main():
    mapping = await HuggingFaceAPI.get_mapping("google/gemma-3-27b-it", api_key="YOUR_API_KEY")
    print(mapping)

asyncio.run(main())
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_base: str = None,
        api_key: str = None,
        max_tokens: int = 2048,
        max_inputs_lenght: int = 10000,
        media: MediaListType = None,
        **kwargs
    ):
        """Создает асинхронный генератор.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений.
            api_base (str, optional): Базовый URL API. По умолчанию `None`.
            api_key (str, optional): Ключ API. По умолчанию `None`.
            max_tokens (int, optional): Максимальное количество токенов. По умолчанию 2048.
            max_inputs_lenght (int, optional): Максимальная длина входных данных. По умолчанию 10000.
            media (MediaListType, optional): Список медиафайлов. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.
        """
        ...
```

**Назначение**:
Этот метод создает асинхронный генератор для генерации текста с использованием API Hugging Face.

**Параметры**:
- `model` (str): Имя модели, которую необходимо использовать для генерации текста.
- `messages` (Messages): Список сообщений, которые будут отправлены в API для генерации текста.
- `api_base` (str, optional): Базовый URL API. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов, которые должны быть сгенерированы. По умолчанию 2048.
- `max_inputs_lenght` (int, optional): Максимальная длина входных данных. По умолчанию 10000.
- `media` (MediaListType, optional): Список медиафайлов, которые будут отправлены в API. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, которые могут потребоваться для создания генератора.

**Как работает функция**:
Функция сначала получает модель, используя метод `cls.get_model(model)`. Затем она получает отображение моделей провайдеров, 
используя метод `cls.get_mapping(model, api_key)`. Если отображение не найдено, выбрасывается исключение `ModelNotSupportedError`. 
Затем функция итерируется по провайдерам в отображении и пытается создать асинхронный генератор, используя метод `super().create_async_generator()`. 
Если возникает ошибка `PaymentRequiredError`, функция перехватывает её и пытается использовать другого провайдера.

**Примеры**:

```python
import asyncio
async def main():
    messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
    generator = HuggingFaceAPI.create_async_generator(model="google/gemma-3-27b-it", messages=messages, api_key="YOUR_API_KEY")
    async for chunk in await generator:
        print(chunk)

asyncio.run(main())
```

## Функции

### `calculate_lenght`

```python
def calculate_lenght(messages: Messages) -> int:
    """Вычисляет длину сообщений.

    Args:
        messages (Messages): Список сообщений.

    Returns:
        int: Суммарная длина сообщений.
    """
    ...
```

**Назначение**:
Функция `calculate_lenght` предназначена для вычисления суммарной длины списка сообщений.

**Параметры**:
- `messages` (Messages): Список сообщений, для которых необходимо вычислить длину.

**Возвращает**:
- `int`: Суммарная длина всех сообщений в списке.

**Как работает функция**:
Функция итерируется по каждому сообщению в списке `messages` и вычисляет длину содержимого каждого сообщения, добавляя 16 к этой длине. Затем она суммирует все эти значения и возвращает результат.

**Примеры**:

```python
messages = [{"role": "user", "content": "Привет"}, {"role": "assistant", "content": "Как дела?"}]
total_length = calculate_lenght(messages)
print(total_length)  # Вывод: 24 + 20 = 44