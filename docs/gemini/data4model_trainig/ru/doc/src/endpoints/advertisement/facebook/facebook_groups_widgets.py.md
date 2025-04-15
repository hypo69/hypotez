# Модуль для работы с виджетом групп Facebook

## Обзор

Модуль `facebook_groups_widgets.py` предназначен для создания и отображения выпадающего списка с URL групп Facebook. Он использует библиотеку `ipywidgets` для создания интерактивного элемента, который позволяет пользователю выбирать группы Facebook из списка, полученного из JSON-файла.

## Подробней

Этот модуль предоставляет класс `FacebookGroupsWidget`, который инициализируется путем загрузки данных о группах Facebook из JSON-файла и создает на основе этих данных выпадающий список. Виджет отображается с использованием функции `display` из библиотеки `IPython.display`.

## Классы

### `FacebookGroupsWidget`

**Описание**: Класс для создания и отображения выпадающего списка с URL групп Facebook.

**Атрибуты**:
- `groups_data` (SimpleNamespace): Данные о группах Facebook, загруженные из JSON-файла.
- `dropdown` (Dropdown): Виджет выпадающего списка с URL групп Facebook.

**Методы**:
- `__init__(self, json_file_path: Path)`: Инициализирует виджет, загружает данные о группах и создает выпадающий список.
- `create_dropdown(self) -> Dropdown`: Создает и возвращает виджет выпадающего списка на основе данных групп.
- `display_widget(self)`: Отображает виджет выпадающего списка.

#### `__init__(self, json_file_path: Path)`

**Назначение**: Инициализация виджета с выпадающим списком для групп Facebook.

**Параметры**:
- `json_file_path` (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.

**Как работает функция**:
1. Загружает данные о группах Facebook из JSON-файла, используя функцию `j_loads_ns` из модуля `src.utils.jjson`, и сохраняет их в атрибуте `self.groups_data`.
2. Создает выпадающий список, вызывая метод `self.create_dropdown()`, и сохраняет его в атрибуте `self.dropdown`.

**Примеры**:
```python
from pathlib import Path
json_file_path = Path('path/to/your/groups.json')
widget = FacebookGroupsWidget(json_file_path)
```

#### `create_dropdown(self) -> Dropdown`

**Назначение**: Создает и возвращает виджет выпадающего списка на основе данных групп.

**Возвращает**:
- `Dropdown`: Виджет выпадающего списка с URL групп Facebook.

**Как работает функция**:
1. Извлекает ключи (URL групп) из атрибута `self.groups_data.__dict__` и преобразует их в список.
2. Создает экземпляр класса `Dropdown` из библиотеки `ipywidgets`, передавая список URL групп в качестве опций, устанавливает описание виджета как "Facebook Groups:", и отключает возможность редактирования.
3. Возвращает созданный виджет выпадающего списка.

**Примеры**:
```python
from pathlib import Path
json_file_path = Path('path/to/your/groups.json')
widget = FacebookGroupsWidget(json_file_path)
dropdown = widget.create_dropdown()
```

#### `display_widget(self)`

**Назначение**: Отображает виджет выпадающего списка.

**Как работает функция**:
1. Использует функцию `display` из библиотеки `IPython.display` для отображения виджета выпадающего списка `self.dropdown`.

**Примеры**:
```python
from pathlib import Path
json_file_path = Path('path/to/your/groups.json')
widget = FacebookGroupsWidget(json_file_path)
widget.display_widget()
```