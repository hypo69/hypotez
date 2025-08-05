# Модуль TinySocialNetwork

## Обзор

Этот модуль реализует среду TinySocialNetwork, которая представляет собой  тип среды TinyWorld, 
специализированный для имитации социальных сетей. 

## Подробней

Модуль TinySocialNetwork наследует от TinyWorld и реализует дополнительную функциональность, связанную 
с отношениями между агентами (TinyPerson), такими как добавление и проверка отношений между агентами. 

## Классы

### `TinySocialNetwork`

**Описание**: Класс, представляющий собой среду TinySocialNetwork. Наследуется от TinyWorld.

**Наследует**: TinyWorld

**Атрибуты**:

- `relations (dict)`: Словарь, хранящий все отношения между агентами. Ключи словаря - имена отношений, 
  значения - списки пар агентов, находящихся в этом отношении. 

**Методы**:

- `add_relation(self, agent_1, agent_2, name="default")`:  Добавляет отношение между двумя агентами. 
  Автоматически добавляет агентов в список агентов среды, если они еще не добавлены.

- `_update_agents_contexts(self)`: Обновляет контексты наблюдения агентов на основе их отношений 
  и состояния мира. 

- `_step(self)`: Выполняет шаг в среде, вызывая метод _step базового класса и обновляя 
  контексты наблюдения агентов.

- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие 
  REACH_OUT. В этой реализации действие REACH_OUT может быть выполнено только в том случае, 
  если целевой агент находится в том же отношении, что и исходный агент. 

- `is_in_relation_with(self, agent_1:TinyPerson, agent_2:TinyPerson, relation_name=None) -> bool`: 
  Проверяет, находятся ли два агента в отношении. 

**Примеры**:

```python
# Создание среды TinySocialNetwork
network = TinySocialNetwork("MySocialNetwork")

# Создание агентов
alice = TinyPerson("Alice")
bob = TinyPerson("Bob")

# Добавление отношения между агентами
network.add_relation(alice, bob, name="Friends")

# Проверка отношения между агентами
print(network.is_in_relation_with(alice, bob, name="Friends"))  # Вывод: True
print(network.is_in_relation_with(alice, bob, name="Enemies"))  # Вывод: False
```

## Функции

### `is_in_relation_with`

**Назначение**:  Проверяет, находятся ли два агента в отношении. 

**Параметры**:

- `agent_1 (TinyPerson)`: Первый агент.
- `agent_2 (TinyPerson)`: Второй агент.
- `relation_name (str, optional)`:  Название отношения, которое нужно проверить. Если не указано, 
  проверяется наличие любого отношения. 

**Возвращает**:

- `bool`:  `True`, если агенты находятся в заданном отношении, `False` в противном случае.

**Как работает функция**:

Функция iterates через все отношения в среде TinySocialNetwork. Если `relation_name` не указан, 
проверяется наличие любого отношения между `agent_1` и `agent_2`, иначе проверяется только 
отношение с именем `relation_name`.

**Примеры**:

```python
# Создание среды TinySocialNetwork
network = TinySocialNetwork("MySocialNetwork")

# Создание агентов
alice = TinyPerson("Alice")
bob = TinyPerson("Bob")
charlie = TinyPerson("Charlie")

# Добавление отношений
network.add_relation(alice, bob, name="Friends")
network.add_relation(bob, charlie, name="Colleagues")

# Проверка отношений
print(network.is_in_relation_with(alice, bob, name="Friends"))  # Вывод: True
print(network.is_in_relation_with(alice, charlie)) # Вывод: True (поскольку они связаны через "Bob")
print(network.is_in_relation_with(alice, charlie, name="Friends")) # Вывод: False 
```