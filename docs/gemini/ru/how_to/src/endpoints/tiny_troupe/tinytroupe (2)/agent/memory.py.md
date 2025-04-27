## Как использовать класс TinyMemory
=========================================================================================

Описание
-------------------------
Класс `TinyMemory` - это базовый класс для различных типов памяти, которые могут быть использованы в агенте. Он предоставляет методы для хранения, извлечения и управления информацией в памяти. 

Шаги выполнения
-------------------------
1. **Создание экземпляра класса:** Создайте объект класса `TinyMemory`, например: `memory = TinyMemory()`.
2. **Хранение значения:** Используйте метод `store(value: dict)` для хранения значения в памяти. 
3. **Извлечение значения:** Используйте методы `retrieve(first_n: int, last_n: int, include_omission_info:bool=True)`, `retrieve_recent(include_omission_info:bool=True)`, `retrieve_all()`, `retrieve_relevant(relevance_target:str, top_k=20)` для извлечения значений из памяти. 

Пример использования
-------------------------

```python
from tinytroupe.agent.memory import TinyMemory

# Создаем экземпляр класса TinyMemory
memory = TinyMemory()

# Храним значение в памяти
memory.store({'type': 'action', 'content': 'Я открыл дверь', 'simulation_timestamp': '2023-10-26 10:00:00'})

# Извлекаем последнее значение
last_value = memory.retrieve_recent()
print(last_value)

# Извлекаем первые 3 значения
first_three_values = memory.retrieve(first_n=3)
print(first_three_values)

# Извлекаем все значения
all_values = memory.retrieve_all()
print(all_values)

# Извлекаем значения, связанные с заданным целевым значением (например, "дверь")
relevant_values = memory.retrieve_relevant(relevance_target='дверь')
print(relevant_values)
```

**Важно:** 

-  `TinyMemory` - это базовый класс. Для реализации конкретного типа памяти, необходимо создать подкласс `TinyMemory` и реализовать методы `_store` и `retrieve`.
- Класс `EpisodicMemory` - это подкласс `TinyMemory`, который реализует эпизодическую память. 
- Класс `SemanticMemory` - это подкласс `TinyMemory`, который реализует семантическую память.