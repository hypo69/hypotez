### Как использовать блок кода `test_extract_json`
=========================================================================================

Описание
-------------------------
`test_extract_json` — это функция тестирования, предназначенная для проверки корректности извлечения JSON-объектов из текстовых строк. Функция проверяет различные сценарии, включая извлечение простых JSON-объектов, массивов JSON, объектов с экранированными символами, некорректных JSON-объектов и ситуаций, когда JSON отсутствует.

Шаги выполнения
-------------------------
1. Определяются несколько тестовых случаев:
   - Строка с простым JSON-объектом.
   - Строка с JSON-массивом.
   - Строка с экранированными символами в JSON.
   - Строка с некорректным JSON (например, с висячей запятой).
   - Строка без JSON.
2. Для каждого тестового случая вызывается функция `extract_json` с соответствующей строкой.
3. Утверждается, что возвращаемое значение `extract_json` соответствует ожидаемому результату для каждого случая.

Пример использования
-------------------------

```python
def test_extract_json():
    # Test with a simple JSON string
    text = 'Some text before {"key": "value"} some text after'
    result = extract_json(text)
    assert result == {"key": "value"}

    # Test with a JSON array
    text = 'Some text before [{"key": "value"}, {"key2": "value2"}] some text after'
    result = extract_json(text)
    assert result == [{"key": "value"}, {"key2": "value2"}]

    # Test with escaped characters
    text = 'Some text before {"key": "\\\'value\\\'"} some text after'
    result = extract_json(text)
    assert result == {"key": "\'value\'"}

    # Test with invalid JSON
    text = 'Some text before {"key": "value",} some text after'
    result = extract_json(text)
    assert result == {}

    # Test with no JSON
    text = 'Some text with no JSON'
    result = extract_json(text)
    assert result == {}
```
### Как использовать блок кода `test_name_or_empty`
=========================================================================================

Описание
-------------------------
`test_name_or_empty` — это функция тестирования, предназначенная для проверки функции `name_or_empty`, которая извлекает имя из объекта, если оно существует, или возвращает пустую строку, если объект равен `None`.

Шаги выполнения
-------------------------
1. Определяется класс `MockEntity` с атрибутом `name`.
2. Создается экземпляр `MockEntity` с заданным именем.
3. Вызывается функция `name_or_empty` с экземпляром `MockEntity`.
4. Утверждается, что возвращаемое значение соответствует имени, заданному при создании экземпляра `MockEntity`.
5. Вызывается функция `name_or_empty` со значением `None`.
6. Утверждается, что возвращаемое значение является пустой строкой.

Пример использования
-------------------------

```python
def test_name_or_empty():
    class MockEntity:
        def __init__(self, name):
            self.name = name

    # Test with a named entity
    entity = MockEntity("Test")
    result = name_or_empty(entity)
    assert result == "Test"

    # Test with None
    result = name_or_empty(None)
    assert result == ""
```
### Как использовать блок кода `test_repeat_on_error`
=========================================================================================

Описание
-------------------------
`test_repeat_on_error` — это функция тестирования, предназначенная для проверки декоратора `repeat_on_error`, который позволяет повторно выполнять функцию заданное количество раз, если возникает определенное исключение.

Шаги выполнения
-------------------------
1. Определяется класс исключения `DummyException`.
2. Тестируется сценарий, когда исключение возникает и функция повторяется заданное количество раз:
   - Устанавливается количество повторных попыток (`retries`).
   - Создается мок-объект функции (`dummy_function`), который вызывает `DummyException`.
   - Декорируется функция `decorated_function` с помощью `repeat_on_error`, указывая количество повторных попыток и тип исключения (`DummyException`).
   - Вызывается `decorated_function`, и проверяется, что возникает `DummyException`.
   - Утверждается, что мок-объект функции был вызван `retries` раз.
3. Тестируется сценарий, когда исключение не возникает:
   - Устанавливается количество повторных попыток (`retries`).
   - Создается мок-объект функции (`dummy_function`), который не вызывает исключение.
   - Декорируется функция `decorated_function` с помощью `repeat_on_error`, указывая количество повторных попыток и тип исключения (`DummyException`).
   - Вызывается `decorated_function`.
   - Утверждается, что мок-объект функции был вызван только один раз.
4. Тестируется сценарий, когда возникает исключение, которое не указано в списке разрешенных для повтора исключений:
   - Устанавливается количество повторных попыток (`retries`).
   - Создается мок-объект функции (`dummy_function`), который вызывает `RuntimeError`.
   - Декорируется функция `decorated_function` с помощью `repeat_on_error`, указывая количество повторных попыток и тип исключения (`DummyException`).
   - Вызывается `decorated_function`, и проверяется, что возникает `RuntimeError`.
   - Утверждается, что мок-объект функции был вызван только один раз.

