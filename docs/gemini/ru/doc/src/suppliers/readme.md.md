# Модули для работы с WebDriver и сбора данных

## Обзор

Этот набор модулей (`src/suppliers`) предназначен для автоматизации взаимодействия с веб-браузерами (в первую очередь, Firefox) с использованием Selenium WebDriver и для сбора (парсинга/граббинга) структурированных данных со страниц товаров на сайтах поставщиков. 

Основная цель - предоставить гибкий и расширяемый инструмент для:

1. **Управления WebDriver:** Настройка, запуск и управление экземпляром браузера Firefox с поддержкой профилей, опций запуска, прокси и пользовательских заголовков.
2. **Взаимодействия с веб-страницами:** Поиск элементов по различным стратегиям (локаторам), выполнение действий (клики, ввод текста), получение атрибутов и контента, выполнение JavaScript.
3. **Сбора данных о товарах:** Извлечение специфической информации (название, цена, описание, характеристики, изображения и т.д.) со страниц товаров поставщиков с использованием настраиваемых локаторов и сценариев.


## Ключевые Компоненты и Возможности

### WebDriver

*   **Расширенный WebDriver (`firefox.py`, `driver.py`, `js.py`):**
    *   Инициализация Firefox с гибкой конфигурацией через `firefox.json`.
    *   Поддержка профилей Firefox (системных или внутренних).
    *   Управление опциями запуска (windowless, kiosk, кастомные аргументы).
    *   Автоматическая настройка User-Agent (случайный или из конфига).
    *   Интегрированная поддержка прокси (`proxy.py`): загрузка списка, проверка и автоматическая установка рабочего прокси (SOCKS4/SOCKS5/HTTP) при включении опции.
    *   Вспомогательные методы для общих задач: `get_url` (с ожиданием загрузки), `scroll`, `wait`, `fetch_html`, `locale` (определение языка страницы).
    *   Утилиты для выполнения JavaScript (`js.py`): `readyState`, `window_focus`, `get_referrer`, `get_page_lang`, `unhide_DOM_element`.

### Исполнитель Локаторов

*   **Мощный Исполнитель Локаторов (`executor.py`):**
    *   Класс `ExecuteLocator` для асинхронного поиска элементов и выполнения действий.
    *   Поддержка различных стратегий поиска (`By.XPATH`, `By.CSS_SELECTOR`, `By.ID`, etc.).
    *   Описание локаторов и действий в виде словарей или `SimpleNamespace`.
    *   Выполнение различных событий: `click()`, `type(...)`, `send_keys(...)`, `clear()`, `pause(...)`, `upload_media()`, `screenshot()`.
    *   Получение атрибутов, текста или самих веб-элементов (`WebElement`).
    *   Гибкая обработка списков элементов (`if_list`: "all", "first", "last", "even", "odd", index, list of indices).
    *   Настройка таймаутов ожидания элементов (`presence_of_element_located`, `visibility_of_all_elements_located`).
    *   Возможность сделать скриншот конкретного элемента (`get_webelement_as_screenshot`).
    *   Метод для "печати" текста с задержкой (`send_message`).

### Система Сбора Данных

*   **Система Сбора Данных (`graber.py`, `get_graber_by_supplier.py`, `suppliers_list/*/graber.py`):**
    *   Базовый класс `Graber` (`graber.py`) с общими методами для сбора данных со страницы товара.
    *   Для каждого поставщика создается свой класс-наследник `Graber` (например, `KspGraber`, `AliexpressGraber`) в директории `src/suppliers/suppliers_list/<supplier_prefix>/`.
    *   Загрузка локаторов для полей товара (`product.json`) и категорий (`category.json`) для конкретного поставщика.
    *   Методы для извлечения каждого поля товара (например, `name()`, `price()`, `description()`, `specification()`, `local_image_path()`). Эти методы используют `driver.execute_locator` с соответствующими локаторами.
    *   **Возможность переопределения** методов сбора полей в классах-наследниках для реализации специфичной логики поставщика.
    *   Основной метод сбора `grab_page_async(*fields_to_grab)` для извлечения указанных полей.
    *   **Выполнение сценариев:**
        *   Загрузка сценариев из JSON-файлов в директории `src/suppliers/suppliers_list/<supplier_prefix>/scenarios/`.
        *   Методы `process_supplier_scenarios_async` и `process_scenarios` для автоматического обхода категорий (согласно логике в `scenario.py` поставщика), сбора данных для каждого товара и (в примере) добавления его через `PrestaProduct`.
    *   Фабричные функции (`get_graber_by_supplier.py`) для получения нужного экземпляра грабера по URL или префиксу поставщика.
    *   Декоратор `@close_pop_up()` для выполнения действия (например, закрытия всплывающего окна) перед сбором поля (настраивается через `Config.locator_for_decorator`).

## Структура Модулей

