# Модуль `utils.py`

## Обзор

Модуль содержит различные утилиты и вспомогательные функции, используемые в проекте `tinytroupe`. Он предоставляет инструменты для работы с LLM, обработки текста, управления конфигурацией, логирования, сериализации и десериализации JSON, а также другие полезные функции.

## Подробнее

Этот модуль предоставляет набор инструментов для различных аспектов работы проекта `tinytroupe`. Он включает в себя функции для составления сообщений для LLM, извлечения JSON из текста, обработки ошибок, валидации данных, управления конфигурацией, логирования, сериализации и десериализации JSON, а также другие утилиты.

## Функции

### `compose_initial_LLM_messages_with_templates`

```python
def compose_initial_LLM_messages_with_templates(system_template_name: str, user_template_name: str = None, rendering_configs: dict = {}) -> list:
    """
    Функция составляет начальные сообщения для вызова LLM-модели, предполагая, что всегда используется системное сообщение
    (общее описание задачи) и опциональное сообщение пользователя (конкретное описание задачи).
    Эти сообщения составляются с использованием указанных шаблонов и конфигураций рендеринга.

    Args:
        system_template_name (str): Имя файла шаблона для системного сообщения.
        user_template_name (str, optional): Имя файла шаблона для сообщения пользователя. По умолчанию `None`.
        rendering_configs (dict, optional): Словарь с конфигурациями для рендеринга шаблонов. По умолчанию `{}`.

    Returns:
        list: Список сообщений, готовых для отправки в LLM-модель.

    
    - Функция принимает имена файлов шаблонов для системного и пользовательского сообщений, а также словарь с конфигурациями рендеринга.
    - Формирует путь к файлам шаблонов, объединяя имя файла с путем к директории `prompts`.
    - Добавляет системное сообщение в список сообщений, выполняя рендеринг шаблона с использованием библиотеки `chevron` и переданных конфигураций.
    - Если указано имя файла шаблона для пользовательского сообщения, добавляет и его в список сообщений, также выполняя рендеринг.
    - Возвращает список сообщений, готовых для отправки в LLM-модель.

    Примеры:
        >>> messages = compose_initial_LLM_messages_with_templates('system.md', 'user.md', {'name': 'Example'})
        >>> print(messages)
        [{'role': 'system', 'content': 'System message content'}, {'role': 'user', 'content': 'User message content'}]
    """
```

### `extract_json`

