### Как использовать класс `TinyWorld`
=========================================================================================

Описание
-------------------------
Класс `TinyWorld` предназначен для моделирования окружения, в котором взаимодействуют агенты (`TinyPerson`). Он управляет временем, агентами, событиями и взаимодействиями между ними.

Шаги выполнения
-------------------------
1. **Создание окружения**:
   - Создайте экземпляр класса `TinyWorld`, указав имя, список агентов, начальное время и другие параметры.

2. **Добавление агентов**:
   - Используйте метод `add_agents` или `add_agent` для добавления агентов в окружение.

3. **Запуск симуляции**:
   - Используйте методы `run`, `run_minutes`, `run_hours`, `run_days`, `run_weeks`, `run_months` или `run_years` для запуска симуляции на определенное количество шагов или времени.
   - Используйте методы `skip`, `skip_minutes`, `skip_hours`, `skip_days`, `skip_weeks`, `skip_months` или `skip_years` для пропуска симуляции на определенное количество шагов или времени.

4. **Взаимодействие агентов**:
   - Агенты могут взаимодействовать друг с другом через действия, которые обрабатываются методами `_handle_reach_out` и `_handle_talk`.
   - Используйте методы `broadcast`, `broadcast_thought`, `broadcast_internal_goal` и `broadcast_context_change` для отправки сообщений всем агентам в окружении.

5. **Управление событиями**:
   - Добавляйте события (interventions) в окружение с помощью метода `add_intervention`.

6. **Получение информации**:
   - Используйте методы `get_agent_by_name` и `get_environment_by_name` для получения информации об агентах и окружениях.

7. **Управление состоянием**:
   - Используйте методы `encode_complete_state` и `decode_complete_state` для сохранения и восстановления состояния окружения.

Пример использования
-------------------------

```python
from datetime import datetime, timedelta
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.tiny_person import TinyPerson

# 1. Создание агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")

# 2. Создание окружения
world = TinyWorld(
    name="MyTinyWorld",
    agents=[agent1, agent2],
    initial_datetime=datetime.now(),
)

# 3. Запуск симуляции на 5 шагов с интервалом в 1 минуту
world.run(steps=5, timedelta_per_step=timedelta(minutes=1))

# 4. Отправка сообщения от Alice к Bob
world._handle_talk(source_agent=agent1, content="Привет, Bob!", target="Bob")

# 5. Вывод истории взаимодействия агентов
world.pp_current_interactions()

# 6. Получение состояния окружения
state = world.encode_complete_state()

# 7. Восстановление состояния окружения
new_world = TinyWorld(name="NewWorld")
new_world.decode_complete_state(state)

print(f"Окружение: {world.name}")
print(f"Агенты: {[agent.name for agent in world.agents]}")