# Модуль agent.py

## Обзор

Модуль `agent.py` предоставляет основные классы и функции для создания и управления агентами TinyTroupe. Агенты представляют собой абстракции, имитирующие людей или сущности, взаимодействующие друг с другом и средой. В отличие от агентов, ориентированных на поддержку AI-ассистентов или других инструментов повышения производительности, агенты TinyTroupe стремятся представлять человеческое поведение, включая идиосинкразии, эмоции и другие человеческие черты. В основе лежит когнитивная психология, поэтому агенты имеют внутренние когнитивные состояния, такие как внимание, эмоции и цели, а также разделение памяти на эпизодическую и семантическую.

## Подробней

Модуль содержит классы для представления агентов (`TinyPerson`), их ментальных способностей (`TinyMentalFaculty`, `RecallFaculty`, `FilesAndWebGroundingFaculty`, `TinyToolUse`) и механизмов памяти (`TinyMemory`, `EpisodicMemory`, `SemanticMemory`).

## Классы

### `TinyPerson`

**Описание**:
Класс `TinyPerson` представляет собой симулированного персонажа во вселенной TinyTroupe.

**Принцип работы**:
Класс включает в себя методы для инициализации персонажа, определения его конфигурации, взаимодействия с окружением и другими агентами, управления памятью и ментальными способностями.

**Атрибуты**:
- `MAX_ACTIONS_BEFORE_DONE` (int): Максимальное количество действий, которое агент может выполнить до завершения.
- `PP_TEXT_WIDTH` (int): Ширина текста для pretty print.
- `serializable_attributes` (list): Список атрибутов, которые будут сериализованы при сохранении.
- `all_agents` (dict): Словарь всех созданных агентов (имя -> агент).
- `communication_style` (str): Стиль общения для всех агентов: "simplified" или "full".
- `communication_display` (bool): Флаг, определяющий, отображать ли общение.

