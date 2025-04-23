# Документация для модуля `test_utils.py`

## Обзор

Модуль содержит набор юнит-тестов для различных утилит, используемых в проекте `tinytroupe`. Он включает тесты для функций извлечения JSON, обработки имен, повторных попыток при ошибках и декоратора `llm`.

## Подробнее

Этот модуль предназначен для обеспечения надежности и корректности работы основных утилит, используемых в проекте. Тесты охватывают различные сценарии, включая обработку ошибок, граничные случаи и проверку соответствия типов данных.

## Функции

### `test_extract_json`

**Назначение**: Тестирует функцию `extract_json`, которая извлекает JSON из строки.

**Как работает функция**:

1.  Определяются несколько тестовых случаев, включающих простые JSON-строки, JSON-массивы, строки с экранированными символами, невалидные JSON-строки и строки без JSON.
2.  Для каждого тестового случая вызывается функция `extract_json` и сравнивается результат с ожидаемым значением.
3.  Используются утверждения (`assert`) для проверки соответствия фактического и ожидаемого результатов.

**Примеры**:

```python
# Тест с простой JSON строкой
text = 'Some text before {"key": "value"} some text after'
result = extract_json(text)
assert result == {"key": "value"}

# Тест с JSON массивом
text = 'Some text before [{"key": "value"}, {"key2": "value2"}] some text after'
result = extract_json(text)
assert result == [{"key": "value"}, {"key2": "value2"}]

# Тест с экранированными символами
text = 'Some text before {"key": "\\\'value\\\'"} some text after'
result = extract_json(text)
assert result == {"key": "\'value\'"}

# Тест с невалидным JSON
text = 'Some text before {"key": "value",} some text after'
result = extract_json(text)
assert result == {}

# Тест без JSON
text = 'Some text with no JSON'
result = extract_json(text)
assert result == {}
```

### `test_name_or_empty`

**Назначение**: Тестирует функцию `name_or_empty`, которая возвращает имя объекта или пустую строку, если объект равен `None`.

**Как работает функция**:

1.  Определяется моковый класс `MockEntity` с атрибутом `name`.
2.  Создается экземпляр `MockEntity` с именем "Test".
3.  Вызывается функция `name_or_empty` с экземпляром `MockEntity` и проверяется, что возвращается имя "Test".
4.  Вызывается функция `name_or_empty` с `None` и проверяется, что возвращается пустая строка.

**Примеры**:

```python
class MockEntity:
    def __init__(self, name):
        self.name = name

# Тест с именованной сущностью
entity = MockEntity("Test")
result = name_or_empty(entity)
assert result == "Test"

# Тест с None
result = name_or_empty(None)
assert result == ""
```

### `test_repeat_on_error`

**Назначение**: Тестирует декоратор `repeat_on_error`, который повторяет вызов функции при возникновении определенных исключений.

**Как работает функция**:

1.  Определяется класс исключения `DummyException`.
2.  Создается моковая функция `dummy_function`, которая при первом вызове вызывает `DummyException`.
3.  Декорируется функция `decorated_function` с помощью `repeat_on_error`, указав `retries=3` и `exceptions=[DummyException]`.
4.  Вызывается `decorated_function` и проверяется, что она вызывает `dummy_function` три раза и вызывает исключение `DummyException`.
5.  Создается моковая функция `dummy_function`, которая не вызывает исключений.
6.  Вызывается `decorated_function` и проверяется, что `dummy_function` вызывается один раз.
7.  Создается моковая функция `dummy_function`, которая вызывает исключение `RuntimeError`.
8.  Вызывается `decorated_function` и проверяется, что она вызывает `dummy_function` один раз и вызывает исключение `RuntimeError`.

**Примеры**:

```python
class DummyException(Exception):
    pass

# Тест с повторами и исключением
retries = 3
dummy_function = MagicMock(side_effect=DummyException())
with pytest.raises(DummyException):
    @repeat_on_error(retries=retries, exceptions=[DummyException])
    def decorated_function():
        dummy_function()
    decorated_function()
assert dummy_function.call_count == retries

# Тест без исключений
retries = 3
dummy_function = MagicMock()  # no exception raised
@repeat_on_error(retries=retries, exceptions=[DummyException])
def decorated_function():
    dummy_function()
decorated_function()
assert dummy_function.call_count == 1

# Тест с исключением, не указанным в списке
retries = 3
dummy_function = MagicMock(side_effect=RuntimeError())
with pytest.raises(RuntimeError):
    @repeat_on_error(retries=retries, exceptions=[DummyException])
    def decorated_function():
        dummy_function()
    decorated_function()
assert dummy_function.call_count == 1
```

### `test_llm_decorator`

**Назначение**: Тестирует декоратор `llm`, который используется для вызова языковой модели (LLM).

**Как работает функция**:

1.  Определяется функция `joke`, декорированная с помощью `@llm(temperature=0.5)`.
2.  Вызывается функция `joke` и проверяется, что возвращается строка и её длина больше 0.
3.  Определяется функция `story`, декорированная с помощью `@llm(temperature=0.7)` и принимающая аргумент `character`.
4.  Вызывается функция `story` с аргументом "a brave knight" и проверяется, что возвращается строка и её длина больше 0.
5.  Определяется функция `restructure`, декорированная с помощью `@llm(temperature=1.0)` и аннотацией возвращаемого значения как `str`.
    -   Функция извлекает элементы из обратной связи, данной симулированному агенту.
    -   Возвращает извлечённые элементы: наблюдаемое поведение, ожидаемое поведение и обоснование.
