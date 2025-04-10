# Модуль для работы с OpenAI API
=====================================

Модуль предоставляет инструменты для взаимодействия с OpenAI API, включая поддержку кэширования запросов, обработку различных типов ответов и интеграцию с Azure OpenAI Service.

## Обзор

Этот модуль содержит классы и функции, упрощающие взаимодействие с OpenAI API. Он включает в себя поддержку различных моделей, управление параметрами запросов, кэширование API-вызовов и обработку ошибок. Модуль также предоставляет возможность интеграции с Azure OpenAI Service.

## Подробней

Модуль предназначен для упрощения работы с OpenAI API, предоставляя удобные инструменты для отправки запросов и получения ответов. Он поддерживает различные типы ответов, такие как строки, целые числа, числа с плавающей запятой и булевы значения. Кроме того, модуль обеспечивает кэширование API-вызовов для повышения производительности и снижения затрат. Поддерживается работа как с OpenAI, так и с Azure OpenAI Service.

## Классы

### `LLMRequest`

**Описание**: Класс, представляющий собой запрос к языковой модели (LLM). Он содержит входные сообщения, конфигурацию модели и вывод модели.

**Принцип работы**: Класс `LLMRequest` позволяет формировать запросы к языковой модели, указывая системные и пользовательские подсказки, а также параметры модели. Он также обрабатывает ответы модели, преобразуя их в нужный тип данных.

**Атрибуты**:
- `system_template_name` (str, optional): Имя системного шаблона.
- `system_prompt` (str, optional): Системная подсказка.
- `user_template_name` (str, optional): Имя пользовательского шаблона.
- `user_prompt` (str, optional): Пользовательская подсказка.
- `output_type` (type, optional): Ожидаемый тип данных вывода модели.
- `model_params` (dict): Параметры модели.
- `model_output` (any): Вывод модели.
- `messages` (list): Список сообщений для отправки в модель.
- `response_raw` (str): Необработанный ответ от модели.
- `response_json` (dict): Ответ от модели в формате JSON.
- `response_value` (any): Преобразованное значение ответа.
- `response_justification` (str): Обоснование ответа.
- `response_confidence` (float): Уровень уверенности в ответе.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `LLMRequest`.
- `call`: Вызывает языковую модель с указанными конфигурациями рендеринга.
- `_coerce_to_bool`: Преобразует вывод LLM в булево значение.
- `_request_bool_llm_message`: Формирует сообщение для запроса булевого значения от LLM.
- `_coerce_to_integer`: Преобразует вывод LLM в целое число.
- `_request_integer_llm_message`: Формирует сообщение для запроса целого числа от LLM.
- `_coerce_to_float`: Преобразует вывод LLM в число с плавающей запятой.
- `_request_float_llm_message`: Формирует сообщение для запроса числа с плавающей запятой от LLM.
- `_coerce_to_enumerable`: Преобразует вывод LLM в одно из указанных значений перечисления.
- `_request_enumerable_llm_message`: Формирует сообщение для запроса значения перечисления от LLM.

#### `__init__`
```python
def __init__(self, system_template_name:str=None, system_prompt:str=None, 
                 user_template_name:str=None, user_prompt:str=None, 
                 output_type=None,
                 **model_params) -> None:
    """
    Инициализирует экземпляр класса `LLMRequest` с указанными системными и пользовательскими шаблонами или подсказками.

    Args:
        system_template_name (str, optional): Имя системного шаблона.
        system_prompt (str, optional): Системная подсказка.
        user_template_name (str, optional): Имя пользовательского шаблона.
        user_prompt (str, optional): Пользовательская подсказка.
        output_type (type, optional): Ожидаемый тип данных вывода модели.
        **model_params: Дополнительные параметры модели.

    Raises:
        ValueError: Если указаны одновременно шаблон и подсказка, или если не указаны ни шаблон, ни подсказка.
    """
```

#### `call`
```python
def call(self, **rendering_configs) -> any:
    """
    Вызывает языковую модель с указанными конфигурациями рендеринга.

    Args:
        rendering_configs (dict): Конфигурации рендеринга (переменные шаблона) для использования при составлении начальных сообщений.

    Returns:
        any: Содержимое ответа модели.
    """
```

