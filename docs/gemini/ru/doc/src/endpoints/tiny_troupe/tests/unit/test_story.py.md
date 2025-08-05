# Модуль `test_story.py`

## Обзор

Этот модуль содержит юнит-тесты для проверки работы функции `start_story` и `continue_story` класса `TinyStory` из модуля `tinytroupe.steering`.  

## Подробней

Этот модуль проверяет функциональность генерации начальной части истории и продолжения истории с помощью модели LLM. 

## Тесты

### `test_story_start`

**Описание**: Проверяет, что функция `start_story` генерирует правдоподобное начало истории, которое соответствует заданным параметрам (в данном случае, имена персонажей).

**Параметры**:

- `setup`:  Фикстура pytest, которая устанавливает начальное состояние тестового окружения.
- `focus_group_world`: Фикстура pytest, которая создает объект `World`  с заданным фокусом группы.

**Возвращает**: 

- Нет

**Вызывает исключения**:

- `AssertionError`: Если утверждение о правдоподобности начала истории не выполняется.

**Принцип работы**:

- Тест создает объект `TinyStory` с заданным миром.
- Вызывает функцию `start_story` для получения начала истории.
- Проверяет, что полученный текст соответствует заданным требованиям, используя функцию `proposition_holds`, которая проверяет утверждение на основе LLM.

**Примеры**:

```python
>>> test_story_start(setup, focus_group_world)
Story start:  Lisa, Marcos, and Oscar were sitting in a coffee shop, discussing their plans for the weekend. 
Proposition is true according to the LLM.
```


### `test_story_start_2`

**Описание**: Проверяет, что функция `start_story` генерирует правдоподобное начало истории, которое соответствует заданным параметрам (в данном случае, имена персонажей и требования к сюжету).

**Параметры**:

- `setup`:  Фикстура pytest, которая устанавливает начальное состояние тестового окружения.
- `focus_group_world`: Фикстура pytest, которая создает объект `World`  с заданным фокусом группы.

**Возвращает**: 

- Нет

**Вызывает исключения**:

- `AssertionError`: Если утверждение о правдоподобности начала истории не выполняется.

**Принцип работы**:

- Тест создает объект `TinyStory` с заданным миром.
- Вызывает функцию `start_story` с дополнительным параметром `requirements`, задавая требования к сюжету.
- Проверяет, что полученный текст соответствует заданным требованиям, используя функцию `proposition_holds`, которая проверяет утверждение на основе LLM.

**Примеры**:

```python
>>> test_story_start_2(setup, focus_group_world)
Story start:  Lisa, Marcos, and Oscar were sitting in a coffee shop, discussing their plans for the weekend. 
Proposition is true according to the LLM.
```


### `test_story_continuation`

**Описание**: Проверяет, что функция `continue_story` генерирует правдоподобное продолжение истории, которое логически связано с началом истории.

**Параметры**:

- `setup`:  Фикстура pytest, которая устанавливает начальное состояние тестового окружения.
- `focus_group_world`: Фикстура pytest, которая создает объект `World`  с заданным фокусом группы.

**Возвращает**: 

- Нет

**Вызывает исключения**:

- `AssertionError`: Если утверждение о правдоподобности продолжения истории не выполняется.

**Принцип работы**:

- Тест создает объект `World` и задает начальную часть истории.
- Вызывает функцию `continue_story` для получения продолжения истории.
- Проверяет, что полученный текст логически связан с началом истории, используя функцию `proposition_holds`, которая проверяет утверждение на основе LLM.

**Примеры**:

```python
>>> test_story_continuation(setup, focus_group_world)
Story continuation:  Zog explained that it was from a planet called Zorg, and that Zorg was much more advanced than Earth. Zorg was full of strange and wonderful things, including a talking cat who was also a scientist, and a race of aliens who had mastered the art of telepathy.  
Proposition is true according to the LLM.
```

## Функции

### `proposition_holds`

**Описание**: Проверяет утверждение на основе LLM.

**Параметры**:

- `proposition` (str): Утверждение, которое нужно проверить.

**Возвращает**:

- `bool`: `True`, если утверждение считается истинным, `False` в противном случае.

**Вызывает исключения**:

- Нет

**Принцип работы**:

- Функция использует LLM для проверки утверждения.
- Возвращает `True`, если LLM считает утверждение истинным, `False` в противном случае.