# Модуль тестирования `testing_utils.py`

## Обзор

Модуль `testing_utils.py` содержит набор утилитных функций и фикстур, используемых для тестирования компонентов проекта `hypotez`, в частности, связанных с моделированием поведения агентов (`TinyPerson`), виртуальных сред (`TinyWorld`) и социальных сетей (`TinySocialNetwork`). Он предоставляет инструменты для кэширования результатов API, проверки действий агентов и стимулов, а также для сравнения конфигураций агентов.

## Подробнее

Модуль содержит функции для управления файлами, проверки наличия определенных типов действий или стимулов в списках, сравнения конфигураций агентов и создания тестовых окружений. Кроме того, в модуле определены фикстуры `focus_group_world` и `setup`, используемые для настройки тестового окружения перед выполнением тестов.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `remove_file_if_exists`

```python
def remove_file_if_exists(file_path: str) -> None:
    """
    Удаляет файл по указанному пути, если он существует.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        None

    Пример:
        >>> remove_file_if_exists('temp.txt')
    """
```

**Как работает функция**:

Функция `remove_file_if_exists` принимает путь к файлу в качестве аргумента и удаляет этот файл, если он существует. Используется для очистки файловой системы от временных файлов, созданных в процессе тестирования.

### `contains_action_type`

```python
def contains_action_type(actions: list, action_type: str) -> bool:
    """
    Проверяет, содержит ли список действий действие указанного типа.

    Args:
        actions (list): Список действий, где каждое действие представлено словарем.
        action_type (str): Тип действия для поиска.

    Returns:
        bool: `True`, если действие указанного типа найдено в списке, `False` в противном случае.

    Пример:
        >>> actions = [{"action": {"type": "move", "content": "left"}}, {"action": {"type": "eat", "content": "apple"}}]
        >>> contains_action_type(actions, "move")
        True
        >>> contains_action_type(actions, "sleep")
        False
    """
```

**Как работает функция**:

Функция `contains_action_type` перебирает список действий и проверяет, соответствует ли тип каждого действия заданному типу `action_type`. Если соответствие найдено, функция возвращает `True`. Если список действий пуст или соответствие не найдено, функция возвращает `False`.

### `contains_action_content`

```python
def contains_action_content(actions: list, action_content: str) -> bool:
    """
    Проверяет, содержит ли список действий действие с указанным содержимым.

    Args:
        actions (list): Список действий, где каждое действие представлено словарем.
        action_content (str): Содержимое для поиска в действиях.

    Returns:
        bool: `True`, если действие с указанным содержимым найдено в списке, `False` в противном случае.

    Пример:
        >>> actions = [{"action": {"type": "move", "content": "left"}}, {"action": {"type": "eat", "content": "apple"}}]
        >>> contains_action_content(actions, "left")
        True
        >>> contains_action_content(actions, "banana")
        False
    """
```

**Как работает функция**:

Функция `contains_action_content` перебирает список действий и проверяет, содержит ли содержимое каждого действия заданную строку `action_content`. Поиск выполняется без учета регистра. Если соответствие найдено, функция возвращает `True`. Если список действий пуст или соответствие не найдено, функция возвращает `False`.

### `contains_stimulus_type`

```python
def contains_stimulus_type(stimuli: list, stimulus_type: str) -> bool:
    """
    Проверяет, содержит ли список стимулов стимул указанного типа.

    Args:
        stimuli (list): Список стимулов.
        stimulus_type (str): Тип стимула для поиска.

    Returns:
        bool: `True`, если стимул указанного типа найден в списке, `False` в противном случае.

    Пример:
        >>> stimuli = [{"type": "sound", "content": "loud"}, {"type": "image", "content": "bright"}]
        >>> contains_stimulus_type(stimuli, "sound")
        True
        >>> contains_stimulus_type(stimuli, "smell")
        False
    """
```

**Как работает функция**:

Функция `contains_stimulus_type` перебирает список стимулов и проверяет, соответствует ли тип каждого стимула заданному типу `stimulus_type`. Если соответствие найдено, функция возвращает `True`. Если список стимулов пуст или соответствие не найдено, функция возвращает `False`.

### `contains_stimulus_content`

