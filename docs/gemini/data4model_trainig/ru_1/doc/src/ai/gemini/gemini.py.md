# Модуль для взаимодействия с Google Gemini

## Обзор

Модуль `gemini.py` предназначен для интеграции с моделями Google Generative AI. Он содержит класс `GoogleGenerativeAi`, который позволяет взаимодействовать с различными моделями Gemini, отправлять текстовые запросы, загружать файлы и описывать изображения.

## Подробней

Этот модуль обеспечивает удобный интерфейс для работы с Google Gemini, предоставляя методы для инициализации модели, отправки запросов, управления историей чата и обработки ответов. Он также включает обработку ошибок и повторные попытки для обеспечения надежности взаимодействия с API.

## Классы

### `Config`

**Описание**:
Не реализован. Используется как заполнитель.

### `GoogleGenerativeAi`

**Описание**:
Класс для взаимодействия с моделями Google Generative AI.

**Атрибуты**:
- `api_key` (str): Ключ API для доступа к Google Generative AI.
- `model_name` (str): Имя используемой модели Gemini. По умолчанию "gemini-2.0-flash-exp".
- `dialogue_txt_path` (Path): Путь к файлу для записи логов диалогов.
- `generation_config` (Dict): Конфигурация генерации ответов. По умолчанию `{"response_mime_type": "text/plain"}`.
- `system_instruction` (Optional[str]): Системная инструкция для модели.
- `history_dir` (Path): Путь к директории для хранения истории чата.
- `history_txt_file` (Path): Путь к текстовому файлу для хранения истории чата.
- `history_json_file` (Path): Путь к JSON файлу для хранения истории чата.
- `config` (SimpleNamespace): Конфигурация, загруженная из `gemini.json`.
- `chat_history` (List[Dict]): История чата в виде списка словарей.
- `model` (Any): Объект модели Gemini.
- `_chat` (Any): Объект чата.
- `MODELS` (List[str]): Список доступных моделей Gemini.

**Методы**:
- `__post_init__()`: Инициализация модели GoogleGenerativeAi с дополнительными настройками.
- `normalize_answer(text: str) -> str`: Очистка вывода от форматирования.
- `_start_chat()`: Запуск чата с начальной настройкой.
- `clear_history()`: Очищает историю чата в памяти и удаляет файл истории, если он существует.
- `_save_chat_history(chat_data_folder: Optional[str | Path])`: Сохраняет всю историю чата в JSON файл.
- `_load_chat_history(chat_data_folder: Optional[str | Path])`: Загружает историю чата из JSON файла.
- `chat(q: str, chat_data_folder: Optional[str | Path], flag: str = "save_chat") -> Optional[str]`: Обрабатывает чат-запрос с различными режимами управления историей чата.
- `ask(q: str, attempts: int = 15, save_history: bool = False, clean_response: bool = True) -> Optional[str]`: Отправляет текстовый запрос модели и возвращает ответ.
- `ask_async(q: str, attempts: int = 15, save_history: bool = False, clean_response: bool = True) -> Optional[str]`: Асинхронно отправляет текстовый запрос модели и возвращает ответ.
- `describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]`: Отправляет изображение в Gemini Pro Vision и возвращает его текстовое описание.
- `upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`: Загружает файл в Gemini.

## Методы класса

### `__post_init__`

```python
def __post_init__(self):
    """Инициализация модели GoogleGenerativeAi с дополнительными настройками."""
    ...
```

**Назначение**: Инициализирует экземпляр класса `GoogleGenerativeAi` после создания, загружая конфигурацию, устанавливая пути к файлам истории и настраивая модель Gemini.

**Как работает функция**:
- Загружает конфигурацию из файла `gemini.json`.
- Определяет пути для файлов логов и истории чата.
- Инициализирует модель Gemini с использованием предоставленного API-ключа, имени модели и системных инструкций.
- Запускает чат с помощью метода `_start_chat`.

### `normalize_answer`

```python
def normalize_answer(self, text: str) -> str:
    """Очистка вывода от 
    ```md, ```python, ```json, ```html, ит.п.
    """
    ...
```

**Назначение**:
Очищает текстовый вывод модели от различных видов форматирования, таких как Markdown, Python, JSON и HTML.

**Параметры**:
- `text` (str): Текст, который необходимо очистить.

