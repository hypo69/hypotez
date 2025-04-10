# Модуль для работы с ассистентом программиста

## Обзор

Модуль содержит класс `CodeAssistant`, который используется для взаимодействия с различными AI-моделями
(например, Google Gemini и OpenAI) и выполнения задач обработки кода.

Модуль предназначен для обучения модели машинного обучения на кодовой базе, составления документации к проекту, примеров кода и тестов.
Класс `CodeAssistant` читает файлы кода, передает код в модели, модель обрабатывает код и возвращает его в класс, а класс сохраняет результат
в директории `docs/gemini`. В зависимости от роли файлы сохраняются в различных форматах.

## Подробней

Модуль `code_assistant.py` является ключевым компонентом в проекте `hypotez`, предназначенным для автоматизации задач, связанных с кодом, таких как создание документации, проверка качества кода и генерация тестов. Он использует AI-модели, такие как Google Gemini и OpenAI, для анализа и обработки кода.

Этот модуль предоставляет гибкий и расширяемый способ интеграции AI-моделей в процесс разработки, позволяя автоматизировать рутинные задачи и повысить качество конечного продукта.

## Классы

### `Config`

**Описание**: Класс `Config` предназначен для хранения и управления конфигурационными параметрами, используемыми в модуле `code_assistant`. Он загружает конфигурацию из файла `code_assistant.json` и предоставляет доступ к различным настройкам, таким как список ролей, языков, директорий для обработки, исключений и инструкций для моделей.

**Принцип работы**:
1.  **Инициализация**: При создании экземпляра класса `Config` происходит загрузка конфигурации из файла `code_assistant.json` с использованием функции `j_loads_ns`.
2.  **Доступ к параметрам**: Класс предоставляет доступ к различным параметрам конфигурации через атрибуты класса, такие как `roles_list`, `languages_list`, `process_dirs`, `exclude_dirs` и другие.
3.  **Динамическое обновление инструкций**: Класс предоставляет методы `code_instruction` и `system_instruction`, которые при каждом вызове читают файлы с инструкциями, что позволяет обновлять инструкции "на лету".
4.  **Управление параметрами моделей**: Класс управляет параметрами для моделей Gemini и OpenAI, загружая их из переменных окружения или из файла конфигурации.

**Аттрибуты**:

*   `base_path` (Path): Базовый путь к директории `code_assistant`.
*   `config` (SimpleNamespace): Объект, содержащий конфигурацию из файла `code_assistant.json`.
*   `roles_list` (list): Список ролей.
*   `languages_list` (list): Список языков.
*   `role` (str): Текущая роль. По умолчанию `'doc_writer_md'`.
*   `lang` (str): Текущий язык. По умолчанию `'ru'`.
*   `process_dirs` (list[Path]): Список директорий для обработки.
*   `exclude_dirs` (list[Path]): Список исключенных директорий.
*   `exclude_files_patterns` (list[Path]): Список шаблонов исключенных файлов.
*   `include_files_patterns` (list[Path]): Список шаблонов включенных файлов.
*   `exclude_files` (list[Path]): Список исключенных файлов.
*   `exclude_dirs` (list[Path]): Список исключенных директорий.
*   `response_mime_type` (str): MIME-тип ответа.
*   `output_directory_patterns` (list): Список шаблонов директорий вывода.
*   `gemini` (SimpleNamespace): Объект, содержащий параметры для модели Gemini.

**Методы**:

*   `code_instruction`: Возвращает инструкцию для кода, прочитанную из файла.
*   `system_instruction`: Возвращает инструкцию для модели, прочитанную из файла.

#### `code_instruction`

```python
@classmethod
@property
def code_instruction(self):
    """code_instruction - Инструкция для кода.
    При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету"
    """
    return Path( Config.base_path / 'instructions'/ f'instruction_{Config.role}_{Config.lang}.md'
        ).read_text(encoding='UTF-8')
```

**Назначение**: Возвращает инструкцию для кода, прочитанную из файла.

**Как работает функция**:

1.  Определяется путь к файлу с инструкцией на основе текущей роли и языка.
2.  Читает содержимое файла и возвращает его.

#### `system_instruction`

```python
@classmethod
@property
def system_instruction(self):
    """Инструкция для модели.
    При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету"
    """        
    return Path(Config.base_path / 'instructions' / f'CODE_RULES.{Config.lang}.MD'
                        ).read_text(encoding='UTF-8')
```

