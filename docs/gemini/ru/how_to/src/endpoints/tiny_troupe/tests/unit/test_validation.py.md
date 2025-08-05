## Как использовать блок кода `test_validate_person` 
=========================================================================================

### Описание
-------------------------
Этот блок кода представляет собой тест для валидации `TinyPerson` объекта. Он проверяет, насколько хорошо созданный персонаж (с помощью `TinyPersonFactory`) соответствует заданным ожиданиям (через параметр `expectations`). 

### Шаги выполнения
-------------------------
1. **Определение персонажа:**  Вначале тест определяет два типа персонажей: `banker` и `monk`. 
    - Для каждого персонажа задается описание, которое используется для генерации его свойств (`bank_spec`, `banker_spec`, `monastery_spec`, `monk_spec`).
2. **Создание персонажа:**  Для каждого персонажа создается объект `TinyPerson`  с помощью `TinyPersonFactory`. 
3. **Валидация персонажа:**  Проверяется валидность созданного персонажа с помощью `TinyPersonValidator.validate_person`. В качестве параметра `expectations` передается описание ожидаемых свойств.
4. **Проверка результатов:** Тест проверяет, что:
    - Счет валидации для `banker` и `monk` больше 0.5, что означает хорошее соответствие заданным ожиданиям. 
    - Счет валидации для `monk` с использованием ожиданий `banker` меньше 0.5, что означает, что этот персонаж не соответствует ожиданиям. 

### Пример использования
-------------------------

```python
import pytest
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.validation import TinyPersonValidator

# Определение персонажа
banker_spec = """
    A vice-president of one of the largest brazillian banks. Has a degree in engineering and an MBA in finance.
    """

# Создание персонажа
banker_factory = TinyPersonFactory(banker_spec)
banker = banker_factory.generate_person(banker_spec)

# Ожидания для персонажа
banker_expectations = """
    He/she is:
    - Wealthy
    - Very intelligent and ambitious
    - Has a lot of connections
    - Is in his 40s or 50s
    """

# Валидация персонажа
banker_score, banker_justification = TinyPersonValidator.validate_person(banker, expectations=banker_expectations, include_agent_spec=False, max_content_length=None)

# Вывод результатов
print("Banker score:", banker_score)
print("Banker justification:", banker_justification)

# Проверка результата
assert banker_score > 0.5, f"Validation score is too low: {banker_score:.2f}" 
```