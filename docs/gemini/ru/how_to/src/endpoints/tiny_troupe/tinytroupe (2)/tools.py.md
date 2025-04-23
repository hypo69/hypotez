Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода содержит определения классов `TinyTool`, `TinyCalendar` и `TinyWordProcessor`, предназначенных для моделирования инструментов, используемых агентами в некоторой среде (например, в симуляции). `TinyTool` является базовым классом для создания инструментов, а `TinyCalendar` и `TinyWordProcessor` - это примеры конкретных инструментов: календарь и текстовый процессор, соответственно.

Шаги выполнения
-------------------------
1. **Определение класса `TinyTool`**:
   - Определяется базовый класс `TinyTool`, который служит основой для создания других инструментов.
   - В конструкторе `__init__` инициализируются основные атрибуты инструмента, такие как имя, описание, владелец, наличие побочных эффектов в реальном мире, экспортер и обогатитель.
   - Методы `_process_action`, `_protect_real_world`, `_enforce_ownership`, `set_owner`, `actions_definitions_prompt` и `actions_constraints_prompt` определяются как абстрактные методы, которые должны быть реализованы в подклассах.
   - Метод `process_action` обеспечивает выполнение действий инструмента с учетом защиты от реальных побочных эффектов и проверки прав собственности.

2. **Определение класса `TinyCalendar`**:
   - Определяется класс `TinyCalendar`, наследующийся от `TinyTool`, представляющий собой инструмент для работы с календарем.
   - В конструкторе `__init__` инициализируется календарь как словарь, где ключами являются даты, а значениями - списки событий.
   - Метод `add_event` добавляет новое событие в календарь.
   - Метод `find_events` предназначен для поиска событий в календаре (реализация не завершена).
   - Метод `_process_action` обрабатывает действия, связанные с календарем, такие как создание событий.
   - Методы `actions_definitions_prompt` и `actions_constraints_prompt` возвращают текстовые описания действий и ограничений для использования инструмента.

3. **Определение класса `TinyWordProcessor`**:
   - Определяется класс `TinyWordProcessor`, наследующийся от `TinyTool`, представляющий собой инструмент для работы с текстовыми документами.
   - В конструкторе `__init__` инициализируются атрибуты, специфичные для текстового процессора.
   - Метод `write_document` создает новый документ с заданным заголовком и содержанием, обогащая и экспортируя его при необходимости.
   - Метод `_process_action` обрабатывает действия, связанные с текстовым процессором, такие как создание документов.
   - Методы `actions_definitions_prompt` и `actions_constraints_prompt` возвращают текстовые описания действий и ограничений для использования инструмента.

Пример использования
-------------------------

```python
import logging
from tinytroupe.tools import TinyCalendar, TinyWordProcessor
from tinytroupe.extraction import ArtifactExporter
from tinytroupe.enrichment import TinyEnricher

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("tinytroupe")

# Пример использования TinyCalendar
calendar = TinyCalendar(owner="Иван")
calendar.add_event(date="2024-01-01", title="Новый год", description="Празднование нового года")
print(calendar.calendar)

# Пример использования TinyWordProcessor
exporter = ArtifactExporter(output_dir="output")
enricher = TinyEnricher(openai_api_key="your_api_key")
wordprocessor = TinyWordProcessor(owner="Иван", exporter=exporter, enricher=enricher)
wordprocessor.write_document(title="Отчет", content="Содержание отчета", author="Иван")

# Пример обработки действия для TinyWordProcessor
action = {
    'type': 'WRITE_DOCUMENT',
    'content': {
        'title': 'Новый документ',
        'content': 'Текст документа',
        'author': 'Иван'
    }
}
wordprocessor._process_action(agent=None, action=action)