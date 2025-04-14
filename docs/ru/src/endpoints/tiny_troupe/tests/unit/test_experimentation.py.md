# Модуль тестирования экспериментов

## Обзор

Этот модуль содержит юнит-тесты для проверки функциональности экспериментирования, включая A/B-тестирование и проверку утверждений (proposition) о поведении TinyPerson и TinyWorld. Он проверяет правильность рандомизации, дерандомизации и логики утверждений.

## Подробнее

Этот модуль тестирует различные аспекты экспериментирования в проекте `hypotez`. В частности, он проверяет, как A/B-тесты правильно рандомизируют и дерандомизируют варианты, а также как проверяются утверждения о поведении виртуальных персонажей (TinyPerson) и виртуального мира (TinyWorld).

## Классы

В этом файле нет классов, только функции тестирования.

## Функции

### `test_randomize`

```python
def test_randomize():
    """
    Тестирует корректность рандомизации A/B-тестов.

    Проверяет, что функция `randomize` класса `ABRandomizer` правильно выбирает один из двух вариантов случайным образом.
    """
```

**Как работает функция**:

1.  Создается экземпляр класса `ABRandomizer`.
2.  В цикле 20 раз вызывается метод `randomize` с двумя вариантами ("option1" и "option2").
3.  Для каждой итерации проверяется, какой вариант был выбран, и сравнивается с ожидаемым результатом на основе атрибута `choices` объекта `randomizer`.
4.  Если рандомизация не найдена, выбрасывается исключение.

**Примеры**:

```python
randomizer = ABRandomizer()
a, b = randomizer.randomize(0, "option1", "option2")
# Результат: a и b будут "option1" и "option2" в случайном порядке.
```

### `test_derandomize`

```python
def test_derandomize():
    """
    Тестирует корректность дерандомизации A/B-тестов.

    Проверяет, что функция `derandomize` класса `ABRandomizer` правильно восстанавливает исходный порядок вариантов.
    """
```

**Как работает функция**:

1.  Создается экземпляр класса `ABRandomizer`.
2.  В цикле 20 раз вызывается метод `randomize` с двумя вариантами ("option1" и "option2").
3.  Для каждой итерации вызывается метод `derandomize` с результатами `randomize` и проверяется, что исходный порядок вариантов восстановлен.

**Примеры**:

```python
randomizer = ABRandomizer()
a, b = randomizer.randomize(0, "option1", "option2")
c, d = randomizer.derandomize(0, a, b)
# Результат: c будет "option1", а d будет "option2".
```

### `test_derandomize_name`

```python
def test_derandomize_name():
    """
    Тестирует корректность дерандомизации имени варианта A/B-теста.

    Проверяет, что функция `derandomize_name` класса `ABRandomizer` правильно определяет,
    какой группе (control или treatment) соответствует выбранный вариант.
    """
```

**Как работает функция**:

1.  Создается экземпляр класса `ABRandomizer`.
2.  В цикле 20 раз вызывается метод `randomize` с двумя вариантами ("cats" и "dogs").
3.  Для каждой итерации вызывается метод `derandomize_name` с результатом выбора ("A") и проверяется,
    соответствует ли результат "control" или "treatment" в зависимости от результата рандомизации.

**Примеры**:

```python
randomizer = ABRandomizer()
a, b = randomizer.randomize(0, "cats", "dogs")
real_name = randomizer.derandomize_name(0, "A")
# Результат: real_name будет "control" или "treatment" в зависимости от результата рандомизации.
```

### `test_passtrough_name`

```python
def test_passtrough_name():
    """
    Тестирует сквозное (passtrough) имя варианта A/B-теста.

    Проверяет, что если задано сквозное имя, то функция `derandomize_name` возвращает это имя без изменений.
    """
```

**Как работает функция**:

1.  Создается экземпляр класса `ABRandomizer` с параметром `passtrough_name=["option3"]`.
2.  Вызывается метод `randomize` с двумя вариантами ("option1" и "option2").
3.  Вызывается метод `derandomize_name` с сквозным именем ("option3") и проверяется, что результат равен "option3".

**Примеры**:

```python
randomizer = ABRandomizer(passtrough_name=["option3"])
a, b = randomizer.randomize(0, "option1", "option2")
real_name = randomizer.derandomize_name(0, "option3")
# Результат: real_name будет "option3".
```

### `test_proposition_with_tinyperson`

```python
def test_proposition_with_tinyperson(setup):
    """
    Тестирует утверждения (proposition) о поведении TinyPerson.

    Проверяет, что утверждения о поведении TinyPerson правильно оцениваются как истинные или ложные.
    """
```

**Как работает функция**:

1.  Создается экземпляр `oscar` класса `create_oscar_the_architect`.
2.  `oscar` выполняет действие `listen_and_act("Tell me a bit about your travel preferences.")`.
3.  Создается утверждение `true_proposition`, проверяющее, упоминает ли `oscar` свои предпочтения в путешествиях. Проверяется, что утверждение истинно.
4.  Создается утверждение `false_proposition`, проверяющее, пишет ли `oscar` роман о том, что кошки лучше собак. Проверяется, что утверждение ложно.

**Примеры**:

```python
oscar = create_oscar_the_architect()
oscar.listen_and_act("Tell me a bit about your travel preferences.")
true_proposition = Proposition(target=oscar, claim="Oscar mentions his travel preferences.")
# Результат: true_proposition.check() будет True.
```

