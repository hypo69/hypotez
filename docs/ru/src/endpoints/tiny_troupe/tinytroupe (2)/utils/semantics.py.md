# Модуль для работы с семантикой
## \file hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/utils/semantics.py

Модуль содержит функции для семантической обработки текста, включая перефразировку и реструктуризацию.
Он использует декоратор `@llm()` для обработки функций, связанных с языковой моделью.

## Обзор

Модуль предоставляет функции для работы с семантикой текста, такие как перефразировка и реструктуризация.

## Подробнее

Этот модуль содержит функции для обработки текста с использованием языковой модели. Он включает в себя функции для перефразировки текста в соответствии с заданными правилами и реструктуризации описаний событий для анализа соответствия ожиданиям. Декоратор `@llm()` используется для автоматической обработки этих функций с использованием языковой модели.

## Функции

### `rephrase`

```python
@llm()
def rephrase(observation: str, rule: str) -> str:
    """ Функция перефразирует наблюдение в соответствии с заданным правилом.

    Args:
        observation (str): Наблюдение, которое необходимо перефразировать или изменить. Описание событий или фактов.
        rule (str): Правило, определяющее, как должно быть изменено наблюдение.

    Returns:
        str: Перефразированное или измененное наблюдение.

    Примеры:
        >>> rephrase("You know, I am so sad these days.", "I am always happy and depression is unknown to me")
        "You know, I am so happy these days."
    """
```

**Назначение**: Перефразировка или изменение наблюдения в соответствии с заданным правилом.

**Параметры**:
- `observation` (str): Наблюдение, которое необходимо перефразировать или изменить. Это может быть описание событий или фактов.
- `rule` (str): Правило, определяющее, как должно быть изменено наблюдение.

**Возвращает**:
- `str`: Перефразированное или измененное наблюдение.

**Как работает функция**:
Функция принимает наблюдение и правило, после чего перефразирует или изменяет наблюдение в соответствии с указанным правилом.  Фактическое выполнение функции обрабатывается декоратором `@llm()`.

**Примеры**:

Пример 1:

```python
observation = "You know, I am so sad these days."
rule = "I am always happy and depression is unknown to me"
rephrased_observation = rephrase(observation, rule)
print(rephrased_observation) #  "You know, I am so happy these days."
```

### `restructure_as_observed_vs_expected`

```python
@llm()
def restructure_as_observed_vs_expected(description: str) -> str:
    """ Функция реструктурирует описание события, выделяя наблюдение, ожидание и рассуждение.

    Args:
        description (str): Описание события или концепции, которое либо нарушает, либо соответствует ожиданию.

    Returns:
        str: Реструктурированное описание.

    Примеры:
        >>> restructure_as_observed_vs_expected("Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike of spicy food.")
        "OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.
         BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho.
         REASONING: Ana has a known dislike of spicy food."

        >>> restructure_as_observed_vs_expected("Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture.")
        "OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city.
         MET EXPECTATION: Carlos should have been amazed by the beauty of the city.
         REASONING: Carlos loves art and architecture."
    """
```

**Назначение**: Реструктуризация описания события или концепции, чтобы выделить наблюдение, ожидание (выполненное или нарушенное) и рассуждение.

**Параметры**:
- `description` (str): Описание события или концепции, которое либо нарушает, либо соответствует ожиданию.

**Возвращает**:
- `str`: Реструктурированное описание, содержащее элементы "OBSERVED", "BROKEN EXPECTATION" (или "MET EXPECTATION") и "REASONING".

**Как работает функция**:
Функция принимает описание события и анализирует, соответствует ли оно ожиданиям. Если ожидание нарушено, функция выделяет наблюдение, нарушенное ожидание и рассуждение, объясняющее, почему ожидание было нарушено. Если ожидание выполнено, функция выделяет наблюдение, выполненное ожидание и рассуждение, объясняющее, почему ожидание было выполнено.  Фактическое выполнение функции обрабатывается декоратором `@llm()`.

**Примеры**:

Пример 1: Нарушенное ожидание
```python
description = "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike of spicy food."
restructured_description = restructure_as_observed_vs_expected(description)
print(restructured_description)
# "OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.
#  BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho.
#  REASONING: Ana has a known dislike of spicy food."
```

Пример 2: Выполненное ожидание
```python
description = "Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture."
restructured_description = restructure_as_observed_vs_expected(description)
print(restructured_description)
# "OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city.
#  MET EXPECTATION: Carlos should have been amazed by the beauty of the city.
#  REASONING: Carlos loves art and architecture."