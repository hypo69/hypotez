# Модуль для авторизации на Amazon

## Обзор

Модуль `login.py` предоставляет функциональность для авторизации пользователя на веб-сайте Amazon с использованием веб-драйвера. Он включает функцию `login`, которая реализует процесс входа на сайт с помощью заданных локаторов элементов.

## Подробней

Модуль `login.py` используется для авторизации на сайте Amazon с использованием веб-драйвера. Он использует заданные локаторы элементов для взаимодействия с веб-страницей и выполнения действий, необходимых для входа. 

## Функции

### `login`

**Назначение**: Функция `login` реализует процесс авторизации на сайте Amazon, используя заданные локаторы элементов и веб-драйвер.

**Параметры**:

- `s (Supplier)`: Объект класса `Supplier`, который содержит информацию о поставщике, включая локаторы элементов и веб-драйвер.

**Возвращает**:

- `bool`: Возвращает `True`, если авторизация прошла успешно, иначе `False`.

**Как работает функция**:

1. Функция `login` получает объект `Supplier` в качестве параметра.
2. Извлекает локаторы элементов для входа из атрибута `locators_store` объекта `Supplier`.
3. Инициализирует веб-драйвер из объекта `Supplier`.
4. Устанавливает фокус на текущее окно браузера.
5. Загружает страницу `https://amazon.com/`.
6. Кликает по кнопке для открытия формы ввода логина и пароля.
7. Если кнопка не найдена, пробует выполнить повторную загрузку страницы и повторить попытку клика.
8. Вводит адрес электронной почты в соответствующее поле ввода.
9. Кликает по кнопке "Продолжить".
10. Вводит пароль в соответствующее поле ввода.
11. Кликает по кнопке "Войти".
12. Проверяет, находится ли браузер на странице авторизации `https://www.amazon.com/ap/signin`.
13. Если браузер находится на странице авторизации, это означает, что авторизация не удалась. 
14. В противном случае функция считает авторизацию успешной и возвращает `True`.

**Примеры**:

```python
from src.suppliers.suppliers_list.amazon.login import login
from src.suppliers.suppliers_list.amazon.amazon import Amazon

# Создание объекта Amazon
amazon = Amazon()

# Вызов функции login
result = login(amazon)

# Проверка результата
if result:
    print('Авторизация прошла успешно.')
else:
    print('Авторизация не удалась.')