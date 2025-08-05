# Модуль для обучения модели OpenAI для AliExpress
===============================================================

Модуль для обучения модели OpenAI для AliExpress.  

##  Содержание
- **Описание модуля**: [Описание модуля](#Описание-модуля)
- **Функции**:
    -  `recursively_get_filenames` : [Функция `recursively_get_filenames`](#Функция-recursively_get_filenames)
    -  `read_text_file` : [Функция `read_text_file`](#Функция-read_text_file)
    -  `csv2json_csv2dict` : [Функция `csv2json_csv2dict`](#Функция-csv2json_csv2dict)
    -  `pprint` : [Функция `pprint`](#Функция-pprint)
    -  `OpenAIModel` : [Класс `OpenAIModel`](#Класс-OpenAIModel)
    -  `GoogleGenerativeAi` : [Класс `GoogleGenerativeAi`](#Класс-GoogleGenerativeAi)


## Описание модуля
Модуль содержит код для обучения модели OpenAI для AliExpress. Он использует данные из файлов с названиями товаров для AliExpress и обучается на них с помощью модели OpenAI. 

## Функции

### Функция `recursively_get_filenames`
```python
def recursively_get_filenames(
    dir_path: Path,
    ext: str,
    include_hidden: bool = False,
    case_sensitive: bool = False,
) -> List[Path]:
    """
    Функция рекурсивно обходит директорию и возвращает список путей к файлам,
    соответствующих заданному расширению.

    Args:
        dir_path (Path): Путь к директории.
        ext (str): Расширение файла.
        include_hidden (bool): Включать скрытые файлы. По умолчанию `False`.
        case_sensitive (bool): Чувствительность к регистру. По умолчанию `False`.

    Returns:
        List[Path]: Список путей к файлам.

    Example:
        >>> from pathlib import Path
        >>> dir_path = Path('path/to/directory')
        >>> filenames = recursively_get_filenames(dir_path, '.txt')
        >>> print(filenames)
        [Path('path/to/directory/file1.txt'), Path('path/to/directory/subdirectory/file2.txt')]
    """
    files = []
    for path in dir_path.rglob(f"*{ext}"):
        if not include_hidden and path.name.startswith("."):
            continue
        files.append(path)
    return files
```
####  Описание
Функция рекурсивно обходит директорию и возвращает список путей к файлам, соответствующих заданному расширению.

#### Параметры:
- `dir_path (Path)`: Путь к директории.
- `ext (str)`: Расширение файла.
- `include_hidden (bool)`: Включать скрытые файлы. По умолчанию `False`.
- `case_sensitive (bool)`: Чувствительность к регистру. По умолчанию `False`.

#### Возвращает:
- `List[Path]`: Список путей к файлам.

#### Пример:
```python
>>> from pathlib import Path
>>> dir_path = Path('path/to/directory')
>>> filenames = recursively_get_filenames(dir_path, '.txt')
>>> print(filenames)
[Path('path/to/directory/file1.txt'), Path('path/to/directory/subdirectory/file2.txt')]
```
### Функция `read_text_file`
```python
def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    if Path(file_path).is_dir():
        if extensions is None:
            extensions = [".txt", ".csv", ".json"]
        for path in Path(file_path).glob(f"*{extensions}"):
            for line in read_text_file(path, as_list=as_list):
                yield line
    else:
        try:
            if as_list:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        yield line
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return content
        except Exception as ex:
            logger.error(f"Ошибка при чтении файла {file_path}: {ex}")
            return None
```
#### Описание
Функция считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

#### Параметры:
- `file_path (str | Path)`: Путь к файлу или каталогу.
- `as_list (bool)`: Если `True`, возвращает генератор строк.
- `extensions (Optional[List[str]])`: Список расширений файлов для чтения из каталога.
- `chunk_size (int)`: Размер чанков для чтения файла в байтах.

#### Возвращает:
- `Generator[str, None, None] | str | None`: Генератор строк, объединенная строка или `None` в случае ошибки.

#### Исключения:
- `Exception`: Если возникает ошибка при чтении файла.

#### Пример:
```python
>>> from pathlib import Path
>>> file_path = Path('example.txt')
>>> content = read_text_file(file_path)
>>> if content:
...    print(f'File content: {content[:100]}...')
File content: Example text...
```
### Функция `csv2json_csv2dict`
```python
def csv2json_csv2dict(file_path: str | Path, encoding: str = 'utf-8') -> dict | None:
    """
    Преобразует CSV-файл в JSON-формат.

    Args:
        file_path (str | Path): Путь к CSV-файлу.
        encoding (str): Кодировка файла. По умолчанию `utf-8`.

    Returns:
        dict | None: Словарь с данными из CSV-файла или `None` в случае ошибки.

    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('data.csv')
        >>> data = csv2json_csv2dict(file_path)
        >>> if data:
        ...    print(data)
        {'column1': ['value1', 'value2'], 'column2': ['value3', 'value4']}
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
            return {k: [row[k] for row in data] for k in data[0]}
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return None
    except Exception as ex:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {ex}")
        return None
```
#### Описание
Функция преобразует CSV-файл в JSON-формат.

#### Параметры:
- `file_path (str | Path)`: Путь к CSV-файлу.
- `encoding (str)`: Кодировка файла. По умолчанию `utf-8`.

#### Возвращает:
- `dict | None`: Словарь с данными из CSV-файла или `None` в случае ошибки.

#### Исключения:
- `FileNotFoundError`: Если файл не найден.
- `Exception`: Если возникает ошибка при чтении файла.

#### Пример:
```python
>>> from pathlib import Path
>>> file_path = Path('data.csv')
>>> data = csv2json_csv2dict(file_path)
>>> if data:
...    print(data)
{'column1': ['value1', 'value2'], 'column2': ['value3', 'value4']}
```
### Функция `pprint`
```python
def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """
    Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. The data is printed with optional 
    text color, background color, and font style based on the specified parameters. The function can handle dictionaries, 
    lists, strings, and file paths.

    :param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.
    :param text_color: The color to apply to the text. Default is 'white'. See :ref:`TEXT_COLORS`.
    :param bg_color: The background color to apply to the text. Default is '' (no background color). See :ref:`BG_COLORS`.
    :param font_style: The font style to apply to the text. Default is '' (no font style). See :ref:`FONT_STYLES`.
    :return: None

    :raises: Exception if the data type is unsupported or an error occurs during printing.

    :example:
        >>> pprint({"name": "Alice", "age": 30}, text_color="green")
        \033[32m{
            "name": "Alice",
            "age": 30
        }\033[0m

        >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
        \033[34m\033[1mapple\033[0m
        \033[34m\033[1mbanana\033[0m
        \033[34m\033[1mcherry\033[0m

        >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
        \033[4m\033[33m\033[41mtext example\033[0m
    """
    if not print_data:
        return
    if isinstance(text_color, str):
        text_color = TEXT_COLORS.get(text_color.lower(), TEXT_COLORS["white"])
    if isinstance(bg_color, str):
        bg_color = BG_COLORS.get(bg_color.lower(), "")
    if isinstance(font_style, str):
        font_style = FONT_STYLES.get(font_style.lower(), "")


    try:
        if isinstance(print_data, dict):
            print(_color_text(json.dumps(print_data, indent=4), text_color))
        elif isinstance(print_data, list):
            for item in print_data:
                print(_color_text(str(item), text_color))
        elif isinstance(print_data, (str, Path)) and Path(print_data).is_file():
            ext = Path(print_data).suffix.lower()
            if ext in ['.csv', '.xls']:
                print(_color_text("File reading supported for .csv, .xls only.", text_color))
            else:
                print(_color_text("Unsupported file type.", text_color))
        else:
            print(_color_text(str(print_data), text_color))
    except Exception as ex:
        print(_color_text(f"Error: {ex}", text_color=TEXT_COLORS["red"]))
```
#### Описание
Функция `pprint` красиво печатает переданные данные с использованием ANSI escape кодов для цвета, фона и стиля текста.

#### Параметры:
- `print_data (Any)`: Данные для печати. Может быть `None`, `dict`, `list`, `str` или `Path`.
- `text_color (str)`: Цвет текста. По умолчанию 'white'. 
- `bg_color (str)`: Цвет фона текста. По умолчанию `''` (без цвета фона).
- `font_style (str)`: Стиль текста. По умолчанию `''` (без стиля текста).

#### Возвращает:
- `None`.

#### Исключения:
- `Exception`: Если тип данных не поддерживается или возникла ошибка во время печати.

#### Примеры:
```python
>>> pprint({"name": "Alice", "age": 30}, text_color="green")
\033[32m{
    "name": "Alice",
    "age": 30
}\033[0m

>>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
\033[34m\033[1mapple\033[0m
\033[34m\033[1mbanana\033[0m
\033[34m\033[1mcherry\033[0m

>>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
\033[4m\033[33m\033[41mtext example\033[0m
```
### Класс `OpenAIModel`
```python
class OpenAIModel(LLM):
    """
    Класс для работы с моделью OpenAI.

    Attributes:
        system_instruction (str): Системная инструкция для модели.
        model (str): Имя модели OpenAI.
        temperature (float): Температура модели.
        max_tokens (int): Максимальное количество токенов в ответе.
        top_p (float): Вероятность выбора токена.
        frequency_penalty (float): Штраф за частоту токена.
        presence_penalty (float): Штраф за наличие токена.

    Methods:
        ask(query: str, stream: bool = False) -> str | Generator[str, None, None]:
            Задает вопрос модели OpenAI.
        answer(query: str, stream: bool = False) -> str | Generator[str, None, None]:
            Задает вопрос модели OpenAI.
        generate_code(
            instruction: str,
            parameters: dict = None,
            code_type: str = None,
        ) -> str:
            Генерирует код на основе инструкции.
    """
    def ask(self, query: str, stream: bool = False) -> str | Generator[str, None, None]:
        """
        Задает вопрос модели OpenAI.

        Args:
            query (str): Вопрос.
            stream (bool): Флаг потоковой передачи. По умолчанию `False`.

        Returns:
            str | Generator[str, None, None]: Ответ модели или генератор.

        Example:
            >>> openai = OpenAIModel()
            >>> response = openai.ask('Как дела?')
            >>> print(response)
            Хорошо!
        """
        ...
    def answer(self, query: str, stream: bool = False) -> str | Generator[str, None, None]:
        """
        Задает вопрос модели OpenAI.

        Args:
            query (str): Вопрос.
            stream (bool): Флаг потоковой передачи. По умолчанию `False`.

        Returns:
            str | Generator[str, None, None]: Ответ модели или генератор.

        Example:
            >>> openai = OpenAIModel()
            >>> response = openai.answer('Как дела?')
            >>> print(response)
            Хорошо!
        """
        ...
    def generate_code(
        self,
        instruction: str,
        parameters: dict = None,
        code_type: str = None,
    ) -> str:
        """
        Генерирует код на основе инструкции.

        Args:
            instruction (str): Инструкция для генерации кода.
            parameters (dict): Параметры для генерации кода.
            code_type (str): Тип генерируемого кода.

        Returns:
            str: Сгенерированный код.

        Example:
            >>> openai = OpenAIModel()
            >>> code = openai.generate_code('Создать функцию, которая выводит "Hello, world!"')
            >>> print(code)
            def hello_world():
                print("Hello, world!")
        """
        ...
```
#### Описание
Класс `OpenAIModel` предоставляет интерфейс для взаимодействия с моделью OpenAI.

#### Атрибуты:
- `system_instruction (str)`: Системная инструкция для модели.
- `model (str)`: Имя модели OpenAI.
- `temperature (float)`: Температура модели.
- `max_tokens (int)`: Максимальное количество токенов в ответе.
- `top_p (float)`: Вероятность выбора токена.
- `frequency_penalty (float)`: Штраф за частоту токена.
- `presence_penalty (float)`: Штраф за наличие токена.

#### Методы:
- `ask(query: str, stream: bool = False) -> str | Generator[str, None, None]`: Задает вопрос модели OpenAI.
- `answer(query: str, stream: bool = False) -> str | Generator[str, None, None]`: Задает вопрос модели OpenAI.
- `generate_code(instruction: str, parameters: dict = None, code_type: str = None) -> str`: Генерирует код на основе инструкции.

#### Примеры:
```python
>>> openai = OpenAIModel()
>>> response = openai.ask('Как дела?')
>>> print(response)
Хорошо!
```
### Класс `GoogleGenerativeAi`
```python
class GoogleGenerativeAi(LLM):
    """
    Класс для работы с моделью Google Generative AI.

    Attributes:
        system_instruction (str): Системная инструкция для модели.
        model (str): Имя модели Google Generative AI.

    Methods:
        ask(query: str, stream: bool = False) -> str | Generator[str, None, None]:
            Задает вопрос модели Google Generative AI.
        answer(query: str, stream: bool = False) -> str | Generator[str, None, None]:
            Задает вопрос модели Google Generative AI.
        generate_code(
            instruction: str,
            parameters: dict = None,
            code_type: str = None,
        ) -> str:
            Генерирует код на основе инструкции.
    """
    def ask(self, query: str, stream: bool = False) -> str | Generator[str, None, None]:
        """
        Задает вопрос модели Google Generative AI.

        Args:
            query (str): Вопрос.
            stream (bool): Флаг потоковой передачи. По умолчанию `False`.

        Returns:
            str | Generator[str, None, None]: Ответ модели или генератор.

        Example:
            >>> gemini = GoogleGenerativeAi()
            >>> response = gemini.ask('Как дела?')
            >>> print(response)
            Хорошо!
        """
        ...
    def answer(self, query: str, stream: bool = False) -> str | Generator[str, None, None]:
        """
        Задает вопрос модели Google Generative AI.

        Args:
            query (str): Вопрос.
            stream (bool): Флаг потоковой передачи. По умолчанию `False`.

        Returns:
            str | Generator[str, None, None]: Ответ модели или генератор.

        Example:
            >>> gemini = GoogleGenerativeAi()
            >>> response = gemini.answer('Как дела?')
            >>> print(response)
            Хорошо!
        """
        ...
    def generate_code(
        self,
        instruction: str,
        parameters: dict = None,
        code_type: str = None,
    ) -> str:
        """
        Генерирует код на основе инструкции.

        Args:
            instruction (str): Инструкция для генерации кода.
            parameters (dict): Параметры для генерации кода.
            code_type (str): Тип генерируемого кода.

        Returns:
            str: Сгенерированный код.

        Example:
            >>> gemini = GoogleGenerativeAi()
            >>> code = gemini.generate_code('Создать функцию, которая выводит "Hello, world!"')
            >>> print(code)
            def hello_world():
                print("Hello, world!")
        """
        ...
```
#### Описание
Класс `GoogleGenerativeAi` предоставляет интерфейс для взаимодействия с моделью Google Generative AI.

#### Атрибуты:
- `system_instruction (str)`: Системная инструкция для модели.
- `model (str)`: Имя модели Google Generative AI.

#### Методы:
- `ask(query: str, stream: bool = False) -> str | Generator[str, None, None]`: Задает вопрос модели Google Generative AI.
- `answer(query: str, stream: bool = False) -> str | Generator[str, None, None]`: Задает вопрос модели Google Generative AI.
- `generate_code(instruction: str, parameters: dict = None, code_type: str = None) -> str`: Генерирует код на основе инструкции.

#### Примеры:
```python
>>> gemini = GoogleGenerativeAi()
>>> response = gemini.ask('Как дела?')
>>> print(response)
Хорошо!