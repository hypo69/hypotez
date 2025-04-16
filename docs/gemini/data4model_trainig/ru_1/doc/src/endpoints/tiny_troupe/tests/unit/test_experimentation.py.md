# Модуль тестирования `test_experimentation.py`

## Обзор

Модуль содержит юнит-тесты для проверки функциональности модулей `ABRandomizer` и `Proposition` из пакета `tinytroupe.experimentation`.
Тесты охватывают рандомизацию, дерандомизацию, проверку утверждений с использованием экземпляров `TinyPerson` и `TinyWorld`,
а также проверку утверждений с несколькими целями.

## Подробнее

Модуль тестирует различные аспекты функциональности, такие как правильность рандомизации и дерандомизации вариантов,
проверку утверждений на основе поведения персонажей и мировых событий, а также работу с несколькими целями для утверждений.

## Классы

В данном модуле классы не определены. Здесь находятся юнит-тесты, проверяющие другие классы.

## Функции

### `test_randomize`

```python
def test_randomize():
    """Тестирует рандомизацию вариантов с помощью ABRandomizer.

    Функция создает экземпляр `ABRandomizer` и выполняет несколько итераций,
    чтобы убедиться, что рандомизация работает корректно. Проверяет, что возвращаемые значения соответствуют
    выбранным вариантам в `randomizer.choices`.

    Raises:
        Exception: Если для элемента `i` не найдена рандомизация.

    Пример:
        >>> test_randomize()
    """
    ...
```

**Как работает функция**:
- Создается экземпляр класса `ABRandomizer`.
- В цикле 20 раз вызывается метод `randomize` с различными индексами и вариантами "option1" и "option2".
- Проверяется, что возвращаемые значения `a` и `b` соответствуют значениям в списке `randomizer.choices`.
- Если `randomizer.choices[i]` равно `(0, 1)`, то `(a, b)` должно быть равно `("option1", "option2")`.
- Если `randomizer.choices[i]` равно `(1, 0)`, то `(a, b)` должно быть равно `("option2", "option1")`.
- Если ни одно из условий не выполнено, выбрасывается исключение `Exception`.

### `test_derandomize`

```python
def test_derandomize():
    """Тестирует дерандомизацию вариантов с помощью ABRandomizer.

    Функция создает экземпляр `ABRandomizer` и выполняет несколько итераций,
    чтобы убедиться, что дерандомизация возвращает исходные варианты.

    Пример:
        >>> test_derandomize()
    """
    ...
```

**Как работает функция**:
- Создается экземпляр класса `ABRandomizer`.
- В цикле 20 раз вызывается метод `randomize` с различными индексами и вариантами "option1" и "option2".
- Затем вызывается метод `derandomize` с теми же индексами и возвращенными значениями `a` и `b`.
- Проверяется, что возвращаемые значения `c` и `d` из `derandomize` соответствуют исходным вариантам `("option1", "option2")`.

### `test_derandomize_name`

```python
def test_derandomize_name():
    """Тестирует функцию derandomize_name в классе ABRandomizer.

    Функция проверяет, что derandomize_name правильно определяет контрольную
    и экспериментальную группы на основе выбора пользователя и рандомизации.

    Raises:
        Exception: Если для элемента `i` не найдена рандомизация.

    Пример:
        >>> test_derandomize_name()
    """
    ...
```

**Как работает функция**:
- Создается экземпляр класса `ABRandomizer`.
- В цикле 20 раз вызывается метод `randomize` с вариантами "cats" и "dogs".
- Вызывается метод `derandomize_name` с индексом `i` и выбором пользователя "A".
- Если `randomizer.choices[i]` равно `(0, 1)`, то `real_name` должно быть равно "control".
- Если `randomizer.choices[i]` равно `(1, 0)`, то `real_name` должно быть равно "treatment".
- Если ни одно из условий не выполнено, выбрасывается исключение `Exception`.

### `test_passtrough_name`

```python
def test_passtrough_name():
    """Тестирует сценарий, когда derandomize_name возвращает переданное имя без изменений.

    Функция создает ABRandomizer с passtrough_name и проверяет, что derandomize_name
    возвращает исходное имя, если оно указано в passtrough_name.

    Пример:
        >>> test_passtrough_name()
    """
    ...
```

**Как работает функция**:
- Создается экземпляр класса `ABRandomizer` с `passtrough_name=["option3"]`.
- Вызывается метод `randomize` с вариантами "option1" и "option2".
- Вызывается метод `derandomize_name` с индексом `0` и именем "option3".
- Проверяется, что `real_name` равно "option3".

### `test_proposition_with_tinyperson`

```python
def test_proposition_with_tinyperson(setup):
    """Тестирует проверку утверждений с использованием экземпляра TinyPerson.

    Функция создает экземпляр `TinyPerson` (Oscar) и проверяет,
    что утверждения о его поведении оцениваются правильно.

    Args:
        setup: Аргумент настройки pytest (fixture).

    Пример:
        >>> test_proposition_with_tinyperson(setup)
    """
    ...
```

**Как работает функция**:
- Создается экземпляр `TinyPerson` с именем `oscar` с помощью функции `create_oscar_the_architect()`.
- `oscar` взаимодействует с окружением, выполняя действие "Tell me a bit about your travel preferences.".
- Создается экземпляр класса `Proposition` с целью `oscar` и утверждением "Oscar mentions his travel preferences.".
- Проверяется, что `true_proposition.check()` возвращает `True`.
- Создается экземпляр класса `Proposition` с целью `oscar` и утверждением "Oscar writes a novel about how cats are better than dogs.".
- Проверяется, что `false_proposition.check()` возвращает `False`.

