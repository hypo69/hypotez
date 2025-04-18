### Анализ кода модуля `hypotez/src/webdriver/crawlee_python/README.MD`

# Crawlee Python Module for Automation and Data Scraping

Этот модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee. Он позволяет настраивать параметры запуска браузера, обрабатывать веб-страницы и извлекать данные из них. Конфигурация управляется через файл `crawlee_python.json`.

## Ключевые особенности

-   **Централизованная конфигурация**: Конфигурация управляется через файл `crawlee_python.json`.
-   **Custom Options Support**: Возможность передачи пользовательских опций во время инициализации.
-   **Enhanced Logging and Error Handling**: Предоставляет подробные логи для инициализации, проблем с конфигурацией и ошибок WebDriver.
-   **Proxy Support**: Настройка прокси-серверов для обхода ограничений.
-   **Flexible Browser Settings**: Настройка размера окна просмотра, user-agent и других параметров браузера.

## Требования

Перед использованием этого модуля убедитесь, что установлены следующие зависимости:

*   Python 3.x
*   Playwright
*   Crawlee

Установите необходимые зависимости Python:

```bash
pip install playwright crawlee
```

Дополнительно убедитесь, что Playwright установлен и настроен для работы с браузером. Установите браузеры, используя команду:

```bash
playwright install
```

## Конфигурация

Конфигурация для Crawlee Python хранится в файле `crawlee_python.json`. Ниже приведен пример структуры конфигурационного файла и его описание:

### Пример конфигурации (`crawlee_python.json`)

```json
{
  "max_requests": 10,
  "headless": true,
  "browser_type": "chromium",
  "options": [
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-gpu"
  ],
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
  "proxy": {
    "enabled": false,
    "server": "http://proxy.example.com:8080",
    "username": "user",
    "password": "password"
  },
  "viewport": {
    "width": 1280,
    "height": 720
  },
  "timeout": 30000,
  "ignore_https_errors": false
}
```

### Описание полей конфигурации

#### 1. `max_requests`

Максимальное количество запросов для выполнения во время обхода. По умолчанию `10`.

#### 2. `headless`

Логическое значение, указывающее, следует ли запускать браузер в безголовом режиме. По умолчанию `true`.

#### 3. `browser_type`

Тип используемого браузера. Возможные значения:

*   `chromium` (по умолчанию)
*   `firefox`
*   `webkit`

#### 4. `options`

Список аргументов командной строки, передаваемых в браузер. Примеры:

*   `--disable-dev-shm-usage`: Отключает использование `/dev/shm` в контейнерах Docker.
*   `--no-sandbox`: Отключает режим песочницы.
*   `--disable-gpu`: Отключает аппаратное ускорение GPU.

#### 5. `user_agent`

Строка user-agent, используемая для запросов браузера.

#### 6. `proxy`

Настройки прокси-сервера:

*   **enabled**: Логическое значение, указывающее, следует ли использовать прокси.
*   **server**: Адрес прокси-сервера.
*   **username**: Имя пользователя для аутентификации на прокси-сервере.
*   **password**: Пароль для аутентификации на прокси-сервере.

#### 7. `viewport`

Размеры окна браузера:

*   **width**: Ширина окна.
*   **height**: Высота окна.

#### 8. `timeout`

Максимальное время ожидания для операций (в миллисекундах). По умолчанию `30000` (30 секунд).

#### 9. `ignore_https_errors`

Логическое значение, указывающее, следует ли игнорировать ошибки HTTPS. По умолчанию `false`.

## Использование

Чтобы использовать `CrawleePython` в своем проекте, просто импортируйте и инициализируйте его:

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

# Инициализируйте CrawleePython с пользовательскими опциями
async def main():
    crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium', options=["--headless"])
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

Класс `CrawleePython` автоматически загружает настройки из файла `crawlee_python.json` и использует их для настройки WebDriver. Вы также можете указать пользовательский user-agent и передать дополнительные опции во время инициализации WebDriver.

## Логирование и отладка

Класс WebDriver использует `logger` из `src.logger` для логирования ошибок, предупреждений и общей информации. Все проблемы, возникающие во время инициализации, конфигурации или выполнения, будут регистрироваться для упрощения отладки.

### Пример логов

*   **Ошибка во время инициализации WebDriver**: `Error initializing Crawlee Python: <детали ошибки>`
*   **Проблемы с конфигурацией**: `Error in crawlee_python.json file: <детали проблемы>`

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Смотрите файл [LICENSE](../../LICENSE) для деталей.