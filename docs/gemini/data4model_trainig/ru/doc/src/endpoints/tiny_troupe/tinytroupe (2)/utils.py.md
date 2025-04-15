# Модуль `utils`

## Обзор

Модуль содержит различные утилиты и вспомогательные функции, используемые в проекте `tinytroupe`. Он включает в себя функции для работы с текстовыми шаблонами, извлечения данных из текста (например, JSON), обработки ошибок, валидации данных, prompt engineering, рендеринга и разметки, а также утилиты для ввода-вывода и запуска.

## Подробней

Этот модуль предоставляет набор инструментов для упрощения различных задач, таких как:
- Композиция сообщений для языковых моделей с использованием шаблонов.
- Извлечение JSON-объектов и кодовых блоков из текста.
- Повторный вызов функций при возникновении ошибок.
- Валидация входных данных.
- Санитизация строк и словарей.
- Добавление переменных шаблона для RAI (Responsible AI).
- Внедрение стилей CSS в HTML.
- Разбивка текста на части заданной длины.
- Форматирование даты и времени.
- Чтение конфигурационных файлов.
- Настройка логирования.
- Сериализация и десериализация объектов в JSON.
- Генерация уникальных идентификаторов.

## Функции

### `compose_initial_LLM_messages_with_templates`

```python
def compose_initial_LLM_messages_with_templates(system_template_name: str, user_template_name: str = None, rendering_configs: dict = {}) -> list:
    """
    Составляет начальные сообщения для вызова LLM-модели, предполагая, что всегда есть
    системное (общее описание задачи) и необязательное пользовательское сообщение (специфическое описание задачи).
    Эти сообщения составляются с использованием указанных шаблонов и конфигураций рендеринга.

    Args:
        system_template_name (str): Имя файла шаблона системного сообщения.
        user_template_name (str, optional): Имя файла шаблона пользовательского сообщения. По умолчанию `None`.
        rendering_configs (dict, optional): Словарь с конфигурациями для рендеринга шаблонов. По умолчанию `{}`.

    Returns:
        list: Список составленных сообщений для LLM-модели.

    Пример:
        >>> messages = compose_initial_LLM_messages_with_templates('system_prompt.md', 'user_prompt.md', {'task': 'summarize'})
        >>> print(messages)
        [{'role': 'system', 'content': '...'}, {'role': 'user', 'content': '...'}]
    """
    ...
```

### `extract_json`

