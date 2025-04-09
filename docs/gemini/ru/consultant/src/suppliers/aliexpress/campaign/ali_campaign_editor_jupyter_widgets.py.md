### **Анализ кода модуля `ali_campaign_editor_jupyter_widgets.py`**

## Анализ кода модуля `ali_campaign_editor_jupyter_widgets.py`

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован с использованием классов и функций.
  - Присутствуют docstring для большинства методов и классов, что облегчает понимание кода.
  - Используются аннотации типов.
  - Код разбит на логические блоки, что упрощает его поддержку и расширение.
- **Минусы**:
  - Docstring написаны на английском языке, требуется перевод на русский.
  - Не все функции и методы имеют подробные docstring, особенно в части описания возвращаемых значений и возможных исключений.
  - В некоторых местах используются неявные преобразования типов, что может привести к ошибкам.
  - Не хватает обработки исключений в некоторых функциях, что может привести к неожиданному поведению программы.
  - Есть закомментированный код.
  -  Не все переменные аннотированы типом
  -  Встречается код со старым синтаксисом `dict[str, str]`, необходимо заменить на `dict[str, str]`
  -  `f"..."` - плохо читаемы, нужно использовать `.format()`

**Рекомендации по улучшению:**

1.  **Перевод Docstring на русский язык**:
    - Необходимо перевести все docstring на русский язык, чтобы соответствовать требованиям проекта.
    - Обновите примеры использования в docstring, чтобы они были более понятными и актуальными.

2.  **Улучшение Docstring**:
    - Дополните docstring для всех функций и методов, указав более подробное описание возвращаемых значений и возможных исключений.
    - Укажите примеры использования для каждой функции и метода, чтобы облегчить понимание их работы.

3.  **Явное преобразование типов**:
    - Используйте явное преобразование типов там, где это необходимо, чтобы избежать неявных преобразований и возможных ошибок.

4.  **Обработка исключений**:
    - Добавьте обработку исключений в функции, где это необходимо, чтобы предотвратить неожиданное поведение программы.
    - Используйте `logger.error` для записи информации об ошибках в лог.

5.  **Удаление закомментированного кода**:
    - Удалите закомментированный код, который не используется, чтобы улучшить читаемость кода.

6.  **Использовать `.format()` вместо `f"..."`**:
    - Замените `f"..."` на `.format()`, чтобы улучшить читаемость кода.
    ```python
    f"https://docs.google.com/spreadsheets/d/{self.campaign_editor.spreadsheet_id}/edit"
    # ->
    "https://docs.google.com/spreadsheets/d/{}/edit".format(self.campaign_editor.spreadsheet_id)
    ```

7.  **Обновление аннотации типов**:
    - Обновите аннотацию типов для переменных.

8. **Старый синтаксис**:
    - Замените `dict[str, str]` на `dict[str, str]`

**Оптимизированный код:**

