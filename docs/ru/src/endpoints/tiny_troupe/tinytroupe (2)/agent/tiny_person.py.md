# Модуль `tiny_person.py`

## Обзор

Модуль содержит класс `TinyPerson`, представляющий собой симуляцию личности в виртуальной среде TinyTroupe. Этот класс управляет поведением агентов, их памятью (эпизодической и семантической), ментальными способностями и взаимодействием с окружающей средой.

## Подробнее

Модуль предоставляет инструменты для создания, управления и взаимодействия с виртуальными агентами. `TinyPerson` может воспринимать стимулы из окружающей среды, принимать решения, действовать и изменять своё внутреннее состояние. Модуль также включает механизмы для сохранения и загрузки состояний агентов, что позволяет создавать сложные и динамические симуляции.

## Классы

### `TinyPerson`

**Описание**: Класс `TinyPerson` представляет собой виртуального агента, способного взаимодействовать с виртуальным миром TinyTroupe.

   **Принцип работы**:

   Класс управляет персональными данными агента (`_persona`), его ментальным состоянием (`_mental_state`), ментальными способностями (`_mental_faculties`), а также эпизодической и семантической памятью. Он также предоставляет методы для взаимодействия с окружающей средой, такие как восприятие стимулов, принятие решений и выполнение действий.

   **Аттрибуты**:

   - `name (str)`: Имя агента.
   - `episodic_memory (EpisodicMemory)`: Эпизодическая память агента.
   - `semantic_memory (SemanticMemory)`: Семантическая память агента.
   - `_persona (dict)`: Словарь, содержащий персональные данные агента (имя, возраст, национальность, профессия и т.д.).
   - `_mental_state (dict)`: Словарь, содержащий ментальное состояние агента (время, местоположение, контекст, цели, внимание, эмоции и т.д.).
   - `_mental_faculties (list)`: Список ментальных способностей агента.
   - `MAX_ACTIONS_BEFORE_DONE (int)`: Максимальное количество действий, которые агент может выполнить до того, как потребуется дополнительный стимул (равно 15).
   - `PP_TEXT_WIDTH (int)`: Ширина текста для отображения информации об агенте (равна 100).
   - `serializable_attributes (list)`: Список атрибутов, которые могут быть сериализованы.
   - `serializable_attributes_renaming (dict)`: Словарь, содержащий переименования атрибутов при сериализации.
   - `all_agents (dict)`: Словарь, содержащий всех созданных агентов (имя -> агент).
   - `communication_style (str)`: Стиль коммуникации для всех агентов ("simplified" или "full").
   - `communication_display (bool)`: Флаг, определяющий, нужно ли отображать коммуникации (True для интерактивных приложений).

   **Методы**:
   - `__init__(name: str = None, episodic_memory = None, semantic_memory = None, mental_faculties: list = None)`: Конструктор класса.
   - `_post_init(**kwargs)`: Выполняется после `__init__`, используется для дополнительной инициализации.
   - `generate_agent_system_prompt()`: Генерирует системное сообщение для агента на основе шаблона.
   - `reset_prompt()`: Сбрасывает текущий промпт агента.
   - `get(key)`: Возвращает значение ключа из конфигурации агента.
   - `import_fragment(path)`: Импортирует фрагмент конфигурации персонажа из JSON-файла.
   - `include_persona_definitions(additional_definitions: dict)`: Импортирует набор определений в конфигурацию персонажа.
   - `define(key, value, merge = True, overwrite_scalars = True)`: Определяет значение в конфигурации персонажа.
   - `define_relationships(relationships, replace = True)`: Определяет или обновляет отношения персонажа.
   - `clear_relationships()`: Очищает отношения персонажа.
   - `related_to(other_agent, description, symmetric_description = None)`: Определяет отношение между этим агентом и другим агентом.
   - `add_mental_faculties(mental_faculties)`: Добавляет список ментальных способностей агенту.
   - `add_mental_faculty(faculty)`: Добавляет ментальную способность агенту.
   - `act(until_done = True, n = None, return_actions = False, max_content_length = default["max_content_display_length"])`: Агент действует в окружающей среде и обновляет свое внутреннее когнитивное состояние.
   - `listen(speech, source: AgentOrWorld = None, max_content_length = default["max_content_display_length"])`: Слушает другого агента и обновляет свое внутреннее когнитивное состояние.
   - `socialize(social_description: str, source: AgentOrWorld = None, max_content_length = default["max_content_display_length"])`: Воспринимает социальный стимул через описание и обновляет свое внутреннее когнитивное состояние.
   - `see(visual_description, source: AgentOrWorld = None, max_content_length = default["max_content_display_length"])`: Воспринимает визуальный стимул через описание и обновляет свое внутреннее когнитивное состояние.
   - `think(thought, max_content_length = default["max_content_display_length"])`: Заставляет агента думать о чем-то и обновляет его внутреннее когнитивное состояние.
   - `internalize_goal(goal, max_content_length = default["max_content_display_length"])`: Усваивает цель и обновляет свое внутреннее когнитивное состояние.
   - `_observe(stimulus, max_content_length = default["max_content_display_length"])`: Наблюдает за стимулом и обновляет свое внутреннее когнитивное состояние.
   - `listen_and_act(speech, return_actions = False, max_content_length = default["max_content_display_length"])`: Комбинированный метод `listen` и `act`.
   - `see_and_act(visual_description, return_actions = False, max_content_length = default["max_content_display_length"])`: Комбинированный метод `see` и `act`.
   - `think_and_act(thought, return_actions = False, max_content_length = default["max_content_display_length"])`: Комбинированный метод `think` и `act`.
   - `read_documents_from_folder(documents_path: str)`: Читает документы из каталога и загружает их в семантическую память.
   - `read_document_from_file(file_path: str)`: Читает документ из файла и загружает его в семантическую память.
   - `read_documents_from_web(web_urls: list)`: Читает документы из веб-URL и загружает их в семантическую память.
   - `read_document_from_web(web_url: str)`: Читает документ из веб-URL и загружает его в семантическую память.
   - `move_to(location, context = [])`: Перемещается в новое местоположение и обновляет свое внутреннее когнитивное состояние.
   - `change_context(context: list)`: Изменяет контекст и обновляет свое внутреннее когнитивное состояние.
   - `make_agent_accessible(agent: Self, relation_description: str = "An agent I can currently interact with.")`: Делает агента доступным для этого агента.
   - `make_agent_inaccessible(agent: Self)`: Делает агента недоступным для этого агента.
   - `make_all_agents_inaccessible()`: Делает всех агентов недоступными для этого агента.
   - `_produce_message()`: Генерирует сообщение на основе текущего состояния агента.
   - `_update_cognitive_state(goals = None, context = None, attention = None, emotions = None)`: Обновляет когнитивное состояние TinyPerson.
   - `store_in_memory(value: Any) -> list`: Сохраняет значение в памяти.
   - `optimize_memory()`: Оптимизирует память.
   - `retrieve_memories(first_n: int, last_n: int, include_omission_info: bool = True, max_content_length: int = None) -> list`: Извлекает воспоминания из памяти.
   - `retrieve_recent_memories(max_content_length: int = None) -> list`: Извлекает последние воспоминания.
   - `retrieve_relevant_memories(relevance_target: str, top_k = 20) -> list`: Извлекает релевантные воспоминания.
   - `retrieve_relevant_memories_for_current_context(top_k = 7) -> list`: Извлекает релевантные воспоминания для текущего контекста.
   - `_display_communication(role, content, kind, simplified = True, max_content_length = default["max_content_display_length"])`: Отображает текущую коммуникацию и сохраняет ее в буфере.
   - `_push_and_display_latest_communication(communication)`: Добавляет последние коммуникации в буфер агента.
   - `pop_and_display_latest_communications()`: Извлекает последние коммуникации и отображает их.
   - `clear_communications_buffer()`: Очищает буфер коммуникаций.
   - `pop_latest_actions() -> list`: Возвращает последние действия, выполненные этим агентом.
   - `pop_actions_and_get_contents_for(action_type: str, only_last_action: bool = True) -> list`: Возвращает содержимое действий заданного типа, выполненных этим агентом.
   - `__repr__()`: Возвращает строковое представление объекта `TinyPerson`.
   - `minibio(extended = True)`: Возвращает мини-биографию `TinyPerson`.
   - `pp_current_interactions(simplified = True, skip_system = True, max_content_length = default["max_content_display_length"])`: Выводит в удобочитаемом формате текущие взаимодействия.
   - `pretty_current_interactions(simplified = True, skip_system = True, max_content_length = default["max_content_display_length"], first_n = None, last_n = None, include_omission_info: bool = True)`: Возвращает удобочитаемую строку с текущими сообщениями.
   - `_pretty_stimuli(role, content, simplified = True, max_content_length = default["max_content_display_length"]) -> list`: Форматирует стимулы для отображения.
   - `_pretty_action(role, content, simplified = True, max_content_length = default["max_content_display_length"]) -> str`: Форматирует действие для отображения.
   - `_pretty_timestamp(role, timestamp) -> str`: Форматирует временную метку для отображения.
   - `iso_datetime() -> str`: Возвращает текущую дату и время в формате ISO.
   - `save_specification(path, include_mental_faculties = True, include_memory = False)`: Сохраняет текущую конфигурацию в JSON-файл.
   - `load_specification(path_or_dict, suppress_mental_faculties = False, suppress_memory = False, auto_rename_agent = False, new_agent_name = None)`: Загружает спецификацию агента из JSON.
   - `encode_complete_state() -> dict`: Кодирует полное состояние `TinyPerson`, включая текущие сообщения, доступных агентов и т. д.
   - `decode_complete_state(state: dict) -> Self`: Загружает полное состояние `TinyPerson`.
   - `create_new_agent_from_current_spec(new_name: str) -> Self`: Создает нового агента на основе текущей спецификации агента.
   - `add_agent(agent)`: Добавляет агента в глобальный список агентов.
   - `has_agent(agent_name: str)`: Проверяет, зарегистрирован ли уже агент.
   - `set_simulation_for_free_agents(simulation)`: Устанавливает симуляцию, если она `None`.
   - `get_agent_by_name(name)`: Получает агента по имени.
   - `all_agents_names()`: Возвращает имена всех агентов.
   - `clear_agents()`: Очищает глобальный список агентов.

