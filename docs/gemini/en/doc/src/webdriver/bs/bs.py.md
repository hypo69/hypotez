# Модуль src.webdriver.bs

## Обзор

Модуль `src.webdriver.bs` предоставляет кастомную реализацию для парсинга HTML-контента с использованием `BeautifulSoup` и XPath.

## Детали

Модуль позволяет работать с HTML-кодом, загружая его из локального файла или из сети, а затем анализируя с помощью `BeautifulSoup`. 
Он предоставляет возможность выполнять поиск элементов на странице по заданным XPath-селекторам. 

Этот модуль используется в проекте для взаимодействия с веб-страницами и извлечения нужной информации. 

## Классы

### `class BS`

**Описание**: Класс `BS` - это основной класс модуля, который обеспечивает функциональность для парсинга HTML-контента.

**Атрибуты**:

 - `html_content (str)`: HTML-контент, который будет парситься.

**Методы**:

- `__init__(self, url: Optional[str] = None)`: Инициализирует парсер `BS` с необязательным URL.

    **Параметры**:

    - `url (Optional[str])`: URL или путь к файлу, из которого нужно загрузить HTML-контент. По умолчанию `None`.

- `get_url(self, url: str) -> bool`: Загружает HTML-контент из файла или URL и парсит его с помощью `BeautifulSoup` и XPath.

    **Параметры**:

    - `url (str)`: Путь к файлу или URL, из которого нужно загрузить HTML-контент.

    **Возвращает**:

    - `bool`: `True`, если контент был успешно загружен, `False` в противном случае.

- `execute_locator(self, locator: Union[SimpleNamespace, dict], url: Optional[str] = None) -> List[etree._Element]`: Выполняет XPath-селектор на HTML-контенте.

    **Параметры**:

    - `locator (Union[SimpleNamespace, dict])`: Объект селектора, содержащий селектор и атрибут.
    - `url (Optional[str])`: Необязательный URL или путь к файлу, из которого нужно загрузить HTML-контент.

    **Возвращает**:

    - `List[etree._Element]`: Список элементов, соответствующих селектору.


## Примеры

```python
# Создание экземпляра парсера
parser = BS()

# Загрузка HTML-контента из URL
parser.get_url('https://example.com')

# Создание объекта селектора
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')

# Выполнение селектора и получение элементов
elements = parser.execute_locator(locator)

# Вывод элементов
print(elements)
```

## Принцип работы 

### `class BS`

- **Инициализация**: При инициализации класса `BS` с необязательным URL, метод `get_url` выполняется для загрузки HTML-контента.
- **Загрузка контента**: Метод `get_url` обрабатывает как локальные файлы, так и сетевые URL. Он проверяет, является ли URL локальным путем к файлу, и если да, то считывает его содержимое. Для сетевых URL метод использует `requests` для загрузки страницы и извлечения текста.
- **Парсинг**: Метод `execute_locator` выполняет XPath-селектор на загруженном HTML-контенте. Он принимает объект селектора, который может быть либо `SimpleNamespace`, либо `dict`. 
- **XPath-поиск**: Метод `execute_locator` конвертирует объект `BeautifulSoup` в `lxml` дерево и использует `xpath` для поиска элементов на странице. 
- **Возврат элементов**: Метод возвращает список элементов, соответствующих селектору. 

## Функции

### `execute_locator`

**Цель**: Выполняет XPath-селектор на HTML-контенте.

**Параметры**:

- `locator (Union[SimpleNamespace, dict])`: Объект селектора, содержащий селектор и атрибут.
- `url (Optional[str])`: Необязательный URL или путь к файлу, из которого нужно загрузить HTML-контент.

**Возвращает**:

- `List[etree._Element]`: Список элементов, соответствующих селектору.

**Повышает исключения**:

- `Exception`: Если возникает ошибка во время парсинга HTML.

**Как работает функция**:

- Функция проверяет, доступен ли HTML-контент для парсинга.
- Если доступен, функция конвертирует объект `BeautifulSoup` в `lxml` дерево.
- Затем функция обрабатывает объект селектора и извлекает из него `by`, `attribute` и `selector`.
- Функция выполняет XPath-селектор на дереве и возвращает список найденных элементов. 

**Примеры**:

```python
# Создание объекта селектора
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')

# Выполнение селектора
elements = parser.execute_locator(locator)

# Вывод элементов
print(elements)

# Создание объекта селектора с использованием словаря
locator = {'by': 'CSS', 'attribute': 'class_name', 'selector': '//*[contains(@class, "class_name")]'}

# Выполнение селектора
elements = parser.execute_locator(locator)

# Вывод элементов
print(elements)
```

## Детали параметров

- `locator (Union[SimpleNamespace, dict])`: Объект селектора, который может быть либо `SimpleNamespace`, либо `dict`. Он должен содержать следующие ключи:
    - `by (str)`: Тип селектора. Возможные значения: `ID`, `CSS`, `TEXT`.
    - `attribute (str)`: Значение атрибута, которое нужно использовать для поиска.
    - `selector (str)`: XPath-селектор, который нужно использовать для поиска.

- `url (Optional[str])`: Необязательный URL или путь к файлу, из которого нужно загрузить HTML-контент. Если не указан, функция будет использовать HTML-контент, доступный в атрибуте `html_content`.

## Примеры вызова функций

### `execute_locator`

```python
# Создание объекта селектора
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')

# Выполнение селектора
elements = parser.execute_locator(locator)

# Вывод элементов
print(elements)

# Создание объекта селектора с использованием словаря
locator = {'by': 'CSS', 'attribute': 'class_name', 'selector': '//*[contains(@class, "class_name")]'}

# Выполнение селектора
elements = parser.execute_locator(locator)

# Вывод элементов
print(elements)
```

```python
# Выполнение селектора на HTML-контенте, полученном из URL
elements = parser.execute_locator(locator, url='https://example.com')
```