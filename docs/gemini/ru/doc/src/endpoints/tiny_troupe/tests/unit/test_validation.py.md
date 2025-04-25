# Модуль `test_validation.py`

## Обзор

Модуль `test_validation.py` содержит набор юнит-тестов для проверки функциональности валидации персонажей в проекте `tinytroupe`.

## Тесты

### `test_validate_person`

**Описание**: Тестовая функция, проверяющая работу валидатора персонажей на примере двух персонажей: банкира и монаха. 

**Параметры**:
- `setup`: Фикстура, устанавливающая тестовую среду.

**Принцип работы**:

- Функция создает два объекта `TinyPerson` с помощью `TinyPersonFactory`: "банкира" и "монаха".
- Определяет ожидания для каждого персонажа с помощью текстовых описаний.
- Выполняет валидацию персонажей с помощью метода `validate_person` класса `TinyPersonValidator`.
- Проверяет, что полученные баллы валидации (banker_score и monk_score) превышают 0.5.
- Проверяет, что результат валидации монаха с ожиданиями для банкира (wrong_expectations_score) меньше 0.5.

**Примеры**:

```python
    banker_score, banker_justification = TinyPersonValidator.validate_person(banker, expectations=banker_expectations, include_agent_spec=False, max_content_length=None)
    assert banker_score > 0.5, f"Validation score is too low: {banker_score:.2f}"

    monk_score, monk_justification = TinyPersonValidator.validate_person(monk, expectations=monk_expectations, include_agent_spec=False, max_content_length=None)
    assert monk_score > 0.5, f"Validation score is too low: {monk_score:.2f}"

    wrong_expectations_score, wrong_expectations_justification = TinyPersonValidator.validate_person(monk, expectations=banker_expectations, include_agent_spec=False, max_content_length=None)
    assert wrong_expectations_score < 0.5, f"Validation score is too high: {wrong_expectations_score:.2f}"
```

## Используемые функции

- **`TinyPersonFactory.generate_person`**: Метод класса `TinyPersonFactory`, генерирующий объект `TinyPerson` на основе заданного описания.
- **`TinyPersonValidator.validate_person`**: Метод класса `TinyPersonValidator`, выполняющий валидацию персонажа на основе заданных ожиданий.

## Используемые модули

- `pytest`: Фреймворк для тестирования.
- `os`: Модуль для работы с файловой системой.
- `sys`: Модуль для работы с системными параметрами.
- `tinytroupe.examples`: Модуль, содержащий примеры персонажей.
- `tinytroupe.control`: Модуль, содержащий класс `Simulation` для управления симуляцией.
- `tinytroupe.factory`: Модуль, содержащий класс `TinyPersonFactory` для создания объектов `TinyPerson`.
- `tinytroupe.validation`: Модуль, содержащий класс `TinyPersonValidator` для валидации персонажей.
- `testing_utils`: Модуль, содержащий вспомогательные функции для тестирования.