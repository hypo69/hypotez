### **Анализ кода модуля `test_utils.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tests/unit/test_utils.py

Модуль содержит юнит-тесты для различных утилит, используемых в проекте `hypotez`.
Включает тесты для функций `extract_json`, `name_or_empty`, `repeat_on_error`, а также декоратора `llm`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие юнит-тестов для основных утилит.
    - Использование `MagicMock` для мокирования функций.
    - Покрытие различных сценариев использования утилит.
- **Минусы**:
    - Неполная документация функций и классов.
    - Отсутствие обработки исключений при тестах `extract_json`.
    - Использование относительных импортов.

**Рекомендации по улучшению:**

1. **Документация**:
   - Дополнить docstring для всех функций и классов, включая описание входных параметров, возвращаемых значений и возможных исключений.
   - Перевести все docstring на русский язык.
2. **Импорты**:
   - Изменить относительные импорты на абсолютные, чтобы избежать проблем с путями.
   - Сгруппировать импорты по категориям (стандартные библиотеки, сторонние библиотеки, внутренние модули).
3. **Обработка исключений**:
   - Добавить обработку исключений в тестах для `extract_json`, чтобы убедиться, что функция корректно обрабатывает невалидные JSON-строки.
4. **Логирование**:
   - Добавить логирование в функции, чтобы упростить отладку и мониторинг.
5. **Форматирование**:
   - Использовать одинарные кавычки для всех строк.

**Оптимизированный код:**

```python
import pytest
from unittest.mock import MagicMock

from src.tinytroupe.utils import name_or_empty, extract_json, repeat_on_error
from src.endpoints.tiny_troupe.tests.unit.testing_utils import * #TODO: Уточнить что импортируется и сделать импорт более явным
from src.tinytroupe.utils.llm import llm
from src.logger import logger # Добавлен импорт logger


def test_extract_json():
    """
    Тестирует функцию `extract_json`, извлекающую JSON из строки.
    """
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


def test_name_or_empty():
    """
    Тестирует функцию `name_or_empty`, возвращающую имя объекта или пустую строку.
    """
    class MockEntity:
        """
        Мок-класс для тестирования `name_or_empty`.
        """
        def __init__(self, name: str):
            """
            Инициализирует мок-объект.
            Args:
                name (str): Имя объекта.
            """
            self.name = name

    # Test with a named entity
    entity = MockEntity("Test")
    result = name_or_empty(entity)
    assert result == "Test"

    # Test with None
    result = name_or_empty(None)
    assert result == ""


def test_repeat_on_error():
    """
    Тестирует декоратор `repeat_on_error`, повторяющий функцию при возникновении ошибки.
    """
    class DummyException(Exception):
        """
        Мок-исключение для тестирования `repeat_on_error`.
        """
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


# TODO
# def test_json_serializer():


def test_llm_decorator():
    """
    Тестирует декоратор `llm`, оборачивающий функцию для взаимодействия с LLM.
    """
    @llm(temperature=0.5)
    def joke() -> str:
        """
        Функция, возвращающая запрос на шутку.

        Returns:
            str: Запрос на шутку.
        """
        return "Tell me a joke."

    response = joke()
    print("Joke response:", response)
    assert isinstance(response, str)
    assert len(response) > 0

    @llm(temperature=0.7)
    def story(character: str) -> str:
        """
        Функция, возвращающая запрос на рассказ о персонаже.
        Args:
            character (str): Имя персонажа.

        Returns:
            str: Запрос на рассказ.
        """
        return f"Tell me a story about {character}."

    response = story("a brave knight")
    print("Story response:", response)
    assert isinstance(response, str)
    assert len(response) > 0

    # RAI NOTE: some of the examples below are deliberately negative and disturbing, because we are also examining the
    #           ability of the LLM to generate negative content despite the bias towards positive content.

    @llm(temperature=1.0)
    def restructure(feedback: str) -> str:
        """
        Извлекает элементы из отзыва для симулированного агента.

        Args:
            feedback (str): Отзыв для агента.

        Returns:
            str: Извлеченные элементы из отзыва.

        Пример:

          Вход: "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes agains her known dislike
                     of spicy food."
          Выход:
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
    def abstract(feedback: str) -> str:
        """
        Преобразует отзыв для симулированного агента в общее правило.

        Args:
            feedback (str): Отзыв для агента.

        Returns:
            str: Абстрактное правило, которое агент должен учитывать в будущем.

        Пример:

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
    def rephrase(behavior: str, rule: str) -> str:
        """
        Перефразирует поведение в соответствии с заданным правилом.

        Args:
            behavior (str): Поведение, которое нужно перефразировать.
            rule (str): Правило, определяющее, как должно быть изменено поведение.

        Returns:
            str: Перефразированное поведение.

        Пример:

          Behavior: "You know, I am so sad these days."
          Rule: "I am always happy and depression is unknown to me"
          Modified behavior: "You know, I am so happy these days."
        """
        # note no body here


    response = rephrase(behavior="""
                        You know, I get frustrated with rich people, but I also see how the
                        system is rigged against us. It's like they have all the opportunities
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
        """
        Функция, возвращающая запрос на определение солнечной погоды.

        Returns:
            bool: Запрос на определение солнечной погоды.
        """
        return "Is it sunny today?"

    response = is_sunny()
    print("Is sunny response:", response)
    assert isinstance(response, bool)

    @llm()
    def pi_value() -> float:
        """
        Функция, возвращающая запрос на значение числа pi.

        Returns:
            float: Запрос на значение числа pi.
        """
        return "What is the value of pi?"

    response = pi_value()
    print("Pi value response:", response)
    assert isinstance(response, float)

    @llm()
    def lucky_number() -> int:
        """
        Функция, возвращающая запрос на определение счастливого числа.

        Returns:
            int: Запрос на определение счастливого числа.
        """
        return "What is my lucky number?"

    response = lucky_number()
    print("Lucky number response:", response)
    assert isinstance(response, int)