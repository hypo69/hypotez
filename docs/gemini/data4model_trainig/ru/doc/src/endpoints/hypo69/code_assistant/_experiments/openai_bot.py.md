# Модуль для экспериментов с моделью AI OpenAI

## Обзор

Модуль предназначен для экспериментов с моделью AI OpenAI. Он обрабатывает исходный код или документацию, отправляет его в модель для анализа и получения ответов.
## Подробней

Модуль использует роль выполнения, установленную внутри кода, для взаимодействия с моделью. Для роли `doc_writer` используется модель **OpenAI GPT-4** для генерации документации или других текстов. Входные данные для модели включают комментарии и код/документацию, которые передаются в модель для обработки. Ответ модели сохраняется в файл с расширением `.md` в зависимости от роли.

Используемая модель:
- **OpenAI GPT-4**: Используется для создания документации и других текстовых материалов.

Ссылки на документацию модели:
- OpenAI: https://platform.openai.com/docs

## Функции

### `main`

**Назначение**: Основная функция для обработки файлов и взаимодействия с моделью.

**Описание**:

Функция считывает файл с комментариями, перебирает указанные файлы в исходном каталоге и отправляет содержимое файла в модель для анализа. Затем она обрабатывает ответ модели.

**Как работает функция**:

1.  Определяет глобальную переменную `role`.
2.  Устанавливает роль выполнения, если она не установлена, по умолчанию `doc_writer`.
3.  В зависимости от роли, устанавливает файлы с комментариями и системными инструкциями.
4.  Считывает содержимое файлов с комментариями и системными инструкциями.
5.  Инициализирует модель `OpenAIModel` с системными инструкциями, именем модели и ID ассистента.
6.  Перебирает файлы в исходном каталоге, используя функцию `yield_files_content`.
7.  Для каждого файла формирует входной контент для модели, включая комментарии, расположение файла и код.
8.  Отправляет контент в модель для получения ответа.
9.  Сохраняет ответ модели в файл с расширением `.md`, используя функцию `save_response`.
10. Обрабатывает возможные исключения, логируя ошибки с помощью `logger.error`.
11. Приостанавливает выполнение на 20 секунд, чтобы предотвратить превышение лимитов API.

**Примеры**:

```python
main()
```

### `save_response`

**Назначение**: Сохраняет ответ модели в файл Markdown с обновленным путем в зависимости от роли.

```python
def save_response(file_path: Path, response: str, from_model: str) -> None:
    """ Save the model's response to a markdown file with updated path based on role.

    Args:
        file_path (Path): The original file path being processed.
        response (str): The response from the model to be saved.
    """
    global role

    # Словарь, ассоциирующий роли с директориями
    role_directories = {
        'doc_writer': f'docs/{from_model}/raw_rst_from_ai',
    }

    # Проверка наличия роли в словаре
    if role not in role_directories:
        logger.error(f"Неизвестная роль: {role}. Файл не будет сохранен.")
        return

    # Получаем директорию, соответствующую роли
    role_directory = role_directories[role]

    # Формируем новый путь с учетом роли
    export_file_path = file_path.parts
    new_parts = []

    for part in export_file_path:
        if part == 'src':
            new_parts.append(role_directory)
        else:
            new_parts.append(part)

    # Сформировать новый путь с замененной частью
    export_file_path = Path(*new_parts)

    # Изменить суффикс файла на .md
    export_file_path = export_file_path.with_suffix(".md")

    # Убедиться, что директория существует
    export_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохранить ответ в новый файл
    export_file_path.write_text(response, encoding="utf-8")
    print(f"Response saved to: {export_file_path}")
```

**Параметры**:

*   `file_path` (`Path`): Исходный путь к обрабатываемому файлу.
*   `response` (`str`): Ответ от модели, который необходимо сохранить.
*   `from_model` (`str`): Имя модели, от которой получен ответ.

**Как работает функция**:

1.  Определяет глобальную переменную `role`.
2.  Определяет словарь `role_directories`, который связывает роли с директориями для сохранения файлов.
3.  Проверяет, существует ли роль в словаре `role_directories`. Если роль не найдена, логирует ошибку и выходит из функции.
4.  Получает директорию, соответствующую роли, из словаря `role_directories`.
5.  Формирует новый путь к файлу, заменяя часть пути `'src'` на директорию, соответствующую роли.
6.  Изменяет суффикс файла на `.md`.
7.  Создает директорию для сохранения файла, если она не существует.
8.  Сохраняет ответ модели в файл по новому пути.
9.  Выводит сообщение о том, куда был сохранен ответ.

**Примеры**:

```python
from pathlib import Path
file_path = Path('src/example.py')
response = "This is a sample response from the model."
save_response(file_path, response, 'openai')
```

### `yield_files_content`

**Назначение**: Предоставляет содержимое файлов на основе шаблонов из исходного каталога, исключая определенные шаблоны и каталоги.

```python
def yield_files_content(
    src_path: Path, patterns: list[str]
) -> Iterator[tuple[Path, str]]:
    """ Yield file content based on patterns from the source directory, excluding certain patterns and directories.

    Args:
        src_path (Path): The base directory to search for files.
        patterns (list[str]): List of file patterns to include (e.g., ['*.py', '*.txt']).

    Yields:
        Iterator[tuple[Path, str]]: A tuple of file path and its content as a string.
    """

    # Регулярные выражения для исключаемых файлов и директорий
    exclude_file_patterns = [
        re.compile(r'.*\\(.*\\).*\'),  # Файлы и директории, содержащие круглые скобки
        re.compile(r'___+.*\'),      # Файлы или директории, начинающиеся с трех и более подчеркиваний
    ]

    # Список служебных директорий, которые необходимо исключить
    exclude_dirs = {'.ipynb_checkpoints', '_experiments', '__pycache__', '.git', '.venv'}

    for pattern in patterns:
        for file_path in src_path.rglob(pattern):
            # Пропустить файлы, которые находятся в исключаемых директориях
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue

            # Пропустить файлы, соответствующие исключаемым паттернам
            if any(exclude.match(str(file_path)) for exclude in exclude_file_patterns):
                continue

            # Чтение содержимого файла
            content = file_path.read_text(encoding="utf-8")
            yield file_path, content
```

**Параметры**:

*   `src_path` (`Path`): Базовый каталог для поиска файлов.
*   `patterns` (`list[str]`): Список шаблонов файлов для включения (например, `['*.py', '*.txt']`).

**Возвращает**:

*   `Iterator[tuple[Path, str]]`: Итератор, возвращающий кортежи, содержащие путь к файлу и его содержимое в виде строки.

**Как работает функция**:

1.  Определяет регулярные выражения для исключаемых файлов и директорий.
2.  Определяет список служебных директорий, которые необходимо исключить.
3.  Перебирает шаблоны файлов в списке `patterns`.
4.  Для каждого шаблона перебирает файлы, соответствующие шаблону, используя `src_path.rglob(pattern)`.
5.  Пропускает файлы, которые находятся в исключаемых директориях.
6.  Пропускает файлы, соответствующие исключаемым шаблонам.
7.  Читает содержимое файла и возвращает путь к файлу и его содержимое в виде кортежа.

**Примеры**:

```python
from pathlib import Path
src_path = Path('src')
patterns = ['*.py', 'README.MD']
for file_path, content in yield_files_content(src_path, patterns):
    print(f"File: {file_path}")
    print(f"Content: {content[:100]}...")
```

## Переменные

*   `role` (`str`): Глобальная переменная, определяющая роль выполнения. По умолчанию установлена в `'doc_writer'`.
*   `openai_model_name` (`str`): Имя используемой модели OpenAI, установленное в `'gpt-4o-mini'`.
*   `openai_assistant_id` (`str`): ID ассистента OpenAI, полученный из настроек `gs.credentials.openai.assistant_id.code_assistant`.
*    `openai_model`(`OpenAIModel`): Инстанс класса `OpenAIModel`, который будет использоваться для взаимодействия с OpenAI API.