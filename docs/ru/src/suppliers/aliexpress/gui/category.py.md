# Модуль `category`

## Обзор

Модуль `category.py` предоставляет класс `CategoryEditor`, который представляет собой графический интерфейс для подготовки рекламных кампаний AliExpress на основе данных из JSON-файлов. Он позволяет открывать JSON-файлы с данными о кампаниях, отображать основную информацию о кампании и категориях, а также запускать асинхронную подготовку всех или конкретной категории.

## Подробнее

Модуль использует библиотеки `PyQt6` для создания графического интерфейса, `qasync` для асинхронного выполнения задач, `src.utils.jjson` для загрузки и сохранения JSON-данных, а также `src.suppliers.aliexpress.campaign.AliCampaignEditor` для подготовки кампаний AliExpress. Расположение файла в проекте указывает на то, что он является частью графического интерфейса для управления кампаниями AliExpress.

## Классы

### `CategoryEditor`

**Описание**: Класс `CategoryEditor` представляет собой виджет (окно) для редактирования категорий кампании. Он позволяет загружать данные о категориях из JSON-файла, отображать их в пользовательском интерфейсе и запускать процесс подготовки категорий (всех или выбранной).

**Наследует**:
- `QtWidgets.QWidget`

**Атрибуты**:
- `campaign_name` (str): Имя кампании.
- `data` (SimpleNamespace): Данные кампании, загруженные из JSON-файла.
- `language` (str): Язык кампании, по умолчанию `'EN'`.
- `currency` (str): Валюта кампании, по умолчанию `'USD'`.
- `file_path` (str): Путь к файлу кампании.
- `editor` (AliCampaignEditor): Экземпляр класса `AliCampaignEditor` для подготовки кампании.
- `main_app` (MainApp): Ссылка на главный экземпляр приложения.
- `open_button` (QtWidgets.QPushButton): Кнопка для открытия JSON-файла.
- `file_name_label` (QtWidgets.QLabel): Метка для отображения имени выбранного файла.
- `prepare_all_button` (QtWidgets.QPushButton): Кнопка для подготовки всех категорий.
- `prepare_specific_button` (QtWidgets.QPushButton): Кнопка для подготовки конкретной категории.

**Принцип работы**:

1.  При инициализации создаются и настраиваются основные элементы интерфейса: кнопки, метки и макет.
2.  При нажатии на кнопку "Open JSON File" открывается диалоговое окно выбора файла, и выбранный файл загружается.
3.  После загрузки файла создаются виджеты для отображения информации о кампании и категориях.
4.  При нажатии на кнопки "Prepare All Categories" или "Prepare Category" запускается соответствующий асинхронный метод для подготовки категорий.

### Методы класса

#### `__init__`

```python
def __init__(self, parent=None, main_app=None):
    """ Initialize the main window"""
```

**Назначение**: Инициализирует экземпляр класса `CategoryEditor`.

