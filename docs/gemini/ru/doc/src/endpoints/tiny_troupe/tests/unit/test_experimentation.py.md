# Модуль тестирования экспериментов

## Обзор

Этот модуль содержит набор тестов для проверки функциональности системы экспериментирования, включая A/B-тестирование и проверку предложений с использованием `TinyPerson` и `TinyWorld`. Он включает в себя тесты для рандомизации, дерандомизации и проверки истинности/ложности предложений на основе действий и высказываний персонажей.

## Подробнее

Модуль использует `pytest` для организации тестов и включает в себя функции для создания тестовых персонажей (например, `create_oscar_the_architect`, `create_lisa_the_data_scientist`) и миров (`focus_group_world`). Тесты охватывают различные аспекты экспериментирования, такие как правильная рандомизация вариантов, дерандомизация для определения исходных вариантов и проверка предложений на основе поведения персонажей в заданных сценариях.

## Классы

### `ABRandomizer`

**Описание**: Класс для проведения A/B-тестирования путем рандомизации и дерандомизации вариантов.

**Атрибуты**:
- `choices (List[Tuple[int, int]])`: Список кортежей, определяющих порядок вариантов для каждой итерации.
- `passtrough_name (Optional[List[str]])`: Список имен, которые всегда возвращаются без рандомизации.

**Методы**:
- `randomize(index: int, option1: str, option2: str) -> Tuple[str, str]`: Рандомизирует порядок двух вариантов на основе заданного индекса.
- `derandomize(index: int, a: str, b: str) -> Tuple[str, str]`: Дерандомизирует порядок двух вариантов на основе заданного индекса и текущего порядка.
- `derandomize_name(index: int, name: str) -> str`: Дерандомизирует имя варианта на основе заданного индекса.

### `Proposition`

**Описание**: Класс для представления предложений, которые могут быть проверены на основе действий и высказываний целевых объектов (например, `TinyPerson`, `TinyWorld`).

**Атрибуты**:
- `target (Any)`: Целевой объект, на котором проверяется предложение.
- `claim (str)`: Утверждение, которое необходимо проверить.
- `last_n (Optional[int])`: Количество последних действий/сообщений для проверки.
- `justification (List[str])`: Список строк, обосновывающих истинность предложения.
- `confidence (float)`: Уверенность в истинности предложения (от 0.0 до 1.0).

**Методы**:
- `check() -> bool`: Проверяет, является ли предложение истинным для заданного целевого объекта.

## Функции

### `test_randomize`

**Назначение**: Тест проверяет правильность рандомизации вариантов с использованием класса `ABRandomizer`.

**Параметры**:
- Нет параметров.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `ABRandomizer`.
- Выполняет цикл 20 раз для проверки рандомизации.
- Для каждой итерации рандомизирует два варианта "option1" и "option2".
- Проверяет, что порядок вариантов соответствует списку `choices` в `ABRandomizer`.
- Если порядок не соответствует, вызывает исключение.

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

**Назначение**: Тест проверяет правильность дерандомизации вариантов с использованием класса `ABRandomizer`.

**Параметры**:
- Нет параметров.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `ABRandomizer`.
- Выполняет цикл 20 раз для проверки дерандомизации.
- Для каждой итерации рандомизирует два варианта "option1" и "option2", затем дерандомизирует их.
- Проверяет, что дерандомизированный порядок соответствует исходному порядку вариантов.

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

**Назначение**: Тест проверяет правильность дерандомизации имени варианта с использованием класса `ABRandomizer`.

**Параметры**:
- Нет параметров.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `ABRandomizer`.
- Выполняет цикл 20 раз для проверки дерандомизации имени.
- Для каждой итерации рандомизирует два варианта "cats" и "dogs", затем дерандомизирует имя "A".
- Проверяет, что дерандомизированное имя соответствует "control" или "treatment" в зависимости от порядка вариантов и выбора пользователя.
- Если порядок не соответствует, вызывает исключение.

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

**Назначение**: Тест проверяет, что имена из списка `passtrough_name` возвращаются без изменений.

