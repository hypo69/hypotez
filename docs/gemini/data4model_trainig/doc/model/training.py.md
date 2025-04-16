## Модуль `model`

### Обзор

Модуль предназначен для работы с OpenAI API, включая обучение моделей и взаимодействие с ними.

### Подробней

Модуль содержит класс `OpenAIModel`, который предоставляет методы для загрузки моделей, отправки запросов, анализа тональности, динамической донастройки моделей на основе диалогов и проведения обучения с использованием предоставленных данных.

## Классы

### `OpenAIModel`

**Описание**: Класс для взаимодействия с OpenAI API и управления моделями.

**Атрибуты**:

*   `model` (str): Имя модели для использования (по умолчанию `"gpt-4o-mini"`).
*   `client` (OpenAI): Клиент для взаимодействия с OpenAI API.
*   `current_job_id` (str): ID текущей задачи обучения.
*   `assistant_id` (str): ID ассистента (по умолчанию берется из конфигурации).
*   `assistant` (Any): Объект ассистента.
*   `thread` (Any): Объект треда.
*   `system_instruction` (str): Системная инструкция для модели.
*   `dialogue_log_path` (str | Path): Путь для сохранения логов диалогов.
*   `dialogue` (List[Dict[str, str]]): Список диалогов.
*   `assistants` (List[SimpleNamespace]): Список доступных ассистентов.
*   `models_list` (List[str]): Список доступных моделей.

**Методы**:

*   `__init__`: Инициализирует объект `OpenAIModel`.
*   `list_models`: Получает список доступных моделей из OpenAI API.
*   `list_assistants`: Загружает список доступных ассистентов из JSON-файла.
*   `set_assistant`: Устанавливает ассистента, используя предоставленный ID.
*   `_save_dialogue`: Сохраняет весь диалог в JSON-файл.
*   `determine_sentiment`: Определяет тональность сообщения (положительная, отрицательная или нейтральная).
*   `ask`: Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.
*   `describe_image`: Отправляет изображение в OpenAI API и получает описание.
*   `dynamic_train`: Динамически загружает предыдущий диалог и выполняет дообучение модели на его основе.
*   `train`: Обучает модель на основе указанных данных или директории.
*   `save_job_id`: Сохраняет ID задачи обучения с описанием в файл.

### `__init__`

```python
def __init__(self, api_key:str, system_instruction: str = None, model_name:str = 'gpt-4o-mini', assistant_id: str = None):
    """Initialize the Model object with API key, assistant ID, and load available models and assistants.

    Args:
        system_instruction (str, optional): An optional system instruction for the model.
        assistant_id (str, optional): An optional assistant ID. Defaults to 'asst_dr5AgQnhhhnef5OSMzQ9zdk9'.
    """
    ...
```

**Назначение**: Инициализирует объект `OpenAIModel`.

**Параметры**:

*   `api_key` (str): Ключ API PrestaShop.
*   `system_instruction` (str, optional): Общая инструкция для модели.
*   `model_name` (str, optional): Название языковой модели OpenAI для использования (по умолчанию `"gpt-4o-mini"`).
*   `assistant_id` (str, optional): ID ассистента.

**Как работает функция**:

1.  Инициализирует клиент OpenAI с использованием предоставленного API-ключа.
2.  Устанавливает `current_job_id` в `None`.
3.  Устанавливает `assistant_id` для использования в дальнейшем.
4.  Загружает ассистента и поток (thread) во время инициализации.
5.  Сохраняет system_instruction

### `list_models`

```python
@property
def list_models(self) -> List[str]:
    """Dynamically fetch and return available models from the OpenAI API.

    Returns:
        List[str]: A list of model IDs available via the OpenAI API.
    """
    ...
```

**Назначение**: Получает список доступных моделей из OpenAI API.

**Возвращает**:
* `List[str]`: A list of model IDs available via the OpenAI API.

**Как работает функция**:
1. Запрашивает список моделей из OpenAI API.
2. Извлекает идентификаторы моделей из ответа.
3. Логирует информацию о загруженных моделях.
4. Возвращает список идентификаторов моделей.

### `list_assistants`

```python
@property
def list_assistants(self) -> List[str]:
    """Dynamically load available assistants from a JSON file.

    Returns:
        List[str]: A list of assistant names.
    """
    ...
```

**Назначение**: Динамически загружает список доступных ассистентов из JSON-файла.

**Возвращает**:
- `List[str]`: A list of assistant names.

**Как работает функция**:

1.  Загружает данные об ассистентах из JSON-файла.
2.  Извлекает имена ассистентов из загруженных данных.
3.  Логирует информацию о загруженных ассистентах.
4.  Возвращает список имен ассистентов.

### `set_assistant`

```python
def set_assistant(self, assistant_id: str):
    """Set the assistant using the provided assistant ID.

    Args:
        assistant_id (str): The ID of the assistant to set.
    """
    ...
```

