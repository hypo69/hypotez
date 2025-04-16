# Модуль для создания выпадающего списка групп Facebook

## Обзор

Модуль `src.endpoints.advertisement.facebook.facebook_groups_widgets` предназначен для создания выпадающего списка с URL групп Facebook.

## Подробней

Модуль предоставляет класс `FacebookGroupsWidget`, который создает выпадающий список с URL групп Facebook из предоставленного JSON.

## Классы

### `FacebookGroupsWidget`

**Описание**: Создает выпадающий список с URL групп Facebook из предоставленного JSON.

**Атрибуты**:

*   `groups_data` (SimpleNamespace): Данные о группах, загруженные из JSON-файла.
*   `dropdown` (Dropdown): Виджет выпадающего списка.

**Методы**:

*   `__init__(self, json_file_path: Path)`: Инициализирует виджет с выпадающим списком для групп Facebook.
*   `create_dropdown(self) -> Dropdown`: Создает и возвращает виджет выпадающего списка на основе данных групп.
*   `display_widget(self)`: Отображает виджет выпадающего списка.

## Методы класса `FacebookGroupsWidget`

### `__init__`

```python
def __init__(self, json_file_path: Path):
```

**Назначение**: Инициализирует виджет с выпадающим списком для групп Facebook.

**Параметры**:

*   `json_file_path` (Path): Путь к JSON-файлу, содержащему информацию о группах Facebook.

**Как работает функция**:

1.  Загружает данные о группах из JSON-файла, используя `j_loads_ns`.
2.  Создает виджет выпадающего списка, вызывая метод `create_dropdown`.

### `create_dropdown`

```python
def create_dropdown(self) -> Dropdown:
```

**Назначение**: Создает и возвращает виджет выпадающего списка на основе данных групп.

**Возвращает**:

*   `Dropdown`: Виджет выпадающего списка с URL групп Facebook.

**Как работает функция**:

1.  Извлекает ключи (URL групп) из `self.groups_data`.
2.  Создает виджет `Dropdown` с URL групп в качестве опций.
3.  Устанавливает описание виджета в "Facebook Groups:".
4.  Возвращает созданный виджет `Dropdown`.

### `display_widget`

```python
def display_widget(self):
```

**Назначение**: Отображает виджет выпадающего списка.

**Как работает функция**:

1.  Использует функцию `display` из библиотеки `IPython.display` для отображения виджета `self.dropdown`.