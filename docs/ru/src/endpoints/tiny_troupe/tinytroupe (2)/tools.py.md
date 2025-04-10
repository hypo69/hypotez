# Модуль `tools`

## Обзор

Модуль содержит инструменты, позволяющие агентам выполнять специализированные задачи.

## Подробнее

Этот модуль определяет базовый класс `TinyTool`, от которого наследуются другие инструменты, такие как `TinyCalendar` и `TinyWordProcessor`. Инструменты позволяют агентам выполнять различные действия, такие как ведение календаря или обработка текста. Модуль использует логирование для отслеживания работы инструментов и обработки ошибок.

## Классы

### `TinyTool`

**Описание**: Базовый класс для всех инструментов.

**Принцип работы**:
Класс `TinyTool` является абстрактным базовым классом для создания инструментов, доступных агентам. Он определяет общие атрибуты и методы, такие как имя, описание, владельца, наличие побочных эффектов в реальном мире, экспортер и обогатитель. Класс также содержит методы для защиты от реальных побочных эффектов и принудительного определения владельца инструмента.

**Атрибуты**:

- `name` (str): Имя инструмента.
- `description` (str): Краткое описание инструмента.
- `owner` (str): Агент, владеющий инструментом. Если `None`, инструмент может использоваться любым агентом.
- `real_world_side_effects` (bool): Указывает, имеет ли инструмент побочные эффекты в реальном мире.
- `exporter` (ArtifactExporter): Экспортер для экспорта результатов работы инструмента.
- `enricher` (TinyEnricher): Обогатитель для обогащения результатов работы инструмента.

**Методы**:

- `__init__(self, name: str, description: str, owner: str = None, real_world_side_effects: bool = False, exporter: ArtifactExporter = None, enricher: TinyEnricher = None)`:
    ```python
    def __init__(self, name: str, description: str, owner: str = None, real_world_side_effects: bool = False, exporter: ArtifactExporter = None, enricher: TinyEnricher = None):
        """
        Инициализирует новый инструмент.

        Args:
            name (str): Имя инструмента.
            description (str): Краткое описание инструмента.
            owner (str): Агент, владеющий инструментом. Если None, инструмент может использоваться любым агентом.
            real_world_side_effects (bool): Указывает, имеет ли инструмент побочные эффекты в реальном мире.
            exporter (ArtifactExporter): Экспортер для экспорта результатов работы инструмента. Если None, инструмент не сможет экспортировать результаты.
            enricher (TinyEnricher): Обогатитель для обогащения результатов работы инструмента. Если None, инструмент не сможет обогащать результаты.
        """
    ```
- `_process_action(self, agent, action: dict) -> bool`:
    ```python
    def _process_action(self, agent, action: dict) -> bool:
        """
        Обрабатывает действие агента.

        Args:
            agent: Агент, выполняющий действие.
            action (dict): Словарь, представляющий действие.

        Returns:
            bool: True, если действие было успешно обработано, иначе False.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```
- `_protect_real_world(self)`:
    ```python
    def _protect_real_world(self):
        """
        Предупреждает о реальных побочных эффектах инструмента.
        """
    ```
- `_enforce_ownership(self, agent)`:
    ```python
    def _enforce_ownership(self, agent):
        """
        Проверяет, имеет ли агент право на использование инструмента.

        Args:
            agent: Агент, пытающийся использовать инструмент.

        Raises:
            ValueError: Если агент не является владельцем инструмента.
        """
    ```
- `set_owner(self, owner)`:
    ```python
    def set_owner(self, owner):
        """
        Устанавливает владельца инструмента.

        Args:
            owner: Новый владелец инструмента.
        """
    ```
- `actions_definitions_prompt(self) -> str`:
    ```python
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения возможных действий инструмента.

        Returns:
            str: Prompt для определения возможных действий.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```
- `actions_constraints_prompt(self) -> str`:
    ```python
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия инструмента.

        Returns:
            str: Prompt для определения ограничений на действия.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```
- `process_action(self, agent, action: dict) -> bool`:
    ```python
    def process_action(self, agent, action: dict) -> bool:
        """
        Обрабатывает действие агента, проверяя наличие побочных эффектов и владельца.

        Args:
            agent: Агент, выполняющий действие.
            action (dict): Словарь, представляющий действие.

        Returns:
            bool: True, если действие было успешно обработано, иначе False.
        """
    ```

### `TinyCalendar`

**Описание**: Инструмент для ведения календаря.

**Наследует**:
`TinyTool`

**Принцип работы**:
Класс `TinyCalendar` позволяет агентам добавлять и находить события в календаре. Каждое событие содержит такую информацию, как название, описание, владельца, обязательных и необязательных участников, время начала и окончания. Календарь представляет собой словарь, где ключом является дата, а значением - список событий.

