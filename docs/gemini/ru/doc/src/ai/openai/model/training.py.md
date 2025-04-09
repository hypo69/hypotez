# Модуль для работы с OpenAI Model

## Обзор

Модуль `training.py` содержит класс `OpenAIModel`, предназначенный для взаимодействия с OpenAI API, управления моделями и их обучения. Класс предоставляет методы для получения списка доступных моделей и ассистентов, установки ассистента, отправки сообщений, обучения модели на основе предоставленных данных и сохранения идентификаторов задач обучения.

## Подробней

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с OpenAI API для выполнения различных задач, таких как обучение моделей, ведение диалогов и анализ тональности. Он использует модуль `src.logger` для логирования информации об ошибках и процессе работы.

## Классы

### `OpenAIModel`

**Описание**: Класс `OpenAIModel` предназначен для взаимодействия с OpenAI API, управления моделями и их обучения.

**Принцип работы**:

1.  **Инициализация**: При инициализации класса устанавливается соединение с OpenAI API с использованием предоставленного API-ключа. Загружаются доступные модели и ассистенты, а также создается ассистент и поток (thread) для взаимодействия.

2.  **Взаимодействие с API**: Класс предоставляет методы для отправки сообщений в модель, получения ответов, анализа тональности ответов и сохранения диалогов.

3.  **Обучение модели**: Класс позволяет обучать модель на основе предоставленных данных, таких как CSV-файлы или строки в формате CSV.

4.  **Управление ассистентами**: Класс предоставляет методы для установки и получения списка доступных ассистентов.

**Аттрибуты**:

*   `model` (str): Имя используемой модели (по умолчанию "gpt-4o-mini").
*   `client` (OpenAI): Клиент OpenAI для взаимодействия с API.
*   `current_job_id` (str): Идентификатор текущей задачи обучения.
*   `assistant_id` (str): Идентификатор используемого ассистента.
*   `assistant` (Any): Объект ассистента OpenAI.
*   `thread` (Any): Объект потока OpenAI.
*   `system_instruction` (str): Системные инструкции для модели.
*   `dialogue_log_path` (str | Path): Путь к файлу для сохранения диалогов.
*   `dialogue` (List[Dict[str, str]]): Список диалогов.
*   `assistants` (List[SimpleNamespace]): Список доступных ассистентов.
*   `models_list` (List[str]): Список доступных моделей.

**Методы**:

*   `__init__(api_key: str, system_instruction: str = None, model_name: str = 'gpt-4o-mini', assistant_id: str = None)`: Инициализирует объект `OpenAIModel`.
*   `list_models() -> List[str]`: Динамически получает и возвращает доступные модели из OpenAI API.
*   `list_assistants() -> List[str]`: Динамически загружает доступных ассистентов из JSON-файла.
*   `set_assistant(assistant_id: str)`: Устанавливает ассистента, используя предоставленный идентификатор.
*   `_save_dialogue()`: Сохраняет весь диалог в JSON-файл.
*   `determine_sentiment(message: str) -> str`: Определяет тональность сообщения (положительная, отрицательная или нейтральная).
*   `ask(message: str, system_instruction: str = None, attempts: int = 3) -> str`: Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.
*   `describe_image(image_path: str | Path, prompt:Optional[str] = None, system_instruction:Optional[str] = None ) -> str`: Отправляет изображение модели и возвращает описание изображения.
*   `describe_image_by_requests(image_path: str | Path, prompt:str = None) -> str`: Отправляет изображение в OpenAI API и получает описание, используя requests.post.
*   `dynamic_train()`: Динамически загружает предыдущий диалог и дообучает модель на его основе.
*   `train(data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None`: Обучает модель на основе указанных данных или каталога.
*   `save_job_id(job_id: str, description: str, filename: str = "job_ids.json")`: Сохраняет идентификатор задачи обучения с описанием в файл.

## Функции

### `__init__`