**Параметры**:
- `parent` (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
- `main_app` (MainApp, optional): Экземпляр главного приложения. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор базового класса `QtWidgets.QWidget`.
- Сохраняет ссылку на главный экземпляр приложения в атрибуте `self.main_app`.
- Вызывает методы `setup_ui()` и `setup_connections()` для настройки пользовательского интерфейса и связей между сигналами и слотами.

#### `setup_ui`

```python
def setup_ui(self):
    """ Setup the user interface"""
```

**Назначение**: Настраивает пользовательский интерфейс виджета.

**Как работает функция**:
- Устанавливает заголовок окна.
- Устанавливает размеры окна.
- Создает кнопки "Open JSON File", "Prepare All Categories" и "Prepare Category".
- Создает метку для отображения имени файла.
- Устанавливает обработчики нажатия кнопок `open_file`, `prepare_all_categories_async` и `prepare_category_async`.
- Добавляет виджеты в вертикальный макет.
- Устанавливает макет для виджета.

#### `setup_connections`

```python
def setup_connections(self):
    """ Setup signal-slot connections"""
```

**Назначение**: Настраивает связи между сигналами и слотами. В данном случае, метод пустой.

**Как работает функция**:
- В данном примере функция ничего не делает, но может быть использована для установки связей между сигналами и слотами в будущем.

#### `open_file`

```python
def open_file(self):
    """ Open a file dialog to select and load a JSON file """
```

**Назначение**: Открывает диалоговое окно выбора файла и загружает выбранный JSON-файл.

**Как работает функция**:
- Открывает диалоговое окно с помощью `QtWidgets.QFileDialog.getOpenFileName()`.
- Если файл выбран, вызывает метод `load_file()` для загрузки содержимого файла.

#### `load_file`

```python
def load_file(self, campaign_file):
    """ Load a JSON file """
```

**Назначение**: Загружает JSON-файл и отображает данные в интерфейсе.

**Параметры**:
- `campaign_file` (str): Путь к JSON-файлу.

**Как работает функция**:
- Загружает JSON-данные из файла с помощью `j_loads_ns()`.
- Сохраняет путь к файлу в атрибуте `self.campaign_file`.
- Извлекает имя кампании из данных и сохраняет в атрибуте `self.campaign_name`.
- Извлекает язык кампании из имени файла и сохраняет в атрибуте `self.language`.
- Создает экземпляр класса `AliCampaignEditor` для подготовки кампании.
- Вызывает метод `create_widgets()` для создания виджетов на основе загруженных данных.
- В случае ошибки отображает сообщение об ошибке с помощью `QtWidgets.QMessageBox.critical()`.

#### `create_widgets`

```python
def create_widgets(self, data):
    """ Create widgets based on the data loaded from the JSON file """
```

**Назначение**: Создает виджеты для отображения данных из JSON-файла.

**Параметры**:
- `data` (SimpleNamespace): Данные кампании, загруженные из JSON-файла.

**Как работает функция**:
- Получает макет виджета.
- Удаляет все предыдущие виджеты из макета, кроме кнопок открытия файла и подготовки категорий, а также метки с именем файла.
- Создает метки для отображения заголовка и имени кампании.
- Для каждой категории создает метку с именем категории.
- Добавляет созданные виджеты в макет.

#### `prepare_all_categories_async`

```python
@asyncSlot()
async def prepare_all_categories_async(self):
    """ Asynchronously prepare all categories """
```

**Назначение**: Асинхронно подготавливает все категории кампании.

**Как работает функция**:
- Проверяет, инициализирован ли редактор кампании (`self.editor`).
- Вызывает метод `prepare_all_categories()` редактора кампании асинхронно.
- В случае успеха отображает сообщение об успехе с помощью `QtWidgets.QMessageBox.information()`.
- В случае ошибки отображает сообщение об ошибке с помощью `QtWidgets.QMessageBox.critical()`.

#### `prepare_category_async`

```python
@asyncSlot()
async def prepare_category_async(self):
    """ Asynchronously prepare a specific category """
```

**Назначение**: Асинхронно подготавливает указанную категорию кампании.

**Как работает функция**:
- Проверяет, инициализирован ли редактор кампании (`self.editor`).
- Вызывает метод `prepare_category()` редактора кампании асинхронно, передавая имя кампании.
- В случае успеха отображает сообщение об успехе с помощью `QtWidgets.QMessageBox.information()`.
- В случае ошибки отображает сообщение об ошибке с помощью `QtWidgets.QMessageBox.critical()`.

## Примеры

```python
# Пример создания и использования CategoryEditor
import sys
from PyQt6.QtWidgets import QApplication
from src.suppliers.aliexpress.gui.category import CategoryEditor

app = QApplication(sys.argv)
category_editor = CategoryEditor()
category_editor.show()
sys.exit(app.exec())
```
```python
# Открытие JSON-файла с данными о категориях
category_editor.open_file()
```
```python
# Подготовка всех категорий
category_editor.prepare_all_categories_async()
```
```python
# Подготовка конкретной категории
category_editor.prepare_category_async()