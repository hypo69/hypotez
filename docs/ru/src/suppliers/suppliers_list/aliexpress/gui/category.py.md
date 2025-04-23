# Модуль `category`

## Обзор

Модуль `category.py` предоставляет графический интерфейс (GUI) для подготовки рекламных кампаний AliExpress. Он позволяет загружать JSON-файлы с категориями товаров, отображать информацию о кампаниях и категориях, а также подготавливать все категории или конкретную категорию в асинхронном режиме.

## Подробней

Модуль использует библиотеку `PyQt6` для создания графического интерфейса, `qasync` для асинхронного выполнения задач и модуль `src.utils.jjson` для загрузки и сохранения JSON-данных. Он также взаимодействует с модулем `AliCampaignEditor` для подготовки кампаний.

## Классы

### `CategoryEditor`

**Описание**: Класс `CategoryEditor` представляет собой виджет (окно) для редактирования категорий кампании.

**Наследует**:
- `QtWidgets.QWidget`: Базовый класс для всех виджетов в PyQt6.

**Атрибуты**:
- `campaign_name` (str): Имя кампании.
- `data` (SimpleNamespace): Данные кампании, загруженные из JSON-файла.
- `language` (str): Язык кампании (по умолчанию 'EN').
- `currency` (str): Валюта кампании (по умолчанию 'USD').
- `file_path` (str): Путь к файлу кампании.
- `editor` (AliCampaignEditor): Экземпляр класса `AliCampaignEditor` для подготовки кампании.
- `main_app`: Ссылка на главный экземпляр приложения.
- `open_button` (QtWidgets.QPushButton): Кнопка для открытия JSON-файла.
- `file_name_label` (QtWidgets.QLabel): Метка для отображения имени выбранного файла.
- `prepare_all_button` (QtWidgets.QPushButton): Кнопка для подготовки всех категорий.
- `prepare_specific_button` (QtWidgets.QPushButton): Кнопка для подготовки конкретной категории.

**Методы**:

- `__init__(self, parent=None, main_app=None)`: Инициализирует окно редактора категорий.
- `setup_ui(self)`: Настраивает пользовательский интерфейс.
- `setup_connections(self)`: Настраивает соединения между сигналами и слотами.
- `open_file(self)`: Открывает диалоговое окно для выбора JSON-файла и загружает его.
- `load_file(self, campaign_file)`: Загружает JSON-файл кампании.
- `create_widgets(self, data)`: Создает виджеты на основе данных, загруженных из JSON-файла.
- `prepare_all_categories_async(self)`: Асинхронно подготавливает все категории.
- `prepare_category_async(self)`: Асинхронно подготавливает указанную категорию.

### `__init__`

```python
def __init__(self, parent=None, main_app=None):
    """ Initialize the main window"""
```

**Назначение**:
Инициализирует класс `CategoryEditor`.