```python
def __init__(self, api_key: str, system_instruction: str = None, model_name: str = 'gpt-4o-mini', assistant_id: str = None):
    """Инициализирует объект Model с API-ключом, идентификатором ассистента, а также загружает доступные модели и ассистенты.

    Args:
        api_key (str): API-ключ для доступа к OpenAI API.
        system_instruction (str, optional): Необязательная системная инструкция для модели.
        model_name (str, optional): Имя модели. По умолчанию 'gpt-4o-mini'.
        assistant_id (str, optional): Необязательный идентификатор ассистента. По умолчанию значение из gs.credentials.openai.assistant_id.code_assistant.
    """
    #self.client = OpenAI(api_key = gs.credentials.openai.project_api)
    self.client = OpenAI(api_key = api_key if api_key else gs.credentials.openai.api_key)
    self.current_job_id = None
    self.assistant_id = assistant_id or gs.credentials.openai.assistant_id.code_assistant
    self.system_instruction = system_instruction

    # Load assistant and thread during initialization
    self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
    self.thread = self.client.beta.threads.create()
```

**Назначение**: Инициализирует объект класса `OpenAIModel`, устанавливая API-ключ, идентификатор ассистента и загружая необходимые данные для работы с OpenAI API.

**Параметры**:

*   `api_key` (str): API-ключ для доступа к OpenAI API.
*   `system_instruction` (str, optional): Системная инструкция для модели. По умолчанию `None`.
*   `model_name` (str, optional): Имя используемой модели. По умолчанию `'gpt-4o-mini'`.
*   `assistant_id` (str, optional): Идентификатор ассистента. По умолчанию `None`.

**Как работает функция**:

1.  Функция инициализирует клиент OpenAI с использованием предоставленного API-ключа или ключа из `gs.credentials.openai.api_key`.
2.  Устанавливает идентификатор ассистента, используя предоставленный `assistant_id` или `gs.credentials.openai.assistant_id.code_assistant`, если `assistant_id` не указан.
3.  Сохраняет системную инструкцию.
4.  Загружает ассистента и создает поток (thread) для дальнейшего взаимодействия с моделью.

**Примеры**:

```python
model = OpenAIModel(api_key='YOUR_API_KEY', system_instruction="You are a helpful assistant.")
model = OpenAIModel(api_key='YOUR_API_KEY', assistant_id='asst_1234567890')
```

### `list_models`

```python
@property
def list_models(self) -> List[str]:
    """Динамически получает и возвращает доступные модели из OpenAI API.

    Returns:
        List[str]: Список идентификаторов моделей, доступных через OpenAI API.
    """
    try:
        models = self.client.models.list()
        model_list = [model['id'] for model in models['data']]
        logger.info(f"Loaded models: {model_list}")
        return model_list
    except Exception as ex:
        logger.error("An error occurred while loading models:", ex)
        return []
```

**Назначение**: Получает список доступных моделей из OpenAI API.

**Возвращает**:

*   `List[str]`: Список идентификаторов доступных моделей.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при загрузке моделей.

**Как работает функция**:

1.  Вызывает метод `self.client.models.list()` для получения списка моделей из OpenAI API.
2.  Извлекает идентификаторы моделей из полученного списка и сохраняет их в список `model_list`.
3.  Логирует информацию о загруженных моделях.
4.  Возвращает список идентификаторов моделей.
5.  В случае ошибки логирует ошибку и возвращает пустой список.

**Примеры**:

```python
models = model.list_models
print(models)
```

### `list_assistants`

```python
@property
def list_assistants(self) -> List[str]:
    """Динамически загружает доступных ассистентов из JSON-файла.

    Returns:
        List[str]: Список имен ассистентов.
    """
    try:
        self.assistants = j_loads_ns(gs.path.src / 'ai' / 'openai' / 'model' / 'assistants' / 'assistants.json')
        assistant_list = [assistant.name for assistant in self.assistants]
        logger.info(f"Loaded assistants: {assistant_list}")
        return assistant_list
    except Exception as ex:
        logger.error("An error occurred while loading assistants:", ex)
        return []
```

**Назначение**: Загружает список доступных ассистентов из JSON-файла.

**Возвращает**:

*   `List[str]`: Список имен ассистентов.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при загрузке ассистентов.

**Как работает функция**:

1.  Загружает данные об ассистентах из JSON-файла, используя функцию `j_loads_ns`.
2.  Извлекает имена ассистентов из загруженных данных и сохраняет их в список `assistant_list`.
3.  Логирует информацию о загруженных ассистентах.
4.  Возвращает список имен ассистентов.
5.  В случае ошибки логирует ошибку и возвращает пустой список.

