# Модуль обучения модели машинного обучения кодовой базе, составления документации к проекту, примеров кода и тестов

## Overview

Модуль содержит класс `CodeAssistant`, который используется для работы с различными моделями искусственного интеллекта (например, Google Gemini и OpenAI) и выполнения задач обработки кода. Модель обучена на кодовой базе проекта `hypotez` и умеет генерировать:

- Документацию к коду в различных форматах (Markdown, ReStructuredText, HTML);
- Тесты для существующего кода;
- Примеры кода.

## Details

`CodeAssistant` читает файлы кода, отправляет их в модель, обрабатывает результат и сохраняет его в директории `docs/gemini`. 

### Пример использования
```python
assistant = CodeAssistant(role='code_checker', lang='ru', model=['gemini'])
assistant.process_files()
```

## Classes

### `Config`

**Description**: Класс конфигурации для `CodeAssistant`.

**Attributes**:

- `ENDPOINT` (Path): Путь к директории с конфигурационными файлами.
- `config` (SimpleNamespace): Объект, содержащий конфигурационные данные, загруженные из `code_assistant.json`.
- `roles_list` (list): Список доступных ролей для `CodeAssistant`.
- `languages_list` (list): Список доступных языков для `CodeAssistant`.
- `role` (str): Текущая роль, используемая `CodeAssistant`.
- `lang` (str): Текущий язык, используемый `CodeAssistant`.
- `process_dirs` (list[Path]): Список директорий для обработки.
- `exclude_dirs` (list[Path]): Список директорий, которые не должны обрабатываться.
- `exclude_files_patterns` (list[Path]): Список паттернов для исключения файлов из обработки.
- `include_files_patterns` (list[Path]): Список паттернов для включения файлов в обработку.
- `exclude_files` (list[Path]): Список конкретных файлов, которые не должны обрабатываться.
- `exclude_dirs` (list[Path]): Список директорий, которые не должны обрабатываться.
- `response_mime_type` (str): Тип MIME для ответа модели.
- `output_directory_patterns` (list): Список паттернов для сохранения результатов обработки.
- `remove_prefixes` (str): Список префиксов, которые нужно удалить из ответа модели.

**Methods**:

- `code_instruction()`: Возвращает инструкцию для кода из файла `instruction_<role>_<lang>.md`.
- `system_instruction()`: Возвращает инструкцию для модели из файла `CODE_RULES.<lang>.MD`.

### `CodeAssistant`

**Description**: Класс для работы с ассистентом программиста.

**Attributes**:

- `role` (str): Роль для выполнения задачи.
- `lang` (str): Язык выполнения.
- `gemini` (GoogleGenerativeAi): Объект модели Google Gemini.
- `openai` (OpenAIModel): Объект модели OpenAI (не используется).

**Methods**:

- `__init__(self, role: Optional[str] = 'doc_writer_md', lang: Optional[str] = 'en', model_name:Optional[str] = '', system_instruction: Optional[str | Path] = None, **kwargs) -> None`: Инициализирует ассистента с заданными параметрами.
    - **Parameters**:
        - `role` (str): Роль для выполнения задачи. По умолчанию - `'doc_writer_md'`.
        - `lang` (str): Язык выполнения. По умолчанию - `'en'`.
        - `model_name` (str): Имя модели для инициализации. По умолчанию - `''`.
        - `system_instruction` (str | Path): Общая инструкция для модели. По умолчанию - `None`.
        - `**kwargs`: Дополнительные аргументы для инициализации моделей.
- `send_file(self, file_path: Path) -> Optional[str | None]`: Отправляет файл в модель.
    - **Parameters**:
        - `file_path` (Path): Абсолютный путь к файлу, который нужно отправить.
    - **Returns**:
        - `Optional[str | None]`: URL файла, если успешно отправлен, иначе `None`.
- `process_files(self, process_dirs: Optional[str | Path | list[str | Path]] = None, save_response: bool = True) -> bool`: Обрабатывает файлы, отправляя их в модель и сохраняя результат.
    - **Parameters**:
        - `process_dirs` (Optional[str | Path | list[str | Path]]): Список директорий для обработки. По умолчанию - список из конфигурационного файла.
        - `save_response` (bool): Флаг, определяющий, нужно ли сохранять результат обработки. По умолчанию - `True`.
    - **Returns**:
        - `bool`: `True`, если обработка завершена успешно, иначе `False`.
