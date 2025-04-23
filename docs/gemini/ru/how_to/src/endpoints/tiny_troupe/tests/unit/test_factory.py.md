### Как использовать блок кода TinyPersonFactory для генерации персонажей
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует, как использовать класс `TinyPersonFactory` для генерации описания персонажа на основе заданной спецификации. В данном случае, генерируется описание банкира на основе предоставленного текста.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются классы и функции из `tinytroupe` и `testing_utils`.
2. **Определение спецификации**: Определяется текстовая спецификация для банкира (`banker_spec`), включающая его образование, опыт и текущую ситуацию.
3. **Создание фабрики персонажей**: Создается экземпляр `TinyPersonFactory` с использованием спецификации банкира.
4. **Генерация персонажа**: Вызывается метод `generate_person()` для создания объекта персонажа (`banker`).
5. **Получение мини-биографии**: Вызывается метод `minibio()` для получения краткого описания персонажа.
6. **Проверка соответствия**: Используется функция `proposition_holds()` для проверки, соответствует ли сгенерированная мини-биография ожиданиям.

Пример использования
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
    # Определяем спецификацию для банкира
    banker_spec = """
    A vice-president of one of the largest brazillian banks. Has a degree in engineering and an MBA in finance. 
    Is facing a lot of pressure from the board of directors to fight off the competition from the fintechs.    
    """

    # Создаем фабрику персонажей на основе спецификации
    banker_factory = TinyPersonFactory(banker_spec)

    # Генерируем персонажа
    banker = banker_factory.generate_person()

    # Получаем мини-биографию персонажа
    minibio = banker.minibio()

    # Проверяем, соответствует ли мини-биография ожиданиям
    assert proposition_holds(f"The following is an acceptable short description for someone working in banking: '{minibio}'"), f"Proposition is false according to the LLM."
```