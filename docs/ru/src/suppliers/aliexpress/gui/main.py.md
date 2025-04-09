# Модуль `main.py`

## Обзор

Модуль `main.py` представляет собой основной интерфейс для управления рекламными кампаниями, категориями и продуктами AliExpress. Он предоставляет графический интерфейс пользователя (GUI) на основе библиотеки PyQt6, разделенный на несколько вкладок для удобства работы с различными аспектами управления.

## Подробней

Данный модуль является точкой входа в GUI приложение, предназначенное для управления рекламными кампаниями, категориями и продуктами AliExpress. Он использует библиотеку PyQt6 для создания пользовательского интерфейса и предоставляет следующие возможности:

- Редактирование JSON файлов конфигурации кампаний.
- Управление категориями товаров.
- Редактирование информации о продуктах.
- Открытие и сохранение файлов конфигурации.
- Копирование и вставка текста в текстовых полях.

## Классы

### `MainApp`

**Описание**: Основной класс приложения, представляющий главное окно с вкладками для управления кампаниями, категориями и продуктами.

**Наследует**: `QtWidgets.QMainWindow`

**Атрибуты**:
- `tab_widget` (QtWidgets.QTabWidget): Виджет для отображения вкладок.
- `tab1` (QtWidgets.QWidget): Виджет для вкладки "JSON Editor".
- `promotion_app` (CampaignEditor): Экземпляр класса `CampaignEditor` для управления кампаниями.
- `tab2` (QtWidgets.QWidget): Виджет для вкладки "Campaign Editor".
- `campaign_editor_app` (CategoryEditor): Экземпляр класса `CategoryEditor` для управления категориями.
- `tab3` (QtWidgets.QWidget): Виджет для вкладки "Product Editor".
- `product_editor_app` (ProductEditor): Экземпляр класса `ProductEditor` для управления продуктами.

**Методы**:
- `__init__`: Инициализирует главное окно приложения, создает вкладки и добавляет их в виджет вкладок.
- `create_menubar`: Создает менюбар с опциями для работы с файлами и редактирования.
- `open_file`: Открывает диалоговое окно выбора файла для загрузки JSON файла.
- `save_file`: Сохраняет текущий файл в зависимости от активной вкладки.
- `exit_application`: Закрывает приложение.
- `copy`: Копирует выбранный текст в буфер обмена.
- `paste`: Вставляет текст из буфера обмена.
- `load_file`: Загружает JSON файл.

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
**Как работает функция**:

1. **Инициализация главного окна**:
   - Вызывается конструктор родительского класса `QtWidgets.QMainWindow` для инициализации главного окна приложения.
   - Устанавливается заголовок окна (`setWindowTitle`).
   - Устанавливаются размеры и положение окна (`setGeometry`).
2. **Создание виджета вкладок**:
   - Создается виджет `QTabWidget`, который будет содержать вкладки приложения.
   - `tab_widget` устанавливается как центральный виджет главного окна.
3. **Создание и добавление вкладок**:
   - Создается вкладка "JSON Editor" (`tab1`) и добавляется в `tab_widget`.
   - Создается экземпляр `CampaignEditor`, который отвечает за редактирование JSON файлов конфигурации кампаний, и связывается с вкладкой `tab1`.
   - Аналогично создаются вкладки "Campaign Editor" (`tab2`) и "Product Editor" (`tab3`), а также экземпляры `CategoryEditor` и `ProductEditor` для управления категориями и продуктами соответственно.
4. **Создание менюбара**:
   - Вызывается метод `create_menubar` для создания менюбара приложения.

ASCII схема работы функции:

```
Инициализация QMainWindow
│
├───> Установка заголовка окна
│
├───> Установка геометрии окна
│
├───> Создание QTabWidget
│
├───> Создание вкладок (JSON Editor, Campaign Editor, Product Editor)
│    │
│    ├───> Создание CampaignEditor и связывание с вкладкой JSON Editor
│    │
│    ├───> Создание CategoryEditor и связывание с вкладкой Campaign Editor
│    │
│    └───> Создание ProductEditor и связывание с вкладкой Product Editor
│
└───> Создание менюбара
```

Пример:

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

**Назначение**: Создает менюбар с опциями для работы с файлами и редактирования.

**Как работает функция**:

1. **Создание менюбара**:
   - Получает менюбар главного окна (`self.menuBar()`).
2. **Создание меню "File"**:
   - Создает меню "File" и добавляет в менюбар.
   - Создает действия "Open", "Save", "Exit" и связывает их с соответствующими функциями (`open_file`, `save_file`, `exit_application`).
   - Добавляет действия в меню "File".
3. **Создание меню "Edit"**:
   - Создает меню "Edit" и добавляет в менюбар.
   - Создает действия "Copy", "Paste" и связывает их с соответствующими функциями (`copy`, `paste`).
   - Добавляет действия в меню "Edit".
4. **Добавление действия "Open Product File" в меню "File"**:
   - Создает действие "Open Product File" и связывает его с функцией `open_file` экземпляра `product_editor_app`.
   - Добавляет действие в меню "File".

ASCII схема работы функции:

```
Получение менюбара
│
├───> Создание меню "File"
│    │
│    ├───> Создание действия "Open" и связывание с open_file
│    │
│    ├───> Создание действия "Save" и связывание с save_file
│    │
│    ├───> Создание действия "Exit" и связывание с exit_application
│    │
│    └───> Добавление действий в меню "File"
│
├───> Создание меню "Edit"
│    │
│    ├───> Создание действия "Copy" и связывание с copy
│    │
│    ├───> Создание действия "Paste" и связывание с paste
│    │
│    └───> Добавление действий в меню "Edit"
│
└───> Создание действия "Open Product File" и связывание с product_editor_app.open_file
     │
     └───> Добавление действия в меню "File"
```

