# Модуль для работы с OpenAI API для обучения моделей
## Обзор

Модуль `src.ai.openai.model.training` предоставляет класс `OpenAIModel` для взаимодействия с OpenAI API, управления моделями и их обучения. Он включает в себя функциональность для отправки запросов к моделям, анализа тональности ответов, динамической донастройки моделей на основе истории диалогов и обучения моделей на новых данных.

## Подробней

Модуль предназначен для упрощения работы с OpenAI API, предоставляя удобные методы для выполнения различных задач, связанных с обучением и использованием моделей. Класс `OpenAIModel` инкапсулирует логику взаимодействия с API, обработки данных и управления моделями.

## Классы

### `OpenAIModel`

**Описание**: Класс для взаимодействия с OpenAI API и управления моделями.

**Атрибуты**:

- `model` (str): Имя используемой модели (по умолчанию "gpt-4o-mini").
- `client` (OpenAI): Клиент OpenAI для взаимодействия с API.
- `current_job_id` (str): Идентификатор текущей задачи обучения.
- `assistant_id` (str): Идентификатор используемого ассистента.
- `assistant` (Any): Объект ассистента, полученный из OpenAI API.
- `thread` (Any): Объект треда, используемый для взаимодействия с ассистентом.
- `system_instruction` (str): Системная инструкция для модели.
- `dialogue_log_path` (str | Path): Путь к файлу для сохранения истории диалогов.
- `dialogue` (List[Dict[str, str]]): Список словарей, содержащих историю диалогов.
- `assistants` (List[SimpleNamespace]): Список доступных ассистентов.
- `models_list` (List[str]): Список доступных моделей.

**Методы**:

- `__init__(api_key: str, system_instruction: str = None, model_name: str = 'gpt-4o-mini', assistant_id: str = None)`: Инициализирует объект `OpenAIModel`.
- `list_models() -> List[str]`: Динамически получает и возвращает список доступных моделей из OpenAI API.
- `list_assistants() -> List[str]`: Динамически загружает и возвращает список доступных ассистентов из JSON-файла.
- `set_assistant(assistant_id: str)`: Устанавливает ассистента, используя предоставленный ID.
- `_save_dialogue()`: Сохраняет историю диалогов в JSON-файл.
- `determine_sentiment(message: str) -> str`: Определяет тональность сообщения (положительную, отрицательную или нейтральную).
- `ask(message: str, system_instruction: str = None, attempts: int = 3) -> str`: Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.
- `describe_image(image_path: str | Path, prompt: Optional[str] = None, system_instruction: Optional[str] = None) -> str`: Описывает изображение, отправляя его в OpenAI API.
- `describe_image_by_requests(image_path: str | Path, prompt: str = None) -> str`: Отправляет изображение в OpenAI API и получает описание, используя библиотеку `requests`.
- `dynamic_train()`: Динамически дообучает модель на основе предыдущих диалогов.
- `train(data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None`: Обучает модель на указанных данных.
- `save_job_id(job_id: str, description: str, filename: str = "job_ids.json")`: Сохраняет ID задачи обучения с описанием в файл.

### `__init__`
```python
def __init__(self, api_key: str, system_instruction: str = None, model_name: str = 'gpt-4o-mini', assistant_id: str = None):
    """Инициализирует объект Model с API-ключом, ID ассистента и загружает доступные модели и ассистентов.

    Args:
        api_key (str): API-ключ для доступа к OpenAI API.
        system_instruction (str, optional): Необязательная системная инструкция для модели. По умолчанию `None`.
        model_name (str, optional): Имя модели для использования. По умолчанию 'gpt-4o-mini'.
        assistant_id (str, optional): Необязательный ID ассистента. По умолчанию берется из `gs.credentials.openai.assistant_id.code_assistant`.

    Пример:
        >>> model = OpenAIModel(api_key='YOUR_API_KEY', system_instruction='You are a helpful assistant.', assistant_id='asst_123')
    """
    # Установка клиента OpenAI с использованием предоставленного API-ключа или ключа по умолчанию из gs.credentials.openai.api_key
    self.client = OpenAI(api_key=api_key if api_key else gs.credentials.openai.api_key)
    # Инициализация идентификатора текущей задачи как None
    self.current_job_id = None
    # Установка идентификатора ассистента с использованием предоставленного значения или значения по умолчанию из gs.credentials.openai.assistant_id.code_assistant
    self.assistant_id = assistant_id or gs.credentials.openai.assistant_id.code_assistant
    # Установка системной инструкции
    self.system_instruction = system_instruction

    # Загрузка ассистента и создание треда
    self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
    self.thread = self.client.beta.threads.create()
```

