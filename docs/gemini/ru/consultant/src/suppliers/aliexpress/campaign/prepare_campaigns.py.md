### **Анализ кода модуля `prepare_campaigns.py`**

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на отдельные функции, что облегчает его понимание и поддержку.
  - Используются аннотации типов, что улучшает читаемость кода и помогает в отладке.
  - Присутствуют docstring для функций, описывающие их назначение, аргументы и возвращаемые значения.
  - Используется модуль `logger` для логирования.
- **Минусы**:
  - Docstring написаны на английском языке.
  - Не все функции имеют примеры использования в docstring.
  - В некоторых местах можно улучшить форматирование кода для соответствия PEP8.
  - Отсутствует обработка исключений.
  - В начале файла указана кодировка `# -*- coding: utf-8 -*-`, что может быть избыточно, так как UTF-8 является кодировкой по умолчанию для Python 3.
  - В коде используется конструкция `List[str] | str`, что не соответствует указаниям использовать `|` вместо `Union`.
  - Отсутствует обработка ошибок при работе с файлами и директориями.
  - Не везде используется `logger.error` для логирования ошибок с передачей информации об исключении.

## Рекомендации по улучшению:

- Перевести все docstring на русский язык.
- Добавить примеры использования в docstring для всех функций.
- Улучшить форматирование кода в соответствии с PEP8 (например, добавить пробелы вокруг операторов).
- Добавить обработку исключений для предотвращения неожиданного завершения программы.
- Использовать `logger.error` для логирования ошибок с передачей информации об исключении.
- Заменить конструкцию `List[str] | str` на `str | list[str]`.
- Добавить проверку на существование директорий и файлов перед их обработкой.
- Добавить более подробные комментарии для сложных участков кода.
- Использовать `j_loads` или `j_loads_ns` для чтения конфигурационных файлов, если это необходимо.
- В функции `process_campaign` можно добавить обработку исключений, чтобы логировать ошибки при обработке кампании.
- В функции `process_all_campaigns` можно добавить проверку на существование директории с кампаниями, чтобы избежать ошибок, если директория не существует.
- В функции `main_process` можно добавить обработку исключений, чтобы логировать ошибки при обработке категорий или кампании.

## Оптимизированный код:

```python
## \file /src/suppliers/aliexpress/campaign/prepare_campaigns.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для подготовки кампаний AliExpress
==========================================

Модуль предназначен для подготовки кампаний AliExpress путем обработки категорий,
управления данными кампании и генерации рекламных материалов.

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
from src.suppliers.aliexpress.campaign import AliCampaignEditor
from src.suppliers.aliexpress.utils import locales
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
        List[str]: Список названий продуктов в категории.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        ['Product 1', 'Product 2']
    """
    try:
        return AliCampaignEditor(
            campaign_name=campaign_name, language=language, currency=currency
        ).process_campaign_category(category_name)
    except Exception as ex:
        logger.error(
            f'Ошибка при обработке категории {category_name} в кампании {campaign_name}',
            ex,
            exc_info=True,
        )
        return []


def process_campaign(
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    campaign_file: Optional[str] = None,
) -> bool:
    """
    Обрабатывает кампанию, включая настройку и обработку данных кампании.

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
    _l: list[tuple[str, str]] = [
        (lang, curr) for locale in locales for lang, curr in locale.items()
    ]

    # Если указаны язык и валюта, фильтруем список по ним
    if language and currency:
        _l = [(language, currency)]

    # Обрабатываем каждую пару (language, currency)
    for language, currency in _l:
        logger.info(
            f'Обработка кампании: {campaign_name=}, {language=}, {currency=}'
        )
        try:
            editor = AliCampaignEditor(
                campaign_name=campaign_name, language=language, currency=currency
            )
            editor.process_campaign()
        except Exception as ex:
            logger.error(
                f'Ошибка при обработке кампании {campaign_name} для языка {language} и валюты {currency}',
                ex,
                exc_info=True,
            )
            return False

    return True  # Предполагаем, что кампания всегда успешно обрабатывается


def process_all_campaigns(
    language: Optional[str] = None, currency: Optional[str] = None
) -> None:
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
        _l: list[tuple[str, str]] = [
            (lang, curr) for locale in locales for lang, curr in locale.items()
        ]
    else:
        _l = [(language, currency)]
    pprint(f'{_l=}')
    for lang, curr in _l:
        try:
            campaigns_dir = get_directory_names(campaigns_directory)
            pprint(f'{campaigns_dir=}')
            for campaign_name in campaigns_dir:
                logger.info(
                    f'Начало обработки {campaign_name=}, {lang=}, {curr=}'
                )
                try:
                    editor = AliCampaignEditor(
                        campaign_name=campaign_name, language=lang, currency=curr
                    )
                    editor.process_campaign()
                except Exception as ex:
                    logger.error(
                        f'Ошибка при обработке кампании {campaign_name} для языка {lang} и валюты {curr}',
                        ex,
                        exc_info=True,
                    )
        except Exception as ex:
            logger.error(
                'Ошибка при получении списка директорий кампаний', ex, exc_info=True
            )


def main_process(
    campaign_name: str,
    categories: str | list[str],
    language: Optional[str] = None,
    currency: Optional[str] = None,
) -> None:
    """
    Основная функция для обработки кампании.

    Args:
        campaign_name (str): Название рекламной кампании.
        categories (str | list[str]): Список категорий для кампании. Если пуст, обрабатывается вся кампания без учета категорий.
        language (Optional[str]): Язык для кампании.
        currency (Optional[str]): Валюта для кампании.

    Example:
        >>> main_process("summer_sale", ["electronics"], "EN", "USD")
        >>> main_process("summer_sale", [], "EN", "USD")
    """
    # Determine locales based on provided language and currency
    locales_to_process: list[tuple[str, str]] = (
        [(language, currency)]
        if language and currency
        else [(lang, curr) for locale in locales for lang, curr in locale.items()]
    )

    for lang, curr in locales_to_process:
        if categories:
            # Process each specified category
            for category in categories:
                logger.info(
                    f'Обработка конкретной категории {category=}, {lang=}, {curr=}'
                )
                process_campaign_category(campaign_name, category, lang, curr)
        else:
            # Process the entire campaign if no specific categories are provided
            logger.info(
                f'Обработка всей кампании {campaign_name=}, {lang=}, {curr=}'
            )
            process_campaign(campaign_name, lang, curr)


def main() -> None:
    """
    Основная функция для разбора аргументов командной строки и запуска обработки.

    Example:
        >>> main()
    """
    parser = argparse.ArgumentParser(description='Prepare AliExpress Campaign')
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

    args = parser.parse_args()

    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        main_process(
            args.campaign_name, args.categories or [], args.language, args.currency
        )


if __name__ == '__main__':
    main()