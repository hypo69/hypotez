# src.suppliers.suppliers_list.aliexpress.gui.main

## Обзор

Модуль предоставляет основной интерфейс для управления рекламными кампаниями. Он содержит главное окно приложения с вкладками для редактирования JSON, управления кампаниями и редактирования товаров.

## Подробней

Модуль `main.py` является точкой входа в графическое приложение, предназначенное для управления рекламными кампаниями AliExpress. Он использует библиотеку PyQt6 для создания графического интерфейса и включает в себя несколько вкладок для работы с различными аспектами управления кампаниями, такими как редактирование JSON-файлов, управление категориями и редактирование информации о товарах.

## Классы

### `MainApp`

**Описание**: Главное окно приложения, которое содержит вкладки для редактирования JSON, управления кампаниями и редактирования товаров.

**Наследует**: `QtWidgets.QMainWindow`

**Атрибуты**:
- `tab_widget` (QtWidgets.QTabWidget): Виджет для управления вкладками.
- `tab1` (QtWidgets.QWidget): Вкладка для редактирования JSON.
- `promotion_app` (CampaignEditor): Экземпляр класса `CampaignEditor` для управления кампаниями.
- `tab2` (QtWidgets.QWidget): Вкладка для управления кампаниями.
- `campaign_editor_app` (CategoryEditor): Экземпляр класса `CategoryEditor` для управления категориями.
- `tab3` (QtWidgets.QWidget): Вкладка для редактирования товаров.
- `product_editor_app` (ProductEditor): Экземпляр класса `ProductEditor` для редактирования товаров.

**Методы**:
- `__init__()`: Инициализирует главное окно приложения, создает вкладки и добавляет их в виджет вкладок.
- `create_menubar()`: Создает меню с опциями для операций с файлами и командами редактирования.
- `open_file()`: Открывает диалоговое окно для выбора и загрузки JSON-файла.
- `save_file()`: Сохраняет текущий файл.
- `exit_application()`: Закрывает приложение.
- `copy()`: Копирует выделенный текст в буфер обмена.
- `paste()`: Вставляет текст из буфера обмена.
- `load_file()`: Загружает JSON-файл.

### `__init__`

```python
def __init__(self):
    """ Initialize the main application with tabs """
    super().__init__()
    self.setWindowTitle("Main Application with Tabs")
    self.setGeometry(100, 100, 1800, 800)

    self.tab_widget = QtWidgets.QTabWidget()
    self.setCentralWidget(self.tab_widget)

    # Create the JSON Editor tab and add it to the tab widget
    self.tab1 = QtWidgets.QWidget()
    self.tab_widget.addTab(self.tab1, "JSON Editor")
    self.promotion_app = CampaignEditor(self.tab1, self)

    # Create the Campaign Editor tab and add it to the tab widget
    self.tab2 = QtWidgets.QWidget()
    self.tab_widget.addTab(self.tab2, "Campaign Editor")
    self.campaign_editor_app = CategoryEditor(self.tab2, self)

    # Create the Product Editor tab and add it to the tab widget
    self.tab3 = QtWidgets.QWidget()
    self.tab_widget.addTab(self.tab3, "Product Editor")
    self.product_editor_app = ProductEditor(self.tab3, self)

    self.create_menubar()
```

**Назначение**: Инициализирует главное окно приложения с вкладками.

**Как работает функция**:
- Вызывает конструктор родительского класса `QtWidgets.QMainWindow`.
- Устанавливает заголовок окна.
- Устанавливает геометрию окна (размер и положение).
- Создает виджет вкладок `QTabWidget`.
- Устанавливает виджет вкладок в качестве центрального виджета окна.
- Создает три вкладки: "JSON Editor", "Campaign Editor" и "Product Editor".
- Для каждой вкладки создает соответствующие редакторы (`CampaignEditor`, `CategoryEditor`, `ProductEditor`) и добавляет их на вкладки.
- Вызывает метод `create_menubar()` для создания меню.

**Примеры**:
```python
main_app = MainApp()
main_app.show()
```

### `create_menubar`

```python
def create_menubar(self):
    """ Create a menu bar with options for file operations and edit commands """
    menubar = self.menuBar()

    file_menu = menubar.addMenu("File")
    open_action = QtGui.QAction("Open", self)
    open_action.triggered.connect(self.open_file)
    file_menu.addAction(open_action)
    save_action = QtGui.QAction("Save", self)
    save_action.triggered.connect(self.save_file)
    file_menu.addAction(save_action)
    exit_action = QtGui.QAction("Exit", self)
    exit_action.triggered.connect(self.exit_application)
    file_menu.addAction(exit_action)

    edit_menu = menubar.addMenu("Edit")
    copy_action = QtGui.QAction("Copy", self)
    copy_action.triggered.connect(self.copy)
    edit_menu.addAction(copy_action)
    paste_action = QtGui.QAction("Paste", self)
    paste_action.triggered.connect(self.paste)
    edit_menu.addAction(paste_action)

    open_product_action = QtGui.QAction("Open Product File", self)
    open_product_action.triggered.connect(self.product_editor_app.open_file)
    file_menu.addAction(open_product_action)
```

**Назначение**: Создает строку меню с опциями для операций с файлами и командами редактирования.

