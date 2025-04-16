### **Анализ кода модуля `testing_utils.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tests/testing_utils.py

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Наличие функций для облегчения тестирования, таких как проверка типов действий, содержимого стимулов и истинности утверждений.
    - Использование `pytest.fixture` для настройки тестового окружения.
    - Наличие утилит для работы с файлами и путями.
- **Минусы**:
    - Отсутствуют аннотации типов для аргументов и возвращаемых значений функций.
    - Не все функции имеют docstring, что затрудняет понимание их назначения и использования.
    - Использование абсолютных путей в `sys.path.insert` может привести к проблемам при переносе проекта.
    - Нет логирования ошибок и предупреждений.
    - Код не соответствует PEP8 (например, отсутствуют пробелы вокруг операторов).

#### **Рекомендации по улучшению**:

1. **Добавить docstring**:
   - Добавить подробные docstring для каждой функции, включая описание аргументов, возвращаемых значений и возможных исключений.

2. **Добавить аннотации типов**:
   - Добавить аннотации типов для всех аргументов и возвращаемых значений функций.

3. **Улучшить обработку исключений**:
   - Добавить обработку исключений с использованием `try-except` блоков и логированием ошибок с использованием `logger.error`.

4. **Улучшить структуру проекта**:
   - Избегать использования `sys.path.insert` и использовать относительные импорты или настроить `PYTHONPATH`.

5. **Улучшить читаемость**:
   - Следовать стандартам PEP8 для форматирования кода, включая добавление пробелов вокруг операторов.

6. **Использовать `j_loads` или `j_loads_ns`**:
   - Если в коде используются JSON или конфигурационные файлы, заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

#### **Оптимизированный код**:

```python
"""
Модуль содержит утилиты для тестирования.
=========================================

Этот модуль содержит набор утилитных функций и фикстур для облегчения тестирования компонентов TinyTroupe.
Он включает в себя функции для проверки действий, стимулов, утверждений, а также для управления файлами и тестовым окружением.

Пример использования
----------------------

>>> from testing_utils import contains_action_type
>>> actions = [{"action": {"type": "message", "content": "Hello"}}]
>>> contains_action_type(actions, "message")
True
"""
import os
import sys
from time import sleep
from typing import List, Dict, Any, Optional

#sys.path.insert(0, '../../tinytroupe/') # Убрано, т.к. не рекомендуется использовать sys.path.insert
#sys.path.insert(0, '../../')
#sys.path.insert(0, '..')

import tinytroupe.openai_utils as openai_utils
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
import pytest
import importlib

import conftest
from src.logger import logger # Добавлен импорт logger

##################################################
# global constants
##################################################
CACHE_FILE_NAME: str = 'tests_cache.pickle'
EXPORT_BASE_FOLDER: str = os.path.join(os.path.dirname(__file__), 'outputs/exports')
TEMP_SIMULATION_CACHE_FILE_NAME: str = os.path.join(os.path.dirname(__file__), 'simulation_test_case.cache.json')


##################################################
# Caching, in order to save on API usage
##################################################
if conftest.refresh_cache:
    # DELETE the cache file tests_cache.pickle
    try:
        os.remove(CACHE_FILE_NAME)
    except FileNotFoundError as ex:
        logger.warning(f'Cache file {CACHE_FILE_NAME} not found, skipping deletion', ex, exc_info=True) # Добавлено логирование

if conftest.use_cache:
    openai_utils.force_api_cache(True, CACHE_FILE_NAME)
else:
    openai_utils.force_api_cache(False, CACHE_FILE_NAME)


##################################################
# File management
##################################################

def remove_file_if_exists(file_path: str) -> None:
    """
    Удаляет файл по указанному пути, если он существует.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        None
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as ex:
            logger.error(f'Error removing file {file_path}', ex, exc_info=True) # Добавлено логирование

# remove temporary files
remove_file_if_exists(TEMP_SIMULATION_CACHE_FILE_NAME)


##################################################
# Simulation checks utilities
##################################################
def contains_action_type(actions: List[Dict[str, Any]], action_type: str) -> bool:
    """
    Проверяет, содержит ли заданный список действий действие указанного типа.

    Args:
        actions (List[Dict[str, Any]]): Список действий.
        action_type (str): Тип действия для проверки.

    Returns:
        bool: True, если список содержит действие указанного типа, иначе False.
    """
    for action in actions:
        if action['action']['type'] == action_type:
            return True

    return False


def contains_action_content(actions: List[Dict[str, Any]], action_content: str) -> bool:
    """
    Проверяет, содержит ли заданный список действий действие с указанным содержимым.

    Args:
        actions (List[Dict[str, Any]]): Список действий.
        action_content (str): Содержимое действия для проверки.

    Returns:
        bool: True, если список содержит действие с указанным содержимым, иначе False.
    """
    for action in actions:
        # checks whether the desired content is contained in the action content
        if action_content.lower() in action['action']['content'].lower():
            return True

    return False


def contains_stimulus_type(stimuli: List[Dict[str, Any]], stimulus_type: str) -> bool:
    """
    Проверяет, содержит ли заданный список стимулов стимул указанного типа.

    Args:
        stimuli (List[Dict[str, Any]]): Список стимулов.
        stimulus_type (str): Тип стимула для проверки.

    Returns:
        bool: True, если список содержит стимул указанного типа, иначе False.
    """
    for stimulus in stimuli:
        if stimulus['type'] == stimulus_type:
            return True

    return False


def contains_stimulus_content(stimuli: List[Dict[str, Any]], stimulus_content: str) -> bool:
    """
    Проверяет, содержит ли заданный список стимулов стимул с указанным содержимым.

    Args:
        stimuli (List[Dict[str, Any]]): Список стимулов.
        stimulus_content (str): Содержимое стимула для проверки.

    Returns:
        bool: True, если список содержит стимул с указанным содержимым, иначе False.
    """
    for stimulus in stimuli:
        # checks whether the desired content is contained in the stimulus content
        if stimulus_content.lower() in stimulus['content'].lower():
            return True

    return False


def terminates_with_action_type(actions: List[Dict[str, Any]], action_type: str) -> bool:
    """
    Проверяет, завершается ли заданный список действий действием указанного типа.

    Args:
        actions (List[Dict[str, Any]]): Список действий.
        action_type (str): Тип действия для проверки.

    Returns:
        bool: True, если список завершается действием указанного типа, иначе False.
    """
    if len(actions) == 0:
        return False

    return actions[-1]['action']['type'] == action_type


def proposition_holds(proposition: str) -> bool:
    """
    Проверяет, истинно ли заданное утверждение с помощью вызова LLM.

    Args:
        proposition (str): Утверждение для проверки.

    Returns:
        bool: True, если утверждение истинно, иначе False.

    Raises:
        Exception: Если LLM возвращает неожиданный результат.
    """
    system_prompt: str = """
    Check whether the following proposition is true or false. If it is
    true, write "true", otherwise write "false". Don't write anything else!
    """

    user_prompt: str = f"""
    Proposition: {proposition}
    """

    messages: List[Dict[str, str]] = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}]

    # call the LLM
    try:
        next_message = openai_utils.client().send_message(messages)
    except Exception as ex:
        logger.error('Error while sending message to OpenAI', ex, exc_info=True) # Добавлено логирование
        return False

    # check the result
    cleaned_message: str = only_alphanumeric(next_message['content'])
    if cleaned_message.lower().startswith('true'):
        return True
    elif cleaned_message.lower().startswith('false'):
        return False
    else:
        raise Exception(f'LLM returned unexpected result: {cleaned_message}')


def only_alphanumeric(string: str) -> str:
    """
    Возвращает строку, содержащую только буквенно-цифровые символы.

    Args:
        string (str): Входная строка.

    Returns:
        str: Строка, содержащая только буквенно-цифровые символы.
    """
    return ''.join(c for c in string if c.isalnum())


def create_test_system_user_message(user_prompt: Optional[str], system_prompt: str = 'You are a helpful AI assistant.') -> List[Dict[str, str]]:
    """
    Создает список, содержащий одно системное сообщение и одно пользовательское сообщение.

    Args:
        user_prompt (Optional[str]): Пользовательское сообщение.
        system_prompt (str, optional): Системное сообщение. По умолчанию 'You are a helpful AI assistant.'.

    Returns:
        List[Dict[str, str]]: Список сообщений.
    """
    messages: List[Dict[str, str]] = [{'role': 'system', 'content': system_prompt}]

    if user_prompt is not None:
        messages.append({'role': 'user', 'content': user_prompt})

    return messages


def agents_personas_are_equal(agent1: TinyPerson, agent2: TinyPerson, ignore_name: bool = False) -> bool:
    """
    Проверяет, равны ли конфигурации двух агентов.

    Args:
        agent1 (TinyPerson): Первый агент.
        agent2 (TinyPerson): Второй агент.
        ignore_name (bool, optional): Игнорировать ли имя агента. По умолчанию False.

    Returns:
        bool: True, если конфигурации агентов равны, иначе False.
    """
    ignore_keys: List[str] = []
    if ignore_name:
        ignore_keys.append('name')

    for key in agent1._persona.keys():
        if key in ignore_keys:
            continue

        if agent1._persona[key] != agent2._persona[key]:
            return False

    return True


def agent_first_name(agent: TinyPerson) -> str:
    """
    Возвращает имя агента.

    Args:
        agent (TinyPerson): Агент.

    Returns:
        str: Имя агента.
    """
    return agent.name.split()[0]
############################################################################################################
# I/O utilities
############################################################################################################


def get_relative_to_test_path(path_suffix: str) -> str:
    """
    Возвращает путь к тестовому файлу с заданным суффиксом.

    Args:
        path_suffix (str): Суффикс пути.

    Returns:
        str: Путь к тестовому файлу.
    """
    return os.path.join(os.path.dirname(__file__), path_suffix)


############################################################################################################
# Fixtures
############################################################################################################

@pytest.fixture(scope='function')
def focus_group_world() -> TinyWorld:
    """
    Фикстура для создания мира с фокус-группой.

    Returns:
        TinyWorld: Мир с фокус-группой.
    """
    import tinytroupe.examples as examples

    world: TinyWorld = TinyWorld('Focus group', [examples.create_lisa_the_data_scientist(), examples.create_oscar_the_architect(), examples.create_marcos_the_physician()])
    return world


@pytest.fixture(scope='function')
def setup() -> None:
    """
    Фикстура для настройки тестового окружения.

    Yields:
        None
    """
    TinyPerson.clear_agents()
    TinyWorld.clear_environments()

    yield