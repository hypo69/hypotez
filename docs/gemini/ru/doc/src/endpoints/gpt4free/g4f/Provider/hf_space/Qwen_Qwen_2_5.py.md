# Модуль Qwen_Qwen_2_5

## Обзор

Модуль предоставляет класс `Qwen_Qwen_2_5`, который реализует асинхронный генератор для работы с моделью `Qwen-Qwen2.5` от Alibaba Cloud. 

## Подробнее

Этот модуль является частью проекта `hypotez` и обеспечивает взаимодействие с  `Qwen-Qwen2.5`  через  API  `https://qwen-qwen2-5.hf.space`.  Он использует  `aiohttp`  для асинхронного  HTTP  запроса.  

###  Как работает этот модуль?

**1. Создание уникального  ID  сессии:** 

- В `create_async_generator`  генерируется случайный  ID  сессии.

**2. Подготовка запроса  `join`:**

- Запрос  `join`  отправляется на  API  `https://qwen-qwen2-5.hf.space/queue/join`.  
- В  `payload_join`  содержится  prompt  и  system_prompt  (если доступен). 

**3.  Получение  `event_id`  :** 

- В  ответе  на  запрос  `join`  получается  `event_id`.

**4.  Подготовка  `data stream`  запроса:**

- Запрос  `data stream`  отправляется на  API  `https://qwen-qwen2-5.hf.space/queue/data`. 

**5.  Получение  и обработка ответов  в потоке:**

-  `response.content`  возвращает  `data stream`  в виде строк.
-  Обрабатывает  ответы  в виде  `JSON`,  используя  `json.loads`. 
-  Извлекает  `output_data`  и  `fragment`  и  отправляет  их  как  генератор  в  виде  ответов  на  промпт. 
-  Проверяет  `msg`  на  стадии  генерации  и  завершения. 
-  При  завершении  отправляет  последний  отвеот  в виде  `final_text`.

## Классы

### `Qwen_Qwen_2_5`
**Описание**: Класс, представляющий модель `Qwen-Qwen2.5` для проекта `hypotez`.
**Наследует**: 
    - `AsyncGeneratorProvider`:  Класс с  `async`  методами, отвечающими за  асинхронную  обработку данных. 
    - `ProviderModelMixin`:  Класс,  содержащий  общие  свойства  и  методы  для  разных  моделей.
**Атрибуты**: 
    - `label` (str):  Название модели.
    - `url` (str):  Базовый URL  API  модели.
    - `api_endpoint` (str):  URL  API  для  запроса  `join`.
    - `working` (bool):  Флаг, указывающий, что  API  модели  доступен.
    - `supports_stream` (bool):  Флаг, указывающий, что модель поддерживает  потоковую  генерацию.
    - `supports_system_message` (bool):  Флаг, указывающий, что модель поддерживает  системные  сообщения.
    - `supports_message_history` (bool):  Флаг, указывающий, что модель поддерживает  историю  сообщений.
    - `default_model` (str):  Название модели по  умолчанию.
    - `model_aliases` (dict):  Словарь, содержащий  псевдонимы  моделей.
    - `models` (list):  Список  доступных  моделей.
**Методы**: 
    - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: 
        **Описание**:  Создает  асинхронный  генератор  для  модели.
        **Параметры**:
        - `model` (str):  Название  модели.
        - `messages` (Messages):  Список  сообщений  для  модели.
        - `proxy` (str, optional):  Прокси-сервер. По умолчанию `None`.
        - `**kwargs`:  Дополнительные  параметры.
        **Возвращает**: 
            - `AsyncResult`:  Асинхронный  результат  в  виде  генератора.

###  Внутренние функции:

####  `generate_session_hash() -> str`: 

**Описание**:  Генерирует  уникальный  хеш  сессии.

####  `create_async_generator() -> AsyncResult`: 

**Описание**:  Создает  асинхронный  генератор  для  модели.

## Параметры класса
- `label` (str): Название модели.
- `url` (str):  Базовый URL API модели.
- `api_endpoint` (str): URL API для запроса `join`.
- `working` (bool): Флаг, указывающий, что API модели доступен.
- `supports_stream` (bool): Флаг, указывающий, что модель поддерживает потоковую генерацию.
- `supports_system_message` (bool): Флаг, указывающий, что модель поддерживает системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, что модель поддерживает историю сообщений.
- `default_model` (str):  Название модели по умолчанию.
- `model_aliases` (dict):  Словарь, содержащий псевдонимы моделей.
- `models` (list): Список доступных моделей.


## Методы

### `create_async_generator`

**Описание**:  Создает  асинхронный  генератор  для  модели.

**Параметры**:
- `model` (str):  Название модели.
- `messages` (Messages):  Список сообщений для модели.
- `proxy` (str, optional):  Прокси-сервер. По умолчанию `None`.
- `**kwargs`:  Дополнительные параметры.

**Возвращает**:
- `AsyncResult`:  Асинхронный результат в виде генератора.

## Примеры

```python
# Использование модуля
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space import Qwen_Qwen_2_5
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание списка сообщений
messages = Messages([
    {"role": "user", "content": "Привет!"}, 
    {"role": "assistant", "content": "Привет! Как дела?"}
])

# Создание асинхронного генератора для модели
async_generator = Qwen_Qwen_2_5.create_async_generator(model="qwen-2.5", messages=messages)

# Получение ответов из генератора
async for response in async_generator:
    print(response)
```
```markdown