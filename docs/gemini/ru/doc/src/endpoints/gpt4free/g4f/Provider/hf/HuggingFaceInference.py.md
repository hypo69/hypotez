# Модуль HuggingFaceInference

## Обзор

Модуль `HuggingFaceInference` предоставляет класс `HuggingFaceInference`, который является асинхронным генератором для взаимодействия с моделями Hugging Face Inference API. Он поддерживает как текстовые, так и графические модели.

## Подробней

Этот модуль позволяет использовать модели Hugging Face для генерации текста и изображений, а также предоставляет инструменты для форматирования запросов и обработки ответов. Он интегрируется с `StreamSession` для асинхронной потоковой передачи данных.

## Классы

### `HuggingFaceInference`

**Описание**: Класс `HuggingFaceInference` является асинхронным генератором и миксином для работы с моделями Hugging Face Inference API.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL Hugging Face.
- `parent` (str): Название родительского провайдера ("HuggingFace").
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель по умолчанию.
- `default_image_model` (str): Модель для генерации изображений по умолчанию.
- `model_aliases` (dict): Алиасы моделей.
- `image_models` (list): Список моделей для генерации изображений.
- `model_data` (dict[str, dict]): Кэш данных моделей.

**Методы**:
- `get_models()`: Возвращает список поддерживаемых моделей.
- `get_model_data(session: StreamSession, model: str) -> str`: Получает данные о модели из API Hugging Face.
- `create_async_generator(...)`: Создает асинхронный генератор для выполнения запросов к API Hugging Face.

### `get_models`

```python
@classmethod
def get_models(cls) -> list[str]:
    """
    Возвращает список поддерживаемых моделей.

    Args:
        cls (HuggingFaceInference): Класс HuggingFaceInference.

    Returns:
        list[str]: Список поддерживаемых моделей.

    Как работает функция:
    1. Проверяет, инициализирован ли уже список моделей (`cls.models`).
    2. Если список моделей пуст, создает его, начиная с копии `text_models`.
    3. Запрашивает дополнительные текстовые модели с API Hugging Face, фильтруя их по популярности (`trendingScore` >= 10).
    4. Добавляет полученные модели в общий список, сохраняя уникальность и порядок.
    5. Аналогично получает и добавляет модели для генерации изображений.
    6. Сохраняет полученный список в `cls.models` и возвращает его.

    ASCII flowchart:
    A: Проверка `cls.models`
    |
    B: Создание списка моделей (текстовые)
    |
    C: Запрос дополнительных текстовых моделей
    |
    D: Фильтрация по `trendingScore`
    |
    E: Добавление моделей в список
    |
    F: Запрос моделей для генерации изображений
    |
    G: Фильтрация по `trendingScore`
    |
    H: Добавление моделей в список
    |
    I: Сохранение и возврат списка

    Примеры:
        >>> HuggingFaceInference.get_models()
        ['model1', 'model2', ...]
    """
    ...
```

### `get_model_data`

