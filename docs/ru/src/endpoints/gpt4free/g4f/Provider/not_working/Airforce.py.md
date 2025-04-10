# Модуль для работы с провайдером Airforce
=================================================

Модуль содержит класс `Airforce`, который используется для взаимодействия с API Airforce для генерации текста и изображений.

Пример использования
----------------------

```python
# Пример генерации текста
messages = [{"role": "user", "content": "Hello, world!"}]
async for result in Airforce.create_async_generator(model="llama-3.1-70b-chat", messages=messages):
    print(result)

# Пример генерации изображения
async for result in Airforce.create_async_generator(model="flux", messages=messages, prompt="A cat"):
    print(result)
```

## Обзор

Модуль `Airforce` предоставляет асинхронный интерфейс для взаимодействия с API Airforce, позволяя генерировать текст и изображения. Он поддерживает потоковую передачу данных для текстовой генерации и предоставляет методы для фильтрации нежелательного контента из ответов.

## Подробней

Этот код используется для интеграции с API Airforce, предоставляя функциональность для генерации текста и изображений. Он обрабатывает запросы к API, фильтрует ответы и возвращает результаты в асинхронном режиме. В проекте `hypotez` данный модуль позволяет использовать модели Airforce для различных задач, таких как создание контента и обработка изображений.

## Классы

### `Airforce`

**Описание**: Класс `Airforce` является асинхронным провайдером для работы с API Airforce. Он предоставляет методы для генерации текста и изображений, а также для получения списка доступных моделей.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): Базовый URL API Airforce.
- `api_endpoint_completions` (str): URL для генерации текста.
- `api_endpoint_imagine2` (str): URL для генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `models` (List[str]): Список доступных моделей для генерации текста.
- `image_models` (List[str]): Список доступных моделей для генерации изображений.
- `hidden_models` (Set[str]): Набор скрытых моделей, которые не должны отображаться в списке доступных моделей.
- `additional_models_imagine` (List[str]): Список дополнительных моделей для генерации изображений.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей, позволяющий использовать более короткие и понятные имена для моделей.

**Методы**:
- `get_models()`: Возвращает список доступных моделей.
- `get_model(model: str) -> str`: Возвращает фактическое имя модели по псевдониму.
- `_filter_content(part_response: str) -> str`: Фильтрует нежелательный контент из частичного ответа.
- `_filter_response(response: str) -> str`: Фильтрует полный ответ, удаляя системные ошибки и другой нежелательный текст.
- `generate_image(model: str, prompt: str, size: str, seed: int, proxy: str = None) -> AsyncResult`: Генерирует изображение на основе заданных параметров.
- `generate_text(model: str, messages: Messages, max_tokens: int, temperature: float, top_p: float, stream: bool, proxy: str = None) -> AsyncResult`: Генерирует текст на основе заданных параметров.
- `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, max_tokens: int = 512, temperature: float = 1, top_p: float = 1, stream: bool = True, size: str = "1:1", seed: int = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для генерации текста или изображений.

## Функции

### `split_message`

```python
def split_message(message: str, max_length: int = 1000) -> List[str]:
    """Splits the message into parts up to (max_length)."""
    ...
```

**Назначение**: Разделяет сообщение на части длиной до `max_length` символов.

**Параметры**:
- `message` (str): Сообщение для разделения.
- `max_length` (int, optional): Максимальная длина каждой части сообщения. По умолчанию 1000.

**Возвращает**:
- `List[str]`: Список частей сообщения.

**Как работает функция**:
1. **Инициализация**: Функция принимает строку сообщения и максимальную длину чанка.
2. **Разделение на чанки**: Пока длина сообщения больше максимальной длины:
   - Находится последняя позиция пробела в пределах максимальной длины.
   - Если пробел не найден, сообщение разделяется по максимальной длине.
   - Первый чанк добавляется в список чанков, а сообщение обновляется, чтобы содержать оставшуюся часть.
3. **Добавление остатка**: Если после разделения остается часть сообщения, она добавляется в список чанков.
4. **Возврат результата**: Функция возвращает список чанков.

```
A: Начало
│
B: Проверка длины сообщения > max_length
│
├── Да ── C: Поиск последней позиции пробела в пределах max_length
│   │
│   ├── Найдено ── D: Добавление чанка в список и обновление сообщения
│   │   │
│   │   E: Повтор B
│   │
│   └── Не найдено ── F: Разделение сообщения по max_length
│       │
│       G: Добавление чанка в список и обновление сообщения
│       │
│       H: Повтор B
│
└── Нет ── I: Добавление остатка сообщения в список
    │
    J: Возврат списка чанков
```

**Примеры**:

```python
>>> split_message("This is a long message that needs to be split", max_length=10)
['This is a ', 'long messa', 'ge that ne', 'eds to be ', 'split']

