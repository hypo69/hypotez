# Модуль `tiny_person`

## Обзор

Модуль `tiny_person` предназначен для создания и управления виртуальными агентами (TinyPerson) в рамках симуляции. Он включает в себя классы для представления агентов, управления их памятью, когнитивными функциями и взаимодействием с окружением.

## Подробнее

Модуль предоставляет класс `TinyPerson`, который позволяет создавать симулированных персонажей с уникальными характеристиками, воспоминаниями и моделями поведения. Эти агенты могут взаимодействовать друг с другом и с окружением, выполняя действия и реагируя на стимулы.

## Классы

### `TinyPerson`

**Описание**: Класс `TinyPerson` представляет собой симулированного персонажа в виртуальной вселенной.

**Наследует**:
- `JsonSerializableRegistry`: Обеспечивает возможность сериализации и десериализации объектов класса в формат JSON.

**Атрибуты**:

- `MAX_ACTIONS_BEFORE_DONE` (int): Максимальное количество действий, которое агент может выполнить до того, как потребуется дополнительный стимул (по умолчанию: 15).
- `PP_TEXT_WIDTH` (int): Ширина текста для форматированного вывода (по умолчанию: 100).
- `serializable_attributes` (list): Список атрибутов, которые будут сериализованы при сохранении состояния агента.
- `serializable_attributes_renaming` (dict): Словарь, определяющий переименование атрибутов при сериализации.
- `all_agents` (dict): Словарь, содержащий всех созданных агентов (имя -> агент).
- `communication_style` (str): Стиль коммуникации для всех агентов ("simplified" или "full").
- `communication_display` (bool): Флаг, определяющий, отображать ли коммуникацию агентов (True для интерактивных приложений).
- `name` (str): Имя агента.
- `episodic_memory` (EpisodicMemory): Эпизодическая память агента.
- `semantic_memory` (SemanticMemory): Семантическая память агента.
- `_mental_faculties` (list): Список когнитивных функций агента.
- `current_messages` (list): Список текущих сообщений агента.
- `environment` (Environment): Текущее окружение, в котором действует агент.
- `_actions_buffer` (list): Список действий, выполненных агентом, но еще не обработанных окружением.
- `_accessible_agents` (list): Список агентов, с которыми данный агент может взаимодействовать.
- `_displayed_communications_buffer` (list): Буфер отображаемых коммуникаций агента.
- `_persona` (dict): Словарь, содержащий описание личности агента (имя, возраст, национальность и т.д.).
- `_mental_state` (dict): Словарь, содержащий текущее психическое состояние агента (время, местоположение, контекст, цели и т.д.).
- `_extended_agent_summary` (str): Расширенное описание агента.
- `_prompt_template_path` (str): Путь к шаблону промпта агента.
- `_init_system_message` (str): Исходное системное сообщение агента.

**Принцип работы**:

Класс `TinyPerson` предоставляет функциональность для создания и управления виртуальными агентами. При инициализации агента задаются его имя, память (эпизодическая и семантическая) и когнитивные функции. Класс также управляет состоянием агента, включая его местоположение, контекст и цели.

**Методы**:

- `__init__(name: str = None, episodic_memory = None, semantic_memory = None, mental_faculties: list = None)`
- `_post_init(**kwargs)`
- `_rename(new_name: str)`
- `generate_agent_system_prompt()`
- `reset_prompt()`
- `get(key)`
- `import_fragment(path)`
- `include_persona_definitions(additional_definitions: dict)`
- `define(key, value, merge: bool = True, overwrite_scalars: bool = True)`
- `define_relationships(relationships, replace: bool = True)`
- `clear_relationships()`
- `related_to(other_agent, description, symmetric_description = None)`
- `add_mental_faculties(mental_faculties)`
- `add_mental_faculty(faculty)`
- `act(until_done: bool = True, n = None, return_actions: bool = False, max_content_length = default["max_content_display_length"])`
- `listen(speech, source: AgentOrWorld = None, max_content_length = default["max_content_display_length"])`
- `socialize(social_description: str, source: AgentOrWorld = None, max_content_length = default["max_content_display_length"])`
- `see(visual_description, source: AgentOrWorld = None, max_content_length = default["max_content_display_length"])`
- `think(thought, max_content_length = default["max_content_display_length"])`
- `internalize_goal(goal, max_content_length = default["max_content_display_length"])`
- `_observe(stimulus, max_content_length = default["max_content_display_length"])`
- `listen_and_act(speech, return_actions: bool = False, max_content_length = default["max_content_display_length"])`
- `see_and_act(visual_description, return_actions: bool = False, max_content_length = default["max_content_display_length"])`
- `think_and_act(thought, return_actions: bool = False, max_content_length = default["max_content_display_length"])`
- `read_documents_from_folder(documents_path: str)`
- `read_document_from_file(file_path: str)`
- `read_documents_from_web(web_urls: list)`
- `read_document_from_web(web_url: str)`
- `move_to(location, context: list = [])`
- `change_context(context: list)`
- `make_agent_accessible(agent: Self, relation_description: str = "An agent I can currently interact with.")`
- `make_agent_inaccessible(agent: Self)`
- `make_all_agents_inaccessible()`
- `_produce_message()`
- `_update_cognitive_state(goals = None, context = None, attention = None, emotions = None)`
- `store_in_memory(value: Any) -> list`
- `optimize_memory()`
- `retrieve_memories(first_n: int, last_n: int, include_omission_info: bool = True, max_content_length: int = None) -> list`
- `retrieve_recent_memories(max_content_length: int = None) -> list`
- `retrieve_relevant_memories(relevance_target: str, top_k = 20) -> list`
- `retrieve_relevant_memories_for_current_context(top_k = 7) -> list`
- `_display_communication(role, content, kind, simplified: bool = True, max_content_length = default["max_content_display_length"])`
- `_push_and_display_latest_communication(communication)`
- `pop_and_display_latest_communications()`
- `clear_communications_buffer()`
- `pop_latest_actions() -> list`
- `pop_actions_and_get_contents_for(action_type: str, only_last_action: bool = True) -> list`
- `__repr__()`
- `minibio(extended: bool = True)`
- `pp_current_interactions(simplified: bool = True, skip_system: bool = True, max_content_length = default["max_content_display_length"])`
- `pretty_current_interactions(simplified: bool = True, skip_system: bool = True, max_content_length = default["max_content_display_length"], first_n = None, last_n = None, include_omission_info: bool = True)`
- `_pretty_stimuli(role, content, simplified: bool = True, max_content_length = default["max_content_display_length"]) -> list`
- `_pretty_action(role, content, simplified: bool = True, max_content_length = default["max_content_display_length"]) -> str`
- `_pretty_timestamp(role, timestamp) -> str`
- `iso_datetime() -> str`
- `save_specification(path, include_mental_faculties: bool = True, include_memory: bool = False)`
- `load_specification(path_or_dict, suppress_mental_faculties: bool = False, suppress_memory: bool = False, auto_rename_agent: bool = False, new_agent_name = None)`
- `encode_complete_state() -> dict`
- `decode_complete_state(state: dict) -> Self`
- `create_new_agent_from_current_spec(new_name: str) -> Self`
- `add_agent(agent)`
- `has_agent(agent_name: str) -> bool`
- `set_simulation_for_free_agents(simulation)`
- `get_agent_by_name(name)`
- `all_agents_names() -> list`
- `clear_agents()`

## Методы класса

### `__init__`

```python
def __init__(self, name: str = None, 
                 episodic_memory=None,
                 semantic_memory=None,
                 mental_faculties:list=None):
    """
    Creates a TinyPerson.

    Args:
        name (str): The name of the TinyPerson. Either this or spec_path must be specified.
        episodic_memory (EpisodicMemory, optional): The memory implementation to use. Defaults to EpisodicMemory().
        semantic_memory (SemanticMemory, optional): The memory implementation to use. Defaults to SemanticMemory().
        mental_faculties (list, optional): A list of mental faculties to add to the agent. Defaults to None.
    """
```

