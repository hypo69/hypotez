# Модуль тестов `test_factory.py`

## Обзор

Этот модуль содержит юнит-тесты для модуля `tinytroupe.factory`, который отвечает за создание персонажей в системе.

## Подробнее

Тесты проверяют, что фабрика персонажей создает корректные экземпляры персонажей с заданными спецификациями. 

## Функции

### `test_generate_person(setup)`

**Назначение**: Тестирование функции `generate_person()` фабрики персонажей.

**Параметры**:

- `setup`: Фикстура для настройки окружения (не определена в предоставленном коде).

**Как работает функция**:

1. Создает спецификацию персонажа `banker_spec`.
2. Создает фабрику персонажей `banker_factory` с заданной спецификацией.
3. Использует фабрику для создания экземпляра персонажа `banker`.
4. Извлекает краткое описание персонажа `minibio`.
5. Используя `proposition_holds`, проверяет, что `minibio` является подходящим кратким описанием для человека, работающего в банковской сфере.

**Примеры**:

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
    banker_spec ='''
    A vice-president of one of the largest brazillian banks. Has a degree in engineering and an MBA in finance. 
    Is facing a lot of pressure from the board of directors to fight off the competition from the fintechs.    
    '''

    banker_factory = TinyPersonFactory(banker_spec)

    banker = banker_factory.generate_person()

    minibio = banker.minibio()

    assert proposition_holds(f"The following is an acceptable short description for someone working in banking: '{minibio}'"), f"Proposition is false according to the LLM."