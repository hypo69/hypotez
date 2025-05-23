# Модуль Авторизации на Amazon

## Обзор

Этот модуль содержит функцию `login`, которая реализует процесс авторизации на Amazon с использованием вебдрайвера. 

## Подробности

Функция `login` выполняет следующие действия:

1. Открывает веб-страницу Amazon.
2. Находит и нажимает кнопку входа.
3. Вводит адрес электронной почты в поле ввода.
4. Нажимает кнопку "Продолжить".
5. Вводит пароль в поле ввода.
6. Нажимает кнопку "Войти".
7. Проверяет успешность входа, сравнивая текущий URL с URL страницы входа.
8. Выводит сообщение об успешном или неуспешном входе.

## Функции

### `login(s: Supplier) -> bool`

**Цель**: Авторизация на Amazon с использованием вебдрайвера.

**Параметры**:

- `s (Supplier)`: Объект, представляющий поставщика.

**Возвращаемое значение**:

- `bool`: `True` в случае успешного входа, `False` в противном случае.

**Исключения**:

- `Exception`: Возникает в случае непредвиденных ошибок.

**Пример**:

```python
from src.suppliers.suppliers_list.amazon.login import login
from src.suppliers.suppliers_list.amazon.amazon import Amazon

supplier = Amazon()
success = login(supplier)
if success:
    print("Авторизация прошла успешно!")
else:
    print("Ошибка при авторизации.")
```

**Как работает функция**:

1. Функция `login` получает объект `Supplier` в качестве параметра.
2. Извлекает из объекта `Supplier` локаторы для элементов страницы входа (например, "открыть поля входа", "поле ввода email", "кнопка продолжить" и т. д.).
3. Выполняет ряд действий по взаимодействию с вебдрайвером:
    - Переходит на страницу входа Amazon.
    - Находит и нажимает кнопку входа.
    - Вводит адрес электронной почты в поле ввода.
    - Нажимает кнопку "Продолжить".
    - Вводит пароль в поле ввода.
    - Нажимает кнопку "Войти".
    - Проверяет URL страницы.
4. Возвращает `True` в случае успешного входа, `False` в противном случае.

**Примечания**:

- В коде функции `login` есть несколько комментариев TODO, которые указывают на места, где требуется доработка логики обработки ошибок.
- В коде используется вебдрайвер для взаимодействия с веб-страницей.
- Для логгирования используется модуль `logger` из `src.logger.logger`.

## Пример вызова функции:

```python
from src.suppliers.suppliers_list.amazon.login import login
from src.suppliers.suppliers_list.amazon.amazon import Amazon

supplier = Amazon()
result = login(supplier)
```

## Пример использования вебдрайвера:

```python
from src.webdriver import Driver, Chrome

# Создание экземпляра вебдрайвера (в данном случае Chrome)
driver = Driver(Chrome)

# Выполнение действий с вебдрайвером
result = driver.execute_locator({
    # Определение локатора для веб-элемента
    "attribute": null,
    "by": "XPATH",
    "selector": "//button[@id = 'closeXButton']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "click()",
    "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
})
```