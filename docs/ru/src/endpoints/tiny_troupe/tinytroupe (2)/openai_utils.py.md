# Модуль для работы с OpenAI API
## Обзор

Модуль `openai_utils.py` предназначен для взаимодействия с API OpenAI и Azure OpenAI. Он содержит классы для отправки запросов к моделям, обработки ответов и управления кэшированием API-вызовов. Модуль также включает вспомогательные функции для работы с текстом и токенами, а также определения исключений для обработки ошибок при работе с API.

## Подробнее

Этот модуль предоставляет инструменты для упрощения взаимодействия с API OpenAI, включая:

-   Управление конфигурацией через файл `config.ini`.
-   Кэширование API-вызовов для повышения производительности и снижения затрат.
-   Автоматическое преобразование типов данных в ответах от API.
-   Обработка ошибок и повторные попытки при сбоях API.
-   Поддержка различных моделей OpenAI и Azure OpenAI.

## Классы

### `LLMRequest`

Описание класса для представления запроса к языковой модели (LLM). Он содержит входные сообщения, конфигурацию модели и вывод модели.
**Атрибуты**:
-   `system_template_name` (str, optional): Имя системного шаблона.
-   `user_template_name` (str, optional): Имя пользовательского шаблона.
-   `system_prompt` (str, optional): Системный промпт.
-   `user_prompt` (str, optional): Пользовательский промпт.
-   `output_type` (type, optional): Тип ожидаемого вывода.
-   `model_params` (dict): Параметры модели.
-   `model_output` (Any): Вывод модели.
-   `messages` (list): Список сообщений для отправки в модель.
-   `response_raw` (str): Необработанный ответ от модели.
-   `response_json` (dict): Ответ от модели в формате JSON.
-   `response_value` (Any): Значение ответа от модели.
-   `response_justification` (str): Обоснование ответа от модели.
-   `response_confidence` (float): Уровень уверенности в ответе от модели.

**Методы**:

-   `__init__(self, system_template_name: str = None, system_prompt: str = None, user_template_name: str = None, user_prompt: str = None, output_type = None, \*\*model_params)`

    ```python
    def __init__(self, system_template_name:str=None, system_prompt:str=None,
                     user_template_name:str=None, user_prompt:str=None,
                     output_type=None,
                     **model_params) -> None:
        """
        Инициализирует экземпляр LLMCall с указанными системными и пользовательскими шаблонами или системными и пользовательскими подсказками.
        Если указан шаблон, соответствующая подсказка должна быть None, и наоборот.

        Args:
            system_template_name (str, optional): Имя системного шаблона.
            system_prompt (str, optional): Системный промпт.
            user_template_name (str, optional): Имя пользовательского шаблона.
            user_prompt (str, optional): Пользовательский промпт.
            output_type (type, optional): Тип ожидаемого вывода.
            **model_params: Дополнительные параметры модели.

        Raises:
            ValueError: Если указаны одновременно шаблон и промпт, или если не указаны ни шаблон, ни промпт.
        """
    ```

-   `call(self, \*\*rendering_configs)`

    ```python
    def call(self, **rendering_configs) -> Any:
        """
        Вызывает модель LLM с указанными конфигурациями рендеринга.
        Args:
            rendering_configs: Конфигурации рендеринга (переменные шаблона), используемые при составлении начальных сообщений.

        Returns:
            content: Содержимое ответа модели.
        """
    ```

-   `_coerce_to_bool(self, llm_output: str | bool) -> bool`

    ```python
    def _coerce_to_bool(self, llm_output: str | bool) -> bool:
        """
        Приводит вывод LLM к логическому значению.

        Этот метод ищет строку "True", "False", "Yes", "No", "Positive", "Negative" в выводе LLM, так что
          - регистр нейтрализуется;
          - учитывается первое вхождение строки, остальное игнорируется. Например, " Yes, that is true" будет считаться "Yes";
          - если такая строка не найдена, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали логическое значение.

        Args:
            llm_output (str, bool): Вывод LLM для приведения.

        Returns:
            bool: Логическое значение вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого логического значения.
        """
    ```

