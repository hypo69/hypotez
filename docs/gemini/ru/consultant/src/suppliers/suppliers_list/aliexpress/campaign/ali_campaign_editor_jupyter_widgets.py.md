### Анализ кода модуля `ali_campaign_editor_jupyter_widgets.py`

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая организация кода в классы и методы.
  - Использование аннотаций типов.
  - Четкое разделение ответственности между методами.
  - Использование `logger` для логирования ошибок и предупреждений.
- **Минусы**:
  - Местами отсутствует документация.
  - Не все переменные класса аннотированы в начале класса.
  - В docstring есть английский язык, надо перевести.
  - Не все docstring соответствуют принятому стандарту оформления.

**Рекомендации по улучшению:**

1.  **Документация**:
    - Дополнить документацию для всех методов и классов, используя принятый формат.
    - Перевести все docstring на русский язык.
    - Добавить примеры использования в docstring, где это уместно.

2.  **Аннотации**:
    - Добавить аннотации типов для всех переменных класса в начале класса.

3.  **Комментарии**:
    - Уточнить комментарии, чтобы они были более информативными и соответствовали стилю, принятому в проекте.
    - Избегать общих фраз вроде "получаем", "делаем", заменяя их на более конкретные, например, "извлекаем", "проверяем", "выполняем".

4.  **Исключения**:
    - Убедиться, что все исключения обрабатываются с использованием `logger.error` и передачей информации об ошибке (`ex`, `exc_info=True`).

5.  **Общая структура**:
    - Убедиться, что все функции и методы имеют docstring, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor_jupyter_widgets.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль содержит Jupyter widgets для редактора кампаний AliExpress.
==================================================================

Этот модуль предоставляет widgets для управления кампаниями AliExpress в Jupyter notebooks.

Testfile:
    file test_ali_campaign_editor_jupyter_widgets.py