*   `/src/webdriver/`: Модули для работы с WebDriver.
    *   `driver.py`: Общие вспомогательные методы для драйвера.
    *   `firefox/`: Все для Firefox.
        *   `firefox.py`: Класс `Firefox`, инициализация, настройка, внедрение методов.
        *   `firefox.json`: Файл конфигурации Firefox.
    *   `js.py`: Утилиты JavaScript.
    *   `executor.py`: `ExecuteLocator` для работы с элементами.
    *   `proxy.py`: Логика работы с прокси.
    *   `proxies.txt`: (Автоматически создаваемый) Список прокси.
*   `/src/suppliers/`: Модули для работы с поставщиками.
    *   `graber.py`: Базовый класс `Graber`.
    *   `get_graber_by_supplier.py`: Фабрика для получения нужного грабера.
    *   `suppliers_list/`: Директория для каждого поставщика.
        *   `<supplier_prefix>/`: Папка конкретного поставщика (например, `ksp`, `aliexpress`).
            *   `graber.py`: Класс-наследник `Graber` для этого поставщика (с возможным переопределением методов).
            *   `locators/`: JSON-файлы с локаторами.
                *   `product.json`: Локаторы для полей на странице товара.
                *   `category.json`: Локаторы для элементов на странице категории.
            *   `scenarios/`: JSON-файлы со сценариями сбора данных (например, URL категорий и соответствующие ID категорий в PrestaShop).
            *   `scenario.py`: (Опционально, но используется в `process_scenarios`) Python-модуль с логикой сценария, например, функция `get_list_products_in_category` для получения ссылок на товары со страницы категории.

## Установка Зависимостей

Убедитесь, что установлены необходимые библиотеки:

```bash
pip install selenium requests fake-useragent # Добавьте другие, если они используются (например, langdetect)
```

Также необходимо:

1. Установить браузер **Mozilla Firefox**.
2. Скачать **GeckoDriver**, совместимый с вашей версией Firefox и ОС.
3. Указать **правильные пути** к `firefox.exe` (или бинарному файлу Firefox) и `geckodriver.exe` в файле `src/webdriver/firefox/firefox.json`.

## Конфигурация (`firefox.json`)

Файл `/src/webdriver/firefox/firefox.json` управляет настройками драйвера Firefox.

```json
{
  "options": [], // Доп. аргументы командной строки Firefox (напр., "--private")
  "disabled_options": [ "--kiosk", "--headless" ], // Пример отключенных (не используются)
  "profile_directory": {
    // Путь к профилю Firefox
    "os": "%LOCALAPPDATA%\\\\Mozilla\\\\Firefox\\\\Profiles\\\\xxxxx.default-release", // Системный профиль (Windows)
    "internal": "webdriver\\\\firefox\\\\profiles\\\\xxxxx.default-release", // Профиль внутри проекта
    "default": "os" // Использовать "os" или "internal" по умолчанию
  },
  "executable_path": {
    // Пути к исполняемым файлам (относительно корня проекта)
    "firefox_binary": "bin\\\\webdrivers\\\\firefox\\\\ff\\\\core-XXX\\\\firefox.exe",
    "geckodriver": "bin\\\\webdrivers\\\\firefox\\\\gecko\\\\XXX\\\\geckodriver.exe"
  },
  "headers": { // Устанавливаются через preferences, не прямые HTTP-заголовки
    "User-Agent": "Mozilla/5.0 ...", // Переопределение User-Agent
    "Accept": "text/html...",
    // ... другие
    "Connection": "keep-alive"
  },
  "proxy_enabled": false, // Использовать прокси? (true/false)
  "window_mode": null // Режим окна: null (обычный), "kiosk", "headless", и т.д.
}
```

**Важно:**

*   Пути в `executable_path` и `profile_directory.internal` должны быть указаны **относительно корня проекта**.
*   Переменная окружения `%LOCALAPPDATA%` (для `profile_directory.os`) будет автоматически раскрыта в Windows.
*   Убедитесь, что указанные пути и версии драйверов **актуальны** для вашей системы.

## Использование

### 1. Инициализация WebDriver

```python
import asyncio
from src.webdriver.firefox import Firefox
from src.logger.logger import logger

try:
    # Инициализация с настройками из firefox.json
    # Можно переопределить параметры: window_mode, profile_name
    driver = Firefox(window_mode="kiosk")
    # Или использовать настройки по умолчанию:
    # driver = Firefox()
    logger.info("Драйвер Firefox успешно запущен.")
except Exception as e:
    logger.critical(f"Не удалось инициализировать драйвер Firefox: {e}")
    exit()

# 'driver' теперь содержит стандартные методы Selenium + добавленные
```

### 2. Базовые Действия с WebDriver

