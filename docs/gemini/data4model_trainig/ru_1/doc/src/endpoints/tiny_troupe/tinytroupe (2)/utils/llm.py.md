# Модуль для работы с большими языковыми моделями (LLM)
====================================================

Модуль содержит набор утилит для взаимодействия с большими языковыми моделями (LLM), такими как OpenAI и Google Gemini.
Он предоставляет функции для подготовки входных данных для моделей, обработки выходных данных,
а также управления выполнением запросов к моделям.

## Обзор

Модуль `llm.py` предоставляет инструменты для упрощения работы с большими языковыми моделями (LLM). Он включает в себя функции для:

- Композиции сообщений для LLM с использованием шаблонов.
- Превращения функций в LLM-функции с помощью декоратора `@llm`.
- Извлечения JSON-объектов и блоков кода из текста.
- Повторного выполнения функций при возникновении ошибок.
- Добавления переменных шаблона RAI (Responsible AI).
- Усечения содержимого действий или стимулов.

## Подробнее

Этот модуль облегчает интеграцию LLM в проект `hypotez`, предоставляя удобные инструменты для подготовки запросов, обработки ответов и управления поведением моделей. Он позволяет использовать шаблоны для создания структурированных запросов, автоматически преобразовывать функции в LLM-функции и обрабатывать ошибки.

## Содержание

