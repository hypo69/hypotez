# Модуль: src.suppliers.suppliers_list.aliexpress.gui.campaign

## Обзор

Модуль `campaign.py` предоставляет графический интерфейс для редактирования кампаний AliExpress. Он включает в себя функции для загрузки, отображения и подготовки данных кампаний, хранящихся в JSON-файлах. Модуль использует библиотеку PyQt6 для создания интерфейса и `asyncio` для асинхронного выполнения задач.

## Подробнее

Этот модуль предназначен для создания и редактирования рекламных кампаний AliExpress через графический интерфейс. Он позволяет пользователям открывать JSON-файлы, содержащие данные кампаний, редактировать их и подготавливать к использованию.
В данном модуле реализован класс `CampaignEditor`, который расширяет функциональность `QtWidgets.QWidget` и предоставляет инструменты для работы с интерфейсом редактора кампаний. Класс включает методы для настройки пользовательского интерфейса, обработки событий (например, нажатия кнопок) и асинхронной подготовки кампаний.

## Классы

### `CampaignEditor`

**Описание**: Класс `CampaignEditor` представляет собой виджет для редактирования кампаний, который позволяет загружать, отображать и изменять данные кампаний AliExpress.

**Наследует**:
- `QtWidgets.QWidget`

**Атрибуты**:
- `data` (SimpleNamespace): Пространство имен для хранения данных кампании.
- `current_campaign_file` (str): Путь к текущему открытому файлу кампании.
- `editor` (AliCampaignEditor): Экземпляр редактора кампаний AliExpress.
- `main_app` : экземпляр главного приложения.
- `scroll_area`: область с возможностью прокрутки контента
- `scroll_content_widget`:  Виджет для контента внутри области прокрутки
- `layout`: Макет для размещения виджетов
- `open_button`: кнопка для открытия JSON файлов
- `file_name_label`: Отображает имя выбранного файла
- `prepare_button`: Кнопка для подготовки кампании
- `title_input` (QtWidgets.QLineEdit): Текстовое поле для ввода заголовка кампании.
- `description_input` (QtWidgets.QLineEdit): Текстовое поле для ввода описания кампании.
- `promotion_name_input` (QtWidgets.QLineEdit): Текстовое поле для ввода названия акции кампании.

**Методы**:
- `__init__`: Инициализирует виджет CampaignEditor.
- `setup_ui`: Настраивает пользовательский интерфейс.
- `setup_connections`: Устанавливает соединения между сигналами и слотами.
- `open_file`: Открывает диалоговое окно выбора файла для загрузки JSON-файла.
- `load_file`: Загружает JSON-файл и создает виджеты на основе данных.
- `create_widgets`: Создает виджеты для отображения и редактирования данных кампании.
- `prepare_campaign`: Асинхронно подготавливает кампанию.

**Принцип работы**:

Класс `CampaignEditor` создает графический интерфейс для редактирования данных кампаний AliExpress. При инициализации класса настраивается пользовательский интерфейс, включающий кнопки для открытия файлов и подготовки кампаний, а также текстовые поля для отображения и редактирования данных кампании.

Пользователь может открыть JSON-файл с данными кампании, после чего интерфейс отображает заголовок, описание и название акции кампании в соответствующих текстовых полях. После редактирования данных пользователь может подготовить кампанию, вызвав метод `prepare_campaign`, который асинхронно выполняет подготовку кампании с использованием класса `AliCampaignEditor`.

## Методы класса

### `__init__(self, parent=None, main_app=None)`

```python
def __init__(self, parent=None, main_app=None):
    """ Initialize the CampaignEditor widget """
    super().__init__(parent)
    self.main_app = main_app  # Save the MainApp instance

    self.setup_ui()
    self.setup_connections()
```

**Назначение**: Инициализирует виджет `CampaignEditor`.

