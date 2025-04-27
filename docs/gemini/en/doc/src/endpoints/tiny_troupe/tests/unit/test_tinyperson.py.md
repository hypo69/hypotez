# Модуль `test_tinyperson.py`

## Обзор

Модуль `test_tinyperson.py` содержит набор юнит-тестов для класса `TinyPerson`,  определенного в пакете `tinytroupe`. 
Тесты проверяют функциональность различных методов класса, включая взаимодействие с пользователем, обработку 
информации,  определение переменных, сохранение состояния и другие.

## Детали

###  `test_act(setup)`

**Цель**: Проверка функции `act` агента. Проверяется, что агент реагирует на сообщение пользователя 
  и генерирует адекватные действия, которые могут включать `TALK` (говорить), `THINK` (думать),  
  `DONE` (завершение действия).

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_act(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        actions = agent.listen_and_act("Tell me a bit about your life.", return_actions=True)
        logger.info(agent.pp_current_interactions())
        assert len(actions) >= 1, f"{agent.name} should have at least one action to perform (even if it is just DONE)."
        assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since we asked him to do so."
        assert terminates_with_action_type(actions, "DONE"), f"{agent.name} should always terminate with a DONE action."
```

### `test_listen(setup)`

**Цель**: Проверка функции `listen`, которая позволяет агенту получить сообщение от пользователя 
  и добавить его в текущие сообщения.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_listen(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.listen("Hello, how are you?")
        assert len(agent.current_messages) > 0, f"{agent.name} should have at least one message in its current messages."
        assert agent.episodic_memory.retrieve_all()[-1]['role'] == 'user', f"{agent.name} should have the last message as 'user'."
        assert agent.episodic_memory.retrieve_all()[-1]['content']['stimuli'][0]['type'] == 'CONVERSATION', f"{agent.name} should have the last message as a 'CONVERSATION' stimulus."
        assert agent.episodic_memory.retrieve_all()[-1]['content']['stimuli'][0]['content'] == 'Hello, how are you?', f"{agent.name} should have the last message with the correct content."
```

### `test_define(setup)`

**Цель**: Проверка функции `define`, которая позволяет агенту добавить  значение в свою конфигурацию 
  и обновить свой текст.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_define(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        original_prompt = agent.current_messages[0]['content']
        agent.define('age', 25)
        assert agent._persona['age'] == 25, f"{agent.name} should have the age set to 25."
        assert agent.current_messages[0]['content'] != original_prompt, f"{agent.name} should have a different prompt after defining a new value."
        assert '25' in agent.current_messages[0]['content'], f"{agent.name} should have the age in the prompt."
```

### `test_define_several(setup)`

**Цель**: Проверка функции `define`, которая позволяет агенту добавить список значений в свою конфигурацию.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_define_several(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.define("skills", ["Python", "Machine learning", "GPT-3"])
        assert "Python" in agent._persona["skills"], f"{agent.name} should have Python as a skill."
        assert "Machine learning" in agent._persona["skills"], f"{agent.name} should have Machine learning as a skill."
        assert "GPT-3" in agent._persona["skills"], f"{agent.name} should have GPT-3 as a skill."
```

### `test_socialize(setup)`

**Цель**: Проверка функции `socialize`, которая позволяет агенту взаимодействовать с другим агентом 
  и добавлять его в список доступных агентов.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_socialize(setup):
    an_oscar = create_oscar_the_architect()
    a_lisa = create_lisa_the_data_scientist()
    for agent in [an_oscar, a_lisa]:
        other = a_lisa if agent.name == "Oscar" else an_oscar
        agent.make_agent_accessible(other, relation_description="My friend")
        agent.listen(f"Hi {agent.name}, I am {other.name}.")
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."
        assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since we started a conversation."
        assert contains_action_content(actions, agent_first_name(other)), f"{agent.name} should mention {other.name}'s first name in the TALK action, since they are friends."
```

### `test_see(setup)`

**Цель**: Проверка функции `see`, которая позволяет агенту обрабатывать визуальный стимул.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_see(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.see("A beautiful sunset over the ocean.")
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."
        assert contains_action_type(actions, "THINK"), f"{agent.name} should have at least one THINK action to perform, since they saw something interesting."
        assert contains_action_content(actions, "sunset"), f"{agent.name} should mention the sunset in the THINK action, since they saw it."
```

### `test_think(setup)`

**Цель**: Проверка функции `think`, которая позволяет агенту обрабатывать мысленные действия.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_think(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.think("I will tell everyone right now how awesome life is!")
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."
        assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since they are eager to talk."
        assert contains_action_content(actions, "life"), f"{agent.name} should mention life in the TALK action, since they thought about it."
```

### `test_internalize_goal(setup)`

**Цель**: Проверка функции `internalize_goal`, которая позволяет агенту добавить цель в свое состояние.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_internalize_goal(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.internalize_goal("I want to compose in my head a wonderful poem about how cats are glorious creatures.")
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f"{agent.name} should have at least one action to perform."
        assert contains_action_type(actions, "THINK"), f"{agent.name} should have at least one THINK action to perform, since they internalized a goal."
        assert contains_action_content(actions, "cats"), f"{agent.name} should mention cats in the THINK action, since they internalized a goal about them."
```

### `test_move_to(setup)`

**Цель**: Проверка функции `move_to`, которая позволяет агенту перемещаться в новое местоположение.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_move_to(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.move_to("New York", context=["city", "busy", "diverse"])
        assert agent._mental_state["location"] == "New York", f"{agent.name} should have New York as the current location."
        assert "city" in agent._mental_state["context"], f"{agent.name} should have city as part of the current context."
        assert "busy" in agent._mental_state["context"], f"{agent.name} should have busy as part of the current context."
        assert "diverse" in agent._mental_state["context"], f"{agent.name} should have diverse as part of the current context."
```

### `test_change_context(setup)`

**Цель**: Проверка функции `change_context`, которая позволяет агенту изменить контекст.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_change_context(setup):
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.change_context(["home", "relaxed", "comfortable"])
        assert "home" in agent._mental_state["context"], f"{agent.name} should have home as part of the current context."
        assert "relaxed" in agent._mental_state["context"], f"{agent.name} should have relaxed as part of the current context."
        assert "comfortable" in agent._mental_state["context"], f"{agent.name} should have comfortable as part of the current context."
```

### `test_save_specification(setup)`

**Цель**: Проверка функции `save_specification`, которая позволяет агенту сохранить свою конфигурацию 
  в файл.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_save_specification(setup):   
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.save_specification(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json"), include_memory=True)
        assert os.path.exists(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json")), f"{agent.name} should have saved the file."
        loaded_name = f"{agent.name}_loaded"
        loaded_agent = TinyPerson.load_specification(get_relative_to_test_path(f"{EXPORT_BASE_FOLDER}/serialization/{agent.name}.tinyperson.json"), new_agent_name=loaded_name)
        assert loaded_agent.name == loaded_name, f"{agent.name} should have the same name as the loaded agent."
        assert agents_personas_are_equal(agent, loaded_agent, ignore_name=True), f"{agent.name} should have the same configuration as the loaded agent, except for the name."
```

### `test_programmatic_definitions(setup)`

**Цель**: Проверка  сценария,  где агент  программно  определяет  свои  свойства  и  действия.

**Параметры**:

  - `setup`: Фикстура для настройки тестовой среды.

**Пример**:

```python
def test_programmatic_definitions(setup):
    for agent in [create_oscar_the_architect_2(), create_lisa_the_data_scientist_2()]:
        agent.listen_and_act("Tell me a bit about your life.")
```

## Фикстуры

### `setup`

Фикстура `setup` используется для настройки тестовой среды перед запуском каждого теста. Она не имеет 
  описания,  так  как  ее  реализация  находится  в  отдельном  файле  `testing_utils.py`, который не 
  предоставлен.

## Дополнительные функции

### `create_oscar_the_architect()`, `create_lisa_the_data_scientist()`, 
### `create_oscar_the_architect_2()`, `create_lisa_the_data_scientist_2()`

Эти функции создают экземпляры  агентов  `Oscar` и `Lisa` с  определенными  характеристиками 
  и  конфигурациями.   Их  реализация  также  находится  в  файле  `testing_utils.py`.

### `contains_action_type(actions, action_type)`, 
### `terminates_with_action_type(actions, action_type)`,
### `contains_action_content(actions, content)`, 
### `agent_first_name(agent)`

Эти  функции  используются  для  проверки  содержимого  и  типов  действий  агента,  
  а  также  для  извлечения  имени  агента.  Реализация  этих  функций  находится  в  файле  
  `testing_utils.py`.

### `get_relative_to_test_path(file_path)`, `agents_personas_are_equal(agent1, agent2, ignore_name=False)`

Эти функции используются для работы с файлами и для сравнения конфигураций агентов. Реализация 
  этих  функций  находится  в  файле  `testing_utils.py`.

##  Важно

- В  данном  модуле  используется  `logger`  из  `src.logger.logger` для  вывода  информации  
  и  отладки.
-  Тесты  могут  использовать  встроенный  `pytest` для  запуска  и  управления  тестовым  
  процессом.
-  `EXPORT_BASE_FOLDER` -  глобальная  константа,  определяющая  каталог  для  сохранения  
  данных,  используемая  в  тестах.
-  Реализация  некоторых  функций  находится  в  отдельном  файле  `testing_utils.py`, который 
  не  предоставлен.
-  Тесты  используют  функции,  связанные  с  `TinyPerson`,  что  указывает  на  то,  что  
  данный  модуль  является  частью  тестовой  среды  для  класса  `TinyPerson`.