### `__init__`
   ```python
    def __init__(self, name:str=None, 
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

   **Назначение**: Инициализирует экземпляр класса `TinyPerson`.

   **Параметры**:
   - `name (str, optional)`: Имя персонажа. Если не указано, должно быть указано `spec_path`. По умолчанию `None`.
   - `episodic_memory (EpisodicMemory, optional)`: Эпизодическая память для персонажа. По умолчанию `None`.
   - `semantic_memory (SemanticMemory, optional)`: Семантическая память для персонажа. По умолчанию `None`.
   - `mental_faculties (list, optional)`: Список ментальных способностей персонажа. По умолчанию `None`.

   **Как работает функция**:
   1. Проверяет, переданы ли объекты `episodic_memory` и `semantic_memory`, и присваивает их соответствующим атрибутам экземпляра класса.
   2. Проверяет, передан ли список ментальных способностей `mental_faculties`, и присваивает его атрибуту `_mental_faculties` экземпляра класса.
   3. Утверждает, что имя персонажа `name` не `None`.
   4. Присваивает имя персонажа атрибуту `name` экземпляра класса.

   **Примеры**:
   ```python
   from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
   from tinytroupe.agent.tiny_person import TinyPerson
   
   # Создание TinyPerson с именем
   person1 = TinyPerson(name='Alice')
   print(person1.name)  # Вывод: Alice
   
   # Создание TinyPerson с эпизодической и семантической памятью
   episodic_memory = EpisodicMemory()
   semantic_memory = SemanticMemory()
   person2 = TinyPerson(name='Bob', episodic_memory=episodic_memory, semantic_memory=semantic_memory)
   print(person2.episodic_memory)  # Вывод: <tinytroupe.agent.memory.EpisodicMemory object at ...>
   print(person2.semantic_memory)  # Вывод: <tinytroupe.agent.memory.SemanticMemory object at ...>
   
   # Создание TinyPerson с ментальными способностями
   mental_faculties = ['способность к обучению', 'способность к анализу']
   person3 = TinyPerson(name='Charlie', mental_faculties=mental_faculties)
   print(person3._mental_faculties)  # Вывод: ['способность к обучению', 'способность к анализу']
   ```

### `_post_init`

```python
    def _post_init(self, **kwargs):
        """
        This will run after __init__, since the class has the @post_init decorator.
        It is convenient to separate some of the initialization processes to make deserialize easier.
        """
