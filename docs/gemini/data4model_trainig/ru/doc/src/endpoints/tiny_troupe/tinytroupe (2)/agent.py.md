# Модуль для работы с агентами TinyTroupe
==============================================

Модуль предоставляет основные классы и функции для агентов TinyTroupe.

Агенты являются ключевой абстракцией, используемой в TinyTroupe. Агент - это имитируемый человек или сущность, которая может взаимодействовать с другими агентами и средой, получая стимулы и производя действия. Агенты имеют когнитивные состояния, которые обновляются по мере их взаимодействия со средой и другими агентами. Агенты также могут хранить и извлекать информацию из памяти и выполнять действия в среде. В отличие от агентов, целью которых является оказание поддержки AI-ассистентам или другим подобным инструментам повышения производительности, **агенты TinyTroupe нацелены на представление человеческого поведения**, которое включает идиосинкразии, эмоции и другие человеческие черты, которые не ожидаются от инструмента повышения производительности.

Общая основополагающая структура вдохновлена главным образом когнитивной психологией, поэтому агенты имеют различные внутренние когнитивные состояния, такие как внимание, эмоции и цели. Именно поэтому память агента, в отличие от других платформ агентов на основе LLM, имеет тонкие внутренние разделения, особенно между эпизодической и семантической памятью. Некоторые бихевиористские концепции также присутствуют, такие как идея "стимула" и "реакции" в методах `listen` и `act`, которые являются ключевыми абстракциями для понимания того, как агенты взаимодействуют со средой и другими агентами.

## Оглавление

