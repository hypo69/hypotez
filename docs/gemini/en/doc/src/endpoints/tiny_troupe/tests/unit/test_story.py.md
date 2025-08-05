# Тесты для класса `TinyStory`

## Обзор

Этот модуль содержит набор юнит-тестов для класса `TinyStory`, который отвечает за генерацию и продолжение историй в проекте `tinytroupe`. 

## Тесты

### `test_story_start`

**Цель**: Проверить, что `TinyStory.start_story()` генерирует правдоподобное начало истории.

**Параметры**: 

- `setup`: Фикстура, устанавливающая окружение для тестов.
- `focus_group_world`: Фикстура, создающая мир с персонажами `Lisa`, `Marcos` и `Oscar`.

**Возвращает**: 

- None

**Как работает**:

1. Тест создает экземпляр `TinyStory` с использованием мира из `focus_group_world`.
2. Вызывает `TinyStory.start_story()` для получения начала истории.
3. Проверяет, что полученное начало истории соответствует предложению, используя функцию `proposition_holds` и LLM (Large Language Model).

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

**Цель**: Проверить, что `TinyStory.start_story()` может генерировать начало истории с заданными требованиями.

**Параметры**: 

- `setup`: Фикстура, устанавливающая окружение для тестов.
- `focus_group_world`: Фикстура, создающая мир с персонажами `Lisa`, `Marcos` и `Oscar`.

**Возвращает**: 

- None

**Как работает**:

1. Тест создает экземпляр `TinyStory` с использованием мира из `focus_group_world`.
2. Вызывает `TinyStory.start_story()` с заданными требованиями (`requirements="Start a story which is extremely crazy and out of this world."`).
3. Проверяет, что полученное начало истории соответствует предложению, используя функцию `proposition_holds` и LLM (Large Language Model).

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

**Цель**: Проверить, что `TinyStory.continue_story()` генерирует правдоподобное продолжение истории, начатой в `story_beginning`.

**Параметры**: 

- `setup`: Фикстура, устанавливающая окружение для тестов.
- `focus_group_world`: Фикстура, создающая мир с персонажами `Lisa`, `Marcos` и `Oscar`.

**Возвращает**: 

- None

**Как работает**:

1. Тест создает экземпляр `TinyStory` с использованием мира из `focus_group_world`.
2. Устанавливает начало истории `story_beginning` в мире.
3. Запускает мир на 2 шага, используя `world.run(2)`, чтобы добавить контекст в историю.
4. Вызывает `TinyStory.continue_story()` для получения продолжения истории.
5. Проверяет, что продолжение истории соответствует началу истории `story_beginning`, используя функцию `proposition_holds` и LLM (Large Language Model).

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
```

## Детали

- Тесты используют функции `proposition_holds` и `setup` из `testing_utils`, которые, скорее всего, содержат логику для взаимодействия с LLM и настройки тестового окружения.
- Тесты проверяют, что `TinyStory` генерирует правдоподобные истории, основываясь на контексте мира и заданных требованиях.
- Тесты используют `assert` для проверки ожидаемого поведения функции `TinyStory.start_story()` и `TinyStory.continue_story()`.

## Дополнительная информация

- Необходимо проанализировать код `testing_utils`, чтобы получить более полное представление о том, как работают функции `proposition_holds` и `setup`.
- Необходимо проанализировать код `TinyStory` и `world`, чтобы понять, как происходит генерация и продолжение историй.