# Модуль `code_assistant`

## Обзор

Модуль предназначен для обучения моделей машинного обучения на кодовой базе, создания документации к проекту, примеров кода и тестов. Он содержит класс `CodeAssistant`, который отвечает за чтение файлов кода, взаимодействие с моделями ИИ для обработки кода и сохранение результатов в директории `docs/gemini`. В зависимости от заданной роли, файлы сохраняются в соответствующих поддиректориях.

## Подробнее

Этот модуль автоматизирует процесс анализа и документирования кода, используя возможности моделей искусственного интеллекта, таких как Google Gemini и OpenAI. Он позволяет генерировать документацию, примеры кода и тесты, что значительно упрощает поддержку и развитие проектов.

## Классы

### `Config`

**Описание**: Класс `Config` предназначен для хранения и управления конфигурационными параметрами, используемыми ассистентом кода. Он предоставляет доступ к различным настройкам, таким как пути к файлам инструкций, спискам ролей и языков, директориям для обработки и исключения, а также параметрам моделей Gemini и OpenAI.

**Принцип работы**:
Класс `Config` инициализируется с базовыми путями и загружает конфигурационные данные из файла `code_assistant.json`. Он также предоставляет свойства класса для доступа к инструкциям для кода и системы, загружаемым из соответствующих файлов. Класс использует `SimpleNamespace` для хранения конфигурационных данных, что обеспечивает удобный доступ к атрибутам через точечную нотацию.

**Атрибуты**:
- `base_path` (Path): Базовый путь к директории `code_assistant`.
- `config` (SimpleNamespace): Конфигурационные данные, загруженные из `code_assistant.json`.
- `roles_list` (list): Список ролей, определенных в конфигурации.
- `languages_list` (list): Список языков, определенных в конфигурации.
- `role` (str): Текущая роль ассистента кода (по умолчанию `doc_writer_md`).
- `lang` (str): Текущий язык ассистента кода (по умолчанию `ru`).
- `process_dirs` (list[Path]): Список директорий для обработки.
- `exclude_dirs` (list[Path]): Список директорий, исключенных из обработки.
- `exclude_files_patterns` (list[Path]): Список шаблонов файлов, исключенных из обработки.
- `include_files_patterns` (list[Path]): Список шаблонов файлов, включенных в обработку.
- `exclude_files` (list[Path]): Список файлов, исключенных из обработки.
- `exclude_dirs` (list[Path]): Список директорий, исключенных из обработки.
- `response_mime_type` (str): MIME-тип ответа (по умолчанию из конфигурации).
- `output_directory_patterns` (list): Список шаблонов директорий для вывода.
- `code_instruction` (str): Инструкция для кода, загружаемая из файла.
- `system_instruction` (str): Инструкция для модели, загружаемая из файла.
- `gemini` (SimpleNamespace): Конфигурационные параметры для модели Gemini.

**Методы**:
- `code_instruction`: Свойство класса, которое читает инструкцию для кода из файла и возвращает ее.
- `system_instruction`: Свойство класса, которое читает инструкцию для модели из файла и возвращает ее.

### `CodeAssistant`

**Описание**: Класс `CodeAssistant` предназначен для взаимодействия с моделями искусственного интеллекта (например, Google Gemini и OpenAI) и выполнения задач обработки кода, таких как создание документации, примеров кода и тестов.

**Принцип работы**:
Класс `CodeAssistant` инициализируется с заданной ролью, языком и списком моделей для использования. Он предоставляет методы для отправки файлов в модель, обработки файлов в директориях и сохранения результатов. Класс использует конфигурационные параметры из класса `Config` для управления процессом обработки файлов и взаимодействия с моделями ИИ.

**Атрибуты**:
- `role` (str): Роль ассистента (например, `doc_writer_md`, `code_checker`).
- `lang` (str): Язык, на котором ассистент должен выполнять задачи.
- `gemini` (GoogleGenerativeAI): Экземпляр класса `GoogleGenerativeAI` для взаимодействия с моделью Gemini.
- `openai` (OpenAIModel): Экземпляр класса `OpenAIModel` для взаимодействия с моделью OpenAI.

