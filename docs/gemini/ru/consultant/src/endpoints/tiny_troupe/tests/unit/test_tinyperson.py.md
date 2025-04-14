### **Анализ кода модуля `test_tinyperson.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на отдельные тестовые функции, каждая из которых тестирует определенную функциональность агента.
    - Используются assertions для проверки ожидаемого поведения агентов.
    - Присутствуют комментарии, описывающие назначение тестов.
- **Минусы**:
    - Не все функции и переменные аннотированы типами.
    - Docstring отсутствует во многих функциях.
    - Используются устаревшие способы добавления путей в `sys.path`.
    - Не используется модуль `logger` из `src.logger` для логирования.
    - Некоторые комментарии не достаточно информативны и используют расплывчатые формулировки.
    - Не все строки используют одинарные кавычки.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.

2.  **Добавить docstring**:
    - Добавить docstring к каждой функции, описывающий ее назначение, аргументы, возвращаемые значения и возможные исключения.
    - Перевести существующие docstring на русский язык.

3.  **Улучшить импорт модулей**:
    - Избегать использования `sys.path.insert` для добавления путей к модулям. Вместо этого, настроить структуру проекта и использовать относительные импорты или установить пакет в виртуальное окружение.

4.  **Использовать модуль логирования `src.logger`**:
    - Заменить `logging.getLogger("tinytroupe")` на `from src.logger import logger` и использовать `logger.info`, `logger.error` и т.д. для логирования.

5.  **Улучшить комментарии**:
    - Сделать комментарии более информативными и конкретными. Избегать расплывчатых формулировок.
    - Использовать русские комментарии.

6.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные, где это необходимо.

7.  **Удалить неиспользуемые импорты и закомментированный код**:
    - Удалить неиспользуемые импорты `import pytest` и закомментированные строки `sys.path.append(...)`.

**Оптимизированный код:**

