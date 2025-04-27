# hypo69
## Обзор

Этот модуль содержит набор конечных точек (endpoints) для разработчика, которые используются для взаимодействия с различными функциями проекта. 

## Детали

Этот модуль предоставляет ряд конечных точек для удобного взаимодействия с различными функциями проекта hypotez. 
Конечные точки предоставляют информацию о различных аспектах проекта, позволяя разработчикам получать доступ к 
важным данным и контролировать работу приложения.

## Классы

### `class Endpoint`

**Описание**: Класс, представляющий единую конечную точку.

**Атрибуты**:
- `name` (str): Имя конечной точки.
- `description` (str): Описание конечной точки.
- `method` (str): HTTP-метод, используемый для запроса (например, 'GET', 'POST').
- `path` (str): URL-путь к конечной точке.

**Методы**:

### `class EndpointGroup`

**Описание**: Класс, представляющий группу связанных конечных точек.

**Атрибуты**:
- `name` (str): Имя группы конечных точек.
- `description` (str): Описание группы конечных точек.
- `endpoints` (list): Список экземпляров класса `Endpoint`, принадлежащих этой группе.

**Методы**:


## Функции

### `get_endpoints()`

**Описание**: Функция, возвращающая список всех конечных точек.

**Возвращаемое значение**:
- `list`: Список экземпляров класса `Endpoint`.

**Пример**:

```python
from src.endpoints.hypo69 import get_endpoints

endpoints = get_endpoints()
for endpoint in endpoints:
    print(f"Endpoint: {endpoint.name} - {endpoint.description}")
```

### `get_endpoint_by_name(name: str)`

**Описание**: Функция, возвращающая конечную точку по ее имени.

**Параметры**:
- `name` (str): Имя конечной точки.

**Возвращаемое значение**:
- `Endpoint | None`: Экземпляр класса `Endpoint` или `None`, если конечная точка не найдена.

**Пример**:

```python
from src.endpoints.hypo69 import get_endpoint_by_name

endpoint = get_endpoint_by_name("product_info")
if endpoint:
    print(f"Endpoint: {endpoint.name} - {endpoint.description}")
else:
    print("Endpoint not found.")
```

### `get_endpoint_group_by_name(name: str)`

**Описание**: Функция, возвращающая группу конечных точек по ее имени.

**Параметры**:
- `name` (str): Имя группы конечных точек.

**Возвращаемое значение**:
- `EndpointGroup | None`: Экземпляр класса `EndpointGroup` или `None`, если группа не найдена.

**Пример**:

```python
from src.endpoints.hypo69 import get_endpoint_group_by_name

group = get_endpoint_group_by_name("product_management")
if group:
    print(f"Endpoint Group: {group.name} - {group.description}")
    for endpoint in group.endpoints:
        print(f" - Endpoint: {endpoint.name} - {endpoint.description}")
else:
    print("Endpoint Group not found.")
```

## Примеры

**Пример 1. Получение списка всех конечных точек:**

```python
from src.endpoints.hypo69 import get_endpoints

endpoints = get_endpoints()
for endpoint in endpoints:
    print(f"Endpoint: {endpoint.name} - {endpoint.description}")
```

**Пример 2. Получение информации о конкретной конечной точке:**

```python
from src.endpoints.hypo69 import get_endpoint_by_name

endpoint = get_endpoint_by_name("product_info")
if endpoint:
    print(f"Endpoint: {endpoint.name} - {endpoint.description}")
    print(f"Method: {endpoint.method}")
    print(f"Path: {endpoint.path}")
else:
    print("Endpoint not found.")
```

**Пример 3. Получение списка конечных точек в группе:**

```python
from src.endpoints.hypo69 import get_endpoint_group_by_name

group = get_endpoint_group_by_name("product_management")
if group:
    print(f"Endpoint Group: {group.name} - {group.description}")
    for endpoint in group.endpoints:
        print(f" - Endpoint: {endpoint.name} - {endpoint.description}")
else:
    print("Endpoint Group not found.")
```


## Как это работает

Модуль `hypo69` предоставляет набор функций для взаимодействия с различными конечными точками. Функции позволяют получить список всех конечных точек, информацию о 
конкретной конечной точке или группу конечных точек. 
Модуль использует конфигурационный файл, где хранится информация о всех доступных конечных точках. 

## Дополнительные сведения

- **Примеры**: Для получения более подробных примеров и инструкций по использованию модуля, пожалуйста, обратитесь к документации проекта.
- **Логирование**: Для отслеживания ошибок и информации используйте модуль `logger` из `src.logger`.
- **Водитель**: Для взаимодействия с веб-элементами используйте `driver` из `src.webdriver`.
- **Дополнительные сведения**: Для получения более подробной информации о конкретных конечных точках, их параметрах и 
ожидаемых ответах, пожалуйста, ознакомьтесь с документацией проекта.