**Методы**:
- `__init__(role: Optional[str] = 'doc_writer_md', lang: Optional[str] = 'en', models_list: Optional[list[str, str] | str] = ['gemini'], system_instruction: Optional[str | Path] = None, **kwards) -> None`: Инициализация ассистента с заданными параметрами.
- `_initialize_models(models_list: list, response_mime_type: Optional[str] = '', **kwards) -> bool`: Инициализация моделей на основе заданных параметров.
- `send_file(file_path: Path) -> Optional[str | None]`: Отправка файла в модель.
- `process_files(process_dirs: Optional[str | Path | list[str | Path]] = None, start_from_file: Optional[int] = 1) -> bool`: Компиляция, отправка запроса и сохранение результата.
- `_create_request(file_path: str, content: str) -> str`: Создание запроса с учетом роли и языка.
- `_yield_files_content(process_directory: str | Path) -> Iterator[tuple[Path, str]]`: Генерация путей файлов и их содержимого по указанным шаблонам.
- `_save_response(file_path: Path, response: str, model_name: str) -> bool`: Сохранение ответа модели в файл с добавлением суффикса.
- `_remove_outer_quotes(response: str) -> str`: Удаление внешних кавычек в начале и в конце строки, если они присутствуют.
- `run(start_from_file: int = 1) -> None`: Запуск процесса обработки файлов.
- `_signal_handler(self, signal, frame) -> None`: Обработка прерывания выполнения.

## Функции

### `Config.code_instruction`

**Назначение**: Возвращает инструкцию для кода, загруженную из файла.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `str`: Инструкция для кода.

**Как работает функция**:
1. Формируется путь к файлу с инструкцией на основе текущей роли и языка из `Config`.
2. Файл читается и его содержимое возвращается как строка.

```ascii
    Get Config.base_path, Config.role, Config.lang -->
    |
    Create instruction file path -->
    |
    Read instruction file -->
    |
    Return content
```

**Примеры**:
```python
instruction = Config.code_instruction
print(instruction)
```

### `Config.system_instruction`

**Назначение**: Возвращает инструкцию для модели, загруженную из файла.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `str`: Инструкция для модели.

**Как работает функция**:
1. Формируется путь к файлу с системной инструкцией на основе текущего языка из `Config`.
2. Файл читается и его содержимое возвращается как строка.

```ascii
    Get Config.base_path, Config.lang -->
    |
    Create instruction file path -->
    |
    Read instruction file -->
    |
    Return content
```

**Примеры**:
```python
instruction = Config.system_instruction
print(instruction)
```

### `CodeAssistant.__init__`

```python
def __init__(
    self,
    role: Optional[str] = 'doc_writer_md',
    lang: Optional[str] = 'en',
    models_list: Optional[list[str, str] | str] = ['gemini'],
    system_instruction: Optional[str | Path] = None,
    **kwards,
) -> None:
    """
    Инициализация ассистента с заданными параметрами.

    Args:
        role (str): Роль для выполнения задачи.
        lang (str): Язык выполнения.
        models_list (list[str]): Список моделей для инициализации.
        system_instruction (str|Path): Общая инструкция для модели. 
        **kwards: Дополнительные аргументы для инициализации моделей.
    """
```

**Назначение**: Инициализирует экземпляр класса `CodeAssistant` с заданными параметрами, такими как роль, язык и список моделей для использования.

**Параметры**:
- `role` (Optional[str]): Роль ассистента (например, `doc_writer_md`, `code_checker`). По умолчанию `'doc_writer_md'`.
- `lang` (Optional[str]): Язык, на котором ассистент должен выполнять задачи. По умолчанию `'en'`.
- `models_list` (Optional[list[str, str] | str]): Список моделей для инициализации. По умолчанию `['gemini']`.
- `system_instruction` (Optional[str | Path]): Общая инструкция для модели. По умолчанию `None`.
- `**kwards`: Дополнительные аргументы для инициализации моделей.

