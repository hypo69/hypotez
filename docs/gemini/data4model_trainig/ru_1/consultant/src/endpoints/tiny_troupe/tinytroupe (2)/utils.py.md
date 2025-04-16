### Анализ кода модуля `utils.py`

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура модуля, разделение на логические блоки (Model input/output, Model control, Validation, Prompt engineering, Rendering, IO).
    - Использование аннотаций типов.
    - Использование `textwrap.dedent` для удаления отступов.
    - Наличие класса `JsonSerializableRegistry` для работы с JSON-сериализацией и десериализацией.
- **Минусы**:
    - Не везде есть docstrings, особенно для простых функций.
    - В некоторых местах используются старые стили форматирования (например, `Union[]` вместо `|`).
    - Отсутствует логирование ошибок.
    - Не все функции имеют примеры использования в docstring.
    - Использование `print` для отладочной информации вместо `logger`.
    - В некоторых функциях отсутствует обработка исключений.
    - В функциях `read_config_file` используется `print` вместо `logger`.

**Рекомендации по улучшению:**

1.  **Документирование**:
    - Добавить docstrings ко всем функциям, классам и методам, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Добавить примеры использования в docstrings, где это уместно.

2.  **Логирование**:
    - Заменить все `print` statements на логирование через модуль `logger`.
    - Добавить логирование в блоки `except` для отслеживания ошибок.

3.  **Форматирование**:
    - Использовать `|` вместо `Union[]` для объединения типов.
    - Обеспечить единообразное форматирование кода в соответствии с PEP8 (пробелы вокруг операторов, длина строк).
    - Использовать только одинарные кавычки для строк.

4.  **Обработка исключений**:
    - Добавить обработку исключений там, где это необходимо, и логировать их с помощью `logger.error`.
    - Использовать `ex` вместо `e` в блоках `except`.

5.  **Конфигурация**:
    - Использовать `j_loads` или `j_loads_ns` для чтения конфигурационных файлов.

6.  **Безопасность**:
    - Рассмотреть возможность использования более надежных методов хеширования, чем `hashlib.sha256`, в зависимости от требований безопасности.

7.  **Аннотации типов**:
    - Убедиться, что все переменные и параметры функций имеют аннотации типов.

8.  **Удалить избыточное логирование**:
    - Убрать `print` из функции `read_config_file` и заменить на `logger.debug`.

**Оптимизированный код:**

