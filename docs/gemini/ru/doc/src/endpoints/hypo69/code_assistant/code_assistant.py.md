# Модуль `code_assistant`

## Обзор

Модуль предназначен для обучения модели машинного обучения на кодовой базе, создания документации к проекту, генерации примеров кода и тестов. Он включает в себя класс `CodeAssistant`, который читает файлы кода, отправляет код в модели, получает обработанный код от модели и сохраняет результат в директории `docs/gemini`. В зависимости от заданной роли, файлы сохраняются в различных поддиректориях.

## Подробнее

Модуль `code_assistant` автоматизирует процесс анализа и документирования кодовой базы. Он позволяет использовать различные AI-модели для обработки кода и генерации документации, примеров кода и тестов. Это значительно упрощает поддержку и развитие проекта, обеспечивая актуальную и качественную документацию.

## Классы

### `Config`

**Описание**: Класс, содержащий конфигурационные параметры для работы `CodeAssistant`.

**Атрибуты**:

- `ENDPOINT` (Path): Путь к директории с конфигурационными файлами.
- `config` (SimpleNamespace): Объект, содержащий конфигурационные параметры из файла `code_assistant.json`.
- `roles_list` (list): Список ролей, определенных в конфигурации.
- `languages_list` (list): Список языков, определенных в конфигурации.
- `role` (str): Текущая роль ассистента (по умолчанию `'doc_writer_md'`).
- `lang` (str): Текущий язык ассистента (по умолчанию `'ru'`).
- `process_dirs` (list[Path]): Список директорий для обработки.
- `exclude_dirs` (list[Path]): Список директорий, которые следует исключить из обработки.
- `exclude_files_patterns` (list[Path]): Список шаблонов файлов, которые следует исключить из обработки.
- `include_files_patterns` (list[Path]): Список шаблонов файлов, которые следует включить в обработку.
- `exclude_files` (list[Path]): Список конкретных файлов, которые следует исключить из обработки.
- `response_mime_type` (str): MIME-тип ответа (по умолчанию из конфигурации).
- `output_directory_patterns` (list): Шаблоны для формирования директорий вывода.
- `remove_prefixes` (str): Префиксы, которые нужно удалять из ответов модели.
- `gemini` (SimpleNamespace): Конфигурация для модели Gemini, включающая имя модели и ключ API.

**Методы**:

- `code_instruction`: Возвращает инструкцию для кода, читая файл с инструкциями на основе текущей роли и языка.
- `system_instruction`: Возвращает общую инструкцию для модели, читая файл с общими правилами на основе текущего языка.

### `CodeAssistant`

**Описание**: Класс для работы ассистента программиста с моделями ИИ.

**Атрибуты**:

- `role` (str): Роль ассистента.
- `lang` (str): Язык ассистента.
- `gemini` (GoogleGenerativeAi): Инстанс класса `GoogleGenerativeAi` для работы с моделью Gemini.
- `openai` (OpenAIModel): Инстанс класса `OpenAIModel` для работы с моделью OpenAI.

**Методы**:

- `__init__`: Инициализация ассистента с заданными параметрами.
- `send_file`: Отправка файла в модель.
- `process_files`: Компиляция, отправка запроса и сохранение результата.
- `_create_request`: Создание запроса с учетом роли и языка.
- `_yield_files_content`: Генерация путей файлов и их содержимого по указанным шаблонам.
- `_save_response`: Сохранение ответа модели в файл с добавлением суффикса.
- `_remove_outer_quotes`: Удаление внешних кавычек в начале и в конце строки, если они присутствуют.
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
Возвращает инструкцию для кода, читая файл с инструкциями на основе текущей роли и языка.

**Как работает функция**:
Функция `code_instruction` использует декораторы `@classmethod` и `@property`, чтобы быть методом класса и одновременно свойством. Это позволяет обращаться к ней как к атрибуту класса (`Config.code_instruction`). При каждом обращении к этому свойству происходит чтение файла с инструкцией, что позволяет обновлять инструкции "на лету". Путь к файлу формируется на основе текущей роли (`Config.role`) и языка (`Config.lang`), а также константы `Config.ENDPOINT`, определяющей базовую директорию для инструкций.

**Примеры**:
```python
# Пример использования code_instruction
instruction = Config.code_instruction
print(instruction)
```

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
Возвращает общую инструкцию для модели, читая файл с общими правилами на основе текущего языка.