**Примеры**:

```python
assistants = model.list_assistants
print(assistants)
```

### `set_assistant`

```python
def set_assistant(self, assistant_id: str):
    """Устанавливает ассистента, используя предоставленный идентификатор.

    Args:
        assistant_id (str): Идентификатор ассистента для установки.
    """
    try:
        self.assistant_id = assistant_id
        self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        logger.info(f"Assistant set successfully: {assistant_id}")
    except Exception as ex:
        logger.error("An error occurred while setting the assistant:", ex)
```

**Назначение**: Устанавливает ассистента, используя предоставленный идентификатор.

**Параметры**:

*   `assistant_id` (str): Идентификатор ассистента для установки.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при установке ассистента.

**Как работает функция**:

1.  Устанавливает идентификатор ассистента.
2.  Получает объект ассистента из OpenAI API с использованием предоставленного идентификатора.
3.  Логирует информацию об успешной установке ассистента.
4.  В случае ошибки логирует ошибку.

**Примеры**:

```python
model.set_assistant(assistant_id='asst_1234567890')
```

### `_save_dialogue`

```python
def _save_dialogue(self):
    """Сохраняет весь диалог в JSON-файл."""
    j_dumps(self.dialogue, self.dialogue_log_path)
```

**Назначение**: Сохраняет весь диалог в JSON-файл.

**Как работает функция**:

1.  Использует функцию `j_dumps` для сохранения списка диалогов `self.dialogue` в файл, указанный в `self.dialogue_log_path`.

**Примеры**:

```python
model._save_dialogue()
```

### `determine_sentiment`

```python
def determine_sentiment(self, message: str) -> str:
    """Определяет тональность сообщения (положительная, отрицательная или нейтральная).

    Args:
        message (str): Сообщение для анализа.

    Returns:
        str: Тональность ('positive', 'negative' или 'neutral').
    """
    positive_words = ["good", "great", "excellent", "happy", "love", "wonderful", "amazing", "positive"]
    negative_words = ["bad", "terrible", "hate", "sad", "angry", "horrible", "negative", "awful"]
    neutral_words = ["okay", "fine", "neutral", "average", "moderate", "acceptable", "sufficient"]

    message_lower = message.lower()

    if any(word in message_lower for word in positive_words):
        return "positive"
    elif any(word in message_lower for word in negative_words):
        return "negative"
    elif any(word in message_lower for word in neutral_words):
        return "neutral"
    else:
        return "neutral"
```

**Назначение**: Определяет тональность сообщения (положительная, отрицательная или нейтральная).

**Параметры**:

*   `message` (str): Сообщение для анализа.

**Возвращает**:

*   `str`: Тональность сообщения (`'positive'`, `'negative'` или `'neutral'`).

**Как работает функция**:

1.  Приводит сообщение к нижнему регистру.
2.  Проверяет наличие позитивных слов в сообщении. Если найдено, возвращает `'positive'`.
3.  Проверяет наличие негативных слов в сообщении. Если найдено, возвращает `'negative'`.
4.  Проверяет наличие нейтральных слов в сообщении. Если найдено, возвращает `'neutral'`.
5.  Если не найдено ни одного из вышеперечисленных слов, возвращает `'neutral'`.

**Примеры**:

```python
sentiment = model.determine_sentiment("This is a great day!")
print(sentiment)  # Вывод: positive
```

### `ask`