**Назначение**: Устанавливает ассистента, используя предоставленный ID.

**Параметры**:
- `assistant_id` (str): The ID of the assistant to set.

**Как работает функция**:

1.  Устанавливает `assistant_id` для использования в дальнейшем.
2.  Получает объект ассистента из OpenAI API, используя предоставленный `assistant_id`.
3.  Логирует информацию об успешной установке ассистента.

### `_save_dialogue`

```python
def _save_dialogue(self):
    """Save the entire dialogue to the JSON file."""
    ...
```

**Назначение**: Сохраняет весь диалог в JSON-файл.

**Как работает функция**:
1. Сохраняет содержимое списка `self.dialogue` в JSON-файл по пути `self.dialogue_log_path` с использованием функции `j_dumps`.

### `determine_sentiment`

```python
def determine_sentiment(self, message: str) -> str:
    """Determine the sentiment of a message (positive, negative, or neutral).

    Args:
        message (str): The message to analyze.

    Returns:
        str: The sentiment ('positive', 'negative', or 'neutral').
    """
    ...
```

**Назначение**: Определяет тональность сообщения (положительная, отрицательная или нейтральная).

**Параметры**:
- `message` (str): The message to analyze.

**Возвращает**:
- `str`: The sentiment ('positive', 'negative', or 'neutral').

**Как работает функция**:

1.  Приводит сообщение к нижнему регистру.
2.  Проверяет наличие в сообщении ключевых слов, связанных с положительной, отрицательной или нейтральной тональностью.
3.  Возвращает определенную тональность на основе наличия ключевых слов.

### `ask`

```python
def ask(self, message: str, system_instruction: str = None, attempts: int = 3) -> str:
    """Send a message to the model and return the response, along with sentiment analysis.

    Args:
        message (str): The message to send to the model.
        system_instruction (str, optional): Optional system instruction.
        attempts (int, optional): Number of retry attempts. Defaults to 3.

    Returns:
        str: The response from the model.
    """
    ...
```

**Назначение**: Отправляет сообщение модели и возвращает ответ, а также анализ тональности.

**Параметры**:

*   `message` (str): Сообщение для отправки модели.
*   `system_instruction` (str, optional): Опциональная системная инструкция (по умолчанию `None`).
*   `attempts` (int, optional): Количество попыток при возникновении ошибки (по умолчанию `3`).

**Возвращает**:

*   `str`: Ответ от модели.

**Как работает функция**:

1.  Формирует список сообщений для отправки в модель, включая системную инструкцию и сообщение пользователя.
2.  Отправляет запрос к OpenAI API с использованием `self.client.chat.completions.create`.
3.  Анализирует тональность полученного ответа.
4.  Сохраняет сообщения и тональность в диалог.
5.  Сохраняет диалог в файл.
6.  Возвращает ответ модели.

### `describe_image`

```python
def describe_image(self, image_path: str | Path, prompt:Optional[str] = None, system_instruction:Optional[str] = None ) -> str:
    """"""
    ...
```

**Назначение**: Отправляет изображение в OpenAI API и получает описание.

**Параметры**:

*   `image_path` (str | Path): Путь к изображению.
*   `prompt` (Optional[str]): Опциональный промпт для описания изображения.
*   `system_instruction` (Optional[str]): Опциональная системная инструкция для модели

**Возвращает**:
* `str`: Текстовое описание изображения.

**Как работает функция**:

1. Кодирует изображение в base64.
2. Формирует запрос к OpenAI API, включая изображение и промпт.
3. Отправляет запрос и получает ответ.
4. Извлекает текстовое описание из ответа.

### `describe_image_by_requests`

```python
def describe_image_by_requests(self, image_path: str | Path, prompt:str = None) -> str:
    """Send an image to the OpenAI API and receive a description."""
    ...
```

**Назначение**: Отправляет изображение в OpenAI API и получает описание.

**Параметры**:
- `image_path` (str | Path): Путь к изображению.
-  `prompt` (str): Опциональный промпт для описания изображения.

**Возвращает**:
- `str`: Описание изображения.

**Как работает функция**:
1.  Кодирует изображение в base64.
2.  Создает заголовки и полезную нагрузку запроса, включая закодированное изображение и, если предоставлено, подсказку.
3.  Отправляет POST-запрос в конечную точку API OpenAI с использованием библиотеки запросов.
4.  Анализирует ответ JSON и возвращает результат.

### `dynamic_train`

```python
def dynamic_train(self):
    """Dynamically load previous dialogue and fine-tune the model based on it."""
    ...
```

**Назначение**: Динамически загружает предыдущий диалог и выполняет дообучение модели на его основе.

**Как работает функция**:

1.  Загружает сообщения из JSON-файла, содержащего предыдущий диалог.
2.  Отправляет сообщения в OpenAI API для дообучения модели.

### `train`