**Как работает функция**:
1. Устанавливает значения атрибутов `role` и `lang` из переданных аргументов или использует значения по умолчанию из `Config`.
2. Инициализирует модели, указанные в `models_list`, с помощью метода `_initialize_models`.

```ascii
    Get role, lang, models_list, system_instruction, kwards -->
    |
    Set Config.role, Config.lang, Config.system_instruction -->
    |
    Call _initialize_models()
```

**Примеры**:
```python
assistant = CodeAssistant(role='doc_writer_md', lang='ru', models_list=['gemini'])
```

### `CodeAssistant._initialize_models`

```python
def _initialize_models(self, models_list: list, response_mime_type: Optional[str] = '', **kwards) -> bool:
    """
    Инициализация моделей на основе заданных параметров.

    Args:
        models_list (list[str]): Список моделей для инициализации.
        **kwards: Дополнительные аргументы для инициализации моделей.

    Returns:
        bool: Успешность инициализации моделей.

    Raises:
        Exception: Если произошла ошибка при инициализации моделей.
    """
```

**Назначение**: Инициализирует модели ИИ на основе заданных параметров, таких как список моделей и дополнительные аргументы.

**Параметры**:
- `models_list` (list[str]): Список моделей для инициализации (например, `['gemini']`).
- `response_mime_type` (Optional[str]): MIME-тип ответа. По умолчанию `''`.
- `**kwards`: Дополнительные аргументы для инициализации моделей.

**Возвращает**:
- `bool`: `True`, если инициализация моделей прошла успешно, `False` в противном случае.

**Вызывает исключения**:
- `Exception`: Если произошла ошибка при инициализации моделей.

**Как работает функция**:
1. Проверяет, присутствует ли `'gemini'` в списке моделей.
2. Если да, пытается инициализировать модель `GoogleGenerativeAI` с использованием параметров из `kwards` и `Config`.
3. В случае успеха возвращает `True`, в противном случае логирует ошибку и возвращает `False`.

```ascii
    Get models_list, kwards -->
    |
    Check if 'gemini' in models_list -->
    |
    Try to initialize GoogleGenerativeAI -->
    |
    Return True if successful, False otherwise
```

**Примеры**:
```python
assistant = CodeAssistant()
success = assistant._initialize_models(['gemini'])
print(success)
```

### `CodeAssistant.send_file`

```python
def send_file(self, file_path: Path) -> Optional[str | None]:
    """
    Отправка файла в модель.

    Args:
        file_path (Path): Абсолютный путь к файлу, который нужно отправить.
        file_name (Optional[str]): Имя файла для отправки. Если не указано и \'src\' отсутствует, используется имя файла без изменений.

    Returns:
        Optional[str | None]: URL файла, если успешно отправлен, иначе None.
    """
```

**Назначение**: Отправляет файл в модель Gemini для обработки.

**Параметры**:
- `file_path` (Path): Абсолютный путь к файлу, который нужно отправить.

**Возвращает**:
- `Optional[str | None]`: URL файла, если файл успешно отправлен в модель и получен ответ, иначе `None`.

**Как работает функция**:
1. Пытается отправить файл в модель Gemini с помощью метода `upload_file`.
2. Если получен ответ, проверяет наличие атрибута `url` в ответе и возвращает его значение.
3. В случае ошибки логирует ошибку и возвращает `None`.

```ascii
    Get file_path -->
    |
    Try to upload file to Gemini -->
    |
    Check if response has url -->
    |
    Return url if successful, None otherwise
```

**Примеры**:
```python
file_path = Path('example.txt')
url = assistant.send_file(file_path)
if url:
    print(f'File URL: {url}')
```

### `CodeAssistant.process_files`

```python
async def process_files(
    self, process_dirs: Optional[str | Path | list[str | Path]] = None, start_from_file: Optional[int] = 1
) -> bool:
    """компиляция, отправка запроса и сохранение результата."""
```

**Назначение**: Компилирует, отправляет запросы и сохраняет результаты обработки файлов в указанных директориях.