```python
    @classmethod
    async def get_model_data(cls, session: StreamSession, model: str) -> str:
        """
        Получает данные о модели из API Hugging Face.

        Args:
            cls (HuggingFaceInference): Класс HuggingFaceInference.
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            model (str): Название модели.

        Returns:
            str: Данные о модели в формате JSON.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.

        Как работает функция:
        1. Проверяет, есть ли данные о модели в кэше (`cls.model_data`). Если есть, возвращает их.
        2. Если данных в кэше нет, выполняет запрос к API Hugging Face для получения информации о модели.
        3. Обрабатывает ошибку 404, выбрасывая исключение `ModelNotSupportedError`, если модель не найдена.
        4. Сохраняет полученные данные в кэше `cls.model_data` и возвращает их.

        ASCII flowchart:
        A: Проверка наличия данных в `cls.model_data`
        |
        B: Выполнение запроса к API Hugging Face
        |
        C: Обработка ошибки 404
        |
        D: Сохранение данных в `cls.model_data` и возврат

        Примеры:
            >>> import asyncio
            >>> from aiohttp import ClientSession
            >>> async def get_data():
            ...     async with ClientSession() as session:
            ...         data = await HuggingFaceInference.get_model_data(StreamSession(session=session), "gpt2")
            ...         print(data)
            >>> asyncio.run(get_data())
            {'model': 'gpt2', ...}
        """
    ...
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        timeout: int = 600,
        api_base: str = "https://api-inference.huggingface.co",
        api_key: str = None,
        max_tokens: int = 1024,
        temperature: float = None,
        prompt: str = None,
        action: str = None,
        extra_data: dict = {},
        seed: int = None,
        aspect_ratio: str = None,
        width: int = None,
        height: int = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для выполнения запросов к API Hugging Face.

        Args:
            cls (HuggingFaceInference): Класс HuggingFaceInference.
            model (str): Название модели.
            messages (Messages): Список сообщений для передачи в модель.
            stream (bool): Флаг, указывающий на использование потоковой передачи данных.
            proxy (str): Прокси-сервер для использования.
            timeout (int): Время ожидания запроса в секундах.
            api_base (str): Базовый URL API Hugging Face.
            api_key (str): API ключ для аутентификации.
            max_tokens (int): Максимальное количество токенов в ответе.
            temperature (float): Температура для генерации текста.
            prompt (str): Дополнительный промпт для генерации изображений.
            action (str): Действие (например, "continue").
            extra_data (dict): Дополнительные данные для передачи в модель.
            seed (int): Зерно для генерации случайных чисел (для воспроизводимости).
            aspect_ratio (str): Соотношение сторон для генерации изображений.
            width (int): Ширина изображения.
            height (int): Высота изображения.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор для получения результатов.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
            ResponseError: Если произошла ошибка при получении ответа от API.

        Как работает функция:
        1. Определяет параметры запроса, включая заголовки и полезную нагрузку (payload), в зависимости от типа модели (текстовая или графическая).
        2. Выполняет POST-запрос к API Hugging Face с использованием `StreamSession`.
        3. Для потоковых текстовых моделей:
           - Читает ответ построчно.
           - Извлекает текст из JSON-ответа.
           - Удаляет начальные пробелы из первого чанка.
           - Генерирует чанки текста.
           - Обрабатывает специальные токены, определяя причину завершения генерации.
        4. Для графических моделей:
           - Сохраняет полученные изображения.
           - Генерирует URL изображений.

        ASCII flowchart:
        A: Определение параметров запроса
        |
        B: Выполнение POST-запроса к API
        |
        C: Проверка типа модели (текст/изображение)
        |
        D: Обработка потокового ответа (текст)
        |
        E: Извлечение текста из JSON
        |
        F: Генерация чанков текста
        |
        G: Обработка специальных токенов
        |
        H: Сохранение изображений (изображение)
        |
        I: Генерация URL изображений

        Примеры:
            Примеры использования этой функции требуют настройки асинхронной среды и, следовательно, не могут быть выполнены непосредственно в документации.
        """
    ...
```

## Функции

### `format_prompt_mistral`

```python
def format_prompt_mistral(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Mistral.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на продолжение предыдущего разговора.

    Returns:
        str: Отформатированный промпт.

    Как работает функция:
    1. Извлекает системные сообщения из списка `messages`.
    2. Формирует вопрос, объединяя последнее сообщение пользователя и системные сообщения.
    3. Создает историю разговора, форматируя каждое сообщение пользователя и ассистента в определенный формат.
    4. Если `do_continue` равен `True`, обрезает последний тег `</s>` из истории.
    5. Возвращает отформатированный промпт.

    ASCII flowchart:
    A: Извлечение системных сообщений
    |
    B: Формирование вопроса
    |
    C: Создание истории разговора
    |
    D: Проверка `do_continue`
    |
    E: Обрезка последнего тега (если `do_continue`)
    |
    F: Возврат отформатированного промпта

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        >>> format_prompt_mistral(messages)
        '<s>[INST]Hello [/INST] Hi</s>\\n<s>[INST] Hello [/INST]'
    """
    ...
```

### `format_prompt_qwen`

```python
def format_prompt_qwen(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Qwen.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на продолжение предыдущего разговора.

    Returns:
        str: Отформатированный промпт.

    Как работает функция:
    1. Объединяет сообщения, форматируя каждое сообщение с тегами `<|im_start|>` и `<|im_end|>`.
    2. Если `do_continue` равен `False`, добавляет тег начала сообщения ассистента.
    3. Если `do_continue` равен `True`, удаляет последний тег `\\n<|im_end|>\\n`.
    4. Возвращает отформатированный промпт.

    ASCII flowchart:
    A: Объединение и форматирование сообщений
    |
    B: Проверка `do_continue`
    |
    C: Добавление тега ассистента (если `do_continue` == False)
    |
    D: Удаление последнего тега (если `do_continue` == True)
    |
    E: Возврат отформатированного промпта

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        >>> format_prompt_qwen(messages)
        '<|im_start|>user\\nHello\\n<|im_end|>\\n<|im_start|>assistant\\nHi\\n<|im_end|>\\n<|im_start|>assistant\\n'
    """
    ...
```

### `format_prompt_qwen2`

