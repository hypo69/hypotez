# Модуль TinyTools

## Обзор

Модуль содержит набор инструментов для работы с TinyTroupe agents, позволяющий агентам выполнять специализированные задачи. Инструменты реализованы в виде класса `TinyTool`, который наследуется от `JsonSerializableRegistry`. 

## Подробней

Модуль TinyTools предоставляет инструменты, которые агенты могут использовать для выполнения различных задач. Каждый инструмент обладает специфическим функционалом и может иметь свои особенности.

Например, инструмент TinyCalendar позволяет агентам планировать встречи и события, TinyWordProcessor — создавать и редактировать документы.

Модуль TinyTools позволяет создавать инструменты с помощью класса `TinyTool`, который наследуется от `JsonSerializableRegistry`. Это позволяет сохранять и загружать инструменты в JSON-формате, обеспечивая удобство работы с ними.

## Классы

### `TinyTool`

**Описание**: Базовый класс для всех инструментов в TinyTroupe. 
**Наследует**: `JsonSerializableRegistry` 

**Атрибуты**:

- `name` (str): Имя инструмента.
- `description` (str): Краткое описание инструмента.
- `owner` (str): Владелец инструмента. 
- `real_world_side_effects` (bool): Флаг, указывающий, имеет ли инструмент реальные побочные эффекты.
- `exporter` (ArtifactExporter): Экспортер для экспорта результатов действий инструмента.
- `enricher` (Enricher): Обогатитель для обогащения результатов действий инструмента.

**Методы**:

- `_process_action(agent, action)`: Абстрактный метод, который должен быть переопределен в подклассах. Этот метод обрабатывает действия агента, которые связаны с инструментом.
- `_protect_real_world()`: Выводит предупреждение, если инструмент имеет реальные побочные эффекты.
- `_enforce_ownership(agent)`: Проверяет, является ли агент владельцем инструмента.
- `set_owner(owner)`: Устанавливает владельца инструмента.
- `actions_definitions_prompt()`: Возвращает подсказку с описанием доступных действий для инструмента.
- `actions_constraints_prompt()`: Возвращает подсказку с ограничениями на использование инструмента.
- `process_action(agent, action)`: Обрабатывает действие агента, проверяя права и выполняя соответствующую обработку.

### `TinyCalendar`

**Описание**: Базовый класс для календаря, который позволяет агентам отслеживать встречи и записи. 
**Наследует**: `TinyTool` 

**Атрибуты**:

- `calendar` (dict): Словарь, который отображает дату в список событий. Каждое событие — это словарь с ключами: "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time".

**Методы**:

- `add_event(date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Добавляет новое событие в календарь.
- `find_events(year, month, day, hour=None, minute=None)`: Находит события в календаре по дате и времени.
- `_process_action(agent, action)`: Обрабатывает действия агента, связанные с календарем.
- `actions_definitions_prompt()`: Возвращает подсказку с описанием доступных действий для календаря.
- `actions_constraints_prompt()`: Возвращает подсказку с ограничениями на использование календаря.

### `TinyWordProcessor`

**Описание**: Базовый класс для текстового процессора, который позволяет агентам создавать документы. 
**Наследует**: `TinyTool`

**Атрибуты**:

- `exporter` (ArtifactExporter): Экспортер для экспорта результатов действий инструмента.
- `enricher` (Enricher): Обогатитель для обогащения результатов действий инструмента.

**Методы**:

- `write_document(title, content, author=None)`: Создает новый документ с заданным названием, содержанием и автором. 
- `_process_action(agent, action)`: Обрабатывает действия агента, связанные с текстовым процессором.
- `actions_definitions_prompt()`: Возвращает подсказку с описанием доступных действий для текстового процессора.
- `actions_constraints_prompt()`: Возвращает подсказку с ограничениями на использование текстового процессора.

## Функции

## Параметры

## Примеры
```python
# Создание экземпляра TinyWordProcessor
word_processor = TinyWordProcessor(owner='Agent1')

# Создание документа
word_processor.write_document(title='My document', content='This is the content of the document.', author='Agent1')

# Создание экземпляра TinyCalendar
calendar = TinyCalendar(owner='Agent2')

# Добавление события в календарь
calendar.add_event(date='2024-03-10', title='Meeting with team', description='Discuss project progress', owner='Agent2')

# Вывод события
print(calendar.calendar)
```
```markdown