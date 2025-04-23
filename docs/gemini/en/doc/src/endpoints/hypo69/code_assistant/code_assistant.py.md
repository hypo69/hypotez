# Модуль `code_assistant.py`

## Обзор

Модуль предназначен для обучения модели машинного обучения на кодовой базе, создания документации к проекту, примеров кода и тестов. Он содержит класс `CodeAssistant`, который читает файлы кода, передает код в модели машинного обучения, обрабатывает его и возвращает результат. Затем класс сохраняет результат в директории `docs/gemini` в зависимости от роли.

## Более подробно

Этот модуль автоматизирует процесс создания документации, примеров кода и тестов для проекта, используя возможности моделей машинного обучения. Он позволяет динамически изменять настройки и инструкции для моделей, что делает процесс более гибким и адаптивным.

## Классы

### `Config`

**Описание**: Класс, содержащий конфигурационные параметры для работы ассистента кода.

**Атрибуты**:
- `ENDPOINT` (Path): Путь к директории `code_assistant`.
- `config` (SimpleNamespace): Объект, содержащий конфигурацию из файла `code_assistant.json`.
- `roles_list` (list): Список ролей.
- `languages_list` (list): Список языков.
- `role` (str): Текущая роль.
- `lang` (str): Текущий язык.
- `process_dirs` (list[Path]): Список директорий для обработки.
- `exclude_dirs` (list[Path]): Список директорий, исключенных из обработки.
- `exclude_files_patterns` (list[Path]): Список шаблонов имен файлов, исключенных из обработки.
- `include_files_patterns` (list[Path]): Список шаблонов имен файлов, включенных в обработку.
- `exclude_files` (list[Path]): Список файлов, исключенных из обработки.
- `response_mime_type` (str): MIME-тип ответа.
- `output_directory_patterns` (list): Список шаблонов для директорий вывода.
- `remove_prefixes` (str): Префиксы, удаляемые из ответа модели.
- `gemini` (SimpleNamespace): Конфигурация для модели Gemini, включая имя модели и ключ API.

**Методы**:
- `code_instruction`: Инструкция для кода. При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету".
- `system_instruction`: Инструкция для модели. При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету".

### `CodeAssistant`

**Описание**: Класс для работы ассистента программиста с моделями ИИ.

**Атрибуты**:
- `role` (str): Роль для выполнения задачи.
- `lang` (str): Язык выполнения.
- `gemini` (GoogleGenerativeAi): Экземпляр класса `GoogleGenerativeAi` для работы с моделью Gemini.
- `openai` (OpenAIModel): Экземпляр класса `OpenAIModel` для работы с моделью OpenAI.

**Методы**:
- `__init__`: Инициализация ассистента с заданными параметрами.
- `send_file`: Отправка файла в модель.
- `process_files`: Компиляция, отправка запроса и сохранение результата.
- `_create_request`: Создание запроса с учетом роли и языка.
- `_yield_files_content`: Генерирует пути файлов и их содержимое по указанным шаблонам.
- `_save_response`: Сохранение ответа модели в файл с добавлением суффикса.
- `_remove_outer_quotes`: Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.
- `run`: Запуск процесса обработки файлов.
- `_signal_handler`: Обработка прерывания выполнения.

## Методы класса `Config`

### `code_instruction`

```python
    @classmethod
    @property
    def code_instruction(self):
        """code_instruction - Инструкция для кода.
        При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету"
        """
        return Path( Config.ENDPOINT / 'instructions'/ f'instruction_{Config.role}_{Config.lang}.md'
            ).read_text(encoding='UTF-8')
```

**Назначение**:
Возвращает инструкцию для обработки кода, считывая ее из файла.

**Как работает**:
- Формирует путь к файлу инструкции на основе текущей роли и языка.
- Считывает содержимое файла и возвращает его.

### `system_instruction`

```python
    @classmethod
    @property
    def system_instruction(self):
        """Инструкция для модели.
        При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету
        """        
        return Path(Config.ENDPOINT / 'instructions' / f'CODE_RULES.{Config.lang}.MD'
                            ).read_text(encoding='UTF-8')
```

