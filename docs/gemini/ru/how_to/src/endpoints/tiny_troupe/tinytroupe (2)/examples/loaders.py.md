## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код обеспечивает функции для загрузки и перечисления примеров спецификаций агентов и фрагментов, которые используются в TinyTroupe. 

Шаги выполнения
-------------------------
1. **Функции `load_example_agent_specification` и `load_example_fragment_specification`** загружают JSON-файлы, представляющие спецификации агентов и фрагментов соответственно. Они принимают имя агента или фрагмента в качестве параметра и возвращают словарь, представляющий спецификацию.
2. **Функции `list_example_agents` и `list_example_fragments`** возвращают списки доступных примеров агентов и фрагментов, которые хранятся в соответствующих папках. Они перечисляют все JSON-файлы в указанной папке и удаляют суффикс ".agent.json" или ".fragment.json" из имен файлов, чтобы получить имена агентов или фрагментов.

Пример использования
-------------------------

```python
    from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).examples.loaders import load_example_agent_specification, list_example_agents

    # Загрузить спецификацию агента по имени
    agent_spec = load_example_agent_specification('my_agent')
    print(f'Agent specification: {agent_spec}') 

    # Перечислить доступные агенты
    available_agents = list_example_agents()
    print(f'Available agents: {available_agents}') 
```