### `test_proposition_with_tinyperson_at_multiple_points`

```python
def test_proposition_with_tinyperson_at_multiple_points(setup):
    """
    Тестирует утверждения о поведении TinyPerson в нескольких точках времени.

    Проверяет, что утверждения о поведении TinyPerson правильно оцениваются как истинные или ложные в зависимости от контекста и времени.
    """
```

**Как работает функция**:

1.  Создается экземпляр `oscar` класса `create_oscar_the_architect`.
2.  `oscar` выполняет действие `listen_and_act("Tell me a bit about your travel preferences.")`.
3.  Создается утверждение `proposition`, проверяющее, говорит ли `oscar` о своих предпочтениях в путешествиях в последние 3 действия. Проверяется, что утверждение истинно.
4.  Выводятся `proposition.justification` и `proposition.confidence`. Проверяется, что длина `proposition.justification` больше 0 и что `proposition.confidence` больше или равно 0.0.
5.  `oscar` выполняет действие `listen_and_act("Now let\'s change subjects. What do you work with?")`.
6.  Проверяется, что то же самое утверждение `proposition` теперь ложно, так как `oscar` сменил тему.

**Примеры**:

```python
oscar = create_oscar_the_architect()
oscar.listen_and_act("Tell me a bit about your travel preferences.")
proposition = Proposition(target=oscar, claim="Oscar talks about his travel preferences", last_n=3)
# Результат: proposition.check() будет True.
oscar.listen_and_act("Now let\'s change subjects. What do you work with?")
# Результат: proposition.check() будет False.
```

### `test_proposition_with_tinyworld`

```python
def test_proposition_with_tinyworld(setup, focus_group_world):
    """
    Тестирует утверждения о поведении TinyWorld.

    Проверяет, что утверждения о событиях в TinyWorld правильно оцениваются как истинные или ложные.
    """
```

**Как работает функция**:

1.  Используется `focus_group_world` как `world` (предположительно, это экземпляр TinyWorld).
2.  `world` выполняет действие `broadcast("Discuss the comparative advantages of dogs and cats.")`.
3.  `world` запускается на 2 шага.
4.  Создается утверждение `true_proposition`, проверяющее, идет ли обсуждение о собаках и кошках. Проверяется, что утверждение истинно.
5.  Создается утверждение `false_proposition`, проверяющее, идет ли обсуждение о портвейне против французского вина. Проверяется, что утверждение ложно.

**Примеры**:

```python
world = focus_group_world
world.broadcast("Discuss the comparative advantages of dogs and cats.")
world.run(2)
true_proposition = Proposition(target=world, claim="There\'s a discussion about dogs and cats.")
# Результат: true_proposition.check() будет True.
```

### `test_proposition_with_multiple_targets`

```python
def test_proposition_with_multiple_targets(setup):
    """
    Тестирует утверждения о поведении нескольких TinyPerson.

    Проверяет, что утверждения о поведении нескольких TinyPerson правильно оцениваются как истинные или ложные.
    """
```

**Как работает функция**:

1.  Создаются экземпляры `oscar` класса `create_oscar_the_architect` и `lisa` класса `create_lisa_the_data_scientist`.
2.  `oscar` выполняет действие `listen_and_act("Tell me a bit about your travel preferences.")`.
3.  `lisa` выполняет действие `listen_and_act("Tell me about your data science projects.")`.
4.  Создается список `targets` из `oscar` и `lisa`.
5.  Создается утверждение `true_proposition`, проверяющее, упоминает ли `oscar` свои предпочтения в путешествиях, и обсуждает ли `lisa` проекты по науке о данных. Проверяется, что утверждение истинно.
6.  Создается утверждение `false_proposition`, проверяющее, пишет ли `oscar` роман о том, что кошки лучше собак. Проверяется, что утверждение ложно.

**Примеры**:

```python
oscar = create_oscar_the_architect()
lisa = create_lisa_the_data_scientist()
oscar.listen_and_act("Tell me a bit about your travel preferences.")
lisa.listen_and_act("Tell me about your data science projects.")
targets = [oscar, lisa]
true_proposition = Proposition(target=targets, claim="Oscar mentions his travel preferences and Lisa discusses data science projects.")
# Результат: true_proposition.check() будет True.
```

### `test_proposition_class_method`

```python
def test_proposition_class_method(setup):
    """
    Тестирует метод класса `check_proposition` для проверки утверждений.

    Проверяет, что метод класса `check_proposition` правильно оценивает утверждения как истинные или ложные.
    """
```

**Как работает функция**:

1.  Создается экземпляр `oscar` класса `create_oscar_the_architect`.
2.  `oscar` выполняет действие `listen_and_act("Tell me a bit about your travel preferences.")`.
3.  Используется метод класса `check_proposition` для проверки утверждения, упоминает ли `oscar` свои предпочтения в путешествиях. Проверяется, что утверждение истинно.
4.  Используется метод класса `check_proposition` для проверки утверждения, пишет ли `oscar` роман о том, что кошки лучше собак. Проверяется, что утверждение ложно.

**Примеры**:

```python
oscar = create_oscar_the_architect()
oscar.listen_and_act("Tell me a bit about your travel preferences.")
# Результат: check_proposition(target=oscar, claim="Oscar mentions his travel preferences.") будет True.
```