```python
# Переход по URL
if driver.get_url("https://www.example.com"):
    logger.info(f"Перешли на {driver.current_url}")

    # Прокрутка страницы
    driver.scroll(scrolls=1, direction='down')

    # Ожидание
    driver.wait(1)

    # Получение HTML
    html = driver.fetch_html()
    if html:
        logger.info("HTML получен.")
else:
    logger.error("Не удалось загрузить страницу.")

# Закрытие драйвера
# driver.quit()
```

### 3. Взаимодействие с Элементами (`ExecuteLocator`)

```python
from types import SimpleNamespace

# Определяем локатор (словарь или SimpleNamespace)
login_button_locator = {
    "locator_description": "Кнопка входа",
    "by": "id",
    "selector": "login-button",
    "event": "click()", # Действие - клик
    "mandatory": True,
    "timeout": 10
}

input_field_locator = SimpleNamespace(
    locator_description="Поле ввода имени",
    by="css selector",
    selector="input[name='username']",
    # event="type(МойЛогин)", # Ввести текст
    attribute="value", # Или получить атрибут 'value'
    mandatory=True,
    timeout=5
)

async def perform_actions():
    # Выполняем клик
    click_success = await driver.execute_locator(login_button_locator)
    if click_success:
        logger.info("Клик выполнен.")

    # Получаем значение атрибута
    input_value = await driver.execute_locator(input_field_locator)
    if input_value is not None:
        logger.info(f"Значение поля ввода: {input_value}")

    # Можно также получить WebElement, если event и attribute не указаны
    element = await driver.get_webelement_by_locator(input_field_locator)
    if element:
        logger.info(f"Найден элемент: {element.tag_name}")

# Запуск асинхронной функции
# asyncio.run(perform_actions())

# ВАЖНО: driver.execute_locator и другие методы executor.py - асинхронные!
```

### 4. Использование Системы Сбора Данных (`Graber`)

**Сценарий 1: Запуск автоматического сбора по сценариям поставщика**

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix
# Предполагается, что driver уже инициализирован

supplier = "ksp" # Префикс поставщика
lang_id = 2 # ID языка в PrestaShop

# Получаем экземпляр грабера для KSP
graber = get_graber_by_supplier_prefix(driver, supplier, lang_index=lang_id)

if graber:
    logger.info(f"Грабер для '{supplier}' получен.")

    async def run_supplier_processing():
        # Запускаем обработку всех сценариев из папки scenarios/ для ksp
        # Эта функция сама обойдет категории, получит URL товаров,
        # вызовет grab_page_async для каждого и добавит товар в PrestaShop
        # (согласно логике в graber.py и scenario.py)
        results = await graber.process_supplier_scenarios_async(supplier_prefix=supplier, id_lang=lang_id)
        if results:
            logger.info(f"Обработка сценариев для '{supplier}' завершена. Собрано {len(results)} товаров.")
        else:
            logger.error(f"Ошибка при обработке сценариев для '{supplier}'.")

    # Запуск
    asyncio.run(run_supplier_processing())

else:
    logger.error(f"Не удалось получить грабер для поставщика '{supplier}'.")

```

**Сценарий 2: Ручной сбор данных с конкретной страницы товара**

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
# Предполагается, что driver уже инициализирован

product_url = "https://ksp.co.il/web/item/12345" # Пример URL товара
lang_id = 2

# Получаем грабер по URL
graber = get_graber_by_supplier_url(driver, product_url, lang_index=lang_id)
# Важно: get_graber_by_supplier_url уже выполняет driver.get_url(product_url)

if graber:
    logger.info(f"Грабер для URL {product_url} получен.")

    async def grab_single_product():
        # Определяем, какие поля мы хотим собрать
        fields_to_grab = [
            'id_product', 'name', 'price', 'description',
            'specification', 'local_image_path', 'id_supplier'
        ]
        # Вызываем метод сбора для текущей страницы
        product_data: ProductFields = await graber.grab_page_async(*fields_to_grab, id_lang=lang_id)

        if product_data:
            logger.success(f"Данные для товара успешно собраны:")
            # Выводим или обрабатываем собранные данные
            print(product_data.to_dict()) # Пример вывода словаря
            # Дальнейшие действия: сохранение в БД, отправка в API и т.д.
            # Например, добавление через PrestaProduct
            # from src.endpoints.prestashop.product import PrestaProduct
            # pp = PrestaProduct()
            # pp.add_new_product(product_data)
        else:
            logger.error(f"Не удалось собрать данные со страницы {product_url}")

    # Запуск
    asyncio.run(grab_single_product())

else:
    logger.error(f"Не найден подходящий грабер для URL: {product_url}")

# Не забываем закрыть драйвер после всех операций
driver.quit()
```

### 5. Логирование

Модуль использует настроенный логгер (`src/logger/logger.py`) для вывода информации о процессе работы, предупреждений и ошибок. Настройте уровень и формат логирования в файле логгера.

## Завершение Работы

Всегда закрывайте WebDriver после завершения работы для освобождения ресурсов:

```python
driver.quit()