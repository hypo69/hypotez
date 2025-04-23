### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор утилитных функций, предназначенных для работы с сущностями агентов и окружений в контексте Tiny Troupe. Функции включают в себя получение имени, генерацию детерминированных хешей и управление уникальными идентификаторами.

Шаги выполнения
-------------------------
1. **`name_or_empty(named_entity: AgentOrWorld)`**:
   - Функция принимает сущность агента или окружения (`named_entity`).
   - Проверяет, является ли сущность `None`.
   - Если сущность не `None`, возвращает её имя.
   - Если сущность `None`, возвращает пустую строку.

2. **`custom_hash(obj)`**:
   - Функция принимает произвольный объект (`obj`).
   - Преобразует объект в строку.
   - Вычисляет SHA-256 хеш от строкового представления объекта, обеспечивая детерминированный хеш.
   - Возвращает хеш в шестнадцатеричном формате.

3. **`fresh_id()`**:
   - Функция генерирует уникальный идентификатор.
   - Увеличивает глобальный счетчик `_fresh_id_counter`.
   - Возвращает текущее значение счетчика.

4. **`reset_fresh_id()`**:
   - Функция сбрасывает счетчик уникальных идентификаторов `_fresh_id_counter` в ноль.
   - Используется для сброса состояния генерации идентификаторов, например, в тестах.

Пример использования
-------------------------

```python
import hashlib
from typing import Union
AgentOrWorld = Union["TinyPerson", "TinyWorld"]

################################################################################
# Other
################################################################################
def name_or_empty(named_entity: AgentOrWorld):
    """
    Returns the name of the specified agent or environment, or an empty string if the agent is None.
    """
    if named_entity is None:
        return ""
    else:
        return named_entity.name

def custom_hash(obj):
    """
    Returns a hash for the specified object. The object is first converted
    to a string, to make it hashable. This method is deterministic,
    contrary to the built-in hash() function.
    """

    return hashlib.sha256(str(obj).encode()).hexdigest()

_fresh_id_counter = 0
def fresh_id():
    """
    Returns a fresh ID for a new object. This is useful for generating unique IDs for objects.
    """
    global _fresh_id_counter
    _fresh_id_counter += 1
    return _fresh_id_counter

def reset_fresh_id():
    """
    Resets the fresh ID counter. This is useful for testing purposes.
    """
    global _fresh_id_counter
    _fresh_id_counter = 0

# Пример использования name_or_empty
class MockAgent:
    def __init__(self, name):
        self.name = name

agent = MockAgent("Alice")
empty_name = name_or_empty(None)
agent_name = name_or_empty(agent)
print(f"Имя агента: {agent_name}")
print(f"Имя пустого агента: {empty_name}")

# Пример использования custom_hash
obj1 = "Пример строки"
obj2 = {"ключ": "значение"}
hash1 = custom_hash(obj1)
hash2 = custom_hash(obj2)
print(f"Хеш строки: {hash1}")
print(f"Хеш словаря: {hash2}")

# Пример использования fresh_id и reset_fresh_id
id1 = fresh_id()
id2 = fresh_id()
print(f"Первый ID: {id1}")
print(f"Второй ID: {id2}")

reset_fresh_id()
id3 = fresh_id()
print(f"ID после сброса: {id3}")