### `list_models`

```python
    @property
    def list_models(self) -> List[str]:
        """Динамически получает и возвращает доступные модели из OpenAI API.

        Returns:
            List[str]: Список идентификаторов моделей, доступных через OpenAI API.

        Raises:
            Exception: Если возникает ошибка при загрузке моделей.

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> models = model.list_models
            >>> print(models)
            ['gpt-4o', 'gpt-3.5-turbo', ...]
        """
        try:
            # Получение списка моделей из OpenAI API
            models = self.client.models.list()
            # Извлечение идентификаторов моделей из полученных данных
            model_list = [model['id'] for model in models['data']]
            # Логирование списка загруженных моделей
            logger.info(f"Loaded models: {model_list}")
            # Возврат списка моделей
            return model_list
        except Exception as ex:
            # Логирование ошибки, если она произошла
            logger.error("An error occurred while loading models:", ex)
            # Возврат пустого списка в случае ошибки
            return []
```

### `list_assistants`

```python
    @property
    def list_assistants(self) -> List[str]:
        """Динамически загружает доступных ассистентов из JSON-файла.

        Returns:
            List[str]: Список имен ассистентов.

        Raises:
            Exception: Если возникает ошибка при загрузке ассистентов.

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> assistants = model.list_assistants
            >>> print(assistants)
            ['Code Assistant', 'Data Analyzer', ...]
        """
        try:
            # Загрузка ассистентов из JSON-файла
            self.assistants = j_loads_ns(gs.path.src / 'ai' / 'openai' / 'model' / 'assistants' / 'assistants.json')
            # Извлечение имен ассистентов из загруженных данных
            assistant_list = [assistant.name for assistant in self.assistants]
            # Логирование списка загруженных ассистентов
            logger.info(f"Loaded assistants: {assistant_list}")
            # Возврат списка ассистентов
            return assistant_list
        except Exception as ex:
            # Логирование ошибки, если она произошла
            logger.error("An error occurred while loading assistants:", ex)
            # Возврат пустого списка в случае ошибки
            return []
```

### `set_assistant`

```python
    def set_assistant(self, assistant_id: str):
        """Устанавливает ассистента, используя предоставленный ID.

        Args:
            assistant_id (str): ID ассистента, которого нужно установить.

        Raises:
            Exception: Если возникает ошибка при установке ассистента.

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> model.set_assistant('asst_123')
            >>> print(model.assistant_id)
            asst_123
        """
        try:
            # Установка идентификатора ассистента
            self.assistant_id = assistant_id
            # Получение объекта ассистента из OpenAI API
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
            # Логирование успешной установки ассистента
            logger.info(f"Assistant set successfully: {assistant_id}")
        except Exception as ex:
            # Логирование ошибки, если она произошла
            logger.error("An error occurred while setting the assistant:", ex)
```

### `_save_dialogue`

```python
    def _save_dialogue(self):
        """Сохраняет историю диалогов в JSON-файл."""
        # Используем j_dumps для сохранения истории диалогов в файл
        j_dumps(self.dialogue, self.dialogue_log_path)
```

### `determine_sentiment`