- [Обзор](#обзор)
- [Классы](#классы)
    - [TinyPerson](#tinyperson)
    - [TinyMentalFaculty](#tinymentalfaculty)
    - [RecallFaculty](#recallfaculty)
    - [FilesAndWebGroundingFaculty](#filesandwebgroundingfaculty)
    - [TinyToolUse](#tinytooluse)
    - [TinyMemory](#tinymemory)
    - [EpisodicMemory](#episodicmemory)
    - [SemanticMemory](#semanticmemory)
- [Переменные](#переменные)

## Обзор

В этом модуле определены основные классы для создания и управления агентами в симуляции TinyTroupe. Он включает в себя классы для представления агентов (`TinyPerson`), их когнитивных способностей (`TinyMentalFaculty`), различных типов памяти (`EpisodicMemory`, `SemanticMemory`) и инструментов, которые они могут использовать (`TinyToolUse`).

## Подробнее

Этот модуль является сердцем системы агентов TinyTroupe. Он предоставляет строительные блоки для создания сложных симуляций с участием агентов, взаимодействующих друг с другом и с окружающей средой. Класс `TinyPerson` представляет собой основного агента, а классы ментальных способностей и памяти позволяют агентам мыслить, учиться и адаптироваться к новым ситуациям.

## Классы

### `TinyPerson`

**Описание**: Имитирует личность в TinyTroupe вселенной.

**Наследует**: `JsonSerializableRegistry`

**Атрибуты**:
- `MAX_ACTIONS_BEFORE_DONE` (int): Максимальное количество действий, которое агент может выполнить до завершения.
- `PP_TEXT_WIDTH` (int): Ширина текста для pretty print.
- `serializable_attributes` (list): Список атрибутов, которые могут быть сериализованы в JSON.
- `all_agents` (dict): Словарь всех созданных агентов (name -> agent).
- `communication_style` (str): Стиль общения для всех агентов: "simplified" или "full".
- `communication_display` (bool): Определяет, отображать ли общение. True - для интерактивных приложений.

**Методы**:
- `__init__(self, name: str = None, episodic_memory=None, semantic_memory=None, mental_faculties: list = None)`: Создает экземпляр TinyPerson.
- `_post_init(self, **kwargs)`: Выполняет постобработку инициализации после `__init__`.
- `generate_agent_prompt(self)`: Генерирует prompt для агента на основе шаблона.
- `reset_prompt(self)`: Сбрасывает prompt агента.
- `get(self, key)`: Возвращает значение ключа из конфигурации агента.
- `define(self, key, value, group=None)`: Определяет значение в конфигурации агента.
- `define_several(self, group, records)`: Определяет несколько значений в конфигурации агента, принадлежащих к одной группе.
- `define_relationships(self, relationships, replace=True)`: Определяет или обновляет отношения агента.
- `clear_relationships(self)`: Очищает отношения агента.
- `related_to(self, other_agent, description, symmetric_description=None)`: Определяет отношение между этим агентом и другим агентом.
- `add_mental_faculties(self, mental_faculties)`: Добавляет список ментальных способностей агенту.
- `add_mental_faculty(self, faculty)`: Добавляет ментальную способность агенту.
- `act(self, until_done=True, n=None, return_actions=False, max_content_length=default["max_content_display_length"])`: Выполняет действие в среде и обновляет внутреннее когнитивное состояние.
- `listen(self, speech, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Слушает другого агента и обновляет внутреннее когнитивное состояние.
- `socialize(self, social_description: str, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Воспринимает социальный стимул и обновляет внутреннее когнитивное состояние.
- `see(self, visual_description, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Воспринимает визуальный стимул и обновляет внутреннее когнитивное состояние.
- `think(self, thought, max_content_length=default["max_content_display_length"])`: Заставляет агента думать о чем-то и обновляет внутреннее когнитивное состояние.
- `internalize_goal(self, goal, max_content_length=default["max_content_display_length"])`: Интериоризирует цель и обновляет внутреннее когнитивное состояние.
- `_observe(self, stimulus, max_content_length=default["max_content_display_length"])`: Наблюдает стимул и обновляет внутреннее когнитивное состояние.
- `listen_and_act(self, speech, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинирует методы `listen` и `act`.
- `see_and_act(self, visual_description, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинирует методы `see` и `act`.
- `think_and_act(self, thought, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинирует методы `think` и `act`.
- `read_documents_from_folder(self, documents_path: str)`: Читает документы из папки и загружает их в семантическую память.
- `read_documents_from_web(self, web_urls: list)`: Читает документы из веб-URL и загружает их в семантическую память.
- `move_to(self, location, context=[])`: Перемещается в новое местоположение и обновляет внутреннее когнитивное состояние.
- `change_context(self, context: list)`: Изменяет контекст и обновляет внутреннее когнитивное состояние.
- `make_agent_accessible(self, agent: Self, relation_description: str = "An agent I can currently interact with.")`: Делает агента доступным для этого агента.
- `make_agent_inaccessible(self, agent: Self)`: Делает агента недоступным для этого агента.
- `make_all_agents_inaccessible(self)`: Делает всех агентов недоступными для этого агента.
- `_produce_message(self)`: Генерирует сообщение для отправки в OpenAI API.
- `_update_cognitive_state(self, goals=None, context=None, attention=None, emotions=None)`: Обновляет когнитивное состояние TinyPerson.
- `_display_communication(self, role, content, kind, simplified=True, max_content_length=default["max_content_display_length"])`: Отображает текущее общение и сохраняет его в буфере для последующего использования.
- `_push_and_display_latest_communication(self, rendering)`: Добавляет последние сообщения в буфер агента.
- `pop_and_display_latest_communications(self)`: Выводит последние сообщения из буфера.
- `clear_communications_buffer(self)`: Очищает буфер сообщений.
- `pop_latest_actions(self) -> list`: Возвращает последние действия, выполненные этим агентом.
- `pop_actions_and_get_contents_for(self, action_type: str, only_last_action: bool = True) -> list`: Возвращает содержимое действий заданного типа, выполненных этим агентом.
- `__repr__(self)`: Возвращает строковое представление объекта `TinyPerson`.
- `minibio(self)`: Возвращает мини-биографию `TinyPerson`.
- `pp_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"])`: Выводит текущие взаимодействия.
- `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info: bool = True)`:  Возвращает строку с текущими сообщениями.
- `_pretty_stimuli(self, role, content, simplified=True, max_content_length=default["max_content_display_length"]) -> list`: Форматирует стимулы для отображения.
- `_pretty_action(self, role, content, simplified=True, max_content_length=default["max_content_display_length"]) -> str`: Форматирует действие для отображения.
- `_pretty_timestamp(self, role, timestamp) -> str`: Форматирует временную метку для отображения.
- `iso_datetime(self) -> str`: Возвращает текущую дату и время среды, если есть.
- `save_spec(self, path, include_mental_faculties=True, include_memory=False)`: Сохраняет текущую конфигурацию в файл JSON.
- `load_spec(path, suppress_mental_faculties=False, suppress_memory=False, auto_rename_agent=False, new_agent_name=None)`: Загружает спецификацию агента из JSON-файла.
- `encode_complete_state(self) -> dict`: Кодирует полное состояние `TinyPerson`, включая текущие сообщения, доступных агентов и т. д.
- `decode_complete_state(self, state: dict) -> Self`: Загружает полное состояние `TinyPerson`, включая текущие сообщения, и создает новый экземпляр `TinyPerson`.
- `create_new_agent_from_current_spec(self, new_name: str) -> Self`: Создает нового агента из спецификации текущего агента.
- `add_agent(agent)`: Добавляет агента в глобальный список агентов.
- `has_agent(agent_name: str)`: Проверяет, зарегистрирован ли уже агент.
- `set_simulation_for_free_agents(simulation)`: Устанавливает симуляцию, если она None.
- `get_agent_by_name(name)`: Возвращает агента по имени.
- `clear_agents()`: Очищает глобальный список агентов.

**Принцип работы**:

Класс `TinyPerson` является основой для создания агентов в TinyTroupe. Он содержит всю информацию, необходимую для представления агента, включая его имя, память, ментальные способности и конфигурацию. Методы класса позволяют агенту взаимодействовать с окружающей средой, общаться с другими агентами и обновлять свое внутреннее когнитивное состояние.

Класс использует `JsonSerializableRegistry` для сериализации и десериализации, что позволяет сохранять и загружать состояние агента.

### `TinyMentalFaculty`

**Описание**:
Представляет ментальную способность агента. Ментальные способности - это когнитивные способности, которыми обладает агент.

**Атрибуты**:
- `name` (str): Название ментальной способности.
- `requires_faculties` (list): Список ментальных способностей, необходимых для правильной работы этой способности.

**Методы**:
- `__init__(self, name: str, requires_faculties: list = None) -> None`: Инициализирует ментальную способность.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие, связанное с этой способностью.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действия, связанные с этой способностью.

**Принцип работы**:

`TinyMentalFaculty` - это базовый класс для всех ментальных способностей агента. Он определяет интерфейс для обработки действий и предоставления подсказок для определения действий и ограничений.

### `RecallFaculty`

**Описание**:
Предоставляет агенту способность вспоминать информацию из памяти.

**Наследует**: `TinyMentalFaculty`

**Методы**:
- `__init__(self)`: Инициализирует способность "Memory Recall".
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие RECALL.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действия, связанные с этой способностью.

**Принцип работы**:

`RecallFaculty` позволяет агенту извлекать информацию из своей семантической памяти на основе предоставленного запроса. Если релевантная информация найдена, агент "думает" об этом и использует ее для дальнейших действий.

### `FilesAndWebGroundingFaculty`

**Описание**:
Позволяет агенту получать доступ к локальным файлам и веб-страницам для обоснования своих знаний.

**Наследует**: `TinyMentalFaculty`

**Методы**:
- `__init__(self)`: Инициализирует способность "Local Grounding".
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действия CONSULT и LIST_DOCUMENTS.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действия, связанные с этой способностью.

**Принцип работы**:

`FilesAndWebGroundingFaculty` предоставляет агенту возможность доступа к локальным файлам и веб-страницам, что позволяет ему расширять свои знания и принимать более обоснованные решения.

### `TinyToolUse`

**Описание**:
Позволяет агенту использовать инструменты для выполнения задач.

**Наследует**: `TinyMentalFaculty`

**Методы**:
- `__init__(self, tools: list) -> None`: Инициализирует способность "Tool Use".
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие, связанное с использованием инструмента.
- `actions_definitions_prompt(self) -> str`: Возвращает prompt для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`: Возвращает prompt для определения ограничений на действия, связанные с этой способностью.

**Принцип работы**:

`TinyToolUse` позволяет агенту использовать различные инструменты для выполнения задач. Каждый инструмент предоставляет свои собственные определения действий и ограничения.

### `TinyMemory`

**Описание**:
Базовый класс для различных типов памяти.

**Наследует**: `TinyMentalFaculty`

**Методы**:
- `store(self, value: Any) -> None`: Сохраняет значение в памяти.
- `retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list`: Извлекает первые n и/или последние n значений из памяти.
- `retrieve_recent(self) -> list`: Извлекает n самых последних значений из памяти.
- `retrieve_all(self) -> list`: Извлекает все значения из памяти.
- `retrieve_relevant(self, relevance_target: str, top_k=5) -> list`: Извлекает все значения из памяти, релевантные данной цели.

**Принцип работы**:

`TinyMemory` является базовым классом для различных типов памяти, таких как эпизодическая и семантическая память. Он определяет интерфейс для хранения и извлечения информации из памяти.

### `EpisodicMemory`

**Описание**:
Предоставляет агенту возможность эпизодической памяти. Эпизодическая память - это способность помнить конкретные события или эпизоды в прошлом.

**Наследует**: `TinyMemory`

**Атрибуты**:
- `MEMORY_BLOCK_OMISSION_INFO` (dict): Информация об опущенных сообщениях.
- `fixed_prefix_length` (int): Фиксированная длина префикса.
- `lookback_length` (int): Длина ретроспективы.
- `memory` (list): Список сообщений в памяти.

**Методы**:
- `__init__(self, fixed_prefix_length: int = 100, lookback_length: int = 100) -> None`: Инициализирует память.
- `store(self, value: Any) -> None`: Сохраняет значение в памяти.
- `count(self) -> int`: Возвращает количество значений в памяти.
- `retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list`: Извлекает первые n и/или последние n значения из памяти.
- `retrieve_recent(self, include_omission_info: bool = True) -> list`: Извлекает n самых последних значений из памяти.
- `retrieve_all(self) -> list`: Извлекает все значения из памяти.
- `retrieve_relevant(self, relevance_target: str) -> list`: Извлекает все значения из памяти, релевантные данной цели.
- `retrieve_first(self, n: int, include_omission_info: bool = True) -> list`: Извлекает первые n значений из памяти.
- `retrieve_last(self, n: int, include_omission_info: bool = True) -> list`: Извлекает последние n значений из памяти.

**Принцип работы**:

`EpisodicMemory` хранит последовательность сообщений, представляющих эпизоды, которые пережил агент. Он предоставляет методы для извлечения недавних эпизодов, всех эпизодов или только первых/последних n эпизодов.

### `SemanticMemory`

**Описание**:
Семантическая память - это память о значениях, пониманиях и других знаниях, основанных на концепциях, не связанных с конкретным опытом.

**Наследует**: `TinyMemory`

**Атрибуты**:
- `suppress_attributes_from_serialization` (list): Атрибуты, которые не должны быть сериализованы.
- `index` (Any): Индекс для семантического поиска.
- `documents_paths` (list): Список путей к папкам с документами.
- `documents_web_urls` (list): Список веб-URL документов.
- `documents` (list): Список документов в памяти.
- `filename_to_document` (dict): Словарь, отображающий имена файлов в документы.

**Методы**:
- `__init__(self, documents_paths: list = None, web_urls: list = None) -> None`: Инициализирует память.
- `retrieve_relevant(self, relevance_target: str, top_k=5) -> list`: Извлекает все значения из памяти, релевантные данной цели.
- `retrieve_document_content_by_name(self, document_name: str) -> str`: Извлекает документ по его имени.
- `list_documents_names(self) -> list`: Перечисляет имена документов в памяти.
- `add_documents_paths(self, documents_paths: list) -> None`: Добавляет путь к папке с документами, используемыми для семантической памяти.
- `add_documents_path(self, documents_path: str) -> None`: Добавляет путь к папке с документами, используемыми для семантической памяти.
- `add_web_urls(self, web_urls: list) -> None`: Добавляет данные, полученные из указанных URL-адресов, к документам, используемым для семантической памяти.
- `add_web_url(self, web_url: str) -> None`: Добавляет данные, полученные из указанного URL-адреса, к документам, используемым для семантической памяти.
- `_add_documents(self, new_documents, doc_to_name_func) -> list`: Добавляет документы в семантическую память.
- `_post_deserialization_init(self)`: Выполняет постобработку инициализации после десериализации.

**Принцип работы**:

`SemanticMemory` хранит знания агента о мире. Он использует `llama_index` для индексации документов и извлечения релевантной информации на основе семантического поиска.

## Переменные

- `config` (dict): Конфигурация, прочитанная из файла конфигурации.
- `default` (dict): Словарь значений по умолчанию для различных параметров.
    - `default["embedding_model"]` (str): Модель встраивания по умолчанию.
    - `default["max_content_display_length"]` (int): Максимальная длина контента для отображения.
- `llmaindex_openai_embed_model` (OpenAIEmbedding): Модель встраивания OpenAI для llama_index.