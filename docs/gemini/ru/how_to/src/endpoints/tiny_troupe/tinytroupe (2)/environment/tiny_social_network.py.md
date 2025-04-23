### Как использовать класс `TinySocialNetwork`
=========================================================================================

Описание
-------------------------
`TinySocialNetwork` - это класс, представляющий собой социальную сеть, основанную на `TinyWorld`. Он расширяет возможности `TinyWorld`, добавляя поддержку отношений между агентами (`TinyPerson`). Класс позволяет создавать, управлять отношениями между агентами и контролировать взаимодействие между ними.

Шаги выполнения
-------------------------
1. **Создание экземпляра `TinySocialNetwork`**:
   - Создайте экземпляр класса `TinySocialNetwork`, указав имя сети и флаг `broadcast_if_no_target`.
   - Флаг `broadcast_if_no_target` определяет, будет ли действие транслироваться через доступные отношения агента, если цель действия не найдена.

2. **Добавление отношений между агентами**:
   - Используйте метод `add_relation` для установления связи между двумя агентами.
   - Укажите агента 1, агента 2 и имя отношения (например, "друг", "коллега").
   - Если агенты еще не добавлены в сеть, они будут добавлены автоматически.

3. **Обновление контекстов агентов**:
   - Вызовите метод `_update_agents_contexts`, чтобы обновить наблюдения агентов на основе текущего состояния сети.
   - Этот метод делает агентов доступными друг для друга в зависимости от установленных отношений.

4. **Выполнение шага симуляции**:
   - Вызовите метод `_step`, чтобы выполнить один шаг симуляции в социальной сети.
   - Сначала обновляются контексты агентов, а затем выполняется основной шаг симуляции, унаследованный от `TinyWorld`.

5. **Обработка действия `REACH_OUT`**:
   - Метод `_handle_reach_out` обрабатывает попытки агентов связаться друг с другом.
   - Связь будет успешной только в том случае, если целевой агент находится в тех же отношениях, что и исходный агент.

6. **Проверка наличия отношения между агентами**:
   - Используйте метод `is_in_relation_with`, чтобы проверить, связаны ли два агента.
   - Можно указать имя конкретного отношения или проверить наличие любой связи между агентами.

Пример использования
-------------------------

```python
from tinytroupe.environment.tiny_social_network import TinySocialNetwork
from tinytroupe.agent import TinyPerson

# Создание социальной сети
social_network = TinySocialNetwork(name="MySocialNetwork", broadcast_if_no_target=True)

# Создание агентов
agent_1 = TinyPerson(name="Alice")
agent_2 = TinyPerson(name="Bob")
agent_3 = TinyPerson(name="Charlie")

# Добавление отношений между агентами
social_network.add_relation(agent_1, agent_2, name="friends")
social_network.add_relation(agent_2, agent_3, name="colleagues")

# Проверка, находятся ли агенты в отношениях
print(f"Alice and Bob are friends: {social_network.is_in_relation_with(agent_1, agent_2, relation_name='friends')}")
print(f"Alice and Charlie are friends: {social_network.is_in_relation_with(agent_1, agent_3, relation_name='friends')}")
print(f"Bob and Charlie are colleagues: {social_network.is_in_relation_with(agent_2, agent_3, relation_name='colleagues')}")

# Обновление контекстов агентов
social_network._update_agents_contexts()

# Попытка агента связаться с другим агентом
social_network._handle_reach_out(source_agent=agent_1, content="Hello, Bob!", target="Bob")
social_network._handle_reach_out(source_agent=agent_1, content="Hello, Charlie!", target="Charlie")