**Назначение**: Возвращает инструкцию для модели, прочитанную из файла.

**Как работает функция**:

1.  Определяется путь к файлу с инструкцией для модели на основе текущего языка.
2.  Читает содержимое файла и возвращает его.

### `CodeAssistant`

**Описание**: Класс `CodeAssistant` предназначен для взаимодействия с AI-моделями (Google Gemini и OpenAI) для выполнения задач обработки кода, таких как создание документации, проверка качества кода и генерация тестов.

**Принцип работы**:

1.  **Инициализация**: При создании экземпляра класса `CodeAssistant` происходит инициализация параметров, таких как роль, язык и список моделей для использования.
2.  **Инициализация моделей**: На основе списка моделей происходит инициализация выбранных моделей (в данном случае Google Gemini).
3.  **Обработка файлов**: Класс предоставляет методы для обработки файлов, включая чтение содержимого файлов, отправку запросов в модель, получение ответов и сохранение результатов.
4.  **Создание запросов**: Класс создает запросы для модели с учетом роли, языка и содержимого файла.
5.  **Сохранение ответов**: Класс сохраняет ответы модели в файлы с добавлением суффикса, определяемого ролью.

**Аттрибуты**:

*   `role` (str): Роль для выполнения задачи.
*   `lang` (str): Язык выполнения.
*   `gemini` (GoogleGenerativeAI): Экземпляр класса `GoogleGenerativeAI` для взаимодействия с моделью Gemini.
*   `openai` (OpenAIModel): Экземпляр класса `OpenAIModel` для взаимодействия с моделью OpenAI.

**Методы**:

*   `__init__`: Инициализация ассистента с заданными параметрами.
*   `_initialize_models`: Инициализация моделей на основе заданных параметров.
*   `send_file`: Отправка файла в модель.
*   `process_files`: Компиляция, отправка запроса и сохранение результата.
*   `_create_request`: Создание запроса с учетом роли и языка.
*   `_yield_files_content`: Генерирует пути файлов и их содержимое по указанным шаблонам.
*   `_save_response`: Сохранение ответа модели в файл с добавлением суффикса.
*   `_remove_outer_quotes`: Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.
*   `run`: Запуск процесса обработки файлов.
*   `_signal_handler`: Обработка прерывания выполнения.

#### `__init__`

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
    Config.role = role if role else Config.role
    Config.lang = lang if lang else Config.lang
    Config.system_instruction = system_instruction if system_instruction else Config.system_instruction
    
    self._initialize_models(list(models_list), **kwards)
```

**Назначение**: Инициализация экземпляра класса `CodeAssistant` с заданными параметрами.

**Параметры**:

*   `role` (Optional[str]): Роль для выполнения задачи. По умолчанию `'doc_writer_md'`.
*   `lang` (Optional[str]): Язык выполнения. По умолчанию `'en'`.
*   `models_list` (Optional[list[str, str] | str]): Список моделей для инициализации. По умолчанию `['gemini']`.
*   `system_instruction` (Optional[str | Path]): Общая инструкция для модели.
*   `**kwards`: Дополнительные аргументы для инициализации моделей.

**Как работает функция**:

1.  Устанавливает значения параметров конфигурации `Config.role`, `Config.lang` и `Config.system_instruction` на основе переданных аргументов или значений по умолчанию.
2.  Вызывает метод `_initialize_models` для инициализации моделей на основе заданных параметров.

#### `_initialize_models`

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

    if 'gemini' in models_list:
        # Определение значений по умолчанию

        try:
            # Фильтрация kwards для удаления известных аргументов
            filtered_kwargs = {
                k: v
                for k, v in kwards.items()
                if k not in ('model_name', 'api_key', 'generation_config', 'system_instruction')
            }

            # Создание экземпляра модели Gemini
            self.gemini = GoogleGenerativeAI(
                model_name=kwards.get('model_name', Config.gemini.model_name),  # Значение из kwards имеет приоритет,
                api_key=kwards.get('api_key', Config.gemini.api_key),
                system_instruction= kwards.get('system_instruction', Config.system_instruction),
                generation_config = {'response_mime_type': kwards.get( 'response_mime_type',  Config.response_mime_type)},
                **filtered_kwargs,
            )
            ...
            return True
        except Exception as ex:
            logger.error(f'Ошибка при инициализации Gemini:', ex, None)
            return False
```