**Методы**:
- `__init__(self, name: str = None, episodic_memory = None, semantic_memory = None, mental_faculties: list = None)`: Инициализирует экземпляр класса `TinyPerson`.
- `_post_init(self, **kwargs)`: Выполняет постобработку после инициализации, устанавливает значения по умолчанию для атрибутов.
- `generate_agent_prompt(self)`: Генерирует prompt для агента на основе mustache-шаблона.
- `reset_prompt(self)`: Сбрасывает текущий prompt агента, перечитывая шаблон и восстанавливая сообщения из памяти.
- `get(self, key)`: Возвращает значение из конфигурации агента по ключу.
- `define(self, key, value, group=None)`: Определяет значение в конфигурации агента.
- `define_several(self, group, records)`: Определяет несколько значений в конфигурации агента, принадлежащих к одной группе.
- `define_relationships(self, relationships, replace=True)`: Определяет или обновляет отношения агента с другими агентами.
- `clear_relationships(self)`: Очищает список отношений агента.
- `related_to(self, other_agent, description, symmetric_description=None)`: Устанавливает отношение между агентом и другим агентом.
- `add_mental_faculties(self, mental_faculties)`: Добавляет список ментальных способностей агенту.
- `add_mental_faculty(self, faculty)`: Добавляет ментальную способность агенту.
- `act(self, until_done=True, n=None, return_actions=False, max_content_length=default["max_content_display_length"])`: Заставляет агента действовать в окружающей среде и обновляет его внутреннее когнитивное состояние.
- `listen(self, speech, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Заставляет агента слушать другого агента и обновляет его внутреннее когнитивное состояние.
- `socialize(self, social_description: str, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Заставляет агента воспринимать социальный стимул и обновляет его внутреннее когнитивное состояние.
- `see(self, visual_description, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Заставляет агента воспринимать визуальный стимул и обновляет его внутреннее когнитивное состояние.
- `think(self, thought, max_content_length=default["max_content_display_length"])`: Заставляет агента думать о чем-то и обновляет его внутреннее когнитивное состояние.
- `internalize_goal(self, goal, max_content_length=default["max_content_display_length"])`: Заставляет агента усвоить цель и обновляет его внутреннее когнитивное состояние.
- `_observe(self, stimulus, max_content_length=default["max_content_display_length"])`: Наблюдает за стимулом и обновляет внутреннее состояние агента.
- `listen_and_act(self, speech, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинирует методы `listen` и `act`.
- `see_and_act(self, visual_description, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинирует методы `see` и `act`.
- `think_and_act(self, thought, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинирует методы `think` и `act`.
- `read_documents_from_folder(self, documents_path:str)`: Считывает документы из указанной папки и загружает их в семантическую память агента.
- `read_documents_from_web(self, web_urls:list)`: Считывает документы из указанных URL и загружает их в семантическую память агента.
- `move_to(self, location, context=[])`: Перемещает агента в новое местоположение и обновляет его внутреннее когнитивное состояние.
- `change_context(self, context: list)`: Изменяет контекст агента и обновляет его внутреннее когнитивное состояние.
- `make_agent_accessible(self, agent: Self, relation_description: str = "An agent I can currently interact with.")`: Делает агента доступным для взаимодействия.
- `make_agent_inaccessible(self, agent: Self)`: Делает агента недоступным для взаимодействия.
- `make_all_agents_inaccessible(self)`: Делает всех агентов недоступными для взаимодействия.
- `_produce_message(self)`: Генерирует сообщение от агента, используя OpenAI API.
- `_update_cognitive_state(self, goals=None, context=None, attention=None, emotions=None)`: Обновляет когнитивное состояние агента.
- `_display_communication(self, role, content, kind, simplified=True, max_content_length=default["max_content_display_length"])`: Отображает текущее взаимодействие и сохраняет его в буфере.
- `_push_and_display_latest_communication(self, rendering)`: Добавляет последнее сообщение в буфер и отображает его.
- `pop_and_display_latest_communications(self)`: Извлекает и отображает последние сообщения из буфера.
- `clear_communications_buffer(self)`: Очищает буфер сообщений.
- `pop_latest_actions(self) -> list`: Возвращает последние действия, выполненные агентом.
- `pop_actions_and_get_contents_for(self, action_type: str, only_last_action: bool = True) -> list`: Возвращает содержимое действий указанного типа.
- `__repr__(self)`: Возвращает строковое представление объекта `TinyPerson`.
- `minibio(self)`: Возвращает мини-биографию агента.
- `pp_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"])`: Выводит на экран текущие взаимодействия агента.
- `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info:bool=True)`: Возвращает строку с текущими взаимодействиями агента в удобном для чтения формате.
- `_pretty_stimuli(self, role, content, simplified=True, max_content_length=default["max_content_display_length"]) -> list`: Форматирует стимулы для отображения.
- `_pretty_action(self, role, content, simplified=True, max_content_length=default["max_content_display_length"]) -> str`: Форматирует действие для отображения.
- `_pretty_timestamp(self, role, timestamp) -> str`: Форматирует временную метку для отображения.
- `iso_datetime(self) -> str`: Возвращает текущую дату и время среды в формате ISO.
- `save_spec(self, path, include_mental_faculties=True, include_memory=False)`: Сохраняет текущую конфигурацию агента в JSON-файл.
- `load_spec(path, suppress_mental_faculties=False, suppress_memory=False, auto_rename_agent=False, new_agent_name=None)`: Загружает конфигурацию агента из JSON-файла.
- `encode_complete_state(self) -> dict`: Кодирует полное состояние агента для сериализации и кэширования.
- `decode_complete_state(self, state: dict) -> Self`: Загружает полное состояние агента из словаря и создает новый экземпляр `TinyPerson`.
- `create_new_agent_from_current_spec(self, new_name:str) -> Self`: Создает нового агента на основе текущей спецификации агента.
- `add_agent(agent)`: Добавляет агента в глобальный список агентов.
- `has_agent(agent_name: str)`: Проверяет, зарегистрирован ли агент.
- `set_simulation_for_free_agents(simulation)`: Устанавливает симуляцию для свободных агентов.
- `get_agent_by_name(name)`: Возвращает агента по имени.
- `clear_agents()`: Очищает глобальный список агентов.

### `TinyMentalFaculty`

**Описание**:
Представляет ментальную способность агента.

**Принцип работы**:
Базовый класс для различных ментальных способностей, таких как память, рассуждение и т. д.

**Методы**:
- `__init__(self, name: str, requires_faculties: list=None) -> None`: Инициализирует ментальную способность.
- `__str__(self) -> str`: Возвращает строковое представление ментальной способности.
- `__eq__(self, other)`: Сравнивает две ментальные способности на равенство.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие, связанное с этой способностью.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действия, связанные с этой способностью.

### `RecallFaculty`

**Описание**:
Обеспечивает агенту возможность вспоминать информацию из памяти.

**Принцип работы**:
Позволяет агенту извлекать релевантную информацию из семантической памяти на основе заданного запроса.

**Методы**:
- `__init__(self)`: Инициализирует способность вспоминать.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие "RECALL", извлекая информацию из семантической памяти.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действия "RECALL".
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действие "RECALL".

### `FilesAndWebGroundingFaculty`

**Описание**:
Позволяет агенту получать доступ к локальным файлам и веб-страницам для обоснования своих знаний.

**Принцип работы**:
Обеспечивает агенту возможность консультироваться с документами и списками документов, чтобы расширить свою базу знаний.

**Методы**:
- `__init__(self)`: Инициализирует способность к обоснованию.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действия "CONSULT" и "LIST_DOCUMENTS", предоставляя агенту доступ к документам.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действий "CONSULT" и "LIST_DOCUMENTS".
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действия "CONSULT" и "LIST_DOCUMENTS".

### `TinyToolUse`

**Описание**:
Позволяет агенту использовать инструменты для выполнения задач.

**Принцип работы**:
Предоставляет агенту возможность использовать различные инструменты для выполнения задач.

**Методы**:
- `__init__(self, tools:list) -> None`: Инициализирует способность использовать инструменты.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие, передавая его каждому инструменту.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действий, связанных с использованием инструментов.
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действия, связанные с использованием инструментов.

### `TinyMemory`

**Описание**:
Базовый класс для различных типов памяти.

**Принцип работы**:
Абстрактный класс, определяющий интерфейс для различных типов памяти, таких как эпизодическая и семантическая память.

**Методы**:
- `store(self, value: Any) -> None`: Сохраняет значение в памяти.
- `retrieve(self, first_n: int, last_n: int, include_omission_info:bool=True) -> list`: Извлекает значения из памяти.
- `retrieve_recent(self) -> list`: Извлекает последние значения из памяти.
- `retrieve_all(self) -> list`: Извлекает все значения из памяти.
- `retrieve_relevant(self, relevance_target:str, top_k=5) -> list`: Извлекает значения из памяти, релевантные заданной цели.

### `EpisodicMemory`

**Описание**:
Предоставляет агенту эпизодическую память.

**Принцип работы**:
Реализует эпизодическую память, позволяя агенту запоминать конкретные события или эпизоды из прошлого.

**Методы**:
- `__init__(self, fixed_prefix_length: int = 100, lookback_length: int = 100) -> None`: Инициализирует эпизодическую память.
- `store(self, value: Any) -> None`: Сохраняет значение в эпизодической памяти.
- `count(self) -> int`: Возвращает количество значений в эпизодической памяти.
- `retrieve(self, first_n: int, last_n: int, include_omission_info:bool=True) -> list`: Извлекает значения из эпизодической памяти.
- `retrieve_recent(self, include_omission_info:bool=True) -> list`: Извлекает последние значения из эпизодической памяти.
- `retrieve_all(self) -> list`: Извлекает все значения из эпизодической памяти.
- `retrieve_relevant(self, relevance_target: str) -> list`: Извлекает значения из эпизодической памяти, релевантные заданной цели.
- `retrieve_first(self, n: int, include_omission_info:bool=True) -> list`: Извлекает первые n значений из памяти.
- `retrieve_last(self, n: int, include_omission_info:bool=True) -> list`: Извлекает последние n значений из памяти.

### `SemanticMemory`

**Описание**:
Семантическая память агента.

**Принцип работы**:
Реализует семантическую память, позволяя агенту хранить и извлекать знания, не связанные с конкретными событиями или эпизодами.

**Методы**:
- `__init__(self, documents_paths: list=None, web_urls: list=None) -> None`: Инициализирует семантическую память.
- `retrieve_relevant(self, relevance_target:str, top_k=5) -> list`: Извлекает значения из памяти, релевантные заданной цели.
- `retrieve_document_content_by_name(self, document_name:str) -> str`: Извлекает документ по имени.
- `list_documents_names(self) -> list`: Перечисляет имена документов в памяти.
- `add_documents_paths(self, documents_paths:list) -> None`: Добавляет пути к папкам с документами.
- `add_documents_path(self, documents_path:str) -> None`: Добавляет путь к папке с документами.
- `add_web_urls(self, web_urls:list) -> None`: Добавляет данные, полученные из указанных URL, в документы, используемые для семантической памяти.
- `add_web_url(self, web_url:str) -> None`: Добавляет данные, полученные из указанного URL, в документы, используемые для семантической памяти.
- `_add_documents(self, new_documents, doc_to_name_func) -> list`: Добавляет документы в семантическую память.
- `_post_deserialization_init(self)`: Выполняет инициализацию после десериализации.

## Функции

В данном модуле отсутствуют отдельные функции, не являющиеся методами классов.

**Как работает функция**:\n
1. Данный модуль предоставляет основу для создания агентов TinyTroupe, моделируя их поведение и когнитивные способности.\n
2. Он включает в себя классы для представления агентов, их ментальных способностей и механизмов памяти.\n
3. Модуль использует OpenAI API для генерации сообщений и взаимодействия агентов с окружением.

```
+---------------------+
|  Начало работы       |
+---------------------+
|
↓
+---------------------+
|  Инициализация     |
|  агента TinyPerson   |
+---------------------+
|
↓
+---------------------+
|  Определение конфиг.  |
|  и ментальных способ. |
+---------------------+
|
↓
+---------------------+
|  Взаимодействие с   |
|  окружением и др.   |
|  агентами           |
+---------------------+
|
↓
+---------------------+
|  Обновление когнитив.|
|  состояния и памяти   |
+---------------------+
|
↓
+---------------------+
|  Генерация сообщений |
|  и действий          |
+---------------------+
|
↓
+---------------------+
|  Конец работы        |
+---------------------+
```

**Примеры**:

Примеры использования классов и методов данного модуля можно найти в других частях проекта TinyTroupe, где создаются и управляются агенты для различных целей.
```python
from tinytroupe.agent import TinyPerson, EpisodicMemory

# Создание экземпляра агента
agent = TinyPerson(name='Alice')

# Определение цели агента
agent.define('goal', 'Найти работу')

# Прослушивание сообщения
agent.listen('Привет, Алиса! Как дела?')

# Действие агента
agent.act()
```
```python
from tinytroupe.agent import TinyPerson, SemanticMemory

# Создание экземпляра агента
agent = TinyPerson(name='Bob')

# Чтение документов из папки
agent.read_documents_from_folder('/path/to/documents')

# Поиск релевантной информации
relevant_info = agent.semantic_memory.retrieve_relevant('поиск работы')
print(relevant_info)
```
```python
from tinytroupe.agent import TinyPerson, RecallFaculty

# Создание экземпляра агента
agent = TinyPerson(name='Charlie')

# Добавление ментальной способности
agent.add_mental_faculty(RecallFaculty())

# Запоминание информации
agent.episodic_memory.store({'role': 'assistant', 'content': 'Я иду искать работу'})

# Действие агента с использованием способности к вспоминанию
agent.act()