```python
def ask(self, message: str, system_instruction: str = None, attempts: int = 3) -> str:
    """Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.

    Args:
        message (str): Сообщение для отправки модели.
        system_instruction (str, optional): Необязательная системная инструкция.
        attempts (int, optional): Количество попыток повтора запроса. По умолчанию 3.

    Returns:
        str: Ответ от модели.
    """
    try:
        messages = []
        if self.system_instruction or system_instruction:
            system_instruction_escaped = (system_instruction or self.system_instruction).replace('"', r'\"')
            messages.append({"role": "system", "content": system_instruction_escaped})

        message_escaped = message.replace('"', r'\"')
        messages.append({
                        "role": "user", 
                         "content": message_escaped
                         })

        # Отправка запроса к модели
        response = self.client.chat.completions.create(
            model = self.model,
            
            messages = messages,
            temperature = 0,
            max_tokens=8000,
        )
        reply = response.choices[0].message.content.strip()

        # Анализ тональности
        sentiment = self.determine_sentiment(reply)

        # Добавление сообщений и тональности в диалог
        self.dialogue.append({"role": "system", "content": system_instruction or self.system_instruction})
        self.dialogue.append({"role": "user", "content": message_escaped})
        self.dialogue.append({"role": "assistant", "content": reply, "sentiment": sentiment})

        # Сохранение диалога
        self._save_dialogue()

        return reply
    except Exception as ex:
        logger.debug(f"An error occurred while sending the message: \n-----\n {pprint(messages)} \n-----\n", ex, True)
        time.sleep(3)
        if attempts > 0:
            return self.ask(message, attempts - 1)
        return
```

**Назначение**: Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.

**Параметры**:

*   `message` (str): Сообщение для отправки модели.
*   `system_instruction` (str, optional): Системная инструкция для модели. По умолчанию `None`.
*   `attempts` (int, optional): Количество попыток повтора запроса в случае ошибки. По умолчанию `3`.

**Возвращает**:

*   `str`: Ответ от модели.

**Как работает функция**:

1.  Формирует список сообщений для отправки в модель, включая системную инструкцию и сообщение пользователя.
2.  Отправляет запрос в модель с использованием `self.client.chat.completions.create`.
3.  Извлекает ответ из полученного ответа модели.
4.  Анализирует тональность ответа с помощью метода `self.determine_sentiment`.
5.  Добавляет сообщения и тональность в диалог.
6.  Сохраняет диалог с помощью метода `self._save_dialogue`.
7.  Возвращает ответ от модели.
8.  В случае ошибки логирует ошибку и повторяет запрос указанное количество раз.

**Примеры**:

```python
response = model.ask("Hello, how are you?")
print(response)
```

### `describe_image`

```python
def describe_image(self, image_path: str | Path, prompt:Optional[str] = None, system_instruction:Optional[str] = None ) -> str:
    """"""
    ...
    
    messages:list = []
    base64_image = base64encode(image_path)

    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})

    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": prompt if prompt else "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                },
            ],
        }
    )
    try:
        response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                temperature = 0,
                max_tokens=800,
            )
    
        reply = response
        ...
        try:
            raw_reply = response.choices[0].message.content.strip()
            return j_loads_ns(raw_reply)
        except Exception as ex:
            logger.error(f"Trouble in reponse {response}", ex, True)
            ...
            return

    except Exception as ex:
        logger.error(f"Ошибка openai", ex, True)
        ...
        return
```

**Назначение**: Отправляет изображение в OpenAI API и возвращает описание изображения.

**Параметры**:

*   `image_path` (str | Path): Путь к файлу изображения.
*   `prompt` (Optional[str], optional): Необязательный запрос для описания изображения. По умолчанию `None`.
*   `system_instruction` (Optional[str], optional): Необязательная системная инструкция для модели. По умолчанию `None`.

**Как работает функция**:

1.  Кодирует изображение в формат base64.
2.  Формирует список сообщений для отправки в модель, включая системную инструкцию, запрос пользователя и изображение в формате base64.
3.  Отправляет запрос в модель с использованием `self.client.chat.completions.create`.
4.  Извлекает ответ из полученного ответа модели.
5.  Пытается загрузить ответ как JSON, используя `j_loads_ns`.
6.  В случае ошибки логирует ошибку и возвращает `None`.

**Примеры**:

```python
image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
description = model.describe_image(image_path, prompt="Describe this image in detail.")
print(description)
```

### `describe_image_by_requests`

```python
def describe_image_by_requests(self, image_path: str | Path, prompt:str = None) -> str:
    """Отправляет изображение в OpenAI API и получает описание."""
    # Getting the base64 string
    base64_image = base64encode(image_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {gs.credentials.openai.project_api}"
    }

    payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt if prompt else "What’s in this image?"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_json = response.json()
        ...
    except Exception as ex:
        logger.error(f"Error in image description {image_path=}\\n", ex)
```

