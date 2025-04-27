## Как использовать модуль BeautifulSoup и XPath Parser
=========================================================================================

Описание
-------------------------
Этот модуль обеспечивает реализацию для парсинга HTML-контента с использованием BeautifulSoup и XPath. Он позволяет извлекать HTML-контент из файлов или URL-адресов, анализировать его и извлекать элементы с использованием локаторов XPath.

Шаги выполнения
-------------------------
1. **Импортируйте модуль и создайте объект `BS`**:
   - Используйте `from src.webdriver.bs import BS` для импорта модуля.
   - Создайте объект `BS` с помощью `parser = BS()`, чтобы инициализировать парсер.

2. **Загрузите конфигурацию**:
   - Загрузите конфигурацию из файла `bs.json` с помощью `j_loads_ns`: 
     ```python
     from src.utils.jjson import j_loads_ns
     from pathlib import Path

     settings_path = Path('path/to/bs.json')
     settings = j_loads_ns(settings_path)
     ```

3. **Получите HTML-контент**:
   - Используйте метод `get_url` для получения HTML-контента из файла или URL-адреса.
   -  ```python
     parser.get_url('file://path/to/your/file.html')
     ```  или  
     ```python
     parser.get_url('https://example.com')
     ```

4. **Определите локатор**:
   -  Создайте объект `SimpleNamespace` для определения локатора XPath.
   -  ```python
     from types import SimpleNamespace
     locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
     ```

5. **Выполните локатор**:
   - Используйте метод `execute_locator` для выполнения локатора XPath и извлечения соответствующих элементов.
   -  ```python
     elements = parser.execute_locator(locator)
     ```

6. **Обработайте результаты**:
   - Вывод будет содержать список найденных элементов, с которыми вы можете работать. 
   - ```python
     print(elements)
     ```

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

# Инициализация парсера BS с помощью URL по умолчанию
parser = BS(url=settings.default_url)

# Использование локатора по умолчанию из конфигурации
locator = SimpleNamespace(**settings.default_locator)
elements = parser.execute_locator(locator)
print(elements)
```
```

### Пример: Извлечение HTML из файла

```python
parser = BS()
parser.get_url('file://path/to/your/file.html')
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
elements = parser.execute_locator(locator)
print(elements)
```

### Пример: Извлечение HTML из URL

```python
parser = BS()
parser.get_url('https://example.com')
locator = SimpleNamespace(by='CSS', attribute='class_name', selector='//*[contains(@class, "class_name")]')
elements = parser.execute_locator(locator)
print(elements)
```

## Логирование и отладка

Модуль `BS` использует `logger` из `src.logger` для записи ошибок, предупреждений и общей информации. Все проблемы, возникающие при инициализации, конфигурации или выполнении, будут записаны в журнал для удобной отладки.

### Пример записей журнала

- **Ошибка при инициализации**: `Ошибка инициализации парсера BS: <подробности ошибки>`
- **Проблемы с конфигурацией**: `Ошибка в файле bs.json: <подробности проблемы>`

## Лицензия

Этот проект распространяется по лицензии MIT. Подробности см. в файле [LICENSE](../../LICENSE).