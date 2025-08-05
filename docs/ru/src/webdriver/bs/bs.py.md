# Модуль `src.webdriver.bs`

## Обзор

Модуль `src.webdriver.bs` предназначен для парсинга HTML-контента с использованием библиотек `BeautifulSoup` и `lxml` с поддержкой XPath. Он предоставляет класс `BS` для загрузки HTML-контента из URL или локального файла, а также для выполнения XPath-запросов к этому контенту.

## Подробнее

Модуль `src.webdriver.bs` упрощает процесс извлечения данных из HTML-страниц, предоставляя удобный интерфейс для выполнения XPath-запросов. Он автоматически определяет, загружать ли контент из файла или URL, и обеспечивает обработку ошибок при загрузке контента.

## Классы

### `BS`

**Описание**: Класс для парсинга HTML-контента с использованием BeautifulSoup и XPath.

**Атрибуты**:
- `html_content` (str): HTML-контент для парсинга.

**Методы**:
- `__init__(self, url: Optional[str] = None)`: Инициализирует парсер `BS` с необязательным URL.
- `get_url(self, url: str) -> bool`: Загружает HTML-контент из файла или URL и парсит его с помощью BeautifulSoup и XPath.
- `execute_locator(self, locator: Union[SimpleNamespace, dict], url: Optional[str] = None) -> List[etree._Element]`: Выполняет XPath-локатор на HTML-контенте.

### `BS.__init__(self, url: Optional[str] = None)`

**Назначение**: Инициализирует экземпляр класса `BS`.

**Параметры**:
- `url` (Optional[str], optional): URL или путь к файлу для загрузки HTML-контента. По умолчанию `None`.

**Как работает функция**:
- Если `url` указан, то вызывает метод `self.get_url(url)` для загрузки и парсинга HTML-контента.

### `BS.get_url(self, url: str) -> bool`

**Назначение**: Загружает HTML-контент из файла или URL и парсит его с помощью BeautifulSoup и XPath.

**Параметры**:
- `url` (str): URL или путь к файлу для загрузки HTML-контента.

**Возвращает**:
- `bool`: `True`, если контент был успешно загружен, `False` в противном случае.

**Как работает функция**:
1. Проверяет, начинается ли `url` с `'file://'`. Если да, то пытается загрузить контент из локального файла.
2. Если `url` начинается с `'https://'`, то пытается загрузить контент из сети, используя библиотеку `requests`.
3. В случае успеха сохраняет HTML-контент в атрибут `self.html_content`.
4. При возникновении ошибок записывает сообщение об ошибке в лог с использованием `logger.error`.

**Примеры**:
```python
parser = BS()
result = parser.get_url('file:///c:/path/to/your/file.html')
print(result) # Вывод: True или False в зависимости от успеха загрузки

parser = BS()
result = parser.get_url('https://example.com')
print(result) # Вывод: True или False в зависимости от успеха загрузки
```

### `BS.execute_locator(self, locator: Union[SimpleNamespace, dict], url: Optional[str] = None) -> List[etree._Element]`

**Назначение**: Выполняет XPath-локатор на HTML-контенте.

**Параметры**:
- `locator` (Union[SimpleNamespace, dict]): Объект локатора, содержащий селектор и атрибут.
- `url` (Optional[str], optional): URL или путь к файлу для загрузки HTML-контента. По умолчанию `None`.

**Возвращает**:
- `List[etree._Element]`: Список элементов, соответствующих локатору.

**Как работает функция**:
1. Если указан `url`, то вызывает метод `self.get_url(url)` для загрузки HTML-контента.
2. Проверяет, загружен ли HTML-контент в атрибут `self.html_content`. Если нет, то записывает сообщение об ошибке в лог с использованием `logger.error` и возвращает пустой список.
3. Преобразует HTML-контент в объект `BeautifulSoup`, а затем в объект `lxml.etree`.
4. Извлекает атрибуты локатора (`attribute`, `by`, `selector`) из объекта `locator`.
5. Выполняет XPath-запрос в зависимости от значения атрибута `by` (`'ID'`, `'CSS'`, `'TEXT'` или XPath-селектор).
6. Возвращает список элементов, соответствующих локатору.

**Примеры**:

```python
from types import SimpleNamespace

parser = BS()
parser.get_url('https://example.com')
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
elements = parser.execute_locator(locator)
print(elements)  # Вывод: Список найденных элементов или пустой список, если ничего не найдено
```
```python
# Использование execute_locator с передачей URL
from types import SimpleNamespace
parser = BS()
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
elements = parser.execute_locator(locator, url='https://example.com')
print(elements)
```

## Примеры использования

```python
if __name__ == "__main__":
    parser = BS()
    parser.get_url('https://example.com')
    locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
    elements = parser.execute_locator(locator)
    print(elements)