**Параметры**:
- `parent` (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
- `main_app` (optional): Ссылка на главный экземпляр приложения. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `QtWidgets.QWidget`.
- Сохраняет ссылку на экземпляр `MainApp`.
- Вызывает методы `setup_ui()` и `setup_connections()` для настройки интерфейса и соединений.

### `setup_ui`

```python
def setup_ui(self):
    """ Setup the user interface"""
```

**Назначение**:
Настраивает пользовательский интерфейс виджета.

**Как работает функция**:
- Устанавливает заголовок окна как "Category Editor".
- Устанавливает размер окна 1800x800 пикселей.
- Определяет компоненты пользовательского интерфейса:
  - `open_button`: Кнопка "Open JSON File" для открытия файла. При нажатии вызывается метод `open_file`.
  - `file_name_label`: Метка "No file selected" для отображения имени файла.
  - `prepare_all_button`: Кнопка "Prepare All Categories" для подготовки всех категорий. При нажатии вызывается метод `prepare_all_categories_async`.
  - `prepare_specific_button`: Кнопка "Prepare Category" для подготовки определенной категории. При нажатии вызывается метод `prepare_category_async`.
- Создает вертикальный макет (`QVBoxLayout`) и добавляет в него компоненты.
- Устанавливает макет для виджета.

### `setup_connections`

```python
def setup_connections(self):
    """ Setup signal-slot connections"""
```

**Назначение**:
Настраивает соединения между сигналами и слотами.

**Как работает функция**:
- В текущей реализации функция пуста, но может быть использована для установки связей между сигналами и слотами в будущем.

### `open_file`

```python
def open_file(self):
    """ Open a file dialog to select and load a JSON file """
```

**Назначение**:
Открывает диалоговое окно для выбора JSON-файла и загружает его.

**Как работает функция**:
- Открывает диалоговое окно с помощью `QtWidgets.QFileDialog.getOpenFileName()` для выбора JSON-файла.
- Если файл выбран, вызывает метод `load_file()` для загрузки содержимого файла.

### `load_file`

```python
def load_file(self, campaign_file):
    """ Load a JSON file """
```

**Назначение**:
Загружает JSON-файл кампании.

**Параметры**:
- `campaign_file` (str): Путь к JSON-файлу кампании.

**Как работает функция**:
- Пытается загрузить данные из указанного файла с использованием `j_loads_ns()`.
- Сохраняет путь к файлу в `self.campaign_file` и устанавливает текст метки `self.file_name_label`.
- Извлекает имя кампании из загруженных данных и сохраняет его в `self.campaign_name`.
- Извлекает язык кампании из имени файла (без расширения) и сохраняет его в `self.language`.
- Создает экземпляр класса `AliCampaignEditor`, передавая путь к файлу кампании.
- Вызывает метод `create_widgets()` для создания виджетов на основе загруженных данных.
- В случае ошибки отображает сообщение об ошибке с использованием `QtWidgets.QMessageBox.critical()`.

### `create_widgets`

```python
def create_widgets(self, data):
    """ Create widgets based on the data loaded from the JSON file """
```

**Назначение**:
Создает виджеты на основе данных, загруженных из JSON-файла.

**Параметры**:
- `data` (SimpleNamespace): Данные кампании, загруженные из JSON-файла.

**Как работает функция**:
- Получает макет (`layout`) виджета.
- Удаляет предыдущие виджеты из макета, за исключением кнопок `open_button`, `file_name_label`, `prepare_all_button`, `prepare_specific_button`.
- Создает метку для отображения заголовка кампании (`title_label`) и добавляет ее в макет.
- Создает метку для отображения имени кампании (`campaign_label`) и добавляет ее в макет.
- Перебирает категории в данных кампании и создает метки для отображения имени каждой категории (`category_label`), добавляя их в макет.

### `prepare_all_categories_async`

```python
@asyncSlot()
async def prepare_all_categories_async(self):
    """ Asynchronously prepare all categories """
```

**Назначение**:
Асинхронно подготавливает все категории.

**Как работает функция**:
- Проверяет, инициализирован ли редактор (`self.editor`).
- Вызывает асинхронный метод `prepare_all_categories()` редактора.
- В случае успеха отображает сообщение об успехе с использованием `QtWidgets.QMessageBox.information()`.
- В случае ошибки отображает сообщение об ошибке с использованием `QtWidgets.QMessageBox.critical()`.

### `prepare_category_async`

```python
@asyncSlot()
async def prepare_category_async(self):
    """ Asynchronously prepare a specific category """
```

**Назначение**:
Асинхронно подготавливает указанную категорию.

**Как работает функция**:
- Проверяет, инициализирован ли редактор (`self.editor`).
- Вызывает асинхронный метод `prepare_category()` редактора, передавая имя кампании.
- В случае успеха отображает сообщение об успехе с использованием `QtWidgets.QMessageBox.information()`.
- В случае ошибки отображает сообщение об ошибке с использованием `QtWidgets.QMessageBox.critical()`.