**Назначение**: Инициализирует объект `TinyPerson`.

**Параметры**:
- `name` (str, optional): Имя персонажа.
- `episodic_memory` (EpisodicMemory, optional): Эпизодическая память агента.
- `semantic_memory` (SemanticMemory, optional): Семантическая память агента.
- `mental_faculties` (list, optional): Список когнитивных функций агента.

**Как работает функция**:
- Функция инициализирует экземпляр класса `TinyPerson`. Если `episodic_memory` или `semantic_memory` не переданы, они будут инициализированы позже в методе `_post_init`.
- Проверяет, что имя агента указано.

### `_post_init`

```python
def _post_init(self, **kwargs):
    """
    This will run after __init__, since the class has the @post_init decorator.
    It is convenient to separate some of the initialization processes to make deserialize easier.
    """
```

**Назначение**: Выполняет постобработку после инициализации объекта `TinyPerson`.

**Параметры**:
- `kwargs` (dict): Дополнительные параметры.

**Как работает функция**:
- Инициализирует значения по умолчанию для атрибутов агента, таких как `current_messages`, `environment`, `_actions_buffer`, `_accessible_agents` и `_displayed_communications_buffer`.
- Если `episodic_memory` или `semantic_memory` не были установлены при инициализации, они создаются здесь.
- Создает конфигурационные словари `_persona` и `_mental_state`, если они еще не существуют.
- Обрабатывает переименование агента, если указано в `kwargs`.
- Регистрирует агента в глобальном списке агентов (`TinyPerson.all_agents`).
- Сбрасывает промпт агента.

**Внутренние функции**:
- Нет.

### `_rename`

```python
def _rename(self, new_name:str):    
    """
    Renames the agent.

    Args:
        new_name (str): The new name of the agent.
    """
    self.name = new_name
    self._persona["name"] = self.name
```

**Назначение**: Переименовывает агента.

**Параметры**:
- `new_name` (str): Новое имя агента.

**Как работает функция**:
- Функция изменяет имя агента и обновляет имя в словаре `_persona`.

### `generate_agent_system_prompt`

```python
def generate_agent_system_prompt(self):
    """
    Generates the system prompt for the agent.

    Returns:
        str: The generated system prompt.
    """
    with open(self._prompt_template_path, "r") as f:
        agent_prompt_template = f.read()

    # let's operate on top of a copy of the configuration, because we'll need to add more variables, etc.
    template_variables = self._persona.copy()    
    template_variables["persona"] = json.dumps(self._persona.copy(), indent=4)    

    # Prepare additional action definitions and constraints
    actions_definitions_prompt = ""
    actions_constraints_prompt = ""
    for faculty in self._mental_faculties:
        actions_definitions_prompt += f"{faculty.actions_definitions_prompt()}\\n"
        actions_constraints_prompt += f"{faculty.actions_constraints_prompt()}\\n"

    # Make the additional prompt pieces available to the template. 
    # Identation here is to align with the text structure in the template.
    template_variables['actions_definitions_prompt'] = textwrap.indent(actions_definitions_prompt.strip(), "  ")
    template_variables['actions_constraints_prompt'] = textwrap.indent(actions_constraints_prompt.strip(), "  ")

    # RAI prompt components, if requested
    template_variables = utils.add_rai_template_variables_if_enabled(template_variables)

    return chevron.render(agent_prompt_template, template_variables)
```

**Назначение**: Генерирует системный промпт для агента на основе шаблона и конфигурации.

**Возвращает**:
- `str`: Сгенерированный системный промпт.

**Как работает функция**:
- Читает шаблон промпта агента из файла, указанного в `self._prompt_template_path`.
- Создает копию словаря `self._persona` для использования в качестве переменных шаблона.
- Подготавливает определения и ограничения действий на основе когнитивных функций агента.
- Добавляет дополнительные переменные шаблона, если включены компоненты RAI.
- Визуализирует шаблон с использованием библиотеки `chevron` и возвращает результат.

### `reset_prompt`

