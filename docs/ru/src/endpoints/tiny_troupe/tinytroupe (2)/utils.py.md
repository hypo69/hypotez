# Модуль `utils`

## Обзор

Модуль содержит общие утилиты и вспомогательные функции, используемые в проекте `tinytroupe`. Включает функции для работы с текстовыми шаблонами, JSON, кодом, обработки исключений, валидации данных, prompt engineering, рендеринга, IO и конфигурационными файлами, а также классы для JSON сериализации и десериализации.

## Подробней

Этот модуль предоставляет набор инструментов для упрощения разработки и поддержки проекта `tinytroupe`. Он содержит функции для обработки входных и выходных данных моделей машинного обучения, управления их поведением, обеспечения безопасности и валидации данных, а также для работы с конфигурацией и логированием. Модуль также предоставляет классы для удобной сериализации и десериализации объектов в формат JSON.

## Функции

### `compose_initial_LLM_messages_with_templates`

```python
def compose_initial_LLM_messages_with_templates(system_template_name: str, user_template_name: str = None, rendering_configs: dict = {}) -> list:
    """
    Composes the initial messages for the LLM model call, under the assumption that it always involves 
    a system (overall task description) and an optional user message (specific task description). 
    These messages are composed using the specified templates and rendering configurations.
    """
```

**Назначение**: Формирует начальные сообщения для вызова LLM модели, предполагая, что всегда есть системное сообщение (общее описание задачи) и опциональное пользовательское сообщение (специфическое описание задачи). Эти сообщения формируются с использованием указанных шаблонов и конфигураций рендеринга.

**Параметры**:
- `system_template_name` (str): Имя файла шаблона для системного сообщения.
- `user_template_name` (str, optional): Имя файла шаблона для пользовательского сообщения. По умолчанию `None`.
- `rendering_configs` (dict, optional): Словарь с конфигурациями для рендеринга шаблонов. По умолчанию `{}`.

**Возвращает**:
- `list`: Список, содержащий сформированные сообщения для LLM модели.

**Как работает функция**:

1.  **Определение путей к шаблонам**: Определяются пути к файлам шаблонов системного и пользовательского сообщений на основе переданных имен шаблонов.
2.  **Инициализация списка сообщений**: Создается пустой список `messages`, который будет содержать сообщения для LLM.
3.  **Добавление системного сообщения**: Формируется системное сообщение с использованием шаблона и конфигураций рендеринга. Шаблон читается из файла, указанного в `system_prompt_template_path`, и рендерится с помощью библиотеки `chevron` с использованием `rendering_configs`. Результат добавляется в список `messages` с ролью "system".
4.  **Добавление пользовательского сообщения (опционально)**: Если указано имя файла шаблона для пользовательского сообщения (`user_template_name` не `None`), формируется пользовательское сообщение аналогично системному. Результат добавляется в список `messages` с ролью "user".
5.  **Возврат списка сообщений**: Функция возвращает список `messages`, содержащий сформированные сообщения для LLM.

**ASCII flowchart**:

```
A[Определение путей к шаблонам]
    |
    B[Инициализация списка сообщений]
    |
    C[Добавление системного сообщения]
    |
    D[Проверка наличия пользовательского сообщения]
    |
    E[Добавление пользовательского сообщения (если есть)]
    |
    F[Возврат списка сообщений]
```

**Примеры**:

```python
# Пример 1: С использованием только системного шаблона
messages = compose_initial_LLM_messages_with_templates("system_prompt.md", rendering_configs={"task": "Выполни задачу"})
print(messages)
# Вывод: [{'role': 'system', 'content': 'Сообщение из system_prompt.md с подставленной задачей: Выполни задачу'}]

# Пример 2: С использованием системного и пользовательского шаблонов
messages = compose_initial_LLM_messages_with_templates("system_prompt.md", "user_prompt.md", rendering_configs={"task": "Выполни задачу", "instruction": "Сделай это хорошо"})
print(messages)
# Вывод: [{'role': 'system', 'content': 'Сообщение из system_prompt.md с подставленной задачей: Выполни задачу'}, {'role': 'user', 'content': 'Сообщение из user_prompt.md с подставленной инструкцией: Сделай это хорошо'}]
```

