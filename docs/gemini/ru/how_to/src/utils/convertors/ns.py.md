### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет набор функций для преобразования объектов `SimpleNamespace` в различные форматы: словарь, JSON, CSV, XML и XLS. Каждая функция предназначена для упрощения процесса преобразования данных и сохранения их в соответствующем формате.

Шаги выполнения
-------------------------
1. **Импорт модуля**: Импортируйте модуль `src.utils.convertors.ns` в свой проект.
2. **Использование функций**: Выберите необходимую функцию в зависимости от требуемого формата преобразования.

Пример использования
-------------------------

```python
from types import SimpleNamespace
from pathlib import Path
from src.utils.convertors.ns import ns2dict, ns2csv, ns2xml, ns2xls

# Пример объекта SimpleNamespace
data = SimpleNamespace(
    name="Example",
    value=123,
    items=[SimpleNamespace(id=1, label="A"), SimpleNamespace(id=2, label="B")]
)

# Преобразование в словарь
dict_data = ns2dict(data)
print(dict_data)
# {'name': 'Example', 'value': 123, 'items': [{ 'id': 1, 'label': 'A'}, { 'id': 2, 'label': 'B'}]}

# Преобразование в CSV
csv_file = Path("example.csv")
ns2csv(data, csv_file)

# Преобразование в XML
xml_data = ns2xml(data, root_tag="root")
print(xml_data)
# <?xml version="1.0" encoding="UTF-8"?>
# <root><name>Example</name><value>123</value><items><item><id>1</id><label>A</label></item><item><id>2</id><label>B</label></item></items></root>

# Преобразование в XLS
xls_file = Path("example.xls")
ns2xls(data, xls_file)