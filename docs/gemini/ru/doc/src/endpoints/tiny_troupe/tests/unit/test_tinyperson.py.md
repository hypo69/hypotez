# Модуль тестирования `tinyperson`

## Обзор

Этот модуль содержит набор юнит-тестов для проверки функциональности класса `TinyPerson` из проекта `hypotez`. 

## Подробнее

Тесты охватывают основные функции `TinyPerson`, такие как:
- `listen_and_act()`: проверка реакции агента на стимул и выполнения действий.
- `listen()`: проверка того, что агент слышит и запоминает информацию.
- `define()`: проверка установки значений в конфигурации агента.
- `define_several()`: проверка корректной установки нескольких значений в группу конфигурации агента.
- `socialize()`: проверка взаимодействия с другими агентами.
- `see()`: проверка реакции агента на визуальный стимул.
- `think()`: проверка реакции агента на мысли.
- `internalize_goal()`: проверка реакции агента на установку цели.
- `move_to()`: проверка перемещения агента в новое местоположение.
- `change_context()`: проверка изменения контекста.
- `save_specification()`: проверка сохранения спецификации агента в файл.
- `programmatic_definitions()`: проверка установки значений в конфигурации агента программным способом.

## Классы 

### `class test_act`

**Описание**:  Класс для тестирования функции `act()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_act(setup)`: Тестирует реакцию агента на стимул "Tell me a bit about your life." и проверку выполнения действий.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `listen_and_act()` для каждого агента.
    - Проверяет количество действий, тип действий и завершение действием "DONE".

### `class test_listen`

**Описание**: Класс для тестирования функции `listen()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_listen(setup)`: Тестирует, что агент слышит и запоминает информацию.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `listen()` для каждого агента с сообщением "Hello, how are you?".
    - Проверяет наличие сообщения в текущих сообщениях, роль последнего сообщения и тип стимула.

### `class test_define`

**Описание**: Класс для тестирования функции `define()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_define(setup)`: Тестирует установку значения в конфигурации агента.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `define()` для каждого агента, устанавливая значение `age` на 25.
    - Проверяет установленное значение в конфигурации, изменение промпта и наличие значения в промте.

### `class test_define_several`

**Описание**: Класс для тестирования функции `define_several()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_define_several(setup)`: Тестирует установку нескольких значений в конфигурации агента.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `define_several()` для каждого агента, устанавливая набор навыков.
    - Проверяет наличие каждого навыка в конфигурации.

### `class test_socialize`

**Описание**: Класс для тестирования функции `socialize()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_socialize(setup)`: Тестирует взаимодействие с другим агентом.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `make_agent_accessible()` для каждого агента, делая другого агента доступным как друга.
    - Вызывает метод `listen()` для каждого агента с приветствием, содержащим имя другого агента.
    - Проверяет количество действий, тип действий и упоминание имени друга в действиях.

### `class test_see`

**Описание**: Класс для тестирования функции `see()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_see(setup)`: Тестирует реакцию агента на визуальный стимул.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `see()` для каждого агента с описанием визуального стимула.
    - Проверяет количество действий, тип действий и упоминание визуального стимула в действиях.

### `class test_think`

**Описание**: Класс для тестирования функции `think()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_think(setup)`: Тестирует реакцию агента на мысли.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `think()` для каждого агента с описанием мысли.
    - Проверяет количество действий, тип действий и упоминание темы мысли в действиях.

### `class test_internalize_goal`

**Описание**: Класс для тестирования функции `internalize_goal()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_internalize_goal(setup)`: Тестирует реакцию агента на установку цели.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `internalize_goal()` для каждого агента с описанием цели.
    - Проверяет количество действий, тип действий и упоминание темы цели в действиях.

### `class test_move_to`

**Описание**: Класс для тестирования функции `move_to()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_move_to(setup)`: Тестирует перемещение агента в новое местоположение.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `move_to()` для каждого агента с описанием нового местоположения и контекста.
    - Проверяет установленное местоположение и контекст в `_mental_state`.

### `class test_change_context`

**Описание**: Класс для тестирования функции `change_context()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_change_context(setup)`: Тестирует изменение контекста.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `change_context()` для каждого агента с описанием нового контекста.
    - Проверяет наличие элементов нового контекста в `_mental_state`.

### `class test_save_specification`

