## Как использовать класс `TinyTool`
=========================================================================================

Описание
-------------------------
Класс `TinyTool` - это базовый класс для создания инструментов в TinyTroupe. Он предоставляет стандартные функции для проверки прав доступа, предупреждения о потенциальных реальных последствиях и обработки действий агентов. 

Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создайте экземпляр класса `TinyTool`, передав в него имя, описание, владельца (опционально), флаг `real_world_side_effects` (указывает на реальные последствия, которые могут иметь действия инструмента), экспортер (для сохранения результатов) и enricher (для обогащения результатов).
    - Например:
        ```python
        from tinytroupe.tools import TinyTool
        my_tool = TinyTool("My Tool", "This is a tool for doing something", owner="Agent1", real_world_side_effects=True)
        ```
2. **Определение действий**:
    - Переопределите метод `_process_action` в подклассе `TinyTool` и определите логику выполнения действий, которые инструмент должен выполнить.
3. **Защита от реальных последствий**:
    - Метод `_protect_real_world` предупреждает пользователя о потенциальных реальных последствиях, если инструмент имеет флаг `real_world_side_effects`.
4. **Проверка прав доступа**:
    - Метод `_enforce_ownership` проверяет, что агент, использующий инструмент, имеет права доступа к нему.
5. **Обработка действий**:
    - Метод `process_action` объединяет проверку прав доступа, предупреждение о реальных последствиях и выполнение действий.
6. **Определение подсказок**:
    - Переопределите методы `actions_definitions_prompt` и `actions_constraints_prompt` в подклассе `TinyTool` для предоставления подсказок по определению действий и ограничений, которые инструмент может выполнять.

Пример использования
-------------------------

```python
from tinytroupe.tools import TinyTool
from tinytroupe.agents import Agent

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None):
        super().__init__(name, description, owner, real_world_side_effects=False)

    def _process_action(self, agent, action: dict) -> bool:
        # Здесь реализуйте логику выполнения действия
        print(f"Agent {agent.name} выполняет действие {action} с помощью инструмента {self.name}")
        return True

my_tool = MyTool("My Tool", "This tool does something.")
my_agent = Agent("Agent1")

my_tool.process_action(my_agent, {"action": "do something"}) 
```