```python
def reset_prompt(self):
    """
    Resets the agent's prompt.
    """

    # render the template with the current configuration
    self._init_system_message = self.generate_agent_system_prompt()

    # TODO actually, figure out another way to update agent state without "changing history"

    # reset system message
    self.current_messages = [
        {"role": "system", "content": self._init_system_message}
    ]

    # sets up the actual interaction messages to use for prompting
    self.current_messages += self.retrieve_recent_memories()

    # add a final user message, which is neither stimuli or action, to instigate the agent to act properly
    self.current_messages.append({"role": "user", 
                                  "content": "Now you **must** generate a sequence of actions following your interaction directives, " +\\
                                             "and complying with **all** instructions and contraints related to the action you use." +\\
                                             "DO NOT repeat the exact same action more than once in a row!" +\\
                                             "DO NOT keep saying or doing very similar things, but instead try to adapt and make the interactions look natural." +\\
                                             "These actions **MUST** be rendered following the JSON specification perfectly, including all required keys (even if their value is empty), **ALWAYS**."
                                 })
```

**Назначение**: Сбрасывает промпт агента, генерируя новый системный промпт и восстанавливая историю взаимодействия.

**Как работает функция**:
- Генерирует системный промпт с использованием текущей конфигурации агента.
- Сбрасывает текущие сообщения агента, устанавливая системное сообщение в качестве первого сообщения.
- Извлекает недавние воспоминания агента и добавляет их к текущим сообщениям.
- Добавляет финальное пользовательское сообщение, чтобы побудить агента к действию.

### `get`

```python
def get(self, key):
    """
    Returns the definition of a key in the TinyPerson's configuration.
    """
    return self._persona.get(key, None)
```

**Назначение**: Возвращает значение ключа из конфигурации агента (`_persona`).

**Параметры**:
- `key` (str): Ключ для поиска в конфигурации.

**Возвращает**:
- Значение ключа или `None`, если ключ не найден.

### `import_fragment`

```python
@transactional
def import_fragment(self, path):
    """
    Imports a fragment of a persona configuration from a JSON file.
    """
    with open(path, "r") as f:
        fragment = json.load(f)

    # check the type is "Fragment" and that there's also a "persona" key
    if fragment.get("type", None) == "Fragment" and fragment.get("persona", None) is not None:
        self.include_persona_definitions(fragment["persona"])
    else:
        raise ValueError("The imported JSON file must be a valid fragment of a persona configuration.")

    # must reset prompt after adding to configuration
    self.reset_prompt()
```

**Назначение**: Импортирует фрагмент конфигурации персонажа из JSON-файла.

**Параметры**:
- `path` (str): Путь к JSON-файлу.

**Как работает функция**:
- Открывает JSON-файл по указанному пути.
- Проверяет, что файл содержит фрагмент конфигурации персонажа с типом "Fragment" и ключом "persona".
- Включает определения персонажа из фрагмента в текущую конфигурацию.
- Сбрасывает промпт агента.

### `include_persona_definitions`

```python
@transactional
def include_persona_definitions(self, additional_definitions: dict):
    """
    Imports a set of definitions into the TinyPerson. They will be merged with the current configuration.
    It is also a convenient way to include multiple bundled definitions into the agent.

    Args:
        additional_definitions (dict): The additional definitions to import.
    """

    self._persona = utils.merge_dicts(self._persona, additional_definitions)

    # must reset prompt after adding to configuration
    self.reset_prompt()
```

**Назначение**: Импортирует набор определений в `TinyPerson`.

**Параметры**:
- `additional_definitions` (dict): Дополнительные определения для импорта.

**Как работает функция**:
- Объединяет переданные определения с текущей конфигурацией агента.
- Сбрасывает промпт агента.

### `define`

