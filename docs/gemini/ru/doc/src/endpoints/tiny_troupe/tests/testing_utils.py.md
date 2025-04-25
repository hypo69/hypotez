# Модуль `testing_utils`

## Обзор

Модуль `testing_utils` предоставляет набор вспомогательных функций для тестирования агентов, мира и других элементов платформы `tinytroupe`. 

## Подробнее

В модуле `testing_utils` реализованы функции, которые упрощают процесс тестирования, предоставляя возможности для проверки действий, стимулов, пропозиций и конфигураций агентов, а также управления файлами и кешированием.

## Функции

### `remove_file_if_exists`

**Назначение**: Удаляет файл по указанному пути, если он существует.

**Параметры**:
- `file_path` (str): Путь к файлу.

**Возвращает**:
- None

**Примеры**:
```python
>>> remove_file_if_exists("test.txt")  # Удаляет файл "test.txt", если он существует
```

### `contains_action_type`

**Назначение**: Проверяет, содержит ли заданный список действий действие заданного типа.

**Параметры**:
- `actions` (list): Список действий.
- `action_type` (str): Тип действия, которое нужно найти.

**Возвращает**:
- bool: `True`, если список действий содержит действие заданного типа, иначе `False`.

**Примеры**:
```python
>>> actions = [{"action": {"type": "say"}}, {"action": {"type": "ask"}}]
>>> contains_action_type(actions, "say")  # Возвращает True
>>> contains_action_type(actions, "write")  # Возвращает False
```

### `contains_action_content`

**Назначение**: Проверяет, содержит ли заданный список действий действие с заданным содержимым.

**Параметры**:
- `actions` (list): Список действий.
- `action_content` (str): Содержимое действия, которое нужно найти.

**Возвращает**:
- bool: `True`, если список действий содержит действие с заданным содержимым, иначе `False`.

**Примеры**:
```python
>>> actions = [{"action": {"content": "Hello, world!"}}, {"action": {"content": "What's your name?"}}]
>>> contains_action_content(actions, "Hello, world!")  # Возвращает True
>>> contains_action_content(actions, "What's up?")  # Возвращает False
```

### `contains_stimulus_type`

**Назначение**: Проверяет, содержит ли заданный список стимулов стимул заданного типа.

**Параметры**:
- `stimuli` (list): Список стимулов.
- `stimulus_type` (str): Тип стимула, который нужно найти.

**Возвращает**:
- bool: `True`, если список стимулов содержит стимул заданного типа, иначе `False`.

**Примеры**:
```python
>>> stimuli = [{"type": "text"}, {"type": "image"}]
>>> contains_stimulus_type(stimuli, "text")  # Возвращает True
>>> contains_stimulus_type(stimuli, "audio")  # Возвращает False
```

### `contains_stimulus_content`

**Назначение**: Проверяет, содержит ли заданный список стимулов стимул с заданным содержимым.

**Параметры**:
- `stimuli` (list): Список стимулов.
- `stimulus_content` (str): Содержимое стимула, которое нужно найти.

**Возвращает**:
- bool: `True`, если список стимулов содержит стимул с заданным содержимым, иначе `False`.

**Примеры**:
```python
>>> stimuli = [{"content": "Hello, world!"}, {"content": "What's your name?"}]
>>> contains_stimulus_content(stimuli, "Hello, world!")  # Возвращает True
>>> contains_stimulus_content(stimuli, "What's up?")  # Возвращает False
```

### `terminates_with_action_type`

**Назначение**: Проверяет, завершается ли заданный список действий действием заданного типа.

**Параметры**:
- `actions` (list): Список действий.
- `action_type` (str): Тип действия, которое нужно найти.

**Возвращает**:
- bool: `True`, если список действий завершается действием заданного типа, иначе `False`.

**Примеры**:
```python
>>> actions = [{"action": {"type": "say"}}, {"action": {"type": "ask"}}]
>>> terminates_with_action_type(actions, "ask")  # Возвращает True
>>> terminates_with_action_type(actions, "say")  # Возвращает False
```

