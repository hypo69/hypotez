# Модуль `category.py`

## Обзор

Модуль `category.py` предоставляет графический интерфейс для редактирования категорий рекламных кампаний AliExpress. Он позволяет открывать JSON-файлы с данными о кампаниях, отображать информацию о категориях и подготавливать все категории или конкретную категорию асинхронно.

## Подробней

Этот модуль является частью GUI приложения и предназначен для упрощения работы с категориями рекламных кампаний AliExpress. Он использует библиотеку PyQt6 для создания интерфейса и `AliCampaignEditor` для подготовки категорий.

## Классы

### `CategoryEditor`

**Описание**: Главный класс виджета для редактирования категорий.

**Наследует**:

- `QtWidgets.QWidget`: Базовый класс для всех виджетов PyQt6.

**Атрибуты**:

- `campaign_name` (str): Имя кампании.
- `data` (`SimpleNamespace`): Данные, загруженные из JSON-файла.
- `language` (str): Язык кампании (по умолчанию 'EN').
- `currency` (str): Валюта кампании (по умолчанию 'USD').
- `file_path` (str): Путь к файлу кампании.
- `editor` (`AliCampaignEditor`): Экземпляр класса `AliCampaignEditor` для подготовки категорий.
- `main_app`: Ссылка на главный экземпляр приложения.
- `open_button`: Кнопка для открытия JSON файла.
- `file_name_label`: Метка для отображения имени файла.
- `prepare_all_button`: Кнопка для подготовки всех категорий.
- `prepare_specific_button`: Кнопка для подготовки конкретной категории.

**Методы**:

- `__init__(self, parent=None, main_app=None)`: Инициализирует главный интерфейс окна.
- `setup_ui(self)`: Настраивает пользовательский интерфейс.
- `setup_connections(self)`: Устанавливает связи между сигналами и слотами.
- `open_file(self)`: Открывает диалоговое окно выбора файла для загрузки JSON-файла.
- `load_file(self, campaign_file)`: Загружает JSON-файл.
- `create_widgets(self, data)`: Создает виджеты на основе данных, загруженных из JSON-файла.
- `prepare_all_categories_async(self)`: Асинхронно подготавливает все категории.
- `prepare_category_async(self)`: Асинхронно подготавливает конкретную категорию.

### `__init__`

```python
def __init__(self, parent=None, main_app=None):
    """ Initialize the main window"""
    super().__init__(parent)
    self.main_app = main_app  # Save the MainApp instance

    self.setup_ui()
    self.setup_connections()
```

**Назначение**: Инициализирует окно редактора категорий.

**Параметры**:

- `parent` (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
- `main_app` (MainApp, optional): Главный экземпляр приложения. По умолчанию `None`.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `QtWidgets.QWidget`.
2.  Сохраняет ссылку на главный экземпляр приложения `main_app`.
3.  Вызывает методы `setup_ui()` и `setup_connections()` для настройки пользовательского интерфейса и связей между сигналами и слотами.

### `setup_ui`

```python
def setup_ui(self):
    """ Setup the user interface"""
    self.setWindowTitle("Category Editor")
    self.resize(1800, 800)

    # Define UI components
    self.open_button = QtWidgets.QPushButton("Open JSON File")
    self.open_button.clicked.connect(self.open_file)

    self.file_name_label = QtWidgets.QLabel("No file selected")

    self.prepare_all_button = QtWidgets.QPushButton("Prepare All Categories")
    self.prepare_all_button.clicked.connect(self.prepare_all_categories_async)

    self.prepare_specific_button = QtWidgets.QPushButton("Prepare Category")
    self.prepare_specific_button.clicked.connect(self.prepare_category_async)

    layout = QtWidgets.QVBoxLayout(self)
    layout.addWidget(self.open_button)
    layout.addWidget(self.file_name_label)
    layout.addWidget(self.prepare_all_button)
    layout.addWidget(self.prepare_specific_button)

    self.setLayout(layout)
```

**Назначение**: Настраивает пользовательский интерфейс окна редактора категорий.

**Как работает функция**:

1.  Устанавливает заголовок окна как "Category Editor".
2.  Устанавливает размеры окна как 1800x800 пикселей.
3.  Определяет компоненты пользовательского интерфейса:
    *   Кнопку "Open JSON File" (`open_button`), связывая её с методом `open_file()`.
    *   Метку `file_name_label` для отображения имени выбранного файла.
    *   Кнопку "Prepare All Categories" (`prepare_all_button`), связывая её с методом `prepare_all_categories_async()`.
    *   Кнопку "Prepare Category" (`prepare_specific_button`), связывая её с методом `prepare_category_async()`.
4.  Создает вертикальный макет (`QVBoxLayout`) и добавляет в него созданные компоненты.
5.  Устанавливает созданный макет для виджета.

### `setup_connections`

```python
def setup_connections(self):
    """ Setup signal-slot connections"""
    pass
```

**Назначение**: Устанавливает связи между сигналами и слотами.

**Как работает функция**:

Функция пока не содержит реализацию и предназначена для установки связей между сигналами и слотами, если это потребуется в будущем.

### `open_file`

```python
def open_file(self):
    """ Open a file dialog to select and load a JSON file """
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
        self,
        "Open JSON File",
        "c:/user/documents/repos/hypotez/data/aliexpress/campaigns",
        "JSON files (*.json)"
    )
    if not file_path:
        return  # No file selected

    self.load_file(file_path)
```

**Назначение**: Открывает диалоговое окно выбора файла для загрузки JSON-файла.

**Как работает функция**:

1.  Открывает диалоговое окно выбора файла с помощью `QtWidgets.QFileDialog.getOpenFileName()`.
2.  Устанавливает заголовок окна как "Open JSON File".
3.  Устанавливает начальный каталог для поиска файлов.
4.  Устанавливает фильтр для отображения только JSON-файлов.
5.  Если файл не выбран (путь к файлу пустой), функция завершается.
6.  Вызывает метод `load_file()` для загрузки выбранного файла.

### `load_file`

```python
def load_file(self, campaign_file):
    """ Load a JSON file """
    try:
        self.data = j_loads_ns(campaign_file)
        self.campaign_file = campaign_file
        self.file_name_label.setText(f"File: {self.campaign_file}")
        self.campaign_name = self.data.campaign_name
        path = Path(campaign_file)
        self.language = path.stem  # This will give you the file name without extension
        self.editor = AliCampaignEditor(campaign_file=campaign_file)
        self.create_widgets(self.data)
    except Exception as ex:
        QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")
```

**Назначение**: Загружает JSON-файл.

**Параметры**:

- `campaign_file` (str): Путь к JSON-файлу.

**Как работает функция**:

1.  Пытается загрузить JSON-файл с использованием функции `j_loads_ns()`.
2.  Сохраняет путь к файлу в атрибуте `campaign_file`.
3.  Устанавливает текст метки `file_name_label` с именем загруженного файла.
4.  Извлекает имя кампании из загруженных данных и сохраняет его в атрибуте `campaign_name`.
5.  Извлекает язык кампании из имени файла без расширения.
6.  Создает экземпляр класса `AliCampaignEditor`, передавая путь к файлу кампании.
7.  Вызывает метод `create_widgets()` для создания виджетов на основе загруженных данных.
8.  В случае возникновения исключения отображает сообщение об ошибке с использованием `QtWidgets.QMessageBox.critical()`.

### `create_widgets`

```python
def create_widgets(self, data):
    """ Create widgets based on the data loaded from the JSON file """
    layout = self.layout()

    # Remove previous widgets except open button and file label
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget not in [self.open_button, self.file_name_label, self.prepare_all_button, self.prepare_specific_button]:
            widget.deleteLater()

    title_label = QtWidgets.QLabel(f"Title: {data.title}")
    layout.addWidget(title_label)

    campaign_label = QtWidgets.QLabel(f"Campaign Name: {data.campaign_name}")
    layout.addWidget(campaign_label)

    # Correct way to handle SimpleNamespace as a dict
    for category in data.categories:
        category_label = QtWidgets.QLabel(f"Category: {category.name}")
        layout.addWidget(category_label)
```

**Назначение**: Создает виджеты на основе данных, загруженных из JSON-файла.

**Параметры**:

- `data` (`SimpleNamespace`): Данные, загруженные из JSON-файла.

**Как работает функция**:

1.  Получает макет виджета.
2.  Удаляет все предыдущие виджеты из макета, кроме кнопок `open_button`, `file_name_label`, `prepare_all_button`, `prepare_specific_button`.
3.  Создает метку с заголовком кампании (`title_label`) и добавляет её в макет.
4.  Создает метку с именем кампании (`campaign_label`) и добавляет её в макет.
5.  Перебирает категории в данных и для каждой категории создает метку с именем категории (`category_label`), добавляя её в макет.

### `prepare_all_categories_async`

```python
@asyncSlot()
async def prepare_all_categories_async(self):
    """ Asynchronously prepare all categories """
    if self.editor:
        try:
            await self.editor.prepare_all_categories()
            QtWidgets.QMessageBox.information(self, "Success", "All categories prepared successfully.")
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to prepare all categories: {ex}")
```

**Назначение**: Асинхронно подготавливает все категории.

**Как работает функция**:

1.  Проверяет, инициализирован ли редактор (`self.editor`).
2.  Если редактор инициализирован, пытается асинхронно подготовить все категории с помощью метода `self.editor.prepare_all_categories()`.
3.  В случае успеха отображает сообщение об успехе с использованием `QtWidgets.QMessageBox.information()`.
4.  В случае возникновения исключения отображает сообщение об ошибке с использованием `QtWidgets.QMessageBox.critical()`.

### `prepare_category_async`

```python
@asyncSlot()
async def prepare_category_async(self):
    """ Asynchronously prepare a specific category """
    if self.editor:
        try:
            await self.editor.prepare_category(self.data.campaign_name)
            QtWidgets.QMessageBox.information(self, "Success", "Category prepared successfully.")
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to prepare category: {ex}")
```

**Назначение**: Асинхронно подготавливает конкретную категорию.

**Как работает функция**:

1.  Проверяет, инициализирован ли редактор (`self.editor`).
2.  Если редактор инициализирован, пытается асинхронно подготовить конкретную категорию с помощью метода `self.editor.prepare_category()`, передавая имя кампании.
3.  В случае успеха отображает сообщение об успехе с использованием `QtWidgets.QMessageBox.information()`.
4.  В случае возникновения исключения отображает сообщение об ошибке с использованием `QtWidgets.QMessageBox.critical()`.