```python
@transactional
def define(self, key, value, merge=True, overwrite_scalars=True):
    """
    Define a value to the TinyPerson's persona configuration. Value can either be a scalar or a dictionary.
    If the value is a dictionary or list, you can choose to merge it with the existing value or replace it. 
    If the value is a scalar, you can choose to overwrite the existing value or not.

    Args:
        key (str): The key to define.
        value (Any): The value to define.
        merge (bool, optional): Whether to merge the dict/list values with the existing values or replace them. Defaults to True.
        overwrite_scalars (bool, optional): Whether to overwrite scalar values or not. Defaults to True.
    """

    # dedent value if it is a string
    if isinstance(value, str):
        value = textwrap.dedent(value)

    # if the value is a dictionary, we can choose to merge it with the existing value or replace it
    if isinstance(value, dict) or isinstance(value, list):
        if merge:
            self._persona = utils.merge_dicts(self._persona, {key: value})
        else:
            self._persona[key] = value

    # if the value is a scalar, we can choose to overwrite it or not
    elif overwrite_scalars or (key not in self._persona):
        self._persona[key] = value

    else:
        raise ValueError(f"The key '{key}' already exists in the persona configuration and overwrite_scalars is set to False.")


    # must reset prompt after adding to configuration
    self.reset_prompt()
```

**Назначение**: Определяет значение в конфигурации персонажа `TinyPerson`.

**Параметры**:
- `key` (str): Ключ для определения.
- `value` (Any): Значение для определения.
- `merge` (bool, optional): Определяет, нужно ли объединять значения dict/list с существующими значениями или заменять их. По умолчанию `True`.
- `overwrite_scalars` (bool, optional): Определяет, нужно ли перезаписывать скалярные значения или нет. По умолчанию `True`.

**Как работает функция**:
- Если значение является строкой, удаляет отступы.
- Если значение является словарем или списком, объединяет или заменяет его в зависимости от параметра `merge`.
- Если значение является скаляром, перезаписывает его или нет в зависимости от параметра `overwrite_scalars`.
- Сбрасывает промпт агента.

### `define_relationships`

```python
@transactional
def define_relationships(self, relationships, replace=True):
    """
    Defines or updates the TinyPerson's relationships.

    Args:
        relationships (list or dict): The relationships to add or replace. Either a list of dicts mapping agent names to relationship descriptions,
          or a single dict mapping one agent name to its relationship description.
        replace (bool, optional): Whether to replace the current relationships or just add to them. Defaults to True.
    """

    if (replace == True) and (isinstance(relationships, list)):
        self._persona['relationships'] = relationships

    elif replace == False:
        current_relationships = self._persona['relationships']
        if isinstance(relationships, list):
            for r in relationships:
                current_relationships.append(r)

        elif isinstance(relationships, dict) and len(relationships) == 2: #{"Name": ..., "Description": ...}
            current_relationships.append(relationships)

        else:
            raise Exception("Only one key-value pair is allowed in the relationships dict.")

    else:
        raise Exception("Invalid arguments for define_relationships.")
```

**Назначение**: Определяет или обновляет отношения `TinyPerson`.

**Параметры**:
- `relationships` (list или dict): Отношения для добавления или замены.
- `replace` (bool, optional): Определяет, нужно ли заменять текущие отношения или просто добавлять к ним. По умолчанию `True`.

**Как работает функция**:
- Заменяет текущие отношения, если `replace` равен `True` и `relationships` является списком.
- Добавляет новые отношения, если `replace` равен `False`.

### `clear_relationships`

```python
@transactional
def clear_relationships(self):
    """
    Clears the TinyPerson's relationships.
    """
    self._persona['relationships'] = []  

    return self      
```

**Назначение**: Очищает отношения `TinyPerson`.

**Как работает функция**:
- Устанавливает `relationships` в пустой список.

### `related_to`

```python
@transactional
def related_to(self, other_agent, description, symmetric_description=None):
    """
    Defines a relationship between this agent and another agent.

    Args:
        other_agent (TinyPerson): The other agent.
        description (str): The description of the relationship.
        symmetric (bool): Whether the relationship is symmetric or not. That is, 
          if the relationship is defined for both agents.

    Returns:
        TinyPerson: The agent itself, to facilitate chaining.
    """
    self.define_relationships([{"Name": other_agent.name, "Description": description}], replace=False)
    if symmetric_description is not None:
        other_agent.define_relationships([{"Name": self.name, "Description": symmetric_description}], replace=False)

    return self
```