**Параметры**:
- `process_dirs` (Optional[str | Path | list[str | Path]]): Список директорий для обработки. Если не указан, используется `Config.process_dirs`.
- `start_from_file` (Optional[int]): Номер файла, с которого начинается обработка. По умолчанию `1`.

**Возвращает**:
- `bool`: `True`, если обработка файлов прошла успешно, `False` в противном случае.

**Как работает функция**:
1. Устанавливает `Config.process_dirs` из переданного аргумента или использует значение по умолчанию.
2. Итерируется по каждой директории в `Config.process_dirs`.
3. Проверяет существование и тип директории.
4. Итерируется по каждому файлу в директории с использованием `_yield_files_content`.
5. Пропускает файлы до `start_from_file`.
6. Создает запрос с использованием `_create_request`.
7. Отправляет запрос в модель Gemini с использованием `gemini.ask_async`.
8. Сохраняет ответ с использованием `_save_response`.

```ascii
    Get process_dirs, start_from_file -->
    |
    Set Config.process_dirs -->
    |
    Iterate through process_directories -->
    |
    Check if directory exists and is a directory -->
    |
    Iterate through files in directory -->
    |
    Skip files before start_from_file -->
    |
    Create request using _create_request -->
    |
    Send request to Gemini using gemini.ask_async -->
    |
    Save response using _save_response
```

**Примеры**:
```python
assistant = CodeAssistant()
asyncio.run(assistant.process_files(process_dirs=['src']))
```

### `CodeAssistant._create_request`

```python
def _create_request(self, file_path: str, content: str) -> str:
    """Создание запроса с учетом роли и языка."""
```

**Назначение**: Создает запрос для модели с учетом роли, языка и содержимого файла.

**Параметры**:
- `file_path` (str): Путь к файлу.
- `content` (str): Содержимое файла.

**Возвращает**:
- `str`: Строковое представление запроса.

**Как работает функция**:
1. Формирует словарь `content_request` с информацией о роли, языке, пути к файлу и содержимом файла.
2. Преобразует словарь в строку и возвращает ее.

```ascii
    Get file_path, content -->
    |
    Create content_request dictionary -->
    |
    Convert dictionary to string -->
    |
    Return string
```

**Примеры**:
```python
file_path = 'example.py'
content = 'def hello(): print("Hello")'
request = assistant._create_request(file_path, content)
print(request)
```

### `CodeAssistant._yield_files_content`

```python
def _yield_files_content(
    self,
    process_directory: str | Path,
) -> Iterator[tuple[Path, str]]:
    """
    Генерирует пути файлов и их содержимое по указанным шаблонам.

    Args:
        process_directory (Path | str): Абсолютный путь к стартовой директории

    Returns:
        bool: Iterator
    """
```

**Назначение**: Генерирует пути файлов и их содержимое в указанной директории, учитывая шаблоны включения и исключения.

**Параметры**:
- `process_directory` (str | Path): Путь к директории для обработки.

**Возвращает**:
- `Iterator[tuple[Path, str]]`: Итератор, возвращающий кортежи, содержащие путь к файлу и его содержимое.

**Как работает функция**:
1. Компилирует шаблоны исключаемых файлов из `Config.exclude_files_patterns`.
2. Итерируется по всем файлам в директории, используя `rglob('*')`.
3. Проверяет соответствие имени файла шаблонам включения из `Config.include_files_patterns`. Если ни одному шаблону не соответствует, переходит к следующему файлу.
4. Проверяет, не находится ли файл в исключенной директории из `Config.exclude_dirs`. Если находится, переходит к следующему файлу.
5. Проверяет, не соответствует ли имя файла шаблону исключения из `exclude_files_patterns`. Если соответствует, переходит к следующему файлу.
6. Проверяет, не находится ли имя файла в списке исключенных файлов из `Config.exclude_files`. Если находится, переходит к следующему файлу.
7. Читает содержимое файла и возвращает путь к файлу и его содержимое в виде кортежа.
8. В случае ошибки чтения файла логирует ошибку и возвращает `(None, None)`.

