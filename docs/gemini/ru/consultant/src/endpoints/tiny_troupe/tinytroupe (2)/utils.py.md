### **Анализ кода модуля `utils.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/utils.py

Модуль содержит набор общих утилитных функций и классов, используемых в проекте TinyTroupe. Он включает функции для работы с LLM, обработки текста, валидации данных, управления конфигурацией, а также класс для JSON сериализации.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая организация кода по функциональным блокам.
    - Использование аннотаций типов для параметров и возвращаемых значений функций.
    - Наличие docstring для большинства функций и классов.
    - Использование `logger` для логирования.
    - Реализация JSON сериализации с возможностью расширения и настройки.
- **Минусы**:
    - Docstring написаны на английском языке.
    - Не все функции имеют подробное описание в docstring.
    - Местами отсутствует обработка исключений.
    - В некоторых местах используется устаревший стиль кодирования (например, `Union[]` вместо `|`).

**Рекомендации по улучшению:**

1.  **Перевести docstring на русский язык.** Необходимо перевести все docstring на русский язык, чтобы соответствовать требованиям.
2.  **Дополнить docstring подробными описаниями.** Добавить подробные описания для всех функций, включая описание параметров, возвращаемых значений и возможных исключений.
3.  **Заменить `Union[]` на `|`.** В аннотациях типов использовать `|` вместо `Union[]`.
4.  **Улучшить обработку исключений.** Добавить обработку исключений в тех местах, где она отсутствует, и логировать ошибки с использованием `logger.error`.
5.  **Добавить примеры использования в docstring.** Для каждой функции добавить примеры использования, чтобы облегчить понимание ее работы.
6.  **Проверить и обновить комментарии.** Убедиться, что все комментарии актуальны и соответствуют коду. Если комментарий кажется устаревшим или неясным, не изменяйте его, а отметьте его в разделе изменений.
7.  **Заменить стандартные `open` и `json.load` на `j_loads` или `j_loads_ns`.** Для чтения JSON или конфигурационных файлов использовать `j_loads` или `j_loads_ns` вместо стандартных функций.

**Оптимизированный код:**