**Описание**: Класс для тестирования функции `save_specification()` в `TinyPerson`.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_save_specification(setup)`: Тестирует сохранение спецификации агента в файл.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `save_specification()` для каждого агента.
    - Проверяет наличие сохраненного файла.
    - Загружает сохраненный файл и сравнивает его с исходным агентом, игнорируя имя агента.

### `class test_programmatic_definitions`

**Описание**: Класс для тестирования установки значений в конфигурации агента программным способом.
**Наследует**: 
**Атрибуты**:
**Методы**:
- `test_programmatic_definitions(setup)`: Тестирует установку значений в конфигурации агента программным способом.
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `listen_and_act()` для каждого агента с сообщением "Tell me a bit about your life.".
    - Проверяет корректность работы агента с конфигурацией, установленной программным способом.


## Функции 

### `test_act(setup)`

**Назначение**: Тестирует реакцию агента на стимул "Tell me a bit about your life." и проверку выполнения действий.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `listen_and_act()` для каждого агента.
    - Проверяет количество действий, тип действий и завершение действием "DONE".
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
actions = agent.listen_and_act("Tell me a bit about your life.", return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform (even if it is just DONE)."
assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since we asked him to do so."
assert terminates_with_action_type(actions, "DONE"), f"{agent.name} should always terminate with a DONE action."
# Пример 2
agent = create_lisa_the_data_scientist()
actions = agent.listen_and_act("Tell me a bit about your life.", return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform (even if it is just DONE)."
assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since we asked him to do so."
assert terminates_with_action_type(actions, "DONE"), f"{agent.name} should always terminate with a DONE action."
```

### `test_listen(setup)`

**Назначение**: Тестирует, что агент слышит и запоминает информацию.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `listen()` для каждого агента с сообщением "Hello, how are you?".
    - Проверяет наличие сообщения в текущих сообщениях, роль последнего сообщения и тип стимула.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.listen("Hello, how are you?")