```python
    def determine_sentiment(self, message: str) -> str:
        """Определяет тональность сообщения (положительную, отрицательную или нейтральную).

        Args:
            message (str): Сообщение для анализа.

        Returns:
            str: Тональность ('positive', 'negative' или 'neutral').

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> model.determine_sentiment('This is a great product!')
            'positive'
            >>> model.determine_sentiment('I hate this.')
            'negative'
            >>> model.determine_sentiment('It's okay.')
            'neutral'
        """
        # Списки ключевых слов для определения тональности
        positive_words = ["good", "great", "excellent", "happy", "love", "wonderful", "amazing", "positive"]
        negative_words = ["bad", "terrible", "hate", "sad", "angry", "horrible", "negative", "awful"]
        neutral_words = ["okay", "fine", "neutral", "average", "moderate", "acceptable", "sufficient"]

        # Приведение сообщения к нижнему регистру для упрощения анализа
        message_lower = message.lower()

        # Проверка наличия положительных слов в сообщении
        if any(word in message_lower for word in positive_words):
            return "positive"
        # Проверка наличия отрицательных слов в сообщении
        elif any(word in message_lower for word in negative_words):
            return "negative"
        # Проверка наличия нейтральных слов в сообщении
        elif any(word in message_lower for word in neutral_words):
            return "neutral"
        # Если не найдено ключевых слов, возвращается нейтральная тональность
        else:
            return "neutral"
```

### `ask`

```python
    def ask(self, message: str, system_instruction: str = None, attempts: int = 3) -> str:
        """Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.

        Args:
            message (str): Сообщение для отправки модели.
            system_instruction (str, optional): Необязательная системная инструкция. По умолчанию `None`.
            attempts (int, optional): Количество попыток повтора запроса. По умолчанию 3.

        Returns:
            str: Ответ от модели.

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> model.ask('Hello, how are you?')
            'I am doing well, thank you for asking.'
        """
        try:
            messages = []
            # Если предоставлена системная инструкция или она уже установлена
            if self.system_instruction or system_instruction:
                # Экранирование кавычек в системной инструкции
                system_instruction_escaped = (system_instruction or self.system_instruction).replace('"', r'\"')
                # Добавление системной инструкции в список сообщений
                messages.append({"role": "system", "content": system_instruction_escaped})

            # Экранирование кавычек в сообщении пользователя
            message_escaped = message.replace('"', r'\"')
            # Добавление сообщения пользователя в список сообщений
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
            # Извлечение ответа из полученных данных
            reply = response.choices[0].message.content.strip()

            # Анализ тональности ответа
            sentiment = self.determine_sentiment(reply)

            # Добавление сообщений и тональности в историю диалогов
            self.dialogue.append({"role": "system", "content": system_instruction or self.system_instruction})
            self.dialogue.append({"role": "user", "content": message_escaped})
            self.dialogue.append({"role": "assistant", "content": reply, "sentiment": sentiment})

            # Сохранение истории диалогов
            self._save_dialogue()

            # Возврат ответа
            return reply
        except Exception as ex:
            # Логирование ошибки, если она произошла
            logger.debug(f"An error occurred while sending the message: \n-----\n {pprint(messages)} \n-----\n", ex, True)
            # Пауза перед повторной попыткой
            time.sleep(3)
            # Повторная попытка, если количество попыток не исчерпано
            if attempts > 0:
                return self.ask(message, attempts - 1)
            # Возврат None, если все попытки исчерпаны
            return 
```

### `describe_image`

```python
def describe_image(self, image_path: str | Path, prompt: Optional[str] = None, system_instruction: Optional[str] = None) -> str:
    """Описывает изображение, отправляя его в OpenAI API.

    Args:
        image_path (str | Path): Путь к изображению.
        prompt (Optional[str], optional): Дополнительный запрос для описания изображения. По умолчанию `None`.
        system_instruction (Optional[str], optional): Системная инструкция для модели. По умолчанию `None`.

    Returns:
        str: Описание изображения.
    """
    ...

    # Инициализация списка сообщений для отправки в OpenAI API
    messages: list = []
    # Кодирование изображения в формат base64
    base64_image = base64encode(image_path)

    # Если предоставлена системная инструкция, добавляем ее в список сообщений
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})

    # Формирование сообщения с запросом на описание изображения
    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt if prompt else "What's in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        }
    )
    try:
        # Отправка запроса в OpenAI API для получения описания изображения
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            max_tokens=800,
        )

        # Сохранение ответа
        reply = response
        ...
        try:
            # Извлечение и обработка ответа от OpenAI API
            raw_reply = response.choices[0].message.content.strip()
            return j_loads_ns(raw_reply)
        except Exception as ex:
            # Логирование ошибки при обработке ответа
            logger.error(f"Trouble in reponse {response}", ex, True)
            ...
            return

    except Exception as ex:
        # Логирование ошибки при отправке запроса в OpenAI API
        logger.error(f"Ошибка openai", ex, True)
        ...
        return
```

