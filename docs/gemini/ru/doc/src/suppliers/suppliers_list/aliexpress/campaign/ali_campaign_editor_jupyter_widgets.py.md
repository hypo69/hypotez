# Jupyter Widgets для редактора кампаний AliExpress

## Обзор

Этот модуль содержит виджеты для управления кампаниями AliExpress в Jupyter notebooks. 
Виджеты предоставляют удобный интерфейс для выбора кампаний, категорий и языков, а также для выполнения действий, таких как 
инициализация редактора, сохранение кампаний и показ продуктов.

## Подробней

Модуль использует класс `JupyterCampaignEditorWidgets`, который предоставляет виджеты для работы с редакторам кампаний AliExpress в 
Jupyter Notebooks. Класс работает с Google Sheets. В модуле определены методы, которые отвечают за 
инициализацию редактора, сохранение кампаний и показ продуктов.

## Классы

### `JupyterCampaignEditorWidgets`

**Описание**:  Класс предоставляет виджеты для управления кампаниями AliExpress в Jupyter notebooks.

**Атрибуты**:

- `language: str`:  Язык кампании.
- `currency: str`:  Валюта кампании.
- `campaign_name: str`:  Название кампании.
- `category_name: str`:  Название категории.
- `category:SimpleNamespace`:  Объект, содержащий информацию о категории.
- `campaign_editor: AliCampaignEditor`:  Объект редактора кампании.
- `products:list[SimpleNamespace]`: Список продуктов в выбранной категории.

**Методы**:

- `__init__(self)`: Инициализирует виджеты и устанавливает редактор кампании.
- `initialize_campaign_editor(self, _)`: Инициализирует редактор кампании на основе выбранной кампании и категории.
- `update_category_dropdown(self, campaign_name: str)`: Обновляет выпадающий список категорий на основе выбранной кампании.
- `on_campaign_name_change(self, change: dict[str, str])`: Обрабатывает изменения в выпадающем списке названий кампаний.
- `on_category_change(self, change: dict[str, str])`: Обрабатывает изменения в выпадающем списке категорий.
- `on_language_change(self, change: dict[str, str])`: Обрабатывает изменения в выпадающем списке языков.
- `save_campaign(self, _)`: Сохраняет кампанию и ее категории.
- `show_products(self, _)`: Отображает продукты в выбранной категории.
- `open_spreadsheet(self, _)`: Открывает Google Spreadsheet в браузере.
- `setup_callbacks(self)`: Устанавливает обратные вызовы для виджетов.
- `display_widgets(self)`: Отображает виджеты для взаимодействия в Jupyter notebook.

**Принцип работы**: 
   
   1.  **Инициализация**:  При создании объекта `JupyterCampaignEditorWidgets`  инициализируются виджеты для выбора кампаний, категорий и языков, 
       а также  `campaign_editor`, который является объектом класса  `AliCampaignEditor`, отвечающим за взаимодействие с Google Sheets.
   2.  **Выбор кампании**:  При изменении выбора кампании в выпадающем списке `campaign_name_dropdown` вызывается метод  `on_campaign_name_change`, 
       который обновляет выпадающий список категорий и инициализирует редактор кампании.
   3.  **Выбор категории**:  При изменении выбора категории в выпадающем списке  `category_name_dropdown` вызывается метод  `on_category_change`, 
       который инициализирует редактор кампании.
   4.  **Выбор языка**:  При изменении выбора языка в выпадающем списке `language_dropdown` вызывается метод  `on_language_change`, 
       который инициализирует редактор кампании.
   5.  **Сохранение**:  Метод  `save_campaign`  сохраняет кампанию и ее категории в Google Sheets, используя методы  `AliCampaignEditor`.
   6.  **Показ продуктов**:  Метод  `show_products`  отображает продукты в выбранной категории, используя методы  `AliCampaignEditor`.
   7.  **Открытие Google Sheets**:  Метод  `open_spreadsheet`  открывает Google Spreadsheet в браузере.

## Параметры класса

