# Модуль semantic.py

## Обзор

Модуль `semantic.py` предоставляет механизмы, связанные с семантическим анализом текста. Он содержит функции для перефразировки текста и реструктуризации описаний событий, основываясь на ожиданиях. Для работы с языковыми моделями (LLM) используется декоратор `@llm` из модуля `tinytroupe.utils`.

## Подробнее

Этот модуль предназначен для обработки и анализа текста с использованием языковых моделей. Он позволяет изменять и структурировать текст в соответствии с заданными правилами и ожиданиями, что может быть полезно для различных задач, таких как анализ тональности, извлечение информации и модификация системных выводов.

## Функции

### `rephrase`

```python
@llm()
def rephrase(observation, rule) -> str:
    """
    Перефразирует или полностью изменяет наблюдение в соответствии с заданным правилом.

    Args:
        observation (str): Наблюдение, которое нужно перефразировать или изменить. Это может быть описание события или факта.
        rule (str): Правило, определяющее, как должно быть изменено наблюдение.

    Returns:
        str: Перефразированное или измененное наблюдение.

    Примеры:
        >>> rephrase("You know, I am so sad these days.", "I am always happy and depression is unknown to me")
        "You know, I am so happy these days."
    """
    # llm decorator will handle the body of this function
```

**Назначение**: Функция `rephrase` принимает наблюдение и правило, после чего перефразирует или полностью изменяет предоставленное наблюдение, основываясь на указанном правиле.

**Параметры**:
- `observation` (str): Наблюдение для перефразировки. Представляет собой описание событий или фактов.
- `rule` (str): Правило, которое определяет, как необходимо изменить исходное наблюдение.

**Возвращает**:
- `str`: Перефразированное или модифицированное наблюдение.

**Как работает функция**:
- Функция `rephrase` использует декоратор `@llm()`, который обрабатывает тело функции и выполняет взаимодействие с языковой моделью.

**Примеры**:

```python
>>> rephrase("You know, I am so sad these days.", "I am always happy and depression is unknown to me")
"You know, I am so happy these days."
```

### `restructure_as_observed_vs_expected`

```python
@llm()
def restructure_as_observed_vs_expected(description) -> str:
    """
    Извлекает элементы из описания события или концепции, которые либо нарушают, либо соответствуют ожиданиям.

    Args:
        description (str): Описание события или концепции, которое либо нарушает, либо соответствует ожиданию.

    Returns:
        str: Реструктурированное описание.

    Примеры:
        >>> restructure_as_observed_vs_expected("Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike of spicy food.")
        "OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho. REASONING: Ana has a known dislike of spicy food."
        >>> restructure_as_observed_vs_expected("Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture.")
        "OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city. MET EXPECTATION: Carlos should have been amazed by the beauty of the city. REASONING: Carlos loves art and architecture."
    """
    # llm decorator will handle the body of this function
```

**Назначение**: Функция `restructure_as_observed_vs_expected` принимает описание события или концепции и реструктурирует его, выделяя элементы, связанные с нарушенными или оправдавшимися ожиданиями.

**Параметры**:
- `description` (str): Описание события или концепции.

**Возвращает**:
- `str`: Реструктурированное описание, содержащее информацию об OBSERVED, BROKEN EXPECTATION/MET EXPECTATION и REASONING.

**Как работает функция**:
- Функция `restructure_as_observed_vs_expected` использует декоратор `@llm()`, чтобы делегировать обработку текста языковой модели. В зависимости от того, нарушает ли описание ожидания или нет, функция извлекает соответствующие элементы:
    - Если ожидания нарушены, извлекаются OBSERVED, BROKEN EXPECTATION и REASONING.
    - Если ожидания оправданы, извлекаются OBSERVED, MET EXPECTATION и REASONING.

**Примеры**:

```python
>>> restructure_as_observed_vs_expected("Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike of spicy food.")
"OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho. REASONING: Ana has a known dislike of spicy food."
>>> restructure_as_observed_vs_expected("Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture.")
"OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city. MET EXPECTATION: Carlos should have been amazed by the beauty of the city. REASONING: Carlos loves art and architecture."