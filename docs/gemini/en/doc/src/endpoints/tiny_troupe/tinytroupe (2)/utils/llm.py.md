# Module for working with Large Language Models (LLMs)
=====================================================

The `llm.py` module provides tools and utilities for interacting with LLMs, including model input and output handling, prompt engineering, and truncation of actions/stimuli.

## Table of Contents

- [LLM Input Utilities](#llm-input-utilities)
    - [`compose_initial_LLM_messages_with_templates()`](#compose_initial_llm_messages_with_templates)
    - [`llm()`](#llm)
- [LLM Output Utilities](#llm-output-utilities)
    - [`extract_json()`](#extract_json)
    - [`extract_code_block()`](#extract_code_block)
- [Model Control Utilities](#model-control-utilities)
    - [`repeat_on_error()`](#repeat_on_error)
- [Prompt Engineering](#prompt-engineering)
    - [`add_rai_template_variables_if_enabled()`](#add_rai_template_variables_if_enabled)
- [Truncation](#truncation)
    - [`truncate_actions_or_stimuli()`](#truncate_actions_or_stimuli)


## LLM Input Utilities

### `compose_initial_LLM_messages_with_templates()`

**Purpose**: Собирает начальные сообщения для вызова модели LLM, предполагая, что всегда используется системное сообщение (общее описание задачи) и дополнительное сообщение пользователя (специфическое описание задачи). Эти сообщения создаются с использованием заданных шаблонов и конфигураций рендеринга.

**Parameters**:

- `system_template_name` (str): Имя шаблона для системного сообщения.
- `user_template_name` (str, optional): Имя шаблона для сообщения пользователя. По умолчанию - None.
- `base_module_folder` (str, optional): Путь к базовому каталогу модуля. По умолчанию - None.
- `rendering_configs` (dict, optional): Конфигурации рендеринга. По умолчанию - {}.

**Returns**:

- list: Список сообщений для модели LLM.


### `llm()`

**Purpose**: Декоратор, который превращает декорированную функцию в функцию, основанную на LLM. Декорированная функция должна возвращать строку (инструкцию для LLM) или использовать параметры функции в качестве инструкции для LLM. Ответ LLM преобразуется к типу возвращаемого значения аннотации функции, если таковой есть.

**Usage Example**:

```python
@llm(model="gpt-4-0613", temperature=0.5, max_tokens=100)
def joke():
    return "Tell me a joke."
```


## LLM Output Utilities

### `extract_json()`

**Purpose**: Извлекает объект JSON из строки, игнорируя: любой текст перед первой открывающейся фигурной скобкой; и любые теги открытия (```json) или закрытия (```) Markdown.

**Parameters**:

- `text` (str): Строка, из которой нужно извлечь JSON-объект.

**Returns**:

- dict: Парсированный объект JSON.

**Raises Exceptions**:

- `Exception`: Если во время извлечения JSON произошла ошибка.


### `extract_code_block()`

**Purpose**: Извлекает блок кода из строки, игнорируя любой текст перед первыми тремя обратными кавычками и любой текст после последних трех обратных кавычек.

**Parameters**:

- `text` (str): Строка, из которой нужно извлечь блок кода.

**Returns**:

- str: Извлеченный блок кода.

**Raises Exceptions**:

- `Exception`: Если во время извлечения блока кода произошла ошибка.


## Model Control Utilities

### `repeat_on_error()`

**Purpose**: Декоратор, который повторяет вызов указанной функции, если произойдет одно из указанных исключений, до достижения указанного количества повторов. Если это количество повторов превышено, исключение возбуждается. Если исключение не происходит, функция возвращает значение нормально.

**Parameters**:

- `retries` (int): Количество попыток повтора.
- `exceptions` (list): Список классов исключений для перехвата.

**Returns**:

- `function`: Декорированная функция.


## Prompt Engineering

### `add_rai_template_variables_if_enabled()`

**Purpose**: Добавляет переменные шаблона RAI в указанный словарь, если включены отказники RAI. Их можно настроить в файле config.ini. Если включены, переменные будут загружать отказники RAI из соответствующих файлов в каталоге prompts. В противном случае переменные будут установлены в None.

**Parameters**:

- `template_variables` (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

**Returns**:

- dict: Обновленный словарь переменных шаблона.


## Truncation

### `truncate_actions_or_stimuli()`

**Purpose**: Укорачивает содержимое действий или стимулов до указанной максимальной длины. Не изменяет исходный список.

**Parameters**:

- `list_of_actions_or_stimuli` (Collection[dict]): Список действий или стимулов для усечения.
- `max_content_length` (int): Максимальная длина содержимого.

**Returns**:

- Collection[str]: Усеченный список действий или стимулов. Это новый список, а не ссылка на исходный список, чтобы избежать непредвиденных побочных эффектов.