**Назначение**: Отправляет изображение в OpenAI API и получает описание, используя `requests.post`.

**Параметры**:

*   `image_path` (str | Path): Путь к файлу изображения.
*   `prompt` (str, optional): Необязательный запрос для описания изображения. По умолчанию `None`.

**Как работает функция**:

1.  Кодирует изображение в формат base64.
2.  Формирует заголовки запроса, включая API-ключ.
3.  Формирует полезную нагрузку (payload) запроса, включая модель, сообщение пользователя и изображение в формате base64.
4.  Отправляет POST-запрос в OpenAI API с использованием библиотеки `requests`.
5.  В случае ошибки логирует ошибку.

**Примеры**:

```python
image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
description = model.describe_image_by_requests(image_path, prompt="Describe this image in detail.")
print(description)
```

### `dynamic_train`

```python
def dynamic_train(self):
    """Динамически загружает предыдущий диалог и дообучает модель на его основе."""
    try:
        messages = j_loads(gs.path.google_drive / 'AI' / 'conversation' / 'dailogue.json')

        if messages:
            response = self.client.chat.completions.create(
                model=self.model,
                assistant=self.assistant_id,
                messages=messages,
                temperature=0,
            )
            logger.info("Fine-tuning during the conversation was successful.")
        else:
            logger.info("No previous dialogue found for fine-tuning.")
    except Exception as ex:
        logger.error(f"Error during dynamic fine-tuning: {ex}")
```

**Назначение**: Динамически загружает предыдущий диалог и дообучает модель на его основе.

**Как работает функция**:

1.  Загружает предыдущий диалог из файла `dailogue.json` с использованием функции `j_loads`.
2.  Если диалог найден, отправляет запрос в OpenAI API для дообучения модели на основе загруженного диалога.
3.  Логирует информацию об успешном или неуспешном дообучении.
4.  В случае ошибки логирует ошибку.

**Примеры**:

```python
model.dynamic_train()
```

### `train`

```python
def train(self, data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None:
    """Обучает модель на основе указанных данных или каталога.

    Args:
        data (str, optional): Путь к CSV-файлу или CSV-форматированная строка с данными.
        data_dir (Path | str, optional): Каталог, содержащий CSV-файлы для обучения.
        data_file (Path | str, optional): Путь к одному CSV-файлу с данными для обучения.
        positive (bool, optional): Указывает, являются ли данные позитивными или негативными. По умолчанию `True`.

    Returns:
        str | None: Идентификатор задачи обучения или `None`, если произошла ошибка.
    """
    if not data_dir:
        data_dir = gs.path.google_drive / 'AI' / 'training'

    try:
        documents = j_loads(data if data else data_file if data_file else data_dir)

        response = self.client.Training.create(
            model=self.model,
            documents=documents,
            labels=["positive" if positive else "negative"] * len(documents),
            show_progress=True
        )
        self.current_job_id = response.id
        return response.id

    except Exception as ex:
        logger.error("An error occurred during training:", ex)
        return
```

**Назначение**: Обучает модель на основе указанных данных или каталога.

**Параметры**:

*   `data` (str, optional): Путь к CSV-файлу или CSV-форматированная строка с данными.
*   `data_dir` (Path | str, optional): Каталог, содержащий CSV-файлы для обучения.
*   `data_file` (Path | str, optional): Путь к одному CSV-файлу с данными для обучения.
*   `positive` (bool, optional): Указывает, являются ли данные позитивными или негативными. По умолчанию `True`.

**Возвращает**:

*   `str | None`: Идентификатор задачи обучения или `None`, если произошла ошибка.

**Как работает функция**:

1.  Определяет каталог с данными для обучения.
2.  Загружает данные из указанного источника (строка, файл или каталог) с использованием функции `j_loads`.
3.  Отправляет запрос в OpenAI API для обучения модели на основе загруженных данных.
4.  Возвращает идентификатор задачи обучения.
5.  В случае ошибки логирует ошибку и возвращает `None`.

**Примеры**:

```python
training_result = model.train(data_file=gs.path.google_drive / 'AI' / 'training_data.csv')
print(training_result)
```

