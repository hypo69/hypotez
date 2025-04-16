# Модуль autodoc

## Обзор

Модуль содержит декоратор `autodoc`, который автоматически обновляет docstring функции, добавляя информацию о времени последнего вызова. Это полезно для отслеживания использования и времени выполнения функций в процессе разработки и отладки.

## Подробней

Модуль предоставляет функцию `autodoc`, используемую в качестве декоратора для автоматического обновления docstring функций. Также включает функцию `update_docstring`, которая добавляет информацию о времени последнего вызова функции в её docstring.

## Функции

### `autodoc`

**Назначение**: Декоратор для автоматического обновления docstring функции.

**Параметры**:
- `func` (function): Функция, для которой необходимо обновить docstring.

**Возвращает**:
- `wrapper` (function): Обернутая функция с обновленным docstring.

**Как работает функция**:
- Декоратор `autodoc` принимает функцию `func` в качестве аргумента.
- Он оборачивает функцию `func` во внутреннюю функцию `wrapper`.
- При вызове `wrapper` сначала вызывается функция `update_docstring(func)` для обновления docstring функции `func`.
- Затем вызывается сама функция `func` с переданными аргументами, и возвращается результат её выполнения.

### `update_docstring`

**Назначение**: Обновляет docstring функции, добавляя информацию о времени последнего вызова.

**Параметры**:
- `func` (function): Функция, docstring которой необходимо обновить.

**Как работает функция**:
- Функция `update_docstring` принимает функцию `func` в качестве аргумента.
- Она получает текущее время в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС".
- Проверяет, существует ли docstring у функции `func`.
  - Если docstring существует, добавляет строку с информацией о времени последнего вызова в конец docstring.
  - Если docstring не существует, создает новый docstring с информацией о времени последнего вызова.
  
**Примеры**:

```python
def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

update_docstring(example_function)
print(example_function.__doc__)
```

## Примеры

### Пример использования декоратора `autodoc`

```python
from dev_utils.autodoc import autodoc

@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

# Тестирование функции
example_function(1, "test")
print(example_function.__doc__)  # Вывод обновленного docstring
example_function(2, "another test")
print(example_function.__doc__)  # Вывод обновленного docstring