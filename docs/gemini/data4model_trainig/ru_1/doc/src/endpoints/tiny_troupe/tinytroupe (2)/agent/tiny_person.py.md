# Модуль `tiny_person.py`

## Обзор

Модуль содержит класс `TinyPerson`, который представляет собой симуляцию личности в виртуальной среде TinyTroupe. Он управляет памятью, умственными способностями и взаимодействием агента с окружающей средой.

## Подробнее

Модуль предоставляет инструменты для создания, загрузки, сохранения и управления агентами `TinyPerson`. Он включает в себя механизмы для восприятия, мышления, действия и общения агентов. Модуль также обеспечивает интеграцию с памятью (эпизодической и семантической) и поддерживает различные способы взаимодействия с окружающей средой.

## Классы

### `TinyPerson`

**Описание**: Класс `TinyPerson` представляет собой виртуального агента, способного воспринимать окружающую среду, мыслить, действовать и общаться.

**Наследует**: `JsonSerializableRegistry`

**Атрибуты**:

- `MAX_ACTIONS_BEFORE_DONE` (int): Максимальное количество действий, которое агент может выполнить до завершения.
- `PP_TEXT_WIDTH` (int): Ширина текста для форматированного вывода.
- `serializable_attributes` (list): Список атрибутов, подлежащих сериализации.
- `serializable_attributes_renaming` (dict): Словарь для переименования атрибутов при сериализации.
- `all_agents` (dict): Словарь всех созданных агентов (имя -> агент).
- `communication_style` (str): Стиль общения для всех агентов ("simplified" или "full").
- `communication_display` (bool): Определяет, отображать ли сообщения агентов в процессе симуляции.

**Методы**:

- `__init__(self, name: str = None, episodic_memory = None, semantic_memory = None, mental_faculties: list = None)`: Конструктор класса `TinyPerson`.
- `_post_init(self, **kwargs)`: Выполняет постобработку инициализации экземпляра класса.
- `generate_agent_system_prompt(self)`: Генерирует системное сообщение для агента на основе шаблона.
- `reset_prompt(self)`: Сбрасывает текущее системное сообщение агента.
- `get(self, key)`: Возвращает значение ключа из конфигурации агента.
- `import_fragment(self, path)`: Импортирует фрагмент конфигурации агента из JSON-файла.
- `include_persona_definitions(self, additional_definitions: dict)`: Добавляет определения к текущей конфигурации агента.
- `define(self, key, value, merge=True, overwrite_scalars=True)`: Определяет значение в конфигурации агента.
- `define_relationships(self, relationships, replace=True)`: Определяет или обновляет отношения агента с другими агентами.
- `clear_relationships(self)`: Очищает список отношений агента.
- `related_to(self, other_agent, description, symmetric_description=None)`: Определяет отношение между этим агентом и другим.
- `add_mental_faculties(self, mental_faculties)`: Добавляет список умственных способностей агенту.
- `add_mental_faculty(self, faculty)`: Добавляет умственную способность агенту.
- `act(self, until_done=True, n=None, return_actions=False, max_content_length=default["max_content_display_length"])`: Выполняет действие в среде и обновляет внутреннее состояние агента.
- `listen(self, speech, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Слушает другого агента и обновляет свое внутреннее состояние.
- `socialize(self, social_description: str, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Воспринимает социальный стимул и обновляет внутреннее состояние.
- `see(self, visual_description, source: AgentOrWorld = None, max_content_length=default["max_content_display_length"])`: Воспринимает визуальный стимул и обновляет внутреннее состояние.
- `think(self, thought, max_content_length=default["max_content_display_length"])`: Заставляет агента думать о чем-то и обновляет его внутреннее состояние.
- `internalize_goal(self, goal, max_content_length=default["max_content_display_length"])`: Усваивает цель и обновляет внутреннее состояние.
- `_observe(self, stimulus, max_content_length=default["max_content_display_length"])`: Наблюдает за стимулом и обновляет внутреннее состояние.
- `listen_and_act(self, speech, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинированный метод `listen` и `act`.
- `see_and_act(self, visual_description, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинированный метод `see` и `act`.
- `think_and_act(self, thought, return_actions=False, max_content_length=default["max_content_display_length"])`: Комбинированный метод `think` и `act`.
- `read_documents_from_folder(self, documents_path: str)`: Считывает документы из каталога и загружает их в семантическую память.
- `read_document_from_file(self, file_path: str)`: Считывает документ из файла и загружает его в семантическую память.
- `read_documents_from_web(self, web_urls: list)`: Считывает документы из веб-адресов и загружает их в семантическую память.
- `read_document_from_web(self, web_url: str)`: Считывает документ из веб-адреса и загружает его в семантическую память.
- `move_to(self, location, context=[])`: Перемещает агента в новое местоположение и обновляет контекст.
- `change_context(self, context: list)`: Изменяет контекст и обновляет внутреннее состояние агента.
- `make_agent_accessible(self, agent: Self, relation_description: str = "An agent I can currently interact with.")`: Делает агента доступным для взаимодействия.
- `make_agent_inaccessible(self, agent: Self)`: Делает агента недоступным для взаимодействия.
- `make_all_agents_inaccessible(self)`: Делает всех агентов недоступными для взаимодействия.
- `_produce_message(self)`: Генерирует сообщение для отправки в OpenAI API.
- `_update_cognitive_state(self, goals=None, context=None, attention=None, emotions=None)`: Обновляет когнитивное состояние агента.
- `store_in_memory(self, value: Any) -> list`: Сохраняет значение в памяти агента.
- `optimize_memory(self)`: Оптимизирует память агента.
- `retrieve_memories(self, first_n: int, last_n: int, include_omission_info: bool = True, max_content_length: int = None) -> list`: Извлекает эпизоды из памяти агента.
- `retrieve_recent_memories(self, max_content_length: int = None) -> list`: Извлекает последние эпизоды из памяти агента.
- `retrieve_relevant_memories(self, relevance_target: str, top_k=20) -> list`: Извлекает релевантные воспоминания из семантической памяти.
- `retrieve_relevant_memories_for_current_context(self, top_k=7) -> list`: Извлекает релевантные воспоминания для текущего контекста.
- `_display_communication(self, role, content, kind, simplified=True, max_content_length=default["max_content_display_length"])`: Отображает текущее взаимодействие.
- `_push_and_display_latest_communication(self, communication)`: Добавляет последнее сообщение в буфер коммуникаций агента.
- `pop_and_display_latest_communications(self)`: Выводит на экран последние сообщения агента.
- `clear_communications_buffer(self)`: Очищает буфер сообщений агента.
- `pop_latest_actions(self) -> list`: Возвращает последние действия, выполненные агентом.
- `pop_actions_and_get_contents_for(self, action_type: str, only_last_action: bool = True) -> list`: Возвращает содержимое действий заданного типа, выполненных этим агентом.
- `__repr__(self)`: Возвращает строковое представление объекта `TinyPerson`.
- `minibio(self, extended=True)`: Возвращает краткую биографию агента.
- `pp_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"])`: Выводит на экран текущие взаимодействия.
- `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info: bool = True)`: Возвращает строку с текущими сообщениями.
- `_pretty_stimuli(self, role, content, simplified=True, max_content_length=default["max_content_display_length"]) -> list`: Форматирует стимулы для вывода.
- `_pretty_action(self, role, content, simplified=True, max_content_length=default["max_content_display_length"]) -> str`: Форматирует действие для вывода.
- `_pretty_timestamp(self, role, timestamp) -> str`: Форматирует временную метку для вывода.
- `iso_datetime(self) -> str`: Возвращает текущую дату и время среды, если есть.
- `save_specification(self, path, include_mental_faculties=True, include_memory=False)`: Сохраняет текущую конфигурацию в файл JSON.
- `load_specification(path_or_dict, suppress_mental_faculties=False, suppress_memory=False, auto_rename_agent=False, new_agent_name=None)`: Загружает конфигурацию агента из файла JSON.
- `encode_complete_state(self) -> dict`: Кодирует полное состояние агента.
- `decode_complete_state(self, state: dict) -> Self`: Загружает полное состояние агента.
- `create_new_agent_from_current_spec(self, new_name: str) -> Self`: Создает нового агента на основе текущей спецификации.
- `add_agent(agent)`: Добавляет агента в глобальный список агентов.
- `has_agent(agent_name: str)`: Проверяет, зарегистрирован ли агент.
- `set_simulation_for_free_agents(simulation)`: Устанавливает симуляцию для свободных агентов.
- `get_agent_by_name(name)`: Возвращает агента по имени.
- `all_agents_names()`: Возвращает имена всех агентов.
- `clear_agents()`: Очищает глобальный список агентов.

### `__init__`
```python
def __init__(self, name:str=None, 
                 episodic_memory=None,
                 semantic_memory=None,
                 mental_faculties:list=None):
    """
    Создает экземпляр класса `TinyPerson`.

    Args:
        name (str, optional): Имя агента `TinyPerson`. Должно быть указано либо имя, либо путь к файлу спецификации.
        episodic_memory (EpisodicMemory, optional): Реализация эпизодической памяти для использования. По умолчанию `EpisodicMemory()`.
        semantic_memory (SemanticMemory, optional): Реализация семантической памяти для использования. По умолчанию `SemanticMemory()`.
        mental_faculties (list, optional): Список умственных способностей, добавляемых агенту. По умолчанию `None`.
    
    Raises:
        AssertionError: Если не указано имя агента.
    """
    ...
```
### `_post_init`
```python
def _post_init(self, **kwargs):
    """
    Выполняет постобработку инициализации экземпляра класса `TinyPerson`.

    Args:
        **kwargs: Произвольные ключевые аргументы.

    Описание:
        Метод вызывается после `__init__` благодаря декоратору `@post_init`.
        Он выполняет дополнительную настройку объекта,
        включая установку значений по умолчанию для различных атрибутов,
        таких как текущие сообщения, окружение, буфер действий, доступные агенты,
        а также инициализацию эпизодической и семантической памяти, умственных способностей,
        персоны и ментального состояния агента.

        Кроме того, метод обрабатывает специальные механизмы,
        используемые во время десериализации, такие как переименование агента
        или автоматическое переименование при конфликте имен.
        В конце инициализации агент регистрируется в глобальном списке агентов
        и сбрасывается его системный промпт.

        Если агент создается в контексте симуляции,
        его идентификатор симуляции устанавливается соответствующим образом.
    """
    ...
```

### `generate_agent_system_prompt`
```python
 def generate_agent_system_prompt(self):
        """
        Генерирует системное сообщение для агента.

        Описание:
            Этот метод считывает шаблон промпта агента из файла,
            заполняет его переменными из конфигурации персоны агента,
            добавляет определения и ограничения действий из умственных способностей агента,
            и возвращает сгенерированное системное сообщение.

        Returns:
            str: Сгенерированное системное сообщение для агента.
        """
        ...
```

### `reset_prompt`
```python
def reset_prompt(self):
        """
        Сбрасывает промпт агента.

        Описание:
            Этот метод генерирует новое системное сообщение для агента,
            используя текущую конфигурацию и шаблон промпта.
            Он также сбрасывает текущие сообщения агента,
            добавляя новое системное сообщение и извлекая последние воспоминания.
            В конце добавляется пользовательское сообщение,
            чтобы побудить агента к действию в соответствии с директивами.
        """
        ...
```

### `get`
```python
def get(self, key):
        """
        Возвращает значение ключа из конфигурации агента.

        Args:
            key (str): Ключ для поиска значения.

        Returns:
            Any: Значение ключа, или None, если ключ не найден.
        """
        ...
```

### `import_fragment`
```python
@transactional
def import_fragment(self, path):
    """
    Импортирует фрагмент конфигурации персоны из JSON-файла.

    Args:
        path (str): Путь к JSON-файлу, содержащему фрагмент конфигурации.

    Raises:
        ValueError: Если JSON-файл не является допустимым фрагментом конфигурации персоны.
    """
    ...
```

### `include_persona_definitions`
```python
 @transactional
    def include_persona_definitions(self, additional_definitions: dict):
        """
        Включает набор определений в TinyPerson.

        Args:
            additional_definitions (dict): Дополнительные определения для импорта.
        """
        ...
```

### `define`
```python
 @transactional
    def define(self, key, value, merge=True, overwrite_scalars=True):
        """
        Определяет значение в конфигурации персоны TinyPerson.

        Args:
            key (str): Ключ для определения.
            value (Any): Значение для определения.
            merge (bool, optional): Определяет, объединять ли значения dict/list с существующими значениями или заменять их. По умолчанию True.
            overwrite_scalars (bool, optional): Определяет, перезаписывать ли скалярные значения или нет. По умолчанию True.
        """
        ...
```

### `define_relationships`
```python
@transactional
    def define_relationships(self, relationships, replace=True):
        """
        Определяет или обновляет отношения TinyPerson.

        Args:
            relationships (list or dict): Отношения для добавления или замены. Либо список словарей, сопоставляющих имена агентов с описаниями отношений,
              либо один словарь, сопоставляющий одно имя агента с его описанием отношений.
            replace (bool, optional): Определяет, заменять ли текущие отношения или просто добавлять к ним. По умолчанию True.
        """
        ...
```

### `clear_relationships`
```python
@transactional
    def clear_relationships(self):
        """
        Очищает отношения TinyPerson.
        """
        ...
```

### `related_to`
```python
@transactional
    def related_to(self, other_agent, description, symmetric_description=None):
        """
        Определяет отношение между этим агентом и другим агентом.

        Args:
            other_agent (TinyPerson): Другой агент.
            description (str): Описание отношения.
            symmetric (bool): Определяет, является ли отношение симметричным или нет. То есть,
              если отношение определено для обоих агентов.

        Returns:
            TinyPerson: Сам агент, чтобы облегчить объединение в цепочку.
        """
        ...
```

### `add_mental_faculties`
```python
def add_mental_faculties(self, mental_faculties):
        """
        Добавляет список умственных способностей агенту.
        """
        ...
```

### `add_mental_faculty`
```python
def add_mental_faculty(self, faculty):
        """
        Добавляет умственную способность агенту.
        """
        ...
```

### `act`
```python
@transactional
    def act(
        self,
        until_done=True,
        n=None,
        return_actions=False,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Действует в окружающей среде и обновляет свое внутреннее когнитивное состояние.
        Либо действует, пока агент не будет завершен и не потребуются дополнительные стимулы, либо действует фиксированное количество раз,
        но не оба сразу.

        Args:
            until_done (bool): Определяет, продолжать ли действовать до тех пор, пока агент не будет завершен и не потребуются дополнительные стимулы.
            n (int): Количество действий для выполнения. По умолчанию None.
            return_actions (bool): Определяет, возвращать ли действия или нет. По умолчанию False.
        """
        ...
```

#### Внутренние функции:
- `aux_pre_act()`:
  ```python
   def aux_pre_act():
            """
             Функция, выполняющаяся перед каждым действием агента.

             Описание:
                 В настоящее время функция пуста и не выполняет никаких действий.
                 Предположительно, она предназначена для выполнения каких-либо предварительных действий
                 перед каждым шагом агента, но в текущей реализации не используется.
             """
            ...
  ```
- `aux_act_once()`:
   ```python
   @repeat_on_error(retries=5, exceptions=[KeyError, TypeError])
        def aux_act_once():
            """
            Выполняет ровно одно действие агента.

            Описание:
                Эта функция отвечает за выполнение одного шага действия агента.
                Она вызывает метод `_produce_message()` для получения сообщения от агента,
                затем извлекает когнитивное состояние и действие из сообщения.
                Полученные действие добавляется в буфер действий агента,
                а когнитивное состояние обновляется.
                После этого действие сохраняется в памяти агента
                и отображается с использованием метода `_display_communication()`.
                В завершение, метод проходит по списку умственных способностей агента
                и вызывает метод `process_action()` для каждой из них,
                чтобы обработать действие и вызвать побочные эффекты.

            Returns:
                Tuple[str, Dict]: Кортеж, содержащий роль и содержимое сообщения.

            Raises:
                KeyError: Если в содержимом сообщения отсутствуют необходимые ключи.
                TypeError: Если содержимое сообщения имеет неверный тип.
            """
            ...
   ```

### `listen`
```python
@transactional
    def listen(
        self,
        speech,
        source: AgentOrWorld = None,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Слушает другого агента (искусственного или человека) и обновляет свое внутреннее когнитивное состояние.

        Args:
            speech (str): Речь для прослушивания.
            source (AgentOrWorld, optional): Источник речи. По умолчанию None.
        """
        ...
```

### `socialize`
```python
 def socialize(
        self,
        social_description: str,
        source: AgentOrWorld = None,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Воспринимает социальный стимул через описание и обновляет свое внутреннее когнитивное состояние.

        Args:
            social_description (str): Описание социального стимула.
            source (AgentOrWorld, optional): Источник социального стимула. По умолчанию None.
        """
        ...
```

### `see`
```python
def see(
        self,
        visual_description,
        source: AgentOrWorld = None,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Воспринимает визуальный стимул через описание и обновляет свое внутреннее когнитивное состояние.

        Args:
            visual_description (str): Описание визуального стимула.
            source (AgentOrWorld, optional): Источник визуального стимула. По умолчанию None.
        """
        ...
```

### `think`
```python
 def think(self, thought, max_content_length=default["max_content_display_length"]):
        """
        Заставляет агента подумать о чем-то и обновляет свое внутреннее когнитивное состояние.

        Args:
            thought (str): Мысль для обдумывания.
            max_content_length (int, optional): Максимальная длина содержимого. По умолчанию значение из `default["max_content_display_length"]`.
        """
        ...
```

### `internalize_goal`
```python
 def internalize_goal(
        self, goal, max_content_length=default["max_content_display_length"]
    ):
        """
        Интернализует цель и обновляет свое внутреннее когнитивное состояние.

        Args:
            goal (str): Цель для интернализации.
            max_content_length (int, optional): Максимальная длина содержимого. По умолчанию значение из `default["max_content_display_length"]`.
        """
        ...
```

### `_observe`
```python
@transactional
    def _observe(self, stimulus, max_content_length=default["max_content_display_length"]):
        """
        Наблюдает за стимулом и обновляет свое внутреннее когнитивное состояние.

        Args:
            stimulus (dict): Стимул для наблюдения.
            max_content_length (int, optional): Максимальная длина содержимого. По умолчанию значение из `default["max_content_display_length"]`.
        """
        ...
```

### `listen_and_act`
```python
@transactional
    def listen_and_act(
        self,
        speech,
        return_actions=False,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Комбинированный метод, объединяющий методы `listen` и `act`.

        Args:
            speech (str): Речь для прослушивания.
            return_actions (bool, optional): Определяет, возвращать ли действия или нет. По умолчанию False.
            max_content_length (int, optional): Максимальная длина содержимого. По умолчанию значение из `default["max_content_display_length"]`.
        """
        ...
```

### `see_and_act`
```python
 @transactional
    def see_and_act(
        self,
        visual_description,
        return_actions=False,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Комбинированный метод, объединяющий методы `see` и `act`.

        Args:
            visual_description (str): Описание визуального стимула.
            return_actions (bool, optional): Определяет, возвращать ли действия или нет. По умолчанию False.
            max_content_length (int, optional): Максимальная длина содержимого. По умолчанию значение из `default["max_content_display_length"]`.
        """
        ...
```

### `think_and_act`
```python
@transactional
    def think_and_act(
        self,
        thought,
        return_actions=False,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Комбинированный метод, объединяющий методы `think` и `act`.

        Args:
            thought (str): Мысль для обдумывания.
            return_actions (bool, optional): Определяет, возвращать ли действия или нет. По умолчанию False.
            max_content_length (int, optional): Максимальная длина содержимого. По умолчанию значение из `default["max_content_display_length"]`.
        """
        ...
```

### `read_documents_from_folder`
```python
 def read_documents_from_folder(self, documents_path:str):
        """
        Считывает документы из каталога и загружает их в семантическую память.

        Args:
            documents_path (str): Путь к каталогу с документами.
        """
        ...
```

### `read_document_from_file`
```python
def read_document_from_file(self, file_path:str):
        """
        Считывает документ из файла и загружает его в семантическую память.

        Args:
            file_path (str): Путь к файлу документа.
        """
        ...
```

### `read_documents_from_web`
```python
 def read_documents_from_web(self, web_urls:list):
        """
        Считывает документы из веб-адресов и загружает их в семантическую память.

        Args:
            web_urls (list): Список веб-адресов документов.
        """
        ...
```

### `read_document_from_web`
```python
 def read_document_from_web(self, web_url:str):
        """
        Считывает документ из веб-адреса и загружает его в семантическую память.

        Args:
            web_url (str): Веб-адрес документа.
        """
        ...
```

### `move_to`
```python
@transactional
    def move_to(self, location, context=[]):
        """
        Перемещается в новое местоположение и обновляет свое внутреннее когнитивное состояние.

        Args:
            location (str): Новое местоположение.
            context (list, optional): Контекст местоположения. По умолчанию [].
        """
        ...
```

### `change_context`
```python
 @transactional
    def change_context(self, context: list):
        """
        Изменяет контекст и обновляет свое внутреннее когнитивное состояние.

        Args:
            context (list): Новый контекст.
        """
        ...
```

### `make_agent_accessible`
```python
 @transactional
    def make_agent_accessible(
        self,
        agent: Self,
        relation_description: str = "An agent I can currently interact with.",
    ):
        """
        Делает агента доступным для этого агента.

        Args:
            agent (Self): Агент, которого нужно сделать доступным.
            relation_description (str, optional): Описание отношения. По умолчанию "An agent I can currently interact with.".
        """
        ...
```

### `make_agent_inaccessible`
```python
 @transactional
    def make_agent_inaccessible(self, agent: Self):
        """
        Делает агента недоступным для этого агента.

        Args:
            agent (Self): Агент, которого нужно сделать недоступным.
        """
        ...
```

### `make_all_agents_inaccessible`
```python
 @transactional
    def make_all_agents_inaccessible(self):
        """
        Делает всех агентов недоступными для этого агента.
        """
        ...
```

### `_produce_message`
```python
 @transactional
    def _produce_message(self):
        """
        Создает сообщение для отправки в OpenAI API.

        Returns:
            Tuple[str, dict]: Роль и содержимое сообщения.
        """
        ...
```

### `_update_cognitive_state`
```python
 @transactional
    def _update_cognitive_state(
        self, goals=None, context=None, attention=None, emotions=None
    ):
        """
        Обновляет когнитивное состояние TinyPerson.

        Args:
            goals (list, optional): Цели. По умолчанию None.
            context (list, optional): Контекст. По умолчанию None.
            attention (str, optional): Внимание. По умолчанию None.
            emotions (str, optional): Эмоции. По умолчанию None.
        """
        ...
```

### `store_in_memory`
```python
def store_in_memory(self, value: Any) -> list:
    """
    Сохраняет значение в памяти агента.

    Args:
        value (Any): Значение для сохранения в памяти.

    Returns:
        list: Список сохраненных значений в эпизодической памяти.
    """
    ...
```

### `optimize_memory`
```python
def optimize_memory(self):
    """
    Оптимизирует память агента.
    """
    ...
```

### `retrieve_memories`
```python
def retrieve_memories(self, first_n: int, last_n: int, include_omission_info:bool=True, max_content_length:int=None) -> list:
    """
    Извлекает воспоминания из памяти агента.

    Args:
        first_n (int): Количество первых воспоминаний для извлечения.
        last_n (int): Количество последних воспоминаний для извлечения.
        include_omission_info (bool, optional): Включать ли информацию об опущениях. По умолчанию True.
        max_content_length (int, optional): Максимальная длина содержимого воспоминаний. По умолчанию None.

    Returns:
        list: Список извлеченных воспоминаний.
    """
    ...
```

### `retrieve_recent_memories`
```python
def retrieve_recent_memories(self, max_content_length:int=None) -> list:
    """
    Извлекает последние воспоминания агента.

    Args:
        max_content_length (int, optional): Максимальная длина содержимого воспоминаний. По умолчанию None.

    Returns:
        list: Список извлеченных воспоминаний.
    """
    ...
```

### `retrieve_relevant_memories`
```python
 def retrieve_relevant_memories(self, relevance_target:str, top_k=20) -> list:
        """
        Извлекает релевантные воспоминания из семантической памяти.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int, optional): Количество лучших воспоминаний для извлечения. По умолчанию 20.

        Returns:
            list: Список извлеченных воспоминаний.
        """
        ...
```

### `retrieve_relevant_memories_for_current_context`
```python
def retrieve_relevant_memories_for_current_context(self, top_k=7) -> list:
        """
        Извлекает релевантные воспоминания для текущего контекста.

        Args:
            top_k (int, optional): Количество лучших воспоминаний для извлечения. По умолчанию 7.

        Returns:
            list: Список извлеченных воспоминаний.
        """
        ...
```

### `_display_communication`
```python
 def _display_communication(
        self,
        role,
        content,
        kind,
        simplified=True,
        max_content_length=default["max_content_display_length"],
    ):
        """
        Отображает текущее сообщение и сохраняет его в буфере для последующего использования.

        Args:
            role (str): Роль отправителя сообщения.
            content (dict): Содержимое сообщения.
            kind (str): Тип сообщения ("stimuli" или "action").
            simplified (bool, optional): Упрощенный формат вывода. По умолчанию True.
            max_content_length (int, optional): Максимальная длина содержимого для отображения. По умолчанию используется значение из `default["max_content_display_length"]`.

        Raises:
            ValueError: Если указан неизвестный тип сообщения.
        """
        ...
```

### `_push_and_display_latest_communication`
```python
 def _push_and_display_latest_communication(self, communication):
        """
        Добавляет последнее сообщение в буфер коммуникаций агента и отображает его.

        Args:
            communication (dict): Словарь, содержащий информацию о сообщении (тип, содержимое, источник, цель и отрендеренное представление).

        Описание:
            Этот метод добавляет информацию о последнем сообщении в буфер `_displayed_communications_buffer` агента
            и выводит на экран отрендеренное представление сообщения.
        """
        ...
```

### `pop_and_display_latest_communications`
```python
def pop_and_display_latest_communications(self):
        """
        Извлекает последние сообщения из буфера и отображает их.

        Returns:
            list: Список извлеченных сообщений.
        """
        ...
```

### `clear_communications_buffer`
```python
def clear_communications_buffer(self):
        """
        Очищает буфер коммуникаций агента.
        """
        ...
```

### `pop_latest_actions