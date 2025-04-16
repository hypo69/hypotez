### **Анализ кода модуля `ali_campaign_editor_jupyter_widgets.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на логические блоки.
  - Присутствуют docstring для классов и методов.
  - Используются аннотации типов.
  - Код соответствует основным принципам SOLID.
- **Минусы**:
  - Не все docstring соответствуют требуемому формату.
  - В некоторых местах отсутствуют пробелы вокруг операторов присваивания.
  - Есть закомментированный код.
  - Не везде используется `logger` для логирования ошибок.

#### **Рекомендации по улучшению**:
- Переработать docstring в соответствии с заданным форматом.
- Убрать закомментированный код.
- Добавить обработку исключений и логирование с использованием `logger` там, где это необходимо.
- Добавить пробелы вокруг операторов присваивания.
- Добавить docstring для внутренних функций.
- Заменить множественные `print()` на `logger.info()`
- Все переменные должны быть аннотированы типами

#### **Оптимизированный код**:

```python
## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor_jupyter_widgets.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для создания Jupyter widgets для редактора кампаний AliExpress
====================================================================

Этот модуль содержит widgets для управления кампаниями AliExpress в Jupyter notebooks.

Testfile:
    file test_ali_campaign_editor_jupyter_widgets.py
"""

from types import SimpleNamespace
import header
from pathlib import Path
from ipywidgets import widgets
from IPython.display import display
import webbrowser
from typing import Optional, List, Dict, Tuple

from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress.utils import locales
from src.utils.printer import pprint, get_directory_names
from src.logger.logger import logger


class JupyterCampaignEditorWidgets:
    """
    Widgets для редактора кампаний AliExpress.

    Этот класс предоставляет widgets для взаимодействия и управления кампаниями AliExpress,
    включая выбор кампаний, категорий и языков, а также выполнение таких действий, как
    инициализация редакторов, сохранение кампаний и отображение продуктов.

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
    products: list[SimpleNamespace] = None

    def __init__(self) -> None:
        """
        Инициализирует widgets и настраивает редактор кампаний.

        Настраивает widgets для выбора кампаний, категорий и языков. Также устанавливает
        значения по умолчанию и обратные вызовы для widgets.
        """
        self.campaigns_directory: Path = Path(
            gs.path.google_drive, "aliexpress", "campaigns"
        )

        if not self.campaigns_directory.exists():
            raise FileNotFoundError(
                f"Directory does not exist: {self.campaigns_directory}"
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
                f"{key} {value}" for locale in locales for key, value in locale.items()
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

    def initialize_campaign_editor(self, _: Optional[widgets.Button] = None) -> None:
        """
        Инициализирует редактор кампаний.

        Args:
            _ (Optional[widgets.Button], optional): Неиспользуемый аргумент, необходим для обратного вызова кнопки. Defaults to None.

        Устанавливает редактор кампаний на основе выбранной кампании и категории.
        """

        self.campaign_name: Optional[str] = self.campaign_name_dropdown.value or None
        self.category_name: Optional[str] = self.category_name_dropdown.value or None

        if self.language_dropdown.value:
            self.language, self.currency = self.language_dropdown.value.split()
        else:
            self.language, self.currency = None, None

        if self.campaign_name:
            self.update_category_dropdown(self.campaign_name)
            self.campaign_editor: Optional[AliCampaignEditor] = AliCampaignEditor(
                campaign_name=self.campaign_name,
                language=self.language,
                currency=self.currency,
            )

            if self.category_name:
                self.category: SimpleNamespace = (
                    self.campaign_editor.get_category(self.category_name)
                    if self.campaign_editor
                    else None
                )
                self.products: list[SimpleNamespace] = (
                    self.campaign_editor.get_category_products(self.category_name)
                    if self.campaign_editor
                    else None
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

        Example:
            >>> self.update_category_dropdown("SummerSale")
        """

        campaign_path: Path = self.campaigns_directory / campaign_name / "category"
        campaign_categories: list[str] = get_directory_names(campaign_path)
        self.category_name_dropdown.options = campaign_categories

    def on_campaign_name_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке названий кампаний.

        Args:
            change (Dict[str, str]): Словарь изменений, содержащий новое значение.

        Example:
            >>> self.on_campaign_name_change({'new': 'SummerSale'})
        """
        self.campaign_name: str = change["new"]
        self.update_category_dropdown(self.campaign_name)
        self.initialize_campaign_editor(
            None
        )  # Reinitialize with newcampaign. TODO: Check if that is necessary

    def on_category_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке категорий.

        Args:
            change (Dict[str, str]): Словарь изменений, содержащий новое значение.

        Example:
            >>> self.on_category_change({'new': 'Electronics'})
        """
        self.category_name: str = change["new"]
        self.initialize_campaign_editor(
            None
        )  # Reinitialize with new category. TODO: Check if that is necessary

    def on_language_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке языков.

        Args:
            change (Dict[str, str]): Словарь изменений, содержащий новое значение.

        Example:
            >>> self.on_language_change({'new': 'EN USD'})
        """
        if change["new"]:
            self.language, self.currency = change["new"].split()
        else:
            self.language, self.currency = None, None
        self.initialize_campaign_editor(
            None
        )  # Reinitialize with new language/currency. TODO: Check if that is necessary

    def save_campaign(self, _: Optional[widgets.Button] = None) -> None:
        """
        Сохраняет кампанию и ее категории.

        Args:
            _ (Optional[widgets.Button], optional): Неиспользуемый аргумент, необходим для обратного вызова кнопки. Defaults to None.

        Example:
            >>> self.save_campaign(None)
        """
        self.campaign_name: str = self.campaign_name_dropdown.value
        self.category_name: str = self.category_name_dropdown.value
        if self.language_dropdown.value:
            self.language, self.currency = self.language_dropdown.value.split()
        else:
            self.language, self.currency = None, None

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

    def show_products(self, _: Optional[widgets.Button] = None) -> None:
        """
        Отображает продукты в выбранной категории.

        Args:
            _ (Optional[widgets.Button], optional): Неиспользуемый аргумент, необходим для обратного вызова кнопки. Defaults to None.

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

    def open_spreadsheet(self, _: Optional[widgets.Button] = None) -> None:
        """
        Открывает Google Spreadsheet в браузере.

        Args:
            _ (Optional[widgets.Button], optional): Неиспользуемый аргумент, необходим для обратного вызова кнопки. Defaults to None.

        Example:
            >>> self.open_spreadsheet(None)
        """
        if self.campaign_editor:
            spreadsheet_url: str = (
                f"https://docs.google.com/spreadsheets/d/{self.campaign_editor.spreadsheet_id}/edit"
            )
            webbrowser.open(spreadsheet_url)
        else:
            logger.info("Please initialize the campaign editor first.")

    def setup_callbacks(self) -> None:
        """Настраивает обратные вызовы для widgets."""
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

        Инициализирует редактор кампаний автоматически с первой выбранной кампанией.

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