```python
"""
Общие утилиты и вспомогательные функции.
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
from typing import Any, TypeVar, Union
AgentOrWorld = Union["TinyPerson", "TinyWorld"]

# logger
logger = logging.getLogger("tinytroupe")


################################################################################
# Model input utilities
################################################################################

def compose_initial_LLM_messages_with_templates(system_template_name: str, user_template_name: Optional[str] = None, rendering_configs: dict = {}) -> list:
    """
    Создает начальные сообщения для вызова LLM модели, предполагая, что всегда используется
    системное (общее описание задачи) и необязательное пользовательское сообщение (конкретное описание задачи).
    Эти сообщения составляются с использованием указанных шаблонов и конфигураций рендеринга.

    Args:
        system_template_name (str): Имя шаблона системного сообщения.
        user_template_name (Optional[str], optional): Имя шаблона пользовательского сообщения. По умолчанию None.
        rendering_configs (dict, optional): Конфигурации рендеринга. По умолчанию {}.

    Returns:
        list: Список сообщений для LLM.

    Example:
        >>> compose_initial_LLM_messages_with_templates('system.mustache', 'user.mustache', {'name': 'test'})
        [{'role': 'system', 'content': 'System message'}, {'role': 'user', 'content': 'User message'}]
    """
    system_prompt_template_path = os.path.join(os.path.dirname(__file__), f'prompts/{system_template_name}')
    user_prompt_template_path = os.path.join(os.path.dirname(__file__), f'prompts/{user_template_name}')

    messages = []

    try:
        with open(system_prompt_template_path, 'r', encoding='utf-8') as f:
            system_content = chevron.render(f.read(), rendering_configs)
        messages.append({'role': 'system', 'content': system_content})

        if user_template_name is not None:
            with open(user_prompt_template_path, 'r', encoding='utf-8') as f:
                user_content = chevron.render(f.read(), rendering_configs)
            messages.append({'role': 'user', 'content': user_content})
    except FileNotFoundError as ex:
        logger.error(f'Template file not found: {ex}', exc_info=True)
        return []
    except Exception as ex:
        logger.error(f'Error composing LLM messages: {ex}', exc_info=True)
        return []

    return messages


################################################################################
# Model output utilities
################################################################################
def extract_json(text: str) -> dict:
    """
    Извлекает JSON объект из строки, игнорируя: любой текст до первой
    открывающей фигурной скобки; и любые Markdown открывающие (```json) или закрывающие (```) теги.

    Args:
        text (str): Строка для извлечения JSON.

    Returns:
        dict: Извлеченный JSON объект или пустой словарь в случае ошибки.

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
        text = re.sub("\\\\'", "'", text)  # re.sub(r\'\\\\\\\'\', r"\'", text)

        # return the parsed JSON object
        return json.loads(text)

    except json.JSONDecodeError as ex:
        logger.error(f'JSONDecodeError: {ex}', exc_info=True)
        return {}
    except Exception as ex:
        logger.error(f'Error extracting JSON: {ex}', exc_info=True)
        return {}


def extract_code_block(text: str) -> str:
    """
    Извлекает блок кода из строки, игнорируя любой текст до первого
    открывающего тройного обратного апострофа и любой текст после закрывающего тройного обратного апострофа.

    Args:
        text (str): Строка для извлечения блока кода.

    Returns:
        str: Извлеченный блок кода или пустая строка в случае ошибки.

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
        logger.error(f'Error extracting code block: {ex}', exc_info=True)
        return ''


################################################################################
# Model control utilities
################################################################################

def repeat_on_error(retries: int, exceptions: list):
    """
    Декоратор, который повторяет вызов указанной функции, если происходит исключение из числа указанных,
    до указанного количества повторных попыток. Если это количество повторных попыток превышено,
    исключение генерируется. Если исключение не происходит, функция возвращается нормально.

    Args:
        retries (int): Количество повторных попыток.
        exceptions (list): Список классов исключений для перехвата.
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
                        logger.debug(f"Retrying ({i + 1}/{retries})...")
                        continue

        return wrapper

    return decorator


################################################################################
# Validation
################################################################################
def check_valid_fields(obj: dict, valid_fields: list) -> None:
    """
    Проверяет, являются ли поля в указанном словаре допустимыми, в соответствии со списком допустимых полей.
    Если нет, вызывает ValueError.

    Args:
        obj (dict): Словарь для проверки.
        valid_fields (list): Список допустимых полей.

    Raises:
        ValueError: Если в словаре есть недопустимые ключи.

    Example:
        >>> check_valid_fields({'a': 1, 'b': 2}, ['a', 'b'])
        >>> check_valid_fields({'a': 1, 'c': 2}, ['a', 'b'])
        ValueError: Invalid key c in dictionary. Valid keys are: ['a', 'b']
    """
    for key in obj:
        if key not in valid_fields:
            raise ValueError(f'Invalid key {key} in dictionary. Valid keys are: {valid_fields}')


def sanitize_raw_string(value: str) -> str:
    """
    Очищает указанную строку путем:
      - удаления любых недопустимых символов.
      - обеспечения того, чтобы она не была длиннее максимальной длины строки Python.

    Это делается из соображений предосторожности для обеспечения безопасности, чтобы избежать любых потенциальных проблем со строкой.

    Args:
        value (str): Строка для очистки.

    Returns:
        str: Очищенная строка.
    """

    # remove any invalid characters by making sure it is a valid UTF-8 string
    value = value.encode('utf-8', 'ignore').decode('utf-8')

    # ensure it is not longer than the maximum Python string length
    return value[:sys.maxsize]


def sanitize_dict(value: dict) -> dict:
    """
    Очищает указанный словарь путем:
      - удаления любых недопустимых символов.
      - обеспечения того, чтобы словарь не был слишком глубоко вложен.

    Args:
        value (dict): Словарь для очистки.

    Returns:
        dict: Очищенный словарь.

    Example:
        >>> sanitize_dict({'a': 'b', 'c': {'d': 'e'}})
        {'a': 'b', 'c': {'d': 'e'}}
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
    Добавляет переменные шаблона RAI в указанный словарь, если включены отказы от ответственности RAI.
    Они могут быть настроены в файле config.ini. Если включено, переменные будут загружать отказы от ответственности RAI из
    соответствующих файлов в каталоге prompts. В противном случае переменные будут установлены в None.

    Args:
        template_variables (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

    Returns:
        dict: Обновленный словарь переменных шаблона.
    """

    from tinytroupe import config  # avoids circular import

    rai_harmful_content_prevention = config["Simulation"].getboolean(
        "RAI_HARMFUL_CONTENT_PREVENTION", True
    )
    rai_copyright_infringement_prevention = config["Simulation"].getboolean(
        "RAI_COPYRIGHT_INFRINGEMENT_PREVENTION", True
    )

    try:
        # Harmful content
        with open(os.path.join(os.path.dirname(__file__), "prompts/rai_harmful_content_prevention.md"), "r", encoding='utf-8') as f:
            rai_harmful_content_prevention_content = f.read()

        template_variables['rai_harmful_content_prevention'] = rai_harmful_content_prevention_content if rai_harmful_content_prevention else None

        # Copyright infringement
        with open(os.path.join(os.path.dirname(__file__), "prompts/rai_copyright_infringement_prevention.md"), "r", encoding='utf-8') as f:
            rai_copyright_infringement_prevention_content = f.read()

        template_variables['rai_copyright_infringement_prevention'] = rai_copyright_infringement_prevention_content if rai_copyright_infringement_prevention else None

    except FileNotFoundError as ex:
        logger.error(f'RAI disclaimer file not found: {ex}', exc_info=True)
        template_variables['rai_harmful_content_prevention'] = None
        template_variables['rai_copyright_infringement_prevention'] = None
    except Exception as ex:
        logger.error(f'Error adding RAI template variables: {ex}', exc_info=True)
        template_variables['rai_harmful_content_prevention'] = None
        template_variables['rai_copyright_infringement_prevention'] = None

    return template_variables


################################################################################
# Rendering and markup
################################################################################
def inject_html_css_style_prefix(html: str, style_prefix_attributes: str) -> str:
    """
    Вставляет префикс стиля ко всем атрибутам стиля в заданной HTML строке.

    Например, если вы хотите добавить префикс стиля ко всем атрибутам стиля в HTML строке
    ``<div style="color: red;">Hello</div>``, вы можете использовать эту функцию следующим образом:
    inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')
    """
    return html.replace('style="', f'style="{style_prefix_attributes};')


def break_text_at_length(text: str | dict, max_length: Optional[int] = None) -> str:
    """
    Разбивает текст (или JSON) на указанной длине, вставляя строку "(...)" в точке разрыва.
    Если максимальная длина равна None, содержимое возвращается как есть.

    Args:
        text (str | dict): Текст или JSON для разбивки.
        max_length (Optional[int], optional): Максимальная длина текста. По умолчанию None.

    Returns:
        str: Разбитый текст.
    """
    if isinstance(text, dict):
        text = json.dumps(text, indent=4)

    if max_length is None or len(text) <= max_length:
        return text
    else:
        return text[:max_length] + ' (...)'


def pretty_datetime(dt: datetime) -> str:
    """
    Возвращает строковое представление указанного объекта datetime.

    Args:
        dt (datetime): Объект datetime.

    Returns:
        str: Строковое представление datetime.
    """
    return dt.strftime('%Y-%m-%d %H:%M')


def dedent(text: str) -> str:
    """
    Удаляет отступы из указанного текста, удаляя любые начальные пробелы и отступы.

    Args:
        text (str): Текст для удаления отступов.

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
        use_cache (bool, optional): Использовать кэшированную конфигурацию. По умолчанию True.
        verbose (bool, optional): Выводить отладочную информацию. По умолчанию True.

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
        logger.debug(f"Looking for default config on: {config_file_path}") if verbose else None
        if config_file_path.exists():
            config.read(config_file_path)
            _config = config
        else:
            raise ValueError(f"Failed to find default config on: {config_file_path}")

        # Now, let's override any specific default value, if there's a custom .ini config.
        # Try the directory of the current main program
        config_file_path = Path.cwd() / "config.ini"
        if config_file_path.exists():
            logger.debug(f"Found custom config on: {config_file_path}") if verbose else None
            config.read(config_file_path)  # this only overrides the values that are present in the custom config
            _config = config
            return config
        else:
            if verbose:
                logger.debug(f"Failed to find custom config on: {config_file_path}") if verbose else None
                logger.debug("Will use only default values. IF THINGS FAIL, TRY CUSTOMIZING MODEL, API TYPE, etc.") if verbose else None

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
    Запускает логгер.

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
    Миксин, который предоставляет JSON сериализацию, десериализацию и регистрацию подклассов.
    """

    class_mapping = {}

    def to_json(self, include: Optional[List[str]] = None, suppress: Optional[List[str]] = None, file_path: Optional[str] = None) -> dict:
        """
        Возвращает JSON представление объекта.

        Args:
            include (Optional[List[str]], optional): Атрибуты для включения в сериализацию.
            suppress (Optional[List[str]], optional): Атрибуты для исключения из сериализации.
            file_path (Optional[str], optional): Путь к файлу, куда будет записан JSON.
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

        if file_path:
            # Create directories if they do not exist
            import os
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(result, f, indent=4)

        return result

    @classmethod
    def from_json(cls, json_dict_or_path: Union[dict, str], suppress: Optional[List[str]] = None, post_init_params: Optional[dict] = None):
        """
        Загружает JSON представление объекта и создает экземпляр класса.

        Args:
            json_dict_or_path (Union[dict, str]): JSON словарь, представляющий объект, или путь к файлу для загрузки JSON.
            suppress (Optional[List[str]], optional): Атрибуты, которые нужно исключить из загрузки.

        Returns:
            Экземпляр класса, заполненный данными из json_dict_or_path.
        """
        if isinstance(json_dict_or_path, str):
            try:
                with open(json_dict_or_path, 'r') as f:
                    json_dict = json.load(f)
            except FileNotFoundError as ex:
                logger.error(f'File not found: {ex}', exc_info=True)
                return None
            except json.JSONDecodeError as ex:
                logger.error(f'JSONDecodeError: {ex}', exc_info=True)
                return None
            except Exception as ex:
                logger.error(f'Error loading JSON: {ex}', exc_info=True)
                return None
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
    Декоратор для принудительного вызова метода post-initialization в классе, если он есть.
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

    Args:
        named_entity (AgentOrWorld): Агент или среда.

    Returns:
        str: Имя агента или среды.
    """
    if named_entity is None:
        return ''
    else:
        return named_entity.name


def custom_hash(obj: Any) -> str:
    """
    Возвращает хеш для указанного объекта. Объект сначала преобразуется
    в строку, чтобы сделать его хешируемым. Этот метод является детерминированным,
    в отличие от встроенной функции hash().

    Args:
        obj (Any): Объект для хеширования.

    Returns:
        str: Хеш объекта.
    """
    return hashlib.sha256(str(obj).encode()).hexdigest()


_fresh_id_counter = 0


def fresh_id() -> int:
    """
    Возвращает новый ID для нового объекта. Это полезно для создания уникальных ID для объектов.

    Returns:
        int: Новый ID.
    """
    global _fresh_id_counter
    _fresh_id_counter += 1
    return _fresh_id_counter