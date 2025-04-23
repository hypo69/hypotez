### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор тестов для проверки функциональности классов `ABRandomizer` и `Proposition`, используемых для A/B-тестирования и проверки утверждений (proposition) в контексте `tinytroupe`. Тесты охватывают рандомизацию, дерандомизацию, проверку утверждений с участием объектов `TinyPerson` и `TinyWorld`, а также проверку утверждений с использованием множественных целей.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей и классов**:
   - Импортируются модули `pytest`, `ABRandomizer`, `Proposition`, `check_proposition`, а также функции для создания объектов `TinyPerson` (например, `create_oscar_the_architect`).
   - `sys.path.append` используется для добавления путей к директориям, содержащим необходимые модули, чтобы их можно было импортировать.

2. **Тест `test_randomize`**:
   - Создается экземпляр класса `ABRandomizer`.
   - В цикле 20 раз вызывается метод `randomize` с различными индексами `i` и двумя опциями (`"option1"`, `"option2"`).
   - Проверяется, что возвращаемые значения `a` и `b` соответствуют ожидаемым на основе `randomizer.choices[i]`.

3. **Тест `test_derandomize`**:
   - Создается экземпляр класса `ABRandomizer`.
   - В цикле 20 раз вызывается метод `randomize`, а затем метод `derandomize` с полученными значениями `a` и `b`.
   - Проверяется, что `derandomize` возвращает исходные опции (`"option1"`, `"option2"`).

4. **Тест `test_derandomize_name`**:
   - Создается экземпляр класса `ABRandomizer`.
   - В цикле 20 раз вызывается метод `randomize` с опциями `"cats"` и `"dogs"`.
   - Вызывается метод `derandomize_name` с полученными значениями и проверяется, что возвращаемое значение (`"control"` или `"treatment"`) соответствует ожидаемому на основе `randomizer.choices[i]`.

5. **Тест `test_passtrough_name`**:
   - Создается экземпляр класса `ABRandomizer` с параметром `passtrough_name=["option3"]`.
   - Вызывается метод `randomize` с опциями `"option1"` и `"option2"`.
   - Вызывается метод `derandomize_name` с опцией `"option3"` и проверяется, что возвращается `"option3"`.

6. **Тест `test_proposition_with_tinyperson`**:
   - Создается объект `oscar` с помощью функции `create_oscar_the_architect()`.
   - Вызывается метод `listen_and_act` у объекта `oscar`.
   - Создаются два объекта `Proposition`: `true_proposition` и `false_proposition`.
   - Проверяется, что `true_proposition.check()` возвращает `True`, а `false_proposition.check()` возвращает `False`.

7. **Тест `test_proposition_with_tinyperson_at_multiple_points`**:
   - Создается объект `oscar` с помощью функции `create_oscar_the_architect()`.
   - Вызывается метод `listen_and_act` у объекта `oscar`.
   - Создается объект `Proposition` с параметром `last_n=3`.
   - Проверяется, что `proposition.check()` возвращает `True`, а также что длина `proposition.justification` больше 0 и `proposition.confidence` больше или равна 0.0.
   - Вызывается метод `listen_and_act` еще раз, и проверяется, что `proposition.check()` теперь возвращает `False`.

8. **Тест `test_proposition_with_tinyworld`**:
   - Получается объект `world` из фикстуры `focus_group_world`.
   - Вызывается метод `broadcast` у объекта `world` и метод `run`.
   - Создаются два объекта `Proposition`: `true_proposition` и `false_proposition`.
   - Проверяется, что `true_proposition.check()` возвращает `True`, а `false_proposition.check()` возвращает `False`.

9. **Тест `test_proposition_with_multiple_targets`**:
   - Создаются объекты `oscar` и `lisa` с помощью соответствующих функций.
   - Вызываются методы `listen_and_act` у обоих объектов.
   - Создается список `targets`, содержащий `oscar` и `lisa`.
   - Создаются два объекта `Proposition`: `true_proposition` и `false_proposition` с `target=targets`.
   - Проверяется, что `true_proposition.check()` возвращает `True`, а `false_proposition.check()` возвращает `False`.

10. **Тест `test_proposition_class_method`**:
    - Создается объект `oscar` с помощью функции `create_oscar_the_architect()`.
    - Вызывается метод `listen_and_act` у объекта `oscar`.
    - Используется функция `check_proposition` (как классовый метод) для проверки утверждений об объекте `oscar`.
    - Проверяется, что утверждения возвращают ожидаемые значения `True` или `False`.

Пример использования
-------------------------

```python
import pytest
from tinytroupe.experimentation import ABRandomizer, Proposition
from tinytroupe.examples import create_oscar_the_architect

def test_randomize():
    randomizer = ABRandomizer()
    for i in range(20):
        a, b = randomizer.randomize(i, "option1", "option2")

        if randomizer.choices[i] == (0, 1):
            assert (a, b) == ("option1", "option2")
        elif randomizer.choices[i] == (1, 0):
            assert (a, b) == ("option2", "option1")

def test_proposition_with_tinyperson(setup):
    oscar = create_oscar_the_architect()
    oscar.listen_and_act("Tell me a bit about your travel preferences.")
    
    true_proposition = Proposition(target=oscar, claim="Oscar mentions his travel preferences.")
    assert true_proposition.check() == True

    false_proposition = Proposition(target=oscar, claim="Oscar writes a novel about how cats are better than dogs.")
    assert false_proposition.check() == False