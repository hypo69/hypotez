# Модуль `product.py`

## Обзор

Модуль `product.py` представляет собой часть проекта `hypotez` и предназначен для создания графического интерфейса (GUI) редактора товаров. Этот редактор позволяет открывать, просматривать и подготавливать информацию о товарах, загружаемую из JSON-файлов. Модуль использует библиотеку PyQt6 для создания интерфейса и включает функциональность для асинхронной подготовки товаров с использованием класса `AliCampaignEditor`.

## Подробнее

Модуль предоставляет класс `ProductEditor`, который является основным виджетом для редактирования информации о товарах. Он позволяет загружать данные о товарах из JSON-файлов, отображать основные детали, такие как заголовок и описание, и подготавливать товары к дальнейшей обработке.

## Классы

### `ProductEditor`

**Описание**: Класс `ProductEditor` представляет собой виджет PyQt6 для редактирования информации о товарах, загружаемой из JSON-файлов.

**Наследует**:
- `QtWidgets.QWidget`

**Атрибуты**:
- `data` (SimpleNamespace): Пространство имен для хранения данных о товаре. Изначально установлено в `None`.
- `language` (str): Язык, используемый в редакторе. По умолчанию установлен в `'EN'`.
- `currency` (str): Валюта, используемая в редакторе. По умолчанию установлена в `'USD'`.
- `file_path` (str): Путь к загруженному JSON-файлу. Изначально установлен в `None`.
- `editor` (AliCampaignEditor): Экземпляр класса `AliCampaignEditor` для подготовки товара.
- `main_app` (MainApp): Ссылка на экземпляр главного приложения.

**Методы**:
- `__init__(self, parent=None, main_app=None)`: Инициализирует виджет `ProductEditor`, настраивает пользовательский интерфейс и устанавливает соединения между сигналами и слотами.
- `setup_ui(self)`: Создает и настраивает компоненты пользовательского интерфейса, такие как кнопки и метки.
- `setup_connections(self)`: Устанавливает связи между сигналами и слотами. В текущей реализации отсутствует какая-либо функциональность.
- `open_file(self)`: Открывает диалоговое окно для выбора JSON-файла и загружает его содержимое.
- `load_file(self, file_path)`: Загружает JSON-файл по указанному пути и создает виджеты на основе загруженных данных.
- `create_widgets(self, data)`: Создает виджеты для отображения информации о товаре на основе загруженных данных.
- `prepare_product_async(self)`: Асинхронно подготавливает продукт с использованием `AliCampaignEditor`.

## Методы класса

### `__init__`

```python
def __init__(self, parent=None, main_app=None):
    """ Initialize the ProductEditor widget """
    super().__init__(parent)
    self.main_app = main_app  # Save the MainApp instance

    self.setup_ui()
    self.setup_connections()
```

**Назначение**: Инициализирует виджет `ProductEditor`, сохраняет ссылку на главный класс приложения, настраивает пользовательский интерфейс и устанавливает соединения между сигналами и слотами.