```
   **Назначение**: Метод `_post_init` вызывается после `__init__` благодаря декоратору `@utils.post_init`. Этот метод предназначен для выполнения дополнительной инициализации объекта, особенно при десериализации.

   **Параметры**:
   - `**kwargs`: Произвольные ключевые аргументы, которые могут быть переданы при вызове метода.

   **Как работает функция**:
   1. **Инициализация значений по умолчанию**:
      - Создает пустой список `self.current_messages` для хранения текущих сообщений агента.
      - Устанавливает `self.environment` в `None`, указывая на отсутствие окружения у агента.
      - Создает пустой список `self._actions_buffer` для хранения действий, ожидающих выполнения.
      - Создает пустой список `self._accessible_agents` для хранения агентов, с которыми данный агент может взаимодействовать.
      - Создает пустой список `self._displayed_communications_buffer` для хранения отображенных сообщений.

   2. **Инициализация памяти, если она не была передана**:
      - Проверяет, существует ли атрибут `episodic_memory`. Если нет, создает новый экземпляр `EpisodicMemory` и присваивает его `self.episodic_memory`.
      - Проверяет, существует ли атрибут `semantic_memory`. Если нет, создает новый экземпляр `SemanticMemory` и присваивает его `self.semantic_memory`.
      - Проверяет, существует ли атрибут `_mental_faculties`. Если нет, создает пустой список и присваивает его `self._mental_faculties`.

   3. **Создание конфигурации персонажа**:
      - Проверяет, существует ли атрибут `_persona`. Если нет, создает словарь с основными характеристиками персонажа (имя, возраст, национальность, место жительства, профессия, рутины, описание профессии, черты характера, интересы, навыки, отношения).

   4. **Присвоение имени из `_persona`**:
      - Проверяет, существует ли атрибут `name`. Если нет, присваивает ему значение из `self._persona["name"]`.

   5. **Создание ментального состояния**:
      - Проверяет, существует ли атрибут `_mental_state`. Если нет, создает словарь с основными аспектами ментального состояния (дата и время, местоположение, контекст, цели, внимание, эмоции, контекст памяти, доступные агенты).

   6. **Инициализация расширенного описания агента**:
      - Устанавливает `self._extended_agent_summary` в `None`.

   7. **Настройка путей к шаблонам**:
      - Устанавливает путь к шаблону промпта агента `self._prompt_template_path` и инициализирует `self._init_system_message` в `None`.

   8. **Механизмы десериализации**:
      - Если передан аргумент `new_agent_name`, вызывает метод `self._rename` для переименования агента.
      - Если передан аргумент `auto_rename` и он равен `True`, пытается переименовать агента, добавляя уникальный идентификатор к имени, пока имя не станет уникальным.

   9. **Регистрация агента**:
      - Регистрирует агента в глобальном списке агентов с помощью `TinyPerson.add_agent(self)`.

   10. **Сброс промпта**:
       - Вызывает метод `self.reset_prompt()` для очистки и установки начального промпта агента.

   11. **Установка идентификатора симуляции**:
       - Проверяет, выполняется ли код в контексте симуляции. Если да, добавляет агента в текущую симуляцию. В противном случае устанавливает `self.simulation_id` в `None`.

   **Примеры**:
   ```python
   from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
   from tinytroupe.agent.tiny_person import TinyPerson
   
   # Пример создания TinyPerson с указанием имени
   person = TinyPerson(name="Alice")
   person._post_init()
   print(person.name)
   
   # Пример создания TinyPerson с указанием имени и автоматическим переименованием
   person = TinyPerson(name="Alice")
   person._post_init(auto_rename=True)
   print(person.name)
   
   # Пример создания TinyPerson с указанием имени и новым именем
   person = TinyPerson(name="Alice")
   person._post_init(new_agent_name="Bob")
   print(person.name)
   ```

### `generate_agent_system_prompt`

```python
    def generate_agent_system_prompt(self):
        with open(self._prompt_template_path, "r") as f:
            agent_prompt_template = f.read()

        # let\'s operate on top of a copy of the configuration, because we\'ll need to add more variables, etc.
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
        template_variables[\'actions_definitions_prompt\'] = textwrap.indent(actions_definitions_prompt.strip(), "  ")
        template_variables[\'actions_constraints_prompt\'] = textwrap.indent(actions_constraints_prompt.strip(), "  ")

        # RAI prompt components, if requested
        template_variables = utils.add_rai_template_variables_if_enabled(template_variables)

        return chevron.render(agent_prompt_template, template_variables)
```

   **Назначение**: Генерирует системный промпт для агента, используя шаблон Mustache и данные из конфигурации персонажа и ментальных способностей.

   **Как работает функция**:
   1. Читает шаблон промпта агента из файла, указанного в `self._prompt_template_path`.
   2. Создает копию словаря `self._persona` для работы с переменными шаблона.
   3. Преобразует словарь `self._persona` в JSON-строку с отступами и добавляет её в `template_variables` под ключом `"persona"`.
   4. Подготавливает строки для определений и ограничений действий, итерируясь по ментальным способностям агента (`self._mental_faculties`).
   5. Добавляет определения и ограничения действий в `template_variables`, используя `textwrap.indent` для форматирования.
   6. Добавляет компоненты RAI (Responsible AI), если они включены, с помощью `utils.add_rai_template_variables_if_enabled`.
   7. Рендерит шаблон `agent_prompt_template` с использованием `template_variables` и возвращает результат.

   **Параметры**:
   - Нет параметров.

   **Возвращает**:
   - `str`: Сгенерированный системный промпт для агента.

   **Примеры**:
   ```python
   from tinytroupe.agent.tiny_person import TinyPerson
   import os
   
   # Создание экземпляра TinyPerson (необходимо указать имя)
   agent = TinyPerson(name="TestAgent")
   agent._prompt_template_path = os.path.join(
       os.path.dirname(__file__), "prompts/tiny_person.mustache"
   )
   # Генерация системного промпта
   system_prompt = agent.generate_agent_system_prompt()
   print(system_prompt)
   ```

### `reset_prompt`

```python
    def reset_prompt(self):

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
                                                 "and complying with **all** instructions and contraints related to the action you use." +\\\
                                                 "DO NOT repeat the exact same action more than once in a row!" +\\\
                                                 "DO NOT keep saying or doing very similar things, but instead try to adapt and make the interactions look natural." +\\\
                                                 "These actions **MUST** be rendered following the JSON specification perfectly, including all required keys (even if their value is empty), **ALWAYS**."
                                     })