-   `_request_bool_llm_message(self) -> dict`

    ```python
    def _request_bool_llm_message(self) -> dict:
        """
        Формирует сообщение для запроса логического значения от LLM.

        Returns:
            dict: Словарь, содержащий сообщение для запроса логического значения.
        """
    ```

-   `_coerce_to_integer(self, llm_output: str) -> int`

    ```python
    def _coerce_to_integer(self, llm_output: str) -> int:
        """
        Приводит вывод LLM к целочисленному значению.

        Этот метод ищет первое вхождение целого числа в выводе LLM, так что
          - учитывается первое вхождение целого числа, остальное игнорируется. Например, "There are 3 cats" будет считаться 3;
          - если целое число не найдено, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали целочисленное значение.

        Args:
            llm_output (str, int): Вывод LLM для приведения.

        Returns:
            int: Целочисленное значение вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого целочисленного значения.
        """
    ```

-   `_request_integer_llm_message(self) -> dict`

    ```python
    def _request_integer_llm_message(self) -> dict:
        """
        Формирует сообщение для запроса целочисленного значения от LLM.

        Returns:
            dict: Словарь, содержащий сообщение для запроса целочисленного значения.
        """
    ```

-   `_coerce_to_float(self, llm_output: str) -> float`

    ```python
    def _coerce_to_float(self, llm_output: str) -> float:
        """
        Приводит вывод LLM к значению с плавающей точкой.

        Этот метод ищет первое вхождение числа с плавающей точкой в выводе LLM, так что
          - учитывается первое вхождение числа с плавающей точкой, остальное игнорируется. Например, "The price is $3.50" будет считаться 3.50;
          - если число с плавающей точкой не найдено, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали значение с плавающей точкой.

        Args:
            llm_output (str, float): Вывод LLM для приведения.

        Returns:
            float: Значение с плавающей точкой вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого значения с плавающей точкой.
        """
    ```

-   `_request_float_llm_message(self) -> dict`

    ```python
    def _request_float_llm_message(self) -> dict:
        """
        Формирует сообщение для запроса значения с плавающей точкой от LLM.

        Returns:
            dict: Словарь, содержащий сообщение для запроса значения с плавающей точкой.
        """
    ```

-   `_coerce_to_enumerable(self, llm_output: str, options: list) -> str`

    ```python
    def _coerce_to_enumerable(self, llm_output: str, options: list) -> str:
        """
        Приводит вывод LLM к одному из указанных вариантов.

        Этот метод ищет первое вхождение одного из указанных вариантов в выводе LLM, так что
          - учитывается первое вхождение варианта, остальное игнорируется. Например, "I prefer cats" будет считаться "cats";
          - если вариант не найден, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали один из указанных вариантов.

        Args:
            llm_output (str): Вывод LLM для приведения.
            options (list): Список вариантов для рассмотрения.

        Returns:
            str: Значение варианта вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого значения варианта.
        """
    ```

-   `_request_enumerable_llm_message(self, options: list) -> dict`

    ```python
    def _request_enumerable_llm_message(self, options: list) -> dict:
        """
        Формирует сообщение для запроса одного из указанных вариантов от LLM.

        Args:
            options (list): Список допустимых вариантов.

        Returns:
            dict: Словарь, содержащий сообщение для запроса одного из указанных вариантов.
        """
    ```

-   `__repr__(self) -> str`

    ```python
    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта LLMRequest.

        Returns:
            str: Строковое представление объекта LLMRequest.
        """
    ```

### `LLMScalarWithJustificationResponse`

```python
class LLMScalarWithJustificationResponse(BaseModel):
    """
    LLMTypedResponse представляет типизированный ответ от LLM (Language Learning Model).
    Attributes:
        value (str, int, float, list): Значение ответа.
        justification (str): Обоснование или объяснение ответа.
    """
    value: Union[str, int, float, bool]
    justification: str
    confidence: float
```