- `campaigns_directory:str`: Путь к каталогу, где хранятся кампании.
- `campaign_name_dropdown: widgets.Dropdown`:  Выпадающий список для выбора названия кампании.
- `category_name_dropdown: widgets.Dropdown`:  Выпадающий список для выбора названия категории.
- `language_dropdown: widgets.Dropdown`:  Выпадающий список для выбора языка и валюты.
- `initialize_button: widgets.Button`: Кнопка для инициализации редактора кампании.
- `save_button: widgets.Button`:  Кнопка для сохранения кампании.
- `show_products_button: widgets.Button`:  Кнопка для отображения продуктов.
- `open_spreadsheet_button: widgets.Button`:  Кнопка для открытия Google Spreadsheet.

## Примеры

```python
from src.suppliers.suppliers_list.aliexpress.campaign import JupyterCampaignEditorWidgets

# Создание объекта виджетов
editor_widgets: JupyterCampaignEditorWidgets = JupyterCampaignEditorWidgets()

# Отображение виджетов
editor_widgets.display_widgets()

# Инициализация редактора с использованием первой выбранной кампании
editor_widgets.initialize_campaign_editor(None)
```

## Методы класса

### `initialize_campaign_editor(self, _)`

```python
    def initialize_campaign_editor(self, _):
        """Инициализирует редактор кампании.\n\n        Args:\n            _: Unused argument, required for button callback.\n\n        Sets up the campaign editor based on the selected campaign and category.\n        """
        
        self.campaign_name = self.campaign_name_dropdown.value or None
        self.category_name = self.category_name_dropdown.value or None
        
        self.language, self.currency = self.language_dropdown.value.split()
        if self.campaign_name:
            self.update_category_dropdown(self.campaign_name)
            self.campaign_editor = AliCampaignEditor(campaign_name = self.campaign_name, language = self.language, currency = self.currency)
            
            if self.category_name:
                self.category = self.campaign_editor.get_category(self.category_name)
                self.products = self.campaign_editor.get_category_products(self.category_name)
        else:
            logger.warning(
                "Please select a campaign name before initializing the editor."
            )

```

**Назначение**: Метод инициализирует редактор кампании  `AliCampaignEditor`  на основе выбранной кампании, категории и языка.

**Параметры**:

- `_`:  Неиспользуемый параметр, необходимый для обратного вызова кнопки.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод извлекает значения выбранной кампании, категории и языка из соответствующих виджетов.
   -  Если выбрана кампания, метод обновляет выпадающий список категорий с использованием метода  `update_category_dropdown`.
   -  Создает объект  `AliCampaignEditor`  и инициализирует его выбранными параметрами.
   -  Если выбрана категория, метод извлекает информацию о категории и список продуктов с использованием методов  `AliCampaignEditor`.

**Пример**: 

   ```python
   # Инициализация редактора с выбранной кампанией 'SummerSale' и категорией 'Electronics'
   editor_widgets.initialize_campaign_editor(None) 
   ```

### `update_category_dropdown(self, campaign_name: str)`

```python
    def update_category_dropdown(self, campaign_name: str):
        """Update the category dropdown based on the selected campaign.\n\n        Args:\n            campaign_name (str): The name of the campaign.\n\n        Example:\n            >>> self.update_category_dropdown("SummerSale")\n        """
        
        campaign_path = self.campaigns_directory / campaign_name / "category"
        campaign_categories = get_directory_names(campaign_path)
        self.category_name_dropdown.options = campaign_categories
```

**Назначение**: Метод обновляет выпадающий список категорий на основе выбранной кампании.

**Параметры**:

- `campaign_name (str)`:  Название кампании.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод извлекает список категорий из каталога кампании, используя функцию  `get_directory_names`.
   -  Обновляет выпадающий список категорий  `category_name_dropdown`  полученным списком.

**Пример**: 

   ```python
   # Обновление выпадающего списка категорий для кампании 'SummerSale'
   editor_widgets.update_category_dropdown("SummerSale")
   ```

### `on_campaign_name_change(self, change: dict[str, str])`

```python
    def on_campaign_name_change(self, change: dict[str, str]):
        """Handle changes in the campaign name dropdown.\n\n        Args:\n            change (dict[str, str]): The change dictionary containing the new value.\n\n        Example:\n            >>> self.on_campaign_name_change({\'new\': \'SummerSale\'})\n        """
        self.campaign_name = change["new"]
        self.update_category_dropdown(self.campaign_name)
        self.initialize_campaign_editor(None)  # Reinitialize with newcampaign
```

