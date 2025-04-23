# Модуль интеграции Google Generative AI

## Обзор

Класс `GoogleGenerativeAi` предназначен для взаимодействия с моделями Google Generative AI. Этот класс предоставляет методы для отправки запросов, обработки ответов, управления диалогами и интеграции с различными функциональностями ИИ. Он включает в себя надежную обработку ошибок, ведение журнала и настройки конфигурации для обеспечения беспрепятственной работы.

## Подробнее

Модуль предоставляет интеграцию с Google Generative AI, обеспечивая удобный интерфейс для взаимодействия с ИИ моделями. Он включает в себя функциональность для текстовых запросов, чата, описания изображений и загрузки файлов. Модуль разработан с учетом надежной обработки ошибок, ведения журнала и возможности настройки конфигурации.

## Классы

### `GoogleGenerativeAi`

**Описание**: Класс для взаимодействия с моделями Google Generative AI.

**Атрибуты**:
- `api_key` (str): Ключ API для доступа к сервисам Google Generative AI.
- `model_name` (Optional[str]): Имя используемой модели. По умолчанию `None`.
- `generation_config` (Optional[Dict]): Конфигурация генерации для модели. По умолчанию `None`.
- `system_instruction` (Optional[str]): Системная инструкция для модели. По умолчанию `None`.

**Методы**:
- `__init__(...)`: Инициализирует класс `GoogleGenerativeAi`.
- `config()`: Получает конфигурацию из файла настроек.
- `_start_chat()`: Запускает сессию чата с моделью ИИ.
- `_save_dialogue(dialogue: list)`: Сохраняет диалог в текстовые и JSON файлы.
- `ask(q: str, attempts: int = 15)`: Отправляет текстовый запрос модели ИИ и получает ответ.
- `chat(q: str)`: Отправляет сообщение чата модели ИИ и получает ответ.
- `describe_image(image_path: Path)`: Генерирует текстовое описание изображения.
- `upload_file(file: str | Path | IOBase, file_name: Optional[str] = None)`: Загружает файл в модель ИИ.

## Методы класса

### `__init__`

```python
def __init__(self, api_key: str, model_name: Optional[str] = None, generation_config: Optional[Dict] = None, system_instruction: Optional[str] = None, **kwargs)
```

**Назначение**: Инициализирует класс `GoogleGenerativeAi` с необходимыми конфигурациями.

**Параметры**:
- `api_key` (str): Ключ API для доступа к сервисам Google Generative AI.
- `model_name` (Optional[str], optional): Имя используемой модели. По умолчанию `None`.
- `generation_config` (Optional[Dict], optional): Конфигурация генерации для модели. По умолчанию `None`.
- `system_instruction` (Optional[str], optional): Системная инструкция для модели. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры конфигурации.

**Как работает функция**:
- Функция устанавливает ключ API, имя модели, конфигурацию генерации и системную инструкцию.
- Определяет пути для ведения журнала диалогов и хранения истории.
- Инициализирует модель Google Generative AI.

**Примеры**:
```python
ai = GoogleGenerativeAi(api_key="your_api_key", system_instruction="Instruction")
```

### `config`

```python
def config(self)
```

**Назначение**: Получает конфигурацию из файла настроек.

**Как работает функция**:
- Функция читает и разбирает файл конфигурации, расположенный по пути `gs.path.src / 'ai' / 'gemini' / 'gemini.json'`.

**Примеры**:
```python
ai = GoogleGenerativeAi(api_key="your_api_key")
config = ai.config()
```

### `_start_chat`

```python
def _start_chat(self)
```

**Назначение**: Запускает сессию чата с моделью ИИ.

**Как работает функция**:
- Функция инициализирует сессию чата с пустой историей.

**Примеры**:
```python
ai = GoogleGenerativeAi(api_key="your_api_key")
ai._start_chat()
```

### `_save_dialogue`

```python
def _save_dialogue(self, dialogue: list)
```

**Назначение**: Сохраняет диалог в текстовые и JSON файлы.

**Параметры**:
- `dialogue` (list): Список сообщений для сохранения.

**Как работает функция**:
- Функция добавляет каждое сообщение в диалоге в текстовый файл.
- Добавляет каждое сообщение в формате JSON в JSON файл.

**Примеры**:
```python
ai = GoogleGenerativeAi(api_key="your_api_key")
dialogue = ["Привет!", "Как дела?"]
ai._save_dialogue(dialogue)
```

