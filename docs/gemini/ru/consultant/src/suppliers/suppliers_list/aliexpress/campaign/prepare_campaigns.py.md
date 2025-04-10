### **Анализ кода модуля `prepare_campaigns`**

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структура модуля, наличие docstring для основных функций.
  - Использование `logger` для логирования.
  - Четкое разделение на функции для обработки кампаний, категорий и всего списка кампаний.
- **Минусы**:
  - Docstring написаны на английском языке, необходимо перевести на русский.
  - Не везде указаны типы для переменных внутри функций.
  - В docstring не указаны возможные исключения (Raises).
  - Отсутствуют примеры использования в docstring для некоторых функций.
  - Не все переменные внутри функций имеют аннотацию типов.
  - Строки требуется заключать в одинарные кавычки.

**Рекомендации по улучшению:**

1.  **Перевести docstring на русский язык**. Все описания функций, аргументов и возвращаемых значений должны быть на русском языке.
2.  **Добавить/уточнить типы переменных**. Указать типы для всех переменных, чтобы улучшить читаемость и предотвратить ошибки.
3.  **Указать возможные исключения (Raises)**. Добавить информацию о возможных исключениях, которые могут быть выброшены функциями.
4.  **Добавить примеры использования в docstring**. Примеры использования помогут понять, как правильно использовать функции.
5.  **Использовать одинарные кавычки**. Заменить двойные кавычки на одинарные.
6.  **Добавить аннотацию типов для всех переменных**

**Оптимизированный код:**

```python
## \file /src/suppliers/suppliers_list/aliexpress/campaign/prepare_campaigns.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для подготовки рекламных кампаний AliExpress.
=====================================================

Модуль обрабатывает категории, управляет данными кампаний и генерирует рекламные материалы.

Примеры:
--------
Чтобы запустить скрипт для конкретной кампании:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py summer_sale -c electronics -l EN -cu USD

Чтобы обработать все кампании:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py --all -l EN -cu USD
"""

import header
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


# Define the path to the directory with campaigns
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
        List[str]: Список наименований продуктов в категории.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        ['Product 1', 'Product 2']
    """
    return AliCampaignEditor(
        campaign_name=campaign_name, language=language, currency=currency
    ).process_campaign_category(category_name)


def process_campaign(
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    campaign_file: Optional[str] = None,
) -> bool:
    """
    Обрабатывает кампанию, включая её настройку и обработку.

    Args:
        campaign_name (str): Название рекламной кампании.
        language (Optional[str]): Язык для кампании. Если не указан, обрабатываются все локали.
        currency (Optional[str]): Валюта для кампании. Если не указана, обрабатываются все локали.
        campaign_file (Optional[str]): Необязательный путь к файлу кампании.

    Returns:
        bool: True, если кампания обработана успешно, иначе False.

    Example:
        >>> res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
    """

    # Преобразуем список словарей в список пар (language, currency)
    _l: List[tuple[str, str]] = [(lang, curr) for locale in locales for lang, curr in locale.items()]

    # Если указаны язык и валюта, фильтруем список по ним
    if language and currency:
        _l = [(language, currency)]

    # Обрабатываем каждую пару (language, currency)
    for language, currency in _l:
        logger.info(f'Processing campaign: {campaign_name=}, {language=}, {currency=}')
        editor: AliCampaignEditor = AliCampaignEditor(
            campaign_name=campaign_name,
            language=language,
            currency=currency,
        )

        editor.process_campaign()

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
        _l: List[tuple[str, str]] = [(language, currency)]
    pprint(f'{_l=}')
    for lang, curr in _l:
        campaigns_dir: List[str] = get_directory_names(campaigns_directory)
        pprint(f'{campaigns_dir=}')
        for campaign_name in campaigns_dir:
            logger.info(f'Start processing {campaign_name=}, {lang=}, {curr=}')
            editor: AliCampaignEditor = AliCampaignEditor(
                campaign_name=campaign_name,
                language=lang,
                currency=curr
            )
            editor.process_campaign()


def main_process(campaign_name: str, categories: List[str] | str, language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """
    Основная функция для обработки кампании.

    Args:
        campaign_name (str): Название рекламной кампании.
        categories (List[str] | str): Список категорий для кампании. Если пуст, обрабатывается вся кампания без категорий.
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
                logger.info(f'Processing specific category {category=}, {lang=}, {curr=}')
                process_campaign_category(campaign_name, category, lang, curr)
        else:
            # Process the entire campaign if no specific categories are provided
            logger.info(f'Processing entire campaign {campaign_name=}, {lang=}, {curr=}')
            process_campaign(campaign_name, lang, curr)


def main() -> None:
    """
    Основная функция для разбора аргументов командной строки и запуска обработки.

    Example:
        >>> main()
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Prepare AliExpress Campaign')
    parser.add_argument('campaign_name', type=str, help='Name of the campaign')
    parser.add_argument(
        '-c',
        '--categories',
        nargs='+',
        help='List of categories (if not provided, all categories will be used)',
    )
    parser.add_argument(
        '-l', '--language', type=str, default=None, help='Language for the campaign'
    )
    parser.add_argument(
        '-cu', '--currency', type=str, default=None, help='Currency for the campaign'
    )
    parser.add_argument('--all', action='store_true', help='Process all campaigns')

    args: argparse.Namespace = parser.parse_args()

    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        main_process(
            args.campaign_name, args.categories or [], args.language, args.currency
        )


if __name__ == '__main__':
    main()