```python
def extract_json(text: str) -> dict:
    """
    Извлекает JSON-объект из строки, игнорируя: любой текст перед первой
    открывающей фигурной скобкой; и любые открывающие (```json) или закрывающие (```) теги Markdown.

    Args:
        text (str): Строка, из которой нужно извлечь JSON.

    Returns:
        dict: Извлеченный JSON-объект в виде словаря. Если извлечение не удалось, возвращает пустой словарь `{}`.

    Пример:
        >>> extract_json('Some text { "key": "value" }')
        {'key': 'value'}
        >>> extract_json('```json { "key": "value" } ```')
        {'key': 'value'}
    """
    ...
```

### `extract_code_block`

```python
def extract_code_block(text: str) -> str:
    """
    Извлекает кодовый блок из строки, игнорируя любой текст перед первым
    открывающим тройным обратным апострофом и любой текст после закрывающего тройного обратного апострофа.

    Args:
        text (str): Строка, из которой нужно извлечь кодовый блок.

    Returns:
        str: Извлеченный кодовый блок. Если извлечение не удалось, возвращает пустую строку `""`.

    Пример:
        >>> extract_code_block('Some text ```python print("Hello") ```')
        '```python print("Hello") ```'
    """
    ...
```

### `repeat_on_error`

```python
def repeat_on_error(retries: int, exceptions: list):
    """
    Декоратор, который повторяет вызов указанной функции, если возникает исключение из указанного списка,
    до указанного количества попыток. Если количество попыток превышено, исключение выбрасывается.
    Если исключение не возникает, функция возвращается нормально.

    Args:
        retries (int): Количество попыток повтора.
        exceptions (list): Список классов исключений, которые нужно перехватывать.

    Пример:
        >>> @repeat_on_error(retries=3, exceptions=[ValueError])
        ... def my_func():
        ...     raise ValueError('Some error')
        ...
        >>> my_func()  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        ValueError: Some error
    """
    ...
```

### `check_valid_fields`

```python
def check_valid_fields(obj: dict, valid_fields: list) -> None:
    """
    Проверяет, являются ли поля в указанном словаре допустимыми, согласно списку допустимых полей.
    Если нет, вызывает ValueError.

    Args:
        obj (dict): Проверяемый словарь.
        valid_fields (list): Список допустимых полей.

    Raises:
        ValueError: Если в словаре есть недопустимое поле.

    Пример:
        >>> check_valid_fields({'a': 1, 'b': 2}, ['a', 'b'])
        >>> check_valid_fields({'a': 1, 'c': 2}, ['a', 'b'])  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        ValueError: Invalid key c in dictionary. Valid keys are: ['a', 'b']
    """
    ...
```

### `sanitize_raw_string`

```python
def sanitize_raw_string(value: str) -> str:
    """
    Очищает указанную строку путем:
      - удаления любых недопустимых символов.
      - проверки, что она не длиннее максимальной длины строки Python.

    Это делается для предосторожности в целях безопасности, чтобы избежать любых потенциальных проблем со строкой.

    Args:
        value (str): Очищаемая строка.

    Returns:
        str: Очищенная строка.

    Пример:
        >>> sanitize_raw_string('Invalid char \\x00')
        'Invalid char '
    """
    ...
```

### `sanitize_dict`

```python
def sanitize_dict(value: dict) -> dict:
    """
    Очищает указанный словарь путем:
      - удаления любых недопустимых символов.
      - проверки, что словарь не слишком глубоко вложен.

    Args:
        value (dict): Очищаемый словарь.

    Returns:
        dict: Очищенный словарь.

    Пример:
        >>> sanitize_dict({'a': 'Invalid char \\x00'})
        {'a': 'Invalid char '}
    """
    ...
```

### `add_rai_template_variables_if_enabled`

```python
def add_rai_template_variables_if_enabled(template_variables: dict) -> dict:
    """
    Добавляет переменные шаблона RAI (Responsible AI) в указанный словарь, если включены соответствующие параметры.
    Эти параметры можно настроить в файле config.ini. Если они включены, переменные загрузят дисклеймеры RAI из
    соответствующих файлов в каталоге prompts. В противном случае переменные будут установлены в None.

    Args:
        template_variables (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

    Returns:
        dict: Обновленный словарь переменных шаблона.

    Пример:
        >>> template_variables = {}
        >>> updated_variables = add_rai_template_variables_if_enabled(template_variables)
        >>> print(updated_variables)
        {'rai_harmful_content_prevention': None, 'rai_copyright_infringement_prevention': None}
    """
    ...
```

### `inject_html_css_style_prefix`

```python
def inject_html_css_style_prefix(html, style_prefix_attributes):
    """
    Вставляет префикс стиля во все атрибуты style в данной HTML-строке.

    Например, если вы хотите добавить префикс стиля ко всем атрибутам style в HTML-строке
    ``<div style="color: red;">Hello</div>``, вы можете использовать эту функцию следующим образом:
    inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')
    """
    ...
```

### `break_text_at_length`

```python
def break_text_at_length(text: Union[str, dict], max_length: int = None) -> str:
    """
    Разбивает текст (или JSON) на части указанной длины, вставляя строку "(...)" в точке разрыва.
    Если максимальная длина равна `None`, содержимое возвращается как есть.

    Args:
        text (Union[str, dict]): Текст или JSON для разбивки.
        max_length (int, optional): Максимальная длина текста. По умолчанию `None`.

    Returns:
        str: Разбитый текст.

    Пример:
        >>> break_text_at_length('Some long text', max_length=5)
        'Some  (...)'
        >>> break_text_at_length({'key': 'value'}, max_length=10)
        '{\n    "key":  (...)'
    """
    ...
```

### `pretty_datetime`

```python
def pretty_datetime(dt: datetime) -> str:
    """
    Возвращает строковое представление объекта datetime в формате "год-месяц-день час:минута".

    Args:
        dt (datetime): Объект datetime для форматирования.

    Returns:
        str: Строковое представление даты и времени.

    Пример:
        >>> import datetime
        >>> dt = datetime.datetime(2023, 1, 1, 12, 30)
        >>> pretty_datetime(dt)
        '2023-01-01 12:30'
    """
    ...
```

### `dedent`

```python
def dedent(text: str) -> str:
    """
    Удаляет отступы из указанного текста, удаляя любые начальные пробелы и отступы.

    Args:
        text (str): Текст для удаления отступов.

    Returns:
        str: Текст без отступов.

    Пример:
        >>> text = '  \\n    Some text\\n  '
        >>> dedent(text)
        'Some text'
    """
    ...
```

### `read_config_file`

```python
def read_config_file(use_cache: bool = True, verbose: bool = True) -> configparser.ConfigParser:
    """
    Читает конфигурационный файл config.ini.

    Args:
        use_cache (bool, optional): Использовать ли кэшированную конфигурацию, если она существует. По умолчанию `True`.
        verbose (bool, optional): Выводить ли отладочную информацию в консоль. По умолчанию `True`.

    Returns:
        configparser.ConfigParser: Объект конфигурации.

    Raises:
        ValueError: Если не удается найти файл конфигурации.

    Как работает функция:
    - Сначала проверяется, если кэшированная конфигурация существует и разрешено ее использование. В этом случае она возвращается.
    - Если кэшированной конфигурации нет или ее использование не разрешено, создается новый объект `ConfigParser`.
    - Считываются значения по умолчанию из `config.ini`, расположенного в каталоге модуля.
    - Если существует пользовательский файл `config.ini` в текущем рабочем каталоге, его значения перезаписывают значения по умолчанию.
    - Возвращается объект конфигурации.

    Примеры:
        >>> config = read_config_file()
        >>> type(config)
        <class 'configparser.ConfigParser'>
    """
    ...
```

### `pretty_print_config`

```python
def pretty_print_config(config):
    """
    Выводит в консоль текущую конфигурацию TinyTroupe в удобном для чтения формате.

    Args:
        config: Объект конфигурации, полученный с помощью configparser.ConfigParser.

    Как работает функция:
    - Функция итерирует по всем секциям в объекте конфигурации.
    - Для каждой секции она выводит название секции в квадратных скобках.
    - Затем она итерирует по всем ключам и значениям в каждой секции и выводит их в формате "ключ = значение".
    - Между секциями добавляется пустая строка для улучшения читаемости.

    Примеры:
        >>> import configparser
        >>> config = configparser.ConfigParser()
        >>> config['Section1'] = {'key1': 'value1', 'key2': 'value2'}
        >>> config['Section2'] = {'key3': 'value3', 'key4': 'value4'}
        >>> pretty_print_config(config)
        <BLANKLINE>
        =================================
        Current TinyTroupe configuration 
        =================================
        [Section1]
        key1 = value1
        key2 = value2
        <BLANKLINE>
        [Section2]
        key3 = value3
        key4 = value4
        <BLANKLINE>
    """
    ...
```

### `start_logger`

```python
def start_logger(config: configparser.ConfigParser):
    """
    Настраивает и запускает логгер для приложения TinyTroupe.

    Args:
        config (configparser.ConfigParser): Объект конфигурации, содержащий параметры логирования.

    Как работает функция:
    - Получает уровень логирования из конфигурации (по умолчанию INFO).
    - Создает логгер с именем "tinytroupe".
    - Устанавливает уровень логирования для логгера.
    - Создает обработчик консоли (StreamHandler) и устанавливает для него уровень логирования.
    - Создает форматтер, определяющий формат сообщений лога.
    - Добавляет форматтер к обработчику консоли.
    - Добавляет обработчик консоли к логгеру.

    Примеры:
        >>> import configparser
        >>> config = configparser.ConfigParser()
        >>> config['Logging'] = {'LOGLEVEL': 'DEBUG'}
        >>> start_logger(config)
    """
    ...
```

## Классы

### `JsonSerializableRegistry`

```python
class JsonSerializableRegistry:
    """
    Миксин-класс, обеспечивающий JSON-сериализацию, десериализацию и регистрацию подклассов.

    Атрибуты:
        class_mapping (dict): Словарь, сопоставляющий имена классов с самими классами для десериализации.

    Методы:
        to_json(self, include: list = None, suppress: list = None, file_path: str = None) -> dict:
            Возвращает JSON-представление объекта.
        from_json(cls, json_dict_or_path, suppress: list = None, post_init_params: dict = None):
            Загружает JSON-представление объекта и создает экземпляр класса.
    """

    class_mapping = {}

    def to_json(self, include: list = None, suppress: list = None, file_path: str = None) -> dict:
        """
        Возвращает JSON-представление объекта.

        Args:
            include (list, optional): Атрибуты для включения в сериализацию.
            suppress (list, optional): Атрибуты для исключения из сериализации.
            file_path (str, optional): Путь к файлу, куда будет записан JSON.

        Returns:
            dict: JSON-представление объекта.
        """
        ...

    @classmethod
    def from_json(cls, json_dict_or_path, suppress: list = None, post_init_params: dict = None):
        """
        Загружает JSON-представление объекта и создает экземпляр класса.

        Args:
            json_dict_or_path (dict or str): JSON-словарь, представляющий объект, или путь к файлу для загрузки JSON.
            suppress (list, optional): Атрибуты, которые нужно исключить из загрузки.
            post_init_params (dict, optional): Параметры для передачи в метод `_post_deserialization_init`.

        Returns:
            An instance of the class populated with the data from json_dict_or_path.
        """
        ...

    def __init_subclass__(cls, **kwargs):
        """
        Регистрирует подкласс и автоматически расширяет атрибуты сериализации и инициализаторы из родительских классов.

        Args:
            cls: Подкласс для инициализации.
            **kwargs: Дополнительные аргументы.
        """
        ...

    def _post_deserialization_init(self, **kwargs):
        """
        Вызывает метод `_post_init`, если он существует, после десериализации.

        Args:
            **kwargs: Ключевые аргументы, передаваемые в `_post_init`.
        """
        ...
```

### `post_init`

```python
def post_init(cls):
    """
    Декоратор для принудительного вызова метода постобработки инициализации в классе, если он есть.
    Метод должен называться `_post_init`.

    Args:
        cls: Класс для декорирования.

    Как работает функция:
    - Сохраняет оригинальный метод `__init__` класса.
    - Определяет новый метод `__init__`, который вызывает оригинальный метод `__init__` и, если существует метод `_post_init`, вызывает его.
    - Заменяет оригинальный метод `__init__` новым методом `__init__`.
    - Возвращает класс.

    Примеры:
        >>> @post_init
        ... class MyClass:
        ...     def __init__(self, value):
        ...         self.value = value
        ...     def _post_init(self):
        ...         self.value = self.value * 2
        ...
        >>> my_object = MyClass(5)
        >>> my_object.value
        10
    """
    ...
```

## Другие функции

### `name_or_empty`

```python
def name_or_empty(named_entity: AgentOrWorld):
    """
    Возвращает имя указанного агента или среды, или пустую строку, если агент равен None.

    Args:
        named_entity (AgentOrWorld): Агент или среда.

    Returns:
        str: Имя агента или среды, или пустая строка.

    Пример:
        >>> name_or_empty(None)
        ''
    """
    ...
```

### `custom_hash`

```python
def custom_hash(obj):
    """
    Возвращает хеш для указанного объекта. Объект сначала преобразуется
    в строку, чтобы сделать его хешируемым. Этот метод является детерминированным,
    в отличие от встроенной функции hash().

    Args:
        obj: Объект для хеширования.

    Returns:
        str: Хеш объекта.

    Пример:
        >>> custom_hash('test')
        '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
    """
    ...
```

### `fresh_id`

```python
def fresh_id():
    """
    Возвращает новый ID для нового объекта. Это полезно для создания уникальных ID для объектов.

    Returns:
        int: Новый ID.

    Пример:
        >>> fresh_id()
        1
    """
    ...