Пример использования
-------------------------

```python
def test_repeat_on_error():
    class DummyException(Exception):
        pass

    # Test with retries and an exception occurring
    retries = 3
    dummy_function = MagicMock(side_effect=DummyException())
    with pytest.raises(DummyException):
        @repeat_on_error(retries=retries, exceptions=[DummyException])
        def decorated_function():
            dummy_function()
        decorated_function()
    assert dummy_function.call_count == retries

    # Test without any exception occurring
    retries = 3
    dummy_function = MagicMock()  # no exception raised
    @repeat_on_error(retries=retries, exceptions=[DummyException])
    def decorated_function():
        dummy_function()
    decorated_function()
    assert dummy_function.call_count == 1

    # Test with an exception that is not specified in the exceptions list
    retries = 3
    dummy_function = MagicMock(side_effect=RuntimeError())
    with pytest.raises(RuntimeError):
        @repeat_on_error(retries=retries, exceptions=[DummyException])
        def decorated_function():
            dummy_function()
        decorated_function()
    assert dummy_function.call_count == 1
```
### Как использовать блок кода `test_llm_decorator`
=========================================================================================

Описание
-------------------------
`test_llm_decorator` — это функция тестирования, предназначенная для проверки декоратора `llm`, который оборачивает функцию и, предположительно, взаимодействует с какой-то языковой моделью (LLM). Функция тестирует различные сценарии использования декоратора, включая передачу параметров, определение возвращаемых типов и обработку различных входных данных.

Шаги выполнения
-------------------------
1. Определяется функция `joke`, декорированная с помощью `@llm(temperature=0.5)`. Функция возвращает текстовый запрос.
2. Вызывается декорированная функция `joke`, и проверяется, что возвращаемое значение является строкой и имеет ненулевую длину.
3. Определяется функция `story`, декорированная с помощью `@llm(temperature=0.7)`. Функция принимает параметр `character` и возвращает текстовый запрос.
4. Вызывается декорированная функция `story` с аргументом "a brave knight", и проверяется, что возвращаемое значение является строкой и имеет ненулевую длину.
5. Определяется функция `restructure`, декорированная с помощью `@llm(temperature=1.0)`. Функция принимает параметр `feedback` и возвращает текстовый запрос с инструкциями по извлечению элементов из обратной связи.
6. Вызывается декорированная функция `restructure` с примером обратной связи, и проверяется, что возвращаемое значение является строкой и имеет ненулевую длину.
7. Определяется функция `abstract`, декорированная с помощью `@llm(temperature=1.0)`. Функция принимает параметр `feedback` и возвращает текстовый запрос с инструкциями по преобразованию обратной связи в абстрактное правило.
8. Вызывается декорированная функция `abstract` с примером обратной связи, и проверяется, что возвращаемое значение является строкой и имеет ненулевую длину.
9. Определяется функция `rephrase`, декорированная с помощью `@llm(temperature=1.0)`. Функция принимает параметры `behavior` и `rule` и возвращает текстовый запрос с инструкциями по перефразировке поведения в соответствии с правилом.
10. Вызывается декорированная функция `rephrase` с примерами поведения и правила, и проверяется, что возвращаемое значение является строкой и имеет ненулевую длину.
11. Определяется функция `is_sunny`, декорированная с помощью `@llm()`. Функция возвращает текстовый вопрос.
12. Вызывается декорированная функция `is_sunny`, и проверяется, что возвращаемое значение является булевым значением.
13. Определяется функция `pi_value`, декорированная с помощью `@llm()`. Функция возвращает текстовый вопрос.
14. Вызывается декорированная функция `pi_value`, и проверяется, что возвращаемое значение является числом с плавающей точкой.
15. Определяется функция `lucky_number`, декорированная с помощью `@llm()`. Функция возвращает текстовый вопрос.
16. Вызывается декорированная функция `lucky_number`, и проверяется, что возвращаемое значение является целым числом.

Пример использования
-------------------------

```python
def test_llm_decorator():
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
        return f"Extract the elements from this feedback: '{feedback}'"

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
          Rule: "Whenever I'm proposed spicy foods, I should reject the proposal, because I don't like spicy foods."
        """
        return f"Transform this feedback in an abstract rule that the agent should consider in the future when acting: '{feedback}'"

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
        

    response = rephrase(behavior=\
                        """
                        You know, I get frustrated with rich people, but I also see how the
                        system is rigged against us. It's like they have all the opportunities
                        while we have to fight for scraps. Sometimes, I feel like acting out
                        is the only way to get noticed, but I know deep down that we need to
                        find better ways to make our voices heard.
                        """,
                        
                        rule=\
                        """
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