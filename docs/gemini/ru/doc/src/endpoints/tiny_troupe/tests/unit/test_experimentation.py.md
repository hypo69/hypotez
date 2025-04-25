# Модуль тестирования экспериментальных функций

## Обзор

Этот модуль содержит набор юнит-тестов для проверки функциональности экспериментальных функций в `hypotez`, таких как:

- `ABRandomizer`: Класс, реализующий A/B тестирование с помощью рандомизации вариантов.
- `Proposition`: Класс для проверки утверждений (пропозиций) на основе текстовых ответов персонажей.

## Тесты

### `test_randomize`

**Назначение**: Проверка корректной работы метода `randomize` в `ABRandomizer` для рандомизации вариантов.

**Параметры**:

- `i`: Индекс элемента для рандомизации.

**Как работает**:

- Создается объект `ABRandomizer`.
- В цикле выполняется рандомизация с помощью `randomize` для индекса `i`.
- Проверяется, что полученный результат соответствует ожидаемому в зависимости от случайного выбора вариантов.
- Проверяется, что выбор варианта соответствует рандомизированному выбору.
- При отсутствии рандомизации генерируется исключение.

**Примеры**:

```python
>>> randomizer = ABRandomizer()
>>> a, b = randomizer.randomize(0, "option1", "option2")
>>> if randomizer.choices[0] == (0, 1):
...     assert (a, b) == ("option1", "option2")
... elif randomizer.choices[0] == (1, 0):
...     assert (a, b) == ("option2", "option1")
... else:
...     raise Exception(f"No randomization found for item {0}")
```

### `test_derandomize`

**Назначение**: Проверка корректной работы метода `derandomize` в `ABRandomizer` для восстановления реальных значений вариантов после рандомизации.

**Параметры**:

- `i`: Индекс элемента для дерандомизации.
- `a`: Рандомизированное значение варианта 1.
- `b`: Рандомизированное значение варианта 2.

**Как работает**:

- Создается объект `ABRandomizer`.
- В цикле выполняется рандомизация с помощью `randomize` для индекса `i`.
- Затем выполняется дерандомизация с помощью `derandomize` для восстановления исходных значений.
- Проверяется, что дерандомизированные значения совпадают с исходными значениями вариантов.

**Примеры**:

```python
>>> randomizer = ABRandomizer()
>>> a, b = randomizer.randomize(0, "option1", "option2")
>>> c, d = randomizer.derandomize(0, a, b)
>>> assert (c, d) == ("option1", "option2")
```

### `test_derandomize_name`

**Назначение**: Проверка корректной работы метода `derandomize_name` в `ABRandomizer` для определения реального названия варианта (control/treatment) после рандомизации.

**Параметры**:

- `i`: Индекс элемента для дерандомизации.
- `A`: Рандомизированное название варианта.

**Как работает**:

- Создается объект `ABRandomizer`.
- В цикле выполняется рандомизация с помощью `randomize` для индекса `i`.
- Затем выполняется дерандомизация с помощью `derandomize_name` для определения реального названия варианта.
- Проверяется, что полученное название соответствует рандомизированному выбору.
- Проверяется, что выбор варианта соответствует рандомизированному выбору.
- При отсутствии рандомизации генерируется исключение.

**Примеры**:

```python
>>> randomizer = ABRandomizer()
>>> a, b = randomizer.randomize(0, "cats", "dogs")
>>> real_name = randomizer.derandomize_name(0, "A")
>>> if randomizer.choices[0] == (0, 1):
...     # "Favorite pet? A: cats, B: dogs"
...     # user selects "A"
...     # user selected the control group
...     assert real_name == "control"
... elif randomizer.choices[0] == (1, 0):
...     # "Favorite pet? A: dogs, B: cats"
...     # user selects "A"
...     # user selected the treatment group
...     assert real_name == "treatment"
... else:
...     raise Exception(f"No randomization found for item {0}")
```

