# Модуль `tiny_word_processor.py`

## Обзор

Модуль предоставляет класс `TinyWordProcessor`, который является инструментом для обработки текстовых документов. Он позволяет агентам создавать, обогащать и экспортировать документы в различных форматах, таких как Markdown и JSON.

## Подробней

Этот модуль является частью системы `tinytroupe` и предоставляет функциональность для создания и обработки текстовых документов. Он использует другие модули, такие как `logger` для ведения логов, `TinyTool` в качестве базового класса для инструментов, `utils` для различных утилитных функций, а также `exporter` и `enricher` для экспорта и обогащения контента.

## Классы

### `TinyWordProcessor`

**Описание**: Класс `TinyWordProcessor` предоставляет инструменты для создания, обогащения и экспорта текстовых документов.

**Наследует**:
- `TinyTool`: Класс `TinyWordProcessor` наследует от класса `TinyTool` и расширяет его функциональность для обработки текстовых документов.

**Атрибуты**:
- `owner` (Optional[Any]): Владелец инструмента.
- `exporter` (Optional[Any]): Инструмент для экспорта документов.
- `enricher` (Optional[Any]): Инструмент для обогащения контента документов.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `TinyWordProcessor`.
- `write_document`: Создает и экспортирует документ с заданным заголовком и содержанием.
- `_process_action`: Обрабатывает действие агента, связанное с созданием документа.
- `actions_definitions_prompt`: Возвращает подсказку с определениями действий, которые может выполнять агент.
- `actions_constraints_prompt`: Возвращает подсказку с ограничениями на действия, которые может выполнять агент.

#### `__init__`

```python
def __init__(self, owner=None, exporter=None, enricher=None):
    """Инициализирует экземпляр класса `TinyWordProcessor`.

    Args:
        owner (Optional[Any], optional): Владелец инструмента. По умолчанию `None`.
        exporter (Optional[Any], optional): Инструмент для экспорта документов. По умолчанию `None`.
        enricher (Optional[Any], optional): Инструмент для обогащения контента документов. По умолчанию `None`.

    Returns:
        None
    """
    ...
```

**Назначение**: Инициализирует объект `TinyWordProcessor` с заданными параметрами.

**Параметры**:
- `owner` (Any, optional): Владелец инструмента. По умолчанию `None`.
- `exporter` (Any, optional): Инструмент для экспорта документов. По умолчанию `None`.
- `enricher` (Any, optional): Инструмент для обогащения контента документов. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `TinyTool` с заданными параметрами.
- Устанавливает значения атрибутов `owner`, `exporter` и `enricher`.

**Примеры**:

```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
from tinytroupe.tools.exporter import Exporter
from tinytroupe.tools.enricher import Enricher

exporter = Exporter()
enricher = Enricher()
word_processor = TinyWordProcessor(owner="agent1", exporter=exporter, enricher=enricher)
```

#### `write_document`

```python
def write_document(self, title: str, content: str, author: Optional[str] = None) -> None:
    """Создает и экспортирует документ с заданным заголовком и содержанием.

    Args:
        title (str): Заголовок документа.
        content (str): Содержание документа.
        author (Optional[str], optional): Автор документа. По умолчанию `None`.

    Returns:
        None
    """
    ...
```

**Назначение**: Создает и экспортирует документ с заданным заголовком, содержанием и автором.

**Параметры**:
- `title` (str): Заголовок документа.
- `content` (str): Содержание документа.
- `author` (str, optional): Автор документа. По умолчанию `None`.

**Как работает функция**:
1. Логирует отладочное сообщение о создании документа.
2. Если задан `enricher`, обогащает контент документа, используя `enricher.enrich_content`.
3. Если задан `exporter`, экспортирует документ в форматах `md` и `json`, используя `exporter.export`.

**Примеры**:

```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
from tinytroupe.tools.exporter import Exporter
from tinytroupe.tools.enricher import Enricher

exporter = Exporter()
enricher = Enricher()
word_processor = TinyWordProcessor(exporter=exporter, enricher=enricher)
word_processor.write_document(title="MyDocument", content="This is the content.", author="John Doe")
```

#### `_process_action`

```python
def _process_action(self, agent: str, action: dict) -> bool:
    """Обрабатывает действие агента, связанное с созданием документа.

    Args:
        agent (str): Агент, выполняющий действие.
        action (dict): Словарь, описывающий действие.

    Returns:
        bool: `True`, если действие успешно обработано, `False` в противном случае.
    """
    ...
```

**Назначение**: Обрабатывает действие агента, связанное с созданием документа.

**Параметры**:
- `agent` (str): Агент, выполняющий действие.
- `action` (dict): Словарь, описывающий действие.

**Как работает функция**:
1. Проверяет, что тип действия - `WRITE_DOCUMENT` и контент не `None`.
2. Извлекает JSON из контента действия.
3. Проверяет, что все ключи в JSON валидны.
4. Вызывает `self.write_document` с параметрами из JSON.
5. Перехватывает исключения `json.JSONDecodeError` и `Exception` и логирует ошибки.

**Примеры**:

```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
from tinytroupe.tools.exporter import Exporter
from tinytroupe.tools.enricher import Enricher

exporter = Exporter()
enricher = Enricher()
word_processor = TinyWordProcessor(exporter=exporter, enricher=enricher)
action = {
    "type": "WRITE_DOCUMENT",
    "content": '{"title": "MyDocument", "content": "This is the content.", "author": "John Doe"}'
}
result = word_processor._process_action(agent="agent1", action=action)
print(result) #  True
```

#### `actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """Возвращает подсказку с определениями действий, которые может выполнять агент.

    Returns:
        str: Подсказка с определениями действий.
    """
    ...
```

**Назначение**: Возвращает подсказку с определениями действий, которые может выполнять агент.

**Как работает функция**:
- Определяет строку `prompt`, содержащую описание действия `WRITE_DOCUMENT` и его параметров.
- Использует `utils.dedent` для удаления лишних отступов в строке.
- Возвращает полученную строку.

**Примеры**:

```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor

word_processor = TinyWordProcessor()
prompt = word_processor.actions_definitions_prompt()
print(prompt)
```

#### `actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """Возвращает подсказку с ограничениями на действия, которые может выполнять агент.

    Returns:
        str: Подсказка с ограничениями на действия.
    """
    ...
```

**Назначение**: Возвращает подсказку с ограничениями на действия, которые может выполнять агент.

**Как работает функция**:
- Определяет строку `prompt`, содержащую ограничения на действие `WRITE_DOCUMENT`.
- Использует `utils.dedent` для удаления лишних отступов в строке.
- Возвращает полученную строку.

**Примеры**:

```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor

word_processor = TinyWordProcessor()
prompt = word_processor.actions_constraints_prompt()
print(prompt)
```