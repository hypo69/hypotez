# Модуль tiny_word_processor.py

## Обзор

Модуль `tiny_word_processor.py` предоставляет класс `TinyWordProcessor`, который является инструментом для создания и обработки текстовых документов. Он позволяет агентам (agents) писать документы, обогащать их контент и экспортировать в различные форматы. Модуль интегрируется с другими инструментами, такими как `enricher` (для обогащения контента) и `exporter` (для экспорта документов).

## Подробнее

Этот модуль предназначен для использования в системах, где требуется автоматическое создание и обработка текстовых документов. Класс `TinyWordProcessor` предоставляет основные функции для написания, обогащения и экспорта документов, что делает его полезным инструментом для автоматизации задач, связанных с созданием контента.

## Классы

### `TinyWordProcessor`

**Описание**: Класс `TinyWordProcessor` является инструментом для создания и обработки текстовых документов. Он наследует класс `TinyTool`.

**Наследует**:
- `TinyTool`: Предоставляет базовую функциональность для инструментов в системе.

**Атрибуты**:
- `name` (str): Имя инструмента ("wordprocessor").
- `description` (str): Описание инструмента ("A basic word processor tool that allows agents to write documents.").
- `owner` (Any): Владелец инструмента.
- `exporter` (Any): Инструмент для экспорта документов.
- `enricher` (Any): Инструмент для обогащения контента.
- `real_world_side_effects` (bool): Указывает, имеет ли инструмент побочные эффекты в реальном мире (в данном случае `False`).

**Методы**:
- `__init__(self, owner=None, exporter=None, enricher=None)`: Инициализирует экземпляр класса `TinyWordProcessor`.
- `write_document(self, title, content, author=None)`: Создает и экспортирует документ.
- `_process_action(self, agent, action)`: Обрабатывает действие агента, связанное с созданием документа.
- `actions_definitions_prompt(self)`: Возвращает строку с определениями действий, которые может выполнять инструмент.
- `actions_constraints_prompt(self)`: Возвращает строку с ограничениями на действия, которые может выполнять инструмент.

#### `__init__`

```python
def __init__(self, owner=None, exporter=None, enricher=None):
    """Инициализирует экземпляр класса TinyWordProcessor.

    Args:
        owner (Any, optional): Владелец инструмента. По умолчанию None.
        exporter (Any, optional): Инструмент для экспорта документов. По умолчанию None.
        enricher (Any, optional): Инструмент для обогащения контента. По умолчанию None.
    """
    ...
```

#### `write_document`

```python
def write_document(self, title, content, author=None):
    """Создает и экспортирует документ.

    Args:
        title (str): Заголовок документа.
        content (str): Содержимое документа.
        author (str, optional): Автор документа. По умолчанию None.
    """
    ...
```
- **Как работает функция**:
    - Записывает документ с заданным заголовком и содержимым.
    - Если указан `enricher`, обогащает контент документа, делая его более длинным и подробным.
    - Если указан `exporter`, экспортирует документ в форматах Markdown, DOCX и JSON.
    - Логирует процесс записи документа.
    
    **Внутренние функции**:
    - В данной функции отсутствуют внутренние функции.
    
- **Примеры**:
    ```python
    # Пример создания экземпляра класса TinyWordProcessor
    word_processor = TinyWordProcessor(exporter=exporter, enricher=enricher)

    # Пример вызова функции write_document
    word_processor.write_document(title="My Document", content="This is the content of my document.", author="John Doe")
    ```

#### `_process_action`

```python
def _process_action(self, agent, action) -> bool:
    """Обрабатывает действие агента, связанное с созданием документа.

    Args:
        agent (Any): Агент, выполняющий действие.
        action (dict): Словарь, содержащий информацию о действии.

    Returns:
        bool: True, если действие успешно обработано, иначе False.
    """
    ...
```
- **Как работает функция**:
    - Обрабатывает действие агента, проверяя, является ли оно типом "WRITE_DOCUMENT".
    - Извлекает содержимое документа из действия.
    - Проверяет наличие обязательных полей ("title", "content", "author").
    - Вызывает функцию `write_document` для создания и экспорта документа.
    - Обрабатывает исключения, связанные с парсингом JSON и общими ошибками.
    - Логирует ошибки, если они возникают.

    **Внутренние функции**:
    - В данной функции отсутствуют внутренние функции.

