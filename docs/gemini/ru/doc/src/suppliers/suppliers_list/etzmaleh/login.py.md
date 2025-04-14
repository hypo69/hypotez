# Модуль `login`

## Обзор

Модуль `login` предназначен для реализации процесса авторизации поставщика Etzmaleh с использованием веб-драйвера. В текущей версии модуль содержит заглушку, которая имитирует успешную авторизацию.

## Подробней

Этот модуль является частью системы для работы с поставщиками в проекте `hypotez`. Он содержит функцию `login`, которая должна выполнять вход в систему поставщика Etzmaleh. В текущей реализации функция просто логирует сообщение об успешной авторизации и возвращает `True`.

## Функции

### `login(s: object) -> bool`

**Назначение**:
Функция `login` имитирует процесс авторизации поставщика. В текущей версии она просто логирует сообщение об успешной авторизации и возвращает `True`.

**Параметры**:
- `s` (object): Объект поставщика (Supplier), содержащий информацию, необходимую для авторизации.

**Возвращает**:
- `bool`: `True`, если авторизация прошла успешно (в текущей реализации всегда `True`).

**Как работает функция**:
1. Функция принимает объект поставщика `s`.
2. Логирует сообщение об успешной авторизации с использованием `logger.info`.
3. Всегда возвращает `True`, имитируя успешный вход.

**Примеры**:

```python
from src.suppliers.etzmaleh.login import login

class Supplier:
    def __init__(self, name):
        self.name = name

supplier = Supplier("Etzmaleh")
result = login(supplier)
print(result)  # Вывод: True
```
```python
from src.suppliers.etzmaleh.login import login

class Supplier:
    def __init__(self, name):
        self.name = name

supplier = Supplier("SomeSupplier")
result = login(supplier)
print(result)  # Вывод: True
```
```python
from src.suppliers.etzmaleh.login import login

class Supplier:
    def __init__(self, name):
        self.name = name

supplier = Supplier("AnotherSupplier")
result = login(supplier)
print(result)  # Вывод: True