**Назначение**: Определяет отношения между этим агентом и другим агентом.

**Параметры**:
- `other_agent` (TinyPerson): Другой агент.
- `description` (str): Описание отношений.
- `symmetric_description` (str, optional): Симметричное описание, если отношение симметричное.

**Как работает функция**:
- Определяет отношения между этим агентом и другим агентом, вызывая `define_relationships`. Если предоставлено `symmetric_description`, определяет также отношения другого агента к этому агенту.

### `add_mental_faculties`

```python
def add_mental_faculties(self, mental_faculties):
    """
    Adds a list of mental faculties to the agent.
    """
    for faculty in mental_faculties:
        self.add_mental_faculty(faculty)

    return self
```

**Назначение**: Добавляет список когнитивных функций агенту.

**Параметры**:
- `mental_faculties` (list): Список когнитивных функций.

**Как работает функция**:
- Перебирает список `mental_faculties` и вызывает `add_mental_faculty` для каждой функции.

### `add_mental_faculty`

```python
def add_mental_faculty(self, faculty):
    """
    Adds a mental faculty to the agent.
    """
    # check if the faculty is already there or not
    if faculty not in self._mental_faculties:
        self._mental_faculties.append(faculty)
    else:
        raise Exception(f"The mental faculty {faculty} is already present in the agent.")

    return self
```

**Назначение**: Добавляет когнитивную функцию агенту.

**Параметры**:
- `faculty`: Когнитивная функция.

