# Модуль для тестирования утилит tinytroupe

## Обзор

Этот модуль содержит набор юнит-тестов для функций, расположенных в `tinytroupe/utils.py`. 
Он проверяет корректность работы функций  `name_or_empty`, `extract_json`, `repeat_on_error` и `llm`. 

## Тесты

### `test_extract_json`

**Назначение**: Проверка корректности работы функции `extract_json` для извлечения JSON-данных из текста.

**Параметры**: 

- `text` (str): Строка текста, из которой нужно извлечь JSON-данные.

**Возвращает**: 

- `dict`: Словарь с извлеченными JSON-данными.

**Пример**:

```python
text = 'Some text before {"key": "value"} some text after'
result = extract_json(text)
assert result == {"key": "value"}
```

### `test_name_or_empty`

**Назначение**: Проверка корректности работы функции `name_or_empty` для получения имени объекта или пустой строки.

**Параметры**: 

- `entity`: Объект, у которого может быть атрибут `name`.

**Возвращает**: 

- `str`: Имя объекта, если оно существует, иначе пустая строка.

**Пример**:

```python
class MockEntity:
    def __init__(self, name):
        self.name = name

entity = MockEntity("Test")
result = name_or_empty(entity)
assert result == "Test"
```

### `test_repeat_on_error`

**Назначение**: Проверка корректности работы декоратора `repeat_on_error` для повторного выполнения функции в случае ошибки.

**Параметры**: 

- `retries` (int): Количество повторов в случае ошибки.
- `exceptions` (list): Список исключений, для которых нужно выполнять повторы.

**Возвращает**: 

- `None`: Декоратор не возвращает значение.

**Пример**:

```python
class DummyException(Exception):
    pass

retries = 3
dummy_function = MagicMock(side_effect=DummyException())

with pytest.raises(DummyException):
    @repeat_on_error(retries=retries, exceptions=[DummyException])
    def decorated_function():
        dummy_function()
    decorated_function()

assert dummy_function.call_count == retries
```

### `test_llm_decorator`

**Назначение**: Проверка корректности работы декоратора `llm` для вызова функции, которая отправляет запрос в LLM (например, Google Gemini или OpenAI).

**Параметры**: 

- `temperature` (float, optional): Параметр `temperature` для LLM.

**Возвращает**: 

- `None`: Декоратор не возвращает значение.

**Пример**:

```python
@llm(temperature=0.5)
def joke():
    return "Tell me a joke."

response = joke()
assert isinstance(response, str)
assert len(response) > 0