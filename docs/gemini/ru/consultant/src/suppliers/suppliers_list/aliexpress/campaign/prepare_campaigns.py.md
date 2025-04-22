### **Анализ кода модуля `prepare_campaigns.py`**

## \file /src/suppliers/suppliers_list/aliexpress/campaign/prepare_campaigns.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для подготовки рекламных кампаний AliExpress, обрабатывая категории, данные кампаний и генерируя рекламные материалы
=======================================================================================================================

Модуль :mod:`src.suppliers.suppliers_list.aliexpress.campaign` предназначен для автоматизации процесса подготовки рекламных кампаний на AliExpress. Он включает в себя функции для обработки категорий товаров, настройки параметров кампаний (язык, валюта) и создания необходимых рекламных материалов.

Примеры использования
----------------------

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
campaigns_directory = gs.path.google_drive / 'aliexpress' / 'campaigns'


def process_campaign_category(
    campaign_name: str, category_name: str, language: str, currency: str
) -> List[str]:
    """Функция обрабатывает определенную категорию в рамках кампании для заданного языка и валюты.

    Args:
        campaign_name (str): Название рекламной кампании.
        category_name (str): Категория для кампании.
        language (str): Язык для кампании.
        currency (str): Валюта для кампании.

    Returns:
        List[str]: Список наименований товаров в рамках категории.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        ['Product 1', 'Product 2']
    """
    # Создание экземпляра класса AliCampaignEditor и вызов метода process_campaign_category для обработки категории кампании
    return AliCampaignEditor(
        campaign_name=campaign_name, language=language, currency=currency
    ).process_campaign_category(category_name)


def process_campaign(
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    campaign_file: Optional[str] = None,
) -> bool:
    """Функция обрабатывает кампанию, настраивая и обрабатывая её.

    Args:
        campaign_name (str): Название рекламной кампании.
        language (Optional[str]): Язык для кампании. Если не указан, обрабатываются все локали.
        currency (Optional[str]): Валюта для кампании. Если не указана, обрабатываются все локали.
        campaign_file (Optional[str]): Необязательный путь к файлу конкретной кампании.

    Returns:
        bool: True, если кампания обработана, иначе False.
    """
    # Преобразуем список словарей в список пар (language, currency)
    _l = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    # pprint(_l)
    
    # Если указаны язык и валюта, фильтруем список по ним
    if language and currency:
        _l = [(language, currency)]

    # Обрабатываем каждую пару (language, currency)
    for language, currency in _l:
        logger.info(f"Processing campaign: {campaign_name=}, {language=}, {currency=}")
        editor = AliCampaignEditor(
            campaign_name=campaign_name,
            language=language,
            currency=currency,
        )
        
        editor.process_campaign()

    # Предполагаем, что кампания всегда успешно обрабатывается
    return True


def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Функция обрабатывает все кампании в каталоге 'campaigns' для указанного языка и валюты.

    Args:
        language (Optional[str]): Язык для кампаний.
        currency (Optional[str]): Валюта для кампаний.
    """
    if not language and not currency:
        # Обрабатываем все локали, если язык или валюта не указаны
        _l = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    else:
        _l = [(language, currency)]
    pprint(f"{_l=}")
    for lang, curr in _l:
        campaigns_dir = get_directory_names(campaigns_directory)
        pprint(f"{campaigns_dir=}")
        for campaign_name in campaigns_dir:
            logger.info(f"Start processing {campaign_name=}, {lang=}, {curr=}")
            editor = AliCampaignEditor(
                campaign_name=campaign_name,
                language=lang,
                currency=curr
            )
            # Запускаем процесс обработки кампании
            editor.process_campaign()


def main_process(campaign_name: str, categories: List[str] | str, language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Основная функция для обработки кампании.

    Args:
        campaign_name (str): Название рекламной кампании.
        categories (List[str] | str): Список категорий для кампании. Если пуст, обрабатывается вся кампания без конкретных категорий.
        language (Optional[str]): Язык для кампании.
        currency (Optional[str]): Валюта для кампании.
    """
    # Определяем локали для обработки на основе предоставленных языка и валюты
    locales_to_process = [(language, currency)] if language and currency else [(lang, curr) for locale in locales for lang, curr in locale.items()]

    # Итерируемся по локалям для обработки
    for lang, curr in locales_to_process:
        if categories:
            # Обрабатываем каждую указанную категорию
            for category in categories:
                logger.info(f"Processing specific category {category=}, {lang=}, {curr=}")
                process_campaign_category(campaign_name, category, lang, curr)
        else:
            # Обрабатываем всю кампанию, если не указаны конкретные категории
            logger.info(f"Processing entire campaign {campaign_name=}, {lang=}, {curr=}")
            process_campaign(campaign_name, lang, curr)