**Назначение**:
Возвращает системную инструкцию для модели машинного обучения, считывая ее из файла.

**Как работает**:
- Формирует путь к файлу инструкции на основе текущего языка.
- Считывает содержимое файла и возвращает его.

## Методы класса `CodeAssistant`

### `__init__`

```python
    def __init__(
        self,
        role: Optional[str] = 'doc_writer_md',
        lang: Optional[str] = 'en',
        model_name:str = 'gemini-2.0-flash-exp',
        system_instruction: Optional[str | Path] = None,
        **kwargs,
    ) -> None:
        """
        Инициализация ассистента с заданными параметрами.

        Args:
            role (str): Роль для выполнения задачи.
            lang (str): Язык выполнения.
            models_list (list[str]): Список моделей для инициализации.
            system_instruction (str|Path): Общая инструкция для модели. 
            **kwargs: Дополнительные аргументы для инициализации моделей.
        """
        Config.role = role if role else Config.role
        Config.lang = lang if lang else Config.lang
        Config.system_instruction = system_instruction if system_instruction else Config.system_instruction
        filtered_kwargs = {
                    k: v
                    for k, v in kwargs.items()
                    if k not in ('model_name', 'api_key', 'generation_config', 'system_instruction')
                }
        self.gemini = GoogleGenerativeAi(     
                model_name = model_name,
                api_key=kwargs.get('api_key', Config.gemini.api_key),# Значение из kwargs имеет приоритет,
                system_instruction= system_instruction or Config.system_instruction,
                generation_config = {'response_mime_type': kwargs.get( 'response_mime_type',  Config.response_mime_type)},
                **filtered_kwargs,
            )
        ...
```

**Назначение**:
Инициализирует ассистента с заданными параметрами, такими как роль, язык и модель машинного обучения.

**Параметры**:
- `role` (str, optional): Роль для выполнения задачи. По умолчанию 'doc_writer_md'.
- `lang` (str, optional): Язык выполнения. По умолчанию 'en'.
- `model_name` (str): Имя модели для использования. По умолчанию 'gemini-2.0-flash-exp'.
- `system_instruction` (str | Path, optional): Общая инструкция для модели.
- `**kwargs`: Дополнительные аргументы для инициализации моделей.

**Как работает**:
- Устанавливает значения роли, языка и инструкции из переданных аргументов или из конфигурации.
- Создает экземпляр класса `GoogleGenerativeAi` для работы с моделью Gemini, передавая необходимые параметры.

### `send_file`

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
            response:str = self.gemini.upload_file(file_path)

            if response:
                if hasattr(response, 'url'):
                    return response.url

                ...
                return ''
        except Exception as ex:
            logger.error('Ошибка при отправке файла: ', ex)
            ...
            return ''
```

**Назначение**:
Отправляет файл в модель машинного обучения для обработки.

**Параметры**:
- `file_path` (Path): Абсолютный путь к файлу, который нужно отправить.

**Возвращает**:
- `Optional[str | None]`: URL файла, если успешно отправлен, иначе `None`.

**Как работает**:
- Вызывает метод `upload_file` класса `GoogleGenerativeAi` для отправки файла в модель Gemini.
- Если отправка прошла успешно и ответ содержит URL, возвращает этот URL.
- В случае ошибки логирует ошибку и возвращает пустую строку.

### `process_files`

```python
    async def process_files(
        self, process_dirs: Optional[str | Path | list[str | Path]] = None, 
    ) -> bool:
        """компиляция, отправка запроса и сохранение результата."""
        process_dirs = process_dirs if process_dirs else Config.process_dirs

        for process_directory in process_dirs:

            process_directory:Path = Path(process_directory)
            logger.info(f'Start {process_directory=}')

            if not process_directory.exists():
                logger.error(f"Директория не существует: {process_directory}")
                continue  # Переход к следующей директории, если текущая не существует

            if not process_directory.is_dir():
                logger.error(f"Это не директория: {process_directory}", None, False)
                continue  # Переход к следующей директории, если текущая не является директорией

            for i, (file_path, content) in enumerate(self._yield_files_content(process_directory)):
                if not any((file_path, content)):  # <- ошибка чтения файла
                    logger.error(f'Ошибка чтения содержимого файла {file_path}/Content {content} ')
                    continue

                if file_path and content:
                    logger.debug(f'Чтение файла номер: {i+1}\n{file_path}', None, False)
                    content_request = self._create_request(file_path, content)
                    response = await self.gemini.ask_async(content_request)
                    #response = await self.gemini.chat(content_request,'coder')

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