```python
def contains_stimulus_content(stimuli: list, stimulus_content: str) -> bool:
    """
    Проверяет, содержит ли список стимулов стимул с указанным содержимым.

    Args:
        stimuli (list): Список стимулов.
        stimulus_content (str): Содержимое для поиска в стимулах.

    Returns:
        bool: `True`, если стимул с указанным содержимым найден в списке, `False` в противном случае.
    
    Пример:
        >>> stimuli = [{"type": "sound", "content": "loud"}, {"type": "image", "content": "bright"}]
        >>> contains_stimulus_content(stimuli, "loud")
        True
        >>> contains_stimulus_content(stimuli, "quiet")
        False
    """
```

**Как работает функция**:

Функция `contains_stimulus_content` перебирает список стимулов и проверяет, содержит ли содержимое каждого стимула заданную строку `stimulus_content`. Поиск выполняется без учета регистра. Если соответствие найдено, функция возвращает `True`. Если список стимулов пуст или соответствие не найдено, функция возвращает `False`.

### `terminates_with_action_type`

```python
def terminates_with_action_type(actions: list, action_type: str) -> bool:
    """
    Проверяет, завершается ли список действий действием указанного типа.

    Args:
        actions (list): Список действий.
        action_type (str): Тип действия для поиска в конце списка.

    Returns:
        bool: `True`, если список действий завершается действием указанного типа, `False` в противном случае.

    Пример:
        >>> actions = [{"action": {"type": "move", "content": "left"}}, {"action": {"type": "eat", "content": "apple"}}]
        >>> terminates_with_action_type(actions, "eat")
        True
        >>> terminates_with_action_type(actions, "move")
        False
    """
```

**Как работает функция**:

Функция `terminates_with_action_type` проверяет, является ли последний элемент в списке действий действием указанного типа `action_type`. Если список действий пуст, функция возвращает `False`.

### `proposition_holds`

```python
def proposition_holds(proposition: str) -> bool:
    """
    Проверяет, является ли данное утверждение истинным, используя вызов LLM.
    Используется для проверки текстовых свойств, которые сложно проверить механически.

    Args:
        proposition (str): Утверждение для проверки.

    Returns:
        bool: `True`, если утверждение истинно, `False` в противном случае.

    Raises:
        Exception: Если LLM возвращает неожиданный результат.

    Пример:
        >>> proposition_holds("The text contains some ideas for a product.")
        True
    """
```

**Как работает функция**:

Функция `proposition_holds` отправляет запрос к LLM (Large Language Model) с утверждением, которое необходимо проверить. LLM возвращает результат в виде строки "true" или "false". Функция анализирует ответ LLM и возвращает соответствующее булево значение. Если LLM возвращает неожиданный результат, функция вызывает исключение.
Внутри функции используются следующие переменные:
- `system_prompt` (str): Содержит системное сообщение для LLM, которое указывает, что нужно проверить, является ли утверждение истинным или ложным.
- `user_prompt` (str): Содержит сообщение пользователя с утверждением, которое нужно проверить.
- `messages` (list): Список сообщений, отправляемых в LLM. Содержит системное и пользовательское сообщения.
- `next_message` (dict): Ответ LLM, содержащий результат проверки утверждения.
- `cleaned_message` (str): Очищенный от небуквенно-цифровых символов результат проверки утверждения.

### `only_alphanumeric`

```python
def only_alphanumeric(string: str) -> str:
    """
    Возвращает строку, содержащую только буквенно-цифровые символы.

    Args:
        string (str): Исходная строка.

    Returns:
        str: Строка, содержащая только буквенно-цифровые символы.

    Пример:
        >>> only_alphanumeric("Hello, World!")
        'HelloWorld'
    """
```

**Как работает функция**:

Функция `only_alphanumeric` принимает строку в качестве аргумента и возвращает новую строку, содержащую только буквенно-цифровые символы из исходной строки. Остальные символы отбрасываются.

### `create_test_system_user_message`

```python
def create_test_system_user_message(user_prompt: str, system_prompt: str = "You are a helpful AI assistant.") -> list:
    """
    Создает список, содержащий одно системное сообщение и одно сообщение пользователя.

    Args:
        user_prompt (str): Сообщение пользователя.
        system_prompt (str, optional): Системное сообщение. По умолчанию "You are a helpful AI assistant.".

    Returns:
        list: Список, содержащий системное и пользовательское сообщения.

    Пример:
        >>> create_test_system_user_message("What is the capital of France?", "You are a helpful AI assistant.")
        [{'role': 'system', 'content': 'You are a helpful AI assistant.'}, {'role': 'user', 'content': 'What is the capital of France?'}]
    """
```

