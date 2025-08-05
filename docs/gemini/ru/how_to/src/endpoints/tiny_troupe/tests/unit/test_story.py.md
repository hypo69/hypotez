## Как использовать TinyStory для генерации и продолжения историй
=========================================================================================

Описание
-------------------------
Этот фрагмент кода демонстрирует использование класса `TinyStory` из `tinytroupe.steering` для генерации начала истории и ее продолжения.

Шаги выполнения
-------------------------
1. **Инициализация TinyStory**: Создается объект `TinyStory` с использованием объекта `world` (представление мира, хранящего информацию об истории).
2. **Запуск генерации начала истории**: Вызов метода `start_story()` с опциональным параметром `requirements` генерирует начало истории.
3. **Проверка результата**:  Ассерты проверяют, удовлетворяет ли полученное начало истории заданным требованиям.
4. **Добавление начала истории в мир**: Начало истории добавляется в `world` с помощью метода `broadcast()`.
5. **Имитация прохождения времени**: Метод `run()` имитирует прохождение времени в мире, чтобы история могла развиваться.
6. **Запуск генерации продолжения**: Метод `continue_story()` генерирует продолжение истории, основанное на текущем состоянии `world`.
7. **Проверка результата**:  Ассерты проверяют,  соответствует ли продолжение истории предыдущему ее блоку.

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

    assert proposition_holds(f"The following could plausibly be the start of a story involving people named either Lisa, Marcos or Oscar: \'{start}\'"), f"Proposition is false according to the LLM."

def test_story_start_2(setup, focus_group_world):
    world = focus_group_world

    story = TinyStory(world)

    start = story.start_story(requirements="Start a story which is extremely crazy and out of this world.")

    print("Story start: ", start)

    assert proposition_holds(f"The following could plausibly be the start of a very crazy story involving people named either Lisa, Marcos or Oscar: \'{start}\'"), f"Proposition is false according to the LLM."

def test_story_continuation(setup, focus_group_world):
    world = focus_group_world

    story_beginning = \
          """
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

    assert proposition_holds(f"The following two text blocks could belong to the same story: \n BLOCK 1: \'{story_beginning}\' and \n BLOCK 2: \'{continuation}\'"), f"Proposition is false according to the LLM."
```

**Описание функций:**

- `start_story()`: Генерирует начало истории, принимая опциональные требования к ее содержанию.
- `continue_story()`: Генерирует продолжение истории, основываясь на текущем состоянии мира.
- `broadcast(story_beginning)`: Добавляет начало истории в мир, чтобы его можно было использовать для генерации продолжения.
- `run(2)`: Имитирует прохождение времени в мире. В данном случае продвигаем мир на два шага вперед.

**Использование в проекте:**

Этот код демонстрирует, как можно использовать `TinyStory` для создания и продолжения историй в проекте `hypotez`. Он показывает, как создавать объекты `TinyStory`, генерировать  и продолжать истории, а также проверять, соответствует ли сгенерированный текст заданным требованиям.