```ascii
    Get process_directory -->
    |
    Compile exclude file patterns -->
    |
    Iterate through files in directory -->
    |
    Check include patterns -->
    |
    Check exclude directories -->
    |
    Check exclude file patterns -->
    |
    Check exclude files -->
    |
    Read file content -->
    |
    Yield file path and content
```

**Примеры**:
```python
process_directory = 'src'
for file_path, content in assistant._yield_files_content(process_directory):
    if file_path and content:
        print(f'File: {file_path}')
```

### `CodeAssistant._save_response`

```python
async def _save_response(self, file_path: Path, response: str, model_name: str) -> bool:
    """
    Сохранение ответа модели в файл с добавлением суффикса.

    Метод сохраняет ответ модели в файл, добавляя к текущему расширению файла
    дополнительный суффикс, определяемый ролью.

    Args:
        file_path (Path): Исходный путь к файлу, в который будет записан ответ.
        response (str): Ответ модели, который необходимо сохранить.
        model_name (str): Имя модели, использованной для генерации ответа.

    Raises:
        OSError: Если не удаётся создать директорию или записать в файл.
    """
```

**Назначение**: Сохраняет ответ модели в файл с добавлением суффикса, зависящего от роли.

**Параметры**:
- `file_path` (Path): Исходный путь к файлу, в который будет записан ответ.
- `response` (str): Ответ модели, который необходимо сохранить.
- `model_name` (str): Имя модели, использованной для генерации ответа.

**Возвращает**:
- `bool`: `True`, если файл успешно сохранен, `False` в противном случае.

**Вызывает исключения**:
- `OSError`: Если не удается создать директорию или записать в файл.

**Как работает функция**:
1. Определяет целевую директорию для сохранения файла на основе `Config.output_directory_patterns` и текущей роли.
2. Формирует путь к файлу, заменяя часть пути `src` на целевую директорию и добавляя суффикс, зависящий от роли.
3. Создает директорию, если она не существует.
4. Записывает ответ модели в файл.
5. В случае успеха возвращает `True`, в противном случае логирует ошибку и возвращает `False`.

```ascii
    Get file_path, response, model_name -->
    |
    Determine target directory based on Config.output_directory_patterns and role -->
    |
    Form file path, replacing 'src' with target directory and adding suffix -->
    |
    Create directory if it doesn't exist -->
    |
    Write response to file -->
    |
    Return True if successful, False otherwise
```

**Примеры**:
```python
file_path = Path('src/example.py')
response = 'This is a sample response.'
model_name = 'gemini'
success = asyncio.run(assistant._save_response(file_path, response, model_name))
print(success)
```

### `CodeAssistant._remove_outer_quotes`

```python
def _remove_outer_quotes(self, response: str) -> str:
    """
    Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.

    Args:
        response (str): Ответ модели, который необходимо обработать.

    Returns:
        str: Очищенный контент как строка.

    Example:
        >>> _remove_outer_quotes('```md some content ```')
        'some content'
        >>> _remove_outer_quotes('some content')
        'some content'
        >>> _remove_outer_quotes('```python def hello(): print("Hello") ```')
        '```python def hello(): print("Hello") ```'
    """
```

**Назначение**: Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.

**Параметры**:
- `response` (str): Ответ модели, который необходимо обработать.

**Возвращает**:
- `str`: Очищенный контент как строка.

**Как работает функция**:
1. Удаляет пробелы в начале и в конце строки.
2. Если строка начинается с `'```python'` или `'```mermaid'`, возвращает ее без изменений.
3. Итерируется по префиксам для удаления из `config.remove_prefixes`.
4. Если строка начинается с одного из префиксов, удаляет префикс и суффикс `'```'`, если он есть.
5. Возвращает очищенную строку или исходную строку, если условия не выполнены.

```ascii
    Get response -->
    |
    Strip whitespace -->
    |
    Check if starts with '```python' or '```mermaid' -->
    |
    Iterate through remove prefixes -->
    |
    If starts with prefix, remove prefix and '```' suffix if present -->
    |
    Return cleaned string or original string
