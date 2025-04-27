# Модуль тестирования `experimentation`

## Обзор

Этот модуль содержит юнит-тесты для модуля `experimentation`. В нем проверяется работа классов `ABRandomizer` и `Proposition`, а также функции `check_proposition`. 

## Подробности

Тесты проверяют корректность работы классов и функций, а также правильность их взаимодействия.

## Тесты

### `test_randomize`

**Назначение**: Тестирует функцию `randomize` класса `ABRandomizer`.

**Как работает**: 
- Создает экземпляр класса `ABRandomizer`.
- Проверяет, что функция `randomize` возвращает корректные варианты ("option1", "option2")  в зависимости от результатов рандомизации (0, 1) или (1, 0).
- Проверяет, что функция `randomize` возвращает правильное значение в случае, если нет рандомизации.

**Примеры**:
```python
def test_randomize():
    randomizer = ABRandomizer()
    # run multiple times to make sure the randomization is properly tested
    for i in range(20):
        a, b = randomizer.randomize(i, "option1", "option2")

        if randomizer.choices[i] == (0, 1):
            assert (a, b) == ("option1", "option2")
        elif randomizer.choices[i] == (1, 0):
            assert (a, b) == ("option2", "option1")
        else:
            raise Exception(f"No randomization found for item {i}")
```

### `test_derandomize`

**Назначение**: Тестирует функцию `derandomize` класса `ABRandomizer`.

**Как работает**:
- Создает экземпляр класса `ABRandomizer`.
- Вызывает функцию `randomize` для получения рандомизированных вариантов.
- Проверяет, что функция `derandomize` возвращает исходные варианты ("option1", "option2").

**Примеры**:
```python
def test_derandomize():
    randomizer = ABRandomizer()

    # run multiple times to make sure the randomization is properly tested
    for i in range(20):
        a, b = randomizer.randomize(i, "option1", "option2")
        c, d = randomizer.derandomize(i, a, b)

        assert (c, d) == ("option1", "option2")
```

### `test_derandomize_name`

**Назначение**: Тестирует функцию `derandomize_name` класса `ABRandomizer`.

**Как работает**:
- Создает экземпляр класса `ABRandomizer`.
- Вызывает функцию `randomize` для получения рандомизированных вариантов.
- Вызывает функцию `derandomize_name` для получения исходного имени ("control" или "treatment") в зависимости от результатов рандомизации и выбранного варианта.

**Примеры**:
```python
def test_derandomize_name():
    randomizer = ABRandomizer()

    for i in range(20):
        a, b = randomizer.randomize(i, "cats", "dogs")
        real_name = randomizer.derandomize_name(i, "A")

        if randomizer.choices[i] == (0, 1):
            # "Favorite pet? A: cats, B: dogs"
            # user selects "A"
            # user selected the control group 
            assert real_name == "control"
        elif randomizer.choices[i] == (1, 0):
            # "Favorite pet? A: dogs, B: cats"
            # user selects "A"
            # user selected the treatment group
            assert real_name == "treatment"
        else:
            raise Exception(f"No randomization found for item {i}")
```

### `test_passtrough_name`

**Назначение**: Тестирует работу функции `derandomize_name` в случае, если имя не участвует в рандомизации.

**Как работает**:
- Создает экземпляр класса `ABRandomizer` с параметром `passtrough_name`  
- Вызывает функцию `randomize` для получения рандомизированных вариантов.
- Проверяет, что функция `derandomize_name` возвращает исходное имя, если оно не участвует в рандомизации.

**Примеры**:
```python
def test_passtrough_name():
    randomizer = ABRandomizer(passtrough_name=["option3"])
    a, b = randomizer.randomize(0, "option1", "option2")
    real_name = randomizer.derandomize_name(0, "option3")

    assert real_name == "option3"
```

### `test_proposition_with_tinyperson`

**Назначение**: Тестирует работу класса `Proposition` с использованием `TinyPerson` объекта.

**Как работает**:
- Создает экземпляр `TinyPerson` объекта.
- Создает экземпляр `Proposition` объекта.
- Проверяет, что `Proposition` объект правильно определяет истинность и ложность утверждений.