Как работает функция:

1.  Проверяет, заданы ли имена системного и пользовательского шаблонов. Если да, то составляет начальные сообщения LLM, используя шаблоны и конфигурации рендеринга.
2.  Если имена шаблонов не заданы, использует непосредственно предоставленные системные и пользовательские подсказки для составления сообщений.
3.  Если указан тип выходных данных, добавляет в сообщения инструкции по форматированию ответа в виде JSON объекта с полями "value", "justification" и "confidence".
4.  В зависимости от типа выходных данных добавляет конкретные инструкции по формированию значения ("True" или "False" для булевых значений, целое число, число с плавающей точкой или одно из допустимых значений перечисления).
5.  Вызывает языковую модель с сформированными сообщениями и параметрами модели.
6.  Извлекает содержимое ответа модели.
7.  Если указан тип выходных данных, извлекает JSON из ответа, а затем извлекает значение, обоснование и уровень уверенности.
8.  Преобразует значение в соответствующий тип (булево, целое число, число с плавающей точкой или значение перечисления).
9.  Возвращает преобразованное значение.

```
A: Проверка наличия шаблонов имени системы и имени пользователя
|
B: Использовать шаблоны и параметры рендеринга для компоновки сообщений LLM
|
C: Использовать системные и пользовательские подсказки для компоновки сообщений
|
D: Проверка типа вывода
|
E: Включить запрос на вывод JSON
|
F: Укажите тип значения
|
G: Вызвать модель LLM
|
H: Получить содержимое ответа
|
I: Возврат преобразованного значения
```

#### `_coerce_to_bool`
```python
def _coerce_to_bool(self, llm_output: str | bool) -> bool:
    """
    Преобразует вывод LLM в булево значение.

    Args:
        llm_output (str | bool): Вывод LLM для преобразования.

    Returns:
        bool: Булево значение вывода LLM.

    Raises:
        ValueError: Если вывод LLM не содержит распознаваемого булевого значения.
    """
```

#### `_request_bool_llm_message`
```python
def _request_bool_llm_message(self) -> dict:
    """
    Формирует сообщение для запроса булевого значения от LLM.

    Returns:
        dict: Сообщение для запроса булевого значения от LLM.
    """
```

#### `_coerce_to_integer`
```python
def _coerce_to_integer(self, llm_output: str | int) -> int:
    """
    Преобразует вывод LLM в целое число.

    Args:
        llm_output (str | int): Вывод LLM для преобразования.

    Returns:
        int: Целое число вывода LLM.

    Raises:
        ValueError: Если вывод LLM не содержит распознаваемого целого числа.
    """
```

#### `_request_integer_llm_message`
```python
def _request_integer_llm_message(self) -> dict:
    """
    Формирует сообщение для запроса целого числа от LLM.

    Returns:
        dict: Сообщение для запроса целого числа от LLM.
    """
```

#### `_coerce_to_float`
```python
def _coerce_to_float(self, llm_output: str | float) -> float:
    """
    Преобразует вывод LLM в число с плавающей запятой.

    Args:
        llm_output (str | float): Вывод LLM для преобразования.

    Returns:
        float: Число с плавающей запятой вывода LLM.

    Raises:
        ValueError: Если вывод LLM не содержит распознаваемого числа с плавающей запятой.
    """
```

#### `_request_float_llm_message`
```python
def _request_float_llm_message(self) -> dict:
    """
    Формирует сообщение для запроса числа с плавающей запятой от LLM.

    Returns:
        dict: Сообщение для запроса числа с плавающей запятой от LLM.
    """
```

#### `_coerce_to_enumerable`
```python
def _coerce_to_enumerable(self, llm_output: str, options: list) -> str:
    """
    Преобразует вывод LLM в одно из указанных значений перечисления.

    Args:
        llm_output (str): Вывод LLM для преобразования.
        options (list): Список допустимых значений перечисления.

    Returns:
        str: Значение перечисления вывода LLM.

    Raises:
        ValueError: Если вывод LLM не содержит распознаваемого значения перечисления.
    """
```

