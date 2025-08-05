# hypotez/src/endpoints/tiny_troupe/tests/unit/test_validation.py

## Overview

Этот файл содержит юнит-тесты для модуля `tinytroupe.validation`, который отвечает за валидацию персонажей, созданных с помощью `TinyPersonFactory`. Тесты проверяют корректность работы функции `TinyPersonValidator.validate_person` и её способность оценивать соответствие характеристик персонажа заданным ожиданиям.

## Details

Файл содержит два тестовых сценария:

- **Тестирование валидации "банкира"**:  Тест проверяет, что созданный "банкир" соответствует заданным ожиданиям. Ожидания  описывают  характерные черты  "банкира"  в  контексте его профессии.
- **Тестирование валидации "монаха"**: Тест проверяет, что созданный "монах" соответствует заданным ожиданиям. Ожидания  описывают  характерные черты  "монаха"  в  контексте его образа жизни и философии.

Тесты также проверяют, что функция `TinyPersonValidator.validate_person` возвращает низкую оценку, если  применяются неправильные ожидания для персонажа.

## Classes

### `TinyPersonValidator`

**Description**: Класс, который содержит функции для валидации персонажей, созданных с помощью `TinyPersonFactory`.

**Attributes**:

- `None`: Класс не имеет собственных атрибутов.

**Methods**:

- `validate_person(person: dict, expectations: str, include_agent_spec: bool = False, max_content_length: Optional[int] = None) -> Tuple[float, str]`:  Валидирует персонажа, сравнивая его характеристики с заданными ожиданиями.

## Functions

### `test_validate_person(setup)`

**Purpose**: Проверяет  корректность  работы  функции  `TinyPersonValidator.validate_person`  в  двух  сценариях:  для  "банкира"  и  "монаха".

**Parameters**:

- `setup`: Фикстура, которая инициализирует  необходимые  параметры  перед  запуском  теста.

**Returns**:

- `None`: Тестовая функция не возвращает значение.

**Raises Exceptions**:

- `AssertionError`: Если полученная оценка валидации не соответствует ожидаемому результату.

**Inner Functions**:

-  `None`:  Тестовая  функция  не  использует  внутренние  функции.

**How the Function Works**:

1.  Создается "банкир"  и  "монах"  с  помощью  `TinyPersonFactory`.
2.  Валидация  персонажей  проводится  с  помощью  `TinyPersonValidator.validate_person`,  используя  заданные  ожидания  для  каждого  персонажа.
3.  Ожидания  описывают  характерные  черты  "банкира"  и  "монаха"  соответственно.
4.  Тест  проверяет,  что  оценка  валидации  для  "банкира"  и  "монаха"  превышает  0,5.
5.  Тест  проверяет,  что  оценка  валидации  для  "монаха"  с  ожиданиями,  принадлежащими  "банкиру",  меньше  0,5.
6.  Тест  выводит  результаты  валидации  в  консоль  для  просмотра.

**Examples**:

```python
def test_validate_person(setup):

    ##########################
    # Banker
    ##########################
    bank_spec = ...
    """
    A large brazillian bank. It has a lot of branches and a large number of employees. It is facing a lot of competition from fintechs.
    """

    banker_spec = ...
    """
    A vice-president of one of the largest brazillian banks. Has a degree in engineering and an MBA in finance.
    """
    
    banker_factory = TinyPersonFactory(bank_spec)
    banker = banker_factory.generate_person(banker_spec)

    banker_expectations = ...
    """
    He/she is:
    - Wealthy
    - Very intelligent and ambitious
    - Has a lot of connections
    - Is in his 40s or 50s

    Tastes:
    - Likes to travel to other countries
    - Either read books, collect art or play golf
    - Enjoy only the best, most expensive, wines and food
    - Dislikes taxes and regulation

    Other notable traits:
    - Has some stress issues, and might be a bit of a workaholic
    - Deep knowledge of finance, economics and financial technology
    - Is a bit of a snob
    """
    banker_score, banker_justification = TinyPersonValidator.validate_person(banker, expectations=banker_expectations, include_agent_spec=False, max_content_length=None)
    print("Banker score: ", banker_score)
    print("Banker justification: ", banker_justification)

    assert banker_score > 0.5, f"Validation score is too low: {banker_score:.2f}"


    ##########################
    # Monk  
    ########################## 
    monastery_spec = "A remote monastery in the Himalayas, where only spiritual seekers are allowed."

    monk_spec = ...
    """
    A poor buddhist monk living alone and isolated in a remote montain.
    """
    monk_spec_factory = TinyPersonFactory(monastery_spec)
    monk = monk_spec_factory.generate_person(monk_spec)
    
    monk_expectations = ...
    """
    Some characteristics of this person:
    - Is very poor, and in fact do not seek money
    - Has no formal education, but is very wise
    - Is very calm and patient
    - Is very humble and does not seek attention
    - Honesty is a core value    
    """

    monk_score, monk_justification = TinyPersonValidator.validate_person(monk, expectations=monk_expectations, include_agent_spec=False, max_content_length=None)
    print("Monk score: ", monk_score)
    print("Monk justification: ", monk_justification)
          

    assert monk_score > 0.5, f"Validation score is too low: {monk_score:.2f}"

    # Now, let's check the score for the monk with the wrong expectations! It has to be low!
    wrong_expectations_score, wrong_expectations_justification = TinyPersonValidator.validate_person(monk, expectations=banker_expectations, include_agent_spec=False, max_content_length=None)

    assert wrong_expectations_score < 0.5, f"Validation score is too high: {wrong_expectations_score:.2f}"
    print("Wrong expectations score: ", wrong_expectations_score)
    print("Wrong expectations justification: ", wrong_expectations_justification)
```

## Parameter Details

- `person` (dict): Словарь, который содержит информацию о персонаже, созданном с помощью `TinyPersonFactory`.
- `expectations` (str): Строка, содержащая описание ожидаемых характеристик персонажа.
- `include_agent_spec` (bool, optional): Если `True`, в оценку валидации включается информация о том, как персонаж был создан. По умолчанию `False`.
- `max_content_length` (Optional[int], optional): Максимальная длина текста, который будет использоваться для валидации. По умолчанию `None`, что означает, что  будет  использоваться  весь  текст  описания  персонажа.

## Examples

- **Пример 1**: Проверка валидации "банкира" с использованием правильных ожиданий.
- **Пример 2**: Проверка валидации "монаха" с использованием правильных ожиданий.
- **Пример 3**: Проверка валидации "монаха" с использованием ожиданий, предназначенных для "банкира".