### **Анализ кода модуля `prepare_campaigns.py`**

## \file /src/suppliers/aliexpress/campaign/prepare_campaigns.py

Модуль предназначен для подготовки кампаний AliExpress, включая обработку категорий, данных кампаний и генерацию рекламных материалов.

**Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие docstring для большинства функций.
    - Использование аннотаций типов.
    - Четкая структура основных функций `process_campaign_category`, `process_campaign`, `process_all_campaigns`, `main_process`, `main`.
    - Использование `logger` для логирования.
- **Минусы**:
    - Docstring написаны на английском языке, требуется перевод на русский.
    - Не все функции имеют подробные примеры использования в docstring.
    - Не хватает обработки исключений в некоторых функциях.
    - Не везде используется `j_loads_ns` для чтения конфигурационных файлов.
    - Не все переменные имеют аннотации типов.

**Рекомендации по улучшению**:

1.  **Перевод docstring на русский язык**: Необходимо перевести все docstring на русский язык, сохраняя формат UTF-8.
2.  **Добавление примеров использования**: Добавить примеры использования для каждой функции в docstring.
3.  **Обработка исключений**: Добавить обработку исключений в функциях, где это необходимо, с использованием `logger.error` для логирования ошибок.
4.  **Использование `j_loads_ns`**: Убедиться, что для чтения конфигурационных файлов используется `j_loads_ns`.
5.  **Аннотации типов**: Добавить аннотации типов для всех переменных, где это возможно.
6.  **Более конкретные комментарии**: Избегать общих фраз в комментариях, использовать более конкретные описания действий, которые выполняет код.
7.  **Удалить `# -*- coding: utf-8 -*-`**: Эта строка не нужна в Python 3.
8.  **Удалить `#! .pyenv/bin/python3`**: Эта строка указывает на использование виртуального окружения, но не является необходимой для работы кода.

**Оптимизированный код**:

```python
                ## \file /src/suppliers/aliexpress/campaign/prepare_campaigns.py
"""
Модуль для подготовки кампаний AliExpress
=================================================

Модуль `prepare_campaigns` предназначен для обработки категорий, управления данными кампаний и генерации рекламных материалов для AliExpress.

Пример использования
----------------------

Для запуска скрипта для конкретной кампании:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py summer_sale -c electronics -l EN -cu USD

Для обработки всех кампаний:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py --all -l EN -cu USD
"""

import argparse
import copy
from pathlib import Path
from typing import List, Optional

from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress.utils import locales
from src.utils.printer import pprint
from src.utils.file import get_directory_names
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger


# Определение пути к директории с кампаниями
campaigns_directory: Path = gs.path.google_drive / 'aliexpress' / 'campaigns'


def process_campaign_category(
    campaign_name: str, category_name: str, language: str, currency: str
) -> List[str]:
    """
    Обрабатывает конкретную категорию в рамках кампании для заданного языка и валюты.

    Args:
        campaign_name (str): Название рекламной кампании.
        category_name (str): Категория для кампании.
        language (str): Язык для кампании.
        currency (str): Валюта для кампании.

    Returns:
        List[str]: Список названий продуктов в рамках категории.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        ['Product 1', 'Product 2']
    """
    try:
        editor: AliCampaignEditor = AliCampaignEditor(
            campaign_name=campaign_name, language=language, currency=currency
        )
        return editor.process_campaign_category(category_name)
    except Exception as ex:
        logger.error(f'Ошибка при обработке категории кампании {category_name=}', ex, exc_info=True)
        return []


def process_campaign(
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    campaign_file: Optional[str] = None,
) -> bool:
    """
    Обрабатывает кампанию, настраивая и выполняя обработку кампании.

    Args:
        campaign_name (str): Название рекламной кампании.
        language (Optional[str]): Язык для кампании. Если не указан, обрабатываются все локали.
        currency (Optional[str]): Валюта для кампании. Если не указана, обрабатываются все локали.
        campaign_file (Optional[str]): Необязательный путь к конкретному файлу кампании.

    Returns:
        bool: True, если кампания обработана успешно, иначе False.

    Example:
        >>> res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
    """

    # Преобразуем список словарей в список пар (language, currency)
    _l: List[tuple[str, str]] = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    # pprint(_l)

    # Если указаны язык и валюта, фильтруем список по ним
    if language and currency:
        _l = [(language, currency)]

    # Обрабатываем каждую пару (language, currency)
    for language, currency in _l:
        logger.info(f"Processing campaign: {campaign_name=}, {language=}, {currency=}")
        editor: AliCampaignEditor = AliCampaignEditor(
            campaign_name=campaign_name,
            language=language,
            currency=currency,
        )

        try:
            editor.process_campaign()
        except Exception as ex:
            logger.error(f'Ошибка при обработке кампании {campaign_name=}, {language=}, {currency=}', ex, exc_info=True)
            return False

    return True  # Предполагаем, что кампания всегда успешно обрабатывается


def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """
    Обрабатывает все кампании в директории 'campaigns' для указанного языка и валюты.

    Args:
        language (Optional[str]): Язык для кампаний.
        currency (Optional[str]): Валюта для кампаний.

    Example:
        >>> process_all_campaigns("EN", "USD")
    """
    if not language and not currency:
        # Process all locales if language or currency is not provided
        _l: List[tuple[str, str]] = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    else:
        _l = [(language, currency)]
    pprint(f"{_l=}")
    for lang, curr in _l:
        campaigns_dir: List[str] = get_directory_names(campaigns_directory)
        pprint(f"{campaigns_dir=}")
        for campaign_name in campaigns_dir:
            logger.info(f"Start processing {campaign_name=}, {lang=}, {curr=}")
            try:
                editor: AliCampaignEditor = AliCampaignEditor(
                    campaign_name=campaign_name,
                    language=lang,
                    currency=curr
                )
                editor.process_campaign()
            except Exception as ex:
                logger.error(f'Ошибка при обработке всех кампаний {campaign_name=}, {lang=}, {curr=}', ex, exc_info=True)


def main_process(campaign_name: str, categories: List[str] | str, language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """
    Основная функция для обработки кампании.

    Args:
        campaign_name (str): Название рекламной кампании.
        categories (List[str] | str): Список категорий для кампании. Если пуст, обрабатывается вся кампания без конкретных категорий.
        language (Optional[str]): Язык для кампании.
        currency (Optional[str]): Валюта для кампании.

    Example:
        >>> main_process("summer_sale", ["electronics"], "EN", "USD")
        >>> main_process("summer_sale", [], "EN", "USD")
    """
    # Determine locales based on provided language and currency
    locales_to_process: List[tuple[str, str]] = [(language, currency)] if language and currency else [(lang, curr) for locale in locales for lang, curr in locale.items()]

    for lang, curr in locales_to_process:
        if categories:
            # Process each specified category
            for category in categories:
                logger.info(f"Processing specific category {category=}, {lang=}, {curr=}")
                process_campaign_category(campaign_name, category, lang, curr)
        else:
            # Process the entire campaign if no specific categories are provided
            logger.info(f"Processing entire campaign {campaign_name=}, {lang=}, {curr=}")
            process_campaign(campaign_name, lang, curr)


def main() -> None:
    """
    Основная функция для разбора аргументов командной строки и инициации обработки.

    Example:
        >>> main()
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Prepare AliExpress Campaign")
    parser.add_argument("campaign_name", type=str, help="Name of the campaign")
    parser.add_argument(
        "-c",
        "--categories",
        nargs="+",
        help="List of categories (if not provided, all categories will be used)",
    )
    parser.add_argument(
        "-l", "--language", type=str, default=None, help="Language for the campaign"
    )
    parser.add_argument(
        "-cu", "--currency", type=str, default=None, help="Currency for the campaign"
    )
    parser.add_argument("--all", action="store_true", help="Process all campaigns")

    args: argparse.Namespace = parser.parse_args()

    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        main_process(
            args.campaign_name, args.categories or [], args.language, args.currency
        )


if __name__ == "__main__":
    main()