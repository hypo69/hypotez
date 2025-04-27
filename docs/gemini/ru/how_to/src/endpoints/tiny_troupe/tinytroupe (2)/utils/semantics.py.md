## Как использовать блок кода `semantics.py`
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет две функции, связанные с семантическим анализом текста: `rephrase` и `restructure_as_observed_vs_expected`.

**`rephrase`** - Эта функция принимает на вход наблюдение и правило, и модифицирует наблюдение в соответствии с этим правилом.

**`restructure_as_observed_vs_expected`** - Эта функция принимает на вход описание какого-либо события или абстрактной концепции и извлекает из него определенные элементы: наблюдаемое событие, нарушенное/выполненное ожидание и обоснование для ожидания.


Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
   - `from tinytroupe.utils import llm` - импортирует декоратор `llm`, который позволяет вызывать функции с помощью моделей больших языков. 

2. **Определение функций**:
   - **`rephrase(observation, rule)`**:
      - Принимает на вход `observation` (наблюдение) и `rule` (правило) как аргументы.
      - Использует декоратор `@llm()`, который обрабатывает тело функции с помощью модели большого языка (LLM). 
   - **`restructure_as_observed_vs_expected(description)`**:
      - Принимает на вход `description` (описание события) как аргумент.
      - Использует декоратор `@llm()`, который обрабатывает тело функции с помощью модели большого языка (LLM).

3. **Обработка тела функции**:
    - Тела функций `rephrase` и `restructure_as_observed_vs_expected` пусты, так как их логика реализована в декораторе `@llm()`.
    - Декоратор `@llm()` обрабатывает входные данные и генерирует модифицированное наблюдение или структурированное описание с помощью модели большого языка.


Пример использования
-------------------------
```python
from tinytroupe.utils import semantics

# Используем функцию rephrase
observation = "You know, I am so sad these days."
rule = "I am always happy and depression is unknown to me"
modified_observation = semantics.rephrase(observation, rule)
print(f"Modified observation: {modified_observation}")  # Выведет модифицированное наблюдение

# Используем функцию restructure_as_observed_vs_expected
description = "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike of spicy food."
restructured_description = semantics.restructure_as_observed_vs_expected(description)
print(f"Restructured description:\n{restructured_description}")  # Выведет структурированное описание
```

**Примечание:** В этом примере  функции `rephrase` и `restructure_as_observed_vs_expected` вызываются с помощью импортированного модуля `semantics`.