**Примеры**:
```python
def test_proposition_with_tinyperson(setup):
    oscar = create_oscar_the_architect()
    oscar.listen_and_act("Tell me a bit about your travel preferences.")
    
    true_proposition = Proposition(target=oscar, claim="Oscar mentions his travel preferences.")
    assert true_proposition.check() == True

    false_proposition = Proposition(target=oscar, claim="Oscar writes a novel about how cats are better than dogs.")
    assert false_proposition.check() == False
```

### `test_proposition_with_tinyperson_at_multiple_points`

**Назначение**: Тестирует работу класса `Proposition` с использованием `TinyPerson` объекта в разных точках времени.

**Как работает**:
- Создает экземпляр `TinyPerson` объекта.
- Создает экземпляр `Proposition` объекта.
- Проверяет, что `Proposition` объект правильно определяет истинность и ложность утверждений в разные моменты времени.

**Примеры**:
```python
def test_proposition_with_tinyperson_at_multiple_points(setup):
    oscar = create_oscar_the_architect()
    oscar.listen_and_act("Tell me a bit about your travel preferences.")
    
    proposition = Proposition(target=oscar, 
                              claim="Oscar talks about his travel preferences",
                              last_n=3)
    assert proposition.check() == True

    print(proposition.justification)
    print(proposition.confidence)
    assert len(proposition.justification) > 0
    assert proposition.confidence >= 0.0

    oscar.listen_and_act("Now let's change subjects. What do you work with?")
    assert proposition.check() == False # the _same_ proposition is no longer true, because Oscar changed subjects
```

### `test_proposition_with_tinyworld`

**Назначение**: Тестирует работу класса `Proposition` с использованием `TinyWorld` объекта.

**Как работает**:
- Создает экземпляр `TinyWorld` объекта.
- Создает экземпляр `Proposition` объекта.
- Проверяет, что `Proposition` объект правильно определяет истинность и ложность утверждений в контексте `TinyWorld`.

**Примеры**:
```python
def test_proposition_with_tinyworld(setup, focus_group_world):
    world = focus_group_world
    world.broadcast("Discuss the comparative advantages of dogs and cats.")
    world.run(2)

    true_proposition = Proposition(target=world, claim="There's a discussion about dogs and cats.")
    assert true_proposition.check() == True

    false_proposition = Proposition(target=world, claim="There's a discussion about whether porto wine vs french wine.")
    assert false_proposition.check() == False
```

### `test_proposition_with_multiple_targets`

**Назначение**: Тестирует работу класса `Proposition` с несколькими объектами-целями.

**Как работает**:
- Создает экземпляры `TinyPerson` объектов.
- Создает экземпляр `Proposition` объекта, передавая список объектов-целей.
- Проверяет, что `Proposition` объект правильно определяет истинность и ложность утверждений, учитывая взаимодействие всех объектов.

**Примеры**:
```python
def test_proposition_with_multiple_targets(setup):
    oscar = create_oscar_the_architect()
    lisa = create_lisa_the_data_scientist()

    oscar.listen_and_act("Tell me a bit about your travel preferences.")
    lisa.listen_and_act("Tell me about your data science projects.")

    targets = [oscar, lisa]

    true_proposition = Proposition(target=targets, claim="Oscar mentions his travel preferences and Lisa discusses data science projects.")
    assert true_proposition.check() == True

    false_proposition = Proposition(target=targets, claim="Oscar writes a novel about how cats are better than dogs.")
    assert false_proposition.check() == False
```

### `test_proposition_class_method`

**Назначение**: Тестирует работу функции `check_proposition`.

**Как работает**:
- Создает экземпляр `TinyPerson` объекта.
- Проверяет, что функция `check_proposition` правильно определяет истинность и ложность утверждений, используя как экземпляр `Proposition` объекта, так и напрямую через функцию.

**Примеры**:
```python
def test_proposition_class_method(setup):
    oscar = create_oscar_the_architect()
    oscar.listen_and_act("Tell me a bit about your travel preferences.")
    
    # notice that now we are using the class method, as a convenience
    assert check_proposition(target=oscar, claim="Oscar mentions his travel preferences.") == True
    assert check_proposition(oscar, "Oscar mentions his travel preferences.") == True

    assert check_proposition(target=oscar, claim="Oscar writes a novel about how cats are better than dogs.") == False
    assert check_proposition(oscar, "Oscar writes a novel about how cats are better than dogs.") == False
```