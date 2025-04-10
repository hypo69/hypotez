### **Анализ кода модуля `quotation_builder.py`**

## \file /src/endpoints/kazarinov/scenarios/quotation_builder.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на классы и функции, что улучшает читаемость и поддерживаемость.
  - Используется логирование для отслеживания ошибок и хода выполнения программы.
  - Применяются аннотации типов.
- **Минусы**:
  - Встречаются конструкции `try...except` с пустым блоком `except`, что может скрывать ошибки.
  - Есть участки кода с `...`, что указывает на незавершенность реализации.
  - Не везде используется `logger.error` с передачей исключения `ex` и `exc_info=True`.
  - Некоторые docstring написаны на английском языке.
  - Не все переменные аннотированы типами.
  - Отсутствует обработка исключений при создании инстанса класса `Driver`.

**Рекомендации по улучшению:**

1.  **Документация**:
    - Перевести все docstring на русский язык, сохраняя формат UTF-8.
    - Дополнить описания для всех функций, классов и их параметров, включая возвращаемые значения и возможные исключения.
    - Добавить примеры использования для основных функций.

2.  **Обработка исключений**:
    - В блоках `except` всегда добавлять логирование ошибок с использованием `logger.error(f"Описание ошибки", ex, exc_info=True)`.
    - Избегать пустых блоков `except`, чтобы не скрывать возможные проблемы.
    - Добавить обработку исключений при создании инстанса класса `Driver`.

3.  **Логирование**:
    - Убедиться, что все значимые события и ошибки логируются с достаточным уровнем детализации.

4.  **Завершение реализации**:
    - Заменить все участки кода с `...` на полноценную реализацию или, если это временно, оставить комментарий с объяснением.

5.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это необходимо.
    - Проверить аннотации для всех входных и выходных параметров функций.

6.  **Использование вебдрайвера**:
    - Убедиться, что вебдрайвер инициализируется и используется корректно, с учетом настроек и параметров, определенных в соответствующих классах (`Driver`, `Firefox`, `Playwright`).

7.  **Улучшение стиля кода**:
    - Использовать одинарные кавычки для строк.
    - Добавить пробелы вокруг операторов присваивания.
    - Избегать использования `Union[]`, использовать `|` вместо него.
    - Переписать блок обработки исключений в функции `__init__`.

**Оптимизированный код:**

