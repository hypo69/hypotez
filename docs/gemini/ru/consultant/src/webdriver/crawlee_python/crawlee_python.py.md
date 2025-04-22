### **Анализ кода модуля `crawlee_python.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование Crawlee для управления браузером.
    - Наличие документации для классов и методов.
    - Использование асинхронности для неблокирующих операций.
    - Применение `logger` для логирования.
- **Минусы**:
    - Не все методы и классы имеют подробные docstring.
    - Отсутствуют примеры использования в docstring.
    - Некоторые комментарии в docstring на английском языке.
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Дополнить docstring для всех методов и классов, включая подробное описание аргументов, возвращаемых значений и возможных исключений.
    *   Добавить примеры использования в docstring, чтобы облегчить понимание и использование модуля.
    *   Перевести все комментарии и docstring на русский язык.
2.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных класса, чтобы повысить читаемость и облегчить отладку.
3.  **Обработка исключений**:
    *   Указывать более конкретные типы исключений в блоках `except`, чтобы улучшить обработку ошибок.
4.  **Использовать `j_loads_ns` для чтения конфигурационных файлов, если это необходимо.**
5.  **Удалить `# -* coding: utf-8 -*-` т.к. она устарела для Python3.**

**Оптимизированный код:**

```python
## \file /src/webdriver/crawlee_python/crawlee_python.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для Crawlee Python Crawler
===================================

Этот модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee.
Он позволяет настраивать параметры браузера, обрабатывать запросы и извлекать данные с веб-страниц.

Пример использования:

.. code-block:: python

    if __name__ == "__main__":
        async def main():
            crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox')
            await crawler.run(['https://www.example.com'])

        asyncio.run(main())

.. module:: src.webdriver.crawlee_python
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
from src import gs
import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns


class CrawleePython:
    """
    Пользовательская реализация `PlaywrightCrawler` с использованием библиотеки Crawlee.

    Attributes:
        max_requests (int): Максимальное количество запросов для выполнения во время обхода.
        headless (bool): Запускать ли браузер в режиме без графического интерфейса.
        browser_type (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
        crawler (PlaywrightCrawler): Экземпляр PlaywrightCrawler.
        options (List[str]): Список дополнительных опций для передачи в браузер.
    """

    def __init__(
        self,
        max_requests: int = 5,
        headless: bool = False,
        browser_type: str = 'firefox',
        options: Optional[List[str]] = None,
    ) -> None:
        """
        Инициализирует CrawleePython crawler с указанными параметрами.

        Args:
            max_requests (int): Максимальное количество запросов для выполнения во время обхода. По умолчанию 5.
            headless (bool): Запускать ли браузер в режиме без графического интерфейса. По умолчанию False.
            browser_type (str): Тип используемого браузера ('chromium', 'firefox', 'webkit'). По умолчанию 'firefox'.
            options (Optional[List[str]]): Список дополнительных опций для передачи в браузер. По умолчанию None.

        Example:
            >>> crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium')
        """
        self.max_requests: int = max_requests
        self.headless: bool = headless
        self.browser_type: str = browser_type
        self.options: List[str] = options or []
        self.crawler: Optional[PlaywrightCrawler] = None

    async def setup_crawler(self) -> None:
        """
        Настраивает экземпляр PlaywrightCrawler с указанной конфигурацией.
        """
        self.crawler = PlaywrightCrawler(
            max_requests_per_crawl=self.max_requests,
            headless=self.headless,
            browser_type=self.browser_type,
            launch_options={"args": self.options},
        )

        @self.crawler.router.default_handler
        async def request_handler(context: PlaywrightCrawlingContext) -> None:
            """
            Обработчик запросов по умолчанию для обработки веб-страниц.

            Args:
                context (PlaywrightCrawlingContext): Контекст обхода.

            Example:
                >>> async def request_handler(context: PlaywrightCrawlingContext):
                ...     context.log.info(f'Processing {context.request.url} ...')
            """
            context.log.info(f'Processing {context.request.url} ...')

            # Добавляет в очередь все ссылки, найденные на странице
            await context.enqueue_links()

            # Извлекает данные со страницы с использованием API Playwright
            data: Dict[str, Any] = {
                'url': context.request.url,
                'title': await context.page.title(),
                'content': (await context.page.content())[:100],
            }

            # Отправляет извлеченные данные в набор данных по умолчанию
            await context.push_data(data)

    async def run_crawler(self, urls: List[str]) -> None:
        """
        Запускает crawler с начальным списком URL-адресов.

        Args:
            urls (List[str]): Список URL-адресов для начала обхода.

        Example:
            >>> urls = ['https://www.example.com', 'https://www.example.org']
            >>> await crawler.run_crawler(urls)
        """
        await self.crawler.run(urls)

    async def export_data(self, file_path: str) -> None:
        """
        Экспортирует весь набор данных в JSON-файл.

        Args:
            file_path (str): Путь для сохранения экспортированного JSON-файла.

        Example:
            >>> file_path = 'output.json'
            >>> await crawler.export_data(file_path)
        """
        await self.crawler.export_data(file_path)

    async def get_data(self) -> Dict[str, Any]:
        """
        Извлекает извлеченные данные.

        Returns:
            Dict[str, Any]: Извлеченные данные в виде словаря.

        Example:
            >>> data = await crawler.get_data()
            >>> print(data)
        """
        data: Dict[str, Any] = await self.crawler.get_data()
        return data

    async def run(self, urls: List[str]) -> None:
        """
        Основной метод для настройки, запуска crawler и экспорта данных.

        Args:
            urls (List[str]): Список URL-адресов для начала обхода.

        Raises:
            Exception: Если crawler завершается с ошибкой.

        Example:
            >>> urls = ['https://www.example.com']
            >>> await crawler.run(urls)
        """
        try:
            await self.setup_crawler()
            await self.run_crawler(urls)
            await self.export_data(str(Path(gs.path.tmp / 'results.json')))
            data: Dict[str, Any] = await self.get_data()
            logger.info(f'Extracted data: {data.items()}')
        except Exception as ex:
            logger.critical('Crawler failed with an error:', ex, exc_info=True)


# Пример использования
if __name__ == '__main__':

    async def main():
        crawler: CrawleePython = CrawleePython(
            max_requests=5, headless=False, browser_type='firefox', options=['--headless']
        )
        await crawler.run(['https://www.example.com'])

    asyncio.run(main())