### `proposition_holds`

**Назначение**: Проверяет, является ли заданное утверждение истинным в соответствии с вызовом LLM. 

**Параметры**:
- `proposition` (str): Утверждение, которое нужно проверить.

**Возвращает**:
- bool: `True`, если утверждение истинно, иначе `False`.

**Вызывает исключения**:
- `Exception`: Если LLM возвращает неожиданный результат.

**Примеры**:
```python
>>> proposition_holds("The sky is blue")  # Возвращает True
>>> proposition_holds("The sky is green")  # Возвращает False
```

### `only_alphanumeric`

**Назначение**: Возвращает строку, содержащую только буквенно-цифровые символы.

**Параметры**:
- `string` (str): Строка, из которой нужно извлечь буквенно-цифровые символы.

**Возвращает**:
- str: Строка, содержащая только буквенно-цифровые символы.

**Примеры**:
```python
>>> only_alphanumeric("Hello, world!")  # Возвращает "HelloWorld"
>>> only_alphanumeric("12345")  # Возвращает "12345"
```

### `create_test_system_user_message`

**Назначение**: Создает список, содержащий одно системное сообщение и одно сообщение пользователя. 

**Параметры**:
- `user_prompt` (str): Сообщение пользователя.
- `system_prompt` (str): Системное сообщение. По умолчанию "You are a helpful AI assistant.".

**Возвращает**:
- list: Список сообщений.

**Примеры**:
```python
>>> create_test_system_user_message("Hello, world!")  # Создает список с системным сообщением и сообщением "Hello, world!"
>>> create_test_system_user_message(None)  # Создает список с системным сообщением "You are a helpful AI assistant."
```

### `agents_personas_are_equal`

**Назначение**: Проверяет, равны ли конфигурации двух агентов.

**Параметры**:
- `agent1` (TinyPerson): Первый агент.
- `agent2` (TinyPerson): Второй агент.
- `ignore_name` (bool): Если `True`, то имя агента не учитывается при сравнении. По умолчанию `False`.

**Возвращает**:
- bool: `True`, если конфигурации агентов равны, иначе `False`.

**Примеры**:
```python
>>> agent1 = TinyPerson("Alice", role="code_checker")
>>> agent2 = TinyPerson("Bob", role="code_checker")
>>> agents_personas_are_equal(agent1, agent2)  # Возвращает False
>>> agents_personas_are_equal(agent1, agent2, ignore_name=True)  # Возвращает True
```

### `agent_first_name`

**Назначение**: Возвращает имя агента.

**Параметры**:
- `agent` (TinyPerson): Агент.

**Возвращает**:
- str: Имя агента.

**Примеры**:
```python
>>> agent = TinyPerson("Alice Smith", role="code_checker")
>>> agent_first_name(agent)  # Возвращает "Alice"
```

### `get_relative_to_test_path`

**Назначение**: Возвращает путь к тестовому файлу с заданным суффиксом.

**Параметры**:
- `path_suffix` (str): Суффикс пути.

**Возвращает**:
- str: Путь к тестовому файлу.

**Примеры**:
```python
>>> get_relative_to_test_path("test_file.txt")  # Возвращает путь к файлу "test_file.txt" в каталоге тестов.
```

## Фикстуры

### `focus_group_world`

**Назначение**: Фикстура, которая создает мир "Focus group" с тремя агентами: Lisa the data scientist, Oscar the architect, and Marcos the physician.

**Возвращает**:
- `TinyWorld`: Мир "Focus group".

**Примеры**:
```python
>>> def test_something(focus_group_world):
...     # Используем мир "Focus group" в тесте
...     pass
```

### `setup`

**Назначение**: Фикстура, которая очищает список агентов и список миров перед каждым тестом.

**Возвращает**:
- None

**Примеры**:
```python
>>> def test_something(setup):
...     # Очищаем список агентов и список миров перед тестом
...     pass