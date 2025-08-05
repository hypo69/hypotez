# Модуль FacebookGroupsWidget

## Обзор

Модуль `facebook_groups_widgets.py` предоставляет класс `FacebookGroupsWidget`, который создает выпадающий список с URL групп Facebook из предоставленного JSON-файла. Используется для подачи объявлений в группы Facebook.

## Подробней

Модуль `facebook_groups_widgets.py`  создает виджет выпадающего списка для выбора групп Facebook. Использует JSON-файл с информацией о группах, извлекает из него данные и генерирует список групп. 

## Классы

### `FacebookGroupsWidget`

**Описание**: Класс `FacebookGroupsWidget` создает выпадающий список с URL групп Facebook из предоставленного JSON-файла.

**Атрибуты**:

- `groups_data` (SimpleNamespace): Данные о группах Facebook из JSON-файла.
- `dropdown` (Dropdown): Виджет выпадающего списка с URL групп Facebook.

**Методы**:

- `__init__(self, json_file_path: Path)`: Инициализация виджета с выпадающим списком для групп Facebook.
- `create_dropdown(self) -> Dropdown`: Создает и возвращает виджет выпадающего списка на основе данных групп.
- `display_widget(self)`: Отображает виджет выпадающего списка.

**Принцип работы**:

1. В конструкторе класса `__init__`  извлекаются данные о группах Facebook из JSON-файла.
2. Метод `create_dropdown` создает виджет выпадающего списка (`Dropdown`) с помощью библиотеки `ipywidgets`.
3. Метод `display_widget` отображает созданный виджет выпадающего списка.

### `__init__(self, json_file_path: Path)`

**Назначение**: Инициализация виджета с выпадающим списком для групп Facebook.

**Параметры**:

- `json_file_path` (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.

**Как работает**:

- Извлекает данные о группах Facebook из JSON-файла с помощью `j_loads_ns`.
- Сохраняет извлеченные данные в `self.groups_data` для дальнейшего использования.

### `create_dropdown(self) -> Dropdown`

**Назначение**: Создает и возвращает виджет выпадающего списка на основе данных групп.

**Параметры**:

- `None`

**Возвращает**:

- `Dropdown`: Виджет выпадающего списка с URL групп Facebook.

**Как работает**:

1. Получает список URL групп из `self.groups_data`.
2. Создает виджет выпадающего списка (`Dropdown`) с помощью `ipywidgets`.
3. Устанавливает список URL групп как варианты выбора.
4. Возвращает созданный виджет `Dropdown`.


### `display_widget(self)`

**Назначение**: Отображает виджет выпадающего списка.

**Параметры**:

- `None`

**Как работает**:

- Использует функцию `display` из `IPython.display` для отображения виджета `self.dropdown`.


## Примеры

```python
from pathlib import Path

# Путь к JSON-файлу с данными о группах
json_file_path = Path('path/to/facebook_groups.json')

# Создание экземпляра виджета
groups_widget = FacebookGroupsWidget(json_file_path)

# Отображение виджета
groups_widget.display_widget()
```

##  Внутренние функции 

В коде нет внутренних функций.