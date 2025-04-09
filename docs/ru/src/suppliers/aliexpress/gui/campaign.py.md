# Модуль `campaign`

## Обзор

Модуль `campaign.py` предоставляет графический интерфейс для редактирования и подготовки кампаний AliExpress. Он включает в себя класс `CampaignEditor`, который позволяет пользователю открывать JSON-файлы с данными кампаний, редактировать основные параметры (например, заголовок, описание и название продвижения) и подготавливать кампанию к дальнейшей обработке.

## Подробнее

Модуль использует библиотеку PyQt6 для создания графического интерфейса. Он позволяет загружать файлы конфигурации кампаний в формате JSON, отображать их содержимое в редактируемых полях и запускать процесс подготовки кампании. Этот модуль важен для визуального управления и настройки кампаний AliExpress перед их запуском.

## Классы

### `CampaignEditor`

**Описание**: Класс `CampaignEditor` представляет собой виджет для редактирования кампаний. Он предоставляет интерфейс для загрузки, отображения и изменения данных кампании, а также для запуска процесса подготовки кампании.

**Наследует**: `QtWidgets.QWidget`

**Атрибуты**:

- `data` (SimpleNamespace): Пространство имен, содержащее данные кампании.
- `current_campaign_file` (str): Путь к текущему открытому файлу кампании.
- `editor` (AliCampaignEditor): Объект редактора кампаний `AliCampaignEditor`.
- `main_app` (MainApp): Экземпляр главного приложения.
- `scroll_area` (QtWidgets.QScrollArea): Область прокрутки для содержимого.
- `scroll_content_widget` (QtWidgets.QWidget): Виджет содержимого области прокрутки.
- `layout` (QtWidgets.QGridLayout): Сетка для размещения виджетов.
- `open_button` (QtWidgets.QPushButton): Кнопка открытия файла.
- `file_name_label` (QtWidgets.QLabel): Метка с именем файла.
- `prepare_button` (QtWidgets.QPushButton): Кнопка подготовки кампании.
- `title_input` (QtWidgets.QLineEdit): Поле ввода для заголовка кампании.
- `description_input` (QtWidgets.QLineEdit): Поле ввода для описания кампании.
- `promotion_name_input` (QtWidgets.QLineEdit): Поле ввода для названия продвижения кампании.

**Методы**:

- `__init__(self, parent=None, main_app=None)`: Инициализирует виджет `CampaignEditor`.
- `setup_ui(self)`: Настраивает пользовательский интерфейс.
- `setup_connections(self)`: Устанавливает соединения между сигналами и слотами.
- `open_file(self)`: Открывает диалоговое окно для выбора и загрузки JSON-файла.
- `load_file(self, campaign_file)`: Загружает JSON-файл.
- `create_widgets(self, data)`: Создает виджеты на основе данных из JSON-файла.
- `prepare_campaign(self)`: Асинхронно подготавливает кампанию.

### `__init__(self, parent=None, main_app=None)`

```python
def __init__(self, parent=None, main_app=None):
    """ Initialize the CampaignEditor widget """
    super().__init__(parent)
    self.main_app = main_app  # Save the MainApp instance

    self.setup_ui()
    self.setup_connections()
```

**Назначение**: Инициализирует виджет `CampaignEditor`, сохраняет экземпляр главного приложения, настраивает пользовательский интерфейс и устанавливает соединения.

**Параметры**:

- `parent` (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
- `main_app` (MainApp, optional): Экземпляр главного приложения. По умолчанию `None`.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `QtWidgets.QWidget`.
2.  Сохраняет переданный экземпляр главного приложения в атрибуте `self.main_app`.
3.  Вызывает метод `self.setup_ui()` для настройки пользовательского интерфейса.
4.  Вызывает метод `self.setup_connections()` для установки соединений между сигналами и слотами.

**Примеры**:

```python
# Пример создания экземпляра CampaignEditor
campaign_editor = CampaignEditor(main_app=main_app_instance)
```

### `setup_ui(self)`

```python
def setup_ui(self):
    """ Setup the user interface """
    self.setWindowTitle("Campaign Editor")
    self.resize(1800, 800)

    # Create a QScrollArea
    self.scroll_area = QtWidgets.QScrollArea()
    self.scroll_area.setWidgetResizable(True)

    # Create a QWidget for the content of the scroll area
    self.scroll_content_widget = QtWidgets.QWidget()
    self.scroll_area.setWidget(self.scroll_content_widget)

    # Create the layout for the scroll content widget
    self.layout = QtWidgets.QGridLayout(self.scroll_content_widget)
    self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    # Define UI components
    self.open_button = QtWidgets.QPushButton("Open JSON File")
    self.open_button.clicked.connect(self.open_file)
    set_fixed_size(self.open_button, width=250, height=25)

    self.file_name_label = QtWidgets.QLabel("No file selected")
    set_fixed_size(self.file_name_label, width=500, height=25)

    self.prepare_button = QtWidgets.QPushButton("Prepare Campaign")
    self.prepare_button.clicked.connect(self.prepare_campaign)
    set_fixed_size(self.prepare_button, width=250, height=25)

    # Add components to layout
    self.layout.addWidget(self.open_button, 0, 0)
    self.layout.addWidget(self.file_name_label, 0, 1)
    self.layout.addWidget(self.prepare_button, 1, 0, 1, 2)  # Span across two columns

    # Add the scroll area to the main layout of the widget
    main_layout = QtWidgets.QVBoxLayout(self)
    main_layout.addWidget(self.scroll_area)
    self.setLayout(main_layout)
```

**Назначение**: Настраивает пользовательский интерфейс виджета `CampaignEditor`, включая создание области прокрутки, добавление кнопок и меток, а также установку размеров компонентов.

**Как работает функция**:

1.  Устанавливает заголовок окна виджета как "Campaign Editor".
2.  Устанавливает размер окна виджета как 1800x800 пикселей.
3.  Создает область прокрутки (`QScrollArea`) и устанавливает свойство `widgetResizable` в `True`, чтобы виджет внутри области прокрутки мог изменять свой размер.
4.  Создает виджет (`QWidget`) для содержимого области прокрутки и устанавливает его в качестве виджета для `QScrollArea`.
5.  Создает сетку (`QGridLayout`) для размещения виджетов внутри виджета содержимого области прокрутки и устанавливает выравнивание по верхнему краю.
6.  Определяет UI компоненты:
    *   Кнопку "Open JSON File" (`QPushButton`) и связывает её с методом `self.open_file` при нажатии.
    *   Метку (`QLabel`) для отображения имени выбранного файла с текстом "No file selected".
    *   Кнопку "Prepare Campaign" (`QPushButton`) и связывает её с методом `self.prepare_campaign` при нажатии.
7.  Добавляет компоненты в сетку:
    *   Кнопку открытия файла в позицию (0, 0).
    *   Метку имени файла в позицию (0, 1).
    *   Кнопку подготовки кампании в позицию (1, 0), занимающую две колонки.
8.  Создает основной вертикальный макет (`QVBoxLayout`) для виджета и добавляет в него область прокрутки.
9.  Устанавливает основной макет для виджета.

```
UI Setup Flowchart:

Настройка_UI
│
├───Создание_QScrollArea
│   │
│   └───Создание_QWidget_для_содержимого
│
├───Создание_QGridLayout
│   │
│   └───Определение_UI_компонентов
│       │
│       ├───Создание_Open_Button
│       │   └───Подключение_open_file
│       │
│       ├───Создание_File_Name_Label
│       │
│       └───Создание_Prepare_Button
│           └───Подключение_prepare_campaign
│
└───Добавление_компонентов_в_макет
    │
    └───Создание_основного_QVBoxLayout
        │
        └───Установка_макета_для_виджета
```

**Примеры**:

```python
# Пример вызова метода setup_ui
self.setup_ui()
```

### `setup_connections(self)`

```python
def setup_connections(self):
    """ Setup signal-slot connections """
    pass
```

**Назначение**: Устанавливает соединения между сигналами и слотами. В текущей реализации не выполняет никаких действий.

**Как работает функция**:
Функция пока пуста и не выполняет никаких действий. Она предназначена для установки связей между сигналами и слотами, но в текущей версии программы эти связи не определены.

**Примеры**:

```python
# Пример вызова метода setup_connections
self.setup_connections()
```

### `open_file(self)`

```python
def open_file(self):
    """ Open a file dialog to select and load a JSON file """
    campaign_file, _ = QtWidgets.QFileDialog.getOpenFileName(
        self,
        "Open JSON File",
        "c:/user/documents/repos/hypotez/data/aliexpress/campaigns",
        "JSON files (*.json)"
    )
    if not campaign_file:
        return

    self.load_file(campaign_file)
```

**Назначение**: Открывает диалоговое окно для выбора JSON-файла и загружает выбранный файл.

**Как работает функция**:

1.  Открывает диалоговое окно выбора файла с помощью `QtWidgets.QFileDialog.getOpenFileName`.
    *   Параметры:
        *   `self`: Родительский виджет.
        *   `"Open JSON File"`: Заголовок диалогового окна.
        *   `"c:/user/documents/repos/hypotez/data/aliexpress/campaigns"`: Путь к папке, которая открывается по умолчанию.
        *   `"JSON files (*.json)"`: Фильтр файлов, отображаемых в диалоговом окне.
2.  Проверяет, был ли выбран файл. Если файл не выбран (`campaign_file` пуст), функция завершается.
3.  Если файл выбран, вызывает метод `self.load_file` для загрузки содержимого файла.

```
Open File Flowchart:

Open_File
│
├───Открытие_диалога_выбора_файла
│   │
│   └───Проверка_выбран_ли_файл
│       │
│       ├───Нет: Выход
│       │
│       └───Да: Загрузка_файла
│           │
│           └───Вызов_load_file
│
└───Конец
```

**Примеры**:

```python
# Пример вызова метода open_file
self.open_file()
```

### `load_file(self, campaign_file)`

```python
def load_file(self, campaign_file):
    """ Load a JSON file """
    try:
        self.data = j_loads_ns(campaign_file)
        self.current_campaign_file = campaign_file
        self.file_name_label.setText(f"File: {self.current_campaign_file}")
        self.create_widgets(self.data)
        self.editor = AliCampaignEditor(campaign_file=campaign_file)
    except Exception as ex:
        QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")
```

**Назначение**: Загружает JSON-файл и отображает его содержимое в интерфейсе.

**Параметры**:

- `campaign_file` (str): Путь к JSON-файлу.

**Как работает функция**:

1.  Пытается выполнить следующие действия:
    *   Загружает JSON-файл, используя функцию `j_loads_ns` и сохраняет данные в атрибуте `self.data`.
    *   Сохраняет путь к файлу в атрибуте `self.current_campaign_file`.
    *   Обновляет текст метки `self.file_name_label`, чтобы отобразить имя загруженного файла.
    *   Вызывает метод `self.create_widgets` для создания виджетов на основе загруженных данных.
    *   Создает экземпляр класса `AliCampaignEditor`, передавая путь к файлу кампании.
2.  Если происходит исключение, отображает сообщение об ошибке с помощью `QtWidgets.QMessageBox.critical`.

```
Load File Flowchart:

Load_File
│
├───Попытка
│   │
│   ├───Загрузка_JSON_файла
│   │   └───j_loads_ns
│   │
│   ├───Сохранение_пути_к_файлу
│   │
│   ├───Обновление_метки_имени_файла
│   │
│   ├───Создание_виджетов
│   │   └───create_widgets
│   │
│   └───Создание_AliCampaignEditor
│
└───Перехват_исключения
    │
    └───Вывод_сообщения_об_ошибке
```

**Примеры**:

```python
# Пример вызова метода load_file
self.load_file("path/to/campaign.json")
```

### `create_widgets(self, data)`

```python
def create_widgets(self, data):
    """ Create widgets based on the data loaded from the JSON file """
    layout = self.layout

    # Remove previous widgets except open button and file label
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget not in [self.open_button, self.file_name_label, self.prepare_button]:
            widget.deleteLater()

    self.title_input = QtWidgets.QLineEdit(data.title)
    layout.addWidget(QtWidgets.QLabel("Title:"), 2, 0)
    layout.addWidget(self.title_input, 2, 1)
    set_fixed_size(self.title_input, width=500, height=25)

    self.description_input = QtWidgets.QLineEdit(data.description)
    layout.addWidget(QtWidgets.QLabel("Description:"), 3, 0)
    layout.addWidget(self.description_input, 3, 1)
    set_fixed_size(self.description_input, width=500, height=25)

    self.promotion_name_input = QtWidgets.QLineEdit(data.promotion_name)
    layout.addWidget(QtWidgets.QLabel("Promotion Name:"), 4, 0)
    layout.addWidget(self.promotion_name_input, 4, 1)
    set_fixed_size(self.promotion_name_input, width=500, height=25)
```

**Назначение**: Создает виджеты на основе данных, загруженных из JSON-файла.

**Параметры**:

- `data` (SimpleNamespace): Данные, загруженные из JSON-файла.

**Как работает функция**:

1.  Получает ссылку на макет (`self.layout`).
2.  Удаляет все предыдущие виджеты из макета, кроме кнопок "Open JSON File" (`self.open_button`), "Prepare Campaign" (`self.prepare_button`) и метки имени файла (`self.file_name_label`).
3.  Создает поле ввода (`QLineEdit`) для заголовка кампании (`data.title`) и добавляет его в макет вместе с меткой "Title:".
4.  Создает поле ввода (`QLineEdit`) для описания кампании (`data.description`) и добавляет его в макет вместе с меткой "Description:".
5.  Создает поле ввода (`QLineEdit`) для названия продвижения кампании (`data.promotion_name`) и добавляет его в макет вместе с меткой "Promotion Name:".
    *   Для каждого поля ввода устанавливается фиксированный размер 500x25 пикселей.

```
Create Widgets Flowchart:

Create_Widgets
│
├───Удаление_предыдущих_виджетов
│   │
│   └───Для_каждого_виджета_в_макете
│       │
│       └───Если_виджет_не_open_button_или_file_name_label_или_prepare_button
│           │
│           └───Удаление_виджета
│
├───Создание_поля_ввода_для_заголовка
│   │
│   └───Добавление_поля_ввода_и_метки_в_макет
│
├───Создание_поля_ввода_для_описания
│   │
│   └───Добавление_поля_ввода_и_метки_в_макет
│
├───Создание_поля_ввода_для_названия_продвижения
│   │
│   └───Добавление_поля_ввода_и_метки_в_макет
```

**Примеры**:

```python
# Пример вызова метода create_widgets
self.create_widgets(data)
```

### `prepare_campaign(self)`

```python
@asyncSlot()
async def prepare_campaign(self):
    """ Asynchronously prepare the campaign """
    if self.editor:
        try:
            await self.editor.prepare()
            QtWidgets.QMessageBox.information(self, "Success", "Campaign prepared successfully.")
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to prepare campaign: {ex}")
```

**Назначение**: Асинхронно подготавливает кампанию с использованием `AliCampaignEditor`.

**Как работает функция**:

1.  Проверяет, существует ли экземпляр `self.editor` (то есть был ли загружен файл кампании).
2.  Если `self.editor` существует, пытается выполнить следующие действия:
    *   Вызывает асинхронный метод `self.editor.prepare()` для подготовки кампании.
    *   В случае успеха отображает информационное сообщение с помощью `QtWidgets.QMessageBox.information`.
3.  Если происходит исключение, отображает сообщение об ошибке с помощью `QtWidgets.QMessageBox.critical`.

```
Prepare Campaign Flowchart:

Prepare_Campaign
│
├───Проверка_существования_self.editor
│   │
│   └───Если_self.editor_существует
│       │
│       ├───Попытка
│       │   │
│       │   ├───Асинхронная_подготовка_кампании
│       │   │   └───await self.editor.prepare()
│       │   │
│       │   └───Вывод_информационного_сообщения
│       │
│       └───Перехват_исключения
│           │
│           └───Вывод_сообщения_об_ошибке
```

**Примеры**:

```python
# Пример вызова метода prepare_campaign
await self.prepare_campaign()