Пример:

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

**Назначение**: Открывает диалоговое окно выбора файла для загрузки JSON файла.

**Как работает функция**:

1. **Создание диалогового окна**:
   - Создает экземпляр класса `QFileDialog` для открытия диалогового окна выбора файла.
2. **Открытие диалогового окна и получение пути к файлу**:
   - Открывает диалоговое окно с заголовком "Open File" и фильтром для JSON файлов.
   - Получает путь к выбранному файлу и сохраняет его в переменной `file_path`.
3. **Проверка наличия выбранного файла**:
   - Проверяет, был ли выбран файл. Если файл не выбран, функция завершается.
4. **Загрузка файла**:
   - Проверяет, активна ли вкладка "JSON Editor" (индекс 0).
   - Если вкладка активна, вызывает метод `load_file` для загрузки выбранного файла.

ASCII схема работы функции:

```
Создание QFileDialog
│
├───> Открытие диалогового окна выбора файла
│
├───> Проверка наличия выбранного файла
│    │
│    └───> Если файл не выбран, завершение функции
│
└───> Проверка активной вкладки
     │
     └───> Если активна вкладка "JSON Editor", вызов load_file
```

Пример:

```python
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

1. **Получение индекса активной вкладки**:
   - Получает индекс активной вкладки из виджета `tab_widget`.
2. **Проверка активной вкладки и сохранение файла**:
   - Если активна вкладка "JSON Editor" (индекс 0), вызывает метод `save_changes` экземпляра `promotion_app` для сохранения изменений.
   - Если активна вкладка "Product Editor" (индекс 2), вызывает метод `save_product` экземпляра `product_editor_app` для сохранения продукта.

ASCII схема работы функции:

```
Получение индекса активной вкладки
│
├───> Проверка активной вкладки
│    │
│    ├───> Если активна вкладка "JSON Editor", вызов promotion_app.save_changes
│    │
│    └───> Если активна вкладка "Product Editor", вызов product_editor_app.save_product
```

Пример:

```python
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

1. **Закрытие приложения**:
   - Вызывает метод `close` для закрытия главного окна приложения.

ASCII схема работы функции:

```
Вызов self.close()
```

Пример:

```python
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

**Назначение**: Копирует выбранный текст в буфер обмена.

**Как работает функция**:

1. **Получение виджета в фокусе**:
   - Получает виджет, находящийся в фокусе ввода, с помощью метода `self.focusWidget()`.
2. **Проверка типа виджета**:
   - Проверяет, является ли виджет экземпляром одного из классов: `QtWidgets.QLineEdit`, `QtWidgets.QTextEdit` или `QtWidgets.QPlainTextEdit`.
3. **Копирование текста**:
   - Если виджет является текстовым полем, вызывает метод `copy()` для копирования выделенного текста в буфер обмена.
   - В противном случае, выводит предупреждающее сообщение об отсутствии текстового виджета в фокусе.

ASCII схема работы функции:

```
Получение виджета в фокусе
│
├───> Проверка типа виджета
│    │
│    ├───> Если виджет является текстовым полем, вызов widget.copy()
│    │
│    └───> Если виджет не является текстовым полем, вывод предупреждающего сообщения
```

Пример:

```python
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

1. **Получение виджета в фокусе**:
   - Получает виджет, находящийся в фокусе ввода, с помощью метода `self.focusWidget()`.
2. **Проверка типа виджета**:
   - Проверяет, является ли виджет экземпляром одного из классов: `QtWidgets.QLineEdit`, `QtWidgets.QTextEdit` или `QtWidgets.QPlainTextEdit`.
3. **Вставка текста**:
   - Если виджет является текстовым полем, вызывает метод `paste()` для вставки текста из буфера обмена.
   - В противном случае, выводит предупреждающее сообщение об отсутствии текстового виджета в фокусе.

ASCII схема работы функции:

```
Получение виджета в фокусе
│
├───> Проверка типа виджета
│    │
│    ├───> Если виджет является текстовым полем, вызов widget.paste()
│    │
│    └───> Если виджет не является текстовым полем, вывод предупреждающего сообщения
```

Пример:

```python
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

**Назначение**: Загружает JSON файл.

**Как работает функция**:

1. **Загрузка файла**:
   - Пытается вызвать метод `load_file` экземпляра `promotion_app` для загрузки JSON файла.
2. **Обработка исключений**:
   - Если при загрузке файла возникает исключение, выводит сообщение об ошибке с использованием `QMessageBox`.

ASCII схема работы функции:

```
Попытка вызова promotion_app.load_file(campaign_file)
│
└───> Обработка исключений
     │
     └───> Если возникло исключение, вывод сообщения об ошибке
```

Пример:

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

1. **Инициализация приложения**:
   - Создает экземпляр класса `QApplication`, который является основой любого приложения PyQt.
2. **Создание и установка event loop**:
   - Создает экземпляр `QEventLoop` для асинхронных операций.
   - Устанавливает созданный event loop в качестве текущего event loop для модуля `asyncio`.
3. **Создание и отображение главного окна**:
   - Создает экземпляр класса `MainApp`, который представляет главное окно приложения.
   - Отображает главное окно с помощью метода `show()`.
4. **Запуск event loop**:
   - Запускает event loop, который обрабатывает события и обеспечивает работу приложения.

ASCII схема работы функции:

```
Создание QApplication
│
├───> Создание QEventLoop
│    │
│    └───> Установка QEventLoop в качестве текущего event loop для asyncio
│
├───> Создание MainApp
│    │
│    └───> Отображение главного окна
│
└───> Запуск event loop
```

Пример:

```python
if __name__ == "__main__":
    main()
```