# Модуль `ThebApi`

## Обзор

Модуль `ThebApi` предоставляет класс для взаимодействия с API сервиса TheB.AI. Он наследует функциональность от класса `OpenaiTemplate` и предназначен для создания асинхронных генераторов текста на основе предоставленных сообщений и параметров модели. Модуль поддерживает различные модели, включая GPT-3.5, GPT-4, Claude и Llama.

## Подробней

Модуль `ThebApi` является частью проекта `hypotez` и предназначен для интеграции с API TheB.AI для генерации текста. Он использует асинхронные генераторы для обработки запросов и поддерживает различные параметры, такие как температура и top_p. Этот модуль требует аутентификации для доступа к API TheB.AI.

## Классы

### `ThebApi`

**Описание**: Класс `ThebApi` предназначен для взаимодействия с API сервиса TheB.AI.

**Наследует**:
- `OpenaiTemplate`: Класс наследует функциональность от `OpenaiTemplate`, который, вероятно, предоставляет общую структуру для взаимодействия с API, подобными OpenAI.

**Атрибуты**:
- `label` (str): Метка для идентификации провайдера API ("TheB.AI API").
- `url` (str): URL главной страницы сервиса TheB.AI ("https://theb.ai").
- `login_url` (str): URL страницы входа в сервис TheB.AI ("https://beta.theb.ai/home").
- `api_base` (str): Базовый URL для API запросов ("https://api.theb.ai/v1").
- `working` (bool): Флаг, указывающий, что API в настоящее время работает (True).
- `needs_auth` (bool): Флаг, указывающий, что для доступа к API требуется аутентификация (True).
- `default_model` (str): Модель, используемая по умолчанию ("theb-ai").
- `fallback_models` (list): Список моделей, которые могут быть использованы в случае недоступности модели по умолчанию.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для генерации текста на основе предоставленных сообщений и параметров модели.

## Функции

### `create_async_generator`

```python
@classmethod
def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    temperature: float = None,
    top_p: float = None,
    **kwargs
) -> CreateResult:
    """Создает асинхронный генератор для генерации текста с использованием API TheB.AI.

    Args:
        cls: Класс `ThebApi`.
        model (str): Идентификатор модели для использования.
        messages (Messages): Список сообщений для передачи в модель.
        temperature (float, optional): Температура для управления случайностью генерации. По умолчанию `None`.
        top_p (float, optional): Top-p значение для фильтрации вероятностей токенов. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        CreateResult: Результат создания асинхронного генератора.

    Как работает функция:
    1. Извлекает системные сообщения из списка сообщений и объединяет их в одну строку.
    2. Фильтрует список сообщений, оставляя только сообщения, не являющиеся системными.
    3. Формирует словарь `data` с параметрами запроса, включая системное сообщение, температуру и top_p.
    4. Вызывает метод `create_async_generator` родительского класса (`OpenaiTemplate`) с добавлением сформированного словаря `data` в качестве дополнительных данных.

    ASII flowchart:

    Начало
     ↓
    Извлечение системных сообщений
     ↓
    Фильтрация сообщений
     ↓
    Формирование данных запроса
     ↓
    Вызов create_async_generator родительского класса
     ↓
    Конец
    """
    system_message = "\n".join([message["content"] for message in messages if message["role"] == "system"])
    messages = [message for message in messages if message["role"] != "system"]
    data = {
        "model_params": filter_none(
            system_prompt=system_message,
            temperature=temperature,
            top_p=top_p,
        )
    }
    return super().create_async_generator(model, messages, extra_data=data, **kwargs)
```

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Идентификатор модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений, передаваемых в модель для генерации ответа.
- `temperature` (float, optional): Параметр, контролирующий случайность генерации текста. Чем выше значение, тем более случайным будет результат. По умолчанию `None`.
- `top_p` (float, optional): Параметр, используемый для фильтрации наиболее вероятных токенов при генерации текста. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в функцию.

**Возвращает**:
- `CreateResult`: Результат создания асинхронного генератора.

**Примеры**:

```python
# Пример вызова функции create_async_generator
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
result = ThebApi.create_async_generator(model="gpt-3.5-turbo", messages=messages, temperature=0.7, top_p=0.9)
print(result)