**Назначение**:
Компилирует, отправляет запрос и сохраняет результат обработки файлов.

**Параметры**:
- `process_dirs` (str | Path | list[str | Path], optional): Список директорий для обработки. Если не указан, используется `Config.process_dirs`.

**Возвращает**:
- `bool`: `True`, если обработка прошла успешно, иначе `False`.

**Как работает**:
- Итерируется по списку директорий для обработки.
- Для каждой директории проверяет ее существование и является ли она директорией.
- Использует метод `_yield_files_content` для получения путей файлов и их содержимого.
- Для каждого файла создает запрос с использованием метода `_create_request`.
- Отправляет запрос в модель Gemini с использованием метода `ask_async`.
- Обрабатывает ответ модели, удаляя внешние кавычки с помощью метода `_remove_outer_quotes`.
- Сохраняет ответ в файл с помощью метода `_save_response`.
- В случае ошибки логирует ее.

### `_create_request`

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

**Назначение**:
Создает запрос для модели машинного обучения с учетом роли, языка и содержимого файла.

**Параметры**:
- `file_path` (str): Путь к файлу.
- `content` (str): Содержимое файла.

**Возвращает**:
- `str`: Запрос в виде строки.

**Как работает**:
- Создает словарь, содержащий роль, язык, путь к файлу в проекте, инструкцию и содержимое файла.
- Преобразует словарь в строку и возвращает ее.
- В случае ошибки логирует ее и возвращает содержимое файла.

### `_yield_files_content`

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
                # make_summary( docs_dir = start_dir.parent / 'docs' )  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG  (create `summary.md`)\
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла {file_path}', ex)
                ...
                yield None, None

            ...
```

**Назначение**:
Генерирует пути файлов и их содержимое по указанным шаблонам, исключая файлы и директории, указанные в конфигурации.

**Параметры**:
- `process_directory` (str | Path): Абсолютный путь к стартовой директории.

**Возвращает**:
- `Iterator[tuple[Path, str]]`: Итератор, возвращающий кортежи, содержащие путь к файлу и его содержимое.

**Как работает**:
- Компилирует шаблоны исключаемых файлов в регулярные выражения.
- Итерируется по всем файлам в директории, используя `rglob('*')`.
- Проверяет, соответствует ли имя файла хотя бы одному шаблону включения.
- Проверяет, не находится ли файл в исключенной директории.
- Проверяет, не соответствует ли имя файла хотя бы одному шаблону исключения.
- Проверяет, не является ли файл явно исключенным.
- Считывает содержимое файла и возвращает путь к файлу и его содержимое.
- В случае ошибки логирует ее и возвращает `None` для пути и содержимого файла.

### `_save_response`

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
        export_path:Path = None
        if not Path(file_path).exists(): 
            logger.error(f'Ошибка пути: {file_path}')
            ...
            return False

        try:
            # Получение директории  в зависимости от роли
            _pattern:str = getattr(Config.output_directory_patterns, Config.role)

            for i, part in enumerate(file_path.parts):
                if part == 'hypotez':
                    relative_path = Path(*file_path.parts[i+1:])
                    break

            # Формирование целевой директории с учётом подстановки параметров <model> и <lang>
            target_dir: str = (
                f'docs/{_pattern}'
                .replace('<model>', model_name)
                .replace('<lang>', Config.lang)
                .replace('<module>', str(relative_path))
                )



            # суффикс в зависимости от роли
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

            export_path:Path = Path(f'{__root__/ target_dir}{suffix}')  # Полный путь к конеччому файлу документации

            export_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                export_path.write_text(response, encoding='utf-8')
                logger.success(f'Файл сохранён В:\n{export_path}')
                return True
            except Exception as e:
                logger.error(f'Файл не сохранился по адресу:\n{export_path}\nОшибка: {e}')
                return False


        except Exception as ex:
            logger.critical(f'Ошибка сохранения файла:\n{file_path=}', ex, False)
            ...
            return False
```

