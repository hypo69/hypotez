# Модуль тестирования импорта

## Обзор

Модуль `include.py` содержит класс `TestImport`, используемый для тестирования корректности импорта различных функций и классов из библиотеки `g4f`. В частности, проверяется, что функции и классы импортируются без ошибок и доступны под ожидаемыми именами.

## Подробней

Этот модуль важен для обеспечения стабильности и правильной работы библиотеки `g4f`. Он проверяет, что при изменении структуры библиотеки не возникают проблемы с импортом, которые могут привести к сбоям в работе других модулей или приложений, использующих `g4f`.

## Классы

### `TestImport(unittest.TestCase)`

**Описание**: Класс `TestImport` предназначен для выполнения тестов импорта. Он наследуется от `unittest.TestCase` и содержит методы для проверки корректности импорта функций и классов из библиотеки `g4f`.

**Наследует**: `unittest.TestCase`

**Атрибуты**:
- Отсутствуют.

**Методы**:
- `test_get_cookies()`: Проверяет корректность импорта функции `get_cookies` из модуля `g4f.cookies`.
- `test_requests()`: Проверяет корректность импорта класса `StreamSession` из модуля `g4f.requests`.

**Принцип работы**:
Класс `TestImport` содержит методы, которые используют `assert` для проверки, что импортированные функции и классы соответствуют ожидаемым значениям или типам. Это позволяет убедиться, что импорт работает правильно и что необходимые компоненты доступны для использования.

## Методы класса

### `test_get_cookies()`

```python
def test_get_cookies(self):
    """
    Проверяет корректность импорта функции `get_cookies` из модуля `g4f.cookies`.
    Функция проверяет, что функция `get_cookies_alias`, импортированная как псевдоним,
    совпадает с функцией `get_cookies` из модуля `g4f.cookies`.

    Args:
        self: Экземпляр класса `TestImport`.

    Returns:
        None

    Raises:
        AssertionError: Если импортированные функции не совпадают.

    Example:
        >>> test_instance = TestImport()
        >>> test_instance.test_get_cookies()
    """
```

### `test_requests()`

```python
def test_requests(self):
    """
    Проверяет корректность импорта класса `StreamSession` из модуля `g4f.requests`.
    Функция проверяет, что `StreamSession` является типом (классом).

    Args:
        self: Экземпляр класса `TestImport`.

    Returns:
        None

    Raises:
        AssertionError: Если `StreamSession` не является типом.

    Example:
        >>> test_instance = TestImport()
        >>> test_instance.test_requests()
    """
```

## Запуск тестов

В секции `if __name__ == '__main__':` вызывается `unittest.main()`, что позволяет запускать тесты, определенные в этом модуле, при его непосредственном запуске.

**Примеры**:
```python
import unittest

class TestImport(unittest.TestCase):

    def test_get_cookies(self):
        from g4f import get_cookies as get_cookies_alias
        from g4f.cookies import get_cookies
        self.assertEqual(get_cookies_alias, get_cookies)

    def test_requests(self):
        from g4f.requests import StreamSession
        self.assertIsInstance(StreamSession, type)

if __name__ == '__main__':
    unittest.main()