```python
"""
Модуль общих утилит и вспомогательных функций.
================================================

Модуль содержит набор общих утилитных функций и классов, используемых в проекте TinyTroupe.
Он включает функции для работы с LLM, обработки текста, валидации данных, управления конфигурацией,
а также класс для JSON сериализации.
"""
import re
import json
import os
import sys
import hashlib
import textwrap
import logging
import chevron
import copy
from typing import Collection, Optional, List
from datetime import datetime
from pathlib import Path
import configparser
from typing import Any, TypeVar
AgentOrWorld = "TinyPerson" | "TinyWorld" # Union["TinyPerson", "TinyWorld"]

# logger
logger = logging.getLogger("tinytroupe")


################################################################################
# Model input utilities
################################################################################


def compose_initial_LLM_messages_with_templates(system_template_name: str, user_template_name: Optional[str] = None, rendering_configs: dict = {}) -> list:
    """
    Формирует начальные сообщения для вызова LLM модели, предполагая, что всегда есть
    системное сообщение (общее описание задачи) и опциональное пользовательское сообщение
    (специфическое описание задачи). Эти сообщения формируются с использованием указанных
    шаблонов и конфигураций рендеринга.

    Args:
        system_template_name (str): Имя файла шаблона для системного сообщения.
        user_template_name (Optional[str], optional): Имя файла шаблона для пользовательского сообщения. По умолчанию None.
        rendering_configs (dict, optional): Словарь с конфигурациями для рендеринга шаблонов. По умолчанию {}.

    Returns:
        list: Список словарей, представляющих сообщения для LLM модели.

    Example:
        >>> messages = compose_initial_LLM_messages_with_templates('system_prompt.md', 'user_prompt.md', {'name': 'Agent'})
        >>> print(messages)
        [{'role': 'system', 'content': '...'}, {'role': 'user', 'content': '...'}]
    """
    system_prompt_template_path = os.path.join(os.path.dirname(__file__), f'prompts/{system_template_name}')
    user_prompt_template_path = os.path.join(os.path.dirname(__file__), f'prompts/{user_template_name}')

    messages = []

    messages.append({"role": "system",
                         "content": chevron.render(
                             open(system_prompt_template_path).read(),
                             rendering_configs)})
    
    # optionally add a user message
    if user_template_name is not None:
        messages.append({"role": "user",
                            "content": chevron.render(
                                    open(user_prompt_template_path).read(),
                                    rendering_configs)})
    return messages


################################################################################
# Model output utilities
################################################################################
def extract_json(text: str) -> dict:
    """
    Извлекает JSON объект из строки, игнорируя: любой текст до первой открывающей фигурной скобки;
    и любые Markdown открывающие (```json) или закрывающие (```) теги.

    Args:
        text (str): Строка, из которой нужно извлечь JSON объект.

    Returns:
        dict: Словарь, представляющий извлеченный JSON объект. Возвращает пустой словарь, если извлечение не удалось.

    Raises:
        json.JSONDecodeError: Если строка не содержит валидный JSON.

    Example:
        >>> extract_json('```json { "key": "value" } ```')
        {'key': 'value'}
    """
    try:
        # remove any text before the first opening curly or square braces, using regex. Leave the braces.
        text = re.sub(r'^.*?({|\\[)', r'\\1', text, flags=re.DOTALL)

        # remove any trailing text after the LAST closing curly or square braces, using regex. Leave the braces.
        text = re.sub(r'(}|\\])(?!.*(\\]|\\})).*$', r'\\1', text, flags=re.DOTALL)
        
        # remove invalid escape sequences, which show up sometimes
        # replace \\\' with just \'
        text = re.sub("\\\\\'", "\'", text) #re.sub(r\'\\\\\\\'\', r"\'", text)

        # return the parsed JSON object
        return json.loads(text)
    
    except Exception as ex:
        logger.error('Error while extracting JSON', ex, exc_info=True)
        return {}


def extract_code_block(text: str) -> str:
    """
    Извлекает блок кода из строки, игнорируя любой текст до первого открывающего тройного обратного апострофа
    и любой текст после закрывающего тройного обратного апострофа.

    Args:
        text (str): Строка, из которой нужно извлечь блок кода.

    Returns:
        str: Извлеченный блок кода. Возвращает пустую строку, если извлечение не удалось.

    Example:
        >>> extract_code_block('```python print("Hello") ```')
        '```python print("Hello") ```'
    """
    try:
        # remove any text before the first opening triple backticks, using regex. Leave the backticks.
        text = re.sub(r'^.*?(```)', r'\\1', text, flags=re.DOTALL)

        # remove any trailing text after the LAST closing triple backticks, using regex. Leave the backticks.
        text = re.sub(r'(```)(?!.*```).*$', r'\\1', text, flags=re.DOTALL)
        
        return text
    
    except Exception as ex:
        logger.error('Error while extracting code block', ex, exc_info=True)
        return ""


################################################################################
# Model control utilities
################################################################################