```

**Примеры**:
```python
response = '```md some content ```'
cleaned_response = assistant._remove_outer_quotes(response)
print(cleaned_response)  # Output: some content

response = 'some content'
cleaned_response = assistant._remove_outer_quotes(response)
print(cleaned_response)  # Output: some content

response = '```python def hello(): print("Hello") ```'
cleaned_response = assistant._remove_outer_quotes(response)
print(cleaned_response)  # Output: ```python def hello(): print("Hello") ```
```

### `CodeAssistant.run`

```python
def run(self, start_from_file: int = 1) -> None:
    """Запуск процесса обработки файлов."""
```

**Назначение**: Запускает процесс обработки файлов.

**Параметры**:
- `start_from_file` (int): Номер файла, с которого начинается обработка. По умолчанию `1`.

**Как работает функция**:
1. Устанавливает обработчик сигнала `SIGINT` для обработки прерывания выполнения (Ctrl+C).
2. Запускает асинхронную обработку файлов с помощью `asyncio.run(self.process_files(start_from_file))`.

```ascii
    Get start_from_file -->
    |
    Set signal handler for SIGINT -->
    |
    Run process_files asynchronously
```

**Примеры**:
```python
assistant = CodeAssistant()
assistant.run()
```

### `CodeAssistant._signal_handler`

```python
def _signal_handler(self, signal, frame) -> None:
    """Обработка прерывания выполнения."""
```

**Назначение**: Обрабатывает прерывание выполнения программы (например, при нажатии Ctrl+C).

**Параметры**:
- `signal`: Сигнал, полученный программой.
- `frame`: Текущий кадр стека вызовов.

**Как работает функция**:
1. Логирует сообщение о прерывании процесса.
2. Завершает выполнение программы с кодом выхода `0`.

```ascii
    Get signal, frame -->
    |
    Log interruption message -->
    |
    Exit program
```

**Примеры**:
```python
assistant._signal_handler(signal.SIGINT, None)
```

### `parse_args`

```python
def parse_args() -> dict:
    """Разбор аргументов командной строки."""
```

**Назначение**: Разбирает аргументы командной строки, переданные при запуске программы.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `dict`: Словарь, содержащий значения аргументов командной строки.

**Как работает функция**:
1. Создает экземпляр класса `argparse.ArgumentParser` с описанием назначения программы.
2. Добавляет аргументы `--role`, `--lang`, `--model`, `--start-dirs` и `--start-file-number` с описанием их назначения и значениями по умолчанию.
3. Разбирает аргументы командной строки с помощью метода `parse_args()`.
4. Возвращает словарь, содержащий значения аргументов.

```ascii
    Create ArgumentParser -->
    |
    Add arguments -->
    |
    Parse arguments -->
    |
    Return arguments as dictionary
```

**Примеры**:
```python
args = parse_args()
print(args)
```

### `main`

```python
def main() -> None:
    """
    Функция запускает бесконечный цикл, в котором выполняется обработка файлов с учетом ролей и языков, указанных в конфигурации.
    Конфигурация обновляется в каждом цикле, что позволяет динамически изменять настройки в файле `code_assistant.json` во время работы программы.
    Для каждой комбинации языка и роли создается экземпляр класса :class:`CodeAssistant`, который обрабатывает файлы, используя заданную модель ИИ.
    """
```

**Назначение**: Запускает бесконечный цикл обработки файлов с учетом ролей и языков, указанных в конфигурации.

**Параметры**:
- Нет параметров.

**Как работает функция**:
1. Запускает бесконечный цикл `while True`.
2. Итерируется по каждому языку в `Config.languages_list`.
3. Итерируется по каждой роли в `Config.roles_list`.
4. Создает экземпляр класса `CodeAssistant` с текущей ролью и языком.
5. Запускает обработку файлов с помощью `asyncio.run(assistant_direct.process_files(process_dirs = Config.process_dirs))`.

```ascii
    While True:
    |
    Iterate through languages -->
    |
    Iterate through roles -->
    |
    Create CodeAssistant instance -->
    |
    Run process_files
```

**Примеры**:
```python
if __name__ == '__main__':
    main()
```