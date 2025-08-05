## Как использовать функцию `test_generate_person`

=========================================================================================

### Описание
-------------------------
Функция `test_generate_person` проверяет генерацию описания человека (минибиографии) с помощью фабрики персонажей `TinyPersonFactory`.  В  тесте создаётся описание вице-президента крупного бразильского банка, а затем проверяется, соответствует ли сгенерированное описание ожиданиям  с помощью модели  LLM.

### Шаги выполнения
-------------------------
1. Определяется описание (спецификация) вице-президента банка.
2. Создаётся фабрика персонажей `TinyPersonFactory` с использованием заданной спецификации.
3. Генерируется описание человека с помощью метода `generate_person` фабрики.
4. Вызывается метод `minibio` для получения краткого описания сгенерированного персонажа.
5. Используется функция `proposition_holds` для проверки, соответствует ли сгенерированное описание ожиданиям модели LLM.

### Пример использования
-------------------------

```python
import pytest
import os

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')


from tinytroupe.examples import create_oscar_the_architect
from tinytroupe.control import Simulation
import tinytroupe.control as control
from tinytroupe.factory import TinyPersonFactory

from testing_utils import *

def test_generate_person(setup):
    banker_spec = """
    A vice-president of one of the largest brazillian banks. Has a degree in engineering and an MBA in finance. 
    Is facing a lot of pressure from the board of directors to fight off the competition from the fintechs.    
    """

    banker_factory = TinyPersonFactory(banker_spec)

    banker = banker_factory.generate_person()

    minibio = banker.minibio()

    assert proposition_holds(f"The following is an acceptable short description for someone working in banking: '{minibio}'"), f"Proposition is false according to the LLM."
```