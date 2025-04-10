# Модуль для семантических операций

## Обзор

Модуль `semantics.py` предоставляет функции для работы с семантикой текста, включая перефразировку и структурирование информации об ожиданиях и наблюдениях. Он использует декоратор `@llm` для обработки запросов к большим языковым моделям (LLM).

## Подробнее

Этот модуль предназначен для обработки текста, основанного на семантических правилах. Здесь реализованы функции для перефразировки входных данных и структурирования информации об ожиданиях и наблюдениях. Модуль является частью проекта `hypotez` и используется для улучшения обработки естественного языка.

## Функции

### `rephrase`

```python
def rephrase(observation, rule) -> str:
    """
    Учитывая наблюдение и правило, эта функция перефразирует или полностью изменяет наблюдение в соответствии с тем, что указано в правиле.

    Args:
        observation: Наблюдение, которое следует перефразировать или изменить. То, что сказано или сделано, или описание событий или фактов.
        rule: Правило, определяющее, чему должно соответствовать измененное наблюдение.

    Returns:
        str: Перефразированное или измененное наблюдение.
    """
```

**Назначение**: Перефразирует или изменяет данное наблюдение в соответствии с заданным правилом.

**Параметры**:
- `observation` (str): Наблюдение, которое необходимо перефразировать или изменить.
- `rule` (str): Правило, определяющее, как должно быть изменено наблюдение.

**Возвращает**:
- `str`: Перефразированное или измененное наблюдение.

**Примеры**:

```python
observation = "You know, I am so sad these days."
rule = "I am always happy and depression is unknown to me"
modified_observation = rephrase(observation, rule)  # type: ignore
# Результат: "You know, I am so happy these days."
```

### `restructure_as_observed_vs_expected`

```python
def restructure_as_observed_vs_expected(description) -> str:
    """
    Учитывая описание чего-либо (реального события или абстрактной концепции), но которое нарушает ожидание, эта функция
    извлекает из него следующие элементы:

        - OBSERVED: Наблюдаемое событие или утверждение.
        - BROKEN EXPECTATION: Ожидание, которое было нарушено наблюдаемым событием.
        - REASONING: Обоснование ожидания, которое было нарушено.

    Если в реальности описание не упоминает какого-либо нарушения ожидания, то функция должна вместо этого извлечь
    следующие элементы:

        - OBSERVED: Наблюдаемое событие.
        - MET EXPECTATION: Ожидание, которое было выполнено наблюдаемым событием.
        - REASONING: Обоснование ожидания, которое было выполнено.

    Этот способ реструктуризации описания может быть полезен для последующей обработки, облегчая анализ или
    изменение, например, системных выводов.

    Args:
        description (str): Описание события или концепции, которое либо нарушает, либо соответствует ожиданию.

    Returns:
        str: Реструктурированное описание.
    """
```

**Назначение**: Структурирует описание события или концепции, выделяя наблюдаемые факты, ожидания и обоснования.

**Параметры**:
- `description` (str): Описание события или концепции, которое либо нарушает, либо соответствует ожиданию.

**Возвращает**:
- `str`: Реструктурированное описание, включающее наблюдаемое событие, ожидания и обоснования.

**Примеры**:

```python
description1 = "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike\nof spicy food."
restructured_description1 = restructure_as_observed_vs_expected(description1)  # type: ignore
# Результат:
# "OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.
#  BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho.
#  REASONING: Ana has a known dislike of spicy food."

description2 = "Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture."
restructured_description2 = restructure_as_observed_vs_expected(description2)  # type: ignore
# Результат:
# "OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city.
#  MET EXPECTATION: Carlos should have been amazed by the beauty of the city.
#  REASONING: Carlos loves art and architecture."