```python
## \file /src/endpoints/kazarinov/scenarios/quotation_builder.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для обработки извлечения, разбора и сохранения данных о продуктах поставщиков.
==================================================================

Предоставляет функциональность для извлечения, разбора и обработки данных о продуктах от различных поставщиков.
Модуль обрабатывает подготовку данных, обработку с использованием ИИ и интеграцию с Facebook для публикации продуктов.
"""
import re
from bs4 import BeautifulSoup
from jinja2.utils import F
from pydantic.type_adapter import P
import requests
import asyncio
import random
import shutil
from pathlib import Path
from typing import Optional, List, Any
from types import SimpleNamespace
from dataclasses import field
import telebot

import header
from header import __root__
from src import gs
from src.endpoints.prestashop.product_fields import ProductFields

from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.webdriver.playwright import Playwrid

from src.ai.gemini import GoogleGenerativeAI
from src.endpoints.advertisement.facebook.scenarios import (
    post_message_title, upload_post_media, message_publish
)
from src.suppliers.suppliers_list.morlevi.graber import Graber as MorleviGraber
from src.suppliers.suppliers_list.ksp.graber import Graber as KspGraber
from src.suppliers.suppliers_list.ivory.graber import Graber as IvoryGraber
from src.suppliers.suppliers_list.grandadvance.graber import Graber as GrandadvanceGraber
from src.endpoints.kazarinov.report_generator import ReportGenerator 

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, recursively_get_file_path
from src.utils.image import save_image_from_url_async, save_image
from src.utils.printer import pprint as print
from src.logger.logger import logger

##############################################################

ENDPOINT: str = 'kazarinov'

#############################################################

class QuotationBuilder:
    """
    Обрабатывает извлечение, разбор и сохранение данных о продуктах поставщиков.

    Attributes:
        driver (Driver): Экземпляр Selenium WebDriver.
        export_path (Path): Путь для экспорта данных.
        products_list (List[dict]): Список обработанных данных о продуктах.
        base_path (Path): Базовый путь к файлам модуля.
        config (SimpleNamespace): Конфигурация, загруженная из JSON.
        html_path (str | Path): Путь к HTML файлу.
        pdf_path (str | Path): Путь к PDF файлу.
        docx_path (str | Path): Путь к DOCX файлу.
        mexiron_name (str): Имя Mexiron.
        price (float): Цена.
        timestamp (str): Временная метка.
        model (GoogleGenerativeAI): Модель Google Generative AI.
        translations (SimpleNamespace): Переводы, загруженные из JSON.
        required_fields (tuple): Кортеж необходимых полей товара.
    """
    
    base_path: Path = __root__ / 'src' / 'endpoints' / ENDPOINT

    try:
        config: SimpleNamespace = j_loads_ns(base_path / f'{ENDPOINT}.json')
    except Exception as ex:
        logger.error(f"Ошибка загрузки конфигурации", ex, exc_info=True)

    
    html_path: str | Path
    pdf_path: str | Path
    docx_path: str | Path

    driver: 'Driver'
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: List = field(default_factory=list)
    model: 'GoogleGenerativeAI'
    translations: 'SimpleNamespace' =  j_loads_ns(base_path / 'translations' / 'mexiron.json')

    # Не все поля товара надо заполнять. Вот кортеж необходимых полей:
    required_fields: tuple = ('id_product',
                                'name',
                                'description_short',
                                'description',
                                'specification',
                                'local_image_path')


    def __init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None,  **kwards) -> None:
        """
        Инициализирует класс Mexiron с необходимыми компонентами.

        Args:
            mexiron_name (Optional[str]): Пользовательское имя для процесса Mexiron. По умолчанию текущее время.
            driver (Optional[Firefox | Playwrid | str]): Инстанс Selenium WebDriver. Может быть экземпляром Firefox, Playwrid или строкой 'firefox'/'playwright'. По умолчанию None.
            **kwards: Дополнительные параметры для инициализации веб-драйвера.

        Raises:
            Exception: Если не удалось создать путь для экспорта данных.
            Exception: Если не удалось загрузить модель, инструкции или API ключ.
        """
        self.mexiron_name = mexiron_name
        try:
            self.export_path = gs.path.external_storage / ENDPOINT / 'mexironim' / self.mexiron_name
        except Exception as ex:
            logger.error(f"Ошибка при создании пути для экспорта:", ex, exc_info=True)
            return

        # 1. Initialize webdriver

        try:
            if driver:
                if isinstance(driver, Driver):
                    self.driver = driver
                elif isinstance(driver, (Firefox, Playwrid, )):  # Chrome, Edge
                    self.driver = Driver(driver, **kwards)
                elif isinstance(driver, str):
                    if driver.lower() == 'firefox':
                        self.driver = Driver(Firefox, **kwards)
                    elif driver.lower() == 'playwright':
                        self.driver = Driver(Playwrid, **kwards)
            else:
                self.driver = Driver(Firefox, **kwards)
        except Exception as ex:
             logger.error(f"Ошибка инициализации веб-драйвера:", ex, exc_info=True)
             return        
                
        # 2. Initialize Gemini model

        try:
            system_instruction: str = (gs.path.endpoints / ENDPOINT / 'instructions' / 'system_instruction_mexiron.md').read_text(encoding='UTF-8')
            api_key: str = gs.credentials.gemini.kazarinov
            self.model = GoogleGenerativeAI(
                api_key=api_key,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error(f"Ошибка загрузки модели, инструкций или API ключа:", ex, exc_info=True)
            ...
            

    def convert_product_fields(self, f: ProductFields) -> dict:
        """
        Конвертирует поля продукта в словарь.

        Функция конвертирует поля из объекта `ProductFields` в простой словарь для модели ИИ.

        Args:
            f (ProductFields): Объект, содержащий распарсенные данные продукта.

        Returns:
            dict: Форматированный словарь данных продукта.

        Raises:
            Exception: Если `id_product` отсутствует.

        Example:
            >>> product_fields = ProductFields(...)
            >>> product_data = self.convert_product_fields(product_fields)
            >>> print(product_data)
            {'product_name': '...', 'product_id': '...', ...}

        .. note:: Правила построения полей определяются в `ProductFields`
        """
        if not f.id_product:
            logger.error(f"Сбой при получении полей товара.")
            return {}  # <- сбой при получении полей товара. Такое может произойти если вместо страницы товара попалась страница категории, при невнимательном составлении мехирона из комплектующих
        ...

        product_name: str = f.name['language']['value'] if f.name else ''
        description: str = f.description['language']['value'] if f.description else ''
        description_short: str = f.description_short['language']['value'] if f.description_short else ''
        specification: str = f.specification['language']['value'] if f.specification else ''
        
        if not product_name:
            return {}
        return {
            'product_name': product_name,
            'product_id': f.id_product,
            'description_short': description_short,
            'description': description,
            'specification': specification,
            'local_image_path': str(f.local_image_path),
        }

    def process_ai(self, products_list: List[str], lang: str,  attempts: int = 3) -> dict | bool:
        """
        Обрабатывает список продуктов с использованием AI модели.

        Args:
            products_list (List[str]): Список словарей данных о продуктах в виде строки.
            lang (str): Язык, на котором требуется получить ответ.
            attempts (int, optional): Количество попыток повторного запроса в случае неудачи. По умолчанию 3.

        Returns:
            dict: Обработанный ответ в формате словаря.
            bool: False, если не удалось получить валидный ответ после нескольких попыток.

        Raises:
            Exception: Если нет ответа от модели.
            Exception: Если произошла ошибка при парсинге ответа модели.

        Example:
            >>> products = [...]
            >>> result = self.process_ai(products, 'ru')
            >>> print(result)
            {'ключ': 'значение', ...}

        .. note::
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left

        model_command: str = Path(gs.path.endpoints / ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q: str = model_command + '\n' + str(products_list)
        response: str = self.model.ask(q)
        if not response:
            logger.error(f"Нет ответа от модели", exc_info=True)
            ...
            return {}

        response_dict: dict = j_loads(response)  # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error(f"Ошибка парсинга ответа модели", exc_info=True)
            if attempts > 1:
                ...
                return self.process_ai(products_list, lang, attempts - 1 )
            return {}
        return  response_dict

    async def process_ai_async(self, products_list: List[str], lang: str,  attempts: int = 3) -> dict | bool:
        """
        Асинхронно обрабатывает список продуктов с использованием AI модели.

        Args:
            products_list (List[str]): Список словарей данных о продуктах в виде строки.
            lang (str): Язык, на котором требуется получить ответ.
            attempts (int, optional): Количество попыток повторного запроса в случае неудачи. По умолчанию 3.

        Returns:
            dict: Обработанный ответ в формате словаря.
            bool: False, если не удалось получить валидный ответ после нескольких попыток.

        Raises:
            Exception: Если нет ответа от модели.
            Exception: Если произошла ошибка при парсинге ответа модели.

        Example:
            >>> products = [...]
            >>> result = await self.process_ai_async(products, 'ru')
            >>> print(result)
            {'ключ': 'значение', ...}

        .. note::
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left

        model_command: str = Path(gs.path.endpoints / ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q: str = model_command + '\n' + str(products_list)

        response: str = await self.model.ask_async(q)  # CORRECT

        if not response:
            logger.error(f"Нет ответа от модели", exc_info=True)
            ...
            return {}

        response_dict: dict = j_loads(response)  # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error(f'Ошибка {attempts} парсинга ответа модели', exc_info=True)
            if attempts > 1:
                ...
                return await self.process_ai_async(products_list, lang, attempts - 1)
            return {}
        return  response_dict

    async def save_product_data(self, product_data: dict) -> bool:
        """
        Сохраняет данные отдельного продукта в файл.

        Args:
            product_data (dict): Форматированные данные продукта.

        Returns:
            bool: True, если данные успешно сохранены, иначе False.

        Raises:
            Exception: Если произошла ошибка при сохранении данных.

        Example:
            >>> product_data = {'product_name': '...', 'product_id': '...', ...}
            >>> result = await self.save_product_data(product_data)
            >>> print(result)
            True
        """
        file_path: Path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}', exc_info=True)
            ...
            return
        return True

    async def post_facebook_async(self, mexiron: SimpleNamespace) -> bool:
        """Функция исполняет сценарий рекламного модуля `facvebook`."""
        ...
        self.driver.get_url('https://www.facebook.com/profile.php?id=61566067514123')
        currency: str = "ש''ח"
        title: str = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
        if not post_message_title(self.d, title):
            logger.warning(f'Не получилось отправить название мехирона')
            ...
            return

        if not upload_post_media(self.d, media = mexiron.products):
            logger.warning(f'Не получилось отправить media')
            ...
            return
        if not message_publish(self.d):
            logger.warning(f'Не получилось отправить media')
            ...
            return

        return True

def main() -> None:
    """
    Основная функция для запуска процесса создания отчетов.
    """
    ...
    lang: str = 'he'
    
    mexiron_name: str = '250203025325520'
    base_path: Path = Path(gs.path.external_storage)
    export_path: Path = base_path / ENDPOINT / 'mexironim' / mexiron_name
    html_path: Path = export_path / f'{mexiron_name}_{lang}.html'
    pdf_path: Path = export_path / f'{mexiron_name}_{lang}.pdf'
    docx_path: Path = export_path / f'{mexiron_name}_{lang}.doc'
    data: dict = j_loads(export_path / f'{mexiron_name}_{lang}.json')

    quotation: QuotationBuilder = QuotationBuilder(mexiron_name)
    asyncio.run(quotation.create_reports(data[lang], mexiron_name, lang, html_path, pdf_path, docx_path))
    

if __name__ == '__main__':
    main()