**Параметры**:
- Нет параметров.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `ABRandomizer` с `passtrough_name=["option3"]`.
- Рандомизирует два варианта "option1" и "option2".
- Дерандомизирует имя "option3".
- Проверяет, что возвращаемое имя соответствует "option3".

**Примеры**:
```python
def test_passtrough_name():
    randomizer = ABRandomizer(passtrough_name=["option3"])
    a, b = randomizer.randomize(0, "option1", "option2")
    real_name = randomizer.derandomize_name(0, "option3")

    assert real_name == "option3"
```

### `test_proposition_with_tinyperson`

**Назначение**: Тест проверяет, что предложения правильно оцениваются для `TinyPerson`.

**Параметры**:
- `setup`: Фикстура pytest для настройки тестовой среды.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `TinyPerson` с использованием `create_oscar_the_architect()`.
- Заставляет персонажа высказаться о предпочтениях в путешествиях.
- Создает два предложения: одно истинное и одно ложное.
- Проверяет, что истинное предложение оценивается как `True`, а ложное - как `False`.

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

**Назначение**: Тест проверяет, что предложения правильно оцениваются для `TinyPerson` в разные моменты времени.

**Параметры**:
- `setup`: Фикстура pytest для настройки тестовой среды.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `TinyPerson` с использованием `create_oscar_the_architect()`.
- Заставляет персонажа высказаться о предпочтениях в путешествиях.
- Создает предложение, которое проверяет, говорит ли персонаж о своих предпочтениях в путешествиях в последние 3 действия.
- Проверяет, что предложение оценивается как `True`.
- Заставляет персонажа сменить тему разговора.
- Проверяет, что то же самое предложение теперь оценивается как `False`.

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

    oscar.listen_and_act("Now let\'s change subjects. What do you work with?")
    assert proposition.check() == False # the _same_ proposition is no longer true, because Oscar changed subjects
```

### `test_proposition_with_tinyworld`

**Назначение**: Тест проверяет, что предложения правильно оцениваются для `TinyWorld`.

**Параметры**:
- `setup`: Фикстура pytest для настройки тестовой среды.
- `focus_group_world`: Фикстура pytest для создания тестового мира.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `TinyWorld` с использованием `focus_group_world`.
- Заставляет мир транслировать сообщение об обсуждении преимуществ собак и кошек.
- Запускает мир на 2 шага.
- Создает два предложения: одно истинное и одно ложное.
- Проверяет, что истинное предложение оценивается как `True`, а ложное - как `False`.

**Примеры**:
```python
def test_proposition_with_tinyworld(setup, focus_group_world):
    world = focus_group_world
    world.broadcast("Discuss the comparative advantages of dogs and cats.")
    world.run(2)

    true_proposition = Proposition(target=world, claim="There\'s a discussion about dogs and cats.")
    assert true_proposition.check() == True

    false_proposition = Proposition(target=world, claim="There\'s a discussion about whether porto wine vs french wine.")
    assert false_proposition.check() == False
```

### `test_proposition_with_multiple_targets`

**Назначение**: Тест проверяет, что предложения правильно оцениваются для нескольких целевых объектов.

**Параметры**:
- `setup`: Фикстура pytest для настройки тестовой среды.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает два экземпляра класса `TinyPerson` с использованием `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
- Заставляет каждого персонажа высказаться о разных темах.
- Создает два предложения: одно истинное и одно ложное.
- Проверяет, что истинное предложение оценивается как `True`, а ложное - как `False`.

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

**Назначение**: Тест проверяет, что метод класса `check_proposition` работает правильно.

**Параметры**:
- `setup`: Фикстура pytest для настройки тестовой среды.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:
- Создает экземпляр класса `TinyPerson` с использованием `create_oscar_the_architect()`.
- Заставляет персонажа высказаться о предпочтениях в путешествиях.
- Использует метод класса `check_proposition` для проверки двух предложений: одного истинного и одного ложного.
- Проверяет, что истинное предложение оценивается как `True`, а ложное - как `False`.

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