>>> split_message("Short message", max_length=100)
['Short message']
```

### `Airforce.get_models`

```python
@classmethod
def get_models(cls):
    """Get available models with error handling"""
    ...
```

**Назначение**: Получает список доступных моделей для генерации текста и изображений с обработкой ошибок.

**Возвращает**:
- `List[str]`: Список доступных моделей.

**Как работает функция**:

1. **Проверка кэшированных моделей изображений**: Если список моделей изображений (`cls.image_models`) пуст, то:
   - **Попытка получить модели изображений**:
     - Отправляется GET-запрос к `f"{cls.url}/imagine2/models"` с заголовком User-Agent.
     - Если запрос успешен, результат преобразуется в JSON и сохраняется в `cls.image_models`. Дополнительные модели изображений добавляются к списку.
     - Если запрос не успешен, в консоль выводится сообщение об ошибке, и `cls.image_models` устанавливается равным списку дополнительных моделей изображений.
2. **Проверка кэшированных текстовых моделей**: Если список моделей (`cls.models`) пуст, то:
   - **Попытка получить текстовые модели**:
     - Отправляется GET-запрос к `f"{cls.url}/models"` с заголовком User-Agent.
     - Если запрос успешен:
       - Результат преобразуется в JSON.
       - Если в JSON есть ключ `'data'`, то извлекаются идентификаторы моделей из `data['data']`, добавляются модели изображений, и исключаются скрытые модели.
       - Иначе, `cls.models` устанавливается равным ключам псевдонимов моделей (`cls.model_aliases.keys()`).
     - Если запрос не успешен, в консоль выводится сообщение об ошибке, и `cls.models` устанавливается равным ключам псевдонимов моделей.
3. **Возврат списка моделей**: Возвращается список моделей (`cls.models`) или список ключей псевдонимов моделей, если `cls.models` пуст.

```
A: Начало функции get_models()
│
B: Проверка: cls.image_models пуст?
│
├── Да: ── C: Попытка получить список моделей изображений с API
│   │
│   D: Обработка ответа или ошибки
│
E: Проверка: cls.models пуст?
│
├── Да: ── F: Попытка получить список текстовых моделей с API
│   │
│   G: Обработка ответа или ошибки
│
H: Возврат: cls.models или ключи из cls.model_aliases
│
I: Конец
```

**Примеры**:
```python
>>> Airforce.get_models()
['llama-3.1-70b-chat', 'flux', ...]
```

### `Airforce.get_model`

```python
@classmethod
def get_model(cls, model: str) -> str:
    """Get the actual model name from alias"""
    ...
```

**Назначение**: Получает фактическое имя модели из псевдонима.

**Параметры**:
- `model` (str): Псевдоним модели.

**Возвращает**:
- `str`: Фактическое имя модели.

**Как работает функция**:

1. **Поиск псевдонима**: Функция пытается получить фактическое имя модели из словаря псевдонимов `cls.model_aliases` по заданному псевдониму `model`.
2. **Возврат результата**:
   - Если псевдоним найден, возвращается соответствующее ему фактическое имя модели.
   - Если псевдоним не найден, возвращается либо сам псевдоним `model`, либо значение `cls.default_model`, если `model` равен `None`.

```
A: Начало функции get_model()
│
B: Поиск псевдонима модели в cls.model_aliases
│
├── Псевдоним найден: ── C: Возврат фактического имени модели
│
└── Псевдоним не найден: ── D: Возврат model или cls.default_model
│
E: Конец
```

**Примеры**:

```python
>>> Airforce.get_model("hermes-2-dpo")
'Nous-Hermes-2-Mixtral-8x7B-DPO'

>>> Airforce.get_model("nonexistent-model")
'nonexistent-model'

>>> Airforce.get_model(None)
'llama-3.1-70b-chat'
```

### `Airforce._filter_content`

```python
@classmethod
def _filter_content(cls, part_response: str) -> str:
    """
    Filters out unwanted content from the partial response.
    """
    ...
```

**Назначение**: Фильтрует нежелательный контент из частичного ответа.

**Параметры**:
- `part_response` (str): Частичный ответ для фильтрации.

**Возвращает**:
- `str`: Отфильтрованный частичный ответ.

**Как работает функция**:

1. **Удаление сообщений об ограничении длины**:
   - Используется регулярное выражение для удаления текста, связанного с превышением лимита символов на сообщение.
2. **Удаление сообщений об ограничении скорости**:
   - Используется регулярное выражение для удаления текста, связанного с превышением лимита запросов в минуту.
3. **Возврат отфильтрованного ответа**: Возвращается `part_response` после выполнения замен.

```
A: Начало функции _filter_content()
│
B: Удаление сообщений об ограничении длины
│
C: Удаление сообщений об ограничении скорости
│
D: Возврат отфильтрованного ответа
│
E: Конец
```

**Примеры**:

```python
>>> Airforce._filter_content("One message exceeds the \\d+chars per message limit\\. Join our discord")
''