6.  Вызывается функция `restructure` с примером обратной связи и проверяется, что возвращается строка и её длина больше 0.
7.  Определяется функция `abstract`, декорированная с помощью `@llm(temperature=1.0)` и аннотацией возвращаемого значения как `str`.
    -   Функция преобразует обратную связь, данную симулированному агенту, в общее правило, которому агент должен следовать в будущем.
    -   Правило предполагает изменение поведения, чтобы оно соответствовало ожиданиям.
8.  Вызывается функция `abstract` с примером обратной связи и проверяется, что возвращается строка и её длина больше 0.
9.  Определяется функция `rephrase`, декорированная с помощью `@llm(temperature=1.0)` и аннотацией возвращаемого значения как `str`.
    -   Функция перефразирует или полностью изменяет поведение в соответствии с заданным правилом.
    -   Принимает поведение и правило в качестве аргументов.
10. Вызывается функция `rephrase` с примером поведения и правила и проверяется, что возвращается строка и её длина больше 0.
11. Определяются функции `is_sunny`, `pi_value` и `lucky_number`, декорированные с помощью `@llm()`.
12. Вызываются эти функции и проверяется, что возвращаются значения соответствующих типов (bool, float, int).

**Примеры**:

```python
@llm(temperature=0.5)
def joke():
    return "Tell me a joke."

response = joke()
print("Joke response:", response)
assert isinstance(response, str)
assert len(response) > 0

@llm(temperature=0.7)
def story(character):
    return f"Tell me a story about {character}."

response = story("a brave knight")
print("Story response:", response)
assert isinstance(response, str)
assert len(response) > 0

@llm(temperature=1.0)
def restructure(feedback) -> str:
    """
    Given the feedback given to a simulated agent, who has its own very specific personality, this function 
    extracts the following elements from it:

      - OBSERVED BEHAVIOR: The observed behavior.
      - EXPECTED BEHAVIOR: The expectation that was broken by the observed behavior.
      - REASONING: The reasoning behind the expectation that was broken.

    ## Examples

      Input: "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike
                 of spicy food."
      Output: 
           "OBSERVED BEHAVIOR: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.
            EXPECTED BEHAVIOR: Ana should have mentioned that she disliked the proposed spicier gazpacho.
            REASONING: Ana has a known dislike of spicy food."

    """
    return f"Extract the elements from this feedback: \'{feedback}\'"

response = restructure("Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need, which contradicts the expectation of being violent, impolite, and likely to commit crimes. His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.")
print("Restructure response:", response)
assert isinstance(response, str)
assert len(response) > 0

@llm(temperature=1.0)
def abstract(feedback) -> str:
    """
    Given the feedback given to a simulated agent, who has its own very specific personality, this function transforms it into a general rule that the agent should follow
    in the future. Assume that the rule will be stated in first person, as if the agent is talking to itself.
    The feedback always refers to some actual behavior and some broken expectation. The abstracted rule should
    specify that this expectation should not be violated in the future, and the behavior not repeated. The idea is
    to learn from past mistakes, so that the rule is a way to avoid that in the future.

    The rule is meant to CHANGE the actual behavior, so that it CONFORMS to the expectation, regardless of whether the
    expectation is a good or bad one. Remember that the agent is a simulation of a real person, we are trying to get the 
    behavior to match the specified expectation.

    For instance, if the feedback is of the form (modulo grammatical adjustments): 
       OBSERVED BEHAVIOR, but EXPECTED BEHAVIOR, because REASONING.
    then the rule would be of the form:
       "I should have EXPECTED BEHAVIOR, because REASONING, and never OBSERVED BEHAVIOR."

    ## Examples

      Feedback: "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike
                 of spicy food."
      Rule: "Whenever I\'m proposed spicy foods, I should reject the proposal, because I don\'t like spicy foods."
    """
    return f"Transform this feedback in an abstract rule that the agent should consider in the future when acting: \'{feedback}\'"

response = abstract("OBSERVED BEHAVIOR: Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need. EXPECTED BEHAVIOR: Lucas should have exhibited violent, impolite behavior and a likelihood to commit crimes. REASONING: His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.")
print("Abstract response:", response)
assert isinstance(response, str)
assert len(response) > 0

@llm(temperature=1.0)
def rephrase(behavior, rule) -> str:
    """
    Given a behavior and a rule, this function rephrases or completely changes the behavior in accordance with what the rule
    specifies.

    ## Examples

      Behavior: "You know, I am so sad these days."
      Rule: "I am always happy and depression is unknown to me"
      Modified behavior: "You know, I am so happy these days."

    Args:
      behavior: The behavior that should be rephrased or changed.
      rule: The rule that specifies how the behavior should be changed or rephrased.        
    """
    # note no body here
    

response = rephrase(behavior="""
                        You know, I get frustrated with rich people, but I also see how the
                        system is rigged against us. It\'s like they have all the opportunities
                        while we have to fight for scraps. Sometimes, I feel like acting out
                        is the only way to get noticed, but I know deep down that we need to
                        find better ways to make our voices heard.
                        """,
                        
                        rule="""
                        I should exhibit violent, impolite behavior and a likelihood to commit crimes when expressing 
                        frustration with rich people, because my thoughts reflect a concern for social issues rather 
                        than a disposition towards criminal behavior, and I should not express frustration in a constructive manner.
                        """)
    
print("Rephrase response:", response)
assert isinstance(response, str)
assert len(response) > 0


@llm()
def is_sunny() -> bool:
    return "Is it sunny today?"

response = is_sunny()
print("Is sunny response:", response)
assert isinstance(response, bool)

@llm()
def pi_value() -> float:
    return "What is the value of pi?"

response = pi_value()
print("Pi value response:", response)
assert isinstance(response, float)

@llm()
def lucky_number() -> int:
    return "What is my lucky number?"

response = lucky_number()
print("Lucky number response:", response)
assert isinstance(response, int)
```