#### `_request_enumerable_llm_message`
```python
def _request_enumerable_llm_message(self, options: list) -> dict:
    """
    Формирует сообщение для запроса значения перечисления от LLM.

    Args:
        options (list): Список допустимых значений перечисления.

    Returns:
        dict: Сообщение для запроса значения перечисления от LLM.
    """
```

**Примеры**:

Пример создания экземпляра класса `LLMRequest`:

```python
llm_request = LLMRequest(
    system_prompt="You are a helpful assistant.",
    user_prompt="What is the capital of France?",
    output_type=str
)
```

Пример вызова языковой модели:

```python
response = llm_request.call()
print(response)
```

### `LLMScalarWithJustificationResponse`

**Описание**: Класс, представляющий собой типизированный ответ от языковой модели (LLM).

**Принцип работы**: Класс `LLMScalarWithJustificationResponse` определяет структуру данных для представления ответа от языковой модели, который включает в себя значение, обоснование и уровень уверенности.

**Атрибуты**:
- `value` (str | int | float | bool): Значение ответа.
- `justification` (str): Обоснование или объяснение ответа.
- `confidence` (float): Уровень уверенности в ответе.

**Методы**:
- Нет

**Примеры**:

Пример создания экземпляра класса `LLMScalarWithJustificationResponse`:

```python
response = LLMScalarWithJustificationResponse(
    value="Paris",
    justification="Paris is the capital of France.",
    confidence=0.95
)
```

### `OpenAIClient`

**Описание**: Утилитный класс для взаимодействия с OpenAI API.

**Принцип работы**: Класс `OpenAIClient` предоставляет методы для отправки сообщений в OpenAI API, получения эмбеддингов и управления кэшем API-вызовов.

**Атрибуты**:
- `cache_api_calls` (bool): Флаг, указывающий, следует ли кэшировать API-вызовы.
- `cache_file_name` (str): Имя файла для кэширования API-вызовов.
- `api_cache` (dict): Словарь, содержащий кэшированные API-вызовы.
- `client` (OpenAI): Клиент OpenAI API.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `OpenAIClient`.
- `set_api_cache`: Включает или отключает кэширование API-вызовов.
- `send_message`: Отправляет сообщение в OpenAI API и возвращает ответ.
- `get_embedding`: Получает эмбеддинг заданного текста с использованием указанной модели.
- `_setup_from_config`: Настраивает конфигурации OpenAI API для этого клиента.
- `_raw_model_call`: Вызывает OpenAI API с заданными параметрами.
- `_raw_model_response_extractor`: Извлекает ответ из ответа API.
- `_count_tokens`: Подсчитывает количество токенов OpenAI в списке сообщений, используя tiktoken.
- `_save_cache`: Сохраняет кэш API на диск.
- `_load_cache`: Загружает кэш API с диска.
- `_raw_embedding_model_call`: Вызывает OpenAI API для получения эмбеддинга заданного текста.
- `_raw_embedding_model_response_extractor`: Извлекает эмбеддинг из ответа API.

#### `__init__`
```python
def __init__(self, cache_api_calls=default["cache_api_calls"], cache_file_name=default["cache_file_name"]) -> None:
    """
    Инициализирует экземпляр класса `OpenAIClient`.

    Args:
        cache_api_calls (bool, optional): Флаг, указывающий, следует ли кэшировать API-вызовы. По умолчанию `default["cache_api_calls"]`.
        cache_file_name (str, optional): Имя файла для кэширования API-вызовов. По умолчанию `default["cache_file_name"]`.
    """
```

#### `set_api_cache`
```python
def set_api_cache(self, cache_api_calls: bool, cache_file_name: str = default["cache_file_name"]) -> None:
    """
    Включает или отключает кэширование API-вызовов.

    Args:
        cache_api_calls (bool): Флаг, указывающий, следует ли кэшировать API-вызовы.
        cache_file_name (str, optional): Имя файла для кэширования API-вызовов. По умолчанию `default["cache_file_name"]`.
    """
```

