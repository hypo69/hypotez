### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода создает виджет выпадающего списка с URL-адресами групп Facebook. Он инициализируется путем загрузки данных групп из JSON-файла, а затем создает и отображает выпадающий список, позволяющий пользователю выбирать группы Facebook.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `header`, `display`, `Dropdown`, `j_loads_ns`, `SimpleNamespace` и `Path`.
2. **Определение класса `FacebookGroupsWidget`**: Определяется класс для создания виджета выпадающего списка групп Facebook.
3. **Инициализация класса `FacebookGroupsWidget`**:
   - Функция `__init__` инициализирует виджет, принимая путь к JSON-файлу (`json_file_path`) в качестве аргумента.
   - Функция `j_loads_ns` загружает данные групп из JSON-файла и сохраняет их в атрибуте `groups_data` как `SimpleNamespace`.
   - Функция `create_dropdown` создает виджет выпадающего списка и сохраняет его в атрибуте `dropdown`.
4. **Создание выпадающего списка (`create_dropdown`)**:
   - Функция `create_dropdown` извлекает URL-адреса групп из `groups_data`.
   - Создается виджет `Dropdown` с URL-адресами групп в качестве опций.
   - Функция возвращает созданный виджет `Dropdown`.
5. **Отображение виджета (`display_widget`)**:
   - Функция `display_widget` использует функцию `display` для отображения виджета выпадающего списка.

Пример использования
-------------------------

```python
from pathlib import Path
from src.endpoints.advertisement.facebook.facebook_groups_widgets import FacebookGroupsWidget
from IPython.display import display

# Укажите путь к JSON-файлу с данными о группах Facebook
json_file_path = Path('path/to/your/groups_data.json')

# Создайте экземпляр виджета FacebookGroupsWidget
groups_widget = FacebookGroupsWidget(json_file_path)

# Отобразите виджет выпадающего списка
groups_widget.display_widget()

# Чтобы получить выбранное значение из выпадающего списка:
# selected_group_url = groups_widget.dropdown.value
# print(f"Выбранный URL группы: {selected_group_url}")
```