### `extract_json`

```python
def extract_json(text: str) -> dict:
    """
    Extracts a JSON object from a string, ignoring: any text before the first 
    opening curly brace; and any Markdown opening (```json) or closing(```) tags.
    """
```

**Назначение**: Извлекает JSON объект из строки, игнорируя любой текст до первой открывающей фигурной скобки, а также Markdown теги открытия (````json) или закрытия (```).

**Параметры**:
- `text` (str): Строка, из которой нужно извлечь JSON объект.

**Возвращает**:
- `dict`: Словарь, представляющий извлеченный JSON объект. Возвращает пустой словарь `{}` в случае ошибки.

**Как работает функция**:

1.  **Удаление текста до первой открывающей скобки**: Используется регулярное выражение для удаления любого текста до первой открывающей фигурной или квадратной скобки.
2.  **Удаление текста после последней закрывающей скобки**: Используется регулярное выражение для удаления любого текста после последней закрывающей фигурной или квадратной скобки.
3.  **Удаление некорректных escape-последовательностей**: Заменяет `\\\'` на `\'`, чтобы исправить некорректные escape-последовательности.
4.  **Парсинг JSON**: Пытается распарсить полученную строку как JSON объект с помощью `json.loads()`.
5.  **Обработка исключений**: Если возникает исключение при парсинге JSON, возвращает пустой словарь `{}`.

**ASCII flowchart**:

```
A[Удаление текста до первой открывающей скобки]
    |
    B[Удаление текста после последней закрывающей скобки]
    |
    C[Удаление некорректных escape-последовательностей]
    |
    D[Парсинг JSON]
    |
    E[Обработка исключений]
    |
    F[Возврат JSON объекта или пустого словаря]
```

**Примеры**:

```python
# Пример 1: Извлечение JSON из строки с текстом до и после JSON
text = "Some text {\"key\": \"value\"} More text"
json_obj = extract_json(text)
print(json_obj)
# Вывод: {'key': 'value'}

# Пример 2: Извлечение JSON из строки с Markdown тегами
text = "```json\n{\"key\": \"value\"}\n```"
json_obj = extract_json(text)
print(json_obj)
# Вывод: {'key': 'value'}

# Пример 3: Обработка ошибки парсинга JSON
text = "Invalid JSON"
json_obj = extract_json(text)
print(json_obj)
# Вывод: {}
```

### `extract_code_block`

```python
def extract_code_block(text: str) -> str:
    """
    Extracts a code block from a string, ignoring any text before the first 
    opening triple backticks and any text after the closing triple backticks.
    """
```

**Назначение**: Извлекает блок кода из строки, игнорируя любой текст до первого открытия тройных обратных кавычек и любой текст после закрытия тройных обратных кавычек.

**Параметры**:
- `text` (str): Строка, из которой нужно извлечь блок кода.

**Возвращает**:
- `str`: Извлеченный блок кода. Возвращает пустую строку `""` в случае ошибки.

**Как работает функция**:

1.  **Удаление текста до первого открытия тройных обратных кавычек**: Используется регулярное выражение для удаления любого текста до первого открытия тройных обратных кавычек (```).
2.  **Удаление текста после последнего закрытия тройных обратных кавычек**: Используется регулярное выражение для удаления любого текста после последнего закрытия тройных обратных кавычек (```).
3.  **Обработка исключений**: Если возникает исключение, возвращает пустую строку `""`.

**ASCII flowchart**:

```
A[Удаление текста до первого открытия тройных обратных кавычек]
    |
    B[Удаление текста после последнего закрытия тройных обратных кавычек]
    |
    C[Обработка исключений]
    |
    D[Возврат блока кода или пустой строки]
```

**Примеры**:

```python
# Пример 1: Извлечение блока кода из строки с текстом до и после блока кода
text = "Some text ```python\nprint('Hello')\n``` More text"
code_block = extract_code_block(text)
print(code_block)
# Вывод: ```python\nprint('Hello')\n```

# Пример 2: Извлечение блока кода из строки без текста до и после блока кода
text = "```python\nprint('Hello')\n```"
code_block = extract_code_block(text)
print(code_block)
# Вывод: ```python\nprint('Hello')\n```

# Пример 3: Обработка случая, когда блок кода не найден
text = "Some text"
code_block = extract_code_block(text)
print(code_block)
# Вывод: ""
```

### `repeat_on_error`

```python
def repeat_on_error(retries: int, exceptions: list):
    """
    Decorator that repeats the specified function call if an exception among those specified occurs, 
    up to the specified number of retries. If that number of retries is exceeded, the
    exception is raised. If no exception occurs, the function returns normally.

    Args:
        retries (int): The number of retries to attempt.
        exceptions (list): The list of exception classes to catch.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as e:
                    logger.debug(f"Exception occurred: {e}")
                    if i == retries - 1:
                        raise e
                    else:
                        logger.debug(f"Retrying ({i+1}/{retries})...")
                        continue
        return wrapper
    return decorator
```

**Назначение**: Декоратор, который повторяет вызов указанной функции, если происходит исключение из указанного списка, до указанного количества повторных попыток. Если количество повторных попыток превышено, исключение выбрасывается. Если исключение не происходит, функция возвращается нормально.

**Параметры**:
- `retries` (int): Количество попыток повтора вызова функции.
- `exceptions` (list): Список классов исключений, которые нужно перехватывать.

**Как работает функция**:

1.  **Определение декоратора**: Определяется функция `decorator`, которая принимает функцию `func` в качестве аргумента.
2.  **Определение обертки**: Внутри `decorator` определяется функция `wrapper`, которая принимает произвольные аргументы и ключевые слова.
3.  **Цикл повторных попыток**: Функция `wrapper` выполняет цикл `for` от 0 до `retries`.
4.  **Вызов функции**: Внутри цикла `try` вызывается функция `func` с переданными аргументами и ключевыми словами. Если вызов успешен, функция возвращает результат.
5.  **Перехват исключений**: Если при вызове `func` возникает исключение, оно перехватывается блоком `except`. Проверяется, является ли исключение одним из указанных в списке `exceptions`.
6.  **Логирование исключения**: Если исключение перехвачено, оно логируется с уровнем `DEBUG` с использованием `logger.debug()`.
7.  **Повторный вызов или выброс исключения**: Если текущая итерация не последняя (`i != retries - 1`), то логируется сообщение о повторной попытке и цикл продолжается. Если это последняя итерация, исключение выбрасывается.

**ASCII flowchart**:

```
A[Определение декоратора]
    |
    B[Определение обертки]
    |
    C[Цикл повторных попыток]
    |
    D[Вызов функции]
    |
    E[Перехват исключений]
    |
    F[Логирование исключения]
    |
    G[Проверка последней итерации]
    |
    H[Повторный вызов или выброс исключения]
```

**Примеры**:

```python
from src.logger import logger # Из системной инструкции
# Пример 1: Повторный вызов функции при возникновении OSError
@repeat_on_error(retries=3, exceptions=[OSError])
def read_file(filename):
    with open(filename, "r") as f:
        return f.read()

# Пример 2: Повторный вызов функции при возникновении нескольких типов исключений
@repeat_on_error(retries=2, exceptions=[ValueError, TypeError])
def parse_data(data):
    if not isinstance(data, str):
        raise TypeError("Data must be a string")
    return int(data)
```

### `check_valid_fields`

```python
def check_valid_fields(obj: dict, valid_fields: list) -> None:
    """
    Checks whether the fields in the specified dict are valid, according to the list of valid fields. If not, raises a ValueError.
    """
```

**Назначение**: Проверяет, являются ли поля в указанном словаре допустимыми, согласно списку допустимых полей. Если нет, выбрасывает исключение `ValueError`.

**Параметры**:
- `obj` (dict): Словарь, поля которого нужно проверить.
- `valid_fields` (list): Список допустимых полей.

**Вызывает исключения**:
- `ValueError`: Если обнаружено недопустимое поле в словаре.

**Как работает функция**:

1.  **Итерация по ключам словаря**: Функция проходит по всем ключам в словаре `obj`.
2.  **Проверка допустимости поля**: Для каждого ключа проверяется, содержится ли он в списке допустимых полей `valid_fields`.
3.  **Выброс исключения**: Если ключ не найден в списке `valid_fields`, выбрасывается исключение `ValueError` с сообщением об ошибке, указывающим недопустимый ключ и список допустимых ключей.

**ASCII flowchart**:

```
A[Итерация по ключам словаря]
    |
    B[Проверка допустимости поля]
    |
    C[Выброс исключения (если поле недопустимо)]
```

**Примеры**:

```python
# Пример 1: Проверка словаря с допустимыми полями
obj = {"name": "John", "age": 30}
valid_fields = ["name", "age"]
check_valid_fields(obj, valid_fields)  # Не выбрасывает исключение

# Пример 2: Проверка словаря с недопустимым полем
obj = {"name": "John", "age": 30, "city": "New York"}
valid_fields = ["name", "age"]
try:
    check_valid_fields(obj, valid_fields)
except ValueError as ex:
    print(f"ValueError: {ex}")
# Вывод: ValueError: Invalid key city in dictionary. Valid keys are: ['name', 'age']
```

### `sanitize_raw_string`

```python
def sanitize_raw_string(value: str) -> str:
    """
    Sanitizes the specified string by: 
      - removing any invalid characters.
      - ensuring it is not longer than the maximum Python string length.
    
    This is for an abundance of caution with security, to avoid any potential issues with the string.
    """
```

**Назначение**: Очищает указанную строку, удаляя любые недопустимые символы и обеспечивая, чтобы она не была длиннее максимальной длины строки Python. Это делается для обеспечения безопасности и избежания потенциальных проблем со строкой.

**Параметры**:
- `value` (str): Строка, которую необходимо очистить.

**Возвращает**:
- `str`: Очищенная строка.

**Как работает функция**:

1.  **Удаление недопустимых символов**: Преобразует строку в кодировку UTF-8, игнорируя недопустимые символы, а затем декодирует обратно в UTF-8.
2.  **Обрезание строки**: Обрезает строку до максимальной длины строки Python (`sys.maxsize`).

**ASCII flowchart**:

```
A[Удаление недопустимых символов]
    |
    B[Обрезание строки]
    |
    C[Возврат очищенной строки]
```

**Примеры**:

```python
# Пример 1: Очистка строки с недопустимыми символами
value = "Hello\x00World"
sanitized_value = sanitize_raw_string(value)
print(sanitized_value)
# Вывод: HelloWorld

# Пример 2: Очистка длинной строки
value = "A" * (sys.maxsize + 100)
sanitized_value = sanitize_raw_string(value)
print(len(sanitized_value))
# Вывод: <максимальная длина строки Python>
```

### `sanitize_dict`

```python
def sanitize_dict(value: dict) -> dict:
    """
    Sanitizes the specified dictionary by:
      - removing any invalid characters.
      - ensuring that the dictionary is not too deeply nested.
    """
```

**Назначение**: Очищает указанный словарь, удаляя любые недопустимые символы и обеспечивая, чтобы словарь не был слишком глубоко вложенным.

**Параметры**:
- `value` (dict): Словарь, который необходимо очистить.

**Возвращает**:
- `dict`: Очищенный словарь.

**Как работает функция**:

1.  **Преобразование словаря в строку**: Преобразует словарь в JSON строку с помощью `json.dumps()`, отключая экранирование символов ASCII.
2.  **Очистка строки**: Очищает полученную строку с помощью функции `sanitize_raw_string()`.
3.  **Преобразование строки обратно в словарь**: Преобразует очищенную строку обратно в словарь с помощью `json.loads()`.

**ASCII flowchart**:

```
A[Преобразование словаря в строку]
    |
    B[Очистка строки]
    |
    C[Преобразование строки обратно в словарь]
    |
    D[Возврат очищенного словаря]
```

**Примеры**:

```python
# Пример 1: Очистка словаря с недопустимыми символами
value = {"name": "John\x00", "age": 30}
sanitized_value = sanitize_dict(value)
print(sanitized_value)
# Вывод: {'name': 'John', 'age': 30}

# Пример 2: Очистка словаря с глубокой вложенностью
value = {"level1": {"level2": {"level3": "value"}}}
sanitized_value = sanitize_dict(value)
print(sanitized_value)
# Вывод: {'level1': {'level2': {'level3': 'value'}}}
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

**Назначение**: Добавляет переменные шаблона RAI (Responsible AI) в указанный словарь, если включены соответствующие параметры в файле конфигурации `config.ini`. Если параметры включены, функция загружает текст дисклеймеров RAI из файлов в каталоге `prompts`. В противном случае переменные устанавливаются в `None`.

**Параметры**:
- `template_variables` (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

**Возвращает**:
- `dict`: Обновленный словарь переменных шаблона.

**Как работает функция**:

1.  **Чтение конфигурации**: Функция импортирует модуль `config` из `tinytroupe` (чтобы избежать циклического импорта) и считывает значения параметров `RAI_HARMFUL_CONTENT_PREVENTION` и `RAI_COPYRIGHT_INFRINGEMENT_PREVENTION` из секции `Simulation` файла `config.ini`.
2.  **Загрузка контента дисклеймера о вредоносном контенте**: Если параметр `RAI_HARMFUL_CONTENT_PREVENTION` включен, функция открывает файл `rai_harmful_content_prevention.md` из каталога `prompts`, считывает его содержимое и сохраняет его в переменную `rai_harmful_content_prevention_content`. В противном случае переменная устанавливается в `None`.
3.  **Добавление переменной в словарь**: Функция добавляет переменную `rai_harmful_content_prevention` в словарь `template_variables`, присваивая ей значение `rai_harmful_content_prevention_content` или `None` в зависимости от значения параметра конфигурации.
4.  **Загрузка контента дисклеймера о нарушении авторских прав**: Аналогично загрузке контента о вредоносном контенте, функция загружает содержимое файла `rai_copyright_infringement_prevention.md`, если включен параметр `RAI_COPYRIGHT_INFRINGEMENT_PREVENTION`, и добавляет переменную `rai_copyright_infringement_prevention` в словарь `template_variables`.
5.  **Возврат обновленного словаря**: Функция возвращает обновленный словарь `template_variables`.

**ASCII flowchart**:

```
A[Чтение конфигурации]
    |
    B[Загрузка контента дисклеймера о вредоносном контенте]
    |
    C[Добавление переменной в словарь]
    |
    D[Загрузка контента дисклеймера о нарушении авторских прав]
    |
    E[Добавление переменной в словарь]
    |
    F[Возврат обновленного словаря]
```

**Примеры**:

```python
from src.logger import logger # Из системной инструкции

# Пример 1: Добавление переменных RAI, когда они включены в config.ini
template_variables = {}
updated_variables = add_rai_template_variables_if_enabled(template_variables)
print(updated_variables)
# Вывод: {'rai_harmful_content_prevention': <содержимое rai_harmful_content_prevention.md>, 'rai_copyright_infringement_prevention': <содержимое rai_copyright_infringement_prevention.md>}

# Пример 2: Добавление переменных RAI, когда они отключены в config.ini
# (Предположим, что RAI_HARMFUL_CONTENT_PREVENTION и RAI_COPYRIGHT_INFRINGEMENT_PREVENTION установлены в False в config.ini)
template_variables = {}
updated_variables = add_rai_template_variables_if_enabled(template_variables)
print(updated_variables)
# Вывод: {'rai_harmful_content_prevention': None, 'rai_copyright_infringement_prevention': None}
```

### `inject_html_css_style_prefix`

```python
def inject_html_css_style_prefix(html, style_prefix_attributes):
    """
    Injects a style prefix to all style attributes in the given HTML string.

    For example, if you want to add a style prefix to all style attributes in the HTML string
    ``<div style="color: red;">Hello</div>``, you can use this function as follows:
    inject_html_css_style_prefix(\'<div style="color: red;">Hello</div>\', \'font-size: 20px;\')
    """
```

**Назначение**: Вставляет префикс стиля ко всем атрибутам `style` в заданной HTML строке.

**Параметры**:
- `html` (str): HTML строка, в которую нужно вставить префикс стиля.
- `style_prefix_attributes` (str): Префикс стиля, который нужно вставить.

**Возвращает**:
- `str`: HTML строка с вставленным префиксом стиля.

**Как работает функция**:

1.  **Замена атрибутов style**: Функция использует метод `replace()` для замены всех вхождений `style="` на `style="{style_prefix_attributes};`, где `{style_prefix_attributes}` - это переданный префикс стиля.

**ASCII flowchart**:

```
A[Замена атрибутов style]
    |
    B[Возврат HTML строки с префиксом стиля]
```

**Примеры**:

```python
# Пример 1: Вставка префикса стиля в HTML строку
html = '<div style="color: red;">Hello</div>'
style_prefix = 'font-size: 20px;'
result = inject_html_css_style_prefix(html, style_prefix)
print(result)
# Вывод: <div style="font-size: 20px;;color: red;">Hello</div>

# Пример 2: Вставка префикса стиля в HTML строку с несколькими атрибутами style
html = '<div style="color: red;"><p style="font-weight: bold;">Hello</p></div>'
style_prefix = 'font-size: 20px;'
result = inject_html_css_style_prefix(html, style_prefix)
print(result)
# Вывод: <div style="font-size: 20px;;color: red;"><p style="font-size: 20px;;font-weight: bold;">Hello</p></div>
```

### `break_text_at_length`

```python
def break_text_at_length(text: Union[str, dict], max_length: int = None) -> str:
    """
    Breaks the text (or JSON) at the specified length, inserting a "(...)" string at the break point.
    If the maximum length is `None`, the content is returned as is.
    """
```

**Назначение**: Обрезает текст (или JSON) до указанной длины, вставляя строку "(...)" в точке обрыва. Если максимальная длина равна `None`, контент возвращается как есть.

**Параметры**:
- `text` (str | dict): Текст или JSON, который нужно обрезать.
- `max_length` (int, optional): Максимальная длина текста. По умолчанию `None`.

**Возвращает**:
- `str`: Обрезанный текст с добавленной строкой "(...)" или исходный текст, если `max_length` равен `None` или длина текста меньше `max_length`.

**Как работает функция**:

1.  **Обработка JSON**: Если входной текст является словарем, он преобразуется в JSON строку с отступами.
2.  **Проверка максимальной длины**: Проверяется, является ли `max_length` равным `None` или длина текста меньше или равна `max_length`. Если это так, функция возвращает текст без изменений.
3.  **Обрезание текста**: Если `max_length` указана и длина текста больше `max_length`, функция обрезает текст до `max_length` и добавляет строку "(...)".

**ASCII flowchart**:

```
A[Обработка JSON (если текст - словарь)]
    |
    B[Проверка максимальной длины]
    |
    C[Обрезание текста (если необходимо)]
    |
    D[Возврат обрезанного или исходного текста]
```

**Примеры**:

```python
# Пример 1: Обрезание длинного текста
text = "This is a long text that needs to be broken at a certain length."
max_length = 20
result = break_text_at_length(text, max_length)
print(result)
# Вывод: This is a long text (...)

# Пример 2: Не обрезание текста, если он короче максимальной длины
text = "Short text"
max_length = 20
result = break_text_at_length(text, max_length)
print(result)
# Вывод: Short text

# Пример 3: Не обрезание текста, если max_length равен None
text = "Long text"
max_length = None
result = break_text_at_length(text, max_length)
print(result)
# Вывод: Long text

# Пример 4: Обрезание JSON
text = {"name": "John", "age": 30, "city": "New York"}
max_length = 50
result = break_text_at_length(text, max_length)
print(result)
# Вывод: {\n    "name": "John",\n    "age": 30,\n    "city": (...)
```

### `pretty_datetime`

```python
def pretty_datetime(dt: datetime) -> str:
    """
    Returns a pretty string representation of the specified datetime object.
    """
```

**Назначение**: Возвращает строковое представление указанного объекта `datetime` в формате "YYYY-MM-DD HH:MM".

**Параметры**:
- `dt` (datetime): Объект `datetime`, который нужно отформатировать.

**Возвращает**:
- `str`: Строковое представление объекта `datetime` в формате "YYYY-MM-DD HH:MM".

**Как работает функция**:

1.  **Форматирование datetime**: Функция использует метод `strftime()` объекта `datetime` для форматирования даты и времени в указанный формат.

**ASCII flowchart**:

```
A[Форматирование datetime]
    |
    B[Возврат отформатированной строки]
```

**Примеры**:

```python
from datetime import datetime

# Пример 1: Форматирование текущей даты и времени
dt = datetime.now()
result = pretty_datetime(dt)
print(result)
# Вывод: 2023-10-27 10:30 (пример)

# Пример 2: Форматирование заданной даты и времени
dt = datetime(2023, 12, 31, 23, 59)
result = pretty_datetime(dt)
print(result)
# Вывод: 2023-12-31 23:59
```

### `dedent`

```python
def dedent(text: str) -> str:
    """
    Dedents the specified text, removing any leading whitespace and identation.
    """
```

**Назначение**: Удаляет отступы из указанного текста, удаляя любые начальные пробелы и отступы.

**Параметры**:
- `text` (str): Текст, из которого нужно удалить отступы.

**Возвращает**:
- `str`: Текст без отступов.

**Как работает функция**:

1.  **Удаление отступов**: Функция использует `textwrap.dedent()` для удаления общего начального пробела из каждой строки в тексте.
2.  **Удаление начальных и конечных пробелов**: Функция использует `strip()` для удаления начальных и конечных пробелов из текста.

**ASCII flowchart**:

```
A[Удаление отступов]
    |
    B[Удаление начальных и конечных пробелов]
    |
    C[Возврат текста без отступов]
```

**Примеры**:

```python
# Пример 1: Удаление отступов из текста с начальными пробелами и отступами
text = "  Hello\n    World"
result = dedent(text)
print(result)
# Вывод: Hello\nWorld

# Пример 2: Удаление отступов из текста без начальных пробелов и отступов
text = "Hello\nWorld"
result = dedent(text)
print(result)
# Вывод: Hello\nWorld

# Пример 3: Удаление отступов из текста с конечными пробелами
text = "Hello  \nWorld  "
result = dedent(text)
print(result)
# Вывод: Hello\nWorld
```

### `read_config_file`

```python
def read_config_file(use_cache=True, verbose=True) -> configparser.ConfigParser:
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

        # Now, let\'s override any specific default value, if there's a custom .ini config. 
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
```

**Назначение**: Читает файл конфигурации `config.ini` и возвращает объект `configparser.ConfigParser`.

**Параметры**:
- `use_cache` (bool, optional): Определяет, использовать ли кэшированную конфигурацию, если она существует. По умолчанию `