### `describe_image_by_requests`

```python
    def describe_image_by_requests(self, image_path: str | Path, prompt:str = None) -> str:
        """Отправляет изображение в OpenAI API и получает описание, используя библиотеку `requests`.

        Args:
            image_path (str | Path): Путь к изображению.
            prompt (str, optional): Запрос для описания изображения. По умолчанию `None`.

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> model.describe_image_by_requests('path/to/image.jpg', prompt='Describe the scene.')
            {'description': 'The image shows a...', 'objects': [...]}
        """
        # Кодирование изображения в base64
        base64_image = base64encode(image_path)

        # Заголовки для HTTP-запроса
        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {gs.credentials.openai.project_api}"
        }

        # Формирование тела запроса
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
            # Отправка POST-запроса в OpenAI API
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            # Преобразование ответа в JSON
            response_json = response.json()
            ...
        except Exception as ex:
            # Логирование ошибки, если она произошла
            logger.error(f"Error in image description {image_path=}\\n", ex)
```

### `dynamic_train`

```python
    def dynamic_train(self):
        """Динамически дообучает модель на основе предыдущих диалогов.

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> model.dynamic_train()
        """
        try:
            # Загрузка истории диалогов из файла
            messages = j_loads(gs.path.google_drive / 'AI' / 'conversation' / 'dailogue.json')

            # Если история диалогов не пуста
            if messages:
                # Отправка запроса в OpenAI API для дообучения модели
                response = self.client.chat.completions.create(
                    model=self.model,
                    assistant=self.assistant_id,
                    messages=messages,
                    temperature=0,
                )
                # Логирование успешного дообучения
                logger.info("Fine-tuning during the conversation was successful.")
            else:
                # Логирование отсутствия истории диалогов
                logger.info("No previous dialogue found for fine-tuning.")
        except Exception as ex:
            # Логирование ошибки, если она произошла
            logger.error(f"Error during dynamic fine-tuning: {ex}")
```

### `train`

```python
    def train(self, data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None:
        """Обучает модель на указанных данных.

        Args:
            data (str, optional): Путь к CSV-файлу или CSV-форматированная строка с данными.
            data_dir (Path | str, optional): Директория, содержащая CSV-файлы для обучения.
            data_file (Path | str, optional): Путь к одному CSV-файлу с данными для обучения.
            positive (bool, optional): Определяет, являются ли данные позитивными или негативными. По умолчанию `True`.

        Returns:
            str | None: ID задачи обучения или `None`, если произошла ошибка.

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> model.train(data_file='path/to/training_data.csv')
            'training_job_id'
        """
        # Если не указана директория с данными, используется директория по умолчанию
        if not data_dir:
            data_dir = gs.path.google_drive / 'AI' / 'training'

        try:
            # Загрузка данных из файла или директории
            documents = j_loads(data if data else data_file if data_file else data_dir)

            # Отправка запроса в OpenAI API для обучения модели
            response = self.client.Training.create(
                model=self.model,
                documents=documents,
                labels=["positive" if positive else "negative"] * len(documents),
                show_progress=True
            )
            # Сохранение ID задачи обучения
            self.current_job_id = response.id
            # Возврат ID задачи обучения
            return response.id

        except Exception as ex:
            # Логирование ошибки, если она произошла
            logger.error("An error occurred during training:", ex)
            # Возврат None в случае ошибки
            return
```