**Назначение**: Метод обрабатывает изменения в выпадающем списке названий кампаний.

**Параметры**:

- `change (dict[str, str])`:  Словарь изменений, содержащий новое значение.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод получает новое значение из словаря изменений.
   -  Обновляет  `campaign_name`  с новым значением.
   -  Обновляет выпадающий список категорий с использованием метода  `update_category_dropdown`.
   -  Инициализирует редактор кампании с использованием метода  `initialize_campaign_editor`.

**Пример**: 

   ```python
   # Вызов метода при изменении названия кампании на 'SummerSale'
   editor_widgets.on_campaign_name_change({ 'new': 'SummerSale' })
   ```

### `on_category_change(self, change: dict[str, str])`

```python
    def on_category_change(self, change: dict[str, str]):
        """Handle changes in the category dropdown.\n\n        Args:\n            change (dict[str, str]): The change dictionary containing the new value.\n\n        Example:\n            >>> self.on_category_change({\'new\': \'Electronics\'})\n        """
        self.category_name = change["new"]
        self.initialize_campaign_editor(None)  # Reinitialize with new category
```

**Назначение**: Метод обрабатывает изменения в выпадающем списке категорий.

**Параметры**:

- `change (dict[str, str])`:  Словарь изменений, содержащий новое значение.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод получает новое значение из словаря изменений.
   -  Обновляет  `category_name`  с новым значением.
   -  Инициализирует редактор кампании с использованием метода  `initialize_campaign_editor`.

**Пример**: 

   ```python
   # Вызов метода при изменении категории на 'Electronics'
   editor_widgets.on_category_change({ 'new': 'Electronics' })
   ```

### `on_language_change(self, change: dict[str, str])`

```python
    def on_language_change(self, change: dict[str, str]):
        """Handle changes in the language dropdown.\n\n        Args:\n            change (dict[str, str]): The change dictionary containing the new value.\n\n        Example:\n            >>> self.on_language_change({\'new\': \'EN USD\'})\n        """
        self.language, self.currency = change["new"].split()
        self.initialize_campaign_editor(None)  # Reinitialize with new language/currency
```

**Назначение**: Метод обрабатывает изменения в выпадающем списке языков.

**Параметры**:

- `change (dict[str, str])`:  Словарь изменений, содержащий новое значение.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод получает новое значение из словаря изменений.
   -  Разделяет новое значение на язык и валюту.
   -  Обновляет  `language`  и  `currency`  новыми значениями.
   -  Инициализирует редактор кампании с использованием метода  `initialize_campaign_editor`.

**Пример**: 

   ```python
   # Вызов метода при изменении языка на 'EN USD'
   editor_widgets.on_language_change({ 'new': 'EN USD' })
   ```

### `save_campaign(self, _)`

```python
    def save_campaign(self, _):
        """Save the campaign and its categories.\n\n        Args:\n            _: Unused argument, required for button callback.\n\n        Example:\n            >>> self.save_campaign(None)\n        """
        self.campaign_name = self.campaign_name_dropdown.value
        self.category_name = self.category_name_dropdown.value
        self.language, self.currency = self.language_dropdown.value.split()

        if self.campaign_name and self.language:
            self.campaign_editor = AliCampaignEditor(
                campaign_name=self.campaign_name,
                category_name=self.category_name if self.category_name else None,
                language=self.language,
            )
            try:
                self.campaign_editor.save_categories_from_worksheet()
            except Exception as ex:
                logger.error("Error saving campaign.", ex, True)
        else:
            logger.warning (
                "Please select campaign name and language/currency before saving the campaign."
            )
```

**Назначение**:  Метод сохраняет кампанию и ее категории в Google Sheets.

**Параметры**:

- `_`:  Неиспользуемый параметр, необходимый для обратного вызова кнопки.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод извлекает значения выбранной кампании, категории и языка из соответствующих виджетов.
   -  Если выбраны кампания и язык, метод создает объект  `AliCampaignEditor`  и сохраняет категории из Google Sheets с использованием 
       метода  `save_categories_from_worksheet`.
   -  В случае ошибки при сохранении кампании, метод выводит сообщение об ошибке в лог.

**Пример**: 

   ```python
   # Сохранение кампании
   editor_widgets.save_campaign(None)
   ```

### `show_products(self, _)`