**Атрибуты**:

- `calendar` (dict): Словарь, отображающий дату на список событий.

**Методы**:

- `__init__(self, owner: str = None)`:
    ```python
    def __init__(self, owner: str = None):
        """
        Инициализирует новый календарь.

        Args:
            owner (str): Владелец календаря.
        """
    ```
- `add_event(self, date, title, description: str = None, owner: str = None, mandatory_attendees: str = None, optional_attendees: str = None, start_time: str = None, end_time: str = None)`:
    ```python
    def add_event(self, date, title, description: str = None, owner: str = None, mandatory_attendees: str = None, optional_attendees: str = None, start_time: str = None, end_time: str = None):
        """
        Добавляет новое событие в календарь.

        Args:
            date: Дата события.
            title: Название события.
            description (str, optional): Описание события. По умолчанию None.
            owner (str, optional): Владелец события. По умолчанию None.
            mandatory_attendees (str, optional): Список обязательных участников. По умолчанию None.
            optional_attendees (str, optional): Список необязательных участников. По умолчанию None.
            start_time (str, optional): Время начала события. По умолчанию None.
            end_time (str, optional): Время окончания события. По умолчанию None.
        """
    ```
- `find_events(self, year, month, day, hour: str = None, minute: str = None)`:
    ```python
    def find_events(self, year, month, day, hour: str = None, minute: str = None):
        """
        Находит события в календаре по указанным параметрам.

        Args:
            year: Год события.
            month: Месяц события.
            day: День события.
            hour (str, optional): Час события. По умолчанию None.
            minute (str, optional): Минута события. По умолчанию None.
        """
    ```
- `_process_action(self, agent, action) -> bool`:
    ```python
    def _process_action(self, agent, action) -> bool:
        """
        Обрабатывает действие агента, связанное с календарем.

        Args:
            agent: Агент, выполняющий действие.
            action: Словарь, представляющий действие.

        Returns:
            bool: True, если действие было успешно обработано, иначе False.
        """
    ```
- `actions_definitions_prompt(self) -> str`:
    ```python
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения возможных действий с календарем.

        Returns:
            str: Prompt для определения возможных действий.
        """
    ```
- `actions_constraints_prompt(self) -> str`:
    ```python
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия с календарем.

        Returns:
            str: Prompt для определения ограничений на действия.
        """
    ```

### `TinyWordProcessor`

**Описание**: Инструмент для обработки текста.

**Наследует**:
`TinyTool`

**Принцип работы**:
Класс `TinyWordProcessor` позволяет агентам создавать и экспортировать текстовые документы. Он использует обогатитель (`enricher`) для расширения содержания документа и экспортер (`exporter`) для сохранения документа в различных форматах (например, Markdown, DOCX, JSON).

**Атрибуты**:

- Нет специфичных атрибутов, кроме тех, что наследуются от `TinyTool`.

**Методы**:

- `__init__(self, owner: str = None, exporter: ArtifactExporter = None, enricher: TinyEnricher = None)`:
    ```python
    def __init__(self, owner: str = None, exporter: ArtifactExporter = None, enricher: TinyEnricher = None):
        """
        Инициализирует новый текстовый процессор.

        Args:
            owner (str, optional): Владелец текстового процессора. По умолчанию None.
            exporter (ArtifactExporter, optional): Экспортер для экспорта документов. По умолчанию None.
            enricher (TinyEnricher, optional): Обогатитель для обогащения документов. По умолчанию None.
        """
    ```
- `write_document(self, title, content, author: str = None)`:
    ```python
    def write_document(self, title, content, author: str = None):
        """
        Создает и экспортирует текстовый документ.

        Args:
            title: Название документа.
            content: Содержание документа.
            author (str, optional): Автор документа. По умолчанию None.
        """
    ```
- `_process_action(self, agent, action) -> bool`:
    ```python
    def _process_action(self, agent, action) -> bool:
        """
        Обрабатывает действие агента, связанное с обработкой текста.

        Args:
            agent: Агент, выполняющий действие.
            action: Словарь, представляющий действие.

        Returns:
            bool: True, если действие было успешно обработано, иначе False.
        """
    ```
- `actions_definitions_prompt(self) -> str`:
    ```python
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения возможных действий с текстовым процессором.

        Returns:
            str: Prompt для определения возможных действий.
        """
    ```
- `actions_constraints_prompt(self) -> str`:
    ```python
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия с текстовым процессором.

        Returns:
            str: Prompt для определения ограничений на действия.
        """
    ```

## Функции

В данном модуле нет отдельных функций, только методы классов.