**Как работает функция**:
Функция `system_instruction` использует декораторы `@classmethod` и `@property`, чтобы быть методом класса и одновременно свойством. Это позволяет обращаться к ней как к атрибуту класса (`Config.system_instruction`). При каждом обращении к этому свойству происходит чтение файла с инструкцией, что позволяет обновлять инструкции "на лету". Путь к файлу формируется на основе текущего языка (`Config.lang`), а также константы `Config.ENDPOINT`, определяющей базовую директорию для инструкций.

**Примеры**:
```python
# Пример использования system_instruction
instruction = Config.system_instruction
print(instruction)
```

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
                model_name = model_name,\
                api_key=kwargs.get('api_key', Config.gemini.api_key),# Значение из kwargs имеет приоритет,\
                system_instruction= system_instruction or Config.system_instruction,\
                generation_config = {'response_mime_type': kwargs.get( 'response_mime_type',  Config.response_mime_type)},\
                **filtered_kwargs,\
            )
        ...
```

**Назначение**:
Инициализирует экземпляр класса `CodeAssistant` с заданными параметрами, такими как роль, язык и используемые модели.

**Параметры**:
- `role` (Optional[str]): Роль для выполнения задачи (по умолчанию `'doc_writer_md'`).
- `lang` (Optional[str]): Язык выполнения (по умолчанию `'en'`).
- `model_name` (str): Имя модели для использования (по умолчанию `'gemini-2.0-flash-exp'`).
- `system_instruction` (Optional[str | Path]): Общая инструкция для модели.
- `**kwargs`: Дополнительные аргументы для инициализации моделей.

**Как работает функция**:
Функция `__init__` выполняет следующие шаги:
1. Устанавливает значения `Config.role` и `Config.lang` на основе переданных аргументов, если они указаны, иначе использует значения по умолчанию из класса `Config`.
2. Фильтрует `kwargs`, чтобы исключить параметры, которые не должны передаваться в конструктор `GoogleGenerativeAi`.
3. Инициализирует атрибут `self.gemini` экземпляром класса `GoogleGenerativeAi`, передавая необходимые параметры, такие как имя модели, ключ API, системную инструкцию и конфигурацию генерации.

**Примеры**:
```python
# Пример инициализации CodeAssistant
assistant = CodeAssistant(role='code_checker', lang='ru', model_name='gemini-2.0-flash-exp')
```

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
Отправляет файл в модель Gemini для обработки.

**Параметры**:
- `file_path` (Path): Абсолютный путь к файлу, который нужно отправить.

**Возвращает**:
- `Optional[str | None]`: URL файла, если файл успешно отправлен, иначе `None`.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при отправке файла.

**Как работает функция**:
1. Пытается отправить файл по указанному пути в модель Gemini, используя метод `self.gemini.upload_file(file_path)`.
2. Если ответ получен и содержит атрибут `url`, функция возвращает этот URL.
3. В случае ошибки логирует ошибку с использованием `logger.error` и возвращает пустую строку.

**Примеры**:
```python
# Пример использования send_file
file_path = Path('/path/to/your/file.py')
url = assistant.send_file(file_path)
if url:
    print(f"Файл успешно отправлен. URL: {url}")
else:
    print("Не удалось отправить файл.")
