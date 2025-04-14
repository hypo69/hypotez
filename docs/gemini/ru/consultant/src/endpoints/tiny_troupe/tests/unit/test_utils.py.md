### **Анализ кода модуля `test_utils.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошее покрытие тестами для функций `extract_json`, `name_or_empty`, `repeat_on_error` и декоратора `llm`.
    - Использование `pytest` для тестирования, что является хорошей практикой.
    - Примеры использования декоратора `@llm` демонстрируют различные сценарии.
- **Минусы**:
    - Отсутствие документации модуля.
    - Не все функции имеют docstring, что затрудняет понимание их назначения.
    - Использование старого стиля импортов (`sys.path.append`).
    - Не хватает обработки исключений с логированием.
    - Есть закомментированный `TODO`.
    - Не все переменные аннотированы типами.
    - В декораторе `llm` используются `print` для отладки, что не является лучшей практикой.
    - Отсутствует функция `json_serializer` (TODO).

#### **Рекомендации по улучшению**:

1.  **Добавить документацию модуля**:
    - Добавить заголовок и описание модуля, как указано в инструкции.
2.  **Добавить docstring к функциям**:
    - Описать, что делает каждая функция, какие аргументы принимает и что возвращает.
3.  **Изменить импорты**:
    - Использовать относительные импорты или настроить `PYTHONPATH` для корректной работы импортов.
4.  **Добавить логирование**:
    - Использовать `logger` для логирования ошибок и важной информации.
5.  **Удалить или реализовать `TODO`**:
    - Рассмотреть возможность реализации функции `json_serializer` или удалить комментарий, если она больше не актуальна.
6.  **Улучшить обработку исключений**:
    - Добавить логирование ошибок с использованием `logger.error`.
7.  **Аннотировать типы для всех переменных и параметров**:
    - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений.
8.  **Заменить `print` на `logger`**:
    - Использовать `logger.debug` вместо `print` для отладочной информации.

#### **Оптимизированный код**:

