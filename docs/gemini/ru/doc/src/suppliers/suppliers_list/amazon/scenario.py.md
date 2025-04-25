# Модуль сбора товаров со страницы категорий поставщика amazon.com через вебдрайвер

## Обзор

Модуль `scenario.py` представляет собой сценарий сбора товаров с веб-сайта amazon.com, 
используя вебдрайвер для автоматизации процесса. Он включает в себя функции для 
получения списка категорий, списка товаров из категории и обработки страницы товара. 
Сценарий является частью системы `hypotez`, предназначенной для сбора данных 
о товарах с различных платформ электронной коммерции.

## Подробней

Модуль реализует несколько функций, которые работают в связке для 
получения данных о товарах с amazon.com:

- `get_list_products_in_category`: Возвращает список ссылок на товары 
из заданной категории на сайте amazon.com.

## Функции

### `get_list_products_in_category`

**Назначение**: Получает список ссылок на товары из страницы категории.

**Параметры**:

- `d` (`Driver`): Экземпляр вебдрайвера, используемого для взаимодействия с сайтом.
- `l` (`dict`): Словарь с локаторами для поиска элементов на странице.

**Возвращает**:

- `list[str, str, None]`: Список ссылок на товары, где каждый элемент - это кортеж из двух строк (url товара) или `None`, 
если ссылок на товары не найдено.

**Пример**:

```python
from src.webdirver import Driver, Chrome
driver = Driver(Chrome)
locators = {
  "product_links": {
    "attribute": null,
    "by": "XPATH",
    "selector": "//span[@class = 'a-size-base-plus a-color-base a-text-normal']",
    "if_list": "all",
    "use_mouse": false,
    "mandatory": true,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "get_attribute('href')",
    "locator_description": "Получаем список ссылок на товары"
  }
}
products_urls = get_list_products_in_category(driver, locators)
print(products_urls)
```

**Как работает функция**:

1. Функция `get_list_products_in_category`  прокручивает страницу категории вниз, 
чтобы убедиться, что все элементы страницы загружены.
2. Функция `execute_locator` вебдрайвера (`d.execute_locator()`) 
используется для поиска ссылок на товары по локатору `l['product_links']`.
3. Если ссылок на товары не найдено, функция выводит сообщение в лог 
и возвращает `None`.
4. Если ссылки на товары найдены, функция возвращает список 
ссылок на товары.

##  Методы класса 
### `execute_locator`

**Описание**: Метод выполняет поиск элемента по локатору и возвращает его значение.

**Параметры**:

- `l` (`dict`): Локатор элемента.

**Возвращает**:

- `str`: Значение элемента.
- `None`: Если элемент не найден.

**Пример**:

```python
from src.webdirver import Driver, Chrome
driver = Driver(Chrome)
locator = {
    "attribute": "href",
    "by": "XPATH",
    "selector": "//a[@class='a-link-normal a-text-normal']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": true,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "get_attribute('href')",
    "locator_description": "Получаем значение атрибута href первого найденного элемента."
}
element_value = driver.execute_locator(locator)
print(element_value)
```

**Как работает**:

1. Метод выполняет поиск элемента на странице, используя локатор.
2. Если элемент найден, метод возвращает его значение, используя 
указанный в локаторе атрибут. 
3. Если элемент не найден, метод возвращает `None`.

### `scroll`

**Описание**: Метод прокручивает страницу вниз до конца. 

**Параметры**:

-  `scroll_step` (`int`): Шаг прокрутки, по умолчанию 250px.

**Возвращает**:

- `None`:  

**Пример**:

```python
from src.webdirver import Driver, Chrome
driver = Driver(Chrome)
driver.scroll()
```

**Как работает**:

1. Метод прокручивает страницу вниз на шаг `scroll_step` до тех пор, 
пока не будет достигнут конец страницы.

## Параметры класса 

### `product_links`

**Описание**: Локатор для поиска ссылок на товары.

**Параметры**:

- `attribute` (`str`, `optional`): Атрибут элемента, который нужно получить, 
по умолчанию `None`.
- `by` (`str`): Способ поиска элемента, по умолчанию `XPATH`.
- `selector` (`str`): Селектор элемента, по умолчанию `//span[@class = 'a-size-base-plus a-color-base a-text-normal']`.
- `if_list` (`str`, `optional`):  `all`, `first` или `index`. Определяет, нужно ли получить 
все элементы, первый элемент или элемент по индексу, по умолчанию `all`.
- `use_mouse` (`bool`, `optional`): Нужно ли использовать мышь для взаимодействия с 
элементом, по умолчанию `False`.
- `mandatory` (`bool`, `optional`):  `True`, если элемент обязателен для 
нахождения, по умолчанию `True`. 
- `timeout` (`int`, `optional`): Время ожидания в секундах для появления элемента, 
по умолчанию `0`.
- `timeout_for_event` (`str`, `optional`): Тип события, для которого нужно 
ждать, по умолчанию `presence_of_element_located`.
- `event` (`str`, `optional`): Метод, который нужно применить к элементу, 
по умолчанию `get_attribute('href')`.
- `locator_description` (`str`, `optional`): Описание локатора.

## Примеры

```python
from src.suppliers.suppliers_list.amazon.scenario import get_list_products_in_category
from src.webdirver import Driver, Chrome

driver = Driver(Chrome)

# Локаторы для поиска элементов
locators = {
  "product_links": {
    "attribute": null,
    "by": "XPATH",
    "selector": "//span[@class = 'a-size-base-plus a-color-base a-text-normal']",
    "if_list": "all",
    "use_mouse": false,
    "mandatory": true,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "get_attribute('href')",
    "locator_description": "Получаем список ссылок на товары"
  }
}

# Получаем список ссылок на товары
products_urls = get_list_products_in_category(driver, locators)

# Вывод полученного списка
print(products_urls)

# Закрытие вебдрайвера
driver.close()