```python
def format_prompt_qwen2(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Qwen2.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на продолжение предыдущего разговора.

    Returns:
        str: Отформатированный промпт.

    Как работает функция:
    1. Объединяет сообщения, форматируя каждое сообщение с тегами `\\u003C｜...｜\\u003E`.
    2. Если `do_continue` равен `False`, добавляет тег начала сообщения ассистента.
    3. Если `do_continue` равен `True`, удаляет последний тег `\\u003C｜Assistant｜\\u003E`.
    4. Возвращает отформатированный промпт.

    ASCII flowchart:
    A: Объединение и форматирование сообщений
    |
    B: Проверка `do_continue`
    |
    C: Добавление тега ассистента (если `do_continue` == False)
    |
    D: Удаление последнего тега (если `do_continue` == True)
    |
    E: Возврат отформатированного промпта

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        >>> format_prompt_qwen2(messages)
        '\\u003C｜User｜\\u003EHello\\u003C｜end of sentence｜\\u003E\\u003C｜Assistant｜\\u003EHi\\u003C｜end of sentence｜\\u003E\\u003C｜Assistant｜\\u003E'
    """
    ...
```

### `format_prompt_llama`

```python
def format_prompt_llama(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Llama.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на продолжение предыдущего разговора.

    Returns:
        str: Отформатированный промпт.

    Как работает функция:
    1. Объединяет сообщения, форматируя каждое сообщение с тегами `<|start_header_id|>`, `<|end_header_id|>` и `<|eot_id|>`.
    2. Если `do_continue` равен `False`, добавляет тег начала сообщения ассистента.
    3. Если `do_continue` равен `True`, удаляет последний тег `\\n<|eot_id|>\\n`.
    4. Возвращает отформатированный промпт.

    ASCII flowchart:
    A: Объединение и форматирование сообщений
    |
    B: Проверка `do_continue`
    |
    C: Добавление тега ассистента (если `do_continue` == False)
    |
    D: Удаление последнего тега (если `do_continue` == True)
    |
    E: Возврат отформатированного промпта

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        >>> format_prompt_llama(messages)
        '<|begin_of_text|><|start_header_id|>user<|end_header_id|>\\n\\nHello\\n<|eot_id|>\\n<|start_header_id|>assistant<|end_header_id|>\\n\\nHi\\n<|eot_id|>\\n<|start_header_id|>assistant<|end_header_id|>\\n\\n'
    """
    ...
```

### `format_prompt_custom`

```python
def format_prompt_custom(messages: Messages, end_token: str = "</s>", do_continue: bool = False) -> str:
    """
    Форматирует промпт с пользовательским токеном завершения.

    Args:
        messages (Messages): Список сообщений.
        end_token (str): Пользовательский токен завершения. По умолчанию "</s>".
        do_continue (bool): Флаг, указывающий на продолжение предыдущего разговора.

    Returns:
        str: Отформатированный промпт.

    Как работает функция:
    1. Объединяет сообщения, форматируя каждое сообщение с тегами `<|...|>` и пользовательским токеном завершения.
    2. Если `do_continue` равен `False`, добавляет тег начала сообщения ассистента.
    3. Если `do_continue` равен `True`, удаляет последний тег `end_token + "\\n"`.
    4. Возвращает отформатированный промпт.

    ASCII flowchart:
    A: Объединение и форматирование сообщений
    |
    B: Проверка `do_continue`
    |
    C: Добавление тега ассистента (если `do_continue` == False)
    |
    D: Удаление последнего тега (если `do_continue` == True)
    |
    E: Возврат отформатированного промпта

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        >>> format_prompt_custom(messages)
        '<|user|>\\nHello</s>\\n<|assistant|>\\nHi</s>\\n<|assistant|>\\n'
    """
    ...
```

### `get_inputs`

```python
def get_inputs(messages: Messages, model_data: dict, model_type: str, do_continue: bool = False) -> str:
    """
    Получает входные данные для модели в зависимости от ее типа и конфигурации.

    Args:
        messages (Messages): Список сообщений.
        model_data (dict): Данные о модели.
        model_type (str): Тип модели.
        do_continue (bool): Флаг, указывающий на продолжение предыдущего разговора.

    Returns:
        str: Входные данные для модели.

    Как работает функция:
    1. В зависимости от типа модели (`model_type`) выбирает подходящую функцию форматирования промпта.
    2. Если тип модели `gpt2`, `gpt_neo`, `gemma` или `gemma2`, использует функцию `format_prompt`.
    3. Если тип модели `mistral` и автор `mistralai`, использует функцию `format_prompt_mistral`.
    4. Если в данных модели есть информация о токене завершения (`eos_token`), выбирает функцию форматирования в зависимости от значения этого токена.
    5. Если ни одно из условий не выполнено, использует функцию `format_prompt` по умолчанию.
    6. Возвращает отформатированные входные данные.

    ASCII flowchart:
    A: Проверка типа модели
    |
    B: Выбор функции форматирования промпта
    |
    C: Форматирование входных данных
    |
    D: Возврат отформатированных входных данных

    Примеры:
        Примеры использования этой функции требуют предварительной настройки данных модели и, следовательно, не могут быть выполнены непосредственно в документации.
    """
    ...