### `test_passtrough_name`

**Назначение**: Проверка корректной работы метода `derandomize_name` в `ABRandomizer` для возврата имени варианта, который не участвовал в рандомизации.

**Параметры**:

- `i`: Индекс элемента для дерандомизации.
- `A`: Рандомизированное название варианта.

**Как работает**:

- Создается объект `ABRandomizer` с параметром `passtrough_name`, который содержит список вариантов, не участвующих в рандомизации.
- Выполняется рандомизация с помощью `randomize` для индекса `i`.
- Затем выполняется дерандомизация с помощью `derandomize_name` для определения реального названия варианта.
- Проверяется, что возвращенное название соответствует имени варианта из `passtrough_name`.

**Примеры**:

```python
>>> randomizer = ABRandomizer(passtrough_name=["option3"])
>>> a, b = randomizer.randomize(0, "option1", "option2")
>>> real_name = randomizer.derandomize_name(0, "option3")
>>> assert real_name == "option3"
```

### `test_proposition_with_tinyperson`

**Назначение**: Проверка корректной работы класса `Proposition` для проверки утверждений (пропозиций) на основе текстовых ответов персонажей.

**Параметры**:

- `setup`: Фикстура, устанавливающая тестовый контекст.
- `target`: Объект типа `TinyPerson`, представляющий персонажа.
- `claim`: Текстовое утверждение (пропозиция), которое нужно проверить.

**Как работает**:

- Создается объект `TinyPerson` (в данном случае `oscar`).
- Создается объект `Proposition` с заданными параметрами `target` и `claim`.
- Вызывается метод `check` объекта `Proposition` для проверки утверждения.
- Проверяется, что результат проверки соответствует ожидаемому.

**Примеры**:

```python
>>> oscar = create_oscar_the_architect()
>>> oscar.listen_and_act("Tell me a bit about your travel preferences.")
>>> true_proposition = Proposition(target=oscar, claim="Oscar mentions his travel preferences.")
>>> assert true_proposition.check() == True
>>> false_proposition = Proposition(target=oscar, claim="Oscar writes a novel about how cats are better than dogs.")
>>> assert false_proposition.check() == False
```

### `test_proposition_with_tinyperson_at_multiple_points`

**Назначение**: Проверка корректной работы класса `Proposition` для проверки утверждений (пропозиций) на основе текстовых ответов персонажей, учитывая историю последних ответов.

**Параметры**:

- `setup`: Фикстура, устанавливающая тестовый контекст.
- `target`: Объект типа `TinyPerson`, представляющий персонажа.
- `claim`: Текстовое утверждение (пропозиция), которое нужно проверить.
- `last_n`: Количество последних ответов персонажа, которые нужно учитывать при проверке.

**Как работает**:

- Создается объект `TinyPerson` (в данном случае `oscar`).
- Создается объект `Proposition` с заданными параметрами `target`, `claim` и `last_n`.
- Вызывается метод `check` объекта `Proposition` для проверки утверждения.
- Проверяется, что результат проверки соответствует ожидаемому.
- Проверяется, что в атрибутах `justification` и `confidence` объекта `Proposition` содержатся корректные данные.

**Примеры**:

```python
>>> oscar = create_oscar_the_architect()
>>> oscar.listen_and_act("Tell me a bit about your travel preferences.")
>>> proposition = Proposition(target=oscar, claim="Oscar talks about his travel preferences", last_n=3)
>>> assert proposition.check() == True
>>> print(proposition.justification)
>>> print(proposition.confidence)
>>> assert len(proposition.justification) > 0
>>> assert proposition.confidence >= 0.0
>>> oscar.listen_and_act("Now let's change subjects. What do you work with?")
>>> assert proposition.check() == False # the _same_ proposition is no longer true, because Oscar changed subjects
```

### `test_proposition_with_tinyworld`