#### `send_message`
```python
def send_message(self,
                    current_messages: list,
                     model: str = default["model"],
                     temperature: float = default["temperature"],
                     max_tokens: int = default["max_tokens"],
                     top_p: float = default["top_p"],
                     frequency_penalty: float = default["frequency_penalty"],
                     presence_penalty: float = default["presence_penalty"],
                     stop: list = [],
                     timeout: float = default["timeout"],
                     max_attempts: float = default["max_attempts"],
                     waiting_time: float = default["waiting_time"],
                     exponential_backoff_factor: float = default["exponential_backoff_factor"],
                     n: int = 1,
                     response_format: BaseModel = None,
                     echo: bool = False) -> dict | None:
    """
    Отправляет сообщение в OpenAI API и возвращает ответ.

    Args:
        current_messages (list): Список словарей, представляющих историю разговора.
        model (str, optional): ID модели для использования при создании ответа. По умолчанию `default["model"]`.
        temperature (float, optional): Контролирует "креативность" ответа. Более высокие значения приводят к более разнообразным ответам. По умолчанию `default["temperature"]`.
        max_tokens (int, optional): Максимальное количество токенов (слов или знаков препинания) для создания в ответе. По умолчанию `default["max_tokens"]`.
        top_p (float, optional): Контролирует "качество" ответа. Более высокие значения приводят к более связным ответам. По умолчанию `default["top_p"]`.
        frequency_penalty (float, optional): Контролирует "повторение" ответа. Более высокие значения приводят к меньшему повторению. По умолчанию `default["frequency_penalty"]`.
        presence_penalty (float, optional): Контролирует "разнообразие" ответа. Более высокие значения приводят к более разнообразным ответам. По умолчанию `default["presence_penalty"]`.
        stop (list, optional): Строка, которая, если встречается в сгенерированном ответе, приводит к остановке генерации. По умолчанию `[]`.
        timeout (float, optional): Максимальное количество секунд ожидания ответа от API. По умолчанию `default["timeout"]`.
        max_attempts (float, optional): Максимальное количество попыток, прежде чем отказаться от создания ответа. По умолчанию `default["max_attempts"]`.
        waiting_time (float, optional): Количество секунд ожидания между запросами. По умолчанию `default["waiting_time"]`.
        exponential_backoff_factor (float, optional): Фактор, на который увеличивается время ожидания между запросами. По умолчанию `default["exponential_backoff_factor"]`.
        n (int, optional): Количество завершений для создания. По умолчанию 1.
        response_format (BaseModel, optional): Формат ответа, если есть. По умолчанию `None`.
        echo (bool, optional):  По умолчанию `False`.

    Returns:
        dict | None: Словарь, представляющий сгенерированный ответ, или `None` в случае ошибки.
    """
```

Как работает функция:

1.  Определяет внутреннюю функцию `aux_exponential_backoff`, которая увеличивает время ожидания между запросами в случае ошибки.
2.  Вызывает метод `_setup_from_config` для настройки конфигураций OpenAI API.
3.  Создает словарь `chat_api_params` с параметрами для вызова API чата.
4.  Если указан формат ответа, добавляет его в `chat_api_params`.
5.  Запускает цикл, который повторяет попытки отправки сообщения в API до тех пор, пока не будет достигнуто максимальное количество попыток или не будет получен успешный ответ.
6.  Внутри цикла:
    *   Увеличивает счетчик попыток.
    *   Выводит отладочное сообщение с количеством токенов в текущем сообщении (если подсчет токенов реализован для используемой модели).
    *   Замеряет время начала запроса.
    *   Формирует ключ кэша на основе параметров запроса.
    *   Если кэширование включено и ключ есть в кэше, извлекает ответ из кэша.
    *   В противном случае:
        *   Если время ожидания между запросами больше 0, ждет указанное время.
        *   Вызывает метод `_raw_model_call` для отправки запроса в API.
        *   Если кэширование включено, сохраняет ответ в кэше.
    *   Замеряет время окончания запроса.
    *   Выводит отладочное сообщение с информацией о времени выполнения запроса.
    *   Вызывает метод `_raw_model_response_extractor` для извлечения ответа из ответа API.
    *   Очищает ответ от потенциально опасных данных с помощью `utils.sanitize_dict`.
    *   Возвращает очищенный ответ.
