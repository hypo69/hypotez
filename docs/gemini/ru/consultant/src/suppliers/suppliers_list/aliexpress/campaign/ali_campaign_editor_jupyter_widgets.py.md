### **Анализ кода модуля `ali_campaign_editor_jupyter_widgets.py`**

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и разбит на классы и методы, что облегчает его понимание и поддержку.
    - Используются аннотации типов, что улучшает читаемость и помогает в отладке.
    - Присутствуют docstring для классов и методов, что облегчает понимание назначения кода.
    - Используется модуль `logger` для логирования ошибок и предупреждений.
- **Минусы**:
    - Не все docstring соответствуют требованиям, некоторые из них на английском языке.
    - Отсутствуют примеры использования в docstring для некоторых методов.
    - В некоторых местах отсутствует описание параметров в docstring.
    - Использованы старые конструкции типа `dict[str, str]`, которые нужно заменить на более современные.
    - Не везде используются одинарные кавычки.

## Рекомендации по улучшению:

1.  **Документация**:
    *   Перевести все docstring на русский язык.
    *   Добавить примеры использования в docstring для всех методов, где это возможно.
    *   Уточнить описания параметров и возвращаемых значений в docstring.
    *   Проверить и дополнить описания исключений, которые могут быть выброшены.
2.  **Форматирование**:
    *   Использовать одинарные кавычки (`'`) вместо двойных (`"`) для строк.
    *   Заменить старые конструкции типа `dict[str, str]` на более современные.
3.  **Логирование**:
    *   Проверить все места использования `logger` и убедиться, что передаются все необходимые параметры (сообщение, исключение, `exc_info`).
4.  **Общая структура**:
    *   Рассмотреть возможность использования dataclasses вместо SimpleNamespace для хранения данных.
    *   Убедиться, что все импорты необходимы и используются.
    *   Избавиться от закомментированного кода.
    *   Для класса `JupyterCampaignEditorWidgets` добавить пример использования в docstring модуля.
    *   Проверить, что все переменные класса имеют аннотацию типа.
5.  **Обработка исключений**:
    *   Уточнить тип исключения `Exception` в блоке `try...except`, чтобы обрабатывать только ожидаемые исключения.

## Оптимизированный код:

```python
## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor_jupyter_widgets.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с Jupyter widgets для редактора кампаний AliExpress
===================================================================

Модуль содержит класс :class:`JupyterCampaignEditorWidgets`, который предоставляет widgets
для взаимодействия с кампаниями AliExpress в Jupyter notebooks.

Пример использования:
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
from typing import List, Optional, Tuple, Dict

from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress.utils import locales
from src.utils.printer import pprint, get_directory_names
from src.logger.logger import logger


class JupyterCampaignEditorWidgets:
    """
    Widgets для редактора кампаний AliExpress.

    Этот класс предоставляет widgets для взаимодействия и управления кампаниями AliExpress,
    включая выбор кампаний, категорий и языков, а также выполнение действий, таких как
    инициализация редакторов, сохранение кампаний и отображение продуктов.

    Args:
        campaign_name (str): Название кампании.
        category_name (str): Название категории.
        language (str): Язык кампании.
        currency (str): Валюта кампании.
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

    def __init__(self):
        """
        Инициализирует widgets и настраивает редактор кампаний.

        Настраивает widgets для выбора кампаний, категорий и языков. Также устанавливает
        значения по умолчанию и обратные вызовы для widgets.

        Args:
            campaigns_directory (str): Путь к директории с кампаниями.
            campaign_name_dropdown (widgets.Dropdown): Выпадающий список с названиями кампаний.
            category_name_dropdown (widgets.Dropdown): Выпадающий список с названиями категорий.
            language_dropdown (widgets.Dropdown): Выпадающий список с языками и валютами.
            initialize_button (widgets.Button): Кнопка инициализации редактора кампаний.
            save_button (widgets.Button): Кнопка сохранения кампании.
            show_products_button (widgets.Button): Кнопка отображения продуктов.
            open_spreadsheet_button (widgets.Button): Кнопка открытия Google Spreadsheet.

        Raises:
            FileNotFoundError: Если директория с кампаниями не существует.

        """
        self.campaigns_directory: str = Path(
            gs.path.google_drive, 'aliexpress', 'campaigns'
        )

        if not self.campaigns_directory.exists():
            raise FileNotFoundError(
                f'Directory does not exist: {self.campaigns_directory}'
            )

        # self.languages = {"EN": "USD", "HE": "ILS", "RU": "ILS"}
        self.campaign_name_dropdown = widgets.Dropdown(
            options=get_directory_names(self.campaigns_directory),
            description='Campaign Name:',
        )
        self.category_name_dropdown = widgets.Dropdown(
            options=[], description='Category:'
        )
        self.language_dropdown = widgets.Dropdown(
            options=[
                f'{key} {value}'
                for locale in locales
                for key, value in locale.items()
            ],
            description='Language/Currency:',
        )
        self.initialize_button = widgets.Button(
            description='Initialize Campaign Editor',
            disabled=False,
        )
        self.save_button = widgets.Button(
            description='Save Campaign',
            disabled=False,
        )
        self.show_products_button = widgets.Button(
            description='Show Products',
            disabled=False,
        )
        self.open_spreadsheet_button = widgets.Button(
            description='Open Google Spreadsheet',
            disabled=False,
        )

        # Set up callbacks
        self.setup_callbacks()

        # Initialize with default values
        self.initialize_campaign_editor(None)

    def initialize_campaign_editor(self, _) -> None:
        """
        Инициализирует редактор кампаний.

        Args:
            _ (Any): Неиспользуемый аргумент, необходим для обратного вызова кнопки.

        Устанавливает редактор кампаний на основе выбранной кампании и категории.
        """

        self.campaign_name = self.campaign_name_dropdown.value or None
        self.category_name = self.category_name_dropdown.value or None

        self.language, self.currency = self.language_dropdown.value.split()
        if self.campaign_name:
            self.update_category_dropdown(self.campaign_name)
            self.campaign_editor = AliCampaignEditor(
                campaign_name=self.campaign_name,
                language=self.language,
                currency=self.currency,
            )

            if self.category_name:
                self.category = self.campaign_editor.get_category(
                    self.category_name
                )
                self.products = (
                    self.campaign_editor.get_category_products(
                        self.category_name
                    )
                )
        else:
            logger.warning(
                'Please select a campaign name before initializing the editor.'
            )

    # def get_directory_names(self, path: Path) -> list[str]:
    #     """Get directory names from the specified path.
    #
    #     Args:
    #         path (Path): Path to search for directories.
    #
    #     Returns:
    #         list[str]: List of directory names.
    #
    #     Example:
    #         >>> directories: list[str] = self.get_directory_names(Path("/some/dir"))
    #         >>> print(directories)
    #         ['dir1', 'dir2']
    #     """
    #     return [d.name for d in path.iterdir() if d.is_dir()]\

    def update_category_dropdown(self, campaign_name: str) -> None:
        """
        Обновляет выпадающий список категорий на основе выбранной кампании.

        Args:
            campaign_name (str): Название кампании.

        Example:
            >>> self.update_category_dropdown('SummerSale')
        """

        campaign_path = (
            self.campaigns_directory / campaign_name / 'category'
        )
        campaign_categories = get_directory_names(campaign_path)
        self.category_name_dropdown.options = campaign_categories

    def on_campaign_name_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке названий кампаний.

        Args:
            change (dict[str, str]): Словарь изменений, содержащий новое значение.

        Example:
            >>> self.on_campaign_name_change({'new': 'SummerSale'})
        """
        self.campaign_name = change['new']
        self.update_category_dropdown(self.campaign_name)
        self.initialize_campaign_editor(
            None
        )  # Reinitialize with newcampaign

    def on_category_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке категорий.

        Args:
            change (dict[str, str]): Словарь изменений, содержащий новое значение.

        Example:
            >>> self.on_category_change({'new': 'Electronics'})
        """
        self.category_name = change['new']
        self.initialize_campaign_editor(
            None
        )  # Reinitialize with new category

    def on_language_change(self, change: Dict[str, str]) -> None:
        """
        Обрабатывает изменения в выпадающем списке языков.

        Args:
            change (dict[str, str]): Словарь изменений, содержащий новое значение.

        Example:
            >>> self.on_language_change({'new': 'EN USD'})
        """
        self.language, self.currency = change['new'].split()
        self.initialize_campaign_editor(
            None
        )  # Reinitialize with new language/currency

    def save_campaign(self, _) -> None:
        """
        Сохраняет кампанию и ее категории.

        Args:
            _ (Any): Неиспользуемый аргумент, необходим для обратного вызова кнопки.

        Example:
            >>> self.save_campaign(None)
        """
        self.campaign_name = self.campaign_name_dropdown.value
        self.category_name = self.category_name_dropdown.value
        self.language, self.currency = self.language_dropdown.value.split()

        if self.campaign_name and self.language:
            self.campaign_editor = AliCampaignEditor(
                campaign_name=self.campaign_name,
                category_name=self.category_name
                if self.category_name
                else None,
                language=self.language,
            )
            try:
                self.campaign_editor.save_categories_from_worksheet()
            except Exception as ex:
                logger.error('Error saving campaign.', ex, exc_info=True)
        else:
            logger.warning(
                'Please select campaign name and language/currency before saving the campaign.'
            )

    def show_products(self, _) -> None:
        """
        Отображает продукты в выбранной категории.

        Args:
            _ (Any): Неиспользуемый аргумент, необходим для обратного вызова кнопки.

        Example:
            >>> self.show_products(None)
        """
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
            logger.error('Error displaying products.', ex, exc_info=True)

    def open_spreadsheet(self, _) -> None:
        """
        Открывает Google Spreadsheet в браузере.

        Args:
            _ (Any): Неиспользуемый аргумент, необходим для обратного вызова кнопки.

        Example:
            >>> self.open_spreadsheet(None)
        """
        if self.campaign_editor:
            spreadsheet_url = (
                f'https://docs.google.com/spreadsheets/d/{self.campaign_editor.spreadsheet_id}/edit'
            )
            webbrowser.open(spreadsheet_url)
        else:
            print('Please initialize the campaign editor first.')

    def setup_callbacks(self) -> None:
        """
        Настраивает обратные вызовы для widgets.
        """
        self.campaign_name_dropdown.observe(
            self.on_campaign_name_change, names='value'
        )
        self.category_name_dropdown.observe(
            self.on_category_change, names='value'
        )
        self.language_dropdown.observe(
            self.on_language_change, names='value'
        )
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