Описание структуры данных для представления типизированного ответа от языковой модели с обоснованием и уровнем уверенности.

**Атрибуты**:
-   `value` (str | int | float | bool): Значение ответа.
-   `justification` (str): Обоснование или объяснение ответа.
-   `confidence` (float): Уровень уверенности в ответе.

### `OpenAIClient`

Описание класса для взаимодействия с API OpenAI.

**Атрибуты**:
-   `cache_api_calls` (bool): Флаг, указывающий, следует ли кэшировать API-вызовы.
-   `cache_file_name` (str): Имя файла для кэширования API-вызовов.
-   `api_cache` (dict): Словарь для хранения кэшированных API-вызовов.
-   `client` (openai.OpenAI): Клиент OpenAI.

**Методы**:

-   `__init__(self, cache_api_calls=default["cache_api_calls"], cache_file_name=default["cache_file_name"])`

    ```python
    def __init__(self, cache_api_calls=default["cache_api_calls"], cache_file_name=default["cache_file_name"]) -> None:
        """
        Инициализирует клиент OpenAI.

        Args:
            cache_api_calls (bool): Следует ли кэшировать вызовы API.
            cache_file_name (str): Имя файла для кэширования.
        """
    ```

-   `set_api_cache(self, cache_api_calls: bool, cache_file_name: str = default["cache_file_name"]) -> None`

    ```python
    def set_api_cache(self, cache_api_calls: bool, cache_file_name: str = default["cache_file_name"]) -> None:
        """
        Включает или отключает кэширование API-вызовов.

        Args:
            cache_api_calls (bool): Включать ли кэширование.
            cache_file_name (str): Имя файла для кэширования.
        """
    ```

-   `_setup_from_config(self) -> None`

    ```python
    def _setup_from_config(self) -> None:
        """
        Настраивает конфигурации API OpenAI для этого клиента.
        """
    ```

-   `send_message(self, current_messages: list, model: str = default["model"], temperature: float = default["temperature"], max_tokens: int = default["max_tokens"], top_p: float = default["top_p"], frequency_penalty: float = default["frequency_penalty"], presence_penalty: float = default["presence_penalty"], stop: list = [], timeout: float = default["timeout"], max_attempts: float = default["max_attempts"], waiting_time: float = default["waiting_time"], exponential_backoff_factor: float = default["exponential_backoff_factor"], n: int = 1, response_format = None, echo: bool = False) -> Union[dict, None]`

    ```python
    def send_message(self,
                    current_messages: list,
                     model=default["model"],
                     temperature=default["temperature"],
                     max_tokens=default["max_tokens"],
                     top_p=default["top_p"],
                     frequency_penalty=default["frequency_penalty"],
                     presence_penalty=default["presence_penalty"],
                     stop=[],
                     timeout=default["timeout"],
                     max_attempts=default["max_attempts"],
                     waiting_time=default["waiting_time"],
                     exponential_backoff_factor=default["exponential_backoff_factor"],
                     n = 1,
                     response_format=None,
                     echo=False) -> dict | None:
        """
        Отправляет сообщение в API OpenAI и возвращает ответ.

        Args:
            current_messages (list): Список словарей, представляющих историю разговора.
            model (str): ID модели, используемой для генерации ответа.
            temperature (float): Управляет "креативностью" ответа. Более высокие значения приводят к более разнообразным ответам.
            max_tokens (int): Максимальное количество токенов (слов или знаков препинания) для генерации в ответе.
            top_p (float): Управляет "качеством" ответа. Более высокие значения приводят к более связным ответам.
            frequency_penalty (float): Управляет "повторением" ответа. Более высокие значения приводят к меньшему повторению.
            presence_penalty (float): Управляет "разнообразием" ответа. Более высокие значения приводят к более разнообразным ответам.
            stop (str): Строка, которая, если она встречается в сгенерированном ответе, приведет к остановке генерации.
            max_attempts (int): Максимальное количество попыток, прежде чем отказаться от генерации ответа.
            timeout (int): Максимальное количество секунд ожидания ответа от API.
            waiting_time (int): Количество секунд ожидания между запросами.
            exponential_backoff_factor (int): Фактор, на который увеличивается время ожидания между запросами.
            n (int): Количество завершений для генерации.
            response_format: Формат ответа, если есть.

        Returns:
            dict: Словарь, представляющий сгенерированный ответ.
        """
    ```

    **Внутренние функции**:

    -   `aux_exponential_backoff()`

        ```python
        def aux_exponential_backoff():
            nonlocal waiting_time

            # если время ожидания было изначально установлено на 0
            if waiting_time <= 0:
                waiting_time = 2

            logger.info(f"Запрос не удался. Ожидание {waiting_time} секунд между запросами...")
            time.sleep(waiting_time)

            # экспоненциальное увеличение времени ожидания
            waiting_time = waiting_time * exponential_backoff_factor
        ```

        Внутренняя функция `aux_exponential_backoff` используется для экспоненциального увеличения времени ожидания между повторными запросами к API в случае ошибки. Она увеличивает переменную `waiting_time` на `exponential_backoff_factor` после каждой неудачной попытки.

