# Модуль OpenAI Model

## Обзор

Модуль `src.ai.openai.model.training.py` предоставляет класс `OpenAIModel` для взаимодействия с API OpenAI и управления моделью. Он позволяет отправлять запросы к модели, получать ответы, анализировать тональность ответов и выполнять обучение модели.

## Подробней

Модуль предназначен для работы с моделями OpenAI, такими как `gpt-4o-mini` или `gpt-4o-2024-08-06`. Он предоставляет классы и функции для инициализации модели, отправки запросов, анализа ответов и обучения модели. Модуль использует библиотеку `openai` для взаимодействия с API OpenAI.

## Классы

### `OpenAIModel`

**Описание**: Класс для взаимодействия с API OpenAI и управления моделью.

**Наследует**: Не наследует.

**Атрибуты**:

- `model` (str): Идентификатор модели OpenAI (например, `gpt-4o-mini`).
- `client` (OpenAI): Объект `OpenAI` для взаимодействия с API.
- `current_job_id` (str): ID текущей задачи обучения.
- `assistant_id` (str): ID ассистента.
- `assistant` (SimpleNamespace): Объект, представляющий ассистента.
- `thread` (SimpleNamespace): Объект, представляющий поток диалога.
- `system_instruction` (str): Системная инструкция для модели.
- `dialogue_log_path` (str | Path): Путь к файлу для сохранения диалога.
- `dialogue` (List[Dict[str, str]]): Список сообщений в диалоге.
- `assistants` (List[SimpleNamespace]): Список ассистентов.
- `models_list` (List[str]): Список доступных моделей.

**Методы**:

- `__init__(self, api_key:str, system_instruction: str = None, model_name:str = \'gpt-4o-mini\', assistant_id: str = None)`: Инициализирует объект модели с API-ключом, идентификатором ассистента и загружает доступные модели и ассистентов.
- `list_models(self) -> List[str]`: Получает список доступных моделей OpenAI.
- `list_assistants(self) -> List[str]`: Загружает список доступных ассистентов из файла `assistants.json`.
- `set_assistant(self, assistant_id: str)`: Устанавливает ассистента, используя предоставленный идентификатор.
- `_save_dialogue(self)`: Сохраняет весь диалог в файл JSON.
- `determine_sentiment(self, message: str) -> str`: Определяет тональность сообщения (положительная, отрицательная или нейтральная).
- `ask(self, message: str, system_instruction: str = None, attempts: int = 3) -> str`: Отправляет сообщение модели и возвращает ответ.
- `describe_image(self, image_path: str | Path, prompt:Optional[str] = None, system_instruction:Optional[str] = None ) -> str`: Описывает изображение.
- `describe_image_by_requests(self, image_path: str | Path, prompt:str = None) -> str`: Отправляет изображение в API OpenAI и получает описание.
- `dynamic_train(self)`: Загружает предыдущий диалог и выполняет тонкую настройку модели на основе него.
- `train(self, data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None`: Обучает модель на указанных данных или директории.
- `save_job_id(self, job_id: str, description: str, filename: str = "job_ids.json")`: Сохраняет ID задачи обучения с описанием в файл.

## Функции

### `main()`

**Назначение**: Главная функция для инициализации модели OpenAI и демонстрации ее использования.

**Параметры**: Нет

**Возвращает**: Нет

**Вызывает исключения**: Нет

**Пример**:

```python
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

# Example of describing an image
image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
print("\nDescribing Image:")
description = model.describe_image(image_path)
print(f"Image description: {description}")