```python
def train(self, data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None:
    """Train the model on the specified data or directory.

    Args:
        data (str, optional): Path to a CSV file or CSV-formatted string with data.
        data_dir (Path | str, optional): Directory containing CSV files for training.
        data_file (Path | str, optional): Path to a single CSV file with training data.
        positive (bool, optional): Whether the data is positive or negative. Defaults to True.

    Returns:
        str | None: The job ID of the training job or None if an error occurred.
    """
    ...
```

**Назначение**: Обучает модель на основе указанных данных или директории.

**Параметры**:

*   `data` (str, optional): Путь к CSV-файлу или CSV-форматированная строка с данными.
*   `data_dir` (Path | str, optional): Директория, содержащая CSV-файлы для обучения.
*   `data_file` (Path | str, optional): Путь к одному CSV-файлу с данными для обучения.
*   `positive` (bool, optional): Указывает, являются ли данные положительными или отрицательными. По умолчанию `True`.

**Возвращает**:

*   `str | None`: ID задачи обучения или `None`, если произошла ошибка.

**Как работает функция**:

1.  Загружает данные для обучения из указанного источника (CSV-файл или директория).
2.  Отправляет данные в OpenAI API для обучения модели.
3.  Возвращает ID задачи обучения или `None` в случае ошибки.

### `save_job_id`

```python
def save_job_id(self, job_id: str, description: str, filename: str = "job_ids.json"):
    """Save the job ID with description to a file.

    Args:
        job_id (str): The job ID to save.
        description (str): Description of the job.
        filename (str, optional): The file to save job IDs. Defaults to "job_ids.json".
    """
    ...
```

**Назначение**: Сохраняет ID задачи обучения с описанием в файл.

**Параметры**:

*   `job_id` (str): ID задачи, которую нужно сохранить.
*   `description` (str): Описание задачи.
*   `filename` (str, optional): Имя файла для сохранения ID задач. По умолчанию `"job_ids.json"`.

**Как работает функция**:

1.  Формирует словарь с информацией о задаче обучения (ID, описание, время создания).
2.  Сохраняет информацию в JSON-файл, добавляя ее к существующим данным, если файл уже существует.

## Функция `main`

```python
def main():
    """Main function to initialize the OpenAIModel and demonstrate usage.
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

        After training, the job ID is saved with a description to a JSON file.
    """
    
    # Initialize the model with system instructions and assistant ID (optional)
    model = OpenAIModel(system_instruction="You are a helpful assistant.", assistant_id="asst_dr5AgQnhhhnef5OSMzQ9zdk9")
    
    # Example of listing available models
    print("Available Models:")
    models = model.list_models
    pprint(models)

    # Example of listing available assistants
    print("\\nAvailable Assistants:")
    assistants = model.list_assistants
    pprint(assistants)

    # Example of asking the model a question
    user_input = "Hello, how are you?"
    print("\\nUser Input:", user_input)
    response = model.ask(user_input)
    print("Model Response:", response)

    # Example of dynamic training using past dialogue
    print("\\nPerforming dynamic training...")
    model.dynamic_train()

    # Example of training the model using provided data
    print("\\nTraining the model...")
    training_result = model.train(data_file=gs.path.google_drive / 'AI' / 'training_data.csv')
    print(f"Training job ID: {training_result}")

    # Example of saving a job ID
    if training_result:
        model.save_job_id(training_result, "Training model with new data", filename="job_ids.json")
        print(f"Saved training job ID: {training_result}")

    # Пример описания изображения
    image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
    print("\\nDescribing Image:")
    description = model.describe_image(image_path)
    print(f"Image description: {description}")
```

**Назначение**: Демонстрирует пример использования класса `OpenAIModel` для выполнения различных задач.

**Как работает функция**:

1.  Инициализирует объект `OpenAIModel`.
2.  Вызывает методы `list_models` и `list_assistants` для вывода доступных моделей и ассистентов.
3.  Задает вопрос и получает ответ от модели с помощью метода `ask`.
4.  Выполняет динамическое дообучение модели с помощью метода `dynamic_train`.
5.  Обучает модель с использованием данных из CSV-файла с помощью метода `train`.
6.  Сохраняет ID задачи обучения в файл с помощью метода `save_job_id`.
7.  Выполняет описание изображения с помощью метода `describe_image`.

## Зависимости

*   `openai`
*   `requests`
*   `Pillow` (PIL)
*   `io`
*   `src.utils.jjson`
*   `src.utils.csv`
*   `src.utils.printer`
*   `src.utils.convertors.base64`
*   `src.utils.convertors.md`
*   `src.logger.logger`

## Замечания

Модуль предоставляет функциональность для взаимодействия с OpenAI API, включая обучение моделей и выполнение различных задач. Однако стоит обратить внимание на обработку ошибок, которая может потребовать доработки для обеспечения стабильной работы. Также необходимо обеспечить безопасное хранение API-ключей.

```python
# ai Module: AI Model Management
```

Уберите эти строки - они не несут полезной нагрузки