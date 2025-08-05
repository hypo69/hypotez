# Модуль DeepInfraChat

## Обзор

Модуль `DeepInfraChat` предоставляет класс `DeepInfraChat`, который используется для взаимодействия с API DeepInfra.com и осуществляет запросы к модели DeepSeek, а также к другим моделям, доступным через API DeepInfra.

## Классы

### `class DeepInfraChat`

**Описание**: Класс `DeepInfraChat` наследует класс `OpenaiTemplate` и предоставляет реализацию для работы с API DeepInfra.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `url` (str): URL-адрес для запросов к API DeepInfra.com.
- `api_base` (str): Базовый URL для запросов к API DeepInfra.com.
- `working` (bool): Флаг, указывающий на доступность API DeepInfra.com.
- `default_model` (str): Имя модели по умолчанию для запросов.
- `default_vision_model` (str): Имя модели по умолчанию для запросов, связанных с обработкой изображений.
- `vision_models` (list): Список моделей для запросов, связанных с обработкой изображений.
- `models` (list): Список доступных моделей для запросов.
- `model_aliases` (dict): Словарь соответствия псевдонимов моделей и их полных имен.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.DeepInfraChat import DeepInfraChat

# Создание инстанса класса DeepInfraChat
deepinfra_chat = DeepInfraChat()

# Выполнение запроса к модели DeepSeek
response = deepinfra_chat.get_response(
    "Привет, как дела?",
    model="deepseek-ai/DeepSeek-V3"
)

# Вывод ответа модели
print(response)
```

## Внутренние функции

### `get_response`

**Назначение**: Метод `get_response` отправляет запрос к API DeepInfra.com с заданным текстом и возвращает ответ модели.

**Параметры**:
- `text` (str): Текст запроса.
- `model` (str, optional): Имя модели для запроса. По умолчанию используется `default_model`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию используется значение по умолчанию для модели.
- `temperature` (float, optional): Параметр, влияющий на креативность модели. По умолчанию используется значение по умолчанию для модели.
- `top_p` (float, optional): Параметр, влияющий на выбор токенов. По умолчанию используется значение по умолчанию для модели.
- `top_k` (int, optional): Параметр, влияющий на выбор токенов. По умолчанию используется значение по умолчанию для модели.
- `stream` (bool, optional): Флаг, указывающий на то, нужно ли получать ответ по частям. По умолчанию используется значение по умолчанию для модели.
- `stop` (list, optional): Список токенов, при встрече с которыми модель прекратит генерацию ответа. По умолчанию используется значение по умолчанию для модели.

**Возвращает**:
- `str`: Ответ модели в виде текста.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка во время запроса к API DeepInfra.com.

**Пример**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.DeepInfraChat import DeepInfraChat

# Создание инстанса класса DeepInfraChat
deepinfra_chat = DeepInfraChat()

# Выполнение запроса к модели DeepSeek с указанием максимального количества токенов
response = deepinfra_chat.get_response(
    "Расскажи мне анекдот",
    model="deepseek-ai/DeepSeek-V3",
    max_tokens=50
)

# Вывод ответа модели
print(response)
```