- **Примеры**:
    ```python
    # Пример вызова функции _process_action
    action = {"type": "WRITE_DOCUMENT", "content": '{"title": "My Document", "content": "This is the content.", "author": "John Doe"}'}
    result = word_processor._process_action(agent, action)
    print(result)  # Выведет: True или False в зависимости от успеха обработки
    ```

#### `actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """Возвращает строку с определениями действий, которые может выполнять инструмент.

    Returns:
        str: Строка с определениями действий.
    """
    ...
```
- **Как работает функция**:
    - Возвращает строку, описывающую действие "WRITE_DOCUMENT" и его параметры.
    - Указывает, что содержимое документа должно быть в формате JSON с полями "title", "content" и "author".
    - Использует `utils.dedent` для удаления лишних отступов в строке.

    **Внутренние функции**:
    - В данной функции отсутствуют внутренние функции.

- **Примеры**:
    ```python
    # Пример вызова функции actions_definitions_prompt
    prompt = word_processor.actions_definitions_prompt()
    print(prompt)
    ```

#### `actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """Возвращает строку с ограничениями на действия, которые может выполнять инструмент.

    Returns:
        str: Строка с ограничениями на действия.
    """
    ...
```
- **Как работает функция**:
    - Возвращает строку, описывающую ограничения на действие "WRITE_DOCUMENT".
    - Указывает, что содержимое должно быть длинным и подробным, если нет веских причин для обратного.
    - Требует, чтобы содержимое было в формате JSON с использованием правильных escape-последовательностей.
    - Рекомендует указывать конкретных владельцев или партнерские команды для упоминаемых вех или временных рамок.
    - Использует `utils.dedent` для удаления лишних отступов в строке.

    **Внутренние функции**:
    - В данной функции отсутствуют внутренние функции.

- **Примеры**:
    ```python
    # Пример вызова функции actions_constraints_prompt
    prompt = word_processor.actions_constraints_prompt()
    print(prompt)
    ```

## Методы класса

### `write_document`

**Назначение**: Создает и экспортирует документ с заданным заголовком, содержимым и автором.

**Параметры**:
- `title` (str): Заголовок документа.
- `content` (str): Содержимое документа.
- `author` (str, optional): Автор документа. По умолчанию `None`.

### `_process_action`

**Назначение**: Обрабатывает действие агента, связанное с созданием документа.

**Параметры**:
- `agent` (Any): Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

### `actions_definitions_prompt`

**Назначение**: Возвращает строку с определениями действий, которые может выполнять инструмент.

### `actions_constraints_prompt`

**Назначение**: Возвращает строку с ограничениями на действия, которые может выполнять инструмент.

## Параметры класса

- `owner` (Any, optional): Владелец инструмента. По умолчанию `None`.
- `exporter` (Any, optional): Инструмент для экспорта документов. По умолчанию `None`.
- `enricher` (Any, optional): Инструмент для обогащения контента. По умолчанию `None`.

## Примеры

```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
from tinytroupe.tools import logger

# Пример создания экземпляра класса TinyWordProcessor
word_processor = TinyWordProcessor()

# Пример вызова функции write_document
word_processor.write_document(title="My Document", content="This is the content of my document.", author="John Doe")

# Пример вызова функции _process_action
class MockAgent:
    pass

agent = MockAgent()
action = {"type": "WRITE_DOCUMENT", "content": '{"title": "My Document", "content": "This is the content.", "author": "John Doe"}'}
result = word_processor._process_action(agent, action)
print(result)

# Пример вызова функции actions_definitions_prompt
prompt = word_processor.actions_definitions_prompt()
print(prompt)

# Пример вызова функции actions_constraints_prompt
prompt = word_processor.actions_constraints_prompt()
print(prompt)