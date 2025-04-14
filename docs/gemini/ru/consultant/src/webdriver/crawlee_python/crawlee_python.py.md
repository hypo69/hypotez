### **Анализ кода модуля `crawlee_python.py`**

## \file /src/webdriver/crawlee_python/crawlee_python.py

Модуль предоставляет класс `CrawleePython`, который является оберткой над `PlaywrightCrawler` из библиотеки Crawlee. Он упрощает настройку и запуск веб-скрапера с использованием Playwright.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура класса, разделение на методы `setup_crawler`, `run_crawler`, `export_data` и `get_data`.
    - Использование асинхронности (`async/await`) для неблокирующих операций.
    - Наличие базовой обработки ошибок с логированием.
    - Использование аннотаций типов.
- **Минусы**:
    - Docstring на английском языке.
    - Не все методы имеют подробное описание в docstring.
    - В примере использования хардкодится значение `browser_type='firefox'`.

**Рекомендации по улучшению:**

1.  **Перевести docstring на русский язык** и привести к единообразному формату.
2.  **Добавить более подробные описания** в docstring методов, включая примеры использования.
3.  **Использовать `logger.error`** вместо `logger.critical` при обработке исключений, передавая ошибку как второй аргумент.
4.  **Удалить избыточные комментарии**, такие как `# -*- coding: utf-8 -*-` и `#! .pyenv/bin/python3`.
5.  **Удалить дублирование** `options=["--headless"]` в `if __name__ == '__main__'` в пользу `self.options`.

**Оптимизированный код:**

```python
## \file /src/webdriver/crawlee_python/crawlee_python.py
"""
Модуль для реализации Crawlee веб-скрапера на Python
=====================================================

Модуль предоставляет класс :class:`CrawleePython`, который является оберткой над `PlaywrightCrawler` из библиотеки Crawlee.
Он упрощает настройку и запуск веб-скрапера с использованием Playwright.

Пример использования
----------------------

>>> if __name__ == "__main__":
>>>     async def main():
>>>         crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
>>>         await crawler.run(['https://www.example.com'])
>>>
>>>     asyncio.run(main())
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
    Реализация `PlaywrightCrawler` с использованием библиотеки Crawlee.

    Атрибуты:
        max_requests (int): Максимальное количество запросов для выполнения во время обхода.
        headless (bool): Запуск браузера в headless режиме.
        browser_type (str): Тип браузера для использования ('chromium', 'firefox', 'webkit').
        crawler (PlaywrightCrawler): Экземпляр PlaywrightCrawler.
        options (Optional[List[str]]): Список дополнительных опций для запуска браузера.
    """

    def __init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None):
        """
        Инициализирует CrawleePython с заданными параметрами.

        Args:
            max_requests (int): Максимальное количество запросов для выполнения во время обхода. По умолчанию 5.
            headless (bool): Запуск браузера в headless режиме. По умолчанию False.
            browser_type (str): Тип браузера для использования ('chromium', 'firefox', 'webkit'). По умолчанию 'firefox'.
            options (Optional[List[str]]): Список дополнительных опций для запуска браузера. По умолчанию None.

        Example:
            >>> crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium', options=['--disable-gpu'])
        """
        self.max_requests = max_requests
        self.headless = headless
        self.browser_type = browser_type
        self.options = options or []
        self.crawler = None

    async def setup_crawler(self) -> None:
        """
        Настраивает экземпляр PlaywrightCrawler с указанной конфигурацией.

        Этот метод инициализирует `PlaywrightCrawler` с заданными параметрами, такими как максимальное количество запросов,
        headless режим и тип браузера. Также устанавливается обработчик запросов по умолчанию.

        Raises:
            Exception: В случае ошибки при создании или настройке `PlaywrightCrawler`.

        Example:
            >>> await crawler.setup_crawler()
        """
        self.crawler = PlaywrightCrawler(
            max_requests_per_crawl=self.max_requests,
            headless=self.headless,
            browser_type=self.browser_type,
            launch_options={"args": self.options}
        )

        @self.crawler.router.default_handler
        async def request_handler(context: PlaywrightCrawlingContext) -> None:
            """
            Обработчик запросов по умолчанию для обработки веб-страниц.

            Args:
                context (PlaywrightCrawlingContext): Контекст обхода.

            Этот обработчик извлекает данные из веб-страницы, такие как URL, заголовок и контент, а также добавляет в очередь все ссылки, найденные на странице.

            Raises:
                Exception: В случае ошибки при обработке запроса или извлечении данных.
            """
            context.log.info(f'Processing {context.request.url} ...')

            # Добавляем в очередь все ссылки, найденные на странице
            await context.enqueue_links()

            # Извлекаем данные из страницы с использованием Playwright API
            data = {
                'url': context.request.url,
                'title': await context.page.title(),
                'content': (await context.page.content())[:100],
            }

            # Отправляем извлеченные данные в набор данных по умолчанию
            await context.push_data(data)

    async def run_crawler(self, urls: List[str]) -> None:
        """
        Запускает обход с начальным списком URL-ов.

        Args:
            urls (List[str]): Список URL-ов для начала обхода.

        Raises:
            Exception: В случае ошибки во время выполнения обхода.

        Example:
            >>> await crawler.run_crawler(['https://www.example.com', 'https://www.example.org'])
        """
        await self.crawler.run(urls)

    async def export_data(self, file_path: str) -> None:
        """
        Экспортирует весь набор данных в JSON файл.

        Args:
            file_path (str): Путь для сохранения экспортированного JSON файла.

        Raises:
            Exception: В случае ошибки при экспорте данных.

        Example:
            >>> await crawler.export_data('data.json')
        """
        await self.crawler.export_data(file_path)

    async def get_data(self) -> Dict[str, Any]:
        """
        Извлекает полученные данные.

        Returns:
            Dict[str, Any]: Извлеченные данные в виде словаря.

        Raises:
            Exception: В случае ошибки при получении данных.

        Example:
            >>> data = await crawler.get_data()
            >>> print(data)
            {'url': 'https://www.example.com', 'title': 'Example Domain', 'content': '<!doctype html>...'}
        """
        data = await self.crawler.get_data()
        return data

    async def run(self, urls: List[str]) -> None:
        """
        Основной метод для настройки, запуска обхода и экспорта данных.

        Args:
            urls (List[str]): Список URL-ов для начала обхода.

        Raises:
            Exception: В случае ошибки во время настройки, запуска или экспорта данных.
        """
        try:
            await self.setup_crawler()
            await self.run_crawler(urls)
            await self.export_data(str(Path(gs.path.tmp / 'results.json')))
            data = await self.get_data()
            logger.info(f'Extracted data: {data.items()}')
        except Exception as ex:
            logger.error('Crawler failed with an error:', ex, exc_info=True)


# Пример использования
if __name__ == '__main__':
    async def main():
        crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
        await crawler.run(['https://www.example.com'])

    asyncio.run(main())