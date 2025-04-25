# Модуль `ProductEditor`

## Обзор

Модуль `ProductEditor` реализует класс `ProductEditor` для создания графического редактора продуктов.

## Подробнее

Модуль используется для:

- **Загрузки JSON-файлов с данными о продуктах:**  Файлы должны быть в формате, совместимом с классом `AliCampaignEditor`.
- **Отображения информации о продуктах:** Редактор предоставляет графический интерфейс для отображения данных о продуктах из загруженного файла.
- **Подготовки продуктов:**  Редактор позволяет подготовить продукт для загрузки в PrestaShop, используя функции класса `AliCampaignEditor`. 

## Классы

### `ProductEditor`

**Описание**: Класс `ProductEditor` создает графический редактор для работы с продуктами.

**Наследует**: `QtWidgets.QWidget` 

**Атрибуты**:

- `data (SimpleNamespace)`:  Данные о продукте, загруженные из JSON-файла.
- `language (str)`:  Язык продукта (по умолчанию `EN`).
- `currency (str)`:  Валюта продукта (по умолчанию `USD`).
- `file_path (str)`:  Путь к JSON-файлу с данными о продукте.
- `editor (AliCampaignEditor)`:  Инстанс класса `AliCampaignEditor`, используемый для подготовки продукта. 

**Методы**:

- `__init__(self, parent=None, main_app=None)`: Инициализирует виджет `ProductEditor`, устанавливает соединение с основным приложением `main_app`.
- `setup_ui(self)`:  Создает UI-элементы редактора: кнопку открытия файла, метку имени файла, кнопку подготовки продукта.
- `setup_connections(self)`:  Настраивает связи между сигналами и слотами UI-элементов. 
- `open_file(self)`:  Открывает диалоговое окно для выбора JSON-файла с данными о продукте. 
- `load_file(self, file_path)`: Загружает JSON-файл, парсит данные, устанавливает путь к файлу в `file_path`, отображает имя файла, создает экземпляр `AliCampaignEditor` и создает виджеты для отображения данных.
- `create_widgets(self, data)`:  Создает виджеты для отображения данных продукта.
- `prepare_product_async(self)`:  Асинхронно готовит продукт для загрузки в PrestaShop.

## Методы класса

### `__init__`

```python
    def __init__(self, parent=None, main_app=None):
        """ 
        Инициализирует виджет `ProductEditor`. 

        Args:
            parent (QWidget, optional): Родительский виджет. Defaults to None.
            main_app (MainApp, optional): Основное приложение. Defaults to None.

        Returns:
            None

        """
        super().__init__(parent)
        self.main_app = main_app  # Save the MainApp instance

        self.setup_ui()
        self.setup_connections()
```

**Назначение**:  Создает инстанс `ProductEditor`.

**Параметры**:

- `parent (QWidget, optional)`: Родительский виджет (по умолчанию `None`).
- `main_app (MainApp, optional)`:  Экземпляр основного приложения (по умолчанию `None`).

**Возвращает**: `None`

**Как работает функция**:
- Вызывает конструктор родительского класса `QtWidgets.QWidget`.
- Сохраняет экземпляр основного приложения в `self.main_app`.
- Вызывает методы `setup_ui` и `setup_connections` для настройки UI и связей.

### `setup_ui`

```python
    def setup_ui(self):
        """ 
        Создает UI-элементы редактора: кнопку открытия файла, метку имени файла, кнопку подготовки продукта. 
        """
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

**Назначение**:  Настраивает UI-элементы редактора.

**Параметры**:  `None`

**Возвращает**:  `None`

**Как работает функция**:

- Устанавливает заголовок окна `Product Editor`.
- Устанавливает размер окна (1800 x 800 пикселей).
- Создает кнопку `self.open_button` для открытия файла и подключает к ней сигнал `clicked` обработчик `self.open_file`.
- Создает метку `self.file_name_label` для отображения имени файла и устанавливает ее текст "No file selected". 
- Создает кнопку `self.prepare_button` для подготовки продукта и подключает к ней сигнал `clicked` обработчик `self.prepare_product_async`.
- Создает вертикальный макет `layout` и добавляет в него кнопки и метку.
- Устанавливает макет `layout` для виджета `ProductEditor`.

### `setup_connections`

```python
    def setup_connections(self):
        """ 
        Настраивает связи между сигналами и слотами UI-элементов. 
        """
        pass
