## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль реализует `PlaywrightCrawler` с помощью Playwright, позволяя настроить параметры запуска браузера, такие как user-agent, прокси-сервер, размер окна и другие опции, определенные в `playwrid.json`.

Шаги выполнения
-------------------------
1. **Зависимости:** Установите Playwright и Crawlee:
   ```bash
   pip install playwright crawlee
   ```
2. **Playwright:** Установите браузеры:
   ```bash
   playwright install
   ```
3. **Настройка**: Настройте параметры в файле `playwrid.json`:
   - `browser_type`: Тип браузера (`chromium`, `firefox`, `webkit`).
   - `headless`: Запуск браузера в headless-режиме (`true` или `false`).
   - `options`: Дополнительные параметры запуска браузера.
   - `user_agent`: Строка user-agent для запросов браузера.
   - `proxy`: Настройки прокси-сервера.
   - `viewport`: Размер окна браузера.
   - `timeout`: Максимальное время ожидания операций (в миллисекундах).
   - `ignore_https_errors`: Игнорирование ошибок HTTPS.
4. **Инициализация**: Импортируйте и инициализируйте `Playwrid`:
   ```python
   from src.webdriver.playwright import Playwrid

   # Инициализация Playwright Crawler с пользовательскими опциями
   browser = Playwrid(options=["--headless"])

   # Запуск браузера и переход на сайт
   browser.start("https://www.example.com")
   ```
5. **Использование**: `Playwrid` автоматически загружает настройки из `playwrid.json` и использует их для конфигурации WebDriver. Вы также можете указать пользовательский user-agent и передать дополнительные опции во время инициализации WebDriver.

Пример использования
-------------------------
```python
from src.webdriver.playwright import Playwrid

# Инициализация Playwright Crawler с пользовательскими опциями
browser = Playwrid(options=["--headless"])

# Запуск браузера и переход на сайт
browser.start("https://www.example.com")
```