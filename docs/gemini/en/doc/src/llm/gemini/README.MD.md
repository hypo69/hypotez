# Google Generative AI Integration Module

## Overview

The `GoogleGenerativeAi` class is designed to facilitate interaction with Google's Generative AI models. This class provides methods for sending queries, handling responses, managing dialogues, and integrating with various AI functionalities. It includes robust error handling, logging, and configuration options to ensure seamless operation.

## Table of Contents

- [Overview](#overview)
- [Key Functions](#key-functions)
    - [`__init__(self, api_key: str, model_name: Optional[str] = None, generation_config: Optional[Dict] = None, system_instruction: Optional[str] = None, **kwargs)`](#__init__self-api_key-str-model_name-optionalstr--none-generation_config-optionaldict--none-system_instruction-optionalstr--none-kwargs)
    - [`config()`](#config)
    - [`_start_chat(self)`](#_start_chatself)
    - [`_save_dialogue(self, dialogue: list)`](#_save_dialogueself-dialogue-list)
    - [`ask(self, q: str, attempts: int = 15) -> Optional[str]`](#askself-q-str-attempts-int--15--optionalstr)
    - [`chat(self, q: str) -> str`](#chatself-q-str--str)
    - [`describe_image(self, image_path: Path) -> Optional[str]`](#describe_imageself-image_path-path--optionalstr)
    - [`upload_file(self, file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`](#upload_fileself-file-str--path--iobase-file_name-optionalstr--none--bool)
- [Error Handling](#error-handling)
- [Logging and History](#logging-and-history)
- [Dependencies](#dependencies)
- [Usage Example](#usage-example)

## Key Functions

### `__init__(self, api_key: str, model_name: Optional[str] = None, generation_config: Optional[Dict] = None, system_instruction: Optional[str] = None, **kwargs)`

**Purpose**: Инициализирует класс `GoogleGenerativeAi` с необходимыми конфигурациями.

**Details**:
- Устанавливает API-ключ, имя модели, конфигурацию генерации и системные инструкции.
- Определяет пути для ведения журнала диалогов и хранения истории.
- Инициализирует модель Google Generative AI.

```python
def __init__(
    self,
    api_key: str,
    model_name: Optional[str] = None,
    generation_config: Optional[Dict] = None,
    system_instruction: Optional[str] = None,
    **kwargs
) -> None:
    """
    Инициализирует класс `GoogleGenerativeAi` с необходимыми конфигурациями.

    Args:
        api_key (str): API-ключ для доступа к модели Google Generative AI.
        model_name (Optional[str], optional): Имя модели Google Generative AI. По умолчанию `None`.
        generation_config (Optional[Dict], optional): Конфигурация генерации текста для модели. По умолчанию `None`.
        system_instruction (Optional[str], optional): Системные инструкции для модели. По умолчанию `None`.
        **kwargs: Дополнительные аргументы для инициализации.

    Returns:
        None
    """
    ...
```


### `config()`

**Purpose**: Извлекает конфигурацию из файла настроек.

**Details**:
- Читает и анализирует файл конфигурации, расположенный по адресу `gs.path.src / 'ai' / 'gemini' / 'gemini.json'`.

```python
def config(self) -> Dict:
    """
    Извлекает конфигурацию из файла настроек.

    Returns:
        Dict: Словарь с конфигурацией.
    """
    ...
```


### `_start_chat(self)`

**Purpose**: Начинает сеанс чата с моделью AI.

**Details**:
- Инициализирует сеанс чата с пустой историей.

```python
def _start_chat(self) -> None:
    """
    Начинает сеанс чата с моделью AI.

    Returns:
        None
    """
    ...
```


### `_save_dialogue(self, dialogue: list)`

**Purpose**: Сохраняет диалог в текстовые и JSON-файлы.

**Details**:
- Добавляет каждое сообщение в диалог в текстовый файл.
- Добавляет каждое сообщение в формате JSON в JSON-файл.

```python
def _save_dialogue(self, dialogue: list) -> None:
    """
    Сохраняет диалог в текстовые и JSON-файлы.

    Args:
        dialogue (list): Список сообщений в диалоге.

    Returns:
        None
    """
    ...
```


### `ask(self, q: str, attempts: int = 15) -> Optional[str]`

**Purpose**: Отправляет текстовый запрос в модель AI и получает ответ.

**Details**:
- Обрабатывает несколько попыток в случае сетевых ошибок или недоступности сервиса.
- Ведет журнал ошибок и повторяет попытки с экспоненциальным отступом.
- Сохраняет диалог в файлах истории.

```python
def ask(self, q: str, attempts: int = 15) -> Optional[str]:
    """
    Отправляет текстовый запрос в модель AI и получает ответ.

    Args:
        q (str): Текстовый запрос.
        attempts (int, optional): Количество попыток отправки запроса. По умолчанию 15.

    Returns:
        Optional[str]: Текстовый ответ модели AI, или `None` в случае ошибки.
    """
    ...
```


### `chat(self, q: str) -> str`

**Purpose**: Отправляет сообщение в чат модели AI и получает ответ.

**Details**:
- Использует сеанс чата, инициализированный с помощью `_start_chat`.
- Ведет журнал ошибок и возвращает текст ответа.

```python
def chat(self, q: str) -> str:
    """
    Отправляет сообщение в чат модели AI и получает ответ.

    Args:
        q (str): Сообщение для отправки в чат.

    Returns:
        str: Текстовый ответ модели AI.
    """
    ...
```


### `describe_image(self, image_path: Path) -> Optional[str]`

**Purpose**:  Генерирует текстовое описание изображения.

**Details**:
- Кодирует изображение в base64 и отправляет его в модель AI.
- Возвращает сгенерированное описание или записывает ошибку в журнал, если операция завершилась неудачей.

```python
def describe_image(self, image_path: Path) -> Optional[str]:
    """
    Генерирует текстовое описание изображения.

    Args:
        image_path (Path): Путь к изображению.

    Returns:
        Optional[str]: Текстовое описание изображения, или `None` в случае ошибки.
    """
    ...
```


### `upload_file(self, file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`

**Purpose**: Загружает файл в модель AI.

**Details**:
- Обрабатывает загрузку файлов и записывает в журнал о успехе или неудаче операции.
- Предоставляет логику повтора попыток в случае возникновения ошибок.

```python
def upload_file(self, file: str | Path | IOBase, file_name: Optional[str] = None) -> bool:
    """
    Загружает файл в модель AI.

    Args:
        file (str | Path | IOBase): Путь к файлу или объект файла.
        file_name (Optional[str], optional): Имя файла для загрузки. По умолчанию `None`.

    Returns:
        bool: `True`, если файл успешно загружен, иначе `False`.
    """
    ...
```

## Error Handling

The class includes comprehensive error handling for various scenarios:
- **Network Errors**: Retries with exponential backoff.
- **Service Unavailability**: Logs errors and retries.
- **Quota Limits**: Logs and waits before retrying.
- **Authentication Errors**: Logs and stops further attempts.
- **Invalid Input**: Logs and retries with a timeout.
- **API Errors**: Logs and stops further attempts.

## Logging and History

All interactions with the AI models are logged, and dialogues are saved in both text and JSON formats for future analysis. This ensures that all operations are traceable and can be reviewed for debugging or auditing purposes.

## Dependencies

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

## Usage Example

```python
ai = GoogleGenerativeAi(api_key="your_api_key", system_instruction="Instruction")
response = ai.ask("Как дела?")
print(response)
```

This example initializes the `GoogleGenerativeAi` class and sends a query to the AI model, printing the response.

---

For more detailed information, refer to the source code and comments within the `GoogleGenerativeAi` class.