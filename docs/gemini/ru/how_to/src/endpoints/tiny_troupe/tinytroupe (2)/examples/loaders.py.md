Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода предоставляет функции для загрузки и перечисления примеров спецификаций агентов и фрагментов, хранящихся в формате JSON. Он предназначен для упрощения доступа к предварительно определенным конфигурациям агентов и фрагментов, что может быть полезно для тестирования, демонстрации или в качестве отправной точки для создания новых агентов и фрагментов.

Шаги выполнения
-------------------------
1. **Загрузка спецификации агента:**
   - Функция `load_example_agent_specification(name: str)` извлекает JSON-файл, содержащий спецификацию агента, основываясь на переданном имени агента.
   - Функция формирует путь к файлу, объединяя имя агента с расширением `.agent.json` и базовым путем к директории `agents`.
   - Использует `json.load` для преобразования содержимого файла в словарь Python.

2. **Загрузка спецификации фрагмента:**
   - Функция `load_example_fragment_specification(name: str)` аналогична функции загрузки агента, но предназначена для фрагментов.
   - Она извлекает JSON-файл, содержащий спецификацию фрагмента, основываясь на переданном имени фрагмента.
   - Функция формирует путь к файлу, объединяя имя фрагмента с расширением `.fragment.json` и базовым путем к директории `fragments`.
   - Использует `json.load` для преобразования содержимого файла в словарь Python.

3. **Получение списка доступных агентов:**
   - Функция `list_example_agents()` сканирует директорию `agents` и возвращает список имен файлов, представляющих доступные примеры агентов.
   - Функция исключает расширение `.agent.json` из каждого имени файла, чтобы предоставить чистый список имен агентов.

4. **Получение списка доступных фрагментов:**
   - Функция `list_example_fragments()` сканирует директорию `fragments` и возвращает список имен файлов, представляющих доступные примеры фрагментов.
   - Функция исключает расширение `.fragment.json` из каждого имени файла, чтобы предоставить чистый список имен фрагментов.

Пример использования
-------------------------

```python
import json
import os

def load_example_agent_specification(name:str):
    """
    Load an example agent specification.

    Args:
        name (str): The name of the agent.

    Returns:
        dict: The agent specification.
    """
    return json.load(open(os.path.join(os.path.dirname(__file__), f'./agents/{name}.agent.json')))

def load_example_fragment_specification(name:str):
    """
    Load an example fragment specification.

    Args:
        name (str): The name of the fragment.

    Returns:
        dict: The fragment specification.
    """
    return json.load(open(os.path.join(os.path.dirname(__file__), f'./fragments/{name}.fragment.json')))

def list_example_agents():
    """
    List the available example agents.

    Returns:
        list: A list of the available example agents.
    """
    return [f.replace('.agent.json', '') for f in os.listdir(os.path.join(os.path.dirname(__file__), './agents'))]

def list_example_fragments():
    """
    List the available example fragments.

    Returns:
        list: A list of the available example fragments.
    """
    return [f.replace('.fragment.json', '') for f in os.listdir(os.path.join(os.path.dirname(__file__), './fragments'))]

# Пример использования
agent_name = "example"  # Замените на имя нужного агента
agent_specification = load_example_agent_specification(agent_name)
print(f"Спецификация агента '{agent_name}': {agent_specification}")

fragment_name = "example"  # Замените на имя нужного фрагмента
fragment_specification = load_example_fragment_specification(fragment_name)
print(f"Спецификация фрагмента '{fragment_name}': {fragment_specification}")

available_agents = list_example_agents()
print(f"Доступные агенты: {available_agents}")

available_fragments = list_example_fragments()
print(f"Доступные фрагменты: {available_fragments}")