**Возвращает**:
- `str`: Очищенный текст.

**Примеры**:
```python
ai = GoogleGenerativeAi(api_key='your_api_key')
cleaned_text = ai.normalize_answer("```python\nprint('Hello')\n```")
print(cleaned_text)  # Вывод: print('Hello')
```

### `_start_chat`

```python
def _start_chat(self):
    """Запуск чата с начальной настройкой."""
    ...
```

**Назначение**:
Запускает новый чат с моделью Gemini, используя системные инструкции, если они предоставлены.

**Возвращает**:
- `Any`: Объект чата, созданный моделью Gemini.

**Как работает функция**:
- Если предоставлены системные инструкции (`self.system_instruction`), то запускает чат с этими инструкциями в качестве начального сообщения.
- В противном случае запускает чат без начальных сообщений.

### `clear_history`

```python
def clear_history(self):
    """
    Очищает историю чата в памяти и удаляет файл истории, если он существует.
    """
    ...
```

**Назначение**:
Очищает историю чата, хранящуюся в памяти, и удаляет файл истории чата, если он существует.

**Как работает функция**:
- Очищает список `self.chat_history`, удаляя все записи истории чата.
- Проверяет, существует ли файл истории чата (`self.history_json_file`).
- Если файл существует, пытается удалить его и логирует успешное удаление.
- В случае возникновения ошибки при удалении файла, логирует ошибку.

### `_save_chat_history`

```python
async def _save_chat_history(self, chat_data_folder: Optional[str | Path]):
    """Сохраняет всю историю чата в JSON файл"""
    ...
```

**Назначение**:
Сохраняет историю чата в формате JSON в указанную папку.

**Параметры**:
- `chat_data_folder` (Optional[str | Path]): Путь к папке, в которой будет сохранен файл истории чата. Если `None`, используется путь по умолчанию.

**Как работает функция**:
- Если `chat_data_folder` указан, устанавливает `self.history_json_file` в путь к файлу `history.json` в указанной папке.
- Если история чата (`self.chat_history`) не пуста, сохраняет её в JSON файл с использованием функции `j_dumps`.

### `_load_chat_history`

```python
async def _load_chat_history(self, chat_data_folder: Optional[str | Path]):
    """Загружает историю чата из JSON файла"""
    ...
```

**Назначение**:
Загружает историю чата из JSON файла и восстанавливает состояние чата.

**Параметры**:
- `chat_data_folder` (Optional[str | Path]): Путь к папке, содержащей файл истории чата.

**Как работает функция**:
- Если указана папка `chat_data_folder`, формирует путь к файлу истории `history.json` в этой папке.
- Проверяет, существует ли файл истории. Если да, загружает историю чата из файла с помощью `j_loads`.
- После загрузки истории перезапускает чат с помощью `self._start_chat()` и добавляет все записи из загруженной истории в текущую историю чата (`self._chat.history`).
- Логирует информацию об успешной загрузке истории.
- В случае возникновения ошибки при загрузке, логирует ошибку.

### `chat`

```python
async def chat(self, q: str, chat_data_folder: Optional[str | Path], flag: str = "save_chat") -> Optional[str]:
    """
    Обрабатывает чат-запрос с различными режимами управления историей чата.

    Args:
        q (str): Вопрос пользователя.
        chat_data_folder (Optional[str | Path]): Папка для хранения истории чата.
        flag (str): Режим управления историей. Возможные значения: 
                    "save_chat", "read_and_clear", "clear", "start_new".

    Returns:
        Optional[str]: Ответ модели.
    """
    ...
```

**Назначение**:
Обрабатывает чат-запрос пользователя, управляет историей чата в зависимости от установленного флага и возвращает ответ модели.

**Параметры**:
- `q` (str): Вопрос пользователя.
- `chat_data_folder` (Optional[str | Path]): Папка для хранения истории чата.
- `flag` (str): Режим управления историей чата. Возможные значения:
    - `"save_chat"`: Загружает историю чата, добавляет новый вопрос и ответ, сохраняет историю.
    - `"read_and_clear"`: Загружает историю чата, очищает историю и начинает новый чат.
    - `"read_and_start_new"`: Загружает историю чата, сохраняет её в архив, очищает историю и начинает новый чат.
    - `"clear"`: Очищает историю чата и начинает новый чат.
    - `"start_new"`: Сохраняет текущую историю в архив, очищает историю и начинает новый чат.

