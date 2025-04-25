# Модуль semantics

## Обзор

Модуль содержит набор функций, связанных с семантическим анализом текста. Он предоставляет возможность перефразировать текст в соответствии с заданным правилом, а также извлекать из текста элементы, связанные с нарушением или выполнением ожиданий.

## Классы

### `None`

**Описание**: Модуль не содержит классов. 

## Функции

### `rephrase`

**Назначение**: Перефразировать или изменить текст наблюдения в соответствии с заданным правилом.

**Параметры**:
- `observation` (str): Наблюдение, которое нужно перефразировать или изменить. 
- `rule` (str): Правило, которое определяет, чему должно соответствовать модифицированное наблюдение.

**Возвращает**:
- `str`: Перефразированное или модифицированное наблюдение.

**Пример**:

```python
>>> observation = "You know, I am so sad these days."
>>> rule = "I am always happy and depression is unknown to me"
>>> rephrase(observation, rule)
'You know, I am so happy these days.'
```

**Как работает**:

- Функция использует декоратор `llm()`, который передаёт тело функции в модель машинного обучения, которая выполняет перефразирование текста.

### `restructure_as_observed_vs_expected`

**Назначение**: Извлечь из текста элементы, связанные с нарушением или выполнением ожиданий. 

**Параметры**:
- `description` (str): Описание события или концепции, которое либо нарушает, либо выполняет ожидание.

**Возвращает**:
- `str`: Переструктурированное описание.

**Пример**:

```python
>>> description = "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike of spicy food."
>>> restructure_as_observed_vs_expected(description)
'OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.\nBROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho.\nREASONING: Ana has a known dislike of spicy food.'

>>> description = "Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture."
>>> restructure_as_observed_vs_expected(description)
'OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city.\nMET EXPECTATION: Carlos should have been amazed by the beauty of the city.\nREASONING: Carlos loves art and architecture.'
```

**Как работает**:

- Функция использует декоратор `llm()`, который передаёт тело функции в модель машинного обучения, которая анализирует текст и извлекает необходимые элементы.
- Модель машинного обучения определяет, нарушает ли описание событие ожиданию, или наоборот, выполняет его.
- На основе анализа текст переструктурируется, выделяя наблюдаемое событие, нарушенное или выполненное ожидание, и логическое обоснование.

## Параметры

- `llm`: Декоратор, который вызывает модель машинного обучения для обработки текста.

```python
                """
Semantic-related mechanisms.
"""
from tinytroupe.utils import llm

@llm()
def rephrase(observation, rule) -> str:
    """
    Given an observation and a rule, this function rephrases or completely changes the observation in accordance with what the rule
    specifies.


    ## Examples

        Observation: "You know, I am so sad these days."
        Rule: "I am always happy and depression is unknown to me"
        Modified observation: "You know, I am so happy these days."

    Args:
        observation: The observation that should be rephrased or changed. Something that is said or done, or a description of events or facts.
        rule: The rule that specifies what the modidfied observation should comply with.        

    Returns:
        str: The rephrased or modified observation.
    """
    # llm decorator will handle the body of this function

@llm()
def restructure_as_observed_vs_expected(description) -> str:
    """
    Given the description of something (either a real event or abstract concept), but that violates an expectation, this function 
    extracts the following elements from it:

        - OBSERVED: The observed event or statement.
        - BROKEN EXPECTATION: The expectation that was broken by the observed event.
        - REASONING: The reasoning behind the expectation that was broken.
    
    If in reality the description does not mention any expectation violation, then the function should instead extract
    the following elements:

        - OBSERVED: The observed event.
        - MET EXPECTATION: The expectation that was met by the observed event.
        - REASONING: The reasoning behind the expectation that was met.

    This way of restructuring the description can be useful for downstream processing, making it easier to analyze or
    modify system outputs, for example.

    ## Examples

        Input: "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike
                of spicy food."
        Output: 
            "OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.
             BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho.
             REASONING: Ana has a known dislike of spicy food."

             
        Input: "Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture."
        Output: 
            "OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city.
             MET EXPECTATION: Carlos should have been amazed by the beauty of the city.
             REASONING: Carlos loves art and architecture."

    Args:
        description (str): A description of an event or concept that either violates or meets an expectation.
    
    Returns:
        str: The restructured description.
    """
    # llm decorator will handle the body of this function
                ```