**Как работает функция**:

Функция `create_test_system_user_message` создает список сообщений для отправки в LLM. Список содержит системное сообщение и сообщение пользователя. Если сообщение пользователя не указано, создается только системное сообщение.

### `agents_personas_are_equal`

```python
def agents_personas_are_equal(agent1: TinyPerson, agent2: TinyPerson, ignore_name: bool = False) -> bool:
    """
    Проверяет, равны ли конфигурации двух агентов.

    Args:
        agent1 (TinyPerson): Первый агент.
        agent2 (TinyPerson): Второй агент.
        ignore_name (bool, optional): Если `True`, имя агента игнорируется при сравнении. По умолчанию `False`.

    Returns:
        bool: `True`, если конфигурации агентов равны, `False` в противном случае.

    Пример:
        >>> agent1 = TinyPerson(name="John", persona={"age": 30, "occupation": "engineer"})
        >>> agent2 = TinyPerson(name="Jane", persona={"age": 30, "occupation": "engineer"})
        >>> agents_personas_are_equal(agent1, agent2)
        False
        >>> agents_personas_are_equal(agent1, agent2, ignore_name=True)
        True
    """
```

**Как работает функция**:

Функция `agents_personas_are_equal` сравнивает конфигурации двух агентов, представленных экземплярами класса `TinyPerson`. Если флаг `ignore_name` установлен в `True`, имя агента игнорируется при сравнении. Функция перебирает атрибуты `_persona` первого агента и сравнивает их с соответствующими атрибутами второго агента. Если обнаружено различие, функция возвращает `False`. Если все атрибуты совпадают, функция возвращает `True`.

### `agent_first_name`

```python
def agent_first_name(agent: TinyPerson) -> str:
    """
    Возвращает имя агента.

    Args:
        agent (TinyPerson): Агент, имя которого нужно получить.

    Returns:
        str: Имя агента.

    Пример:
        >>> agent = TinyPerson(name="John Doe", persona={"age": 30, "occupation": "engineer"})
        >>> agent_first_name(agent)
        'John'
    """
```

**Как работает функция**:

Функция `agent_first_name` принимает экземпляр класса `TinyPerson` в качестве аргумента и возвращает имя агента.

### `get_relative_to_test_path`

```python
def get_relative_to_test_path(path_suffix: str) -> str:
    """
    Возвращает путь к файлу теста с заданным суффиксом.

    Args:
        path_suffix (str): Суффикс пути.

    Returns:
        str: Полный путь к файлу теста.

    Пример:
        >>> get_relative_to_test_path('data/test.txt')
        '/path/to/test/data/test.txt'
    """
```

**Как работает функция**:

Функция `get_relative_to_test_path` принимает суффикс пути в качестве аргумента и возвращает полный путь к файлу теста, объединяя текущую директорию с заданным суффиксом. Используется для получения путей к файлам, расположенным относительно текущего файла теста.

## Фикстуры

### `focus_group_world`

```python
@pytest.fixture(scope="function")
def focus_group_world() -> TinyWorld:
    """
    Фикстура, создающая экземпляр TinyWorld с тремя агентами:
    lisa_the_data_scientist, oscar_the_architect, marcos_the_physician.

    Returns:
        TinyWorld: Экземпляр TinyWorld с тремя агентами.
    """
```

**Как работает фикстура**:

Фикстура `focus_group_world` создает экземпляр класса `TinyWorld` с тремя агентами, представляющими различные профессии: Lisa the data scientist, Oscar the architect и Marcos the physician. Фикстура используется для предоставления тестового окружения с предопределенными агентами.

### `setup`

```python
@pytest.fixture(scope="function")
def setup() -> Generator[None, None, None]:
    """
    Фикстура, очищающая списки агентов и сред перед каждым тестом.

    Yields:
        None
    """
```

**Как работает фикстура**:

Фикстура `setup` очищает списки агентов (`TinyPerson.clear_agents()`) и сред (`TinyWorld.clear_environments()`) перед каждым тестом. Это гарантирует, что тесты начинаются с чистого состояния и не зависят от результатов предыдущих тестов. Фикстура использует `yield`, чтобы выполнить очистку перед тестом и после его завершения.