**Назначение**: Инициализация моделей на основе заданных параметров.

**Параметры**:

*   `models_list` (list[str]): Список моделей для инициализации.
*   `**kwards`: Дополнительные аргументы для инициализации моделей.

**Возвращает**:

*   `bool`: `True`, если инициализация моделей прошла успешно, `False` в противном случае.

**Вызывает исключения**:

*   `Exception`: Если произошла ошибка при инициализации моделей.

**Как работает функция**:

1.  Проверяет, есть ли модель `'gemini'` в списке моделей для инициализации.
2.  Если модель `'gemini'` есть в списке, пытается инициализировать модель `GoogleGenerativeAI` с использованием параметров из `kwards` и `Config.gemini`.
3.  В случае успешной инициализации возвращает `True`, в противном случае логирует ошибку и возвращает `False`.

#### `send_file`

```python
def send_file(self, file_path: Path) -> Optional[str | None]:
    """
    Отправка файла в модель.

    Args:
        file_path (Path): Абсолютный путь к файлу, который нужно отправить.
        file_name (Optional[str]): Имя файла для отправки. Если не указано и 'src' отсутствует, используется имя файла без изменений.

    Returns:
        Optional[str | None]: URL файла, если успешно отправлен, иначе None.
    """
    try:
        # Отправка файла в модель
        response = self.gemini.upload_file(file_path)

        if response:
            if hasattr(response, 'url'):
                return response.url

        return None
    except Exception as ex:
        logger.error('Ошибка при отправке файла: ', ex)
        ...
        return None
```

**Назначение**: Отправка файла в модель Gemini.

**Параметры**:

*   `file_path` (Path): Абсолютный путь к файлу, который нужно отправить.

**Возвращает**:

*   `Optional[str | None]`: URL файла, если успешно отправлен, иначе `None`.

**Как работает функция**:

1.  Пытается отправить файл в модель Gemini с использованием метода `self.gemini.upload_file(file_path)`.
2.  Если ответ получен и содержит атрибут `url`, возвращает URL файла.
3.  В случае ошибки логирует ошибку и возвращает `None`.

#### `process_files`

```python
async def process_files(
    self, process_dirs: Optional[str | Path | list[str | Path]] = None, start_from_file: Optional[int] = 1
) -> bool:
    """компиляция, отправка запроса и сохранение результата."""
    Config.process_dirs = process_dirs if process_dirs else Config.process_dirs

    for process_directory in Config.process_dirs:

        process_directory:Path = Path(process_directory)
        logger.info(f'Start {process_directory=}')

        if not process_directory.exists():
            logger.error(f"Директория не существует: {process_directory}")
            continue  # Переходим к следующей директории, если текущая не существует

        if not process_directory.is_dir():
            logger.error(f"Это не директория: {process_directory}", None, False)
            continue  # Переходим к следующей директории, если текущая не является директорией

        for i, (file_path, content) in enumerate(self._yield_files_content(process_directory)):
            if not any((file_path, content)):  # <- ошибка чтения файла
                logger.error(f'Ошибка чтения содержимого файла {file_path}/Content {content} ')
                continue
            if i < start_from_file:  # <- старт с номера файла
                continue
            if file_path and content:
                logger.debug(f'Processed file number: {i}', None, False)
                content_request = self._create_request(file_path, content)
                response = await self.gemini.ask_async(content_request)

                if response:
                    response: str = self._remove_outer_quotes(response)
                    if not await self._save_response(file_path, response, 'gemini'):
                        logger.error(f'Файл {file_path} \n НЕ сохранился')
                        ...
                        continue
                    
                    ...
                else:
                    logger.error('Ошибка ответа модели', None, False)
                    ...
                    continue

            await asyncio.sleep(20)  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG (change timeout)
```

**Назначение**: Компиляция, отправка запроса и сохранение результата обработки файлов.

**Параметры**:

*   `process_dirs` (Optional[str | Path | list[str | Path]]): Список директорий для обработки. По умолчанию `None`.
*   `start_from_file` (Optional[int]): Номер файла, с которого начать обработку. По умолчанию `1`.

**Возвращает**:

*   `bool`: Всегда возвращает `True`, если не возникает исключений.

**Как работает функция**:

1.  Устанавливает значение `Config.process_dirs` на основе переданного аргумента `process_dirs` или значения по умолчанию.
2.  Итерируется по списку директорий для обработки `Config.process_dirs`.
3.  Для каждой директории проверяет, существует ли она и является ли она директорией.
4.  Итерируется по файлам в директории с использованием метода `self._yield_files_content(process_directory)`.
5.  Для каждого файла создает запрос с использованием метода `self._create_request(file_path, content)`.
6.  Отправляет запрос в модель Gemini с использованием метода `self.gemini.ask_async(content_request)`.
7.  Если получен ответ, удаляет внешние кавычки с использованием метода `self._remove_outer_quotes(response)` и сохраняет ответ в файл с использованием метода `self._save_response(file_path, response, 'gemini')`.
8.  В случае ошибки логирует ошибку и переходит к следующему файлу.
9.  После обработки каждого файла ожидает 20 секунд.

#### `_create_request`

```python
def _create_request(self, file_path: str, content: str) -> str:
    """Создание запроса с учетом роли и языка."""
    
    try:
        content_request: dict = {
            'role': Config.role,
            'output_language': Config.lang,
            f'file_location_in_project_hypotez': get_relative_path(file_path, 'hypotez'),
            'instruction': Config.code_instruction or '',
            'input_code': f"""```python
            {content}
            ```""",
        }
    except Exception as ex:
        logger.error(f'Ошибка в составлении запроса ', ex, False)
        ...
        return str(content)

    return str(content_request)
```

**Назначение**: Создание запроса для модели с учетом роли и языка.

**Параметры**:

*   `file_path` (str): Путь к файлу.
*   `content` (str): Содержимое файла.

**Возвращает**:

*   `str`: Строковое представление запроса.

**Как работает функция**:

1.  Создает словарь `content_request`, содержащий роль, язык, путь к файлу, инструкцию и содержимое файла.
2.  Возвращает строковое представление словаря `content_request`.
3.  В случае ошибки логирует ошибку и возвращает строковое представление содержимого файла.

#### `_yield_files_content`

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

    process_directory: Path = process_directory if isinstance(process_directory, Path) else Path(process_directory)

    # Компиляция паттернов исключаемых файлов
    try:
        exclude_files_patterns = [
            re.compile(pattern) for pattern in Config.exclude_files_patterns
        ]

    except Exception as ex:
        logger.error(
            f'Не удалось скомпилировать регулярки из списка:/n{Config.exclude_files_patterns=}\n ', ex
        )
        ...

    # Итерация по всем файлам в директории
    for file_path in process_directory.rglob('*'):
        # Проверка на соответствие шаблонам включения
        if not any(
            fnmatch.fnmatch(file_path.name, pattern) for pattern in Config.include_files_patterns
        ):
            continue

        # Прверка исключенных директорий
        if any(exclude_dir in file_path.parts for exclude_dir in Config.exclude_dirs):
            continue

        # Проверка исключенных файлов по паттерну
        if any(exclude.match(str(file_path.name)) for exclude in exclude_files_patterns):
            continue

        # Проверка конкретных исключенных файлов
        if str(file_path.name) in Config.exclude_files:
            continue

        # Чтение содержимого файла
        try:
            content = file_path.read_text(encoding='utf-8')
            yield file_path, content
            # make_summary( docs_dir = start_dir.parent / 'docs' )  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG  (create `summary.md`)
        except Exception as ex:
            logger.error(f'Ошибка при чтении файла {file_path}', ex)
            ...
            yield None, None

        ...
