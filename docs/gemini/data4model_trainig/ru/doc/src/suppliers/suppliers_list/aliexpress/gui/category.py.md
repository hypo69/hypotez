# Модуль `category.py`

## Обзор

Модуль `category.py` предоставляет графический интерфейс (GUI) для подготовки рекламных кампаний AliExpress. Он позволяет пользователю загружать JSON-файлы с данными о кампаниях, просматривать категории и подготавливать их к использованию.

## Подробней

Модуль использует библиотеку PyQt6 для создания интерфейса. Он включает в себя кнопки для открытия JSON-файлов, отображения информации о файле и подготовки категорий. Основной класс `CategoryEditor` управляет интерфейсом и взаимодействием с классом `AliCampaignEditor` для подготовки кампаний.

## Классы

### `CategoryEditor`

**Описание**:
Класс `CategoryEditor` представляет собой виджет (окно) для редактирования категорий. Он позволяет загружать JSON-файлы с информацией о категориях, отображать эту информацию и запускать процесс подготовки категорий.

**Наследует**:
`QtWidgets.QWidget`

**Атрибуты**:
- `campaign_name` (str): Имя кампании.
- `data` (SimpleNamespace): Данные, загруженные из JSON-файла.
- `language` (str): Язык кампании (по умолчанию 'EN').
- `currency` (str): Валюта кампании (по умолчанию 'USD').
- `file_path` (str): Путь к файлу кампании.
- `editor` (AliCampaignEditor): Экземпляр класса `AliCampaignEditor` для подготовки кампании.
- `main_app` (QtWidgets.QApplication): Главное приложение PyQt6.
- `open_button` (QtWidgets.QPushButton): Кнопка для открытия JSON-файла.
- `file_name_label` (QtWidgets.QLabel): Метка для отображения имени выбранного файла.
- `prepare_all_button` (QtWidgets.QPushButton): Кнопка для подготовки всех категорий.
- `prepare_specific_button` (QtWidgets.QPushButton): Кнопка для подготовки выбранной категории.

**Методы**:
- `__init__(self, parent=None, main_app=None)`: Инициализирует виджет, настраивает пользовательский интерфейс и соединения сигналов и слотов.
- `setup_ui(self)`: Создаёт и настраивает элементы пользовательского интерфейса.
- `setup_connections(self)`: Устанавливает соединения между сигналами и слотами.
- `open_file(self)`: Открывает диалоговое окно для выбора JSON-файла.
- `load_file(self, campaign_file)`: Загружает JSON-файл и создает виджеты на основе данных из файла.
- `create_widgets(self, data)`: Создает виджеты для отображения информации о категориях.
- `prepare_all_categories_async(self)`: Асинхронно подготавливает все категории.
- `prepare_category_async(self)`: Асинхронно подготавливает выбранную категорию.

## Методы класса

### `__init__`

```python
def __init__(self, parent=None, main_app=None):
    """ Initialize the main window"""
    super().__init__(parent)
    self.main_app = main_app  # Save the MainApp instance

    self.setup_ui()
    self.setup_connections()
```

**Назначение**:
Инициализирует экземпляр класса `CategoryEditor`.

**Параметры**:
- `parent` (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
- `main_app` (QtWidgets.QApplication, optional): Экземпляр главного приложения. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `QtWidgets.QWidget`.
- Сохраняет ссылку на главное приложение в атрибуте `self.main_app`.
- Вызывает методы `self.setup_ui()` и `self.setup_connections()` для настройки пользовательского интерфейса и соединений.

**Примеры**:
```python
app = QtWidgets.QApplication([])
editor = CategoryEditor(main_app=app)
editor.show()
app.exec()
```

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

**Назначение**:
Настраивает пользовательский интерфейс виджета.

**Как работает функция**:
- Устанавливает заголовок окна.
- Устанавливает размеры окна.
- Создает кнопки "Open JSON File", "Prepare All Categories" и "Prepare Category".
- Создает метку для отображения имени файла.
- Устанавливает вертикальную компоновку и добавляет виджеты в компоновку.
- Устанавливает компоновку для виджета.

**Примеры**:
```python
editor = CategoryEditor()
editor.setup_ui()
```

### `setup_connections`

```python
def setup_connections(self):
    """ Setup signal-slot connections"""
    pass
```

**Назначение**:
Настраивает соединения между сигналами и слотами.

**Как работает функция**:
- В данном примере функция пуста, но может быть расширена для установки соединений между сигналами и слотами.

**Примеры**:
```python
editor = CategoryEditor()
editor.setup_connections()
```

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

**Назначение**:
Открывает диалоговое окно для выбора JSON-файла.

**Как работает функция**:
- Открывает диалоговое окно с помощью `QtWidgets.QFileDialog.getOpenFileName`.
- Если файл выбран, вызывает метод `self.load_file` для загрузки файла.

**Примеры**:
```python
editor = CategoryEditor()
editor.open_file()
```

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

**Назначение**:
Загружает JSON-файл.

**Параметры**:
- `campaign_file` (str): Путь к файлу кампании.

**Как работает функция**:
- Пытается загрузить JSON-файл с использованием `j_loads_ns`.
- Сохраняет путь к файлу и имя кампании.
- Извлекает язык из имени файла.
- Создает экземпляр класса `AliCampaignEditor`.
- Вызывает метод `self.create_widgets` для создания виджетов на основе данных из файла.
- В случае ошибки отображает сообщение об ошибке.

**Примеры**:
```python
editor = CategoryEditor()
editor.load_file('path/to/campaign.json')
```

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

**Назначение**:
Создает виджеты для отображения информации о категориях.

**Параметры**:
- `data` (SimpleNamespace): Данные о кампаниях и категориях.

**Как работает функция**:
- Получает текущую компоновку виджета.
- Удаляет все предыдущие виджеты, кроме кнопок открытия файла и меток имен файлов.
- Создает метки для отображения названия кампании и категорий.
- Добавляет метки в компоновку.

**Примеры**:
```python
data = SimpleNamespace(title='Test Campaign', campaign_name='test', categories=[SimpleNamespace(name='Category 1'), SimpleNamespace(name='Category 2')])
editor = CategoryEditor()
editor.create_widgets(data)
```

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

**Назначение**:
Асинхронно подготавливает все категории.

**Как работает функция**:
- Проверяет, создан ли экземпляр `self.editor`.
- Вызывает метод `self.editor.prepare_all_categories` асинхронно.
- Отображает сообщение об успешном завершении или сообщение об ошибке.

**Примеры**:
```python
editor = CategoryEditor()
asyncio.run(editor.prepare_all_categories_async())
```

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

**Назначение**:
Асинхронно подготавливает выбранную категорию.

**Как работает функция**:
- Проверяет, создан ли экземпляр `self.editor`.
- Вызывает метод `self.editor.prepare_category` асинхронно.
- Отображает сообщение об успешном завершении или сообщение об ошибке.

**Примеры**:
```python
editor = CategoryEditor()
asyncio.run(editor.prepare_category_async())
```