### `ask`

```python
def ask(self, q: str, attempts: int = 15) -> Optional[str]
```

**Назначение**: Отправляет текстовый запрос модели ИИ и получает ответ.

**Параметры**:
- `q` (str): Текст запроса.
- `attempts` (int, optional): Максимальное количество попыток в случае ошибки. По умолчанию `15`.

**Возвращает**:
- `Optional[str]`: Ответ от модели ИИ или `None` в случае неудачи.

**Как работает функция**:
- Функция обрабатывает несколько попыток в случае ошибок сети или недоступности сервиса.
- Ведет журнал ошибок и повторяет попытки с экспоненциальной задержкой.
- Сохраняет диалог в файлы истории.

**Примеры**:
```python
ai = GoogleGenerativeAi(api_key="your_api_key")
response = ai.ask("Как дела?")
print(response)
```

### `chat`

```python
def chat(self, q: str) -> str
```

**Назначение**: Отправляет сообщение чата модели ИИ и получает ответ.

**Параметры**:
- `q` (str): Текст сообщения для отправки в чат.

**Возвращает**:
- `str`: Ответ от модели ИИ.

**Как работает функция**:
- Функция использует сессию чата, инициализированную методом `_start_chat`.
- Ведет журнал ошибок и возвращает текст ответа.

**Примеры**:
```python
ai = GoogleGenerativeAi(api_key="your_api_key")
response = ai.chat("Как дела?")
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
- `Optional[str]`: Сгенерированное описание изображения или `None` в случае ошибки.

**Как работает функция**:
- Функция кодирует изображение в base64 и отправляет его модели ИИ.
- Возвращает сгенерированное описание или ведет журнал ошибки, если операция не удалась.

**Примеры**:
```python
from pathlib import Path
ai = GoogleGenerativeAi(api_key="your_api_key")
image_path = Path("path/to/image.jpg")
description = ai.describe_image(image_path)
print(description)
```

### `upload_file`

```python
def upload_file(self, file: str | Path | IOBase, file_name: Optional[str] = None) -> bool
```

**Назначение**: Загружает файл в модель ИИ.

**Параметры**:
- `file` (str | Path | IOBase): Путь к файлу, объект Path или файловый объект.
- `file_name` (Optional[str], optional): Имя файла. По умолчанию `None`.

**Возвращает**:
- `bool`: `True`, если загрузка прошла успешно, `False` в противном случае.

**Как работает функция**:
- Функция обрабатывает загрузку файла и ведет журнал успеха или неудачи.
- Предоставляет логику повторных попыток в случае ошибок.

**Примеры**:
```python
from pathlib import Path
ai = GoogleGenerativeAi(api_key="your_api_key")
file_path = Path("path/to/file.txt")
success = ai.upload_file(file_path)
print(success)
```

## Обработка ошибок

Класс включает в себя комплексную обработку ошибок для различных сценариев:
- **Ошибки сети**: Повторяет попытки с экспоненциальной задержкой.
- **Недоступность сервиса**: Ведет журнал ошибок и повторяет попытки.
- **Лимиты квот**: Ведет журнал и ждет перед повторной попыткой.
- **Ошибки аутентификации**: Ведет журнал и прекращает дальнейшие попытки.
- **Неверный ввод**: Ведет журнал и повторяет попытки с таймаутом.
- **Ошибки API**: Ведет журнал и прекращает дальнейшие попытки.

## Ведение журнала и история

Все взаимодействия с моделями ИИ ведутся в журнале, и диалоги сохраняются как в текстовых, так и в JSON форматах для последующего анализа. Это обеспечивает отслеживаемость всех операций и возможность их просмотра для отладки или аудита.

## Зависимости

- `google.generativeai`
- `requests`
- `grpc`
- `google.api_core.exceptions`
- `google.auth.exceptions`
- `src.logger`
- `src.utils.printer`
- `src.utils.file`
- `src.utils.date_time`
- `src.utils.convertors.unicode`
- `src.utils.jjson`

## Пример использования

```python
ai = GoogleGenerativeAi(api_key="your_api_key", system_instruction="Instruction")
response = ai.ask("Как дела?")
print(response)
```

Этот пример инициализирует класс `GoogleGenerativeAi` и отправляет запрос модели ИИ, выводя ответ.

---

Для получения более подробной информации обратитесь к исходному коду и комментариям внутри класса `GoogleGenerativeAi`.