```

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
- `process_dirs` (Optional[str | Path | list[str | Path]]): Директория или список директорий для обработки. Если не указана, используется `Config.process_dirs`.

**Возвращает**:
- `bool`: `True`, если обработка завершилась успешно, иначе `False`.

**Как работает функция**:

1. **Подготовка**:
   - Если `process_dirs` не указан, используется значение из `Config.process_dirs`.
   - Выполняется итерация по каждой директории в `process_dirs`.
   - Проверяется существование и тип директории. В случае отсутствия или некорректного типа директории, в лог записывается ошибка, и происходит переход к следующей директории.
2. **Обработка файлов**:
   - Для каждого файла, полученного из `self._yield_files_content(process_directory)`, выполняется:
     - Проверка на наличие ошибок при чтении файла. Если `file_path` или `content` отсутствуют, в лог записывается ошибка, и происходит переход к следующему файлу.
     - Формирование запроса с использованием `self._create_request(file_path, content)`.
     - Отправка запроса в модель Gemini с использованием `self.gemini.ask_async(content_request)`.
     - Обработка ответа:
       - Удаление внешних кавычек из ответа с использованием `self._remove_outer_quotes(response)`.
       - Сохранение ответа с использованием `self._save_response(file_path, response, 'gemini')`. Если файл не удалось сохранить, в лог записывается ошибка, и происходит переход к следующему файлу.
       - При возникновении ошибки ответа модели - происходит переход к следующему файлу.
3. **Задержка**:
   - После обработки каждого файла выполняется асинхронная задержка в 20 секунд.

**Примеры**:
```python
# Пример вызова функции process_files
assistant = CodeAssistant()
asyncio.run(assistant.process_files(process_dirs=['/path/to/your/directory']))
```

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
Создает запрос для отправки в модель, учитывая роль и язык.

**Параметры**:
- `file_path` (str): Путь к файлу.
- `content` (str): Содержимое файла.

**Возвращает**:
- `str`: Строковое представление запроса.

**Как работает функция**:
1. Формирует словарь `content_request`, включающий:
   - `role`: Роль из `Config.role`.
   - `output_language`: Язык из `Config.lang`.
   - `file_location_in_project_hypotez`: Относительный путь к файлу, полученный с помощью `get_relative_path`.
   - `instruction`: Инструкция из `Config.code_instruction`.
   - `input_code`: Код файла, обернутый в теги ```python.
2. Преобразует словарь в строку и возвращает её.

**Примеры**:
```python
# Пример использования _create_request
file_path = '/path/to/your/file.py'
content = 'print("Hello, world!")'
request = assistant._create_request(file_path, content)
print(request)
```

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
Генерирует пути файлов и их содержимое в указанной директории, исключая файлы и директории, соответствующие заданным шаблонам.

**Параметры**:
- `process_directory` (str | Path): Путь к директории, в которой нужно искать файлы.

**Возвращает**:
- `Iterator[tuple[Path, str]]`: Итератор, возвращающий кортежи, содержащие путь к файлу и его содержимое.

**Как работает функция**:
1. Преобразует `process_directory` в объект `Path`, если это строка.
2. Компилирует шаблоны исключаемых файлов из `Config.exclude_files_patterns` в регулярные выражения.
3. Итерируется по всем файлам в `process_directory` и поддиректориях с помощью `rglob('*')`.
4. Для каждого файла выполняет следующие проверки:
   - Проверяет, соответствует ли имя файла какому-либо шаблону включения из `Config.include_files_patterns`. Если нет, переходит к следующему файлу.
   - Проверяет, содержится ли какая-либо исключенная директория из `Config.exclude_dirs` в пути к файлу. Если да, переходит к следующему файлу.
   - Проверяет, соответствует ли имя файла какому-либо шаблону исключения из `exclude_files_patterns`. Если да, переходит к следующему файлу.
   - Проверяет, находится ли имя файла в списке исключенных файлов `Config.exclude_files`. Если да, переходит к следующему файлу.
5. Если файл проходит все проверки, функция пытается прочитать его содержимое. В случае успеха возвращает путь к файлу и его содержимое. Если при чтении возникает ошибка, в лог записывается информация об ошибке, и возвращается `None, None`.

**Примеры**:
```python
# Пример использования _yield_files_content
process_directory = '/path/to/your/directory'
for file_path, content in assistant._yield_files_content(process_directory):
    if file_path and content:
        print(f"Обработка файла: {file_path}")
        # Дальнейшая обработка содержимого файла
```

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
- `bool`: `True`, если файл успешно сохранен, иначе `False`.

**Как работает функция**:
1. Проверяет существование исходного файла. Если файл не существует, записывает ошибку в лог и возвращает `False`.
2. Определяет директорию для сохранения файла в зависимости от роли, извлекая шаблон из `Config.output_directory_patterns`.
3. Формирует целевую директорию, заменяя параметры `<model>`, `<lang>` и `<module>` в шаблоне.
4. Определяет суффикс файла на основе роли из `suffix_map`. Если роль не найдена в `suffix_map`, используется суффикс `.md` по умолчанию.
5. Формирует полный путь к файлу, объединяя корневую директорию проекта, целевую директорию и суффикс.
6. Создает директорию для сохранения файла, если она не существует.
7. Записывает ответ модели в файл. В случае успеха записывает сообщение об успехе в лог и возвращает `True`. В случае ошибки записывает сообщение об ошибке в лог и возвращает `False`.
8. В случае возникновения исключения на любом этапе процесса, записывает критическое сообщение об ошибке в лог и возвращает `False`.

