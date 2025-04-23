# Модуль `tiny_word_processor.py`

## Обзор

Модуль предоставляет класс `TinyWordProcessor`, который является инструментом для создания и обработки текстовых документов. Этот инструмент позволяет агентам (agents) создавать документы с заданным заголовком, содержанием и автором. Он также предоставляет возможности для расширения и экспорта контента в различные форматы, такие как Markdown и JSON.

## Подробней

Модуль `tiny_word_processor.py` является частью проекта `hypotez` и предназначен для использования в задачах, где требуется автоматическое создание и управление текстовыми документами. Класс `TinyWordProcessor` наследуется от `TinyTool` и предоставляет функциональность для расширения, обработки и экспорта контента. Он интегрируется с другими инструментами, такими как `enricher` (для расширения контента) и `exporter` (для экспорта в различные форматы).

## Классы

### `TinyWordProcessor`

**Описание**: Класс `TinyWordProcessor` предоставляет инструменты для создания, обработки и экспорта текстовых документов.

**Наследует**: `TinyTool`

**Атрибуты**:
- `owner` (Any): Владелец инструмента.
- `exporter` (Any): Инструмент для экспорта документов в различные форматы.
- `enricher` (Any): Инструмент для расширения содержания документов.

**Методы**:
- `__init__(self, owner=None, exporter=None, enricher=None)`: Инициализирует экземпляр класса `TinyWordProcessor`.
- `write_document(self, title, content, author=None)`: Создает документ с заданным заголовком, содержанием и автором.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие агента, связанное с созданием документа.
- `actions_definitions_prompt(self) -> str`: Возвращает описание действий, которые может выполнять инструмент.
- `actions_constraints_prompt(self) -> str`: Возвращает ограничения на действия, выполняемые инструментом.

### `__init__(self, owner=None, exporter=None, enricher=None)`

**Назначение**: Инициализация экземпляра класса `TinyWordProcessor`.

**Параметры**:
- `owner` (Any, optional): Владелец инструмента. По умолчанию `None`.
- `exporter` (Any, optional): Инструмент для экспорта документов в различные форматы. По умолчанию `None`.
- `enricher` (Any, optional): Инструмент для расширения содержания документов. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор базового класса `TinyTool` с указанием имени инструмента (`"wordprocessor"`), описания, владельца, флага `real_world_side_effects` (установлен в `False`) и инструментов `exporter` и `enricher`.

**Примеры**:
```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
word_processor = TinyWordProcessor(owner="SomeOwner", exporter="SomeExporter", enricher="SomeEnricher")
```

### `write_document(self, title, content, author=None)`

**Назначение**: Создает документ с заданным заголовком, содержанием и автором.

**Параметры**:
- `title` (str): Заголовок документа.
- `content` (str): Содержание документа.
- `author` (str, optional): Автор документа. По умолчанию `None`.

**Как работает функция**:
1. Логгирует процесс записи документа с указанием заголовка и содержания.
2. Если `enricher` (инструмент для расширения контента) предоставлен:
   - Определяет требования к расширению контента, указывая, что результат должен быть как минимум в 5 раз больше оригинала по количеству символов и должен включать таблицы, списки и другие элементы.
   - Вызывает метод `enrich_content` инструмента `enricher` для расширения контента.
3. Если `exporter` (инструмент для экспорта) предоставлен:
   - Формирует имя артефакта на основе заголовка и автора (если указан).
   - Вызывает метод `export` инструмента `exporter` для экспорта контента в форматах Markdown (`.md`), Word (`.docx`) и JSON.
   - Создает словарь `json_doc`, содержащий заголовок, содержание и автора документа, и экспортирует его в формате JSON.

**Примеры**:
```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
word_processor = TinyWordProcessor(exporter="SomeExporter", enricher="SomeEnricher")
word_processor.write_document(title="MyDocument", content="Some initial content", author="MySelf")
```

### `_process_action(self, agent, action) -> bool`

**Назначение**: Обрабатывает действие агента, связанное с созданием документа.

**Параметры**:
- `agent` (Any): Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: `True`, если действие успешно обработано, `False` в противном случае.

**Как работает функция**:
1. Проверяет, что тип действия (`action['type']`) равен `"WRITE_DOCUMENT"` и что содержание (`action['content']`) не `None`.
2. Пытается обработать действие:
   - Если содержание является строкой, пытается извлечь JSON из строки с помощью `utils.extract_json`.
   - Если содержание уже является словарем, использует его напрямую.
   - Проверяет наличие недопустимых ключей в словаре с помощью `utils.check_valid_fields`.
   - Вызывает метод `write_document` с использованием извлеченных параметров (`title`, `content`, `author`).
   - В случае успеха возвращает `True`.
3. Обрабатывает исключения:
   - `json.JSONDecodeError`: Логгирует ошибку разбора JSON и возвращает `False`.
   - `Exception`: Логгирует общую ошибку обработки действия и возвращает `False`.

**Примеры**:
```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
word_processor = TinyWordProcessor()
action = {"type": "WRITE_DOCUMENT", "content": '{"title": "TestDoc", "content": "TestContent", "author": "TestAuthor"}'}
result = word_processor._process_action(agent="SomeAgent", action=action)
```

### `actions_definitions_prompt(self) -> str`

**Назначение**: Возвращает описание действий, которые может выполнять инструмент.

**Возвращает**:
- `str`: Строка с описанием доступных действий, форматированная как подсказка для агента.

**Как работает функция**:
- Определяет строку `prompt`, содержащую описание действия `WRITE_DOCUMENT`.
- Использует `utils.dedent` для удаления общих начальных отступов в строке.
- Возвращает отформатированную строку с описанием действия.

**Примеры**:
```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
word_processor = TinyWordProcessor()
prompt = word_processor.actions_definitions_prompt()
print(prompt)
```

### `actions_constraints_prompt(self) -> str`

**Назначение**: Возвращает ограничения на действия, выполняемые инструментом.

**Возвращает**:
- `str`: Строка с описанием ограничений на действия, форматированная как подсказка для агента.

**Как работает функция**:
- Определяет строку `prompt`, содержащую ограничения на действие `WRITE_DOCUMENT`, такие как необходимость записи всего контента сразу, использование JSON для встраивания контента и следование дополнительным рекомендациям.
- Использует `utils.dedent` для удаления общих начальных отступов в строке.
- Возвращает отформатированную строку с описанием ограничений.

**Примеры**:
```python
from tinytroupe.tools.tiny_word_processor import TinyWordProcessor
word_processor = TinyWordProcessor()
prompt = word_processor.actions_constraints_prompt()
print(prompt)
```