```python
                ## \\file /src/suppliers/aliexpress/campaign/ali_campaign_editor_jupyter_widgets.py
# -*- coding: utf-8 -*-\

#! .pyenv/bin/python3

"""
Модуль для работы с Jupyter widgets для редактора кампаний AliExpress
====================================================================

Этот модуль содержит widgets для управления кампаниями AliExpress в Jupyter notebooks.

Testfile:
    file test_ali_campaign_editor_jupyter_widgets.py

Пример использования
----------------------

>>> editor_widgets: JupyterCampaignEditorWidgets = JupyterCampaignEditorWidgets()
>>> editor_widgets.display_widgets()
"""


from types import SimpleNamespace
import header
from pathlib import Path
from ipywidgets import widgets
from IPython.display import display
import webbrowser
from typing import List, Optional, Tuple, Dict, Any

from src import gs
from src.suppliers.aliexpress.campaign import AliCampaignEditor
from src.suppliers.aliexpress.utils import locales
from src.utils.printer import pprint, get_directory_names
from src.logger.logger import logger


class JupyterCampaignEditorWidgets:
    """
    Widgets для редактора кампаний AliExpress.

    Этот класс предоставляет widgets для взаимодействия и управления кампаниями AliExpress,
    включая выбор кампаний, категорий и языков, а также выполнение таких действий, как
    инициализация редакторов, сохранение кампаний и показ продуктов.

    Args:
        language (str): Язык кампании.
        currency (str): Валюта кампании.
        campaign_name (str): Название кампании.
        category_name (str): Название категории.
        category (SimpleNamespace): Объект категории.
        campaign_editor (AliCampaignEditor): Редактор кампании.
        products (list[SimpleNamespace]): Список продуктов.

    Example:
        >>> editor_widgets: JupyterCampaignEditorWidgets = JupyterCampaignEditorWidgets()
        >>> editor_widgets.display_widgets()
    """

    # Class attributes declaration
    language: str = None
    currency: str = None
    campaign_name: str = None
    category_name: str = None
    category: SimpleNamespace = None
    campaign_editor: AliCampaignEditor = None
    products: List[SimpleNamespace] = None

    def __init__(self) -> None:
        """
        Инициализирует widgets и настраивает редактор кампании.

        Настраивает widgets для выбора кампаний, категорий и языков. Также настраивает
        значения по умолчанию и callbacks для widgets.

        Args:
            campaigns_directory (str): Путь к директории кампаний.
            campaign_name_dropdown (widgets.Dropdown): Выпадающий список для выбора названия кампании.
            category_name_dropdown (widgets.Dropdown): Выпадающий список для выбора категории.
            language_dropdown (widgets.Dropdown): Выпадающий список для выбора языка/валюты.
            initialize_button (widgets.Button): Кнопка для инициализации редактора кампании.
            save_button (widgets.Button): Кнопка для сохранения кампании.
            show_products_button (widgets.Button): Кнопка для показа продуктов.
            open_spreadsheet_button (widgets.Button): Кнопка для открытия Google Spreadsheet.

        Raises:
            FileNotFoundError: Если директория кампаний не существует.

        """
        self.campaigns_directory: str = Path(
            gs.path.google_drive, "aliexpress", "campaigns"
        )

        if not self.campaigns_directory.exists():
            raise FileNotFoundError(
                "Directory does not exist: {}".format(self.campaigns_directory)
            )

        # self.languages = {"EN": "USD", "HE": "ILS", "RU": "ILS"}
        self.campaign_name_dropdown: widgets.Dropdown = widgets.Dropdown(
            options=get_directory_names(self.campaigns_directory),
            description="Campaign Name:",
        )
        self.category_name_dropdown: widgets.Dropdown = widgets.Dropdown(
            options=[], description="Category:"
        )
        self.language_dropdown: widgets.Dropdown = widgets.Dropdown(
            options=[
                "{} {}".format(key, value)
                for locale in locales
                for key, value in locale.items()
            ],
            description="Language/Currency:",
        )
        self.initialize_button: widgets.Button = widgets.Button(
            description="Initialize Campaign Editor",
            disabled=False,
        )
        self.save_button: widgets.Button = widgets.Button(
            description="Save Campaign",
            disabled=False,
        )
        self.show_products_button: widgets.Button = widgets.Button(
            description="Show Products",
            disabled=False,
        )
        self.open_spreadsheet_button: widgets.Button = widgets.Button(
            description="Open Google Spreadsheet",
            disabled=False,
        )

        # Set up callbacks
        self.setup_callbacks()

        # Initialize with default values
        self.initialize_campaign_editor(None)

    def initialize_campaign_editor(self, _: Any) -> None:
        """
        Инициализирует редактор кампании.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для button callback.

        Устанавливает редактор кампании на основе выбранной кампании и категории.
        """

        self.campaign_name: Optional[str] = self.campaign_name_dropdown.value or None
        self.category_name: Optional[str] = self.category_name_dropdown.value or None

        language_currency: List[str] = self.language_dropdown.value.split()
        self.language: str = language_currency[0]
        self.currency: str = language_currency[1]

        if self.campaign_name:
            self.update_category_dropdown(self.campaign_name)
            self.campaign_editor: AliCampaignEditor = AliCampaignEditor(
                campaign_name=self.campaign_name,
                language=self.language,
                currency=self.currency,
            )

            if self.category_name:
                self.category: SimpleNamespace = self.campaign_editor.get_category(
                    self.category_name
                )
                self.products: List[SimpleNamespace] = (
                    self.campaign_editor.get_category_products(self.category_name)
                )
        else:
            logger.warning(
                "Please select a campaign name before initializing the editor."
            )

    def update_category_dropdown(self, campaign_name: str) -> None:
        """
        Обновляет выпадающий список категорий на основе выбранной кампании.

        Args:
            campaign_name (str): Название кампании.

        Returns:
            campaign_categories (List[str]): Список категорий кампании.

        Raises:
            FileNotFoundError: Если директория кампании не существует.

        Example:
            >>> self.update_category_dropdown("SummerSale")
        """

        campaign_path: Path = (
            self.campaigns_directory / campaign_name / "category"
        )
        campaign_categories: List[str] = get_directory_names(campaign_path)
        self.category_name_dropdown.options: List[str] = campaign_categories

    def on_campaign_name_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке названий кампаний.

        Args:
            change (Dict[str, str]): Словарь изменений, содержащий новое значение.

        Returns:
            campaign_name (str): Название кампании.

        Raises:
            ValueError: Если новое значение не является строкой.

        Example:
            >>> self.on_campaign_name_change({'new': 'SummerSale'})
        """
        self.campaign_name: str = change["new"]
        self.update_category_dropdown(self.campaign_name)
        self.initialize_campaign_editor(None)  # Reinitialize with new campaign

    def on_category_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке категорий.

        Args:
            change (Dict[str, str]): Словарь изменений, содержащий новое значение.

        Returns:
            category_name (str): Название категории.

        Raises:
            ValueError: Если новое значение не является строкой.

        Example:
            >>> self.on_category_change({'new': 'Electronics'})
        """
        self.category_name: str = change["new"]
        self.initialize_campaign_editor(None)  # Reinitialize with new category

    def on_language_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке языков.

        Args:
            change (dict[str, str]): Словарь изменений, содержащий новое значение.

        Returns:
            language (str): Язык кампании.
            currency (str): Валюта кампании.

        Raises:
            ValueError: Если новое значение не является строкой.

        Example:
            >>> self.on_language_change({'new': 'EN USD'})
        """
        language_currency: List[str] = change["new"].split()
        self.language: str = language_currency[0]
        self.currency: str = language_currency[1]
        self.initialize_campaign_editor(None)  # Reinitialize with new language/currency

    def save_campaign(self, _: Any) -> None:
        """
        Сохраняет кампанию и ее категории.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для button callback.

        Raises:
            Exception: Если произошла ошибка при сохранении кампании.

        Example:
            >>> self.save_campaign(None)
        """
        self.campaign_name: str = self.campaign_name_dropdown.value
        self.category_name: str = self.category_name_dropdown.value
        language_currency: List[str] = self.language_dropdown.value.split()
        self.language: str = language_currency[0]
        self.currency: str = language_currency[1]

        if self.campaign_name and self.language:
            self.campaign_editor: AliCampaignEditor = AliCampaignEditor(
                campaign_name=self.campaign_name,
                category_name=self.category_name if self.category_name else None,
                language=self.language,
            )
            try:
                self.campaign_editor.save_categories_from_worksheet()
            except Exception as ex:
                logger.error("Error saving campaign.", ex, exc_info=True)
        else:
            logger.warning(
                "Please select campaign name and language/currency before saving the campaign."
            )

    def show_products(self, _: Any) -> None:
        """
        Отображает продукты в выбранной категории.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для button callback.

        Raises:
            Exception: Если произошла ошибка при отображении продуктов.

        Example:
            >>> self.show_products(None)
        """
        campaign_name: str = self.campaign_name_dropdown.value
        category_name: str = self.category_name_dropdown.value

        try:
            self.campaign_editor: AliCampaignEditor = AliCampaignEditor(
                campaign_name=campaign_name,
                language=self.language,
                currency=self.currency,
            )
            self.campaign_editor.set_products_worksheet(category_name)
        except Exception as ex:
            logger.error("Error displaying products.", ex, exc_info=True)

    def open_spreadsheet(self, _: Any) -> None:
        """
        Открывает Google Spreadsheet в браузере.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для button callback.

        Raises:
            Exception: Если не удалось открыть Google Spreadsheet.

        Example:
            >>> self.open_spreadsheet(None)
        """
        if self.campaign_editor:
            spreadsheet_url: str = "https://docs.google.com/spreadsheets/d/{}/edit".format(
                self.campaign_editor.spreadsheet_id
            )
            webbrowser.open(spreadsheet_url)
        else:
            print("Please initialize the campaign editor first.")

    def setup_callbacks(self) -> None:
        """Настраивает callbacks для widgets."""
        self.campaign_name_dropdown.observe(
            self.on_campaign_name_change, names="value"
        )
        self.category_name_dropdown.observe(self.on_category_change, names="value")
        self.language_dropdown.observe(self.on_language_change, names="value")
        self.initialize_button.on_click(self.initialize_campaign_editor)
        self.save_button.on_click(self.save_campaign)
        self.show_products_button.on_click(self.show_products)
        self.open_spreadsheet_button.on_click(self.open_spreadsheet)

    def display_widgets(self) -> None:
        """
        Отображает widgets для взаимодействия в Jupyter notebook.

        Инициализирует редактор кампании автоматически с первой выбранной кампанией.

        Raises:
            Exception: Если не удалось отобразить widgets.

        Example:
            >>> self.display_widgets()
        """
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