```

   **Назначение**: Сбрасывает и обновляет текущий промпт агента, генерируя новое системное сообщение на основе текущей конфигурации, добавляя последние воспоминания и финальное сообщение пользователя.

   **Как работает функция**:
   1. Генерирует новое системное сообщение, вызывая `self.generate_agent_system_prompt()`, и присваивает его `self._init_system_message`.
   2. Сбрасывает список текущих сообщений `self.current_messages`, добавляя системное сообщение с ролью "system" и содержимым `self._init_system_message`.
   3. Извлекает последние воспоминания агента, вызывая `self.retrieve_recent_memories()`, и добавляет их в `self.current_messages`.
   4. Добавляет финальное сообщение пользователя с ролью "user", которое инструктирует агента генерировать последовательность действий, соблюдая все инструкции и ограничения.

   **Параметры**:
   - Нет параметров.

   **Примеры**:
   ```python
   from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
   from tinytroupe.agent.tiny_person import TinyPerson
   
   # Создание экземпляра TinyPerson (необходимо указать имя)
   agent = TinyPerson(name="TestAgent")
   
   # Сброс промпта
   agent.reset_prompt()
   
   # Вывод текущих сообщений агента
   for message in agent.current_messages:
       print(message)
   ```

### `get`

```python
    def get(self, key):
        """
        Returns the definition of a key in the TinyPerson\'s configuration.
        """
        return self._persona.get(key, None)