**Назначение**: Проверка корректной работы класса `Proposition` для проверки утверждений (пропозиций) на основе текстовых ответов в `TinyWorld`.

**Параметры**:

- `setup`: Фикстура, устанавливающая тестовый контекст.
- `focus_group_world`: Объект типа `TinyWorld`, представляющий мир с фокус-группой.
- `target`: Объект типа `TinyWorld`, представляющий мир.
- `claim`: Текстовое утверждение (пропозиция), которое нужно проверить.

**Как работает**:

- Создается объект `TinyWorld` (`focus_group_world`).
- Выполняется broadcast сообщения в мир.
- Создается объект `Proposition` с заданными параметрами `target` и `claim`.
- Вызывается метод `check` объекта `Proposition` для проверки утверждения.
- Проверяется, что результат проверки соответствует ожидаемому.

**Примеры**:

```python
>>> world = focus_group_world
>>> world.broadcast("Discuss the comparative advantages of dogs and cats.")
>>> world.run(2)
>>> true_proposition = Proposition(target=world, claim="There's a discussion about dogs and cats.")
>>> assert true_proposition.check() == True
>>> false_proposition = Proposition(target=world, claim="There's a discussion about whether porto wine vs french wine.")
>>> assert false_proposition.check() == False
```

### `test_proposition_with_multiple_targets`

**Назначение**: Проверка корректной работы класса `Proposition` для проверки утверждений (пропозиций) на основе текстовых ответов нескольких персонажей.

**Параметры**:

- `setup`: Фикстура, устанавливающая тестовый контекст.
- `targets`: Список объектов типа `TinyPerson`, представляющих персонажей.
- `claim`: Текстовое утверждение (пропозиция), которое нужно проверить.

**Как работает**:

- Создается объект `TinyPerson` (в данном случае `oscar` и `lisa`).
- Создается список `targets`, содержащий объекты `oscar` и `lisa`.
- Создается объект `Proposition` с заданными параметрами `target` (список `targets`) и `claim`.
- Вызывается метод `check` объекта `Proposition` для проверки утверждения.
- Проверяется, что результат проверки соответствует ожидаемому.

**Примеры**:

```python
>>> oscar = create_oscar_the_architect()
>>> lisa = create_lisa_the_data_scientist()
>>> oscar.listen_and_act("Tell me a bit about your travel preferences.")
>>> lisa.listen_and_act("Tell me about your data science projects.")
>>> targets = [oscar, lisa]
>>> true_proposition = Proposition(target=targets, claim="Oscar mentions his travel preferences and Lisa discusses data science projects.")
>>> assert true_proposition.check() == True
>>> false_proposition = Proposition(target=targets, claim="Oscar writes a novel about how cats are better than dogs.")
>>> assert false_proposition.check() == False
```

### `test_proposition_class_method`

**Назначение**: Проверка корректной работы метода класса `check_proposition` для удобного вызова проверки утверждений (пропозиций).

**Параметры**:

- `setup`: Фикстура, устанавливающая тестовый контекст.
- `target`: Объект типа `TinyPerson`, представляющий персонажа.
- `claim`: Текстовое утверждение (пропозиция), которое нужно проверить.

**Как работает**:

- Создается объект `TinyPerson` (в данном случае `oscar`).
- Вызывается метод класса `check_proposition` с заданными параметрами `target` и `claim`.
- Проверяется, что результат проверки соответствует ожидаемому.

**Примеры**:

```python
>>> oscar = create_oscar_the_architect()
>>> oscar.listen_and_act("Tell me a bit about your travel preferences.")
>>> assert check_proposition(target=oscar, claim="Oscar mentions his travel preferences.") == True
>>> assert check_proposition(oscar, "Oscar mentions his travel preferences.") == True
>>> assert check_proposition(target=oscar, claim="Oscar writes a novel about how cats are better than dogs.") == False
>>> assert check_proposition(oscar, "Oscar writes a novel about how cats are better than dogs.") == False
```