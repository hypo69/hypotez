# Модуль `facebook_groups_widgets`

## Обзор

Модуль `facebook_groups_widgets.py` предназначен для создания интерактивного виджета - выпадающего списка (dropdown) с перечнем групп Facebook. Этот виджет используется для выбора целевой группы при размещении рекламных объявлений. Модуль считывает данные о группах из JSON-файла и отображает их в виде списка, позволяя пользователю выбрать нужную группу.

## Подробней

Этот модуль облегчает выбор целевой группы Facebook для рекламных кампаний, предоставляя удобный пользовательский интерфейс в виде выпадающего списка. Он использует библиотеку `ipywidgets` для создания интерактивных элементов в Jupyter Notebook или подобных средах. JSON-файл, содержащий информацию о группах, загружается с использованием функции `j_loads_ns` из модуля `src.utils.jjson`, что обеспечивает удобное преобразование JSON-данных в пространство имен (`SimpleNamespace`).

## Классы

### `FacebookGroupsWidget`

**Описание**: Класс `FacebookGroupsWidget` создает виджет выпадающего списка с URL групп Facebook на основе данных, считанных из JSON-файла.

**Принцип работы**: Класс инициализируется путем загрузки данных о группах из JSON-файла, создает выпадающий список на основе этих данных и предоставляет метод для отображения виджета.

**Атрибуты**:
- `groups_data` (SimpleNamespace): Пространство имен, содержащее данные о группах Facebook, загруженные из JSON-файла.
- `dropdown` (Dropdown): Виджет выпадающего списка с URL групп Facebook.

**Методы**:
- `__init__(self, json_file_path: Path)`: Инициализирует класс, загружает данные о группах из JSON-файла и создает выпадающий список.
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
        self.groups_data: SimpleNamespace = j_loads_ns(json_file_path)
        self.dropdown = self.create_dropdown()
```

**Назначение**: Инициализирует экземпляр класса `FacebookGroupsWidget`.

**Параметры**:
- `json_file_path` (Path): Путь к JSON-файлу, содержащему данные о группах Facebook.

**Как работает функция**:
1. Загружает данные о группах Facebook из JSON-файла, используя функцию `j_loads_ns` из модуля `src.utils.jjson`. Результат сохраняется в атрибуте `groups_data` как `SimpleNamespace`.
2. Создает виджет выпадающего списка, вызывая метод `self.create_dropdown()`, и сохраняет его в атрибуте `self.dropdown`.

```ascii
JSON-файл --> j_loads_ns() --> groups_data
                                    |
                                    create_dropdown() --> dropdown
```

**Примеры**:
```python
from pathlib import Path
file_path = Path('groups.json')
widget = FacebookGroupsWidget(file_path)
```

### `create_dropdown`

```python
    def create_dropdown(self) -> Dropdown:
        """ Создает и возвращает виджет выпадающего списка на основе данных групп.

        Returns:
            Dropdown: Виджет выпадающего списка с URL групп Facebook.
        """
        group_urls = list(self.groups_data.__dict__.keys())
        dropdown = Dropdown(
            options=group_urls,
            description='Facebook Groups:',
            disabled=False,
        )
        return dropdown
```

**Назначение**: Создает и настраивает виджет выпадающего списка (`Dropdown`) на основе данных о группах Facebook.

**Возвращает**:
- `Dropdown`: Виджет выпадающего списка с URL групп Facebook.

**Как работает функция**:

1. Извлекает ключи (URL групп) из атрибута `self.groups_data.__dict__` и преобразует их в список.
2. Создает экземпляр класса `Dropdown` из библиотеки `ipywidgets`.
3. Устанавливает параметры виджета:
   - `options`: Список URL групп, которые будут отображаться в выпадающем списке.
   - `description`: Текст описания виджета ("Facebook Groups:").
   - `disabled`: Устанавливается в `False`, что означает, что виджет активен и доступен для выбора.
4. Возвращает созданный виджет `Dropdown`.

```ascii
groups_data --> Извлечение ключей --> Список URL групп
                                            |
                                            Создание Dropdown виджета с параметрами
                                            |
                                            Возврат Dropdown виджета
```

**Примеры**:

```python
from pathlib import Path
file_path = Path('groups.json')
widget = FacebookGroupsWidget(file_path)
dropdown = widget.create_dropdown()
```

### `display_widget`

```python
    def display_widget(self):
        """ Отображает виджет выпадающего списка."""
        display(self.dropdown)
```

**Назначение**: Отображает виджет выпадающего списка (`Dropdown`).

**Как работает функция**:
1. Вызывает функцию `display` из модуля `IPython.display` для отображения виджета `self.dropdown`.

```ascii
dropdown --> display() --> Отображение виджета
```

**Примеры**:
```python
from pathlib import Path
file_path = Path('groups.json')
widget = FacebookGroupsWidget(file_path)
widget.display_widget()
```
## Функции
В данном модуле функции отсутствуют