>>> Airforce._filter_content("Rate limit \\(\\d+\\/minute\\) exceeded\\. Join our discord")
''

>>> Airforce._filter_content("This is a clean message")
'This is a clean message'
```

### `Airforce._filter_response`

```python
@classmethod
def _filter_response(cls, response: str) -> str:
    """
    Filters the full response to remove system errors and other unwanted text.
    """
    ...
```

**Назначение**: Фильтрует полный ответ, удаляя системные ошибки и другой нежелательный текст.

**Параметры**:
- `response` (str): Полный ответ для фильтрации.

**Возвращает**:
- `str`: Отфильтрованный ответ.

**Вызывает исключения**:
- `ValueError`: Если ответ содержит сообщение об ошибке "Model not found or too long input. Or any other error (xD)".

**Как работает функция**:

1. **Проверка на наличие ошибки модели**:
   - Если в ответе содержится сообщение "Model not found or too long input. Or any other error (xD)", вызывается исключение `ValueError`.
2. **Удаление идентификаторов ошибок**:
   - Используется регулярное выражение для удаления текста, соответствующего идентификаторам ошибок.
3. **Удаление токенов `<|im_end|>`**:
   - Используется регулярное выражение для удаления токенов `<|im_end|>`.
4. **Удаление токенов `</s>`**:
   - Используется регулярное выражение для удаления токенов `</s>`.
5. **Удаление префиксов**:
   - Используется регулярное выражение для удаления префиксов "Assistant: ", "AI: ", "ANSWER: ", "Output: ".
6. **Фильтрация контента**:
   - Вызывается метод `_filter_content` для дополнительной фильтрации контента.
7. **Возврат отфильтрованного ответа**: Возвращается отфильтрованный ответ.

```
A: Начало функции _filter_response()
│
B: Проверка на наличие ошибки модели
│
├── Ошибка найдена: ── C: Вызов исключения ValueError
│
└── Ошибка не найдена: ── D: Удаление идентификаторов ошибок
    │
    E: Удаление токенов <|im_end|>
    │
    F: Удаление токенов </s>
    │
    G: Удаление префиксов
    │
    H: Фильтрация контента с помощью _filter_content()
    │
    I: Возврат отфильтрованного ответа
│
J: Конец
```

**Примеры**:

```python
>>> Airforce._filter_response("Model not found or too long input. Or any other error (xD)")
ValueError: Model not found or too long input. Or any other error (xD)

>>> Airforce._filter_response("[ERROR] '12345678-1234-1234-1234-123456789012'")
''

>>> Airforce._filter_response("<|im_end|>This is a message")
'This is a message'

>>> Airforce._filter_response("</s>This is a message")
'This is a message'

>>> Airforce._filter_response("Assistant: This is a message")
'This is a message'

>>> Airforce._filter_response("This is a clean message")
'This is a clean message'
```

### `Airforce.generate_image`

```python
@classmethod
async def generate_image(
    cls,
    model: str,
    prompt: str,
    size: str,
    seed: int,
    proxy: str = None
) -> AsyncResult:
    """
    Генерирует изображение на основе заданных параметров.
    """
    ...
```

**Назначение**: Генерирует изображение, используя API Airforce.

**Параметры**:
- `model` (str): Модель для генерации изображения.
- `prompt` (str): Текстовое описание изображения (prompt).
- `size` (str): Размер изображения.
- `seed` (int): Зерно для генерации изображения.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий объект `ImageResponse` с URL изображения.

**Вызывает исключения**:
- `RuntimeError`: Если генерация изображения не удалась.

**Как работает функция**:

1. **Определение заголовков**: Определяются заголовки HTTP-запроса, включая User-Agent, Accept, Accept-Language и Content-Type.
2. **Определение параметров**: Определяются параметры запроса, такие как модель, prompt, размер и зерно.
3. **Создание асинхронной сессии**: Используется `ClientSession` для выполнения асинхронного HTTP-запроса.
4. **Выполнение GET-запроса**: Отправляется GET-запрос к API Airforce для генерации изображения.
5. **Обработка ответа**:
   - Если статус ответа равен 200, извлекается URL изображения из ответа, и генерируется объект `ImageResponse`.
   - Если статус ответа не равен 200, извлекается текст ошибки из ответа и вызывается исключение `RuntimeError`.

```
A: Начало функции generate_image()
│
B: Определение заголовков HTTP-запроса
│
C: Определение параметров запроса
│
D: Создание асинхронной сессии
│
E: Выполнение GET-запроса к API Airforce
│
F: Проверка статуса ответа
│
├── Статус 200: ── G: Извлечение URL изображения и генерация ImageResponse
│
└── Статус не 200: ── H: Извлечение текста ошибки и вызов RuntimeError
│
I: Конец
```

**Примеры**:

```python
async for result in Airforce.generate_image(model="flux", prompt="A cat", size="1:1", seed=123):
    print(result)
