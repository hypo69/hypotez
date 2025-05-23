# Модуль тестирования TinyPerson

## Обзор

Этот модуль содержит юнит-тесты для проверки функциональности класса `TinyPerson`. Он проверяет различные аспекты поведения агентов, такие как действия, прослушивание, определение характеристик, взаимодействие с другими агентами и обработку стимулов.

## Подробней

Модуль тестирует создание агентов `Oscar` и `Lisa`, а также проверяет их способность выполнять различные действия и реагировать на внешние воздействия.

## Классы

В данном модуле не определены классы, но используются функции для тестирования экземпляров агентов `TinyPerson`.

## Функции

### `test_act`

```python
def test_act(setup):
    """Функция проверяет, что агент выполняет действия в ответ на запрос.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не выполняет ни одного действия, не содержит действие типа "TALK" или не завершает действия типом "DONE".

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `listen_and_act` с запросом "Tell me a bit about your life.".
    - Проверяется, что список действий не пуст, содержит действие типа "TALK" и завершается действием типа "DONE".
    """
```

### `test_listen`

```python
def test_listen(setup):
    """Функция проверяет, что агент слушает речь и обновляет свои сообщения.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не добавляет сообщения в `current_messages`, не сохраняет роль как 'user', или не сохраняет стимул типа 'CONVERSATION'.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `listen` с сообщением "Hello, how are you?".
    - Проверяется, что список `current_messages` не пуст, последнее сообщение имеет роль 'user', стимул имеет тип 'CONVERSATION' и содержимое соответствует переданному сообщению.
    """
```

### `test_define`

```python
def test_define(setup):
    """Функция проверяет, что агент определяет значение и сбрасывает свой prompt.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не устанавливает значение в `_persona`, не изменяет prompt или не включает новое значение в prompt.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента сохраняется оригинальный prompt.
    - Определяется новое значение для 'age' (25).
    - Проверяется, что значение установлено в `_persona`, prompt изменился и содержит новое значение.
    """
```

### `test_define_several`

```python
def test_define_several(setup):
    """Функция проверяет, что определение нескольких значений работает корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не добавляет указанные навыки в `_persona["skills"]`.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента определяется список навыков "skills" (Python, Machine learning, GPT-3).
    - Проверяется, что каждый навык присутствует в `_persona["skills"]`.
    """
```

### `test_socialize`

```python
def test_socialize(setup):
    """Функция проверяет, что социализация с другим агентом работает корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не выполняет ни одного действия, не содержит действие типа "TALK" или не упоминает имя другого агента.

    
    - Создаются агенты `an_oscar` и `a_lisa`.
    - Функция перебирает агентов `an_oscar` и `a_lisa`.
    - Для каждого агента определяется другой агент (если текущий `Oscar`, то другой - `Lisa`, и наоборот).
    - Агент делает другого агента доступным через метод `make_agent_accessible`.
    - Агент слушает сообщение "Hi {agent.name}, I am {other.name}.".
    - Проверяется, что список действий не пуст, содержит действие типа "TALK" и упоминает имя другого агента.
    """
```

### `test_see`

```python
def test_see(setup):
    """Функция проверяет, что агент обрабатывает визуальный стимул корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не выполняет ни одного действия, не содержит действие типа "THINK" или не упоминает увиденное.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `see` с описанием "A beautiful sunset over the ocean.".
    - Проверяется, что список действий не пуст, содержит действие типа "THINK" и упоминает увиденное (sunset).
    """
```

### `test_think`

```python
def test_think(setup):
    """Функция проверяет, что агент обрабатывает мысли корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не выполняет ни одного действия, не содержит действие типа "TALK" или не упоминает предмет размышлений.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `think` с сообщением "I will tell everyone right now how awesome life is!".
    - Проверяется, что список действий не пуст, содержит действие типа "TALK" и упоминает предмет размышлений (life).
    """
```

### `test_internalize_goal`

```python
def test_internalize_goal(setup):
    """Функция проверяет, что агент интернализирует цель корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не выполняет ни одного действия, не содержит действие типа "THINK" или не упоминает цель.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `internalize_goal` с целью "I want to compose in my head a wonderful poem about how cats are glorious creatures.".
    - Проверяется, что список действий не пуст, содержит действие типа "THINK" и упоминает предмет цели (cats).
    """
```

### `test_move_to`

```python
def test_move_to(setup):
    """Функция проверяет, что агент перемещается в новое местоположение корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не обновляет местоположение в `_mental_state` или не добавляет контекст.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `move_to` с местоположением "New York" и контекстом ["city", "busy", "diverse"].
    - Проверяется, что местоположение обновлено в `_mental_state` и контекст добавлен.
    """
```

### `test_change_context`

```python
def test_change_context(setup):
    """Функция проверяет, что изменение контекста работает корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если агент не добавляет контекст в `_mental_state`.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `change_context` с контекстом ["home", "relaxed", "comfortable"].
    - Проверяется, что контекст добавлен в `_mental_state`.
    """
```

### `test_save_specification`

```python
def test_save_specification(setup):
    """Функция проверяет, что спецификация агента сохраняется и загружается корректно.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    Raises:
        AssertionError: Если файл не сохраняется, загруженный агент имеет другое имя или конфигурацию.

    
    - Функция перебирает агентов `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
    - Для каждого агента вызывается метод `save_specification` для сохранения спецификации в файл.
    - Проверяется, что файл существует.
    - Загружается спецификация из файла с новым именем.
    - Проверяется, что имя загруженного агента отличается от оригинального, но конфигурация идентична.
    """
```

### `test_programmatic_definitions`

```python
def test_programmatic_definitions(setup):
    """Функция проверяет программное определение свойств агента.

    Args:
        setup: Параметр настройки, предоставляемый `pytest`.

    
    - Функция перебирает агентов `create_oscar_the_architect_2()` и `create_lisa_the_data_scientist_2()`.
    - Вызывает метод `listen_and_act` с запросом "Tell me a bit about your life." для каждого агента.
    """