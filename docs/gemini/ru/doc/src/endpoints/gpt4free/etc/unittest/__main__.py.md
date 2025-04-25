# Модуль unittest для gpt4free

## Обзор

Этот модуль содержит набор юнит-тестов для проверки функциональности модулей `gpt4free`. 

## Подробнее

Модуль `unittest` используется для автоматизации тестирования кода в проекте `gpt4free`. Он предоставляет фреймворк для создания и запуска тестов, а также механизмы для проверки результатов.

## Классы

### `unittest.TestCase`

**Описание**: Базовый класс для создания юнит-тестов.

**Атрибуты**:

- `maxDiff` (int): Максимальное количество различий, которое будет выведено при сравнении строк.

**Методы**:

- `assertEqual(a, b, msg=None)`: Проверяет, равны ли `a` и `b`.
- `assertNotEqual(a, b, msg=None)`: Проверяет, не равны ли `a` и `b`.
- `assertTrue(x, msg=None)`: Проверяет, истинно ли `x`.
- `assertFalse(x, msg=None)`: Проверяет, ложно ли `x`.
- `assertIsNone(x, msg=None)`: Проверяет, является ли `x` `None`.
- `assertIsNotNone(x, msg=None)`: Проверяет, не является ли `x` `None`.
- `assertIn(member, container, msg=None)`: Проверяет, содержится ли `member` в `container`.
- `assertNotIn(member, container, msg=None)`: Проверяет, не содержится ли `member` в `container`.
- `assertIs(a, b, msg=None)`: Проверяет, является ли `a` тем же объектом, что и `b`.
- `assertIsNot(a, b, msg=None)`: Проверяет, не является ли `a` тем же объектом, что и `b`.
- `assertIsInstance(obj, cls, msg=None)`: Проверяет, является ли `obj` экземпляром `cls`.
- `assertNotIsInstance(obj, cls, msg=None)`: Проверяет, не является ли `obj` экземпляром `cls`.
- `assertRaises(excType, callableObj=None, *args, **kwargs)`: Проверяет, вызывает ли вызываемый объект `callableObj` исключение типа `excType`.
- `assertRaisesRegex(excType, regex, callableObj=None, *args, **kwargs)`: Проверяет, вызывает ли вызываемый объект `callableObj` исключение типа `excType` с сообщением, соответствующим регулярному выражению `regex`.
- `assertAlmostEqual(first, second, places=None, msg=None, delta=None)`: Проверяет, почти равны ли `first` и `second` с заданной точностью.
- `assertNotAlmostEqual(first, second, places=None, msg=None, delta=None)`: Проверяет, не почти равны ли `first` и `second` с заданной точностью.
- `assertGreater(a, b, msg=None)`: Проверяет, больше ли `a`, чем `b`.
- `assertGreaterEqual(a, b, msg=None)`: Проверяет, больше или равно ли `a`, чем `b`.
- `assertLess(a, b, msg=None)`: Проверяет, меньше ли `a`, чем `b`.
- `assertLessEqual(a, b, msg=None)`: Проверяет, меньше или равно ли `a`, чем `b`.
- `assertRegex(text, regex, msg=None)`: Проверяет, соответствует ли `text` регулярному выражению `regex`.
- `assertNotRegex(text, regex, msg=None)`: Проверяет, не соответствует ли `text` регулярному выражению `regex`.
- `assertCountEqual(first, second, msg=None)`: Проверяет, одинаковое ли количество элементов в `first` и `second`, независимо от порядка.
- `assertMultiLineEqual(first, second, msg=None)`: Проверяет, идентичны ли `first` и `second` с учетом разрыва строк.
- `assertSequenceEqual(seq1, seq2, msg=None, seq_type=None)`: Проверяет, идентичны ли последовательности `seq1` и `seq2`.
- `assertListEqual(list1, list2, msg=None)`: Проверяет, идентичны ли списки `list1` и `list2`.
- `assertTupleEqual(tuple1, tuple2, msg=None)`: Проверяет, идентичны ли кортежи `tuple1` и `tuple2`.
- `assertDictEqual(dict1, dict2, msg=None)`: Проверяет, идентичны ли словари `dict1` и `dict2`.
- `assertSetEqual(set1, set2, msg=None)`: Проверяет, идентичны ли множества `set1` и `set2`.
- `assertItemsEqual(seq1, seq2, msg=None)`: Проверяет, одинаковы ли элементы в `seq1` и `seq2`, независимо от порядка.

## Функции

### `unittest.main()`

**Назначение**: Запускает тесты в текущем модуле.

**Параметры**:

- `argv`: Список аргументов командной строки.
- `exit`: Если `True`, программа завершается после запуска тестов.
- `verbosity`: Уровень подробности вывода.
- `failfast`: Если `True`, тесты завершаются при первой неудаче.
- `buffer`: Если `True`, вывод буферизуется.
- `catchbreak`: Если `True`, отлавливает исключения `KeyboardInterrupt`.
- `warnings`: Конфигурация предупреждений.
- `module`: Модуль, который нужно тестировать.
- `defaultTest`: Имя теста по умолчанию.
- `testRunner`: Класс тестового прогона.
- `testLoader`: Загрузчик тестов.
- `exitfunc`: Функция, которая вызывается при завершении программы.

**Возвращает**:

- `None`

**Примеры**:

```python
import unittest

# Запуск всех тестов в текущем модуле
unittest.main()

# Запуск тестов с уровнем подробности 2
unittest.main(verbosity=2)

# Запуск тестов с опцией failfast
unittest.main(failfast=True)
```

## Параметры

- `argv`: Список аргументов командной строки.
- `exit`: Если `True`, программа завершается после запуска тестов.
- `verbosity`: Уровень подробности вывода.
- `failfast`: Если `True`, тесты завершаются при первой неудаче.
- `buffer`: Если `True`, вывод буферизуется.
- `catchbreak`: Если `True`, отлавливает исключения `KeyboardInterrupt`.
- `warnings`: Конфигурация предупреждений.
- `module`: Модуль, который нужно тестировать.
- `defaultTest`: Имя теста по умолчанию.
- `testRunner`: Класс тестового прогона.
- `testLoader`: Загрузчик тестов.
- `exitfunc`: Функция, которая вызывается при завершении программы.

## Примеры

```python
import unittest

class TestMyClass(unittest.TestCase):

    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_subtract(self):
        self.assertEqual(3 - 1, 2)

if __name__ == '__main__':
    unittest.main()