```

**Назначение**: Генерация путей файлов и их содержимого по указанным шаблонам.

**Параметры**:

*   `process_directory` (str | Path): Абсолютный путь к стартовой директории.

**Возвращает**:

*   `Iterator[tuple[Path, str]]`: Итератор, возвращающий кортежи, содержащие путь к файлу и его содержимое.

**Как работает функция**:

1.  Преобразует `process_directory` в объект `Path`, если это строка.
2.  Компилирует шаблоны исключаемых файлов в регулярные выражения.
3.  Итерируется по всем файлам в директории с использованием метода `rglob('*')`.
4.  Для каждого файла проверяет, соответствует ли он шаблонам включения, не находится ли в исключенной директории, не соответствует ли шаблону исключения и не является ли исключенным файлом.
5.  Если файл проходит все проверки, читает его содержимое и возвращает путь к файлу и его содержимое в виде кортежа.
6.  В случае ошибки при чтении файла логирует ошибку и возвращает `None, None`.

#### `_save_response`

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
    export_path:Path
    try:
        export_path = Path(file_path)
    except Exception as ex:
        logger.error(f'Ошибка пути: {file_path}')
        ...
        return
    try:
        # Получаем директорию для вывода в зависимости от роли
        output_directory_pattern:str = getattr(Config.output_directory_patterns, Config.role)

        # Формируем целевую директорию с учётом подстановки параметров <model> и <lang>
        target_dir = (
            f'docs/{output_directory_pattern}'.replace('<model>', model_name).replace('<lang>', Config.lang)
        )

        # Заменяем часть пути на целевую директорию
        file_path = str(file_path).replace('src', target_dir)

        # Определяем суффикс для добавления в зависимости от роли
        suffix_map = {
            'code_checker': '.md',
            'doc_writer_md': '.md',
            'doc_writer_rst': '.rst',
            'doc_writer_html': '.html',
            'code_explainer_md': '.md',
            'code_explainer_html': '.html',
            'pytest': '.md',
        }
        suffix = suffix_map.get(Config.role, '.md')  # По умолчанию используется .md

        
        if export_path.suffix == '.md' and suffix == '.md':
            export_path = Path(f'{file_path}')
        else:
            export_path = Path(f'{file_path}{suffix}')

        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(response, encoding='utf-8')
        logger.success(f'{export_path.name}')
        return True

    except Exception as ex:
        logger.critical(f'Ошибка сохранения файла: {export_path=}', ex)
        # sys.exit(0)
        return False
```

**Назначение**: Сохранение ответа модели в файл с добавлением суффикса, определяемого ролью.

**Параметры**:

*   `file_path` (Path): Исходный путь к файлу, в который будет записан ответ.
*   `response` (str): Ответ модели, который необходимо сохранить.
*   `model_name` (str): Имя модели, использованной для генерации ответа.

**Возвращает**:

*   `bool`: `True`, если файл успешно сохранен, `False` в противном случае.

**Как работает функция**:

1.  Формирует путь к файлу для сохранения ответа модели.
2.  Определяет суффикс для добавления к имени файла на основе роли.
3.  Создает директорию для сохранения файла, если она не существует.
4.  Сохраняет ответ модели в файл с добавлением суффикса.
5.  В случае ошибки логирует ошибку и возвращает `False`.

#### `_remove_outer_quotes`

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
    try:
        response = response.strip()
    except Exception as ex:
        logger.error('Exception in `_remove_outer_quotes()`', ex, False)
        return ''

    # Если строка начинается с '```python' или '```mermaid', возвращаем её без изменений. Это годный код
    if response.startswith(('```python', '```mermaid'))):
        return response

    # Удаление маркера для известных форматов, если строка обрамлена в '```'
    config = j_loads_ns(
        gs.path.endpoints / 'hypo69' / 'code_assistant' / 'code_assistant.json'
    )
    for prefix in config.remove_prefixes:
        # Сравнение с префиксом без учёта регистра
        if response.lower().startswith(prefix.lower()):
            # Удаляем префикс и суффикс "```", если он есть
            cleaned_response = response[len(prefix) :].strip()
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[: -len('```')].strip()
            return cleaned_response

    # Возврат строки без изменений, если условия не выполнены
    return response
```

**Назначение**: Удаление внешних кавычек в начале и в конце строки, если они присутствуют.

**Параметры**:

*   `response` (str): Ответ модели, который необходимо обработать.

**Возвращает**:

*   `str`: Очищенный контент как строка.

**Как работает функция**:

1.  Удаляет пробельные символы в начале и в конце строки.
2.  Если строка начинается с `'```python'` или `'```mermaid'`, возвращает ее без изменений.
3.  Итерируется по списку префиксов из конфигурационного файла и проверяет, начинается ли строка с одного из префиксов.
4.  Если строка начинается с префикса, удаляет префикс и суффикс `'```'`, если он есть.
5.  Возвращает очищенную строку.

#### `run`

```python
def run(self, start_from_file: int = 1) -> None:
    """Запуск процесса обработки файлов."""
    signal.signal(signal.SIGINT, self._signal_handler)  # Обработка прерывания (Ctrl+C)
    asyncio.run(self.process_files(start_from_file))