### `save_job_id`

```python
def save_job_id(self, job_id: str, description: str, filename: str = "job_ids.json"):
    """Сохраняет идентификатор задачи обучения с описанием в файл.

    Args:
        job_id (str): Идентификатор задачи для сохранения.
        description (str): Описание задачи.
        filename (str, optional): Имя файла для сохранения идентификаторов задач. По умолчанию "job_ids.json".
    """
    job_data = {"id": job_id, "description": description, "created": time.time()}
    job_file = gs.path.google_drive / filename

    if not job_file.exists():
        j_dumps([job_data], job_file)
    else:
        existing_jobs = j_loads(job_file)
        existing_jobs.append(job_data)
        j_dumps(existing_jobs, job_file)
```

**Назначение**: Сохраняет идентификатор задачи обучения с описанием в файл.

**Параметры**:

*   `job_id` (str): Идентификатор задачи для сохранения.
*   `description` (str): Описание задачи.
*   `filename` (str, optional): Имя файла для сохранения идентификаторов задач. По умолчанию `"job_ids.json"`.

**Как работает функция**:

1.  Формирует словарь с данными о задаче, включая идентификатор, описание и время создания.
2.  Определяет путь к файлу для сохранения данных.
3.  Если файл не существует, создает файл и сохраняет данные в формате JSON.
4.  Если файл существует, загружает существующие данные, добавляет новые данные и сохраняет обновленные данные в файл.

**Примеры**:

```python
model.save_job_id(job_id='job_1234567890', description="Training model with new data")
```

### `main`

```python
def main():
    """Основная функция для инициализации OpenAIModel и демонстрации использования.
    Explanation:
        Initialization of the Model:

        The OpenAIModel is initialized with a system instruction and an assistant ID. You can modify the parameters if necessary.
        Listing Models and Assistants:

        The list_models and list_assistants methods are called to print the available models and assistants.
        Asking the Model a Question:

        The ask() method is used to send a message to the model and retrieve its response.
        Dynamic Training:

        The dynamic_train() method performs dynamic fine-tuning based on past dialogue.
        Training the Model:

        The train() method trains the model using data from a specified file (in this case, 'training_data.csv').
        Saving the Training Job ID:

        After training, the job ID is saved with a description to a JSON file."""
    
    # Initialize the model with system instructions and assistant ID (optional)
    model = OpenAIModel(system_instruction="You are a helpful assistant.", assistant_id="asst_dr5AgQnhhhnef5OSMzQ9zdk9")
    
    # Example of listing available models
    print("Available Models:")
    models = model.list_models
    pprint(models)

    # Example of listing available assistants
    print("\nAvailable Assistants:")
    assistants = model.list_assistants
    pprint(assistants)

    # Example of asking the model a question
    user_input = "Hello, how are you?"
    print("\nUser Input:", user_input)
    response = model.ask(user_input)
    print("Model Response:", response)

    # Example of dynamic training using past dialogue
    print("\nPerforming dynamic training...")
    model.dynamic_train()

    # Example of training the model using provided data
    print("\nTraining the model...")
    training_result = model.train(data_file=gs.path.google_drive / 'AI' / 'training_data.csv')
    print(f"Training job ID: {training_result}")

    # Example of saving a job ID
    if training_result:
        model.save_job_id(training_result, "Training model with new data", filename="job_ids.json")
        print(f"Saved training job ID: {training_result}")

    # Пример описания изображения
    image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
    print("\nDescribing Image:")
    description = model.describe_image(image_path)
    print(f"Image description: {description}")
```

**Назначение**: Инициализирует `OpenAIModel` и демонстрирует основные варианты использования класса.

**Как работает функция**:

1.  Инициализирует объект `OpenAIModel` с системной инструкцией и идентификатором ассистента.
2.  Выводит список доступных моделей и ассистентов.
3.  Задает вопрос модели и выводит ответ.
4.  Выполняет динамическое обучение модели на основе предыдущего диалога.
5.  Обучает модель с использованием данных из указанного файла.
6.  Сохраняет идентификатор задачи обучения.
7.  Описывает изображение и выводит полученное описание.

**Примеры**:

```python
if __name__ == "__main__":
    main()
```