def main() -> None:
    """Основная функция для разбора аргументов и запуска обработки."""
    parser = argparse.ArgumentParser(description="Prepare AliExpress Campaign")
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

    # Разбираем аргументы командной строки
    args = parser.parse_args()

    # Если указан флаг --all, обрабатываем все кампании
    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        # Иначе обрабатываем указанную кампанию с заданными параметрами
        main_process(
            args.campaign_name, args.categories or [], args.language, args.currency
        )

# Запускаем основную функцию, если скрипт запущен напрямую
if __name__ == "__main__":
    main()
```

## Качество кода:

- **Соответствие стандартам**: 8/10
- **Плюсы**:
    - Код хорошо структурирован и читаем.
    - Присутствуют docstring для большинства функций, что облегчает понимание их назначения и использования.
    - Используется модуль `logger` для логирования, что помогает в отслеживании работы скрипта.
    - Присутствуют аннотации типов.
- **Минусы**:
    - Некоторые docstring отсутствуют или не полные.
    - Не все функции имеют примеры использования в docstring.
    - Не везде есть подробные коментарии, предшествующие блоку кода

## Рекомендации по улучшению:

1. **Дополнить Docstring**:
   - Добавить примеры использования для всех функций, где они отсутствуют.
   - Улучшить описания аргументов и возвращаемых значений, чтобы они были более понятными и информативными.

2. **Добавить комментарии к коду**:
   - Добавить подробные коментарии, предшествующие блоку кода.
   - Убедиться, что все функции и классы имеют docstring, соответствующие стандарту.

3. **Улучшить обработку ошибок**:
   - Добавить обработку исключений в функции `process_campaign_category`, `process_campaign` и `process_all_campaigns` для более надежной работы скрипта.
   - Логировать ошибки с использованием `logger.error` с указанием типа исключения и дополнительной информацией.

4. **Согласованность в коде**:
   - Проверить и исправить все места, где используются разные стили форматирования.

5. **Улучшить читаемость кода**:
   - Добавить больше комментариев для сложных участков кода, чтобы облегчить понимание логики работы.

## Оптимизированный код:

```python
## \file /src/suppliers/aliexpress/campaign/prepare_campaigns.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для подготовки рекламных кампаний AliExpress, обрабатывая категории, данные кампаний и генерируя рекламные материалы
=======================================================================================================================

Модуль :mod:`src.suppliers.suppliers_list.aliexpress.campaign` предназначен для автоматизации процесса подготовки рекламных кампаний на AliExpress. Он включает в себя функции для обработки категорий товаров, настройки параметров кампаний (язык, валюта) и создания необходимых рекламных материалов.

Примеры использования
----------------------

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
campaigns_directory = gs.path.google_drive / 'aliexpress' / 'campaigns'


def process_campaign_category(
    campaign_name: str, category_name: str, language: str, currency: str
) -> List[str]:
    """Функция обрабатывает определенную категорию в рамках кампании для заданного языка и валюты.

    Args:
        campaign_name (str): Название рекламной кампании.
        category_name (str): Категория для кампании.
        language (str): Язык для кампании.
        currency (str): Валюта для кампании.

    Returns:
        List[str]: Список наименований товаров в рамках категории.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        ['Product 1', 'Product 2']
    """
    # Создание экземпляра класса AliCampaignEditor и вызов метода process_campaign_category для обработки категории кампании
    try:
        editor = AliCampaignEditor(
            campaign_name=campaign_name, language=language, currency=currency
        )
        # Функция возвращает список заголовков товаров из указанной категории
        return editor.process_campaign_category(category_name)
    except Exception as ex:
        # Логируем ошибку, если что-то пошло не так в процессе обработки категории кампании
        logger.error(f"Error processing category {category_name} in campaign {campaign_name}", ex, exc_info=True)
        return []


