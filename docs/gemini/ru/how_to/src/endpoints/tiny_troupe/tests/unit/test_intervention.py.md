### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код демонстрирует, как использовать класс `Intervention` для изменения поведения персонажа (`Oscar`) в виртуальном мире (`TinyWorld`). Код создает персонажа, моделирует его состояние и действия, а затем применяет `Intervention` для изменения темы его разговора с грустной на радостную.

Шаги выполнения
-------------------------
1. **Создание персонажа:**
   - Функция `create_oscar_the_architect()` вызывается для создания экземпляра персонажа `Oscar`.

2. **Моделирование начального состояния и действия:**
   - `Oscar` "думает" о грустном событии и затем "действует" (вероятно, вербализует свои мысли).
   - Проверяется, что последние высказывания `Oscar` соответствуют теме грусти или несчастья с использованием `check_proposition`.

3. **Создание и настройка Intervention:**
   - Создается экземпляр класса `Intervention` для персонажа `Oscar`.
   - Устанавливается текстовое предусловие (`set_textual_precondition`), которое должно выполняться, чтобы `Intervention` сработало ("Oscar is not very happy.").
   - Устанавливается эффект (`set_effect`) - лямбда-функция, которая заставляет `Oscar` "думать" о чем-то радостном.

4. **Создание и запуск виртуального мира:**
   - Создается экземпляр класса `TinyWorld` с именем "Test World", включающий `Oscar` и созданный `Intervention`.
   - Мир запускается на 2 шага (`world.run(2)`), во время которых `Intervention` может сработать.

5. **Проверка конечного состояния:**
   - Проверяется, что последние высказывания `Oscar` соответствуют теме радости или счастья с использованием `check_proposition`.

Пример использования
-------------------------

```python
import pytest

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from testing_utils import *

from tinytroupe.steering import Intervention
from tinytroupe.experimentation import ABRandomizer
from tinytroupe.experimentation import Proposition, check_proposition
from tinytroupe.examples import create_oscar_the_architect, create_oscar_the_architect_2, create_lisa_the_data_scientist, create_lisa_the_data_scientist_2
from tinytroupe.environment import TinyWorld


def test_intervention_1():
    oscar = create_oscar_the_architect()

    oscar.think("I am terribly sad, as a dear friend has died. I'm going now to verbalize my sadness.")
    oscar.act()

    assert check_proposition(oscar, "Oscar is talking about something sad or unfortunate.", last_n=3)

    intervention = \
        Intervention(oscar)\
        .set_textual_precondition("Oscar is not very happy.")\
        .set_effect(lambda target: target.think("Enough sadness. I will now talk about something else that makes me happy."))
    
    world = TinyWorld("Test World", [oscar], interventions=[intervention])

    world.run(2)

    assert check_proposition(oscar, "Oscar is talking about something that brings joy or happiness to him.", last_n = 3)

    # TODO