-   `_raw_model_call(self, model: str, chat_api_params: dict) -> Any`

    ```python
    def _raw_model_call(self, model: str, chat_api_params: dict) -> Any:
        """
        Вызывает API OpenAI с заданными параметрами. Подклассы должны
        переопределить этот метод, чтобы реализовать свои собственные вызовы API.
        """
    ```

-   `_raw_model_response_extractor(self, response: dict) -> dict`

    ```python
    def _raw_model_response_extractor(self, response: dict) -> dict:
        """
        Извлекает ответ из ответа API. Подклассы должны
        переопределить этот метод, чтобы реализовать свои собственные извлечения ответов.
        """
    ```

-   `_count_tokens(self, messages: list, model: str) -> Union[int, None]`

    ```python
    def _count_tokens(self, messages: list, model: str) -> int | None:
        """
        Подсчитывает количество токенов OpenAI в списке сообщений с использованием tiktoken.

        Адаптировано из https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

        Args:
            messages (list): Список словарей, представляющих историю разговора.
            model (str): Название модели, используемой для кодирования строки.
        """
    ```

-   `_save_cache(self) -> None`

    ```python
    def _save_cache(self) -> None:
        """
        Сохраняет кэш API на диск. Мы используем pickle для этого, потому что некоторые объекты
        не сериализуемы в JSON.
        """
    ```

-   `_load_cache(self) -> dict`

    ```python
    def _load_cache(self) -> dict:
        """
        Загружает кэш API с диска.
        """
    ```

-   `get_embedding(self, text: str, model: str = default["embedding_model"]) -> list`

    ```python
    def get_embedding(self, text: str, model: str = default["embedding_model"]) -> list:
        """
        Получает векторное представление заданного текста с использованием указанной модели.

        Args:
            text (str): Текст для получения векторного представления.
            model (str): Название модели, используемой для получения векторного представления текста.

        Returns:
            list: Векторное представление текста.
        """
    ```

-   `_raw_embedding_model_call(self, text: str, model: str) -> Any`

    ```python
    def _raw_embedding_model_call(self, text: str, model: str) -> Any:
        """
        Вызывает API OpenAI для получения векторного представления заданного текста. Подклассы должны
        переопределить этот метод, чтобы реализовать свои собственные вызовы API.
        """
    ```

-   `_raw_embedding_model_response_extractor(self, response: dict) -> list`

    ```python
    def _raw_embedding_model_response_extractor(self, response: dict) -> list:
        """
        Извлекает векторное представление из ответа API. Подклассы должны
        переопределить этот метод, чтобы реализовать свои собственные извлечения ответов.
        """
    ```

