## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор юнит-тестов для функций, расположенных в модуле `tinytroupe.utils`. Тесты проверяют корректность работы функций, таких как `extract_json`, `name_or_empty`, `repeat_on_error`, и `llm`.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
   - Импортируются модули `pytest`, `MagicMock`, `sys`, `unittest.mock`.
   - Добавляются пути к необходимым директориям в `sys.path`.
   - Импортируются функции из модулей `tinytroupe.utils`, `testing_utils`, `tinytroupe.utils.llm`.

2. **Тестирование функции `extract_json`**:
   - Создаются тестовые случаи с различными входными данными (простой JSON-строка, JSON-массив, строка с экранированными символами, некорректный JSON, строка без JSON).
   - Для каждого тестового случая вызывается функция `extract_json` с соответствующим текстом.
   - Проверяется результат выполнения функции с помощью `assert`. 

3. **Тестирование функции `name_or_empty`**:
   - Создается класс `MockEntity`, имитирующий объект с атрибутом `name`.
   - Вызывается функция `name_or_empty` с объектом `MockEntity`, имеющим имя, и с `None`.
   - Проверяется результат выполнения функции с помощью `assert`.

4. **Тестирование функции `repeat_on_error`**:
   - Создается класс `DummyException` для имитации исключения.
   - Создается функция `dummy_function` с помощью `MagicMock` для имитации вызова функции с побочным эффектом.
   - Вызывается функция `repeat_on_error` с различными параметрами (`retries`, `exceptions`) для проверки ее работы в случае возникновения исключения и без него.
   - Используется `pytest.raises` для проверки ожидаемых исключений.
   - Проверяется количество вызовов функции `dummy_function` с помощью `assert`. 

5. **Тестирование декоратора `llm`**:
   - Создаются тестовые функции (`joke`, `story`, `restructure`, `abstract`, `rephrase`, `is_sunny`, `pi_value`, `lucky_number`) с использованием декоратора `llm`.
   - Вызываются эти функции с различными параметрами.
   - Проверяется результат выполнения функции с помощью `assert`. 

Пример использования
-------------------------
```python
    # Тестирование функции extract_json
    text = 'Some text before {"key": "value"} some text after'
    result = extract_json(text)
    assert result == {"key": "value"}

    # Тестирование функции name_or_empty
    entity = MockEntity("Test")
    result = name_or_empty(entity)
    assert result == "Test"

    # Тестирование функции repeat_on_error
    retries = 3
    dummy_function = MagicMock(side_effect=DummyException())
    with pytest.raises(DummyException):
        @repeat_on_error(retries=retries, exceptions=[DummyException])
        def decorated_function():
            dummy_function()
        decorated_function()
    assert dummy_function.call_count == retries

    # Тестирование декоратора llm
    @llm(temperature=0.5)
    def joke():
        return "Tell me a joke."

    response = joke()
    assert isinstance(response, str)
    assert len(response) > 0
```