```

**Назначение**: Запуск процесса обработки файлов.

**Параметры**:

*   `start_from_file` (int): Номер файла, с которого начать обработку. По умолчанию `1`.

**Как работает функция**:

1.  Устанавливает обработчик сигнала `SIGINT` на метод `self._signal_handler` для обработки прерывания (Ctrl+C).
2.  Запускает асинхронный метод `self.process_files(start_from_file)` для обработки файлов.

#### `_signal_handler`

```python
def _signal_handler(self, signal, frame) -> None:
    """Обработка прерывания выполнения."""
    logger.debug('Процесс был прерван', text_color='red')
    sys.exit(0)
```

**Назначение**: Обработка прерывания выполнения (Ctrl+C).

**Параметры**:

*   `signal`: Сигнал.
*   `frame`: Фрейм.

**Как работает функция**:

1.  Логирует сообщение о прерывании процесса.
2.  Завершает программу с кодом 0.

## Функции

### `parse_args`

```python
def parse_args() -> dict:
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Ассистент для программистов')
    parser.add_argument(
        '--role',
        type=str,
        default='code_checker',
        help='Роль для выполнения задачи',
    )
    parser.add_argument('--lang', type=str, default='ru', help='Язык выполнения')
    parser.add_argument(
        '--model',
        nargs='+',
        type=str,
        default=['gemini'],
        help='Список моделей для инициализации',
    )
    parser.add_argument(
        '--start-dirs',
        nargs='+',
        type=str,
        default=[],
        help='Список директорий для обработки',
    )
    parser.add_argument(
        '--start-file-number',
        type=int,
        default=1,
        help='С какого файла делать обработку. Полезно при сбоях',
    )
    return vars(parser.parse_args())
```

**Назначение**: Разбор аргументов командной строки.

**Параметры**:

*   Нет

**Возвращает**:

*   `dict`: Словарь с аргументами командной строки.

**Как работает функция**:

1.  Создает объект `ArgumentParser` для разбора аргументов командной строки.
2.  Добавляет аргументы `--role`, `--lang`, `--model`, `--start-dirs` и `--start-file-number` с описаниями и значениями по умолчанию.
3.  Разбирает аргументы командной строки с помощью метода `parser.parse_args()`.
4.  Возвращает словарь с аргументами командной строки с помощью функции `vars()`.

**Примеры**:

```python
# Пример вызова функции с аргументами командной строки
# python code_assistant.py --role doc_writer_md --lang ru --model gemini --start-dirs ./src --start-file-number 1
args = parse_args()
print(args)
# {'role': 'doc_writer_md', 'lang': 'ru', 'model': ['gemini'], 'start_dirs': ['./src'], 'start_file_number': 1}
```

### `main`

```python
def main() -> None:
    """
    Функция запускает бесконечный цикл, в котором выполняется обработка файлов с учетом ролей и языков, указанных в конфигурации.
    Конфигурация обновляется в каждом цикле, что позволяет динамически изменять настройки в файле `code_assistant.json` во время работы программы.
    Для каждой комбинации языка и роли создается экземпляр класса :class:`CodeAssistant`, который обрабатывает файлы, используя заданную модель ИИ.
    """

    while True:
       
        # Обработка файлов для каждой комбинации языков и ролей
        for lang in Config.languages_list:
            Config.lang = lang
            for role in Config.roles_list:
                logger.debug(f'Start role: {role}, lang: {lang}', None, False)
                assistant_direct = CodeAssistant(
                    role=role,
                    lang=lang,
                    models_list=['gemini'],
                    system_instruction = Config.system_instruction,
                )
                asyncio.run(assistant_direct.process_files(process_dirs = Config.process_dirs))
```

**Назначение**: Запуск процесса обработки файлов в бесконечном цикле с учетом ролей и языков, указанных в конфигурации.

**Параметры**:

*   Нет

**Как работает функция**:

1.  Запускает бесконечный цикл `while True`.
2.  Итерируется по списку языков `Config.languages_list`.
3.  Итерируется по списку ролей `Config.roles_list`.
4.  Для каждой комбинации языка и роли создает экземпляр класса `CodeAssistant` с заданными параметрами.
5.  Запускает асинхронный метод `assistant_direct.process_files(process_dirs = Config.process_dirs)` для обработки файлов.

Примеры вызова функции:
Для запуска процесса обработки файлов необходимо запустить этот файл.
```python
if __name__ == '__main__':
    main()
```