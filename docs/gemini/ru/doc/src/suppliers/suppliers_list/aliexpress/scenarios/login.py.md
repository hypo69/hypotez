# Модуль входа на AliExpress

## Обзор

Этот модуль содержит функцию `login`, которая реализует логин на платформу AliExpress через WebDriver. 

## Функции

### `login(s: Supplier) -> bool`

**Назначение**: Функция выполняет вход на AliExpress с использованием WebDriver. 

**Параметры**:

- `s` (`Supplier`): Экземпляр класса `Supplier` с запущенным WebDriver.

**Возвращает**:

- `bool`: `True`, если вход выполнен успешно, `False` в случае ошибки. 

**Как работает функция**:

- Функция получает экземпляр класса `Supplier` с запущенным WebDriver.
- Она использует WebDriver для открытия страницы входа на AliExpress.
- Она выполняет действия по вводу логина и пароля (TODO - реализация логики).
- Она возвращает `True`, если вход выполнен успешно.

**Пример**:

```python
from src.suppliers.aliexpress.scenarios.login import login
from src.suppliers.suppliers_list.aliexpress.supplier import Supplier

# Создаем экземпляр класса Supplier
supplier = Supplier(login='your_login', password='your_password')

# Выполняем вход на AliExpress
result = login(supplier)

# Проверяем результат
if result:
    print("Вход на AliExpress выполнен успешно!")
else:
    print("Ошибка входа на AliExpress")
```