```python
    def show_products(self, _):
        """Display the products in the selected category.\n\n        Args:\n            _: Unused argument, required for button callback.\n\n        Example:\n            >>> self.show_products(None)\n        """
        campaign_name = self.campaign_name_dropdown.value
        category_name = self.category_name_dropdown.value

        try:
            self.campaign_editor = AliCampaignEditor(
                campaign_name=campaign_name,
                language=self.language,
                currency=self.currency,
            )
            self.campaign_editor.set_products_worksheet(category_name)
        except Exception as ex:
            logger.error("Error displaying products.", ex, True)
```

**Назначение**: Метод отображает продукты в выбранной категории.

**Параметры**:

- `_`:  Неиспользуемый параметр, необходимый для обратного вызова кнопки.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод извлекает значения выбранной кампании и категории из соответствующих виджетов.
   -  Создает объект  `AliCampaignEditor`  и использует его для настройки листа с продуктами с использованием 
       метода  `set_products_worksheet`.
   -  В случае ошибки при отображении продуктов, метод выводит сообщение об ошибке в лог.

**Пример**: 

   ```python
   # Отображение продуктов в выбранной категории
   editor_widgets.show_products(None)
   ```

### `open_spreadsheet(self, _)`

```python
    def open_spreadsheet(self, _):
        """Open the Google Spreadsheet in a browser.\n\n        Args:\n            _: Unused argument, required for button callback.\n\n        Example:\n            >>> self.open_spreadsheet(None)\n        """
        if self.campaign_editor:
            spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{self.campaign_editor.spreadsheet_id}/edit"
            webbrowser.open(spreadsheet_url)
        else:
            print("Please initialize the campaign editor first.")
```

**Назначение**: Метод открывает Google Spreadsheet в браузере.

**Параметры**:

- `_`:  Неиспользуемый параметр, необходимый для обратного вызова кнопки.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Если редактор кампании инициализирован, метод формирует URL Google Spreadsheet и открывает его в браузере.
   -  В противном случае, метод выводит сообщение о необходимости инициализировать редактор кампании.

**Пример**: 

   ```python
   # Открытие Google Spreadsheet
   editor_widgets.open_spreadsheet(None)
   ```

### `setup_callbacks(self)`

```python
    def setup_callbacks(self):
        """Set up callbacks for the widgets."""
        self.campaign_name_dropdown.observe(self.on_campaign_name_change, names="value")
        self.category_name_dropdown.observe(self.on_category_change, names="value")
        self.language_dropdown.observe(self.on_language_change, names="value")
        self.initialize_button.on_click(self.initialize_campaign_editor)
        self.save_button.on_click(self.save_campaign)
        self.show_products_button.on_click(self.show_products)
        self.open_spreadsheet_button.on_click(self.open_spreadsheet)
```

**Назначение**:  Метод устанавливает обратные вызовы для виджетов.

**Параметры**: 

  - `None`.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод устанавливает обратные вызовы для всех виджетов, чтобы при изменении значения виджета вызывался соответствующий метод 
       класса  `JupyterCampaignEditorWidgets`.

**Пример**: 

   ```python
   # Установка обратных вызовов для виджетов
   editor_widgets.setup_callbacks()
   ```

### `display_widgets(self)`

```python
    def display_widgets(self):
        """Display the widgets for interaction in the Jupyter notebook.\n\n        Initializes the campaign editor automatically with the first campaign selected.\n\n        Example:\n            >>> self.display_widgets()\n        """
        display(
            self.campaign_name_dropdown,
            self.category_name_dropdown,
            self.language_dropdown,
            self.initialize_button,
            self.save_button,
            self.show_products_button,
            self.open_spreadsheet_button,
        )
        # Initialize the campaign editor with the first campaign selected
        self.initialize_campaign_editor(None)
```

**Назначение**: Метод отображает виджеты для взаимодействия в Jupyter notebook.

**Параметры**:

  - `None`.

**Возвращает**:  `None`.

**Принцип работы**: 

   -  Метод отображает все виджеты в Jupyter notebook с использованием функции  `display`.
   -  Автоматически инициализирует редактор кампании с использованием метода  `initialize_campaign_editor`.

**Пример**: 

   ```python
   # Отображение виджетов
   editor_widgets.display_widgets()