def repeat_on_error(retries: int, exceptions: list):
    """
    Декоратор, который повторяет вызов указанной функции, если происходит исключение из числа указанных,
    до указанного количества повторных попыток. Если это количество повторных попыток превышено,
    исключение поднимается. Если исключение не происходит, функция возвращается нормально.

    Args:
        retries (int): Количество повторных попыток.
        exceptions (list): Список классов исключений, которые нужно перехватывать.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as ex:
                    logger.debug(f"Exception occurred: {ex}")
                    if i == retries - 1:
                        raise ex
                    else:
                        logger.debug(f"Retrying ({i+1}/{retries})...")
                        continue
        return wrapper
    return decorator


################################################################################
# Validation
################################################################################
def check_valid_fields(obj: dict, valid_fields: list) -> None:
    """
    Проверяет, являются ли поля в указанном словаре допустимыми, в соответствии со списком допустимых полей.
    Если нет, вызывает исключение ValueError.

    Args:
        obj (dict): Словарь, который нужно проверить.
        valid_fields (list): Список допустимых полей.

    Raises:
        ValueError: Если в словаре есть недопустимые поля.

    Example:
        >>> check_valid_fields({'key1': 'value1', 'key2': 'value2'}, ['key1', 'key2'])
        >>> check_valid_fields({'key1': 'value1', 'key2': 'value2'}, ['key1'])
        ValueError: Invalid key key2 in dictionary. Valid keys are: ['key1']
    """
    for key in obj:
        if key not in valid_fields:
            raise ValueError(f"Invalid key {key} in dictionary. Valid keys are: {valid_fields}")


def sanitize_raw_string(value: str) -> str:
    """
    Очищает указанную строку, выполняя следующие действия:
      - удаляет любые недопустимые символы.
      - проверяет, чтобы она не была длиннее максимальной длины строки Python.

    Это делается из соображений предосторожности с безопасностью, чтобы избежать любых потенциальных проблем со строкой.

    Args:
        value (str): Строка, которую нужно очистить.

    Returns:
        str: Очищенная строка.
    """

    # remove any invalid characters by making sure it is a valid UTF-8 string
    value = value.encode("utf-8", "ignore").decode("utf-8")

    # ensure it is not longer than the maximum Python string length
    return value[:sys.maxsize]


def sanitize_dict(value: dict) -> dict:
    """
    Очищает указанный словарь, выполняя следующие действия:
      - удаляет любые недопустимые символы.
      - проверяет, чтобы словарь не был слишком глубоко вложен.

    Args:
        value (dict): Словарь, который нужно очистить.

    Returns:
        dict: Очищенный словарь.
    """

    # sanitize the string representation of the dictionary
    tmp_str = sanitize_raw_string(json.dumps(value, ensure_ascii=False))

    value = json.loads(tmp_str)

    # ensure that the dictionary is not too deeply nested
    return value
    

################################################################################
# Prompt engineering
################################################################################
def add_rai_template_variables_if_enabled(template_variables: dict) -> dict:
    """
    Добавляет переменные шаблона RAI в указанный словарь, если включены дисклеймеры RAI.
    Они могут быть настроены в файле config.ini. Если включены, переменные будут загружать
    дисклеймеры RAI из соответствующих файлов в каталоге prompts. В противном случае переменные будут установлены в None.

    Args:
        template_variables (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

    Returns:
        dict: Обновленный словарь переменных шаблона.
    """

    from tinytroupe import config # avoids circular import
    rai_harmful_content_prevention = config["Simulation"].getboolean(
        "RAI_HARMFUL_CONTENT_PREVENTION", True
    )
    rai_copyright_infringement_prevention = config["Simulation"].getboolean(
        "RAI_COPYRIGHT_INFRINGEMENT_PREVENTION", True
    )

    # Harmful content
    with open(os.path.join(os.path.dirname(__file__), "prompts/rai_harmful_content_prevention.md"), "r") as f:
        rai_harmful_content_prevention_content = f.read()

    template_variables['rai_harmful_content_prevention'] = rai_harmful_content_prevention_content if rai_harmful_content_prevention else None

    # Copyright infringement
    with open(os.path.join(os.path.dirname(__file__), "prompts/rai_copyright_infringement_prevention.md"), "r") as f:
        rai_copyright_infringement_prevention_content = f.read()

    template_variables['rai_copyright_infringement_prevention'] = rai_copyright_infringement_prevention_content if rai_copyright_infringement_prevention else None

    return template_variables

################################################################################
# Rendering and markup
################################################################################
def inject_html_css_style_prefix(html: str, style_prefix_attributes: str) -> str:
    """
    Вставляет префикс стиля во все атрибуты style в заданной HTML строке.

    Например, если вы хотите добавить префикс стиля ко всем атрибутам style в HTML строке
    ``<div style="color: red;">Hello</div>``, вы можете использовать эту функцию следующим образом:
    inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')

    Args:
        html (str): HTML строка, в которую нужно вставить префикс стиля.
        style_prefix_attributes (str): Префикс стиля, который нужно вставить.

    Returns:
        str: HTML строка с вставленным префиксом стиля.
    """
    return html.replace('style="', f'style="{style_prefix_attributes};')


def break_text_at_length(text: str | dict, max_length: Optional[int] = None) -> str:
    """
    Разбивает текст (или JSON) на указанной длине, вставляя строку "(...)" в точке разрыва.
    Если максимальная длина равна None, контент возвращается как есть.

    Args:
        text (str | dict): Текст или JSON, который нужно разбить.
        max_length (Optional[int], optional): Максимальная длина текста. По умолчанию None.

    Returns:
        str: Разбитый текст.
    """
    if isinstance(text, dict):
        text = json.dumps(text, indent=4)

    if max_length is None or len(text) <= max_length:
        return text
    else:
        return text[:max_length] + " (...)"


def pretty_datetime(dt: datetime) -> str:
    """
    Возвращает строковое представление объекта datetime в удобном формате.

    Args:
        dt (datetime): Объект datetime, который нужно отформатировать.

    Returns:
        str: Строковое представление объекта datetime.
    """
    return dt.strftime("%Y-%m-%d %H:%M")


def dedent(text: str) -> str:
    """
    Удаляет отступы в указанном тексте, удаляя любые начальные пробелы и отступы.

    Args:
        text (str): Текст, из которого нужно удалить отступы.

    Returns:
        str: Текст без отступов.
    """
    return textwrap.dedent(text).strip()


################################################################################
# IO and startup utilities
################################################################################
_config = None


def read_config_file(use_cache: bool = True, verbose: bool = True) -> configparser.ConfigParser:
    """
    Читает файл конфигурации.

    Args:
        use_cache (bool, optional): Использовать ли кэшированную конфигурацию. По умолчанию True.
        verbose (bool, optional): Выводить ли отладочную информацию. По умолчанию True.

    Returns:
        configparser.ConfigParser: Объект конфигурации.
    """
    global _config
    if use_cache and _config is not None:
        # if we have a cached config and accept that, return it
        return _config
    
    else:
        config = configparser.ConfigParser()

        # Read the default values in the module directory.
        config_file_path = Path(__file__).parent.absolute() / 'config.ini'
        print(f"Looking for default config on: {config_file_path}") if verbose else None
        if config_file_path.exists():
            config.read(config_file_path)
            _config = config
        else:
            raise ValueError(f"Failed to find default config on: {config_file_path}")

        # Now, let\'s override any specific default value, if there\'s a custom .ini config.
        # Try the directory of the current main program
        config_file_path = Path.cwd() / "config.ini"
        if config_file_path.exists():
            print(f"Found custom config on: {config_file_path}") if verbose else None
            config.read(config_file_path) # this only overrides the values that are present in the custom config
            _config = config
            return config
        else:
            if verbose:
                print(f"Failed to find custom config on: {config_file_path}") if verbose else None
                print("Will use only default values. IF THINGS FAIL, TRY CUSTOMIZING MODEL, API TYPE, etc.") if verbose else None
        
        return config


def pretty_print_config(config: configparser.ConfigParser) -> None:
    """
    Выводит конфигурацию в удобочитаемом формате.

    Args:
        config (configparser.ConfigParser): Объект конфигурации.
    """
    print()
    print("=================================")
    print("Current TinyTroupe configuration ")
    print("=================================")
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")
        print()


def start_logger(config: configparser.ConfigParser) -> None:
    """
    Инициализирует логгер.

    Args:
        config (configparser.ConfigParser): Объект конфигурации.
    """
    # create logger
    logger = logging.getLogger("tinytroupe")
    log_level = config['Logging'].get('LOGLEVEL', 'INFO').upper()
    logger.setLevel(level=log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


class JsonSerializableRegistry:
    """
    Миксин класс, который обеспечивает JSON сериализацию, десериализацию и регистрацию подклассов.
    """
    
    class_mapping = {}

    def to_json(self, include: Optional[List[str]] = None, suppress: Optional[List[str]] = None, file_path: Optional[str] = None) -> dict:
        """
        Возвращает JSON представление объекта.
        
        Args:
            include (Optional[List[str]], optional): Атрибуты для включения в сериализацию. По умолчанию None.
            suppress (Optional[List[str]], optional): Атрибуты для исключения из сериализации. По умолчанию None.
            file_path (Optional[str], optional): Путь к файлу, куда будет записан JSON. По умолчанию None.
        """
        # Gather all serializable attributes from the class hierarchy
        serializable_attrs = set()
        suppress_attrs = set()
        for cls in self.__class__.__mro__:
            if hasattr(cls, 'serializable_attributes') and isinstance(cls.serializable_attributes, list):
                serializable_attrs.update(cls.serializable_attributes)
            if hasattr(cls, 'suppress_attributes_from_serialization') and isinstance(cls.suppress_attributes_from_serialization, list):
                suppress_attrs.update(cls.suppress_attributes_from_serialization)
        
        # Override attributes with method parameters if provided
        if include:
            serializable_attrs = set(include)
        if suppress:
            suppress_attrs.update(suppress)
        
        result = {"json_serializable_class_name": self.__class__.__name__}
        for attr in serializable_attrs if serializable_attrs else self.__dict__:
            if attr not in suppress_attrs:
                value = getattr(self, attr, None)
                if isinstance(value, JsonSerializableRegistry):
                    result[attr] = value.to_json()
                elif isinstance(value, list):
                    result[attr] = [item.to_json() if isinstance(item, JsonSerializableRegistry) else copy.deepcopy(item) for item in value]
                elif isinstance(value, dict):
                    result[attr] = {k: v.to_json() if isinstance(v, JsonSerializableRegistry) else copy.deepcopy(v) for k, v in value.items()}
                else:
                    result[attr] = copy.deepcopy(value)
        
        if file_path:\n            # Create directories if they do not exist
            import os
            os.makedirs(os.path.dirname(file_path), exist_ok=True)\n            with open(file_path, \'w\') as f:\n                json.dump(result, f, indent=4)\n        \n        return result

    @classmethod
    def from_json(cls, json_dict_or_path: dict | str, suppress: Optional[List[str]] = None, post_init_params: Optional[dict] = None):
        """
        Загружает JSON представление объекта и создает экземпляр класса.
        
        Args:
            json_dict_or_path (dict | str): JSON словарь, представляющий объект, или путь к файлу для загрузки JSON.
            suppress (Optional[List[str]], optional): Атрибуты для исключения из загрузки. По умолчанию None.
            post_init_params (Optional[dict], optional): Параметры для передачи в метод _post_deserialization_init. По умолчанию None.

        Returns:
            An instance of the class populated with the data from json_dict_or_path.
        """
        if isinstance(json_dict_or_path, str):
            with open(json_dict_or_path, 'r') as f:
                json_dict = json.load(f)
        else:
            json_dict = json_dict_or_path
        
        subclass_name = json_dict.get("json_serializable_class_name")
        target_class = cls.class_mapping.get(subclass_name, cls)
        instance = target_class.__new__(target_class)  # Create an instance without calling __init__
        
        # Gather all serializable attributes from the class hierarchy
        serializable_attrs = set()
        custom_serialization_initializers = {}
        suppress_attrs = set(suppress) if suppress else set()
        for cls in target_class.__mro__:
            if hasattr(cls, 'serializable_attributes') and isinstance(cls.serializable_attributes, list):
                serializable_attrs.update(cls.serializable_attributes)
            if hasattr(cls, 'custom_serialization_initializers') and isinstance(cls.custom_serialization_initializers, dict):
                custom_serialization_initializers.update(cls.custom_serialization_initializers)
            if hasattr(cls, 'suppress_attributes_from_serialization') and isinstance(cls.suppress_attributes_from_serialization, list):
                suppress_attrs.update(cls.suppress_attributes_from_serialization)
        
        # Assign values only for serializable attributes if specified, otherwise assign everything
        for key in serializable_attrs if serializable_attrs else json_dict:
            if key in json_dict and key not in suppress_attrs:
                value = json_dict[key]
                if key in custom_serialization_initializers:
                    # Use custom initializer if provided
                    setattr(instance, key, custom_serialization_initializers[key](value))
                elif isinstance(value, dict) and 'json_serializable_class_name' in value:
                    # Assume it's another JsonSerializableRegistry object
                    setattr(instance, key, JsonSerializableRegistry.from_json(value))
                elif isinstance(value, list):
                    # Handle collections, recursively deserialize if items are JsonSerializableRegistry objects
                    deserialized_collection = []
                    for item in value:
                        if isinstance(item, dict) and 'json_serializable_class_name' in item:
                            deserialized_collection.append(JsonSerializableRegistry.from_json(item))
                        else:
                            deserialized_collection.append(copy.deepcopy(item))
                    setattr(instance, key, deserialized_collection)
                else:
                    setattr(instance, key, copy.deepcopy(value))
        
        # Call post-deserialization initialization if available
        if hasattr(instance, '_post_deserialization_init') and callable(instance._post_deserialization_init):
            post_init_params = post_init_params if post_init_params else {}
            instance._post_deserialization_init(**post_init_params)
        
        return instance

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register the subclass using its name as the key
        JsonSerializableRegistry.class_mapping[cls.__name__] = cls
        
        # Automatically extend serializable attributes and custom initializers from parent classes
        if hasattr(cls, 'serializable_attributes') and isinstance(cls.serializable_attributes, list):
            for base in cls.__bases__:
                if hasattr(base, 'serializable_attributes') and isinstance(base.serializable_attributes, list):
                    cls.serializable_attributes = list(set(base.serializable_attributes + cls.serializable_attributes))
        
        if hasattr(cls, 'suppress_attributes_from_serialization') and isinstance(cls.suppress_attributes_from_serialization, list):
            for base in cls.__bases__:
                if hasattr(base, 'suppress_attributes_from_serialization') and isinstance(base.suppress_attributes_from_serialization, list):
                    cls.suppress_attributes_from_serialization = list(set(base.suppress_attributes_from_serialization + cls.suppress_attributes_from_serialization))
        
        if hasattr(cls, 'custom_serialization_initializers') and isinstance(cls.custom_serialization_initializers, dict):
            for base in cls.__bases__:
                if hasattr(base, 'custom_serialization_initializers') and isinstance(base.custom_serialization_initializers, dict):
                    base_initializers = base.custom_serialization_initializers.copy()
                    base_initializers.update(cls.custom_serialization_initializers)
                    cls.custom_serialization_initializers = base_initializers

    def _post_deserialization_init(self, **kwargs):
        # if there's a _post_init method, call it after deserialization
        if hasattr(self, '_post_init'):
            self._post_init(**kwargs)


def post_init(cls):
    """
    Декоратор для принудительного вызова метода post-инициализации в классе, если он есть.
    Метод должен называться `_post_init`.
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if hasattr(self, '_post_init'):
            self._post_init()

    cls.__init__ = new_init
    return cls

################################################################################
# Other
################################################################################
def name_or_empty(named_entity: AgentOrWorld) -> str:
    """
    Возвращает имя указанного агента или среды или пустую строку, если агент равен None.
    """
    if named_entity is None:
        return ""
    else:
        return named_entity.name

def custom_hash(obj) -> str:
    """
    Возвращает хеш для указанного объекта. Объект сначала преобразуется
    в строку, чтобы сделать его хешируемым. Этот метод является детерминированным,
    в отличие от встроенной функции hash().
    """

    return hashlib.sha256(str(obj).encode()).hexdigest()

_fresh_id_counter = 0
def fresh_id() -> int:
    """
    Возвращает свежий ID для нового объекта. Это полезно для создания уникальных ID для объектов.
    """
    global _fresh_id_counter
    _fresh_id_counter += 1
    return _fresh_id_counter