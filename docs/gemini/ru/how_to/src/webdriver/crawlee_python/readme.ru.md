### Как использовать модуль Crawlee Python для автоматизации и сбора данных
=========================================================================================

Описание
-------------------------
Модуль Crawlee Python предоставляет кастомную реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee для автоматизации и сбора данных. Он позволяет настраивать параметры запуска браузера, обрабатывать веб-страницы и извлекать данные из них. Конфигурация управляется через файл `crawlee_python.json`.

Шаги выполнения
-------------------------
1. **Установка зависимостей**:
   - Убедитесь, что установлены Python 3.x, Playwright и Crawlee.
   - Установите необходимые зависимости Python, выполнив команду `pip install playwright crawlee`.
   - Установите браузеры, используя команду `playwright install`.
2. **Настройка конфигурации**:
   - Отредактируйте файл `crawlee_python.json` для указания нужных параметров, таких как `max_requests`, `headless`, `browser_type`, `options`, `user_agent`, `proxy`, `viewport`, `timeout` и `ignore_https_errors`.
3. **Использование в проекте**:
   - Импортируйте класс `CrawleePython` из модуля `src.webdriver.crawlee_python`.
   - Инициализируйте `CrawleePython` с пользовательскими опциями.
   - Вызовите метод `run` с передачей списка URL для обхода.

Пример использования
-------------------------

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

# Функция запускающая асинхронного краулера
async def main():
    # Инициализация CrawleePython с пользовательскими опциями
    crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium', options=["--headless"])
    # Запуск краулера с указанными URL
    await crawler.run(['https://www.example.com'])

# Запуск асинхронной функции
asyncio.run(main())
```