**Возвращает**:
- `Optional[str]`: Ответ модели Gemini на вопрос пользователя.

**Как работает функция**:
- В зависимости от значения флага выполняет различные действия по загрузке, очистке и сохранению истории чата.
- Отправляет вопрос пользователя модели Gemini с помощью метода `self._chat.send_message_async(q)`.
- Если получен ответ от модели, добавляет вопрос и ответ в историю чата, сохраняет историю и возвращает ответ.
- В случае возникновения ошибки логирует ошибку и возвращает `None`.

### `ask`

```python
def ask(self, q: str, attempts: int = 15, save_history: bool = False, clean_response: bool = True) -> Optional[str]:
    """
    Метод отправляет текстовый запрос модели и возвращает ответ.
    """
    ...
```

**Назначение**:
Отправляет текстовый запрос модели Gemini и возвращает ответ, выполняя несколько попыток в случае неудачи.

**Параметры**:
- `q` (str): Текстовый запрос.
- `attempts` (int): Максимальное количество попыток отправки запроса. По умолчанию 15.
- `save_history` (bool): Флаг, указывающий, нужно ли сохранять диалог в историю. По умолчанию `False`.
- `clean_response` (bool): Флаг, указывающий, нужно ли очищать ответ от лишних символов. По умолчанию `True`.

**Возвращает**:
- `Optional[str]`: Ответ модели, очищенный (если `clean_response=True`) или `None` в случае неудачи после всех попыток.

**Как работает функция**:
- Циклически отправляет запрос модели `self.model.generate_content(q)` до тех пор, пока не получит ответ или не истечет количество попыток.
- В случае получения пустого ответа логирует отладочное сообщение и повторяет попытку после небольшой задержки.
- В случае сетевых ошибок (requests.exceptions.RequestException) или ошибок сервиса (GatewayTimeout, ServiceUnavailable) также повторяет попытку после задержки.
- В случае ошибки аутентификации (DefaultCredentialsError, RefreshError) прекращает попытки и возвращает `None`.
- Если `save_history=True`, сохраняет запрос и ответ в историю диалога с помощью метода `self._save_dialogue`.
- Очищает ответ от лишних символов с помощью метода `self.normalize_answer`, если `clean_response=True`.

### `ask_async`

```python
async def ask_async(self, q: str, attempts: int = 15, save_history: bool = False, clean_response: bool = True) -> Optional[str]:
    """
    Метод асинхронно отправляет текстовый запрос модели и возвращает ответ.
    """
    ...
```

**Назначение**:
Асинхронно отправляет текстовый запрос модели Gemini и возвращает ответ, выполняя несколько попыток в случае неудачи.

**Параметры**:
- `q` (str): Текстовый запрос.
- `attempts` (int): Максимальное количество попыток отправки запроса. По умолчанию 15.
- `save_history` (bool): Флаг, указывающий, нужно ли сохранять диалог в историю. По умолчанию `False`.
- `clean_response` (bool): Флаг, указывающий, нужно ли очищать ответ от лишних символов. По умолчанию `True`.

**Возвращает**:
- `Optional[str]`: Ответ модели, очищенный (если `clean_response=True`) или `None` в случае неудачи после всех попыток.

**Как работает функция**:
- Циклически отправляет запрос модели `self.model.generate_content(q)` до тех пор, пока не получит ответ или не истечет количество попыток. Вызов `self.model.generate_content` обернут в `asyncio.to_thread` для неблокирующего выполнения.
- В случае получения пустого ответа логирует отладочное сообщение и повторяет попытку после небольшой задержки с помощью `asyncio.sleep`.
- В случае сетевых ошибок (requests.exceptions.RequestException) или ошибок сервиса (GatewayTimeout, ServiceUnavailable) также повторяет попытку после задержки.
- В случае ошибки аутентификации (DefaultCredentialsError, RefreshError) прекращает попытки и возвращает `None`.
- Если `save_history=True`, сохраняет запрос и ответ в историю диалога с помощью метода `self._save_dialogue`.
- Если `clean_response=True`, ответ очищается c помощью `self.normalize_answer`

### `describe_image`