```

   **Назначение**: Возвращает значение ключа из конфигурации `TinyPerson` (словаря `_persona`).

   **Как работает функция**:
   1. Использует метод `get` словаря `self._persona` для получения значения по указанному ключу.
   2. Если ключ не найден, возвращает `None`.

   **Параметры**:
   - `key (str)`: Ключ, значение которого нужно получить.

   **Возвращает**:
   - Значение ключа из `self._persona` или `None`, если ключ не найден.

   **Примеры**:
   ```python
   from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
   from tinytroupe.agent.tiny_person import TinyPerson
   
   # Создание экземпляра TinyPerson (необходимо указать имя)
   agent = TinyPerson(name="TestAgent")
   
   # Установка возраста в конфигурации персонажа
   agent._persona["age"] = 30
   
   # Получение возраста из конфигурации
   age = agent.get("age")
   print(age)  # Вывод: 30
   
   # Получение значения несуществующего ключа
   non_existent_key = agent.get("non_existent_key")
   print(non_existent_key)  # Вывод: None
   ```

### `import_fragment`

```python
    @transactional
    def import_fragment(self, path):
        """
        Imports a fragment of a persona configuration from a JSON file.
        """
        with open(path, "r") as f:
            fragment = json.load(f)

        # check the type is "Fragment" and that there\'s also a "persona" key
        if fragment.get("type", None) == "Fragment" and fragment.get("persona", None) is not None:
            self.include_persona_definitions(fragment["persona"])\n        else:\n            raise ValueError("The imported JSON file must be a valid fragment of a persona configuration.")
        
        # must reset prompt after adding to configuration
        self.reset_prompt()