**Назначение**:
Сохраняет ответ модели в файл с добавлением суффикса, определяемого ролью.

**Параметры**:
- `file_path` (Path): Исходный путь к файлу, в который будет записан ответ.
- `response` (str): Ответ модели, который необходимо сохранить.
- `model_name` (str): Имя модели, использованной для генерации ответа.

**Возвращает**:
- `bool`: `True`, если сохранение прошло успешно, иначе `False`.

**Как работает**:
- Формирует путь к файлу, в который будет сохранен ответ, на основе роли, языка и имени модели.
- Создает директорию для файла, если она не существует.
- Записывает ответ в файл.
- В случае ошибки логирует ее.

### `_remove_outer_quotes`

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
        if response.startswith(('```python', '```mermaid')):\
            return response

        for prefix in Config.remove_prefixes:
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

**Назначение**:
Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.

**Параметры**:
- `response` (str): Ответ модели, который необходимо обработать.

**Возвращает**:
- `str`: Очищенный контент как строка.

**Как работает**:
- Удаляет пробелы в начале и в конце строки.
- Если строка начинается с `'```python'` или `'```mermaid'`, возвращает ее без изменений.
- Итерируется по списку префиксов, которые нужно удалить.
- Если строка начинается с префикса (без учета регистра), удаляет префикс и суффикс `'```'`, если он есть.
- Возвращает очищенную строку.
- В случае ошибки логирует ее и возвращает пустую строку.

### `run`

```python
    def run(self, start_from_file: int = 1) -> None:
        """Запуск процесса обработки файлов."""
        signal.signal(signal.SIGINT, self._signal_handler)  # Обработка прерывания (Ctrl+C)
        asyncio.run(self.process_files(start_from_file))
```

**Назначение**:
Запускает процесс обработки файлов.

**Параметры**:
- `start_from_file` (int, optional): Номер файла, с которого начать обработку. По умолчанию 1.

**Как работает**:
- Устанавливает обработчик сигнала `SIGINT` для обработки прерывания (Ctrl+C).
- Запускает асинхронную функцию `process_files`.

### `_signal_handler`

```python
    def _signal_handler(self, signal, frame) -> None:
        """Обработка прерывания выполнения."""
        logger.debug('Процесс был прерван', text_color='red')
        sys.exit(0)
```

**Назначение**:
Обрабатывает прерывание выполнения (Ctrl+C).

**Параметры**:
- `signal`: Сигнал.
- `frame`: Фрейм стека.

**Как работает**:
- Логирует сообщение о прерывании процесса.
- Завершает процесс с кодом 0.

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

**Назначение**:
Разбирает аргументы командной строки.

**Возвращает**:
- `dict`: Словарь, содержащий значения аргументов командной строки.

**Как работает**:
- Создает объект `ArgumentParser`.
- Добавляет аргументы `--role`, `--lang`, `--model`, `--start-dirs` и `--start-file-number`.
- Разбирает аргументы командной строки с помощью метода `parse_args`.
- Возвращает словарь, содержащий значения аргументов.

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
            
            for role in Config.roles_list:
                logger.debug(f'Start role: {role}, lang: {lang}', None, False)
                assistant_direct = CodeAssistant(
                    role=role,
                    lang=lang,
                    # model_name = Config.model_name,
                    # system_instruction = Config.system_instruction,
                )
                asyncio.run(assistant_direct.process_files(process_dirs = Config.process_dirs))


if __name__ == '__main__':
    main()
```

**Назначение**:
Запускает бесконечный цикл, в котором выполняется обработка файлов с учетом ролей и языков, указанных в конфигурации.

**Как работает**:
- В бесконечном цикле итерируется по списку языков и ролей, указанных в конфигурации.
- Для каждой комбинации языка и роли создает экземпляр класса `CodeAssistant`.
- Запускает обработку файлов с помощью метода `process_files`.