### `save_job_id`

```python
    def save_job_id(self, job_id: str, description: str, filename: str = "job_ids.json"):
        """Сохраняет ID задачи обучения с описанием в файл.

        Args:
            job_id (str): ID задачи обучения.
            description (str): Описание задачи.
            filename (str, optional): Имя файла для сохранения ID задач. По умолчанию "job_ids.json".

        Пример:
            >>> model = OpenAIModel(api_key='YOUR_API_KEY')
            >>> model.save_job_id('job_123', 'Training model with new data')
        """
        # Формирование данных для сохранения
        job_data = {"id": job_id, "description": description, "created": time.time()}
        # Определение пути к файлу для сохранения данных
        job_file = gs.path.google_drive / filename

        # Если файл не существует, создаем его и сохраняем данные
        if not job_file.exists():
            j_dumps([job_data], job_file)
        # Если файл существует, добавляем новые данные к существующим
        else:
            existing_jobs = j_loads(job_file)
            existing_jobs.append(job_data)
            j_dumps(existing_jobs, job_file)
```

## Функции

### `main`

```python
def main():
    """Основная функция для инициализации OpenAIModel и демонстрации использования.
    
    Объяснение:
        Инициализация модели:

        OpenAIModel инициализируется с системной инструкцией и ID ассистента (опционально). Вы можете изменить параметры при необходимости.
        Вывод списка моделей и ассистентов:

        Методы list_models и list_assistants вызываются для вывода доступных моделей и ассистентов.
        Запрос модели:

        Метод ask() используется для отправки сообщения модели и получения ответа.
        Динамическое обучение:

        Метод dynamic_train() выполняет динамическое дообучение на основе истории диалогов.
        Обучение модели:

        Метод train() обучает модель, используя данные из указанного файла (в данном случае, 'training_data.csv').
        Сохранение ID задачи обучения:

        После обучения, ID задачи сохраняется с описанием в JSON-файл.
    """
    
    # Инициализация модели с системными инструкциями и ID ассистента (опционально)
    model = OpenAIModel(system_instruction="You are a helpful assistant.", assistant_id="asst_dr5AgQnhhhnef5OSMzQ9zdk9")
    
    # Пример вывода списка доступных моделей
    print("Available Models:")
    models = model.list_models
    pprint(models)

    # Пример вывода списка доступных ассистентов
    print("\nAvailable Assistants:")
    assistants = model.list_assistants
    pprint(assistants)

    # Пример запроса модели
    user_input = "Hello, how are you?"
    print("\nUser Input:", user_input)
    response = model.ask(user_input)
    print("Model Response:", response)

    # Пример динамического обучения с использованием истории диалогов
    print("\nPerforming dynamic training...")
    model.dynamic_train()

    # Пример обучения модели с использованием предоставленных данных
    print("\nTraining the model...")
    training_result = model.train(data_file=gs.path.google_drive / 'AI' / 'training_data.csv')
    print(f"Training job ID: {training_result}")

    # Пример сохранения ID задачи
    if training_result:
        model.save_job_id(training_result, "Training model with new data", filename="job_ids.json")
        print(f"Saved training job ID: {training_result}")

    # Пример описания изображения
    image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
    print("\nDescribing Image:")
    description = model.describe_image(image_path)
    print(f"Image description: {description}")
```

## Примеры

### Инициализация и использование `OpenAIModel`

```python
from src.ai.openai.model.training import OpenAIModel
from pathlib import Path

# Инициализация модели с API-ключом и системной инструкцией
model = OpenAIModel(api_key='YOUR_API_KEY', system_instruction='You are a helpful assistant.')

# Получение списка доступных моделей
models = model.list_models

# Получение списка доступных ассистентов
assistants = model.list_assistants

# Отправка сообщения модели и получение ответа
response = model.ask('Hello, how are you?')

# Обучение модели на данных из файла
training_result = model.train(data_file=Path('/path/to/training_data.csv'))

# Сохранение ID задачи обучения
if training_result:
    model.save_job_id(training_result, 'Training model with new data')