### `test_proposition_with_tinyperson_at_multiple_points`

```python
def test_proposition_with_tinyperson_at_multiple_points(setup):
    """Тестирует проверку утверждений в нескольких точках взаимодействия с TinyPerson.

    Функция создает экземпляр `TinyPerson` (Oscar) и проверяет, что утверждения
    о его поведении оцениваются правильно в разные моменты времени.

    Args:
        setup: Аргумент настройки pytest (fixture).

    Пример:
        >>> test_proposition_with_tinyperson_at_multiple_points(setup)
    """
    ...
```

**Как работает функция**:
- Создается экземпляр `TinyPerson` с именем `oscar` с помощью функции `create_oscar_the_architect()`.
- `oscar` взаимодействует с окружением, выполняя действие "Tell me a bit about your travel preferences.".
- Создается экземпляр класса `Proposition` с целью `oscar`, утверждением "Oscar talks about his travel preferences" и параметром `last_n=3`.
- Проверяется, что `proposition.check()` возвращает `True`.
- Выводятся значения `proposition.justification` и `proposition.confidence`.
- Проверяется, что длина `proposition.justification` больше 0 и `proposition.confidence` больше или равно 0.0.
- `oscar` взаимодействует с окружением, выполняя действие "Now let's change subjects. What do you work with?".
- Проверяется, что `proposition.check()` возвращает `False`, так как утверждение больше не соответствует текущему поведению `oscar`.

### `test_proposition_with_tinyworld`

```python
def test_proposition_with_tinyworld(setup, focus_group_world):
    """Тестирует проверку утверждений с использованием экземпляра TinyWorld.

    Функция создает экземпляр `TinyWorld` и проверяет, что утверждения
    о событиях в мире оцениваются правильно.

    Args:
        setup: Аргумент настройки pytest (fixture).
        focus_group_world: Аргумент настройки pytest (fixture), представляющий экземпляр TinyWorld.

    Пример:
        >>> test_proposition_with_tinyworld(setup, focus_group_world)
    """
    ...
```

**Как работает функция**:
- Используется предоставленный `focus_group_world` как экземпляр `TinyWorld`.
- `world` "broadcast" сообщение "Discuss the comparative advantages of dogs and cats.".
- `world` запускается на 2 итерации.
- Создается экземпляр класса `Proposition` с целью `world` и утверждением "There's a discussion about dogs and cats.".
- Проверяется, что `true_proposition.check()` возвращает `True`.
- Создается экземпляр класса `Proposition` с целью `world` и утверждением "There's a discussion about whether porto wine vs french wine.".
- Проверяется, что `false_proposition.check()` возвращает `False`.

### `test_proposition_with_multiple_targets`

```python
def test_proposition_with_multiple_targets(setup):
    """Тестирует проверку утверждений с несколькими целями (TinyPerson).

    Функция создает два экземпляра `TinyPerson` (Oscar и Lisa) и проверяет,
    что утверждения, включающие обоих персонажей, оцениваются правильно.

    Args:
        setup: Аргумент настройки pytest (fixture).

    Пример:
        >>> test_proposition_with_multiple_targets(setup)
    """
    ...
```

**Как работает функция**:
- Создаются экземпляры `TinyPerson` с именами `oscar` и `lisa` с помощью функций `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
- `oscar` взаимодействует с окружением, выполняя действие "Tell me a bit about your travel preferences.".
- `lisa` взаимодействует с окружением, выполняя действие "Tell me about your data science projects.".
- Создается список `targets` с `oscar` и `lisa`.
- Создается экземпляр класса `Proposition` с целью `targets` и утверждением "Oscar mentions his travel preferences and Lisa discusses data science projects.".
- Проверяется, что `true_proposition.check()` возвращает `True`.
- Создается экземпляр класса `Proposition` с целью `targets` и утверждением "Oscar writes a novel about how cats are better than dogs.".
- Проверяется, что `false_proposition.check()` возвращает `False`.

### `test_proposition_class_method`

```python
def test_proposition_class_method(setup):
    """Тестирует проверку утверждений с использованием class method `check_proposition`.

    Функция создает экземпляр `TinyPerson` (Oscar) и проверяет, что утверждения
    о его поведении оцениваются правильно с использованием class method.

    Args:
        setup: Аргумент настройки pytest (fixture).

    Пример:
        >>> test_proposition_class_method(setup)
    """
    ...
```

**Как работает функция**:
- Создается экземпляр `TinyPerson` с именем `oscar` с помощью функции `create_oscar_the_architect()`.
- `oscar` взаимодействует с окружением, выполняя действие "Tell me a bit about your travel preferences.".
- Проверяется, что `check_proposition(target=oscar, claim="Oscar mentions his travel preferences.")` возвращает `True`.
- Проверяется, что `check_proposition(oscar, "Oscar mentions his travel preferences.")` возвращает `True`.
- Проверяется, что `check_proposition(target=oscar, claim="Oscar writes a novel about how cats are better than dogs.")` возвращает `False`.
- Проверяется, что `check_proposition(oscar, "Oscar writes a novel about how cats are better than dogs.")` возвращает `False`.