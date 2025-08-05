# Модуль `include.py`

## Обзор

Модуль `include.py` содержит юнит-тесты для проверки корректности импортов в проекте `hypotez`. Он проверяет доступность необходимых модулей и функций. 

## Подробнее

Этот файл расположен в папке `hypotez/src/endpoints/gpt4free/etc/unittest`. 

## Классы

### `TestImport`

**Описание**:  Класс `TestImport` - юнит-тест для проверки импортов. Наследует класс `unittest.TestCase`. 

**Атрибуты**:  
- `self`:  Ссыльа на экземпляр самого себя.


**Методы**:
- `test_get_cookies()`:  Проверяет правильность импорта функции `get_cookies` из модуля `g4f`.
- `test_requests()`: Проверяет правильность импорта класса `StreamSession` из модуля `g4f.requests`.


## Методы класса

### `test_get_cookies()`

```python
    def test_get_cookies(self):
        from g4f import get_cookies as get_cookies_alias
        from g4f.cookies import get_cookies
        self.assertEqual(get_cookies_alias, get_cookies)
```

**Назначение**: Проверяет корректность импорта функции `get_cookies` из модуля `g4f`.

**Параметры**:
- `self`: Ссылка на экземпляр самого себя.

**Возвращает**:  Нет.

**Вызывает исключения**:  Нет.

**Как работает функция**:
- Функция импортирует функцию `get_cookies`  из модуля `g4f` под именем `get_cookies_alias`.
- Затем импортируется функция `get_cookies` из модуля `g4f.cookies`.
- Используется метод `assertEqual` для сравнения импортированных функций.

**Пример**:
```python
>>> from hypotez.src.endpoints.gpt4free.etc.unittest.include import TestImport
>>> test = TestImport()
>>> test.test_get_cookies()
```

### `test_requests()`

```python
    def test_requests(self):
        from g4f.requests import StreamSession
        self.assertIsInstance(StreamSession, type)
```

**Назначение**: Проверяет правильность импорта класса `StreamSession` из модуля `g4f.requests`.

**Параметры**:
- `self`: Ссылка на экземпляр самого себя.

**Возвращает**:  Нет.

**Вызывает исключения**:  Нет.

**Как работает функция**:
- Функция импортирует класс `StreamSession` из модуля `g4f.requests`.
- Используется метод `assertIsInstance` для проверки того, является ли `StreamSession` типом.

**Пример**:
```python
>>> from hypotez.src.endpoints.gpt4free.etc.unittest.include import TestImport
>>> test = TestImport()
>>> test.test_requests()
```

## Параметры класса

## Примеры

- Запуск всех тестов:
  ```python
  python -m unittest hypotez/src/endpoints/gpt4free/etc/unittest/include.py
  ```