```python
def extract_json(text: str) -> dict:
    """
    Функция извлекает JSON-объект из строки, игнорируя любой текст до первой открывающей фигурной скобки
    и любые теги Markdown (```json) или (```).

    Args:
        text (str): Строка, из которой нужно извлечь JSON.

    Returns:
        dict: Извлеченный JSON-объект в виде словаря. Если извлечение не удалось, возвращается пустой словарь.

    
    - Функция принимает строку `text` в качестве входных данных.
    - Использует регулярные выражения для удаления любого текста до первой открывающей фигурной или квадратной скобки.
    - Удаляет любой текст после последней закрывающей фигурной или квадратной скобки.
    - Заменяет недопустимые escape-последовательности, такие как `\\\'`, на одинарные кавычки (`'`).
    - Пытается распарсить оставшуюся строку как JSON-объект с помощью `json.loads()`.
    - В случае успеха возвращает распарсенный JSON-объект в виде словаря.
    - Если во время парсинга возникает исключение, возвращает пустой словарь.

    Примеры:
        >>> extract_json('{"name": "Example", "value": 123}')
        {'name': 'Example', 'value': 123}

        >>> extract_json('Some text {"name": "Example", "value": 123} More text')
        {'name': 'Example', 'value': 123}

        >>> extract_json('Invalid JSON')
        {}
    """
```

### `extract_code_block`

```python
def extract_code_block(text: str) -> str:
    """
    Функция извлекает блок кода из строки, игнорируя любой текст до первых открывающих тройных обратных кавычек
    и любой текст после закрывающих тройных обратных кавычек.

    Args:
        text (str): Строка, из которой нужно извлечь блок кода.

    Returns:
        str: Извлеченный блок кода. Если извлечение не удалось, возвращается пустая строка.

    
    - Функция принимает строку `text` в качестве входных данных.
    - Использует регулярные выражения для удаления любого текста до первых открывающих тройных обратных кавычек (```).
    - Удаляет любой текст после последних закрывающих тройных обратных кавычек (```).
    - Возвращает извлеченный блок кода.
    - Если во время извлечения возникает исключение, возвращает пустую строку.

    Примеры:
        >>> extract_code_block('```python\nprint("Hello")\n```')
        '```python\nprint("Hello")\n```'

        >>> extract_code_block('Some text ```python\nprint("Hello")\n``` More text')
        '```python\nprint("Hello")\n```'

        >>> extract_code_block('No code block')
        ''
    """
```

### `repeat_on_error`

```python
def repeat_on_error(retries: int, exceptions: list):
    """
    Декоратор, который повторяет вызов указанной функции, если происходит исключение из указанного списка,
    до указанного количества повторных попыток. Если это количество попыток превышено, исключение поднимается.
    Если исключение не происходит, функция возвращается нормально.

    Args:
        retries (int): Количество повторных попыток.
        exceptions (list): Список классов исключений для перехвата.
    """
```

### `check_valid_fields`

```python
def check_valid_fields(obj: dict, valid_fields: list) -> None:
    """
    Функция проверяет, являются ли поля в указанном словаре допустимыми, в соответствии со списком допустимых полей.
    Если нет, вызывает исключение ValueError.

    Args:
        obj (dict): Словарь для проверки.
        valid_fields (list): Список допустимых полей.

    Raises:
        ValueError: Если в словаре есть недопустимые поля.

    
    - Функция принимает словарь `obj` и список допустимых полей `valid_fields` в качестве входных данных.
    - Перебирает все ключи в словаре `obj`.
    - Для каждого ключа проверяет, присутствует ли он в списке `valid_fields`.
    - Если ключ отсутствует в списке `valid_fields`, функция вызывает исключение `ValueError` с сообщением об ошибке, указывающим недопустимый ключ и список допустимых ключей.
    - Если все ключи в словаре `obj` присутствуют в списке `valid_fields`, функция завершается без ошибок.

    Примеры:
        >>> check_valid_fields({'name': 'Example', 'value': 123}, ['name', 'value'])  # No error
        >>> check_valid_fields({'name': 'Example', 'invalid': 123}, ['name', 'value'])
        ValueError: Invalid key invalid in dictionary. Valid keys are: ['name', 'value']
    """
```

### `sanitize_raw_string`

```python
def sanitize_raw_string(value: str) -> str:
    """
    Функция очищает указанную строку путем:
      - удаления любых недопустимых символов.
      - обеспечения того, чтобы она не была длиннее максимальной длины строки Python.

    Это делается из соображений предосторожности для обеспечения безопасности, чтобы избежать любых потенциальных проблем со строкой.

    Args:
        value (str): Строка для очистки.

    Returns:
        str: Очищенная строка.

    
    - Функция принимает строку `value` в качестве входных данных.
    - Удаляет любые недопустимые символы, кодируя строку в UTF-8 с игнорированием ошибок и декодируя обратно в UTF-8.
    - Убеждается, что строка не длиннее максимальной длины строки Python, обрезая ее до `sys.maxsize`.
    - Возвращает очищенную строку.

    Примеры:
        >>> sanitize_raw_string('Example with invalid chars \ud800')
        'Example with invalid chars '

        >>> sanitize_raw_string('Long string' * 100000)  # длинная строка
        'Long stringLong string...'  # обрезанная строка
    """
```

### `sanitize_dict`

```python
def sanitize_dict(value: dict) -> dict:
    """
    Функция очищает указанный словарь путем:
      - удаления любых недопустимых символов.
      - обеспечения того, чтобы словарь не был слишком глубоко вложенным.

    Args:
        value (dict): Словарь для очистки.

    Returns:
        dict: Очищенный словарь.

    
    - Функция принимает словарь `value` в качестве входных данных.
    - Сначала преобразует словарь в строку JSON с помощью `json.dumps()`, чтобы можно было применить очистку строки.
    - Вызывает `sanitize_raw_string()` для очистки строкового представления словаря.
    - Затем преобразует очищенную строку обратно в словарь с помощью `json.loads()`.
    - Возвращает очищенный словарь.

    Примеры:
        >>> sanitize_dict({'name': 'Example', 'value': 'Invalid chars \ud800'})
        {'name': 'Example', 'value': 'Invalid chars '}
    """
```

### `add_rai_template_variables_if_enabled`

```python
def add_rai_template_variables_if_enabled(template_variables: dict) -> dict:
    """
    Функция добавляет переменные шаблона RAI в указанный словарь, если включены отказы от ответственности RAI.
    Они могут быть настроены в файле config.ini. Если они включены, переменные будут загружать отказы от ответственности RAI из
    соответствующих файлов в каталоге prompts. В противном случае переменные будут установлены в None.

    Args:
        template_variables (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

    Returns:
        dict: Обновленный словарь переменных шаблона.

    
    - Функция принимает словарь `template_variables` в качестве входных данных.
    - Импортирует модуль `config` из `tinytroupe`, чтобы получить доступ к настройкам конфигурации.
    - Читает значения `RAI_HARMFUL_CONTENT_PREVENTION` и `RAI_COPYRIGHT_INFRINGEMENT_PREVENTION` из секции `[Simulation]` файла `config.ini`.
    - Открывает файлы `rai_harmful_content_prevention.md` и `rai_copyright_infringement_prevention.md` из каталога `prompts`.
    - Если `rai_harmful_content_prevention` включен, читает содержимое файла и добавляет его в словарь `template_variables` под ключом `'rai_harmful_content_prevention'`. В противном случае устанавливает значение в `None`.
    - Если `rai_copyright_infringement_prevention` включен, читает содержимое файла и добавляет его в словарь `template_variables` под ключом `'rai_copyright_infringement_prevention'`. В противном случае устанавливает значение в `None`.
    - Возвращает обновленный словарь `template_variables`.

    Примеры:
        >>> template_vars = {}
        >>> updated_vars = add_rai_template_variables_if_enabled(template_vars)
        >>> print(updated_vars.keys())
        dict_keys(['rai_harmful_content_prevention', 'rai_copyright_infringement_prevention'])
    """
```

### `inject_html_css_style_prefix`

```python
def inject_html_css_style_prefix(html: str, style_prefix_attributes: str) -> str:
    """
    Вставляет префикс стиля во все атрибуты стиля в данной HTML-строке.

    Например, если вы хотите добавить префикс стиля ко всем атрибутам стиля в HTML-строке
    ``<div style="color: red;">Hello</div>``, вы можете использовать эту функцию следующим образом:
    inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')

    Args:
        html (str): HTML-строка для изменения.
        style_prefix_attributes (str): Префикс стиля для вставки.

    Returns:
        str: HTML-строка с добавленным префиксом стиля.

    
    - Функция принимает HTML-строку `html` и строку с префиксом стиля `style_prefix_attributes` в качестве входных данных.
    - Использует метод `replace()` для замены всех вхождений `style="` на `style="{style_prefix_attributes};`.
    - Возвращает измененную HTML-строку.

    Примеры:
        >>> inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')
        '<div style="font-size: 20px;;color: red;">Hello</div>'
    """
```

### `break_text_at_length`

```python
def break_text_at_length(text: Union[str, dict], max_length: int = None) -> str:
    """
    Разбивает текст (или JSON) на указанной длине, вставляя строку "(...)" в точке разрыва.
    Если максимальная длина равна None, содержимое возвращается как есть.

    Args:
        text (Union[str, dict]): Текст или JSON для разбивки.
        max_length (int, optional): Максимальная длина текста. По умолчанию `None`.

    Returns:
        str: Разбитый текст или JSON.

    
    - Функция принимает текст (или JSON) `text` и максимальную длину `max_length` в качестве входных данных.
    - Если `text` является словарем, преобразует его в строку JSON с отступами с помощью `json.dumps()`.
    - Если `max_length` равен `None` или длина `text` не превышает `max_length`, возвращает `text` без изменений.
    - В противном случае обрезает `text` до `max_length` и добавляет строку "(...)" в конце.
    - Возвращает обрезанный текст.

    Примеры:
        >>> break_text_at_length('Long text', 5)
        'Long ...'

        >>> break_text_at_length({'name': 'Example'}, 10)
        '{\n    "name" (...)'
    """
```

### `pretty_datetime`

```python
def pretty_datetime(dt: datetime) -> str:
    """
    Возвращает красивое строковое представление указанного объекта datetime.

    Args:
        dt (datetime): Объект datetime для форматирования.

    Returns:
        str: Отформатированная строка datetime.

    
    - Функция принимает объект `datetime` в качестве входных данных.
    - Использует метод `strftime()` для форматирования объекта `datetime` в строку в формате "%Y-%m-%d %H:%M".
    - Возвращает отформатированную строку.

    Примеры:
        >>> import datetime
        >>> now = datetime.datetime.now()
        >>> pretty_datetime(now)
        '2024-01-01 12:00'  # Пример вывода
    """
```

### `dedent`

```python
def dedent(text: str) -> str:
    """
    Удаляет отступы из указанного текста, удаляя все начальные пробелы и отступы.

    Args:
        text (str): Текст для удаления отступов.

    Returns:
        str: Текст без отступов.

    
    - Функция принимает строку `text` в качестве входных данных.
    - Использует функцию `textwrap.dedent()` для удаления общего начального пробела из каждой строки в `text`.
    - Использует метод `strip()` для удаления любых начальных и конечных пробелов из результата.
    - Возвращает текст без отступов.

    Примеры:
        >>> dedent('  Hello\n  World')
        'Hello\nWorld'
    """
```

### `read_config_file`

```python
def read_config_file(use_cache: bool = True, verbose: bool = True) -> configparser.ConfigParser:
    """
    Функция читает файл конфигурации и возвращает объект `configparser.ConfigParser`.

    Args:
        use_cache (bool, optional): Если `True`, использует кэшированную конфигурацию, если она доступна. По умолчанию `True`.
        verbose (bool, optional): Если `True`, выводит сообщения о поиске файлов конфигурации. По умолчанию `True`.

    Returns:
        configparser.ConfigParser: Объект `configparser.ConfigParser`, содержащий конфигурацию.

    Raises:
        ValueError: Если не удается найти файл конфигурации по умолчанию.

    
    - Функция принимает два аргумента: `use_cache` и `verbose`.
    - Проверяет, включено ли использование кэша и доступна ли кэшированная конфигурация (`_config`). Если да, возвращает кэшированную конфигурацию.
    - Если использование кэша отключено или кэшированная конфигурация недоступна, создает новый объект `configparser.ConfigParser`.
    - Определяет путь к файлу конфигурации по умолчанию (`config.ini`) в каталоге модуля.
    - Если файл конфигурации по умолчанию существует, читает его и сохраняет в `_config`.
    - Если файл конфигурации по умолчанию не существует, вызывает исключение `ValueError`.
    - Определяет путь к пользовательскому файлу конфигурации (`config.ini`) в текущем рабочем каталоге.
    - Если пользовательский файл конфигурации существует, читает его и перезаписывает значения в `config`.
    - Если пользовательский файл конфигурации не существует, выводит сообщение об этом.
    - Возвращает объект `configparser.ConfigParser`.

    Примеры:
        >>> config = read_config_file()
        >>> print(config.get('Section', 'Key'))
        Value
    """
```

### `pretty_print_config`

```python
def pretty_print_config(config: configparser.ConfigParser) -> None:
    """
    Функция выводит конфигурацию в удобочитаемом формате.

    Args:
        config (configparser.ConfigParser): Объект `configparser.ConfigParser` для вывода.

    Returns:
        None

    
    - Функция принимает объект `configparser.ConfigParser` в качестве входных данных.
    - Выводит заголовок "Current TinyTroupe configuration".
    - Перебирает все секции в конфигурации.
    - Для каждой секции выводит ее имя.
    - Перебирает все элементы в секции и выводит их в формате "key = value".

    Примеры:
        >>> import configparser
        >>> config = configparser.ConfigParser()
        >>> config['Section'] = {'Key': 'Value'}
        >>> pretty_print_config(config)
        =================================
        Current TinyTroupe configuration
        =================================
        [Section]
        key = Value
    """
```

### `start_logger`

```python
def start_logger(config: configparser.ConfigParser) -> None:
    """
    Функция запускает логгер с указанной конфигурацией.

    Args:
        config (configparser.ConfigParser): Объект `configparser.ConfigParser`, содержащий конфигурацию логгера.

    Returns:
        None

    
    - Функция принимает объект `configparser.ConfigParser` в качестве входных данных.
    - Создает логгер с именем "tinytroupe".
    - Получает уровень логирования из конфигурации (по умолчанию "INFO").
    - Устанавливает уровень логирования для логгера.
    - Создает обработчик консоли.
    - Устанавливает уровень логирования для обработчика консоли.
    - Создает форматтер.
    - Добавляет форматтер в обработчик консоли.
    - Добавляет обработчик консоли в логгер.

    Примеры:
        >>> import configparser
        >>> config = configparser.ConfigParser()
        >>> config['Logging'] = {'LOGLEVEL': 'DEBUG'}
        >>> start_logger(config)
        # Логгер запущен с уровнем DEBUG
    """
```

## Классы

### `JsonSerializableRegistry`

```python
class JsonSerializableRegistry:
    """
    Mixin-класс, который предоставляет сериализацию JSON, десериализацию и регистрацию подклассов.

    Attributes:
        class_mapping (dict): Словарь, содержащий соответствие между именами классов и классами.

    Methods:
        to_json(include: list = None, suppress: list = None, file_path: str = None) -> dict: Возвращает JSON-представление объекта.
        from_json(json_dict_or_path: Union[dict, str], suppress: list = None, post_init_params: dict = None): Загружает JSON-представление объекта и создает экземпляр класса.
        __init_subclass__(cls, **kwargs): Регистрирует подкласс при создании.
        _post_deserialization_init(self, **kwargs): Метод, вызываемый после десериализации.

    Принцип работы:
    - Класс `JsonSerializableRegistry` предназначен для упрощения процесса сериализации и десериализации объектов в JSON-формат.
    - Он использует словарь `class_mapping` для хранения соответствия между именами классов и самими классами, что позволяет создавать экземпляры классов из JSON-представления.
    - Методы `to_json()` и `from_json()` обеспечивают сериализацию и десериализацию объектов соответственно.
    - Метод `__init_subclass__()` автоматически регистрирует подклассы при их создании, добавляя их в словарь `class_mapping`.
    - Метод `_post_deserialization_init()` вызывается после десериализации объекта и может быть использован для выполнения дополнительной инициализации.

    """
```

#### `to_json`

```python
    def to_json(self, include: list = None, suppress: list = None, file_path: str = None) -> dict:
        """
        Возвращает JSON представление объекта.

        Args:
            include (list, optional): Атрибуты для включения в сериализацию.
            suppress (list, optional): Атрибуты для исключения из сериализации.
            file_path (str, optional): Путь к файлу, в который будет записан JSON.

        Returns:
            dict: JSON представление объекта.

        
        - Функция принимает три аргумента: `include`, `suppress` и `file_path`.
        - Собирает все сериализуемые атрибуты из иерархии классов.
        - Переопределяет атрибуты с помощью параметров метода, если они предоставлены.
        - Создает словарь `result`, содержащий имя класса и значения атрибутов.
        - Если указан `file_path`, записывает JSON в файл.
        - Возвращает словарь `result`.
        """
```

#### `from_json`

```python
    @classmethod
    def from_json(cls, json_dict_or_path: Union[dict, str], suppress: list = None, post_init_params: dict = None):
        """
        Загружает JSON представление объекта и создает экземпляр класса.

        Args:
            json_dict_or_path (Union[dict, str]): JSON словарь, представляющий объект, или путь к файлу, содержащему JSON.
            suppress (list, optional): Атрибуты для исключения из загрузки.
            post_init_params (dict, optional): Параметры для передачи в метод `_post_deserialization_init`.

        Returns:
            An instance of the class populated with the data from json_dict_or_path.

        
        - Функция принимает три аргумента: `json_dict_or_path`, `suppress` и `post_init_params`.
        - Загружает JSON из файла или словаря.
        - Определяет класс для создания экземпляра.
        - Создает экземпляр класса без вызова `__init__`.
        - Собирает все сериализуемые атрибуты из иерархии классов.
        - Назначает значения атрибутам экземпляра из JSON.
        - Вызывает метод `_post_deserialization_init`, если он существует.
        - Возвращает экземпляр класса.
        """
```

#### `__init_subclass__`

```python
    def __init_subclass__(cls, **kwargs):
        """
        Регистрирует подкласс при создании.
        """
```

#### `_post_deserialization_init`

```python
    def _post_deserialization_init(self, **kwargs):
        """
        Метод, вызываемый после десериализации.
        """
```

### `post_init`

```python
def post_init(cls):
    """
    Декоратор для принудительного вызова метода post-initialization в классе, если он есть.
    Метод должен быть назван `_post_init`.
    """
```

## Другие функции

### `name_or_empty`

```python
def name_or_empty(named_entity: AgentOrWorld):
    """
    Возвращает имя указанного агента или среды, или пустую строку, если агент равен None.
    """
```

### `custom_hash`

```python
def custom_hash(obj):
    """
    Возвращает хэш для указанного объекта. Объект сначала преобразуется
    в строку, чтобы сделать его хэшируемым. Этот метод является детерминированным,
    в отличие от встроенной функции hash().
    """
```

### `fresh_id`

```python
def fresh_id():
    """
    Возвращает свежий идентификатор для нового объекта. Это полезно для создания уникальных идентификаторов для объектов.
    """