1.  [Функции](#Функции)
    *   [compose\_initial\_LLM\_messages\_with\_templates](#compose_initial_LLM_messages_with_templates)
    *   [llm](#llm)
    *   [extract\_json](#extract_json)
    *   [extract\_code\_block](#extract_code_block)
    *   [repeat\_on\_error](#repeat_on_error)
    *   [add\_rai\_template\_variables\_if\_enabled](#add_rai_template_variables_if_enabled)
    *   [truncate\_actions\_or\_stimuli](#truncate_actions_or_stimuli)

## Функции

### `compose_initial_LLM_messages_with_templates`

```python
def compose_initial_LLM_messages_with_templates(system_template_name:str, user_template_name:str=None, 
                                                base_module_folder:str=None,
                                                rendering_configs:dict={}) -> list:
    """
    Composes the initial messages for the LLM model call, under the assumption that it always involves 
    a system (overall task description) and an optional user message (specific task description). 
    These messages are composed using the specified templates and rendering configurations.
    """
```

**Назначение**:
Формирует начальные сообщения для вызова LLM-модели, предполагая, что всегда есть системное сообщение (общее описание задачи)
и необязательное пользовательское сообщение (конкретное описание задачи). Эти сообщения составляются с использованием указанных шаблонов
и конфигураций рендеринга.

**Параметры**:

*   `system_template_name` (str): Имя файла шаблона для системного сообщения.
*   `user_template_name` (str, optional): Имя файла шаблона для пользовательского сообщения. По умолчанию `None`.
*   `base_module_folder` (str, optional): Базовая папка модуля, относительно которой находятся шаблоны. По умолчанию `None`.
*   `rendering_configs` (dict, optional): Словарь с конфигурациями для рендеринга шаблонов. По умолчанию `{}`.

**Возвращает**:

*   `list`: Список, содержащий сообщения для LLM, где каждое сообщение представлено в виде словаря с ключами `"role"` и `"content"`.

**Как работает функция**:

1.  Определяет путь к папке с шаблонами, используя `base_module_folder` или значение по умолчанию `"../prompts/"`.
2.  Формирует полные пути к файлам шаблонов системного и пользовательского сообщений.
3.  Создает список `messages`, который будет содержать сообщения для LLM.
4.  Добавляет системное сообщение, считывая содержимое шаблона и применяя к нему конфигурации рендеринга с помощью `chevron.render`.
5.  Если указано имя файла шаблона пользовательского сообщения, добавляет пользовательское сообщение аналогичным образом.
6.  Возвращает список сообщений.

**Примеры**:

```python
# Пример использования с системным и пользовательским шаблонами
messages = compose_initial_LLM_messages_with_templates(
    system_template_name="system_prompt.md",
    user_template_name="user_prompt.md",
    rendering_configs={"task": "summarize text"}
)
print(messages)
# [{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': 'Summarize the following text: ...'}]

# Пример использования только с системным шаблоном
messages = compose_initial_LLM_messages_with_templates(
    system_template_name="system_prompt.md",
    rendering_configs={"task": "translate to Spanish"}
)
print(messages)
# [{'role': 'system', 'content': 'You are a helpful assistant that translates text to Spanish.'}]
```

### `llm`

```python
def llm(**model_overrides):
    """
    Decorator that turns the decorated function into an LLM-based function.
    The decorated function must either return a string (the instruction to the LLM),
    or the parameters of the function will be used instead as the instruction to the LLM.
    The LLM response is coerced to the function's annotated return type, if present.

    Usage example:
    @llm(model="gpt-4-0613", temperature=0.5, max_tokens=100)
    def joke():
        return "Tell me a joke."
    """
```

**Назначение**:
Декоратор, который преобразует декорируемую функцию в функцию на основе LLM. Декорируемая функция должна возвращать строку (инструкцию для LLM),
или параметры функции будут использоваться в качестве инструкции для LLM. Ответ LLM приводится к аннотированному типу возвращаемого значения функции, если он присутствует.

**Параметры**:

*   `**model_overrides`: Переопределения параметров модели LLM (например, `"model"`, `"temperature"`, `"max_tokens"`).

**Как работает функция**:

1.  Применяет декоратор `functools.wraps` для сохранения метаданных декорируемой функции.
2.  Внутри `wrapper` вызывает декорируемую функцию с переданными аргументами.
3.  Определяет тип возвращаемого значения функции из аннотации, если она есть. В противном случае использует `str`.
4.  Определяет системный промпт из `__doc__` функции, если он есть. В противном случае использует общее сообщение "You are an AI system that executes a computation as requested.".
5.  Если результат вызова функции является строкой, использует ее в качестве пользовательского промпта. В противном случае формирует пользовательский промпт на основе параметров функции.
6.  Создает экземпляр класса `LLMRequest` с системным промптом, пользовательским промптом, типом возвращаемого значения и переопределениями параметров модели.
7.  Вызывает метод `call()` объекта `LLMRequest` для получения ответа от LLM.
8.  Возвращает результат вызова LLM.

**Примеры**:

```python
from tinytroupe.openai_utils import LLMRequest

# Пример использования декоратора для получения шутки
@llm(model="gpt-4-0613", temperature=0.5, max_tokens=100)
def joke() -> str:
    """Tell me a joke."""
    return "Расскажи мне анекдот."

# Пример использования декоратора с параметрами функции
@llm(model="gpt-4-0613", temperature=0.7)
def summarize_text(text: str, max_length: int = 100) -> str:
    """Summarize the following text."""
    return f"Сократи следующий текст до {max_length} символов: {text}"
```

### `extract_json`

```python
def extract_json(text: str) -> dict:
    """
    Extracts a JSON object from a string, ignoring: any text before the first 
    opening curly brace; and any Markdown opening (```json) or closing(```) tags.
    """
```

**Назначение**:
Извлекает JSON-объект из строки, игнорируя: любой текст перед первой открывающей фигурной скобкой;
и любые открывающие (` ```json`) или закрывающие (` ````) теги Markdown.

**Параметры**:

*   `text` (str): Строка, из которой нужно извлечь JSON-объект.

**Возвращает**:

*   `dict`: Извлеченный JSON-объект в виде словаря. Возвращает пустой словарь `{}` в случае ошибки.

**Как работает функция**:

1.  Удаляет любой текст до первой открывающей фигурной или квадратной скобки с помощью регулярного выражения.
2.  Удаляет любой текст после последней закрывающей фигурной или квадратной скобки с помощью регулярного выражения.
3.  Удаляет недопустимые escape-последовательности, такие как `\\\'` и `\\,`.
4.  Использует `json.loads` с `strict=False` для корректного разбора новых строк, табуляций и т.д.
5.  Возвращает разобранный JSON-объект.
6.  В случае возникновения ошибки логирует ее с помощью `logger.error` и возвращает пустой словарь.

**Примеры**:

```python
from src.logger import logger
# Пример извлечения JSON из строки с Markdown-тегами
text = "```json\n{\"name\": \"John\", \"age\": 30}\n```"
json_obj = extract_json(text)
print(json_obj)
# {'name': 'John', 'age': 30}

# Пример извлечения JSON из строки с лишним текстом
text = "Some text before {\"name\": \"John\", \"age\": 30} some text after"
json_obj = extract_json(text)
print(json_obj)
# {'name': 'John', 'age': 30}

# Пример обработки ошибки при разборе JSON
text = "{\"name\": \"John\", \"age\": 30"  # Invalid JSON
json_obj = extract_json(text)
print(json_obj)
# {}  # Returns an empty dictionary in case of error
```

### `extract_code_block`

```python
def extract_code_block(text: str) -> str:
    """
    Extracts a code block from a string, ignoring any text before the first 
    opening triple backticks and any text after the closing triple backticks.
    """
```

**Назначение**:
Извлекает блок кода из строки, игнорируя любой текст перед первыми открывающими тремя обратными кавычками
и любой текст после закрывающих трех обратных кавычек.

**Параметры**:

*   `text` (str): Строка, из которой нужно извлечь блок кода.

**Возвращает**:

*   `str`: Извлеченный блок кода. Возвращает пустую строку `""` в случае ошибки.

**Как работает функция**:

1.  Удаляет любой текст до первых открывающих трех обратных кавычек с помощью регулярного выражения.
2.  Удаляет любой текст после последних закрывающих трех обратных кавычек с помощью регулярного выражения.
3.  Возвращает извлеченный блок кода.
4.  В случае возникновения ошибки возвращает пустую строку.

**Примеры**:

```python
# Пример извлечения блока кода из строки с Markdown-тегами
text = "```python\nprint(\"Hello, world!\")\n```"
code_block = extract_code_block(text)
print(code_block)
# ```python
# print("Hello, world!")
# ```

# Пример извлечения блока кода из строки с лишним текстом
text = "Some text before ```python\nprint(\"Hello, world!\")\n``` some text after"
code_block = extract_code_block(text)
print(code_block)
# ```python
# print("Hello, world!")
# ```

# Пример обработки строки без блока кода
text = "Some text without code block"
code_block = extract_code_block(text)
print(code_block)
# ""  # Returns an empty string
```

### `repeat_on_error`

```python
def repeat_on_error(retries:int, exceptions:list):
    """
    Decorator that repeats the specified function call if an exception among those specified occurs, 
    up to the specified number of retries. If that number of retries is exceeded, the
    exception is raised. If no exception occurs, the function returns normally.

    Args:
        retries (int): The number of retries to attempt.
        exceptions (list): The list of exception classes to catch.
    """
```

**Назначение**:
Декоратор, который повторяет вызов указанной функции, если возникает исключение из числа указанных,
до указанного количества попыток. Если это количество попыток превышено, исключение генерируется.
Если исключение не возникает, функция возвращается нормально.

**Параметры**:

*   `retries` (int): Количество попыток повтора вызова функции.
*   `exceptions` (list): Список классов исключений, которые нужно перехватывать.

**Как работает функция**:

1.  Определяет и возвращает декоратор, который принимает функцию `func` в качестве аргумента.
2.  Внутри декоратора определяется функция `wrapper`, которая принимает произвольные аргументы `*args` и `**kwargs`.
3.  Функция `wrapper` выполняет цикл `for` от `0` до `retries`.
4.  Внутри цикла `try` вызывается функция `func` с аргументами `*args` и `**kwargs`. Если вызов успешен, `wrapper` возвращает результат вызова.
5.  Если во время вызова `func` возникает исключение, которое есть в списке `exceptions`, оно перехватывается.
6.  Внутри блока `except` исключение логируется с помощью `logger.debug`.
7.  Проверяется, является ли текущая итерация последней попыткой. Если да, исключение генерируется повторно.
8.  Если это не последняя попытка, логируется сообщение о повторной попытке, и цикл продолжается.
9.  Если исключение не возникло, функция `func` возвращает результат, и цикл завершается.

**Примеры**:

```python
from src.logger import logger
# Пример использования декоратора для повтора функции при ошибке ConnectionError
@repeat_on_error(retries=3, exceptions=[ConnectionError])
def connect_to_server():
    """Подключается к серверу."""
    print("Попытка подключения к серверу...")
    # Имитация ошибки подключения на первой попытке
    if connect_to_server.counter < 2:
        connect_to_server.counter += 1
        raise ConnectionError("Не удалось подключиться к серверу.")
    else:
        print("Успешное подключение к серверу!")
        return True
connect_to_server.counter = 0

# Вызов функции, которая будет повторяться при ошибке
result = connect_to_server()
print(result)

# Пример использования декоратора для повтора функции при нескольких типах ошибок
@repeat_on_error(retries=2, exceptions=[ValueError, TypeError])
def process_data(data):
    """Обрабатывает данные."""
    if not isinstance(data, int):
        raise TypeError("Данные должны быть числом.")
    if data < 0:
        raise ValueError("Данные должны быть положительными.")
    return data * 2

# Вызов функции, которая может вызывать разные типы исключений
try:
    result = process_data("abc")
    print(result)
except Exception as ex:
    logger.error(f"Произошла ошибка: {ex}", ex, exc_info=True)
```

### `add_rai_template_variables_if_enabled`

```python
def add_rai_template_variables_if_enabled(template_variables: dict) -> dict:
    """
    Adds the RAI template variables to the specified dictionary, if the RAI disclaimers are enabled.
    These can be configured in the config.ini file. If enabled, the variables will then load the RAI disclaimers from the 
    appropriate files in the prompts directory. Otherwise, the variables will be set to None.

    Args:
        template_variables (dict): The dictionary of template variables to add the RAI variables to.

    Returns:
        dict: The updated dictionary of template variables.
    """
```

**Назначение**:
Добавляет переменные шаблона RAI (Responsible AI) в указанный словарь, если включены соответствующие дисклеймеры RAI.
Эти параметры можно настроить в файле `config.ini`. Если они включены, переменные будут загружать дисклеймеры RAI
из соответствующих файлов в каталоге `prompts`. В противном случае переменные будут установлены в `None`.

**Параметры**:

*   `template_variables` (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

**Возвращает**:

*   `dict`: Обновленный словарь переменных шаблона.

**Как работает функция**:

1.  Импортирует модуль `config` из `tinytroupe` для доступа к настройкам конфигурации.
2.  Считывает значения настроек `RAI_HARMFUL_CONTENT_PREVENTION` и `RAI_COPYRIGHT_INFRINGEMENT_PREVENTION` из файла `config.ini`.
3.  Определяет пути к файлам с дисклеймерами RAI для предотвращения вредоносного контента и нарушения авторских прав.
4.  Считывает содержимое файлов с дисклеймерами, если соответствующие настройки включены.
5.  Добавляет переменные `rai_harmful_content_prevention` и `rai_copyright_infringement_prevention` в словарь `template_variables`,
    устанавливая их в содержимое файлов с дисклеймерами или в `None`, в зависимости от значений настроек.
6.  Возвращает обновленный словарь `template_variables`.

**Примеры**:

```python
# Пример использования функции с включенными настройками RAI
template_variables = {}
updated_variables = add_rai_template_variables_if_enabled(template_variables)
print(updated_variables)
# {'rai_harmful_content_prevention': 'Содержимое дисклеймера о вредоносном контенте', 'rai_copyright_infringement_prevention': 'Содержимое дисклеймера о нарушении авторских прав'}

# Пример использования функции с выключенными настройками RAI
# (предполагается, что в config.ini RAI_HARMFUL_CONTENT_PREVENTION и RAI_COPYRIGHT_INFRINGEMENT_PREVENTION установлены в False)
template_variables = {}
updated_variables = add_rai_template_variables_if_enabled(template_variables)
print(updated_variables)
# {'rai_harmful_content_prevention': None, 'rai_copyright_infringement_prevention': None}
```

### `truncate_actions_or_stimuli`

```python
def truncate_actions_or_stimuli(list_of_actions_or_stimuli: Collection[dict], max_content_length: int) -> Collection[str]:
    """
    Truncates the content of actions or stimuli at the specified maximum length. Does not modify the original list.

    Args:
        list_of_actions_or_stimuli (Collection[dict]): The list of actions or stimuli to truncate.
        max_content_length (int): The maximum length of the content.

    Returns:
        Collection[str]: The truncated list of actions or stimuli. It is a new list, not a reference to the original list, 
        to avoid unexpected side effects.
    """
```

**Назначение**:
Усекает содержимое действий или стимулов до указанной максимальной длины. Не изменяет исходный список.

**Параметры**:

*   `list_of_actions_or_stimuli` (Collection[dict]): Список действий или стимулов для усечения.
*   `max_content_length` (int): Максимальная длина содержимого.

**Возвращает**:

*   `Collection[str]`: Усеченный список действий или стимулов. Это новый список, а не ссылка на исходный список,
    чтобы избежать неожиданных побочных эффектов.

**Как работает функция**:

1.  Создает глубокую копию входного списка `list_of_actions_or_stimuli`, чтобы избежать изменения исходного списка.
2.  Перебирает элементы в клонированном списке.
3.  Для каждого элемента проверяет, содержит ли он ключ `"content"`. Если да, то получает содержимое сообщения.
4.  Проверяет, содержит ли содержимое сообщения ключи `"action"`, `"stimulus"` или `"stimuli"`.
5.  Если найден ключ `"action"` или `"stimulus"`, проверяет наличие ключа `"content"` внутри соответствующего словаря и усекает его значение с помощью функции `break_text_at_length`.
6.  Если найден ключ `"stimuli"`, перебирает элементы списка стимулов и усекает значение ключа `"content"` каждого стимула с помощью функции `break_text_at_length`.
7.  Возвращает клонированный список с усеченным содержимым.

**Примеры**:

```python
from tinytroupe.utils.rendering import break_text_at_length
# Пример усечения списка действий
actions = [{"role": "user", "content": {"action": {"content": "This is a long action description."}}},
           {"role": "system", "content": {"action": {"content": "Another long action description."}}}]
truncated_actions = truncate_actions_or_stimuli(actions, 20)
print(truncated_actions)
# [{'role': 'user', 'content': {'action': {'content': 'This is a long act...'}}}, {'role': 'system', 'content': {'action': {'content': 'Another long actio...'}}}]

# Пример усечения списка стимулов
stimuli = [{"role": "user", "content": {"stimulus": {"content": "This is a long stimulus description."}}},
           {"role": "system", "content": {"stimulus": {"content": "Another long stimulus description."}}}]
truncated_stimuli = truncate_actions_or_stimuli(stimuli, 20)
print(truncated_stimuli)
# [{'role': 'user', 'content': {'stimulus': {'content': 'This is a long stim...'}}}, {'role': 'system', 'content': {'stimulus': {'content': 'Another long stimu...'}}}]

# Пример усечения списка стимулов с несколькими элементами
stimuli = [{"role": "user", "content": {"stimuli": [{"content": "This is a long stimulus 1."}, {"content": "This is a long stimulus 2."}]}}]
truncated_stimuli = truncate_actions_or_stimuli(stimuli, 20)
print(truncated_stimuli)
# [{'role': 'user', 'content': {'stimuli': [{'content': 'This is a long stim...'}, {'content': 'This is a long stim...'}]}}]