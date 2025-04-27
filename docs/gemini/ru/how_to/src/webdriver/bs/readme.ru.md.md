## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет кастомную реализацию для парсинга HTML-контента с использованием BeautifulSoup и XPath. Он позволяет загружать HTML-контент из файлов или URL-адресов, парсить его и извлекать элементы с помощью XPath-локаторов.

Шаги выполнения
-------------------------
1. Импортируйте модуль `BS` из `src.webdriver.bs`.
2. Инициализируйте парсер `BS` с URL или путем к файлу, из которого вы хотите загрузить HTML-контент.
3. Создайте объект `SimpleNamespace` с атрибутами `by`, `attribute` и `selector`, определяющими XPath-локатор для извлечения элементов.
4. Используйте метод `execute_locator` парсера `BS` с объектом `SimpleNamespace`, чтобы получить список элементов, соответствующих заданному локатору.

Пример использования
-------------------------

```python
from src.webdriver.bs import BS
from types import SimpleNamespace
from src.utils.jjson import j_loads_ns
from pathlib import Path

# Загрузка настроек из конфигурационного файла
settings_path = Path('path/to/bs.json')
settings = j_loads_ns(settings_path)

# Инициализация парсера BS с URL по умолчанию
parser = BS(url=settings.default_url)

# Использование локатора по умолчанию из конфигурации
locator = SimpleNamespace(**settings.default_locator)
elements = parser.execute_locator(locator)
print(elements)
```

```python
# Пример: Загрузка HTML из файла
parser = BS()
parser.get_url('file://path/to/your/file.html')
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
elements = parser.execute_locator(locator)
print(elements)
```

```python
# Пример: Загрузка HTML из URL
parser = BS()
parser.get_url('https://example.com')
locator = SimpleNamespace(by='CSS', attribute='class_name', selector='//*[contains(@class, "class_name")]')
elements = parser.execute_locator(locator)
print(elements)
```