def process_campaign(
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    campaign_file: Optional[str] = None,
) -> bool:
    """Функция обрабатывает кампанию, настраивая и обрабатывая её.

    Args:
        campaign_name (str): Название рекламной кампании.
        language (Optional[str]): Язык для кампании. Если не указан, обрабатываются все локали.
        currency (Optional[str]): Валюта для кампании. Если не указана, обрабатываются все локали.
        campaign_file (Optional[str]): Необязательный путь к файлу конкретной кампании.

    Returns:
        bool: True, если кампания обработана, иначе False.
    """
    # Преобразуем список словарей в список пар (language, currency)
    _l = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    # pprint(_l)
    
    # Если указаны язык и валюта, фильтруем список по ним
    if language and currency:
        _l = [(language, currency)]

    # Обрабатываем каждую пару (language, currency)
    for language, currency in _l:
        logger.info(f"Processing campaign: {campaign_name=}, {language=}, {currency=}")
        try:
            editor = AliCampaignEditor(
                campaign_name=campaign_name,
                language=language,
                currency=currency,
            )
            # Запускаем процесс обработки кампании
            editor.process_campaign()
        except Exception as ex:
            # Логируем ошибку, если что-то пошло не так в процессе обработки кампании
            logger.error(f"Error processing campaign {campaign_name} for {language=}, {currency=}", ex, exc_info=True)
            return False

    # Предполагаем, что кампания всегда успешно обрабатывается
    return True


def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Функция обрабатывает все кампании в каталоге 'campaigns' для указанного языка и валюты.

    Args:
        language (Optional[str]): Язык для кампаний.
        currency (Optional[str]): Валюта для кампаний.
    """
    # Обрабатываем все локали, если язык или валюта не указаны
    if not language and not currency:
        _l = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    # Если указаны язык и валюта, используем их
    else:
        _l = [(language, currency)]
    pprint(f"{_l=}")
    # Итерируемся по каждой паре язык-валюта
    for lang, curr in _l:
        campaigns_dir = get_directory_names(campaigns_directory)
        pprint(f"{campaigns_dir=}")
        # Итерируемся по каждой кампании в директории
        for campaign_name in campaigns_dir:
            logger.info(f"Start processing {campaign_name=}, {lang=}, {curr=}")
            try:
                editor = AliCampaignEditor(
                    campaign_name=campaign_name,
                    language=lang,
                    currency=curr
                )
                # Запускаем процесс обработки кампании
                editor.process_campaign()
            except Exception as ex:
                # Логируем ошибку, если что-то пошло не так в процессе обработки кампании
                logger.error(f"Error processing all campaigns {campaign_name} for {lang=}, {curr=}", ex, exc_info=True)


def main_process(campaign_name: str, categories: List[str] | str, language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Основная функция для обработки кампании.

    Args:
        campaign_name (str): Название рекламной кампании.
        categories (List[str] | str): Список категорий для кампании. Если пуст, обрабатывается вся кампания без конкретных категорий.
        language (Optional[str]): Язык для кампании.
        currency (Optional[str]): Валюта для кампании.
    """
    # Определяем локали для обработки на основе предоставленных языка и валюты
    locales_to_process = [(language, currency)] if language and currency else [(lang, curr) for locale in locales for lang, curr in locale.items()]

    # Итерируемся по локалям для обработки
    for lang, curr in locales_to_process:
        if categories:
            # Обрабатываем каждую указанную категорию
            for category in categories:
                logger.info(f"Processing specific category {category=}, {lang=}, {curr=}")
                process_campaign_category(campaign_name, category, lang, curr)
        else:
            # Обрабатываем всю кампанию, если не указаны конкретные категории
            logger.info(f"Processing entire campaign {campaign_name=}, {lang=}, {curr=}")
            process_campaign(campaign_name, lang, curr)


def main() -> None:
    """Основная функция для разбора аргументов и запуска обработки."""
    parser = argparse.ArgumentParser(description="Prepare AliExpress Campaign")
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

    # Разбираем аргументы командной строки
    args = parser.parse_args()

    # Если указан флаг --all, обрабатываем все кампании
    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        # Иначе обрабатываем указанную кампанию с заданными параметрами
        main_process(
            args.campaign_name, args.categories or [], args.language, args.currency
        )

# Запускаем основную функцию, если скрипт запущен напрямую
if __name__ == "__main__":
    main()