7.  Обрабатывает возможные исключения:
    *   `InvalidRequestError` и `openai.BadRequestError`: выводят сообщение об ошибке и возвращают `None`.
    *   `openai.RateLimitError`: выводят предупреждение и вызывают `aux_exponential_backoff` для увеличения времени ожидания.
    *   `NonTerminalError`: выводят сообщение об ошибке и вызывают `aux_exponential_backoff`.
    *   `Exception`: выводят сообщение об ошибке.
8.  Если после всех попыток не удалось получить ответ, выводят сообщение об ошибке и возвращают `None`.

```
A: Настройка параметров для вызова API
|
B: Проверка, существует ли формат ответа
|
C: Добавить формат ответа в параметры API
|
D: Вызвать API
|
E: Обработка и возврат ответа
|
F: Обработка исключений
|
G: Вернуть None после нескольких попыток
```

#### `get_embedding`
```python
def get_embedding(self, text: str, model: str = default["embedding_model"]) -> list:
    """
    Получает эмбеддинг заданного текста с использованием указанной модели.

    Args:
        text (str): Текст для эмбеддинга.
        model (str, optional): Имя модели для использования при эмбеддинге текста. По умолчанию `default["embedding_model"]`.

    Returns:
        list: Эмбеддинг текста.
    """
```

#### `_setup_from_config`
```python
def _setup_from_config(self) -> None:
    """
    Настраивает конфигурации OpenAI API для этого клиента.
    """
```

#### `_raw_model_call`
```python
def _raw_model_call(self, model: str, chat_api_params: dict) -> dict:
    """
    Вызывает OpenAI API с заданными параметрами. Подклассы должны
    переопределить этот метод для реализации собственных вызовов API.

    Args:
        model (str): ID модели для использования при вызове API.
        chat_api_params (dict): Словарь параметров для вызова API.

    Returns:
        dict: Ответ от API.
    """
```

#### `_raw_model_response_extractor`
```python
def _raw_model_response_extractor(self, response: dict) -> dict:
    """
    Извлекает ответ из ответа API. Подклассы должны
    переопределить этот метод для реализации собственного извлечения ответа.

    Args:
        response (dict): Ответ от API.

    Returns:
        dict: Извлеченный ответ.
    """
```

#### `_count_tokens`
```python
def _count_tokens(self, messages: list, model: str) -> int | None:
    """
    Подсчитывает количество токенов OpenAI в списке сообщений, используя tiktoken.

    Args:
        messages (list): Список словарей, представляющих историю разговора.
        model (str): Имя модели для использования при кодировании строки.

    Returns:
        int | None: Количество токенов или `None` в случае ошибки.
    """
```

#### `_save_cache`
```python
def _save_cache(self) -> None:
    """
    Сохраняет кэш API на диск. Мы используем pickle для этого, потому что некоторые объекты
    не сериализуемы в JSON.
    """
```

#### `_load_cache`
```python
def _load_cache(self) -> dict:
    """
    Загружает кэш API с диска.
    """
```

#### `_raw_embedding_model_call`
```python
def _raw_embedding_model_call(self, text: str, model: str) -> dict:
    """
    Вызывает OpenAI API для получения эмбеддинга заданного текста. Подклассы должны
    переопределить этот метод для реализации собственных вызовов API.

    Args:
        text (str): Текст для эмбеддинга.
        model (str): Имя модели для использования при эмбеддинге текста.

    Returns:
        dict: Ответ от API.
    """
```

#### `_raw_embedding_model_response_extractor`
```python
def _raw_embedding_model_response_extractor(self, response: dict) -> list:
    """
    Извлекает эмбеддинг из ответа API. Подклассы должны
    переопределить этот метод для реализации собственного извлечения ответа.

    Args:
        response (dict): Ответ от API.

    Returns:
        list: Извлеченный эмбеддинг.
    """
```

**Примеры**:

Пример создания экземпляра класса `OpenAIClient`:

```python
client = OpenAIClient(cache_api_calls=True)
```

Пример отправки сообщения в OpenAI API:

```python
messages = [{"role": "user", "content": "What is the capital of France?"}]
response = client.send_message(messages)
print(response)
```

Пример получения эмбеддинга текста:

```python
text = "This is a sample text."
embedding = client.get_embedding(text)
print(embedding)
```

### `AzureClient`

**Описание**: Подкласс класса `OpenAIClient` для взаимодействия с Azure OpenAI Service API.

**Принцип работы**: Класс `AzureClient` наследует функциональность класса `OpenAIClient` и переопределяет метод `_setup_from_config` для настройки конфигураций Azure OpenAI Service API.

**Атрибуты**:
- Все атрибуты класса `OpenAIClient`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AzureClient`.
- `_setup_from_config`: Настраивает конфигурации Azure OpenAI Service API для этого клиента.

#### `__init__`
```python
def __init__(self, cache_api_calls=default["cache_api_calls"], cache_file_name=default["cache_file_name"]) -> None:
    """
    Инициализирует экземпляр класса `AzureClient`.

    Args:
        cache_api_calls (bool, optional): Флаг, указывающий, следует ли кэшировать API-вызовы. По умолчанию `default["cache_api_calls"]`.
        cache_file_name (str, optional): Имя файла для кэширования API-вызовов. По умолчанию `default["cache_file_name"]`.
    """
```

#### `_setup_from_config`
```python
def _setup_from_config(self) -> None:
    """
    Настраивает конфигурации Azure OpenAI Service API для этого клиента,
    включая конечную точку API и ключ.
    """
```

**Примеры**:

Пример создания экземпляра класса `AzureClient`:

```python
client = AzureClient(cache_api_calls=True)
```

## Исключения

### `InvalidRequestError`

**Описание**: Исключение, которое выбрасывается, когда запрос к OpenAI API является недействительным.

### `NonTerminalError`

**Описание**: Исключение, которое выбрасывается, когда происходит неуказанная ошибка, но мы знаем, что можно повторить попытку.

## Функции

### `register_client`

```python
def register_client(api_type: str, client: OpenAIClient | AzureClient) -> None:
    """
    Регистрирует клиент для заданного типа API.

    Args:
        api_type (str): Тип API, для которого мы хотим зарегистрировать клиент.
        client (OpenAIClient | AzureClient): Клиент для регистрации.
    """
```

### `_get_client_for_api_type`

```python
def _get_client_for_api_type(api_type: str) -> OpenAIClient | AzureClient:
    """
    Возвращает клиент для заданного типа API.

    Args:
        api_type (str): Тип API, для которого мы хотим получить клиент.

    Returns:
        OpenAIClient | AzureClient: Клиент для заданного типа API.

    Raises:
        ValueError: Если тип API не поддерживается.
    """
```

### `client`

```python
def client() -> OpenAIClient | AzureClient:
    """
    Возвращает клиент для настроенного типа API.
    """
```

### `force_api_type`

```python
def force_api_type(api_type: str) -> None:
    """
    Принудительно использует заданный тип API, таким образом переопределяя любую другую конфигурацию.

    Args:
        api_type (str): Тип API для использования.
    """
```

### `force_api_cache`

```python
def force_api_cache(cache_api_calls: bool, cache_file_name: str = default["cache_file_name"]) -> None:
    """
    Принудительно использует заданную конфигурацию кэша API, таким образом переопределяя любую другую конфигурацию.

    Args:
        cache_api_calls (bool): Следует ли кэшировать вызовы API.
        cache_file_name (str, optional): Имя файла для использования для кэширования вызовов API. По умолчанию `default["cache_file_name"]`.
    """
```
```
def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    """ Функция выполняет некоторое действия... <Тут Ты пишешь что именно делает функция> 
    Args:
        param (str): Описание параметра `param`.
        param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.

    Returns:
        dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.

    Raises:
        SomeError: Описание ситуации, в которой возникает исключение `SomeError`.
       ...
       <Выводить тело функции НЕ НАДО. Только docstring>
    """
    def inner_function():
       """ Внутрняя функция Функция выполняет некоторое действия... <Тут Ты пишешь что именно делает функция> 
           Args:
               param (str): Описание параметра `param`.
               param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.

           Returns:
               dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.

           Raises:
               SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

           ...
         
             НЕ ВЫВОДИ КОД ФУНКЦИИ. ТОЛЬКО DOCSTR

           """