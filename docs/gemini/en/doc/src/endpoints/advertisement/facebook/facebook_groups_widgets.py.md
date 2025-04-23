# Module src.endpoints.advertisement.facebook.facebook_groups_widgets

## Overview

Модуль предназначен для создания раскрывающегося меню выбора групп Facebook для подачи объявлений. Он использует библиотеку `ipywidgets` для создания интерактивного элемента Dropdown, который отображает список URL групп Facebook, загруженных из JSON-файла.

## More details

Этот модуль облегчает выбор целевой группы Facebook для рекламных кампаний. Он загружает список групп из JSON-файла, создает виджет выпадающего списка и отображает его для пользователя. Файл `facebook_groups_widgets.py` находится в каталоге `src/endpoints/advertisement/facebook/` проекта `hypotez` и отвечает за предоставление графического интерфейса выбора групп Facebook на основе данных из JSON-файла.

## Classes

### `FacebookGroupsWidget`

**Description**: Класс для создания выпадающего списка с URL групп Facebook из предоставленного JSON.
**Inherits**: Нет.

**Attributes**:
- `groups_data` (SimpleNamespace):  Объект, содержащий данные о группах Facebook, загруженные из JSON-файла.
- `dropdown` (Dropdown): Виджет выпадающего списка с URL групп Facebook.

**Parameters**:
- `json_file_path` (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.

**Working principle**:
Класс `FacebookGroupsWidget` инициализируется путем передачи пути к JSON-файлу, содержащему данные о группах Facebook. При инициализации происходит загрузка данных из JSON-файла и создание виджета выпадающего списка. Класс предоставляет метод для отображения этого виджета.

**Methods**:
- `__init__(self, json_file_path: Path)`: Инициализирует виджет с выпадающим списком для групп Facebook.
- `create_dropdown(self) -> Dropdown`: Создает и возвращает виджет выпадающего списка на основе данных групп.
- `display_widget(self)`: Отображает виджет выпадающего списка.

## Class Methods

### `__init__(self, json_file_path: Path)`

```python
def __init__(self, json_file_path: Path):
    """
    Инициализация виджета с выпадающим списком для групп Facebook.

    Args:
        json_file_path (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.
    """
    ...
```

**Purpose**: Инициализирует экземпляр класса `FacebookGroupsWidget`.
**Parameters**:
- `json_file_path` (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.

**How the function works**:
1. Функция принимает путь к JSON-файлу (`json_file_path`) как аргумент.
2. Загружает данные из JSON-файла, используя функцию `j_loads_ns` и сохраняет их в атрибуте `groups_data`.
3. Вызывает метод `create_dropdown` для создания виджета выпадающего списка и сохраняет его в атрибуте `dropdown`.

**Examples**:
```python
from pathlib import Path
file_path = Path("path/to/your/groups.json")
widget = FacebookGroupsWidget(file_path)
```

### `create_dropdown(self) -> Dropdown`

```python
def create_dropdown(self) -> Dropdown:
    """ Создает и возвращает виджет выпадающего списка на основе данных групп.

    Returns:
        Dropdown: Виджет выпадающего списка с URL групп Facebook.
    """
    ...
```

**Purpose**: Создает и возвращает виджет выпадающего списка на основе данных групп.

**Returns**:
- `Dropdown`: Виджет выпадающего списка с URL групп Facebook.

**How the function works**:
1. Извлекает ключи (URL групп) из атрибута `groups_data`.
2. Создает виджет `Dropdown` из библиотеки `ipywidgets`, используя извлеченные URL групп в качестве опций.
3. Устанавливает описание виджета как "Facebook Groups:".
4. Отключает виджет (`disabled=False`).
5. Возвращает созданный виджет `Dropdown`.

**Examples**:
```python
from pathlib import Path
file_path = Path("path/to/your/groups.json")
widget = FacebookGroupsWidget(file_path)
dropdown = widget.create_dropdown()
```

### `display_widget(self)`

```python
def display_widget(self):
    """ Отображает виджет выпадающего списка."""
    ...
```

**Purpose**: Отображает виджет выпадающего списка.
**Parameters**: None

**How the function works**:
1. Использует функцию `display` из модуля `IPython.display` для отображения виджета `dropdown`.

**Examples**:
```python
from pathlib import Path
file_path = Path("path/to/your/groups.json")
widget = FacebookGroupsWidget(file_path)
widget.display_widget()
```