"""

from types import SimpleNamespace
import header
from pathlib import Path
from ipywidgets import widgets
from IPython.display import display
import webbrowser

from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress.utils import locales
from src.utils.printer import pprint, get_directory_names
from src.logger.logger import logger


class JupyterCampaignEditorWidgets:
    """
    Виджеты для редактора кампаний AliExpress.

    Этот класс предоставляет виджеты для взаимодействия и управления кампаниями AliExpress,
    включая выбор кампаний, категорий и языков, а также выполнение таких действий, как
    инициализация редакторов, сохранение кампаний и отображение товаров.

    Example:
        >>> editor_widgets: JupyterCampaignEditorWidgets = JupyterCampaignEditorWidgets()
        >>> editor_widgets.display_widgets()
    """

    # Объявление атрибутов класса
    language: str = None
    currency: str = None
    campaign_name: str = None
    category_name: str = None
    category: SimpleNamespace = None
    campaign_editor: AliCampaignEditor = None
    products: list[SimpleNamespace] = None

    def __init__(self) -> None:
        """
        Инициализация виджетов и настройка редактора кампаний.

        Настраивает виджеты для выбора кампаний, категорий и языков. Также устанавливает
        значения по умолчанию и обратные вызовы для виджетов.
        """
        self.campaigns_directory: str = Path(
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
                f"{key} {value}"
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

        # Настройка обратных вызовов
        self.setup_callbacks()

        # Инициализация со значениями по умолчанию
        self.initialize_campaign_editor(None)

    def initialize_campaign_editor(self, _) -> None:
        """
        Инициализация редактора кампаний.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для обратного вызова кнопки.

        Настраивает редактор кампаний на основе выбранной кампании и категории.
        """
        self.campaign_name: str = self.campaign_name_dropdown.value or None
        self.category_name: str = self.category_name_dropdown.value or None

        self.language, self.currency = self.language_dropdown.value.split()
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
                self.products: list[
                    SimpleNamespace
                ] = self.campaign_editor.get_category_products(self.category_name)
        else:
            logger.warning(
                "Please select a campaign name before initializing the editor."
            )

    def update_category_dropdown(self, campaign_name: str) -> None:
        """
        Обновление выпадающего списка категорий на основе выбранной кампании.

        Args:
            campaign_name (str): Название кампании.
        """
        campaign_path: Path = (
            self.campaigns_directory / campaign_name / "category"
        )
        campaign_categories: list[str] = get_directory_names(campaign_path)
        self.category_name_dropdown.options = campaign_categories

    def on_campaign_name_change(self, change: dict[str, str]) -> None:
        """
        Обработка изменений в выпадающем списке названий кампаний.

        Args:
            change (dict[str, str]): Словарь изменений, содержащий новое значение.
        """
        self.campaign_name: str = change["new"]
        self.update_category_dropdown(self.campaign_name)
        self.initialize_campaign_editor(
            None
        )  # Повторная инициализация с новой кампанией

    def on_category_change(self, change: dict[str, str]) -> None:
        """
        Обработка изменений в выпадающем списке категорий.

        Args:
            change (dict[str, str]): Словарь изменений, содержащий новое значение.
        """
        self.category_name: str = change["new"]
        self.initialize_campaign_editor(
            None
        )  # Повторная инициализация с новой категорией

    def on_language_change(self, change: dict[str, str]) -> None:
        """
        Обработка изменений в выпадающем списке языков.

        Args:
            change (dict[str, str]): Словарь изменений, содержащий новое значение.
        """
        self.language, self.currency = change["new"].split()
        self.initialize_campaign_editor(
            None
        )  # Повторная инициализация с новым языком/валютой

    def save_campaign(self, _) -> None:
        """
        Сохранение кампании и ее категорий.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для обратного вызова кнопки.
        """
        self.campaign_name: str = self.campaign_name_dropdown.value
        self.category_name: str = self.category_name_dropdown.value
        self.language, self.currency = self.language_dropdown.value.split()

        if self.campaign_name and self.language:
            self.campaign_editor: AliCampaignEditor = AliCampaignEditor(
                campaign_name=self.campaign_name,
                category_name=(
                    self.category_name if self.category_name else None
                ),
                language=self.language,
            )
            try:
                self.campaign_editor.save_categories_from_worksheet()
            except Exception as ex:
                logger.error("Ошибка при сохранении кампании.", ex, True)
        else:
            logger.warning(
                "Пожалуйста, выберите название кампании и язык/валюту перед сохранением кампании."
            )

    def show_products(self, _) -> None:
        """
        Отображение товаров в выбранной категории.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для обратного вызова кнопки.
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
            logger.error("Ошибка при отображении товаров.", ex, True)

    def open_spreadsheet(self, _) -> None:
        """
        Открытие Google Spreadsheet в браузере.

        Args:
            _ (Any): Неиспользуемый аргумент, необходимый для обратного вызова кнопки.
        """
        if self.campaign_editor:
            spreadsheet_url: str = (
                f"https://docs.google.com/spreadsheets/d/{self.campaign_editor.spreadsheet_id}/edit"
            )
            webbrowser.open(spreadsheet_url)
        else:
            print("Please initialize the campaign editor first.")

    def setup_callbacks(self) -> None:
        """Настройка обратных вызовов для виджетов."""
        self.campaign_name_dropdown.observe(
            self.on_campaign_name_change, names="value"
        )
        self.category_name_dropdown.observe(
            self.on_category_change, names="value"
        )
        self.language_dropdown.observe(
            self.on_language_change, names="value"
        )
        self.initialize_button.on_click(self.initialize_campaign_editor)
        self.save_button.on_click(self.save_campaign)
        self.show_products_button.on_click(self.show_products)
        self.open_spreadsheet_button.on_click(self.open_spreadsheet)

    def display_widgets(self) -> None:
        """
        Отображение виджетов для взаимодействия в Jupyter notebook.

        Инициализирует редактор кампаний автоматически с первой выбранной кампанией.
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
        # Инициализация редактора кампаний с первой выбранной кампанией
        self.initialize_campaign_editor(None)