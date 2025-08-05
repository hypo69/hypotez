## Как использовать Intervention
=========================================================================================

Описание
-------------------------
Intervention - это класс, который описывает вмешательство в симуляцию. Вмешательство  - это изменение, которое может быть произведено в TinyWorld или TinyPerson. Вмешательство  - это  комбинация из preconditions (предварительных условий) и эффектов.  

Шаги выполнения
-------------------------
1. Создайте объект Intervention с помощью конструктора. 
2. Установите преconditions с помощью методов  set_textual_precondition или  set_functional_precondition.
3. Установите эффект с помощью метода set_effect.
4. Выполните Intervention с помощью метода `execute` или вызвав Intervention как функцию.


Пример использования
-------------------------

```python
from tinytroupe.experimentation import Proposition
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson
from tinytroupe.steering.intervention import Intervention


# Создайте мир с одним агентом
world = TinyWorld()
person = TinyPerson(world)

# Создайте Intervention, которая заставляет агента говорить "Привет!"
intervention = Intervention(targets=person)
intervention.set_textual_precondition("Агент должен быть счастлив")
intervention.set_effect(lambda targets: targets.say("Привет!"))


# Проверьте Intervention
intervention.execute()


# Вывод
# "Агент сказал: 'Привет!'"
```

В данном примере Intervention будет выполнена, только если агент счастлив.