```python
def describe_image(
    self, image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = ''
) -> Optional[str]:
    """
    Отправляет изображение в Gemini Pro Vision и возвращает его текстовое описание.

    Args:
        image: Путь к файлу изображения или байты изображения

    Returns:
        str: Текстовое описание изображения.
        None: Если произошла ошибка.
    """
    ...
```

**Назначение**:
Отправляет изображение в модель Gemini Pro Vision и возвращает текстовое описание изображения.

**Параметры**:
- `image` (Path | bytes): Путь к файлу изображения или байты изображения.
- `mime_type` (Optional[str]): MIME-тип изображения. По умолчанию 'image/jpeg'.
- `prompt` (Optional[str]): Дополнительный текстовый запрос для описания изображения. По умолчанию ''.

**Возвращает**:
- `Optional[str]`: Текстовое описание изображения или `None` в случае ошибки.

**Как работает функция**:
- Подготавливает контент для запроса, преобразуя изображение в байты, если передан путь к файлу.
- Формирует запрос, включающий MIME-тип и данные изображения.
- Отправляет запрос модели Gemini Pro Vision и получает ответ.
- Обрабатывает возможные исключения, такие как ошибки аутентификации, API, перегрузку модели и другие ошибки.
- Измеряет время выполнения запроса.
- Возвращает текстовое описание изображения, полученное от модели.

### `upload_file`

```python
async def upload_file(
    self, file: str | Path | IOBase, file_name: Optional[str] = None
) -> bool:
    """
    https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai/upload_file.md
    response (file_types.File)
    """
    ...
```

**Назначение**:
Загружает файл в Google Gemini API.

**Параметры**:
- `file` (str | Path | IOBase): Путь к файлу, который нужно загрузить, или объект файла.
- `file_name` (Optional[str]): Имя файла, под которым он будет сохранен в Google Gemini API. Если не указано, будет использовано имя файла из пути.

**Возвращает**:
- `bool`: Возвращает `True` в случае успешной загрузки файла и `False` в случае ошибки.

**Как работает функция**:
- Пытается асинхронно загрузить файл с использованием `genai.upload_file_async`.
- В случае успеха логирует отладочное сообщение и возвращает `True`.
- В случае ошибки логирует сообщение об ошибке и пытается удалить файл, если он был частично загружен.
- Если удаление также вызывает ошибку, логирует сообщение об ошибке и возвращает `False`.

## Параметры класса

- `api_key` (str): Ключ API для доступа к Google Generative AI.
- `model_name` (str): Имя используемой модели Gemini. По умолчанию "gemini-2.0-flash-exp".
- `dialogue_txt_path` (Path): Путь к файлу для записи логов диалогов.
- `generation_config` (Dict): Конфигурация генерации ответов. По умолчанию `{"response_mime_type": "text/plain"}`.
- `system_instruction` (Optional[str]): Системная инструкция для модели.
- `history_dir` (Path): Путь к директории для хранения истории чата.
- `history_txt_file` (Path): Путь к текстовому файлу для хранения истории чата.
- `history_json_file` (Path): Путь к JSON файлу для хранения истории чата.
- `config` (SimpleNamespace): Конфигурация, загруженная из `gemini.json`.
- `chat_history` (List[Dict]): История чата в виде списка словарей.
- `model` (Any): Объект модели Gemini.
- `_chat` (Any): Объект чата.
- `MODELS` (List[str]): Список доступных моделей Gemini.

## Примеры

Пример использования класса `GoogleGenerativeAi`:

```python
from src.ai.gemini.gemini import GoogleGenerativeAi
from pathlib import Path

# Замените на свой ключ API
api_key = "YOUR_API_KEY"

# Создание экземпляра класса
ai = GoogleGenerativeAi(api_key=api_key)

# Пример отправки текстового запроса
response = ai.ask("What is the capital of France?")
print(f"Gemini: {response}")

# Пример описания изображения
image_path = Path("path/to/your/image.jpg")
description = ai.describe_image(image_path)
print(f"Image description: {description}")
```

Пример использования асинхронного метода `ask_async`:

```python
import asyncio
from src.ai.gemini.gemini import GoogleGenerativeAi

async def main():
    # Замените на свой ключ API
    api_key = "YOUR_API_KEY"
    ai = GoogleGenerativeAi(api_key=api_key)
    response = await ai.ask_async("What is the capital of Germany?")
    print(f"Gemini: {response}")

if __name__ == "__main__":
    asyncio.run(main())