**Как работает функция**:
- Создает строку меню.
- Создает меню "File" с опциями "Open", "Save" и "Exit".
- Для каждой опции создает действие (`QAction`) и связывает его с соответствующим методом (`open_file`, `save_file`, `exit_application`).
- Добавляет действия в меню "File".
- Создает меню "Edit" с опциями "Copy" и "Paste".
- Для каждой опции создает действие (`QAction`) и связывает его с соответствующим методом (`copy`, `paste`).
- Добавляет действия в меню "Edit".

**Примеры**:
```python
self.create_menubar()
```

### `open_file`

```python
def open_file(self):
    """ Open a file dialog to select and load a JSON file """
    file_dialog = QtWidgets.QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "JSON files (*.json)")
    if not file_path:
        return

    if self.tab_widget.currentIndex() == 0:
        self.load_file(file_path)
```

**Назначение**: Открывает диалоговое окно для выбора и загрузки JSON-файла.

**Как работает функция**:
- Создает диалоговое окно для выбора файла (`QFileDialog`).
- Открывает диалоговое окно и получает путь к выбранному файлу.
- Если путь к файлу не выбран, функция завершается.
- Проверяет, какая вкладка активна. Если активна первая вкладка (JSON Editor), вызывает метод `load_file` для загрузки файла.

**Примеры**:
```python
open_action = QtGui.QAction("Open", self)
open_action.triggered.connect(self.open_file)
```

### `save_file`

```python
def save_file(self):
    """ Save the current file """
    current_index = self.tab_widget.currentIndex()
    if current_index == 0:
        self.promotion_app.save_changes()
    elif current_index == 2:
        self.product_editor_app.save_product()
```

**Назначение**: Сохраняет текущий файл в зависимости от активной вкладки.

**Как работает функция**:
- Получает индекс активной вкладки.
- Если активна первая вкладка (JSON Editor), вызывает метод `save_changes` объекта `promotion_app`.
- Если активна третья вкладка (Product Editor), вызывает метод `save_product` объекта `product_editor_app`.

**Примеры**:
```python
save_action = QtGui.QAction("Save", self)
save_action.triggered.connect(self.save_file)
```

### `exit_application`

```python
def exit_application(self):
    """ Exit the application """
    self.close()
```

**Назначение**: Закрывает приложение.

**Как работает функция**:
- Вызывает метод `close()` для закрытия главного окна приложения.

**Примеры**:
```python
exit_action = QtGui.QAction("Exit", self)
exit_action.triggered.connect(self.exit_application)
```

### `copy`

```python
def copy(self):
    """ Copy selected text to the clipboard """
    widget = self.focusWidget()
    if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
        widget.copy()
    else:
        QtWidgets.QMessageBox.warning(self, "Warning", "No text widget in focus to copy.")
```

**Назначение**: Копирует выделенный текст в буфер обмена.

**Как работает функция**:
- Получает виджет, находящийся в фокусе.
- Проверяет, является ли виджет текстовым редактором (`QLineEdit`, `QTextEdit`, `QPlainTextEdit`).
- Если виджет является текстовым редактором, вызывает метод `copy()` для копирования выделенного текста в буфер обмена.
- Если виджет не является текстовым редактором, выводит предупреждающее сообщение.

**Примеры**:
```python
copy_action = QtGui.QAction("Copy", self)
copy_action.triggered.connect(self.copy)
```

### `paste`

```python
def paste(self):
    """ Paste text from the clipboard """
    widget = self.focusWidget()
    if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
        widget.paste()
    else:
        QtWidgets.QMessageBox.warning(self, "Warning", "No text widget in focus to paste.")
```

**Назначение**: Вставляет текст из буфера обмена.

**Как работает функция**:
- Получает виджет, находящийся в фокусе.
- Проверяет, является ли виджет текстовым редактором (`QLineEdit`, `QTextEdit`, `QPlainTextEdit`).
- Если виджет является текстовым редактором, вызывает метод `paste()` для вставки текста из буфера обмена.
- Если виджет не является текстовым редактором, выводит предупреждающее сообщение.

**Примеры**:
```python
paste_action = QtGui.QAction("Paste", self)
paste_action.triggered.connect(self.paste)
```

### `load_file`

```python
def load_file(self, campaign_file):
    """ Load the JSON file """
    try:
        self.promotion_app.load_file(campaign_file)
    except Exception as ex:
        QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")
```

**Назначение**: Загружает JSON-файл с использованием `promotion_app`.

**Параметры**:
- `campaign_file` (str): Путь к JSON-файлу.

**Как работает функция**:
- Пытается загрузить JSON-файл, вызывая метод `load_file` объекта `promotion_app`.
- Если во время загрузки файла возникает исключение, выводит сообщение об ошибке.

**Примеры**:
```python
self.load_file(file_path)
```

## Функции

### `main`

```python
def main():
    """ Initialize and run the application """
    app = QtWidgets.QApplication(sys.argv)

    # Create an event loop for asynchronous operations
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_app = MainApp()
    main_app.show()

    # Run the event loop
    with loop:
        loop.run_forever()
```

**Назначение**: Инициализирует и запускает приложение.

**Как работает функция**:
- Создает экземпляр приложения `QApplication`.
- Создает цикл событий для асинхронных операций (`QEventLoop`).
- Устанавливает цикл событий (`asyncio.set_event_loop`).
- Создает экземпляр главного окна приложения (`MainApp`).
- Отображает главное окно приложения (`main_app.show()`).
- Запускает цикл событий (`loop.run_forever()`).

**Примеры**:
```python
if __name__ == "__main__":
    main()