**Примеры**:
```python
# Пример использования _save_response
file_path = Path('/path/to/your/file.py')
response = 'This is the response from the model.'
model_name = 'gemini'
result = asyncio.run(assistant._save_response(file_path, response, model_name))
if result:
    print('Файл успешно сохранен.')
else:
    print('Не удалось сохранить файл.')
```

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
                cleaned_response = response[len(prefix) :] .strip()
                if cleaned_response.endswith('```'):
                    cleaned_response = cleaned_response[: -len('```')].strip()
                return cleaned_response

        # Возврат строки без изменений, если условия не выполнены
        return response
```

**Назначение**:
Удаляет внешние кавычки и префиксы из ответа модели, если они присутствуют.

**Параметры**:
- `response` (str): Ответ модели, который необходимо обработать.

**Возвращает**:
- `str`: Очищенный контент как строка.

**Как работает функция**:
1. Удаляет пробельные символы в начале и конце строки.
2. Если строка начинается с `'```python'` или `'```mermaid'`, возвращает её без изменений.
3. Перебирает префиксы из `Config.remove_prefixes` и проверяет, начинается ли строка с одного из этих префиксов (без учета регистра).
4. Если префикс найден, удаляет его из строки, а также удаляет суффикс `'```'`, если он присутствует.
5. Если ни одно из условий не выполнено, возвращает строку без изменений.

**Примеры**:
```python
# Пример использования _remove_outer_quotes
response = "```md This is some content ```"
cleaned_response = assistant._remove_outer_quotes(response)
print(cleaned_response)  # Вывод: This is some content

response = "Some content"
cleaned_response = assistant._remove_outer_quotes(response)
print(cleaned_response)  # Вывод: Some content

response = "```python def hello(): print('Hello') ```"
cleaned_response = assistant._remove_outer_quotes(response)
print(cleaned_response)  # Вывод: ```python def hello(): print('Hello') ```
```

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
- `start_from_file` (int): Номер файла, с которого начинается обработка (по умолчанию `1`).

**Как работает функция**:
1. Устанавливает обработчик сигнала `SIGINT` для прерывания процесса (Ctrl+C).
2. Запускает асинхронную функцию `self.process_files` для обработки файлов.

**Примеры**:
```python
# Пример использования run
assistant = CodeAssistant()
assistant.run()
```

### `_signal_handler`

```python
    def _signal_handler(self, signal, frame) -> None:
        """Обработка прерывания выполнения."""
        logger.debug('Процесс был прерван', text_color='red')
        sys.exit(0)
```

**Назначение**:
Обрабатывает прерывание выполнения (например, при нажатии Ctrl+C).

**Параметры**:
- `signal`: Номер сигнала.
- `frame`: Текущий кадр стека вызовов.

**Как работает функция**:
1. Регистрирует сообщение в логе о прерывании процесса.
2. Завершает выполнение программы с кодом 0.

**Примеры**:
```python
# Пример использования _signal_handler (не вызывается напрямую)
# Функция вызывается автоматически при получении сигнала SIGINT
```

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
Разбирает аргументы командной строки и возвращает их в виде словаря.

**Параметры**:
- Нет.

**Возвращает**:
- `dict`: Словарь, содержащий аргументы командной строки.

**Как работает функция**:
1. Создает экземпляр `argparse.ArgumentParser` с описанием 'Ассистент для программистов'.
2. Добавляет аргументы:
   - `--role`: Роль для выполнения задачи (по умолчанию 'code_checker').
   - `--lang`: Язык выполнения (по умолчанию 'ru').
   - `--model`: Список моделей для инициализации (по умолчанию ['gemini']).
   - `--start-dirs`: Список директорий для обработки (по умолчанию пустой список).
   - `--start-file-number`: С какого файла начинать обработку (по умолчанию 1).
3. Разбирает аргументы с помощью `parser.parse_args()` и преобразует их в словарь с помощью `vars()`.

**Примеры**:
```python
# Пример использования parse_args
args = parse_args()
print(args)
```

### `main`

```python
def main() -> None:
    """
    Функция