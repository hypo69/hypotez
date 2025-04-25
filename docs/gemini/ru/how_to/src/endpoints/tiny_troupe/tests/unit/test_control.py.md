## Как использовать модуль `control` для управления симуляцией в `tinytroupe`

=========================================================================================

### Описание

Модуль `control` предоставляет функции для управления симуляцией TinyPerson, TinyWorld и TinyPersonFactory.
Он позволяет:

- Начать (begin) и завершить (end) симуляцию
- Создать контрольную точку (checkpoint) для сохранения состояния симуляции
- Сбросить (reset) текущую симуляцию

### Шаги выполнения

1. **Начать симуляцию (begin):**
    - Используйте функцию `control.begin(filename)` для запуска новой симуляции.
    - Передайте имя файла для сохранения состояния симуляции. 
2. **Создать контрольную точку (checkpoint):**
    - Вызовите функцию `control.checkpoint()`, чтобы сохранить текущее состояние симуляции в файл. 
    - Эта функция запишет состояние всех агентов, мира, фабрики персон и т. д., чтобы возобновить симуляцию с этого места. 
3. **Завершить симуляцию (end):**
    - Используйте функцию `control.end()`, чтобы остановить текущую симуляцию. 

4. **Сбросить симуляцию (reset):**
    - Вызовите `control.reset()`, чтобы удалить информацию о текущей симуляции. 

### Пример использования

```python
from tinytroupe.control import Simulation, control
from tinytroupe.examples import create_oscar_the_architect, create_lisa_the_data_scientist
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson, TinyToolUse

# Начинаем симуляцию и сохраняем ее состояние в файл "my_simulation.cache.json"
control.begin("my_simulation.cache.json")

# Создаем мир с двумя агентами
world = TinyWorld("Test World", [create_oscar_the_architect(), create_lisa_the_data_scientist()])

# Выполняем симуляцию в течение 2 шагов
world.run(2)

# Создаем контрольную точку для сохранения состояния
control.checkpoint()

# Продолжаем симуляцию еще на 3 шага
world.run(3)

# Завершаем симуляцию
control.end()

# Сбрасываем информацию о текущей симуляции
control.reset()

```