- `_create_request(self, file_path: str, content: str) -> str`: Создает запрос к модели с учетом роли и языка.
    - **Parameters**:
        - `file_path` (str): Абсолютный путь к файлу.
        - `content` (str): Содержимое файла.
    - **Returns**:
        - `str`: Форматированный JSON-запрос к модели.
- `_yield_files_content(self, process_directory: str | Path) -> Iterator[tuple[Path, str]]`: Генерирует пути файлов и их содержимое по указанным шаблонам.
    - **Parameters**:
        - `process_directory` (Path | str): Абсолютный путь к стартовой директории.
    - **Returns**:
        - `bool`: Итератор, который возвращает кортеж из пути к файлу и его содержимого.
- `_save_response(self, file_path: Path, response: str, model_name: str) -> bool`: Сохраняет ответ модели в файл с добавлением суффикса.
    - **Parameters**:
        - `file_path` (Path): Исходный путь к файлу, в который будет записан ответ.
        - `response` (str): Ответ модели, который необходимо сохранить.
        - `model_name` (str): Имя модели, использованной для генерации ответа.
    - **Returns**:
        - `bool`: `True`, если ответ модели был сохранен успешно, иначе `False`.
- `_remove_outer_quotes(self, response: str) -> str`: Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.
    - **Parameters**:
        - `response` (str): Ответ модели, который необходимо обработать.
    - **Returns**:
        - `str`: Очищенный контент как строка.
- `run(self, start_from_file: int = 1) -> None`: Запускает процесс обработки файлов.
    - **Parameters**:
        - `start_from_file` (int): Номер файла, с которого нужно начать обработку. По умолчанию - `1`.
- `_signal_handler(self, signal, frame) -> None`: Обработка прерывания выполнения.

## Functions

### `parse_args() -> dict`:

**Purpose**: Разбирает аргументы командной строки.

**Parameters**:

- None

**Returns**:

- `dict`: Словарь с разбором аргументов командной строки.

**Examples**:

- `parse_args()`: Возвращает словарь с разбором аргументов командной строки.

### `main() -> None`:

**Purpose**: Функция запускает бесконечный цикл, в котором выполняется обработка файлов с учетом ролей и языков, указанных в конфигурации.

**Parameters**:

- None

**Returns**:

- None

**How the Function Works**:

- Цикл `while True` выполняется бесконечно.
- В каждом цикле перебираются все языки (`Config.languages_list`) и роли (`Config.roles_list`) из конфигурационного файла.
- Для каждой комбинации языка и роли создается экземпляр класса `CodeAssistant`, который обрабатывает файлы, используя заданную модель ИИ.
- Процесс обработки файлов запускается с помощью `asyncio.run(assistant_direct.process_files(process_dirs = Config.process_dirs))`.

**Examples**:

- `main()`: Запускает бесконечный цикл, в котором выполняется обработка файлов с учетом ролей и языков, указанных в конфигурации.

## Parameter Details

- `role` (str): Роль для выполнения задачи. Возможные значения: `code_checker`, `doc_writer_md`, `doc_writer_rst`, `doc_writer_html`, `code_explainer_md`, `code_explainer_html`, `pytest`.
- `lang` (str): Язык выполнения. Возможные значения: `ru`, `en`.
- `model` (list[str]): Список моделей для инициализации. Возможные значения: `gemini`, `openai`.
- `start_dirs` (list[str]): Список директорий для обработки.
- `start_file_number` (int): Номер файла, с которого нужно начать обработку.

## Examples

### Пример использования класса `CodeAssistant`:

```python
# Создание экземпляра класса CodeAssistant с заданными параметрами
assistant = CodeAssistant(role='doc_writer_md', lang='ru', model=['gemini'])

# Обработка файлов
assistant.process_files()
```

### Пример использования функции `parse_args()`:

```python
# Разбор аргументов командной строки
args = parse_args()

# Вывод полученных аргументов
print(args)
```

### Пример использования функции `main()`:

```python
# Запуск функции main()
main()
```