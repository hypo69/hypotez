# Модуль `src.webdriver.bs`

## Обзор

Модуль `src.webdriver.bs` предназначен для парсинга HTML-контента с использованием библиотек `BeautifulSoup` и `lxml` (через XPath). Он предоставляет класс `BS` с методами для получения HTML с URL или из файла, а также для выполнения XPath-запросов к HTML-контенту.

## Подробней

Этот модуль полезен для извлечения данных из веб-страниц или локальных HTML-файлов. Он предоставляет удобный интерфейс для получения контента и поиска элементов на странице с использованием XPath.

## Классы

### `BS`

**Описание**: Класс для парсинга HTML-контента с использованием BeautifulSoup и XPath.

**Атрибуты**:

- `html_content` (str): HTML-контент, который нужно парсить. Изначально имеет значение `None`.

**Методы**:

- `__init__(self, url: Optional[str] = None)`: Инициализирует экземпляр класса `BS`.
- `get_url(self, url: str) -> bool`: Получает HTML-контент с URL или из файла.
- `execute_locator(self, locator: Union[SimpleNamespace, dict], url: Optional[str] = None) -> List[etree._Element]`: Выполняет XPath-запрос к HTML-контенту.

**Принцип работы**:

Класс `BS` предоставляет функциональность для получения и парсинга HTML-контента. При инициализации класса можно передать URL, с которого нужно получить HTML. Метод `get_url` выполняет запрос к указанному URL или считывает HTML из файла. Метод `execute_locator` выполняет XPath-запрос к HTML-контенту и возвращает список найденных элементов.

### `__init__`

```python
def __init__(self, url: Optional[str] = None):
    """
    Initializes the BS parser with an optional URL.

    :param url: The URL or file path to fetch HTML content from.
    :type url: Optional[str]
    """
```

**Назначение**: Инициализирует экземпляр класса `BS` с возможностью сразу получить HTML-контент с указанного URL.

**Параметры**:

- `url` (Optional[str], optional): URL или путь к файлу, откуда нужно получить HTML-контент. По умолчанию `None`.

**Примеры**:

```python
parser = BS('https://example.com')
parser = BS('file:///path/to/file.html')
parser = BS()
```

### `get_url`

```python
def get_url(self, url: str) -> bool:
    """
    Fetch HTML content from a file or URL and parse it with BeautifulSoup and XPath.

    :param url: The file path or URL to fetch HTML content from.
    :type url: str
    :return: True if the content was successfully fetched, False otherwise.
    :rtype: bool
    """
```

**Назначение**: Получает HTML-контент с указанного URL или из файла. Поддерживает `file://` и `https://` протоколы.

**Параметры**:

- `url` (str): URL или путь к файлу, откуда нужно получить HTML-контент.

**Возвращает**:

- `bool`: `True`, если контент успешно получен, `False` в противном случае.

**Как работает функция**:

1.  Проверяет, начинается ли URL с `file://`. Если да, то пытается прочитать HTML-контент из локального файла.
2.  Если URL начинается с `https://`, отправляет HTTP-запрос к указанному URL и сохраняет полученный HTML-контент.
3.  В случае ошибки логирует сообщение об ошибке и возвращает `False`.
4.  Если URL не начинается ни с `file://`, ни с `https://`, логирует сообщение об ошибке и возвращает `False`.

**Примеры**:

```python
parser = BS()
success = parser.get_url('https://example.com')
if success:
    print('HTML content successfully fetched.')
else:
    print('Failed to fetch HTML content.')
```

```python
parser = BS()
success = parser.get_url('file:///path/to/file.html')
if success:
    print('HTML content successfully fetched from file.')
else:
    print('Failed to fetch HTML content from file.')
```

### `execute_locator`

```python
def execute_locator(self, locator: Union[SimpleNamespace, dict], url: Optional[str] = None) -> List[etree._Element]:
    """
    Execute an XPath locator on the HTML content.

    :param locator: The locator object containing the selector and attribute.
    :type locator: Union[SimpleNamespace, dict]
    :param url: Optional URL or file path to fetch HTML content from.
    :type url: Optional[str]
    :return: A list of elements matching the locator.
    :rtype: List[etree._Element]
    """
```

**Назначение**: Выполняет XPath-запрос к HTML-контенту и возвращает список найденных элементов.

**Параметры**:

- `locator` (Union[SimpleNamespace, dict]): Объект локатора, содержащий селектор и атрибут. Может быть экземпляром `SimpleNamespace` или словарем.
- `url` (Optional[str], optional): URL или путь к файлу, откуда нужно получить HTML-контент. Если указан, то HTML-контент будет получен с этого URL. По умолчанию `None`.

**Возвращает**:

- `List[etree._Element]`: Список элементов, соответствующих локатору.

**Как работает функция**:

1.  Если передан параметр `url`, вызывает метод `get_url` для получения HTML-контента.
2.  Проверяет, был ли получен HTML-контент. Если нет, логирует сообщение об ошибке и возвращает пустой список.
3.  Создает объект `BeautifulSoup` из HTML-контента.
4.  Преобразует объект `BeautifulSoup` в дерево `lxml.etree`.
5.  Если `locator` является словарем, преобразует его в экземпляр `SimpleNamespace`.
6.  Извлекает атрибуты `attribute`, `by` и `selector` из объекта `locator`.
7.  В зависимости от значения `by` выполняет XPath-запрос к дереву `lxml.etree`.
8.  Возвращает список найденных элементов.

**Примеры**:

```python
parser = BS()
parser.get_url('https://example.com')
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
elements = parser.execute_locator(locator)
print(elements)
```

```python
parser = BS()
locator = {'by': 'ID', 'attribute': 'element_id', 'selector': '//*[@id="element_id"]'}
elements = parser.execute_locator(locator, 'https://example.com')
print(elements)
```

## `if __name__ == "__main__":`

В данном блоке кода создается экземпляр класса `BS`, выполняется получение HTML-контента с `https://example.com`, задается локатор для поиска элемента по ID и выполняется поиск элементов с использованием метода `execute_locator`. Результат поиска выводится на экран.