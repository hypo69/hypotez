# Модуль интеграции Google Generative AI

## Обзор

Класс `GoogleGenerativeAI` предназначен для взаимодействия с моделями Google Generative AI. Этот класс предоставляет методы для отправки запросов, обработки ответов, управления диалогами и интеграции с различными функциональностями ИИ. Он включает в себя надежную обработку ошибок, ведение журнала и настройки конфигурации для обеспечения беспрепятственной работы.

## Подробнее

Этот модуль обеспечивает интеграцию с Google Generative AI, позволяя отправлять текстовые запросы, вести диалоги, описывать изображения и загружать файлы. Он разработан для обеспечения отказоустойчивости и удобства использования, с акцентом на ведение журнала и обработку ошибок.

## Классы

### `GoogleGenerativeAI`

**Описание**: Класс для взаимодействия с моделями Google Generative AI.

**Атрибуты**:
- `api_key` (str): Ключ API для доступа к сервисам Google Generative AI.
- `model_name` (Optional[str]): Имя используемой модели (по умолчанию `None`).
- `generation_config` (Optional[Dict]): Конфигурация генерации (по умолчанию `None`).
- `system_instruction` (Optional[str]): Системная инструкция для модели (по умолчанию `None`).

**Методы**:
- `__init__`: Инициализирует класс `GoogleGenerativeAI`.
- `config`: Получает конфигурацию из файла настроек.
- `_start_chat`: Запускает сессию чата с моделью ИИ.
- `_save_dialogue`: Сохраняет диалог в текстовые и JSON файлы.
- `ask`: Отправляет текстовый запрос модели ИИ и получает ответ.
- `chat`: Отправляет сообщение чата модели ИИ и получает ответ.
- `describe_image`: Генерирует текстовое описание изображения.
- `upload_file`: Загружает файл в модель ИИ.

**Принцип работы**:
Класс `GoogleGenerativeAI` предоставляет интерфейс для взаимодействия с моделями Google Generative AI. При инициализации класса задаются необходимые параметры, такие как API-ключ, имя модели и системные инструкции. Методы класса позволяют отправлять запросы, вести диалоги, описывать изображения и загружать файлы. Все взаимодействия ведутся в журнале и сохраняются для последующего анализа.

## Методы класса

### `__init__`

```python
def __init__(self, api_key: str, model_name: Optional[str] = None, generation_config: Optional[Dict] = None, system_instruction: Optional[str] = None, **kwargs)
```

**Назначение**: Инициализирует экземпляр класса `GoogleGenerativeAI`.

**Параметры**:
- `api_key` (str): Ключ API для доступа к сервисам Google Generative AI.
- `model_name` (Optional[str], optional): Имя используемой модели. По умолчанию `None`.
- `generation_config` (Optional[Dict], optional): Конфигурация генерации. По умолчанию `None`.
- `system_instruction` (Optional[str], optional): Системная инструкция для модели. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Примеры**:

```python
ai = GoogleGenerativeAI(api_key="your_api_key", system_instruction="Instruction")
```

### `config`

```python
def config()
```

**Назначение**: Получает конфигурацию из файла настроек.

**Возвращает**:
- `dict`: Словарь с конфигурационными параметрами.

**Примеры**:

```python
config_data = GoogleGenerativeAI.config()
```

### `_start_chat`

```python
def _start_chat(self)
```

**Назначение**: Запускает сессию чата с моделью ИИ.

**Примеры**:

```python
ai._start_chat()
```

### `_save_dialogue`

```python
def _save_dialogue(self, dialogue: list)
```

**Назначение**: Сохраняет диалог в текстовые и JSON файлы.

**Параметры**:
- `dialogue` (list): Список сообщений в диалоге.

**Примеры**:

```python
dialogue = ["Привет", "Как дела?"]
ai._save_dialogue(dialogue)
```

### `ask`

```python
def ask(self, q: str, attempts: int = 15) -> Optional[str]
```

**Назначение**: Отправляет текстовый запрос модели ИИ и получает ответ.

**Параметры**:
- `q` (str): Текстовый запрос.
- `attempts` (int, optional): Количество попыток в случае ошибки. По умолчанию 15.

**Возвращает**:
- `Optional[str]`: Ответ модели ИИ или `None` в случае неудачи.

**Вызывает исключения**:
- `Exception`: В случае ошибок при отправке запроса.

**Примеры**:

```python
response = ai.ask("Как дела?")
print(response)
```

### `chat`

```python
def chat(self, q: str) -> str
```

**Назначение**: Отправляет сообщение чата модели ИИ и получает ответ.

**Параметры**:
- `q` (str): Сообщение чата.

**Возвращает**:
- `str`: Ответ модели ИИ.

**Примеры**:

```python
response = ai.chat("Привет")
print(response)
```

### `describe_image`

```python
def describe_image(self, image_path: Path) -> Optional[str]
```

**Назначение**: Генерирует текстовое описание изображения.

**Параметры**:
- `image_path` (Path): Путь к файлу изображения.

**Возвращает**:
- `Optional[str]`: Текстовое описание изображения или `None` в случае неудачи.

**Вызывает исключения**:
- `Exception`: В случае ошибок при обработке изображения.

**Примеры**:

```python
image_description = ai.describe_image(Path("path/to/image.jpg"))
print(image_description)
```

### `upload_file`

```python
def upload_file(self, file: str | Path | IOBase, file_name: Optional[str] = None) -> bool
```

**Назначение**: Загружает файл в модель ИИ.

**Параметры**:
- `file` (str | Path | IOBase): Путь к файлу, объект Path или объект IOBase.
- `file_name` (Optional[str], optional): Имя файла. По умолчанию `None`.

**Возвращает**:
- `bool`: `True` в случае успеха, `False` в случае неудачи.

**Вызывает исключения**:
- `Exception`: В случае ошибок при загрузке файла.

**Примеры**:

```python
success = ai.upload_file("path/to/file.txt")
print(success)
```

## Параметры класса

- `api_key` (str): Ключ API для доступа к сервисам Google Generative AI.
- `model_name` (Optional[str]): Имя используемой модели (по умолчанию `None`).
- `generation_config` (Optional[Dict]): Конфигурация генерации (по умолчанию `None`).
- `system_instruction` (Optional[str]): Системная инструкция для модели (по умолчанию `None`).

## Примеры

```python
ai = GoogleGenerativeAI(api_key="your_api_key", system_instruction="Instruction")
response = ai.ask("Как дела?")
print(response)
```
```python
config_data = GoogleGenerativeAI.config()
```
```python
dialogue = ["Привет", "Как дела?"]
ai._save_dialogue(dialogue)
```
```python
image_description = ai.describe_image(Path("path/to/image.jpg"))
print(image_description)
```
```python
success = ai.upload_file("path/to/file.txt")
print(success)
```