```

   **Назначение**: Импортирует фрагмент конфигурации персонажа из JSON-файла.

   **Как работает функция**:
   1. Открывает JSON-файл по указанному пути `path` для чтения.
   2. Загружает содержимое JSON-файла в переменную `fragment`.
   3. Проверяет, что тип фрагмента (`fragment.get("type", None)`) равен "Fragment" и что во фрагменте присутствует ключ "persona".
   4. Если проверка пройдена, вызывает метод `self.include_persona_definitions(fragment["persona"])` для включения определений персонажа из фрагмента.
   5. Если проверка не пройдена, выбрасывает исключение `ValueError` с сообщением о том, что импортированный JSON-файл должен быть допустимым фрагментом конфигурации персонажа.
   6. Сбрасывает промпт после добавления конфигурации с помощью `self.reset_prompt()`.

   **Параметры**:
   - `path (str)`: Путь к JSON-файлу с фрагментом конфигурации.

   **Вызывает исключения**:
   - `ValueError`: Если импортированный JSON-файл не является допустимым фрагментом конфигурации персонажа.

   **Примеры**:
   ```python
   from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
   from tinytroupe.agent.tiny_person import TinyPerson
   import json
   import os
   
   # Создаем временный JSON-файл для примера
   fragment_data = {
       "type": "Fragment",
       "persona": {
           "age": 30,
           "occupation": "Software Engineer"
       }
   }
   
   fragment_file_path = "temp_fragment.json"
   with open(fragment_file_path, "w") as f:
       json.dump(fragment_data, f)
   
   # Создаем экземпляр TinyPerson (необходимо указать имя)
   agent = TinyPerson(name="TestAgent")
   
   # Импортируем фрагмент конфигурации
   agent.import_fragment(fragment_file_path)
   
   # Проверяем, что данные из фрагмента были импортированы
   print(agent._persona["age"])       # Вывод: 30
   print(agent._persona["occupation"])  # Вывод: Software Engineer
   
   # Удаляем временный файл
   os.remove(fragment_file_path)
   ```

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

   **Назначение**: Импортирует набор определений в `TinyPerson`, объединяя их с текущей конфигурацией.

   **Как работает функция**:
   1. Объединяет `additional_definitions` с текущим словарем `self._persona`, используя функцию `utils.merge_dicts`.
   2. Сбрасывает промпт после добавления конфигурации с помощью `self.reset_prompt()`.

   **Параметры**:
   - `additional_definitions (dict)`: Дополнительные определения для импорта.

   **Примеры**:
   ```python
   from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
   from tinytroupe.agent.tiny_person import TinyPerson
   
   # Создаем экземпляр TinyPerson (необходимо указать имя)
   agent = TinyPerson(name="TestAgent")
   
   # Изначальная конфигурация персонажа
   agent._persona = {
       "name": "TestAgent",
       "age": 25
   }
   
   # Дополнительные определения для импорта
   additional_definitions = {
       "occupation": "Software Engineer",
       "interests": ["Programming", "Hiking"]
   }
   
   # Импортируем дополнительные определения
   agent.include_persona_definitions(additional_definitions)
   
   # Проверяем, что данные были импортированы и объединены
   print(agent._persona["age"])         # Вывод: 25
   print(agent._persona["occupation"])    # Вывод: Software Engineer
   print(agent._persona["interests"])     # Вывод: ['Programming', 'Hiking']
   ```

### `define`

```python
    @transactional
    def define(self, key, value, merge=True, overwrite_scalars=True):
        """
        Define a value to the TinyPerson\'s persona configuration. Value can either be a scalar or a dictionary.\n        If the value is a dictionary or list, you can choose to merge it with the existing value or replace it. \n        If the value is a scalar, you can choose to overwrite the existing value or not.

        Args:
            key (str): The key to define.
            value (Any): The value to define.
            merge (bool, optional): Whether to merge the dict/list values with the existing values or replace them. Defaults to True.\n            overwrite_scalars (bool, optional): Whether to overwrite scalar values or not. Defaults to True.\n        """
```

   **Назначение**: Определяет значение в конфигурации персонажа `TinyPerson`.

   **Как работает функция**:

   1. Делает отступ для значения, если это строка.
   2. Если значение является словарем или списком:
      - Если `merge` равно `True`, объединяет значение с