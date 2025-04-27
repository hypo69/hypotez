# Модуль для проверки локатора закрытия поп-ап окна

## Обзор

Модуль `src.suppliers.morlevi._experiments.close_pop_up.py` предназначен для тестирования локатора закрытия поп-ап окна на сайте Morlevi. Он использует `webdriver` для взаимодействия с браузером и `MorleviGraber` для извлечения информации о товарах.

## Детали

Этот файл выполняет следующие действия:

- Импортирует необходимые модули: `header`, `gs`, `Driver`, `Firefox`, `MorleviGraber`, `j_loads_ns`.
- Создает экземпляр `Driver` с использованием браузера `Firefox`.
- Создает экземпляр `MorleviGraber` с использованием созданного `Driver`.
- Загружает страницу товара на сайте Morlevi.
- Извлекает `id_product` товара с помощью `MorleviGraber`.

## Классы

### `MorleviGraber`

**Описание**: Класс `MorleviGraber` предоставляет методы для извлечения информации о товарах с сайта Morlevi.

**Inherits**: 
    - Наследуется от класса `Graber` 

**Attributes**: 
    - `driver` (Driver): Экземпляр `Driver` для взаимодействия с браузером.

**Methods**: 
    - `id_product()`: Извлекает идентификатор товара с сайта.

## Функции

### `close_pop_up`

**Purpose**: Проверяет локатор закрытия поп-ап окна.

**Parameters**:
- `locator` (dict): Локатор элемента, который нужно найти на странице.

**Returns**:
- `bool`: Возвращает `True`, если локатор найден, и `False`, если нет.

**Raises Exceptions**:
- `Exception`: Если возникает ошибка при поиске элемента.

**How the Function Works**:
- Использует `driver.execute_locator(locator)` для поиска элемента по указанному локатору.
- Возвращает `True`, если элемент найден, и `False`, если нет.

**Examples**:
```python
# Пример 1: Проверка локатора с успешным результатом
locator = {
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
}
result = close_pop_up(locator)
print(result) # Вывод: True

# Пример 2: Проверка локатора с ошибкой
locator = {
    "attribute": null,
    "by": "XPATH",
    "selector": "//button[@id = 'nonexistent_button']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "click()",
    "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}
try:
    result = close_pop_up(locator)
except Exception as ex:
    print(f"Ошибка: {ex}") # Вывод: Ошибка: Ошибка поиска элемента по локатору
```

**Inner Functions**: 
    - Отсутствуют

## Parameter Details

- `locator` (dict): Словарь с параметрами локатора элемента.

## Examples

```python
# Пример 1: Использование close_pop_up для закрытия поп-ап окна
close_banner = {
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
}
close_pop_up(close_banner)

# Пример 2: Использование close_pop_up для проверки наличия элемента
check_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": null,
  "locator_description": "Проверка наличия элемента"
}
is_banner_present = close_pop_up(check_banner)
print(f"Баннер присутствует: {is_banner_present}")
```