**Параметры**:
- `parent` (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
- `main_app` (MainApp, optional): Экземпляр главного приложения. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `QtWidgets.QWidget`.
- Сохраняет ссылку на главный класс приложения в атрибуте `self.main_app`.
- Вызывает методы `self.setup_ui()` и `self.setup_connections()` для настройки пользовательского интерфейса и установки связей между сигналами и слотами.

**Примеры**:
```python
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

app = QtWidgets.QApplication([])
main_app = MainApp()  # Предположим, что MainApp уже определен
product_editor = ProductEditor(main_app=main_app)
product_editor.show()
app.exec()
```

### `setup_ui`

```python
def setup_ui(self):
    """ Setup the user interface """
    self.setWindowTitle("Product Editor")
    self.resize(1800, 800)

    # Define UI components
    self.open_button = QtWidgets.QPushButton("Open JSON File")
    self.open_button.clicked.connect(self.open_file)

    self.file_name_label = QtWidgets.QLabel("No file selected")
    
    self.prepare_button = QtWidgets.QPushButton("Prepare Product")
    self.prepare_button.clicked.connect(self.prepare_product_async)

    layout = QtWidgets.QVBoxLayout(self)
    layout.addWidget(self.open_button)
    layout.addWidget(self.file_name_label)
    layout.addWidget(self.prepare_button)

    self.setLayout(layout)
```

**Назначение**: Настраивает пользовательский интерфейс виджета `ProductEditor`, включая установку заголовка окна, определение размеров и добавление кнопок и меток.

**Как работает функция**:
- Устанавливает заголовок окна виджета `ProductEditor` на "Product Editor".
- Устанавливает размер окна виджета на 1800x800 пикселей.
- Определяет компоненты пользовательского интерфейса, такие как кнопки "Open JSON File" и "Prepare Product", а также метку для отображения имени выбранного файла.
- Устанавливает обработчики событий для кнопок, связывая их с соответствующими методами (`self.open_file` и `self.prepare_product_async`).
- Создает вертикальный макет (`QtWidgets.QVBoxLayout`) и добавляет в него компоненты пользовательского интерфейса.
- Устанавливает созданный макет в качестве макета для виджета `ProductEditor`.

**Примеры**:
```python
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

app = QtWidgets.QApplication([])
product_editor = ProductEditor()
product_editor.show()
app.exec()
```

### `setup_connections`

```python
def setup_connections(self):
    """ Setup signal-slot connections """
    pass
```

**Назначение**: Устанавливает связи между сигналами и слотами. В текущей реализации отсутствует какая-либо функциональность.

**Как работает функция**:
- В текущей реализации функция ничего не делает (`pass`). Она предназначена для установки связей между сигналами и слотами, но в данном случае такие связи не установлены.

**Примеры**:
```python
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

app = QtWidgets.QApplication([])
product_editor = ProductEditor()
product_editor.setup_connections()  # В данном случае ничего не произойдет
product_editor.show()
app.exec()
```

### `open_file`

```python
def open_file(self):
    """ Open a file dialog to select and load a JSON file """
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
        self,
        "Open JSON File",
        "c:/user/documents/repos/hypotez/data/aliexpress/products",
        "JSON files (*.json)"
    )
    if not file_path:
        return  # No file selected

    self.load_file(file_path)
```

**Назначение**: Открывает диалоговое окно для выбора JSON-файла и загружает его содержимое с использованием метода `self.load_file`.

**Как работает функция**:
- Вызывает `QtWidgets.QFileDialog.getOpenFileName` для открытия диалогового окна выбора файла.
- Устанавливает заголовок диалогового окна на "Open JSON File".
- Устанавливает начальную директорию для поиска файлов на "c:/user/documents/repos/hypotez/data/aliexpress/products".
- Устанавливает фильтр файлов, чтобы отображались только JSON-файлы (`"JSON files (*.json)"`).
- Если файл не выбран (путь к файлу пустой), функция завершается.
- Если файл выбран, вызывает метод `self.load_file` для загрузки содержимого файла.

**Примеры**:
```python
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

app = QtWidgets.QApplication([])
product_editor = ProductEditor()
product_editor.open_file()  # Откроется диалоговое окно выбора файла
product_editor.show()
app.exec()
```

### `load_file`

```python
def load_file(self, file_path):
    """ Load a JSON file """
    try:
        self.data = j_loads_ns(file_path)
        self.file_path = file_path
        self.file_name_label.setText(f"File: {self.file_path}")
        self.editor = AliCampaignEditor(file_path=file_path)
        self.create_widgets(self.data)
    except Exception as ex:
        QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")
```

**Назначение**: Загружает JSON-файл по указанному пути, создает экземпляр `AliCampaignEditor` и создает виджеты на основе загруженных данных.

**Параметры**:
- `file_path` (str): Путь к JSON-файлу.

**Как работает функция**:
- Пытается выполнить следующие действия:
  - Загружает JSON-файл с использованием функции `j_loads_ns` и сохраняет данные в атрибуте `self.data`.
  - Сохраняет путь к файлу в атрибуте `self.file_path`.
  - Обновляет текст метки `self.file_name_label`, чтобы отобразить имя выбранного файла.
  - Создает экземпляр класса `AliCampaignEditor`, передавая путь к файлу.
  - Вызывает метод `self.create_widgets` для создания виджетов на основе загруженных данных.
- Если происходит исключение, отображает диалоговое окно с сообщением об ошибке.

**Примеры**:
```python
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

app = QtWidgets.QApplication([])
product_editor = ProductEditor()
file_path = "c:/user/documents/repos/hypotez/data/aliexpress/products/example.json"  # Замените на реальный путь
product_editor.load_file(file_path)
product_editor.show()
app.exec()
```

### `create_widgets`

```python
def create_widgets(self, data):
    """ Create widgets based on the data loaded from the JSON file """
    layout = self.layout()

    # Remove previous widgets except open button and file label
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget not in [self.open_button, self.file_name_label, self.prepare_button]:
            widget.deleteLater()

    title_label = QtWidgets.QLabel(f"Product Title: {data.title}")
    layout.addWidget(title_label)

    # Additional product-specific details
    product_details_label = QtWidgets.QLabel(f"Product Details: {data.details}")
    layout.addWidget(product_details_label)
```

**Назначение**: Создает виджеты для отображения информации о товаре на основе загруженных данных.

**Параметры**:
- `data` (SimpleNamespace): Данные о товаре, загруженные из JSON-файла.

**Как работает функция**:
- Получает макет виджета (`self.layout()`).
- Удаляет все предыдущие виджеты из макета, кроме кнопок `self.open_button`, `self.prepare_button` и метки `self.file_name_label`.
  - Перебирает виджеты в обратном порядке, чтобы избежать проблем с индексацией при удалении.
  - Проверяет, входит ли виджет в список исключений (`[self.open_button, self.file_name_label, self.prepare_button]`).
  - Если виджет не входит в список исключений, вызывает метод `widget.deleteLater()` для его удаления.
- Создает метку для отображения заголовка продукта (`data.title`).
- Добавляет метку заголовка продукта в макет.
- Создает метку для отображения деталей продукта (`data.details`).
- Добавляет метку деталей продукта в макет.

**Примеры**:
```python
from PyQt6 import QtWidgets
from types import SimpleNamespace
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

app = QtWidgets.QApplication([])
product_editor = ProductEditor()
data = SimpleNamespace(title="Example Product", details="Some details about the product.")
product_editor.create_widgets(data)
product_editor.show()
app.exec()
```

### `prepare_product_async`

```python
@asyncSlot()
async def prepare_product_async(self):
    """ Asynchronously prepare the product """
    if self.editor:
        try:
            await self.editor.prepare_product()
            QtWidgets.QMessageBox.information(self, "Success", "Product prepared successfully.")
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to prepare product: {ex}")
```

**Назначение**: Асинхронно подготавливает продукт с использованием `AliCampaignEditor`.

**Как работает функция**:
- Проверяет, существует ли экземпляр `AliCampaignEditor` (`self.editor`).
- Если экземпляр существует, пытается выполнить следующие действия:
  - Асинхронно вызывает метод `prepare_product` экземпляра `AliCampaignEditor`.
  - Отображает диалоговое окно с сообщением об успешной подготовке продукта.
- Если происходит исключение, отображает диалоговое окно с сообщением об ошибке.

**Примеры**:
```python
import asyncio
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor

async def main():
    app = QtWidgets.QApplication([])
    product_editor = ProductEditor()
    product_editor.editor = AliCampaignEditor(file_path="c:/user/documents/repos/hypotez/data/aliexpress/products/example.json")  # Замените на реальный путь
    await product_editor.prepare_product_async()
    product_editor.show()
    app.exec()

if __name__ == "__main__":
    asyncio.run(main())
```

## Параметры класса

- `data` (SimpleNamespace): Пространство имен для хранения данных о товаре. Изначально установлено в `None`.
- `language` (str): Язык, используемый в редакторе. По умолчанию установлен в `'EN'`.
- `currency` (str): Валюта, используемая в редакторе. По умолчанию установлена в `'USD'`.
- `file_path` (str): Путь к загруженному JSON-файлу. Изначально установлен в `None`.
- `editor` (AliCampaignEditor): Экземпляр класса `AliCampaignEditor` для подготовки товара.
- `main_app` (MainApp): Ссылка на экземпляр главного приложения.

**Примеры**:
```python
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

app = QtWidgets.QApplication([])
product_editor = ProductEditor()
product_editor.language = "RU"
product_editor.currency = "RUB"
product_editor.show()
app.exec()