**Как работает функция**:
- Проверяет, присутствует ли функция в `_mental_faculties`. Если нет, добавляет её.

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
    Acts in the environment and updates its internal cognitive state.
    Either acts until the agent is done and needs additional stimuli, or acts a fixed number of times,
    but not both.

    Args:
        until_done (bool): Whether to keep acting until the agent is done and needs additional stimuli.
        n (int): The number of actions to perform. Defaults to None.
        return_actions (bool): Whether to return the actions or not. Defaults to False.
    """
```

**Назначение**: Действует в окружении и обновляет своё внутреннее когнитивное состояние.

**Параметры**:
- `until_done` (bool): Продолжать действовать, пока агент не закончит и не потребуются дополнительные стимулы.
- `n` (int): Количество действий для выполнения.
- `return_actions` (bool): Возвращать ли действия.

**Как работает функция**:
- Выбирает между действием до завершения или выполнением фиксированного количества действий.
- Функция `aux_pre_act` выполняет предварительные действия перед каждым действием.
- Функция `aux_act_once` выполняет одно действие, обрабатывая ошибки и сохраняя результаты.
- В цикле выполняется последовательность действий, пока не будет достигнуто условие завершения или выполнено заданное количество действий.

**Внутренние функции**:
- `aux_pre_act`: Выполняет предварительные действия перед каждым действием.
- `aux_act_once`: Выполняет одно действие, обрабатывая ошибки и сохраняя результаты.

### `listen`

```python
def listen(
    self,
    speech,
    source: AgentOrWorld = None,
    max_content_length=default["max_content_display_length"],
):
    """
    Listens to another agent (artificial or human) and updates its internal cognitive state.

    Args:
        speech (str): The speech to listen to.
        source (AgentOrWorld, optional): The source of the speech. Defaults to None.
    """

    return self._observe(
        stimulus={
            "type": "CONVERSATION",
            "content": speech,
            "source": name_or_empty(source),
        },
        max_content_length=max_content_length,
    )
```

**Назначение**: Слушает другого агента (искусственного или человека) и обновляет своё внутреннее когнитивное состояние.

**Параметры**:
- `speech` (str): Речь для прослушивания.
- `source` (AgentOrWorld, optional): Источник речи.

**Как работает функция**:
- Создаёт стимул типа "CONVERSATION" и вызывает метод `_observe` для обработки стимула.

### `socialize`

```python
def socialize(
    self,
    social_description: str,
    source: AgentOrWorld = None,
    max_content_length=default["max_content_display_length"],
):
    """
    Perceives a social stimulus through a description and updates its internal cognitive state.

    Args:
        social_description (str): The description of the social stimulus.
        source (AgentOrWorld, optional): The source of the social stimulus. Defaults to None.
    """
    return self._observe(
        stimulus={
            "type": "SOCIAL",
            "content": social_description,
            "source": name_or_empty(source),
        },
        max_content_length=max_content_length,
    )
```

**Назначение**: Воспринимает социальный стимул через описание и обновляет своё внутреннее когнитивное состояние.

**Параметры**:
- `social_description` (str): Описание социального стимула.
- `source` (AgentOrWorld, optional): Источник социального стимула.

**Как работает функция**:
- Создаёт стимул типа "SOCIAL" и вызывает метод `_observe` для обработки стимула.

### `see`

```python
def see(
    self,
    visual_description,
    source: AgentOrWorld = None,
    max_content_length=default["max_content_display_length"],
):
    """
    Perceives a visual stimulus through a description and updates its internal cognitive state.

    Args:
        visual_description (str): The description of the visual stimulus.
        source (AgentOrWorld, optional): The source of the visual stimulus. Defaults to None.
    """
    return self._observe(
        stimulus={
            "type": "VISUAL",
            "content": visual_description,
            "source": name_or_empty(source),
        },
        max_content_length=max_content_length,
    )
```

**Назначение**: Воспринимает визуальный стимул через описание и обновляет своё внутреннее когнитивное состояние.

**Параметры**:
- `visual_description` (str): Описание визуального стимула.
- `source` (AgentOrWorld, optional): Источник визуального стимула.

**Как работает функция**:
- Создаёт стимул типа "VISUAL" и вызывает метод `_observe` для обработки стимула.

### `think`

```python
def think(self, thought, max_content_length=default["max_content_display_length"]):
    """
    Forces the agent to think about something and updates its internal cognitive state.
    """
    return self._observe(
        stimulus={
            "type": "THOUGHT",
            "content": thought,
            "source": name_or_empty(self),
        },
        max_content_length=max_content_length,
    )
```

**Назначение**: Заставляет агента подумать о чём-то и обновляет своё внутреннее когнитивное состояние.

**Параметры**:
- `thought` (str): Мысль.

**Как работает функция**:
- Создаёт стимул типа "THOUGHT" и вызывает метод `_observe` для обработки стимула.

### `internalize_goal`

```python
def internalize_goal(
    self, goal, max_content_length=default["max_content_display_length"]
):
    """
    Internalizes a goal and updates its internal cognitive state.
    """
    return self._observe(
        stimulus={
            "type": "INTERNAL_GOAL_FORMULATION",
            "content": goal,
            "source": name_or_empty(self),
        },
        max_content_length=max_content_length,
    )
```

**Назначение**: Интериоризирует цель и обновляет своё внутреннее когнитивное состояние.

**Параметры**:
- `goal` (str): Цель.

**Как работает функция**:
- Создаёт стимул типа "INTERNAL_GOAL_FORMULATION" и вызывает метод `_observe` для обработки стимула.

### `_observe`

```python
@transactional
def _observe(self, stimulus, max_content_length=default["max_content_display_length"]):
    """
    Observes a stimulus and updates its internal cognitive state.
    """
    stimuli = [stimulus]

    content = {"stimuli": stimuli}

    logger.debug(f"[{self.name}] Observing stimuli: {content}")

    # whatever comes from the outside will be interpreted as coming from 'user', simply because
    # this is the counterpart of 'assistant'

    self.store_in_memory({'role': 'user', 'content': content, 
                          'type': 'stimulus',
                          'simulation_timestamp': self.iso_datetime()})

    if TinyPerson.communication_display:
        self._display_communication(
            role="user",
            content=content,
            kind="stimuli",
            simplified=True,
            max_content_length=max_content_length,
        )

    return self  # allows easier chaining of methods