### `AzureClient(OpenAIClient)`

Описание класса для взаимодействия с API Azure OpenAI Service, наследуется от `OpenAIClient`.

**Наследует**:
-   `OpenAIClient`: Этот класс наследует функциональность базового клиента OpenAI и расширяет её для работы с Azure OpenAI Service.

**Методы**:
-   `__init__(self, cache_api_calls=default["cache_api_calls"], cache_file_name=default["cache_file_name"])`

    ```python
    def __init__(self, cache_api_calls=default["cache_api_calls"], cache_file_name=default["cache_file_name"]) -> None:
        """
        Инициализирует клиент Azure.
        Args:
            cache_api_calls (bool): Нужно ли кэшировать вызовы API.
            cache_file_name (str): Имя файла для кэширования.
        """
    ```

-   `_setup_from_config(self)`

    ```python
    def _setup_from_config(self):
        """
        Настраивает конфигурации API Azure OpenAI Service для этого клиента,
        включая конечную точку API и ключ.
        """
    ```

## Исключения

### `InvalidRequestError`

```python
class InvalidRequestError(Exception):
    """
    Исключение, возникающее, когда запрос к API OpenAI недействителен.
    """
    pass
```

Описание исключения, которое выбрасывается при недействительном запросе к API OpenAI.

### `NonTerminalError`

```python
class NonTerminalError(Exception):
    """
    Исключение, возникающее, когда происходит неуказанная ошибка, но мы знаем, что можем повторить попытку.
    """
    pass
```

Описание исключения, которое выбрасывается, когда происходит неуказанная ошибка, но можно повторить попытку.

## Функции

### `register_client(api_type: str, client: object) -> None`

```python
def register_client(api_type: str, client: object) -> None:
    """
    Регистрирует клиент для заданного типа API.

    Args:
        api_type (str): Тип API, для которого мы хотим зарегистрировать клиент.
        client (object): Клиент для регистрации.
    """
```

Регистрирует клиент для указанного типа API.

### `_get_client_for_api_type(api_type: str) -> object`

```python
def _get_client_for_api_type(api_type: str) -> object:
    """
    Возвращает клиент для заданного типа API.

    Args:
        api_type (str): Тип API, для которого мы хотим получить клиент.
    """
```

Возвращает клиент для указанного типа API.

### `client() -> object`

```python
def client() -> object:
    """
    Возвращает клиент для настроенного типа API.
    """
```

Возвращает клиент для настроенного типа API.

### `force_api_type(api_type: str) -> None`

```python
def force_api_type(api_type: str) -> None:
    """
    Принудительно использует заданный тип API, тем самым переопределяя любую другую конфигурацию.

    Args:
        api_type (str): Тип API для использования.
    """
```

Принудительно устанавливает использование указанного типа API, переопределяя любую другую конфигурацию.

### `force_api_cache(cache_api_calls: bool, cache_file_name: str = default["cache_file_name"]) -> None`

```python
def force_api_cache(cache_api_calls: bool, cache_file_name: str = default["cache_file_name"]) -> None:
    """
    Принудительно использует заданную конфигурацию кэша API, тем самым переопределяя любую другую конфигурацию.

    Args:
        cache_api_calls (bool): Следует ли кэшировать вызовы API.
        cache_file_name (str): Имя файла для использования для кэширования вызовов API.
    """
```

Принудительно устанавливает конфигурацию кэша API, переопределяя другие настройки.

## Примеры

### Использование `LLMRequest`

```python
llm_request = LLMRequest(
    system_prompt="You are a helpful assistant.",
    user_prompt="What is the capital of France?",
    model_params={"model": "gpt-3.5-turbo"}
)
response = llm_request.call()
print(response)  # Вывод: Paris
```

### Использование `OpenAIClient`

```python
client = OpenAIClient()
messages = [{"role": "user", "content": "Hello!"}]
response = client.send_message(messages)
print(response)  # Вывод: {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}