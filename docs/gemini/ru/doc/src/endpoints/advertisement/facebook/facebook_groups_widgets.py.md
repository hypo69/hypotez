# Модуль для создания выпадающего списка групп Facebook

## Обзор

Модуль `facebook_groups_widgets.py` предназначен для создания и отображения выпадающего списка с URL групп Facebook. Он использует данные, загруженные из JSON-файла, и предоставляет удобный интерфейс для выбора группы.

## Подробнее

Этот модуль облегчает выбор целевой группы Facebook для размещения рекламы, предоставляя графический интерфейс в виде выпадающего списка. Он использует библиотеку `ipywidgets` для создания интерактивного виджета, который отображается в Jupyter Notebook или аналогичной среде.

## Классы

### `FacebookGroupsWidget`

**Описание**:
Класс `FacebookGroupsWidget` создает выпадающий список с URL групп Facebook на основе данных из JSON-файла.

**Наследует**:
Не наследует никаких классов.

**Атрибуты**:
- `groups_data` (SimpleNamespace): Объект, содержащий данные о группах Facebook, загруженные из JSON-файла.
- `dropdown` (Dropdown): Виджет выпадающего списка с URL групп Facebook.

**Методы**:
- `__init__(self, json_file_path: Path)`: Инициализирует виджет, загружает данные о группах и создает выпадающий список.
- `create_dropdown(self) -> Dropdown`: Создает и возвращает виджет выпадающего списка на основе данных групп.
- `display_widget(self)`: Отображает виджет выпадающего списка.

### `__init__`

```python
def __init__(self, json_file_path: Path):
    """
    Инициализация виджета с выпадающим списком для групп Facebook.

    Args:
        json_file_path (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.
    """
```

**Назначение**:
Инициализирует класс `FacebookGroupsWidget`, загружая данные о группах Facebook из указанного JSON-файла и создавая на основе этих данных выпадающий список.

**Параметры**:
- `json_file_path` (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.

**Как работает функция**:
1. Загружает данные о группах Facebook из JSON-файла, используя функцию `j_loads_ns` из модуля `src.utils.jjson`, и сохраняет их в атрибуте `self.groups_data`.
2. Создает выпадающий список на основе загруженных данных, вызывая метод `self.create_dropdown()`, и сохраняет его в атрибуте `self.dropdown`.

### `create_dropdown`

```python
def create_dropdown(self) -> Dropdown:
    """ Создает и возвращает виджет выпадающего списка на основе данных групп.

    Returns:
        Dropdown: Виджет выпадающего списка с URL групп Facebook.
    """
```

**Назначение**:
Создает и возвращает виджет выпадающего списка (`Dropdown`) на основе данных о группах Facebook, хранящихся в атрибуте `self.groups_data`.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `Dropdown`: Виджет выпадающего списка с URL групп Facebook.

**Как работает функция**:
1. Извлекает ключи (URL групп) из словаря `self.groups_data.__dict__` и преобразует их в список.
2. Создает экземпляр класса `Dropdown` из модуля `ipywidgets`, передавая в него следующие параметры:
   - `options`: Список URL групп Facebook.
   - `description`: Текст описания виджета ("Facebook Groups:").
   - `disabled`: Устанавливается в `False`, что делает виджет активным.
3. Возвращает созданный виджет выпадающего списка.

### `display_widget`

```python
def display_widget(self):
    """ Отображает виджет выпадающего списка."""
```

**Назначение**:
Отображает виджет выпадающего списка (`Dropdown`) в Jupyter Notebook или аналогичной среде.

**Параметры**:
- Отсутствуют.

**Как работает функция**:
1. Использует функцию `display` из модуля `IPython.display` для отображения виджета `self.dropdown`.

```python
from src.endpoints.advertisement.facebook.facebook_groups_widgets import FacebookGroupsWidget
from pathlib import Path

# Предположим, что 'groups.json' находится в той же директории, что и скрипт
json_file_path = Path('groups.json')

# Создание экземпляра виджета
groups_widget = FacebookGroupsWidget(json_file_path)

# Отображение виджета
groups_widget.display_widget()