```

**Назначение**:  Настраивает связи между сигналами и слотами UI-элементов.

**Параметры**:  `None`

**Возвращает**:  `None`

**Как работает функция**:
- В данный момент не содержит никакой функциональности. 
- Вероятно, в будущем в этой функции будет реализована настройка дополнительных связей между сигналами и слотами.

### `open_file`

```python
    def open_file(self):
        """ 
        Открывает диалоговое окно для выбора JSON-файла с данными о продукте. 
        """
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

**Назначение**:  Открывает диалоговое окно для выбора JSON-файла.

**Параметры**:  `None`

**Возвращает**:  `None`

**Как работает функция**:
- Использует `QtWidgets.QFileDialog.getOpenFileName` для открытия диалогового окна выбора файла.
- Задает начальную директорию для открытия диалогового окна: `c:/user/documents/repos/hypotez/data/aliexpress/products`.
- Фильтрует файлы по расширению `*.json`.
- Если файл выбран (`file_path` не пуст), вызывает метод `self.load_file` для загрузки данных из файла.

### `load_file`

```python
    def load_file(self, file_path):
        """ 
        Загружает JSON-файл, парсит данные, устанавливает путь к файлу в `file_path`, отображает имя файла, 
        создает экземпляр `AliCampaignEditor` и создает виджеты для отображения данных. 
        """
        try:
            self.data = j_loads_ns(file_path)
            self.file_path = file_path
            self.file_name_label.setText(f"File: {self.file_path}")
            self.editor = AliCampaignEditor(file_path=file_path)
            self.create_widgets(self.data)
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")
```

**Назначение**:  Загружает JSON-файл, парсит данные и отображает их в редакторе. 

**Параметры**:

- `file_path (str)`:  Путь к JSON-файлу.

**Возвращает**:  `None`

**Как работает функция**:

- Использует функцию `j_loads_ns` из модуля `src.utils.jjson` для парсинга JSON-файла.
- Сохраняет данные о продукте в `self.data`.
- Устанавливает путь к файлу в `self.file_path`.
- Обновляет текст метки `self.file_name_label`, чтобы отобразить имя файла.
- Создает экземпляр `AliCampaignEditor` с указанным путем к файлу.
- Вызывает метод `self.create_widgets` для создания виджетов для отображения данных продукта.
- Если произошла ошибка, выводит сообщение об ошибке с помощью `QtWidgets.QMessageBox.critical`. 

### `create_widgets`

```python
    def create_widgets(self, data):
        """ 
        Создает виджеты для отображения данных продукта. 
        """
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

**Назначение**:  Создает виджеты для отображения данных продукта, загруженных из JSON-файла. 

**Параметры**:

- `data (SimpleNamespace)`:  Данные о продукте.

**Возвращает**:  `None`

**Как работает функция**:

- Получает макет `layout` текущего виджета.
- Удаляет все предыдущие виджеты из макета, кроме кнопки открытия файла, метки имени файла и кнопки подготовки продукта.
- Создает метку `title_label` с заголовком "Product Title" и текстом из атрибута `data.title`.
- Добавляет метку `title_label` в макет `layout`.
- Создает метку `product_details_label` с заголовком "Product Details" и текстом из атрибута `data.details`. 
- Добавляет метку `product_details_label` в макет `layout`.

### `prepare_product_async`

```python
    @asyncSlot()
    async def prepare_product_async(self):
        """ 
        Асинхронно готовит продукт для загрузки в PrestaShop. 
        """
        if self.editor:
            try:
                await self.editor.prepare_product()
                QtWidgets.QMessageBox.information(self, "Success", "Product prepared successfully.")
            except Exception as ex:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to prepare product: {ex}")
```

**Назначение**:  Асинхронно готовит продукт для загрузки в PrestaShop. 

**Параметры**:  `None`

**Возвращает**:  `None`

**Как работает функция**:

- Проверяет, создан ли экземпляр `self.editor`.
- Если `self.editor` существует, запускает асинхронный вызов метода `prepare_product` из `self.editor`.
- При успешной подготовке продукта выводит сообщение об успехе с помощью `QtWidgets.QMessageBox.information`.
- Если произошла ошибка, выводит сообщение об ошибке с помощью `QtWidgets.QMessageBox.critical`.