```python
import os
import sys
from typing import List

# Убеждаемся, что пакет tinytroupe импортируется из родительской директории
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tinytroupe/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# from src.logger import logger # TODO Раскомментировать когда будет решен вопрос с импортом модулей

from tinytroupe.examples import (
    create_oscar_the_architect,
    create_oscar_the_architect_2,
    create_lisa_the_data_scientist,
    create_lisa_the_data_scientist_2,
)
from tinytroupe.tinyperson import TinyPerson

from testing_utils import *


def test_act(setup: None) -> None:
    """
    Тестирует поведение агентов при выполнении действий в ответ на стимул.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None

    """
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        actions = agent.listen_and_act('Tell me a bit about your life.', return_actions=True)

        # logger.info(agent.pp_current_interactions()) # TODO Раскомментировать когда будет решен вопрос с импортом модулей

        assert len(actions) >= 1, f'{agent.name} should have at least one action to perform (even if it is just DONE).'
        assert contains_action_type(actions, 'TALK'), f'{agent.name} should have at least one TALK action to perform, since we asked him to do so.'
        assert terminates_with_action_type(actions, 'DONE'), f'{agent.name} should always terminate with a DONE action.'


def test_listen(setup: None) -> None:
    """
    Тестирует способность агента воспринимать речь и обновлять свои текущие сообщения.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что агент слушает речевой стимул и обновляет свои текущие сообщения
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.listen('Hello, how are you?')

        assert len(agent.current_messages) > 0, f'{agent.name} should have at least one message in its current messages.'
        assert agent.episodic_memory.retrieve_all()[-1]['role'] == 'user', f'{agent.name} should have the last message as \'user\'.'
        assert agent.episodic_memory.retrieve_all()[-1]['content']['stimuli'][0]['type'] == 'CONVERSATION', f'{agent.name} should have the last message as a \'CONVERSATION\' stimulus.'
        assert agent.episodic_memory.retrieve_all()[-1]['content']['stimuli'][0]['content'] == 'Hello, how are you?', f'{agent.name} should have the last message with the correct content.'


def test_define(setup: None) -> None:
    """
    Тестирует определение нового значения в конфигурации агента и сброс его prompt.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что агент определяет значение в своей конфигурации и сбрасывает свой prompt
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        # Сохраняем оригинальный prompt
        original_prompt = agent.current_messages[0]['content']

        # Определяем новое значение
        agent.define('age', 25)

        # Проверяем, что конфигурация имеет новое значение
        assert agent._persona['age'] == 25, f'{agent.name} should have the age set to 25.'

        # Проверяем, что prompt изменился
        assert agent.current_messages[0]['content'] != original_prompt, f'{agent.name} should have a different prompt after defining a new value.'

        # Проверяем, что prompt содержит новое значение
        assert '25' in agent.current_messages[0]['content'], f'{agent.name} should have the age in the prompt.'


def test_define_several(setup: None) -> None:
    """
    Тестирует определение нескольких значений в группе конфигурации агента.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что определение нескольких значений для группы работает правильно
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.define('skills', ['Python', 'Machine learning', 'GPT-3'])

        assert 'Python' in agent._persona['skills'], f'{agent.name} should have Python as a skill.'
        assert 'Machine learning' in agent._persona['skills'], f'{agent.name} should have Machine learning as a skill.'
        assert 'GPT-3' in agent._persona['skills'], f'{agent.name} should have GPT-3 as a skill.'


def test_socialize(setup: None) -> None:
    """
    Тестирует взаимодействие агента с другим агентом.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что взаимодействие с другим агентом работает правильно
    an_oscar = create_oscar_the_architect()
    a_lisa = create_lisa_the_data_scientist()
    for agent in [an_oscar, a_lisa]:
        other = a_lisa if agent.name == 'Oscar' else an_oscar
        agent.make_agent_accessible(other, relation_description='My friend')
        agent.listen(f'Hi {agent.name}, I am {other.name}.')
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f'{agent.name} should have at least one action to perform.'
        assert contains_action_type(actions, 'TALK'), f'{agent.name} should have at least one TALK action to perform, since we started a conversation.'
        assert contains_action_content(actions, agent_first_name(other)), f'{agent.name} should mention {other.name}\'s first name in the TALK action, since they are friends.'


def test_see(setup: None) -> None:
    """
    Тестирует реакцию агента на визуальный стимул.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что просмотр визуального стимула работает правильно
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.see('A beautiful sunset over the ocean.')
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f'{agent.name} should have at least one action to perform.'
        assert contains_action_type(actions, 'THINK'), f'{agent.name} should have at least one THINK action to perform, since they saw something interesting.'
        assert contains_action_content(actions, 'sunset'), f'{agent.name} should mention the sunset in the THINK action, since they saw it.'


def test_think(setup: None) -> None:
    """
    Тестирует процесс мышления агента.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что размышление о чем-то работает правильно
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.think('I will tell everyone right now how awesome life is!')
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f'{agent.name} should have at least one action to perform.'
        assert contains_action_type(actions, 'TALK'), f'{agent.name} should have at least one TALK action to perform, since they are eager to talk.'
        assert contains_action_content(actions, 'life'), f'{agent.name} should mention life in the TALK action, since they thought about it.'


def test_internalize_goal(setup: None) -> None:
    """
    Тестирует усвоение цели агентом.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что интернализация цели работает правильно
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.internalize_goal('I want to compose in my head a wonderful poem about how cats are glorious creatures.')
        actions = agent.act(return_actions=True)
        assert len(actions) >= 1, f'{agent.name} should have at least one action to perform.'
        assert contains_action_type(actions, 'THINK'), f'{agent.name} should have at least one THINK action to perform, since they internalized a goal.'
        assert contains_action_content(actions, 'cats'), f'{agent.name} should mention cats in the THINK action, since they internalized a goal about them.'


def test_move_to(setup: None) -> None:
    """
    Тестирует перемещение агента в новую локацию.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что перемещение в новую локацию работает правильно
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.move_to('New York', context=['city', 'busy', 'diverse'])
        assert agent._mental_state['location'] == 'New York', f'{agent.name} should have New York as the current location.'
        assert 'city' in agent._mental_state['context'], f'{agent.name} should have city as part of the current context.'
        assert 'busy' in agent._mental_state['context'], f'{agent.name} should have busy as part of the current context.'
        assert 'diverse' in agent._mental_state['context'], f'{agent.name} should have diverse as part of the current context.'


def test_change_context(setup: None) -> None:
    """
    Тестирует изменение контекста агента.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем, что изменение контекста работает правильно
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.change_context(['home', 'relaxed', 'comfortable'])
        assert 'home' in agent._mental_state['context'], f'{agent.name} should have home as part of the current context.'
        assert 'relaxed' in agent._mental_state['context'], f'{agent.name} should have relaxed as part of the current context.'
        assert 'comfortable' in agent._mental_state['context'], f'{agent.name} should have comfortable as part of the current context.'


def test_save_specification(setup: None) -> None:
    """
    Тестирует сохранение спецификации агента в файл и загрузку из файла.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    # Проверяем сохранение спецификации агента
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        # Сохраняем в файл
        agent.save_specification(get_relative_to_test_path(f'EXPORT_BASE_FOLDER/serialization/{agent.name}.tinyperson.json'), include_memory=True)

        # Проверяем, что файл существует
        assert os.path.exists(get_relative_to_test_path(f'EXPORT_BASE_FOLDER/serialization/{agent.name}.tinyperson.json')), f'{agent.name} should have saved the file.'

        # Загружаем файл, чтобы проверить, что агент такой же. Имя агента должно отличаться, потому что TinyTroupe не допускает двух агентов с одинаковым именем.
        loaded_name = f'{agent.name}_loaded'
        loaded_agent = TinyPerson.load_specification(get_relative_to_test_path(f'EXPORT_BASE_FOLDER/serialization/{agent.name}.tinyperson.json'), new_agent_name=loaded_name)

        # Проверяем, что загруженный агент такой же, как оригинал
        assert loaded_agent.name == loaded_name, f'{agent.name} should have the same name as the loaded agent.'

        assert agents_personas_are_equal(agent, loaded_agent, ignore_name=True), f'{agent.name} should have the same configuration as the loaded agent, except for the name.'


def test_programmatic_definitions(setup: None) -> None:
    """
    Тестирует программное определение параметров агента.

    Args:
        setup (None): Параметр setup, предоставляемый pytest фикстурой.

    Returns:
        None
    """
    for agent in [create_oscar_the_architect_2(), create_lisa_the_data_scientist_2()]:
        agent.listen_and_act('Tell me a bit about your life.')