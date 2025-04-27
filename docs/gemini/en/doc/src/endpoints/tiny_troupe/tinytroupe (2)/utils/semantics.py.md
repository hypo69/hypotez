# Модуль semantics.py

## Обзор

Модуль `semantics.py` предоставляет набор функций, которые работают с семантикой текста, а именно:

- `rephrase(observation, rule) -> str`: Функция перефразирует или полностью изменяет наблюдение в соответствии с заданным правилом.
- `restructure_as_observed_vs_expected(description) -> str`: Функция преобразует описание события или концепции, нарушающей или удовлетворяющей ожиданию, выделяя наблюдаемое событие, нарушенное или выполненное ожидание, а также обоснование. 

## Детали

Функции этого модуля используются для обработки текстовых данных,  в частности, для изменения смысла текста или его структурной организации. 

- **`rephrase(observation, rule) -> str`**: Эта функция позволяет перефразировать текст, используя правило. Примером может быть изменение выражения "Я очень грустный" на "Я очень счастливый", используя правило "Я всегда счастлив, и депрессия мне неизвестна".
- **`restructure_as_observed_vs_expected(description) -> str`**: Функция анализирует описание события, выявляя нарушенное или выполненное ожидание. Она выделяет наблюдаемое событие, ожидание (нарушенное или выполненное) и обоснование этого ожидания. Это позволяет структурировать текстовые данные для дальнейшей обработки. 

## Функции

### `rephrase(observation, rule) -> str`

**Описание**: Функция перефразирует или полностью изменяет наблюдение в соответствии с заданным правилом. 

**Параметры**:

- `observation`: Наблюдение, которое необходимо перефразировать или изменить. Что-то, что сказано или сделано, или описание событий или фактов.
- `rule`: Правило, которое определяет, чему должно соответствовать модифицированное наблюдение.

**Возвращаемое значение**:

- `str`: Перефразированное или измененное наблюдение.

**Примеры**:

```python
observation = "You know, I am so sad these days."
rule = "I am always happy and depression is unknown to me"
modified_observation = rephrase(observation, rule)
print(modified_observation) # Вывод: "You know, I am so happy these days."
```

### `restructure_as_observed_vs_expected(description) -> str`

**Описание**: Функция преобразует описание события или концепции, нарушающей или удовлетворяющей ожиданию, выделяя наблюдаемое событие, нарушенное или выполненное ожидание, а также обоснование. 

**Параметры**:

- `description`: Описание события или концепции, которое либо нарушает, либо соответствует ожиданию. 

**Возвращаемое значение**:

- `str`: Перестроенное описание. 

**Примеры**:

```python
description = "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike of spicy food."
restructured_description = restructure_as_observed_vs_expected(description)
print(restructured_description) 
# Вывод: 
# "OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.
#  BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho.
#  REASONING: Ana has a known dislike of spicy food."


description = "Carlos traveled to Firenzi and was amazed by the beauty of the city. This was in line with his love for art and architecture."
restructured_description = restructure_as_observed_vs_expected(description)
print(restructured_description) 
# Вывод: 
# "OBSERVED: Carlos traveled to Firenzi and was amazed by the beauty of the city.
#  MET EXPECTATION: Carlos should have been amazed by the beauty of the city.
#  REASONING: Carlos loves art and architecture."
```

## Принципы работы

Функции в этом модуле основаны на использовании декоратора `llm`, который позволяет вызывать большие языковые модели (LLM) для выполнения задач семантической обработки текста. 

- **`rephrase(observation, rule) -> str`**: Функция использует LLM для перефразирования текста, используя заданное правило.
- **`restructure_as_observed_vs_expected(description) -> str`**: Функция использует LLM для анализа текста, выявления нарушенных или выполненных ожиданий и структурирования текста в соответствии с этим.


## Дополнительные замечания

- Модуль `semantics.py` играет важную роль в проекте `hypotez`, предоставляя инструменты для обработки текстовых данных с точки зрения их семантического содержания.
- Этот модуль взаимодействует с другими модулями `hypotez` для обработки текстовых данных, таких как описания товаров, отзывов и т.д.
-  Использование LLM позволяет гибко и эффективно выполнять задачи семантической обработки текста, которые могли быть сложными для реализации с помощью традиционных алгоритмов.