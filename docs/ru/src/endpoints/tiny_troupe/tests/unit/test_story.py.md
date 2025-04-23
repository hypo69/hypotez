# Документация для модуля `test_story.py`

## Обзор

Модуль `test_story.py` содержит набор юнит-тестов для проверки функциональности класса `TinyStory`, который отвечает за генерацию и продолжение историй на основе заданного контекста и требований. Тесты проверяют, насколько правдоподобно и логично LLM (Large Language Model) генерирует начало и продолжение историй с учетом заданных параметров.

## Подробней

Этот модуль предназначен для тестирования основных функций класса `TinyStory`, включая генерацию начала истории (`start_story`) и продолжение истории (`continue_story`). Он использует библиотеку `pytest` для организации тестов и включает в себя вспомогательные функции для проверки правдоподобности сгенерированного текста. Расположение файла в проекте указывает на его роль в проверке функциональности endpoint'а `tinytroupe`.

## Функции

### `test_story_start`

```python
def test_story_start(setup, focus_group_world):
    """
    Тест проверяет генерацию начала истории классом `TinyStory` на основе заданного мира (`world`).

    Args:
        setup: Фикстура pytest для настройки тестовой среды.
        focus_group_world: Фикстура, предоставляющая объект мира для тестирования.

    Returns:
        None

    Raises:
        AssertionError: Если сгенерированное начало истории не является правдоподобным, согласно LLM.

    
    - Функция извлекает объект мира из фикстуры `focus_group_world`.
    - Создает экземпляр класса `TinyStory`, передавая в него объект мира.
    - Вызывает метод `start_story()` для генерации начала истории.
    - Выводит сгенерированное начало истории в консоль.
    - Проверяет, является ли сгенерированное начало истории правдоподобным, используя функцию `proposition_holds()`.
    - Если проверка не проходит, вызывается исключение `AssertionError`.

    Примеры:
    ```python
    # Пример вызова функции в тестовом окружении
    test_story_start(setup_fixture, world_fixture)
    ```
    """
    world = focus_group_world

    story = TinyStory(world)

    start = story.start_story()

    print("Story start: ", start)

    assert proposition_holds(f"The following could plausibly be the start of a story involving people named either Lisa, Marcos or Oscar: \'{start}\'"), f"Proposition is false according to the LLM."
```

### `test_story_start_2`

```python
def test_story_start_2(setup, focus_group_world):
    """
    Тест проверяет генерацию начала истории с дополнительными требованиями к сюжету (например, "Start a story which is extremely crazy and out of this world.").

    Args:
        setup: Фикстура pytest для настройки тестовой среды.
        focus_group_world: Фикстура, предоставляющая объект мира для тестирования.

    Returns:
        None

    Raises:
        AssertionError: Если сгенерированное начало истории не соответствует заданным требованиям или не является правдоподобным, согласно LLM.

    
    - Функция извлекает объект мира из фикстуры `focus_group_world`.
    - Создает экземпляр класса `TinyStory`, передавая в него объект мира.
    - Вызывает метод `start_story()` с заданными требованиями для генерации начала истории.
    - Выводит сгенерированное начало истории в консоль.
    - Проверяет, соответствует ли сгенерированное начало истории заданным требованиям и является ли оно правдоподобным, используя функцию `proposition_holds()`.
    - Если проверка не проходит, вызывается исключение `AssertionError`.

    Примеры:
    ```python
    # Пример вызова функции в тестовом окружении
    test_story_start_2(setup_fixture, world_fixture)
    ```
    """
    world = focus_group_world

    story = TinyStory(world)

    start = story.start_story(requirements="Start a story which is extremely crazy and out of this world.")

    print("Story start: ", start)

    assert proposition_holds(f"The following could plausibly be the start of a very crazy story involving people named either Lisa, Marcos or Oscar: \'{start}\'"), f"Proposition is false according to the LLM."
```

### `test_story_continuation`

```python
def test_story_continuation(setup, focus_group_world):
    """
    Тест проверяет генерацию продолжения истории на основе заданного начала истории и текущего состояния мира.

    Args:
        setup: Фикстура pytest для настройки тестовой среды.
        focus_group_world: Фикстура, предоставляющая объект мира для тестирования.

    Returns:
        None

    Raises:
        AssertionError: Если сгенерированное продолжение истории не является логичным продолжением заданного начала или не является правдоподобным, согласно LLM.

    
    - Функция извлекает объект мира из фикстуры `focus_group_world`.
    - Определяет начало истории (`story_beginning`) в виде многострочной строки.
    - Транслирует начало истории в мир, используя метод `world.broadcast()`.
    - Запускает мир на несколько шагов, чтобы обновить его состояние.
    - Создает экземпляр класса `TinyStory`, передавая в него объект мира.
    - Вызывает метод `continue_story()` для генерации продолжения истории.
    - Выводит сгенерированное продолжение истории в консоль.
    - Проверяет, является ли сгенерированное продолжение истории логичным продолжением заданного начала, используя функцию `proposition_holds()`.
    - Если проверка не проходит, вызывается исключение `AssertionError`.

    Примеры:
    ```python
    # Пример вызова функции в тестовом окружении
    test_story_continuation(setup_fixture, world_fixture)
    ```
    """
    world = focus_group_world

    story_beginning = \
          """
            You were vacationing in the beautiful city of Rio de Janeiro, Brazil. You were walking down the beach when
            the most unexpected thing happened: an Alien spaceship landed right in front of you. The door opened and a
            friendly Alien stepped out. The Alien introduced itself as Zog, and explained that it was on a mission to
            learn more about Earth\'s cultures. You were intrigued by this encounter and decided to help Zog in its mission.
          """

    world.broadcast(story_beginning)
    
    world.run(2)

    story = TinyStory(world)

    continuation = story.continue_story()

    print("Story continuation: ", continuation)

    assert proposition_holds(f"The following two text blocks could belong to the same story: \\n BLOCK 1: \'{story_beginning}\' and \\n BLOCK 2: \'{continuation}\'"), f"Proposition is false according to the LLM."