```

### `Airforce.generate_text`

```python
@classmethod
async def generate_text(
    cls,
    model: str,
    messages: Messages,
    max_tokens: int,
    temperature: float,
    top_p: float,
    stream: bool,
    proxy: str = None
) -> AsyncResult:
    """
    Generates text, buffers the response, filters it, and returns the final result.
    """
    ...
```

**Назначение**: Генерирует текст, используя API Airforce.

**Параметры**:
- `model` (str): Модель для генерации текста.
- `messages` (Messages): Список сообщений для отправки в API.
- `max_tokens` (int): Максимальное количество токенов в ответе.
- `temperature` (float): Температура для генерации текста.
- `top_p` (float): Top-p значение для генерации текста.
- `stream` (bool): Указывает, использовать ли потоковую передачу данных.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий сгенерированный текст.

**Как работает функция**:

1. **Определение заголовков**: Определяются заголовки HTTP-запроса, включая User-Agent, Accept, Accept-Language и Content-Type.
2. **Разделение сообщений на части**: Сообщения разделяются на части длиной до 1000 символов.
3. **Определение данных запроса**: Определяются данные запроса, включая сообщения, модель, температуру, top_p и stream.
4. **Создание асинхронной сессии**: Используется `ClientSession` для выполнения асинхронного HTTP-запроса.
5. **Выполнение POST-запроса**: Отправляется POST-запрос к API Airforce для генерации текста.
6. **Обработка ответа**:
   - Если `stream` равен `True` (потоковая передача):
     - Читаются строки из ответа, декодируются и обрабатываются как JSON.
     - Извлекается контент из JSON, фильтруется и генерируется.
   - Если `stream` равен `False` (не потоковая передача):
     - Извлекается JSON из ответа, фильтруется контент и генерируется.

```
A: Начало функции generate_text()
│
B: Определение заголовков HTTP-запроса
│
C: Разделение сообщений на части
│
D: Определение данных запроса
│
E: Создание асинхронной сессии
│
F: Выполнение POST-запроса к API Airforce
│
G: Проверка stream
│
├── stream=True: ── H: Обработка потокового ответа
│
└── stream=False: ── I: Обработка не потокового ответа
│
J: Конец
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, world!"}]
async for result in Airforce.generate_text(model="llama-3.1-70b-chat", messages=messages, max_tokens=512, temperature=1, top_p=1, stream=True):
    print(result)
```

### `Airforce.create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    proxy: str = None,
    max_tokens: int = 512,
    temperature: float = 1,
    top_p: float = 1,
    stream: bool = True,
    size: str = "1:1",
    seed: int = None,
    **kwargs
) -> AsyncResult:
    """
    """
    ...
```

**Назначение**: Создает асинхронный генератор для генерации текста или изображений.

**Параметры**:
- `model` (str): Модель для генерации.
- `messages` (Messages): Список сообщений для отправки в API.
- `prompt` (str, optional): Текстовое описание изображения (prompt). По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию 512.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию 1.
- `top_p` (float, optional): Top-p значение для генерации текста. По умолчанию 1.
- `stream` (bool, optional): Указывает, использовать ли потоковую передачу данных. По умолчанию `True`.
- `size` (str, optional): Размер изображения. По умолчанию "1:1".
- `seed` (int, optional): Зерно для генерации изображения. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий сгенерированный текст или изображение.

**Как работает функция**:

1. **Получение фактического имени модели**: Получает фактическое имя модели с помощью `cls.get_model(model)`.
2. **Проверка типа модели**:
   - Если модель находится в списке моделей изображений (`cls.image_models`):
     - Если `prompt` не задан, используется контент последнего сообщения из `messages`.
     - Если `seed` не задан, генерируется случайное число.
     - Вызывается метод `cls.generate_image` для генерации изображения.
   - Если модель не находится в списке моделей изображений:
     - Вызывается метод `cls.generate_text` для генерации текста.

```
A: Начало функции create_async_generator()
│
B: Получение фактического имени модели
│
C: Проверка, является ли модель моделью изображения
│
├── Да: ── D: Подготовка параметров для генерации изображения
│   │
│   E: Вызов generate_image()
│
└── Нет: ── F: Вызов generate_text()
│
G: Конец
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, world!"}]
async for result in Airforce.create_async_generator(model="llama-3.1-70b-chat", messages=messages):
    print(result)

async for result in Airforce.create_async_generator(model="flux", messages=messages, prompt="A cat"):
    print(result)