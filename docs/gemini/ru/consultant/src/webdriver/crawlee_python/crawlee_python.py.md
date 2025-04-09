### **Анализ кода модуля `crawlee_python.py`**

## \file /src/webdriver/crawlee_python/crawlee_python.py

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование асинхронности для неблокирующих операций.
  - Четкое разделение на методы для настройки, запуска и экспорта данных.
  - Использование `PlaywrightCrawler` из библиотеки Crawlee.
  - Добавлены аннотации типов.
- **Минусы**:
  - Docstring написаны на английском языке.
  - Не все функции и методы содержат подробное описание входных и выходных параметров.
  - Отсутствуют примеры использования в docstring.
  - Отсутствует обработка ошибок при экспорте данных.
  - Не используется `j_loads` или `j_loads_ns` для чтения конфигурационных файлов (если таковые имеются).
  - Не используется модуль `webdriver` из `hypotez`

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Перевести все docstring на русский язык, сохраняя формат UTF-8.
    *   Добавить примеры использования для основных методов, чтобы облегчить понимание их работы.
    *   Улучшить описание возвращаемых значений и возможных исключений в docstring.
2.  **Обработка ошибок**:
    *   Добавить обработку ошибок в метод `export_data`, чтобы логировать возможные проблемы при экспорте данных.
    *   Использовать `logger.error` с передачей исключения `ex` и `exc_info=True` для более подробного логирования ошибок.
3.  **Конфигурация**:
    *   Если в коде используются конфигурационные файлы, заменить стандартное `open` и `json.load` на `j_loads` или `j_loads_ns`.
4.  **Использование `webdriver` из `hypotez`**:
    *   Рассмотреть возможность использования модуля `webdriver` из `hypotez` для управления браузером, если это соответствует архитектуре проекта.
5.  **Аннотации**:
    *   Убедиться, что аннотации типов используются для всех переменных и параметров функций.
6.  **Комментарии**:
    *   Уточнить комментарии, избегая общих фраз вроде "получаем" или "делаем". Использовать более конкретные термины, такие как "извлекаем", "проверяем", "выполняем".
    *   Проверить, что все комментарии полезны и актуальны.
7.  **Использовать webdriver**:

    ```python
    from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
    driver = Driver(Firefox)

    Пoсле чего может использоваться как

    close_banner = {
      "attribute": null,
      "by": "XPATH",
      "selector": "//button[@id = 'closeXButton']",
      "if_list": "first",
      "use_mouse": false,
      "mandatory": false,
      "timeout": 0,
      "timeout_for_event": "presence_of_element_located",
      "event": "click()",
      "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
    }

    result = driver.execute_locator(close_banner)
    ```

**Оптимизированный код:**

```python
## \file /src/webdriver/crawlee_python/crawlee_python.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для реализации кастомного краулера на базе Crawlee с использованием Playwright.
=========================================================================================

Модуль предоставляет класс :class:`CrawleePython`, который позволяет настраивать параметры браузера,
обрабатывать запросы и извлекать данные с веб-страниц.

Пример использования:
----------------------

>>> if __name__ == "__main__":
>>>     async def main():
>>>         crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox')
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
    Кастомная реализация `PlaywrightCrawler` с использованием библиотеки Crawlee.

    Attributes:
        max_requests (int): Максимальное количество запросов для выполнения во время обхода.
        headless (bool): Запускать ли браузер в режиме без графического интерфейса.
        browser_type (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
        crawler (PlaywrightCrawler): Инстанс PlaywrightCrawler.
    """

    def __init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None) -> None:
        """
        Инициализирует CrawleePython краулер с указанными параметрами.

        Args:
            max_requests (int): Максимальное количество запросов для выполнения во время обхода. По умолчанию 5.
            headless (bool): Запускать ли браузер в режиме без графического интерфейса. По умолчанию False.
            browser_type (str): Тип используемого браузера ('chromium', 'firefox', 'webkit'). По умолчанию 'firefox'.
            options (Optional[List[str]]): Список пользовательских опций для передачи в браузер. По умолчанию None.

        """
        self.max_requests: int = max_requests
        self.headless: bool = headless
        self.browser_type: str = browser_type
        self.options: List[str] = options or []
        self.crawler: PlaywrightCrawler | None = None

    async def setup_crawler(self) -> None:
        """
        Настраивает экземпляр PlaywrightCrawler с указанной конфигурацией.
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
            """
            context.log.info(f'Processing {context.request.url} ...')

            # Добавляем в очередь все ссылки, найденные на странице.
            await context.enqueue_links()

            # Извлекаем данные со страницы с использованием Playwright API.
            data: Dict[str, Any] = {
                'url': context.request.url,
                'title': await context.page.title(),
                'content': (await context.page.content())[:100],
            }

            # Отправляем извлеченные данные в набор данных по умолчанию.
            await context.push_data(data)

    async def run_crawler(self, urls: List[str]) -> None:
        """
        Запускает краулер с начальным списком URL-адресов.

        Args:
            urls (List[str]): Список URL-адресов для начала обхода.
        """
        await self.crawler.run(urls)

    async def export_data(self, file_path: str) -> None:
        """
        Экспортирует весь набор данных в JSON-файл.

        Args:
            file_path (str): Путь для сохранения экспортированного JSON-файла.
        """
        try:
            await self.crawler.export_data(file_path)
        except Exception as ex:
            logger.error(f'Error exporting data to {file_path}', ex, exc_info=True)

    async def get_data(self) -> Dict[str, Any]:
        """
        Извлекает извлеченные данные.

        Returns:
            Dict[str, Any]: Извлеченные данные в виде словаря.
        """
        data: List[Dict] = await self.crawler.get_data()
        return data

    async def run(self, urls: List[str]) -> None:
        """
        Основной метод для настройки, запуска краулера и экспорта данных.

        Args:
            urls (List[str]): Список URL-адресов для начала обхода.
        """
        try:
            await self.setup_crawler()
            await self.run_crawler(urls)
            export_file_path: str = str(Path(gs.path.tmp / 'results.json'))
            await self.export_data(export_file_path)
            data: List[Dict] = await self.get_data()
            logger.info(f'Extracted data: {data}')
        except Exception as ex:
            logger.error('Crawler failed with an error:', ex, exc_info=True)


# Пример использования
if __name__ == '__main__':
    async def main():
        crawler: CrawleePython = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
        await crawler.run(['https://www.example.com'])

    asyncio.run(main())