**Параметры**:
- `parent` (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
- `main_app` (MainApp, optional): экземпляр главного приложения. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:

1. Вызывает конструктор родительского класса `QtWidgets.QWidget`.
2. Сохраняет ссылку на экземпляр главного приложения в атрибуте `main_app`.
3. Вызывает метод `setup_ui` для настройки пользовательского интерфейса.
4. Вызывает метод `setup_connections` для установки связей между сигналами и слотами.

**Примеры**:

```python
editor = CampaignEditor(main_app=main_app_instance)
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

**Назначение**: Настраивает пользовательский интерфейс виджета.

**Параметры**:
- `self` (CampaignEditor): Экземпляр класса `CampaignEditor`.

**Возвращает**:
- `None`

**Как работает функция**:

1. Устанавливает заголовок окна виджета.
2. Устанавливает размеры окна виджета.
3. Создает область прокрутки (`QScrollArea`) и устанавливает ее как изменяемую по размеру.
4. Создает виджет для контента области прокрутки (`QWidget`) и устанавливает его в область прокрутки.
5. Создает макет (`QGridLayout`) для виджета контента области прокрутки и выравнивает его по верхнему краю.
6. Определяет компоненты пользовательского интерфейса, такие как кнопки (`QPushButton`) и метки (`QLabel`).
7. Устанавливает соединения между сигналами и слотами для кнопок.
8. Добавляет компоненты в макет.
9. Добавляет область прокрутки в основной макет виджета.

**Примеры**:

```python
editor = CampaignEditor()
editor.setup_ui()
```

### `setup_connections(self)`

```python
def setup_connections(self):
    """ Setup signal-slot connections """
    pass
```

**Назначение**: Устанавливает соединения между сигналами и слотами. В текущей реализации функция пуста.

**Параметры**:
- `self` (CampaignEditor): Экземпляр класса `CampaignEditor`.

**Возвращает**:
- `None`

**Как работает функция**:

В текущей версии функция не выполняет никаких действий. Предполагается, что в будущем здесь будет добавлен код для установки связей между сигналами и слотами для обработки событий пользовательского интерфейса.

**Примеры**:

```python
editor = CampaignEditor()
editor.setup_connections()
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

**Назначение**: Открывает диалоговое окно для выбора и загрузки JSON-файла.

**Параметры**:
- `self` (CampaignEditor): Экземпляр класса `CampaignEditor`.

**Возвращает**:
- `None`

**Как работает функция**:

1. Открывает диалоговое окно выбора файла с использованием `QtWidgets.QFileDialog.getOpenFileName`.
2. Устанавливает фильтр для отображения только JSON-файлов.
3. Если файл выбран, вызывает метод `self.load_file` для загрузки файла.
4. Если файл не выбран, функция завершает свою работу.

**Примеры**:

```python
editor = CampaignEditor()
editor.open_file()
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

**Назначение**: Загружает JSON-файл.

**Параметры**:
- `self` (CampaignEditor): Экземпляр класса `CampaignEditor`.
- `campaign_file` (str): Путь к JSON-файлу.

**Возвращает**:
- `None`

**Как работает функция**:

1. Пытается загрузить JSON-файл, используя функцию `j_loads_ns`.
2. Сохраняет путь к файлу в атрибуте `self.current_campaign_file`.
3. Обновляет текст метки `self.file_name_label` с именем файла.
4. Вызывает метод `self.create_widgets` для создания виджетов на основе данных из файла.
5. Создает экземпляр класса `AliCampaignEditor`, передавая путь к файлу кампании.
6. В случае ошибки отображает критическое сообщение об ошибке.

**Примеры**:

```python
editor = CampaignEditor()
editor.load_file("path/to/campaign.json")
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
- `self` (CampaignEditor): Экземпляр класса `CampaignEditor`.
- `data` (SimpleNamespace): Данные, загруженные из JSON-файла.

**Возвращает**:
- `None`

**Как работает функция**:

1. Получает макет (`self.layout`) виджета.
2. Удаляет предыдущие виджеты из макета, за исключением кнопок `open_button` и `prepare_button` и метки `file_name_label`.
3. Создает текстовые поля (`QLineEdit`) для заголовка, описания и названия акции кампании.
4. Добавляет метки (`QLabel`) и текстовые поля в макет.

**Примеры**:

```python
editor = CampaignEditor()
data = SimpleNamespace(title="Example Title", description="Example Description", promotion_name="Example Promotion")
editor.create_widgets(data)
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

**Назначение**: Асинхронно подготавливает кампанию.

**Параметры**:
- `self` (CampaignEditor): Экземпляр класса `CampaignEditor`.

**Возвращает**:
- `None`

**Как работает функция**:

1. Проверяет, существует ли экземпляр `self.editor`.
2. Вызывает асинхронный метод `self.editor.prepare()` для подготовки кампании.
3. В случае успешной подготовки отображает информационное сообщение.
4. В случае ошибки отображает критическое сообщение об ошибке.

**Примеры**:

```python
editor = CampaignEditor()
asyncio.run(editor.prepare_campaign())