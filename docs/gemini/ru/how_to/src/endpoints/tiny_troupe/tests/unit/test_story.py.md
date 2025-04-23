### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит тесты для проверки функциональности класса `TinyStory`, который отвечает за генерацию и продолжение историй на основе заданного мира (world). Тесты проверяют, насколько правдоподобно LLM генерирует начало и продолжение истории, учитывая заданные требования и контекст.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек и модулей**:
   - Импортируются библиотеки `pytest`, `logging`.
   - Настраивается логгер `tinytroupe`.
   - Добавляются пути к модулям `tinytroupe` и другим необходимым директориям.
   - Импортируется класс `TinyStory` из модуля `steering`.
   - Импортируются вспомогательные функции из модуля `testing_utils`.

2. **Функция `test_story_start`**:
   - Инициализируется мир (`world`) из `focus_group_world`.
   - Создается экземпляр класса `TinyStory` с переданным миром.
   - Вызывается метод `start_story()` для генерации начала истории.
   - Выводится сгенерированное начало истории в консоль.
   - Проверяется, что сгенерированное начало истории правдоподобно с использованием функции `proposition_holds`.

3. **Функция `test_story_start_2`**:
   - Аналогична `test_story_start`, но с добавлением требования к началу истории: "Start a story which is extremely crazy and out of this world."
   - Проверяется, что сгенерированное начало истории соответствует заданному требованию о "crazy story".

4. **Функция `test_story_continuation`**:
   - Инициализируется мир (`world`) из `focus_group_world`.
   - Определяется начало истории (`story_beginning`) в виде многострочной строки.
   - Начало истории транслируется в мир (`world.broadcast`).
   - Мир запускается на 2 шага (`world.run(2)`).
   - Создается экземпляр класса `TinyStory` с переданным миром.
   - Вызывается метод `continue_story()` для генерации продолжения истории.
   - Выводится сгенерированное продолжение истории в консоль.
   - Проверяется, что сгенерированное продолжение истории логически связано с началом истории с использованием функции `proposition_holds`.

Пример использования
-------------------------

```python
import pytest
import logging
logger = logging.getLogger("tinytroupe")

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from tinytroupe.steering import TinyStory
from testing_utils import *

def test_story_start(setup, focus_group_world):
    world = focus_group_world

    story = TinyStory(world)

    start = story.start_story()

    print("Story start: ", start)

    assert proposition_holds(f"The following could plausibly be the start of a story involving people named either Lisa, Marcos or Oscar: '{start}'"), f"Proposition is false according to the LLM."

def test_story_start_2(setup, focus_group_world):
    world = focus_group_world

    story = TinyStory(world)

    start = story.start_story(requirements="Start a story which is extremely crazy and out of this world.")

    print("Story start: ", start)

    assert proposition_holds(f"The following could plausibly be the start of a very crazy story involving people named either Lisa, Marcos or Oscar: '{start}'"), f"Proposition is false according to the LLM."

def test_story_continuation(setup, focus_group_world):
    world = focus_group_world

    story_beginning = """
        You were vacationing in the beautiful city of Rio de Janeiro, Brazil. You were walking down the beach when
        the most unexpected thing happened: an Alien spaceship landed right in front of you. The door opened and a
        friendly Alien stepped out. The Alien introduced itself as Zog, and explained that it was on a mission to
        learn more about Earth's cultures. You were intrigued by this encounter and decided to help Zog in its mission.
    """

    world.broadcast(story_beginning)
    
    world.run(2)

    story = TinyStory(world)

    continuation = story.continue_story()

    print("Story continuation: ", continuation)

    assert proposition_holds(f"The following two text blocks could belong to the same story: \n BLOCK 1: '{story_beginning}' and \n BLOCK 2: '{continuation}'"), f"Proposition is false according to the LLM."