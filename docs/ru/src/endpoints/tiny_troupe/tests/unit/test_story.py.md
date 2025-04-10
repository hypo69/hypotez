# Модуль тестирования TinyStory
## Обзор
Модуль `test_story.py` содержит юнит-тесты для проверки функциональности класса `TinyStory`, который отвечает за генерацию и продолжение историй на основе заданного мира (world) и персонажей. Тесты проверяют, насколько правдоподобно и логично строятся истории, а также соответствуют ли они заданным требованиям.

## Подробнее
Модуль содержит тесты для проверки начальной генерации истории и продолжения истории на основе заданного начала. В тестах используется библиотека `pytest` для организации и запуска тестов, а также вспомогательные функции для проверки правдоподобности сгенерированного текста с помощью языковой модели.

## Классы

### `TinyStory`
Класс предназначен для генерации и продолжения историй на основе заданного мира и персонажей.

**Принцип работы**:
Класс принимает объект `world`, содержащий информацию об окружении и персонажах. Методы класса используются для генерации начального фрагмента истории (`start_story`) и продолжения существующей истории (`continue_story`). Внутренне класс использует механизмы `world` для взаимодействия с языковой моделью и получения сгенерированных текстов.

**Методы**:
- `start_story()`: Генерирует начальный фрагмент истории.
- `continue_story()`: Продолжает существующую историю.

## Функции

### `test_story_start`

```python
def test_story_start(setup, focus_group_world):
    """Проверяет генерацию начального фрагмента истории.

    Args:
        setup: Фикстура pytest для настройки тестового окружения.
        focus_group_world: Объект `world`, содержащий информацию об окружении и персонажах.

    Returns:
        None

    Raises:
        AssertionError: Если сгенерированный текст неправдоподобен согласно языковой модели.

    """
```
**Назначение**:
Функция `test_story_start` проверяет, что класс `TinyStory` может успешно генерировать начальный фрагмент истории, который является правдоподобным и соответствует заданному миру.

**Как работает функция**:

1.  **Инициализация мира**: Получает объект `world` из аргумента `focus_group_world`.
2.  **Создание экземпляра `TinyStory`**: Создает экземпляр класса `TinyStory`, передавая в него объект `world`.
3.  **Генерация начала истории**: Вызывает метод `start_story()` для генерации начального фрагмента истории.
4.  **Вывод в консоль**: Выводит сгенерированный текст в консоль для отладки.
5.  **Проверка правдоподобности**: Использует функцию `proposition_holds` для проверки, что сгенерированный текст является правдоподобным началом истории с участием определенных персонажей (Lisa, Marcos, Oscar).
6.  **Вывод результата**: Если проверка не проходит, вызывает исключение `AssertionError` с сообщением об ошибке.

**Примеры**:

```python
def test_story_start(setup, focus_group_world):
    world = focus_group_world
    story = TinyStory(world)
    start = story.start_story()
    print("Story start: ", start)
    assert proposition_holds(f"The following could plausibly be the start of a story involving people named either Lisa, Marcos or Oscar: '{start}'"), f"Proposition is false according to the LLM."
```

### `test_story_start_2`

```python
def test_story_start_2(setup, focus_group_world):
    """Проверяет генерацию начального фрагмента истории с дополнительными требованиями.

    Args:
        setup: Фикстура pytest для настройки тестового окружения.
        focus_group_world: Объект `world`, содержащий информацию об окружении и персонажах.

    Returns:
        None

    Raises:
        AssertionError: Если сгенерированный текст неправдоподобен согласно языковой модели.

    """
```

**Назначение**:
Функция `test_story_start_2` проверяет, что класс `TinyStory` может успешно генерировать начальный фрагмент истории, который является правдоподобным, соответствует заданному миру и удовлетворяет дополнительным требованиям (в данном случае, история должна быть "extremely crazy and out of this world").

**Как работает функция**:

1.  **Инициализация мира**: Получает объект `world` из аргумента `focus_group_world`.
2.  **Создание экземпляра `TinyStory`**: Создает экземпляр класса `TinyStory`, передавая в него объект `world`.
3.  **Генерация начала истории с требованиями**: Вызывает метод `start_story()`, передавая в аргумент `requirements` строку с дополнительными требованиями к истории.
4.  **Вывод в консоль**: Выводит сгенерированный текст в консоль для отладки.
5.  **Проверка правдоподобности**: Использует функцию `proposition_holds` для проверки, что сгенерированный текст является правдоподобным началом "очень безумной" истории с участием определенных персонажей (Lisa, Marcos, Oscar).
6.  **Вывод результата**: Если проверка не проходит, вызывает исключение `AssertionError` с сообщением об ошибке.

**Примеры**:

```python
def test_story_start_2(setup, focus_group_world):
    world = focus_group_world
    story = TinyStory(world)
    start = story.start_story(requirements="Start a story which is extremely crazy and out of this world.")
    print("Story start: ", start)
    assert proposition_holds(f"The following could plausibly be the start of a very crazy story involving people named either Lisa, Marcos or Oscar: '{start}'"), f"Proposition is false according to the LLM."
```

### `test_story_continuation`

```python
def test_story_continuation(setup, focus_group_world):
    """Проверяет генерацию продолжения истории на основе заданного начала.

    Args:
        setup: Фикстура pytest для настройки тестового окружения.
        focus_group_world: Объект `world`, содержащий информацию об окружении и персонажей.

    Returns:
        None

    Raises:
        AssertionError: Если сгенерированное продолжение не связано с заданным началом истории.

    """
```

**Назначение**:
Функция `test_story_continuation` проверяет, что класс `TinyStory` может успешно генерировать продолжение истории, которое логически связано с заданным началом.

**Как работает функция**:

1.  **Инициализация мира**: Получает объект `world` из аргумента `focus_group_world`.
2.  **Задание начала истории**: Определяет строку `story_beginning`, содержащую начальный фрагмент истории.
3.  **Трансляция начала истории**: Вызывает метод `world.broadcast`, передавая в него начало истории, чтобы мир знал о текущем состоянии истории.
4.  **Запуск мира**: Вызывает метод `world.run(2)`, чтобы мир обработал начало истории и подготовился к генерации продолжения.
5.  **Создание экземпляра `TinyStory`**: Создает экземпляр класса `TinyStory`, передавая в него объект `world`.
6.  **Генерация продолжения истории**: Вызывает метод `continue_story()` для генерации продолжения истории.
7.  **Вывод в консоль**: Выводит сгенерированный текст в консоль для отладки.
8.  **Проверка связности**: Использует функцию `proposition_holds` для проверки, что начало истории и продолжение истории могут принадлежать одной и той же истории.
9.  **Вывод результата**: Если проверка не проходит, вызывает исключение `AssertionError` с сообщением об ошибке.

**Примеры**:

```python
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