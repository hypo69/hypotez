### **Анализ кода модуля `testing_utils.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tests/testing_utils.py

Модуль содержит набор утилитных функций, используемых для тестирования TinyTroupe. Он включает в себя функции для кэширования, управления файлами, проверки симуляций, создания сообщений, сравнения агентов и работы с путями.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и содержит полезные утилиты для тестирования.
    - Присутствуют функции для работы с кэшем, что позволяет экономить на использовании API.
    - Имеются функции для проверки содержимого действий и стимулов в симуляциях.
    - Есть функции для сравнения агентов и создания сообщений.
- **Минусы**:
    - Отсутствуют docstring для некоторых функций, что затрудняет понимание их назначения.
    - Не все переменные аннотированы типами.
    - Используется устаревший способ добавления путей в `sys.path`.
    - Некоторые комментарии недостаточно информативны.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех функций и классов**, чтобы улучшить понимание кода.
2.  **Добавить аннотации типов для всех переменных и аргументов функций**.
3.  **Заменить устаревший способ добавления путей в `sys.path`** на более современный, например, с использованием `pathlib`.
4.  **Улучшить комментарии**, сделав их более информативными и понятными.
5.  **Использовать `logger`** для логирования вместо `print`.
6.  **Изменить структуру** хранения глобальных переменных, чтобы уменьшить вероятность конфликтов.

**Оптимизированный код:**

```python
"""
Модуль тестирования утилит.
=================================================

Модуль содержит набор утилитных функций, используемых для тестирования TinyTroupe.
Он включает в себя функции для кэширования, управления файлами, проверки симуляций,
создания сообщений, сравнения агентов и работы с путями.
"""
import os
import sys
from time import sleep
from typing import List, Dict, Any, Optional
from pathlib import Path
import pytest
import importlib

# Импорт модулей из проекта TinyTroupe
sys.path.insert(0, '../../tinytroupe/')
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

import tinytroupe.openai_utils as openai_utils
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork

import conftest

# Импорт модуля логгера
from src.logger import logger

##################################################
# Глобальные константы
##################################################
CACHE_FILE_NAME: str = 'tests_cache.pickle'
EXPORT_BASE_FOLDER: str = os.path.join(os.path.dirname(__file__), 'outputs/exports')
TEMP_SIMULATION_CACHE_FILE_NAME: str = os.path.join(os.path.dirname(__file__), 'simulation_test_case.cache.json')


##################################################
# Кэширование для экономии на использовании API
##################################################
if conftest.refresh_cache:
    # Удаление файла кэша tests_cache.pickle
    try:
        os.remove(CACHE_FILE_NAME)
        logger.info(f'Cache file {CACHE_FILE_NAME} removed.')
    except FileNotFoundError as ex:
        logger.warning(f'Cache file {CACHE_FILE_NAME} not found.', ex, exc_info=True)

if conftest.use_cache:
    openai_utils.force_api_cache(True, CACHE_FILE_NAME)
    logger.info(f'API cache enabled, using cache file {CACHE_FILE_NAME}.')
else:
    openai_utils.force_api_cache(False, CACHE_FILE_NAME)
    logger.info('API cache disabled.')


##################################################
# Управление файлами
##################################################

def remove_file_if_exists(file_path: str) -> None:
    """
    Удаляет файл по указанному пути, если он существует.

    Args:
        file_path (str): Путь к файлу.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f'File {file_path} removed.')


# Удаление временных файлов
remove_file_if_exists(TEMP_SIMULATION_CACHE_FILE_NAME)


##################################################
# Утилиты для проверки симуляций
##################################################

def contains_action_type(actions: List[Dict[str, Any]], action_type: str) -> bool:
    """
    Проверяет, содержит ли данный список действий действие указанного типа.

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
    Проверяет, содержит ли данный список действий действие с указанным содержимым.

    Args:
        actions (List[Dict[str, Any]]): Список действий.
        action_content (str): Содержимое действия для проверки.

    Returns:
        bool: True, если список содержит действие с указанным содержимым, иначе False.
    """
    for action in actions:
        # Проверяет, содержится ли желаемое содержимое в содержимом действия
        if action_content.lower() in action['action']['content'].lower():
            return True
    return False


def contains_stimulus_type(stimuli: List[Dict[str, Any]], stimulus_type: str) -> bool:
    """
    Проверяет, содержит ли данный список стимулов стимул указанного типа.

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
    Проверяет, содержит ли данный список стимулов стимул с указанным содержимым.

    Args:
        stimuli (List[Dict[str, Any]]): Список стимулов.
        stimulus_content (str): Содержимое стимула для проверки.

    Returns:
        bool: True, если список содержит стимул с указанным содержимым, иначе False.
    """
    for stimulus in stimuli:
        # Проверяет, содержится ли желаемое содержимое в содержимом стимула
        if stimulus_content.lower() in stimulus['content'].lower():
            return True
    return False


def terminates_with_action_type(actions: List[Dict[str, Any]], action_type: str) -> bool:
    """
    Проверяет, завершается ли данный список действий действием указанного типа.

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
    Проверяет, истинно ли данное утверждение согласно вызову LLM.
    Это можно использовать для проверки текстовых свойств, которые трудно
    проверить механически, например, "текст содержит некоторые идеи для продукта".

    Args:
        proposition (str): Утверждение для проверки.

    Returns:
        bool: True, если утверждение истинно, иначе False.

    Raises:
        Exception: Если LLM возвращает неожиданный результат.
    """
    system_prompt: str = """
    Проверьте, является ли следующее утверждение истинным или ложным. Если это
    правда, напишите "true", иначе напишите "false". Не пишите ничего другого!
    """

    user_prompt: str = f"""
    Утверждение: {proposition}
    """

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt},
                                      {"role": "user", "content": user_prompt}]

    # Вызов LLM
    next_message: Dict[str, Any] = openai_utils.client().send_message(messages)

    # Проверка результата
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
        string (str): Исходная строка.

    Returns:
        str: Строка, содержащая только буквенно-цифровые символы.
    """
    return ''.join(c for c in string if c.isalnum())


def create_test_system_user_message(user_prompt: Optional[str], system_prompt: str = 'You are a helpful AI assistant.') -> List[Dict[str, str]]:
    """
    Создает список, содержащий одно системное сообщение и одно пользовательское сообщение.

    Args:
        user_prompt (Optional[str]): Пользовательское сообщение.
        system_prompt (str): Системное сообщение.

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
        ignore_name (bool): Нужно ли игнорировать имя при сравнении.

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
    Фикстура для создания мира фокус-группы.

    Returns:
        TinyWorld: Мир фокус-группы.
    """
    import tinytroupe.examples as examples

    world: TinyWorld = TinyWorld('Focus group', [examples.create_lisa_the_data_scientist(), examples.create_oscar_the_architect(), examples.create_marcos_the_physician()])
    return world


@pytest.fixture(scope='function')
def setup() -> None:
    """
    Фикстура для настройки тестов.
    """
    TinyPerson.clear_agents()
    TinyWorld.clear_environments()

    yield