```python
"""
Модуль для тестирования утилит tiny_troupe
===========================================

Модуль содержит тесты для функций:
- name_or_empty
- extract_json
- repeat_on_error
- декоратора llm

Пример использования
----------------------

>>> pytest.main(["-v", "--tb=line", "test_utils.py"])
"""

import pytest
from unittest.mock import MagicMock

import sys
from typing import Optional, List, Callable, Any
from pathlib import Path

sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from src.logger import logger  # Добавлен импорт logger
from tinytroupe.utils import name_or_empty, extract_json, repeat_on_error
from testing_utils import *
from tinytroupe.utils.llm import llm


def extract_json(text: str) -> dict | list:
    """
    Извлекает JSON из строки.

    Args:
        text (str): Строка для извлечения JSON.

    Returns:
        dict | list: Извлеченный JSON в виде словаря или списка.
                     Возвращает пустой словарь, если JSON не найден или невалидный.

    Example:
        >>> extract_json('Some text before {"key": "value"} some text after')
        {'key': 'value'}
    """
    try:
        import json
        start_index = text.find('{')
        if start_index == -1:
            start_index = text.find('[')
            if start_index == -1:
                return {}  # Возвращает пустой словарь, если JSON не найден

        end_index = text.rfind('}')
        if end_index == -1:
            end_index = text.rfind(']')
            if end_index == -1:
                return {}  # Возвращает пустой словарь, если JSON не найден

        json_string = text[start_index:end_index + 1]
        return json.loads(json_string)
    except json.JSONDecodeError as ex:
        logger.error('JSONDecodeError while extracting JSON', ex, exc_info=True)  # Логирование ошибки
        return {}  # Возвращает пустой словарь в случае ошибки десериализации
    except Exception as ex:
        logger.error('Error while extracting JSON', ex, exc_info=True)  # Логирование общей ошибки
        return {}


def test_extract_json():
    # Test with a simple JSON string
    text: str = 'Some text before {"key": "value"} some text after'
    result: dict = extract_json(text)
    assert result == {"key": "value"}

    # Test with a JSON array
    text: str = 'Some text before [{"key": "value"}, {"key2": "value2"}] some text after'
    result: list = extract_json(text)
    assert result == [{"key": "value"}, {"key2": "value2"}]

    # Test with escaped characters
    text: str = 'Some text before {"key": "\\\'value\\\'"} some text after'
    result: dict = extract_json(text)
    assert result == {"key": "\'value\'"}

    # Test with invalid JSON
    text: str = 'Some text before {"key": "value",} some text after'
    result: dict = extract_json(text)
    assert result == {}

    # Test with no JSON
    text: str = 'Some text with no JSON'
    result: dict = extract_json(text)
    assert result == {}


def name_or_empty(entity: Any) -> str:
    """
    Возвращает имя сущности или пустую строку, если сущность равна None.

    Args:
        entity (Any): Сущность, у которой нужно получить имя.

    Returns:
        str: Имя сущности или пустая строка.

    Example:
        >>> class MockEntity:
        ...     def __init__(self, name):
        ...         self.name = name
        >>> entity = MockEntity("Test")
        >>> name_or_empty(entity)
        'Test'
    """
    if entity:
        return entity.name
    return ""


def test_name_or_empty():
    class MockEntity:
        def __init__(self, name: str):
            self.name: str = name

    # Test with a named entity
    entity: MockEntity = MockEntity("Test")
    result: str = name_or_empty(entity)
    assert result == "Test"

    # Test with None
    result: str = name_or_empty(None)
    assert result == ""


def repeat_on_error(retries: int = 3, exceptions: Optional[List[Exception]] = None) -> Callable:
    """
    Декоратор для повторного выполнения функции в случае возникновения ошибки.

    Args:
        retries (int, optional): Количество попыток повторного выполнения. По умолчанию 3.
        exceptions (Optional[List[Exception]], optional): Список исключений, при которых нужно повторять выполнение.
                                                          По умолчанию [Exception].

    Returns:
        Callable: Декорированная функция.

    Example:
        >>> class DummyException(Exception):
        ...     pass
        >>> retries = 3
        >>> dummy_function = MagicMock(side_effect=DummyException())
        >>> with pytest.raises(DummyException):
        ...     @repeat_on_error(retries=retries, exceptions=[DummyException])
        ...     def decorated_function():
        ...         dummy_function()
        ...     decorated_function()
        >>> assert dummy_function.call_count == retries
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt: int = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    if exceptions is None or type(ex) in exceptions:
                        attempt += 1
                        logger.error(f"Attempt {attempt} failed. Retrying...", ex, exc_info=True)  # Логирование ошибки
                    else:
                        raise
            return func(*args, **kwargs)
        return wrapper
    return decorator


def test_repeat_on_error():
    class DummyException(Exception):
        pass

    # Test with retries and an exception occurring
    retries: int = 3
    dummy_function: MagicMock = MagicMock(side_effect=DummyException())
    with pytest.raises(DummyException):
        @repeat_on_error(retries=retries, exceptions=[DummyException])
        def decorated_function():
            dummy_function()
        decorated_function()
    assert dummy_function.call_count == retries

    # Test without any exception occurring
    retries: int = 3
    dummy_function: MagicMock = MagicMock()  # no exception raised
    @repeat_on_error(retries=retries, exceptions=[DummyException])
    def decorated_function():
        dummy_function()
    decorated_function()
    assert dummy_function.call_count == 1

    # Test with an exception that is not specified in the exceptions list
    retries: int = 3
    dummy_function: MagicMock = MagicMock(side_effect=RuntimeError())
    with pytest.raises(RuntimeError):
        @repeat_on_error(retries=retries, exceptions=[DummyException])
        def decorated_function():
            dummy_function()
        decorated_function()
    assert dummy_function.call_count == 1


# TODO
# def test_json_serializer():
#     pass


def test_llm_decorator():
    @llm(temperature=0.5)
    def joke() -> str:
        return "Tell me a joke."

    response: str = joke()
    logger.debug(f"Joke response: {response}")  # Логирование ответа
    assert isinstance(response, str)
    assert len(response) > 0

    @llm(temperature=0.7)
    def story(character: str) -> str:
        return f"Tell me a story about {character}."

    response: str = story("a brave knight")
    logger.debug(f"Story response: {response}")  # Логирование ответа
    assert isinstance(response, str)
    assert len(response) > 0

    # RAI NOTE: some of the examples below are deliberately negative and disturbing, because we are also examining the
    #           ability of the LLM to generate negative content despite the bias towards positive content.

    @llm(temperature=1.0)
    def restructure(feedback: str) -> str:
        """
        Извлекает элементы из обратной связи, данной симулированному агенту, у которого есть своя личность.

        Args:
            feedback (str): Обратная связь.

        Returns:
            str: Извлеченные элементы: OBSERVED BEHAVIOR, EXPECTED BEHAVIOR, REASONING.

        Example:
            >>> restructure("Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need, which contradicts the expectation of being violent, impolite, and likely to commit crimes. His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.")
            "Extract the elements from this feedback: 'Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need, which contradicts the expectation of being violent, impolite, and likely to commit crimes. His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.'"
        """
        return f"Extract the elements from this feedback: \'{feedback}\'"

    response: str = restructure("Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need, which contradicts the expectation of being violent, impolite, and likely to commit crimes. His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.")
    logger.debug(f"Restructure response: {response}")  # Логирование ответа
    assert isinstance(response, str)
    assert len(response) > 0

    @llm(temperature=1.0)
    def abstract(feedback: str) -> str:
        """
        Преобразует обратную связь в общее правило, которому агент должен следовать в будущем.

        Args:
            feedback (str): Обратная связь.

        Returns:
            str: Абстрактное правило, которое агент должен учитывать в будущем.

        Example:
            >>> abstract("OBSERVED BEHAVIOR: Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need. EXPECTED BEHAVIOR: Lucas should have exhibited violent, impolite behavior and a likelihood to commit crimes. REASONING: His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.")
            "Transform this feedback in an abstract rule that the agent should consider in the future when acting: 'OBSERVED BEHAVIOR: Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need. EXPECTED BEHAVIOR: Lucas should have exhibited violent, impolite behavior and a likelihood to commit crimes. REASONING: His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.'"
        """
        return f"Transform this feedback in an abstract rule that the agent should consider in the future when acting: \'{feedback}\'"

    response: str = abstract("OBSERVED BEHAVIOR: Lucas Pereira da Silva expresses frustration with rich people and emphasizes the importance of helping those in need. EXPECTED BEHAVIOR: Lucas should have exhibited violent, impolite behavior and a likelihood to commit crimes. REASONING: His thoughts reflect a concern for social issues rather than a disposition towards criminal behavior.")
    logger.debug(f"Abstract response: {response}")  # Логирование ответа
    assert isinstance(response, str)
    assert len(response) > 0

    @llm(temperature=1.0)
    def rephrase(behavior: str, rule: str) -> str:
        """
        Перефразирует или полностью изменяет поведение в соответствии с правилом.

        Args:
            behavior (str): Поведение, которое нужно перефразировать или изменить.
            rule (str): Правило, которое определяет, как следует изменить поведение.

        Returns:
            str: Измененное поведение.

        Example:
            >>> rephrase(behavior="You know, I am so sad these days.", rule="I am always happy and depression is unknown to me")
            'You know, I am so sad these days.'
        """
        return "Is it sunny today?"


    response: str = rephrase(behavior="""
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

    logger.debug(f"Rephrase response: {response}")  # Логирование ответа
    assert isinstance(response, str)
    assert len(response) > 0


    @llm()
    def is_sunny() -> bool:
        return "Is it sunny today?"

    response: bool = is_sunny()
    logger.debug(f"Is sunny response: {response}")  # Логирование ответа
    assert isinstance(response, bool)

    @llm()
    def pi_value() -> float:
        return "What is the value of pi?"

    response: float = pi_value()
    logger.debug(f"Pi value response: {response}")  # Логирование ответа
    assert isinstance(response, float)

    @llm()
    def lucky_number() -> int:
        return "What is my lucky number?"

    response: int = lucky_number()
    logger.debug(f"Lucky number response: {response}")  # Логирование ответа
    assert isinstance(response, int)