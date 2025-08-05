# Модуль для авторизации поставщика Kualastyle

## Обзор

Модуль `login.py` предназначен для автоматизации процесса авторизации на сайте поставщика Kualastyle. Он содержит функции для открытия страницы авторизации, ввода учетных данных и закрытия всплывающих окон, если они появляются.

## Подробней

Модуль содержит функции для автоматизации процесса входа на сайт Kualastyle, включая обработку всплывающих окон и ожидание загрузки страницы.

## Функции

### `login`

```python
def login(s) -> bool:
    """ Функция логин. 
   @param
        s - Supplier
    @returns
        True if login else False

   """
    close_pop_up(s)
    return True
```

**Назначение**:
Осуществляет вход на сайт поставщика. На данный момент функция вызывает `close_pop_up(s)` и всегда возвращает `True`.

**Параметры**:
- `s`: Объект поставщика (`Supplier`), содержащий необходимую информацию для входа, такую как драйвер веб-браузера и локаторы элементов.

**Возвращает**:
- `bool`: Всегда возвращает `True`.

**Как работает функция**:
1. Вызывает функцию `close_pop_up(s)` для закрытия всплывающих окон.
2. Возвращает `True`, указывая на успешное завершение процесса входа (фактически, пока только имитирует вход).

**Примеры**:

```python
# Пример вызова функции login
from src.suppliers.kualastyle.supplier import Supplier  # Допустим, класс Supplier находится здесь

supplier = Supplier()
result = login(supplier)
print(result)  # Вывод: True
```

### `close_pop_up`

```python
def close_pop_up(s) -> bool:
    """ Функция логин
   @param
        s - Supplier
    @returns
        True if login else False

   """
    _d = s.driver
    _l : dict = s.locators['close_pop_up_locator']
    
    _d.get_url('https://www.kualastyle.com')
    _d.window_focus(_d)
    _d.wait(5)
    #_d.page_refresh()
    try:
        _d.execute_locator(_l)
    except Exception as ex:
        logger.warning(f"Не закрыл попап")
    
    ...
```

**Назначение**:
Закрывает всплывающее окно на сайте Kualastyle, если оно присутствует.

**Параметры**:
- `s`: Объект поставщика (`Supplier`), содержащий драйвер веб-браузера и локаторы элементов.

**Возвращает**:
- `bool`: Возвращает `True`, если всплывающее окно было успешно закрыто, в противном случае - `False`.

**Как работает функция**:
1. Извлекает драйвер веб-браузера (`_d`) из объекта поставщика `s`.
2. Извлекает локатор элемента для закрытия всплывающего окна (`_l`) из атрибута `locators` объекта поставщика.
3. Открывает URL `https://www.kualastyle.com` с использованием драйвера (`_d.get_url`).
4. Переключает фокус на текущее окно браузера (`_d.window_focus(_d)`).
5. Ожидает 5 секунд (`_d.wait(5)`).
6. Пытается выполнить действие по локатору (`_d.execute_locator(_l)`), чтобы закрыть всплывающее окно.
7. Если возникает исключение при закрытии всплывающего окна, регистрирует предупреждение с использованием `logger.warning`.

**Примеры**:

```python
# Пример вызова функции close_pop_up
from src.suppliers.kualastyle.supplier import Supplier  # Допустим, класс Supplier находится здесь
from src.logger.logger import logger

supplier = Supplier()
try:
    result = close_pop_up(supplier)
    print(f"Pop-up закрыт: {result}")
except Exception as ex:
    logger.error("Ошибка при закрытии pop-up", ex, exc_info=True)