### **Анализ кода модуля `promoter.py`**

## \file /src/endpoints/advertisement/facebook/promoter.py

Модуль предназначен для автоматизации продвижения контента (сообщений, событий, рекламы) в группах Facebook. Он использует WebDriver для взаимодействия с Facebook, обрабатывает кампании и события, публикуя их в группах, избегая дублирования.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая организация кода по функциям и классам.
  - Использование `logger` для логирования.
  - Наличие docstring для большинства функций и классов.
- **Минусы**:
  - Не все функции и классы имеют подробные docstring, особенно внутренние функции.
  - Некоторые аннотации типов отсутствуют или неполные.
  - Использование `j_loads_ns` не везде, где это возможно.
  - Нет обработки исключений для некоторых операций.

**Рекомендации по улучшению**:

1.  **Документация**:
    *   Добавить подробные docstring для всех функций и методов, включая описание параметров, возвращаемых значений и возможных исключений.
    *   Улучшить описание модуля в целом, добавив примеры использования.
    *   Перевести docstring на русский язык.
2.  **Обработка исключений**:
    *   Добавить блоки `try...except` для обработки возможных исключений, особенно при работе с файлами и веб-драйвером.
    *   Логировать исключения с использованием `logger.error`, передавая информацию об ошибке и `exc_info=True`.
3.  **Типизация**:
    *   Добавить аннотации типов для всех переменных, где это возможно.
    *   Уточнить типы для параметров функций, используя `Optional` и `Union` (`|`) там, где это необходимо.
4.  **Использование `j_loads_ns`**:
    *   Заменить стандартное использование `open` и `json.load` на `j_loads_ns` для чтения JSON-файлов.
5.  **Форматирование**:
    *   Проверить код на соответствие PEP8 и исправить форматирование, где это необходимо.
    *   Использовать одинарные кавычки для строк.
    *   Добавить пробелы вокруг операторов присваивания.
6.  **Логирование**:
    *   Добавить больше информативных сообщений в лог, чтобы облегчить отладку и мониторинг.
7.  **Вебдрайвер**:
    *   Использовать `driver.execute_locator(l:dict)` для взаимодействия с веб-элементами.

**Оптимизированный код**:

```python
## \file /src/endpoints/advertisement/facebook/promoter.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для продвижения сообщений и событий в группах Facebook.
================================================================

Модуль содержит класс :class:`FacebookPromoter`, который используется для автоматической публикации рекламных материалов
в группах Facebook с использованием WebDriver.

Пример использования
----------------------

>>> from src.webdriver.driver import Driver, Firefox
>>> from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
>>> # Инициализация драйвера и промоутера
>>> driver = Driver(Firefox)
>>> promoter = FacebookPromoter(d=driver, promoter='aliexpress')
>>> # Запуск процесса продвижения (требуется настройка campaign_name и других параметров)
>>> # promoter.process_groups(campaign_name='some_campaign', language='ru', currency='RUB')
"""

import random
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode
from types import SimpleNamespace
from typing import Optional, List

from src import gs
from src.endpoints.advertisement import facebook
from src.webdriver.driver import Driver

from src.endpoints.advertisement.facebook.scenarios import (
    post_message,
    post_event,
    post_message_title,
    upload_post_media,
    message_publish,
    post_ad,
)

from src.utils.file import (
    read_text_file,
    get_filenames_from_directory,
    get_directory_names,
)
from src.utils.jjson import j_loads_ns, j_dumps
from src.utils.cursor_spinner import spinning_cursor
from src.logger.logger import logger
import time


def get_event_url(group_url: str) -> str:
    """
    Возвращает URL для создания события в Facebook, заменяя `group_id` на значение из входного URL.

    Args:
        group_url (str): URL группы Facebook, содержащий `group_id`.

    Returns:
        str: Модифицированный URL для создания события.
    """
    group_id = group_url.rstrip('/').split('/')[-1]
    base_url = 'https://www.facebook.com/events/create/'
    params = {
        'acontext': '{"event_action_history":[{"surface":"group"},{"mechanism":"upcoming_events_for_group","surface":"group"}],"ref_notif_type":null}',
        'dialog_entry_point': 'group_events_tab',
        'group_id': group_id
    }

    query_string = urlencode(params)
    return f'{base_url}?{query_string}'


class FacebookPromoter:
    """Класс для продвижения товаров и событий AliExpress в группах Facebook.

    Автоматизирует публикацию рекламных материалов в группах Facebook, используя WebDriver,
    обеспечивая продвижение категорий и событий, избегая дублирования.
    """
    d: Driver = None
    group_file_paths: str | Path = None
    no_video: bool = False
    promoter: str

    def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[List[str | Path] | str | Path] = None, no_video: bool = False) -> None:
        """Инициализирует промоутер для групп Facebook.

        Args:
            d (Driver): Экземпляр WebDriver для автоматизации браузера.
            promoter (str): Название промоутера (например, 'aliexpress').
            group_file_paths (Optional[List[str | Path] | str | Path], optional): Список путей к файлам, содержащим данные о группах. По умолчанию None.
            no_video (bool, optional): Флаг для отключения видео в постах. По умолчанию False.
        """
        self.promoter = promoter
        self.d = d
        self.group_file_paths = group_file_paths if group_file_paths else get_filenames_from_directory(gs.path.google_drive / 'facebook' / 'groups')
        self.no_video = no_video
        self.spinner = spinning_cursor()

    def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
        """Продвигает категорию или событие в группе Facebook.

        Args:
            group (SimpleNamespace): Данные группы Facebook.
            item (SimpleNamespace): Данные категории или события.
            is_event (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию False.
            language (str, optional): Язык продвижения. По умолчанию None.
            currency (str, optional): Валюта продвижения. По умолчанию None.

        Returns:
            bool: True, если продвижение прошло успешно, иначе False.
        """
        if language:
            if group.language.upper() != language.upper():
                return False
        if currency:
            if group.currency.upper() != currency.upper():
                return False

        item_name = item.event_name if is_event else item.category_name
        ev_or_msg = getattr(item.language, group.language) if is_event else item

        # Установка атрибутов события или сообщения
        if is_event:
            ev_or_msg.start = item.start
            ev_or_msg.end = item.end
            ev_or_msg.promotional_link = item.promotional_link

            if not post_event(d=self.d, event=ev_or_msg):
                self.log_promotion_error(is_event, item_name)
                return False
        else:
            if 'kazarinov' in self.promoter or 'emil' in self.promoter:
                if not post_ad(self.d, ev_or_msg):
                    return False

            elif not post_message(d=self.d, message=ev_or_msg, no_video=self.no_video, without_captions=False):
                return False

        # Обновление данных группы после публикации
        self.update_group_promotion_data(group, ev_or_msg.name)
        return True

    def log_promotion_error(self, is_event: bool, item_name: str) -> None:
        """Логирует ошибку продвижения категории или события.

        Args:
            is_event (bool): Флаг, указывающий, является ли продвигаемый элемент событием.
            item_name (str): Название категории или события.
        """
        logger.error(f'Ошибка при публикации {"события" if is_event else "категории"} {item_name}', exc_info=True)

    def update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False) -> None:
        """Обновляет данные группы после успешной публикации.

        Args:
            group (SimpleNamespace): Данные группы Facebook.
            item_name (str): Название категории или события.
            is_event (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию False.
        """
        timestamp = datetime.now().strftime('%d/%m/%y %H:%M')
        group.last_promo_sended = gs.now
        if is_event:
            group.promoted_events = group.promoted_events if isinstance(group.promoted_events, list) else [group.promoted_events]
            group.promoted_events.append(item_name)
        else:
            group.promoted_categories = group.promoted_categories if isinstance(group.promoted_categories, list) else [group.promoted_categories]
            group.promoted_categories.append(item_name)
        group.last_promo_sended = timestamp

    def process_groups(self, campaign_name: str = None, events: Optional[List[SimpleNamespace]] = None, is_event: bool = False, group_file_paths: Optional[List[str]] = None, group_categories_to_adv: List[str] = ['sales'], language: str = None, currency: str = None) -> None:
        """Обрабатывает все группы для текущей кампании или продвижения события.

        Args:
            campaign_name (str, optional): Название кампании. По умолчанию None.
            events (Optional[List[SimpleNamespace]], optional): Список событий для продвижения. По умолчанию None.
            is_event (bool, optional): Флаг, указывающий, является ли продвижение событием. По умолчанию False.
            group_file_paths (Optional[List[str]], optional): Список путей к файлам групп. По умолчанию None.
            group_categories_to_adv (List[str], optional): Список категорий групп для продвижения. По умолчанию ['sales'].
            language (str, optional): Язык продвижения. По умолчанию None.
            currency (str, optional): Валюта продвижения. По умолчанию None.
        """
        if not campaign_name and not events:
            logger.debug('Нечего продвигать!')
            return

        for group_file in group_file_paths:
            path_to_group_file: Path = gs.path.google_drive / 'facebook' / 'groups' / group_file
            try:
                groups_ns: SimpleNamespace = j_loads_ns(path_to_group_file)
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла группы {group_file=}', ex, exc_info=True)
                continue

            if not groups_ns:
                logger.error(f'Проблема в файле групп {group_file=}')
                continue

            for group_url, group in vars(groups_ns).items():
                group.group_url = group_url

                if not is_event and not self.check_interval(group):
                    logger.debug(f'{campaign_name=}\\n Интервал в группе: {group.group_url}', exc_info=True)
                    continue

                if not set(group_categories_to_adv).intersection(group.group_categories if isinstance(group.group_categories, list) else [group.group_categories]) or not 'active' in group.status:
                    continue

                if not is_event:
                    item = self.get_category_item(campaign_name, group, language, currency)
                else:
                    random.shuffle(events)
                    item = events.pop()

                if item.name in (group.promoted_events if is_event else group.promoted_categories):
                    logger.debug('Этот элемент уже был продвинут')
                    continue

                if not group.language.upper() == language.upper() and group.currency.upper() == currency.upper():
                    continue

                self.d.get_url(get_event_url(group.group_url) if is_event else group.group_url)

                if not self.promote(group=group, item=item, is_event=is_event, language=language, currency=currency):
                    continue

                try:
                    j_dumps(groups_ns, path_to_group_file)
                except Exception as ex:
                    logger.error(f'Ошибка при записи в файл группы {group_file=}', ex, exc_info=True)
                    continue

                t = random.randint(30, 420)
                print(f'sleeping {t} sec')
                time.sleep(t)

    def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
        """Получает элемент категории для продвижения на основе кампании и промоутера.

        Args:
            campaign_name (str): Название кампании.
            group (SimpleNamespace): Данные группы Facebook.
            language (str): Язык продвижения.
            currency (str): Валюта продвижения.

        Returns:
            SimpleNamespace: Элемент категории для продвижения.
        """
        if self.promoter == 'aliexpress':
            from src.suppliers.aliexpress.campaign import AliCampaignEditor
            ce = AliCampaignEditor(campaign_name=campaign_name, language=group.language, currency=group.currency)
            list_categories = ce.list_categories
            random.shuffle(list_categories)
            category_name = list_categories.pop()
            item = ce.get_category(category_name)
            item.name = category_name
            item.products = ce.get_category_products(item.category_name)
        else:
            base_path = gs.path.google_drive / self.promoter / 'campaigns' / campaign_name
            try:
                adv: SimpleNamespace = j_loads_ns(base_path / f'{language}_{currency}.json')
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла {language=}_{currency=}.json', ex, exc_info=True)
                return None

            adv_categories = list(vars(adv.category).items())  # Преобразуем в список для перемешивания
            random.shuffle(adv_categories)  # Перемешиваем категории

            for ad_name, ad in adv_categories:
                ad.description = read_text_file(base_path / 'category' / ad_name / 'description.txt')
                if not ad.description:
                    logger.error('ошибка чтения файла', exc_info=True)
                    continue
                item = ad
                item.name = ad_name
                _img = get_filenames_from_directory(base_path / 'category' / ad_name / 'images')
                if _img:
                    _img = _img if isinstance(_img, str) else _img[0]  # Беру только первое изображение
                    item.img_path = Path(gs.path.local) / _img
        return item

    def check_interval(self, group: SimpleNamespace) -> bool:
        """Проверяет, достаточно ли времени прошло для продвижения этой группы.

        Args:
            group (SimpleNamespace): Данные группы Facebook.

        Returns:
            bool: True, если достаточно времени прошло, иначе False.
        """
        # Добавить логику проверки интервала
        return True

    def validate_group(self, group: SimpleNamespace) -> bool:
        """Проверяет, что данные группы корректны.

        Args:
            group (SimpleNamespace): Данные группы Facebook.

        Returns:
            bool: True, если данные группы корректны, иначе False.
        """
        return group and hasattr(group, 'group_url') and hasattr(group, 'group_categories')