assert len(agent.current_messages) > 0, f"{agent.name} should have at least one message in its current messages."
assert agent.episodic_memory.retrieve_all()[-1][\'role\'] == \'user\', f"{agent.name} should have the last message as \'user\'."\
assert agent.episodic_memory.retrieve_all()[-1][\'content\'][\'stimuli\'][0][\'type\'] == \'CONVERSATION\', f"{agent.name} should have the last message as a \'CONVERSATION\' stimulus."\
assert agent.episodic_memory.retrieve_all()[-1][\'content\'][\'stimuli\'][0][\'content\'] == \'Hello, how are you?\', f"{agent.name} should have the last message with the correct content."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.listen("Hello, how are you?")
assert len(agent.current_messages) > 0, f"{agent.name} should have at least one message in its current messages."
assert agent.episodic_memory.retrieve_all()[-1][\'role\'] == \'user\', f"{agent.name} should have the last message as \'user\'."\
assert agent.episodic_memory.retrieve_all()[-1][\'content\'][\'stimuli\'][0][\'type\'] == \'CONVERSATION\', f"{agent.name} should have the last message as a \'CONVERSATION\' stimulus."\
assert agent.episodic_memory.retrieve_all()[-1][\'content\'][\'stimuli\'][0][\'content\'] == \'Hello, how are you?\', f"{agent.name} should have the last message with the correct content."\
```

### `test_define(setup)`

**Назначение**: Тестирует установку значения в конфигурации агента.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `define()` для каждого агента, устанавливая значение `age` на 25.
    - Проверяет установленное значение в конфигурации, изменение промпта и наличие значения в промте.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
original_prompt = agent.current_messages[0][\'content\']
agent.define(\'age\', 25)
assert agent._persona[\'age\'] == 25, f"{agent.name} should have the age set to 25."\
assert agent.current_messages[0][\'content\'] != original_prompt, f"{agent.name} should have a different prompt after defining a new value."\
assert \'25\' in agent.current_messages[0][\'content\'], f"{agent.name} should have the age in the prompt."\
# Пример 2
agent = create_lisa_the_data_scientist()
original_prompt = agent.current_messages[0][\'content\']
agent.define(\'age\', 25)
assert agent._persona[\'age\'] == 25, f"{agent.name} should have the age set to 25."\
assert agent.current_messages[0][\'content\'] != original_prompt, f"{agent.name} should have a different prompt after defining a new value."\
assert \'25\' in agent.current_messages[0][\'content\'], f"{agent.name} should have the age in the prompt."\
```

### `test_define_several(setup)`

**Назначение**: Тестирует установку нескольких значений в конфигурации агента.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `define_several()` для каждого агента, устанавливая набор навыков.
    - Проверяет наличие каждого навыка в конфигурации.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.define("skills", ["Python", "Machine learning", "GPT-3"])
assert "Python" in agent._persona["skills"], f"{agent.name} should have Python as a skill."\
assert "Machine learning" in agent._persona["skills"], f"{agent.name} should have Machine learning as a skill."\
assert "GPT-3" in agent._persona["skills"], f"{agent.name} should have GPT-3 as a skill."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.define("skills", ["Python", "Machine learning", "GPT-3"])
assert "Python" in agent._persona["skills"], f"{agent.name} should have Python as a skill."\
assert "Machine learning" in agent._persona["skills"], f"{agent.name} should have Machine learning as a skill."\
assert "GPT-3" in agent._persona["skills"], f"{agent.name} should have GPT-3 as a skill."\
```

### `test_socialize(setup)`

**Назначение**: Тестирует взаимодействие с другим агентом.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `make_agent_accessible()` для каждого агента, делая другого агента доступным как друга.
    - Вызывает метод `listen()` для каждого агента с приветствием, содержащим имя другого агента.
    - Проверяет количество действий, тип действий и упоминание имени друга в действиях.
**Примеры**:
```python
# Пример 1
an_oscar = create_oscar_the_architect()
a_lisa = create_lisa_the_data_scientist()
an_oscar.make_agent_accessible(a_lisa, relation_description="My friend")
an_oscar.listen(f"Hi {an_oscar.name}, I am {a_lisa.name}.")
actions = an_oscar.act(return_actions=True)
assert len(actions) >= 1, f"{an_oscar.name} should have at least one action to perform."\
assert contains_action_type(actions, "TALK"), f"{an_oscar.name} should have at least one TALK action to perform, since we started a conversation."\
assert contains_action_content(actions, agent_first_name(a_lisa)), f"{an_oscar.name} should mention {a_lisa.name}\'s first name in the TALK action, since they are friends."\
# Пример 2
a_lisa = create_lisa_the_data_scientist()
an_oscar = create_oscar_the_architect()
a_lisa.make_agent_accessible(an_oscar, relation_description="My friend")
a_lisa.listen(f"Hi {a_lisa.name}, I am {an_oscar.name}.")
actions = a_lisa.act(return_actions=True)
assert len(actions) >= 1, f"{a_lisa.name} should have at least one action to perform."\
assert contains_action_type(actions, "TALK"), f"{a_lisa.name} should have at least one TALK action to perform, since we started a conversation."\
assert contains_action_content(actions, agent_first_name(an_oscar)), f"{a_lisa.name} should mention {an_oscar.name}\'s first name in the TALK action, since they are friends."\
```

### `test_see(setup)`

**Назначение**: Тестирует реакцию агента на визуальный стимул.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `see()` для каждого агента с описанием визуального стимула.
    - Проверяет количество действий, тип действий и упоминание визуального стимула в действиях.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.see("A beautiful sunset over the ocean.")
actions = agent.act(return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."\
assert contains_action_type(actions, "THINK"), f"{agent.name} should have at least one THINK action to perform, since they saw something interesting."\
assert contains_action_content(actions, "sunset"), f"{agent.name} should mention the sunset in the THINK action, since they saw it."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.see("A beautiful sunset over the ocean.")
actions = agent.act(return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."\
assert contains_action_type(actions, "THINK"), f"{agent.name} should have at least one THINK action to perform, since they saw something interesting."\
assert contains_action_content(actions, "sunset"), f"{agent.name} should mention the sunset in the THINK action, since they saw it."\
```

### `test_think(setup)`

**Назначение**: Тестирует реакцию агента на мысли.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `think()` для каждого агента с описанием мысли.
    - Проверяет количество действий, тип действий и упоминание темы мысли в действиях.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.think("I will tell everyone right now how awesome life is!")
actions = agent.act(return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."\
assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since they are eager to talk."\
assert contains_action_content(actions, "life"), f"{agent.name} should mention life in the TALK action, since they thought about it."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.think("I will tell everyone right now how awesome life is!")
actions = agent.act(return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."\
assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since they are eager to talk."\
assert contains_action_content(actions, "life"), f"{agent.name} should mention life in the TALK action, since they thought about it."\
```

### `test_internalize_goal(setup)`

**Назначение**: Тестирует реакцию агента на установку цели.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `internalize_goal()` для каждого агента с описанием цели.
    - Проверяет количество действий, тип действий и упоминание темы цели в действиях.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.internalize_goal("I want to compose in my head a wonderful poem about how cats are glorious creatures.")
actions = agent.act(return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."\
assert contains_action_type(actions, "THINK"), f"{agent.name} should have at least one THINK action to perform, since they internalized a goal."\
assert contains_action_content(actions, "cats"), f"{agent.name} should mention cats in the THINK action, since they internalized a goal about them."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.internalize_goal("I want to compose in my head a wonderful poem about how cats are glorious creatures.")
actions = agent.act(return_actions=True)
assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."\
assert contains_action_type(actions, "THINK"), f"{agent.name} should have at least one THINK action to perform, since they internalized a goal."\
assert contains_action_content(actions, "cats"), f"{agent.name} should mention cats in the THINK action, since they internalized a goal about them."\
```

### `test_move_to(setup)`

**Назначение**: Тестирует перемещение агента в новое местоположение.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `move_to()` для каждого агента с описанием нового местоположения и контекста.
    - Проверяет установленное местоположение и контекст в `_mental_state`.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.move_to("New York", context=["city", "busy", "diverse"])
assert agent._mental_state["location"] == "New York", f"{agent.name} should have New York as the current location."\
assert "city" in agent._mental_state["context"], f"{agent.name} should have city as part of the current context."\
assert "busy" in agent._mental_state["context"], f"{agent.name} should have busy as part of the current context."\
assert "diverse" in agent._mental_state["context"], f"{agent.name} should have diverse as part of the current context."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.move_to("New York", context=["city", "busy", "diverse"])
assert agent._mental_state["location"] == "New York", f"{agent.name} should have New York as the current location."\
assert "city" in agent._mental_state["context"], f"{agent.name} should have city as part of the current context."\
assert "busy" in agent._mental_state["context"], f"{agent.name} should have busy as part of the current context."\
assert "diverse" in agent._mental_state["context"], f"{agent.name} should have diverse as part of the current context."\
```

### `test_change_context(setup)`

**Назначение**: Тестирует изменение контекста.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `change_context()` для каждого агента с описанием нового контекста.
    - Проверяет наличие элементов нового контекста в `_mental_state`.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.change_context(["home", "relaxed", "comfortable"])
assert "home" in agent._mental_state["context"], f"{agent.name} should have home as part of the current context."\
assert "relaxed" in agent._mental_state["context"], f"{agent.name} should have relaxed as part of the current context."\
assert "comfortable" in agent._mental_state["context"], f"{agent.name} should have comfortable as part of the current context."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.change_context(["home", "relaxed", "comfortable"])
assert "home" in agent._mental_state["context"], f"{agent.name} should have home as part of the current context."\
assert "relaxed" in agent._mental_state["context"], f"{agent.name} should have relaxed as part of the current context."\
assert "comfortable" in agent._mental_state["context"], f"{agent.name} should have comfortable as part of the current context."\
```

### `test_save_specification(setup)`

**Назначение**: Тестирует сохранение спецификации агента в файл.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `save_specification()` для каждого агента.
    - Проверяет наличие сохраненного файла.
    - Загружает сохраненный файл и сравнивает его с исходным агентом, игнорируя имя агента.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect()
agent.save_specification(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json"), include_memory=True)
assert os.path.exists(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json")), f"{agent.name} should have saved the file."\
loaded_name = f"{agent.name}_loaded"\
loaded_agent = TinyPerson.load_specification(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json"), new_agent_name=loaded_name)\
assert loaded_agent.name == loaded_name, f"{agent.name} should have the same name as the loaded agent."\
assert agents_personas_are_equal(agent, loaded_agent, ignore_name=True), f"{agent.name} should have the same configuration as the loaded agent, except for the name."\
# Пример 2
agent = create_lisa_the_data_scientist()
agent.save_specification(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json"), include_memory=True)
assert os.path.exists(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json")), f"{agent.name} should have saved the file."\
loaded_name = f"{agent.name}_loaded"\
loaded_agent = TinyPerson.load_specification(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json"), new_agent_name=loaded_name)\
assert loaded_agent.name == loaded_name, f"{agent.name} should have the same name as the loaded agent."\
assert agents_personas_are_equal(agent, loaded_agent, ignore_name=True), f"{agent.name} should have the same configuration as the loaded agent, except for the name."\
```

### `test_programmatic_definitions(setup)`

**Назначение**: Тестирует установку значений в конфигурации агента программным способом.
**Параметры**:
- `setup`: Фикстура для настройки тестовой среды.
**Возвращает**: 
**Вызывает исключения**: 
**Как работает функция**: 
    - Создает экземпляры агентов `Oscar` и `Lisa`.
    - Вызывает метод `listen_and_act()` для каждого агента с сообщением "Tell me a bit about your life.".
    - Проверяет корректность работы агента с конфигурацией, установленной программным способом.
**Примеры**:
```python
# Пример 1
agent = create_oscar_the_architect_2()
agent.listen_and_act("Tell me a bit about your life.")
# Пример 2
agent = create_lisa_the_data_scientist_2()
agent.listen_and_act("Tell me a bit about your life.")