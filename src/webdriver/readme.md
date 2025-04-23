# Модуль `webdriver`

## Описание

Модуль `webdriver` предоставляет унифицированный и расширенный интерфейс для работы с веб-драйверами Selenium (в данном примере, с фокусом на Firefox), упрощая автоматизацию взаимодействия с веб-страницами.

Он включает в себя:

1.  **Инициализацию и конфигурацию драйвера:** Гибкая настройка параметров запуска браузера (Firefox), включая пути к исполняемым файлам, использование профилей, опции запуска (например, kiosk, headless), настройку User-Agent и работу с прокси.
2.  **Взаимодействие с элементами:** Мощный механизм (`ExecuteLocator`) для поиска элементов на странице по различным стратегиям (CSS-селекторы, XPath, ID и т.д.) и выполнения с ними действий (клик, ввод текста, получение атрибутов, создание скриншотов элемента). Поддерживает сложные сценарии с ожиданием элементов и обработкой списков.
3.  **Выполнение JavaScript:** Утилиты (`JavaScript`) для выполнения типовых JS-скриптов на странице (например, проверка `readyState`, получение языка страницы, изменение видимости DOM-элементов, установка фокуса на окно).
4.  **Управление прокси:** Функциональность (`proxy.py`) для загрузки списков прокси с удаленного источника, их парсинга и проверки работоспособности. Интегрировано с настройкой драйвера Firefox.
5.  **Вспомогательные методы:** Удобные методы для общих задач, таких как навигация (`get_url`), прокрутка страницы (`scroll`), ожидание (`wait`), получение HTML-кода (`fetch_html`).

## Структура модуля

*   `/src/webdriver/`
    *   `driver.py`: Содержит базовый класс `Driver` (хотя в примере используется прямое наследование от `selenium.webdriver.Firefox`), определяющий общие методы взаимодействия с драйвером (`get_url`, `scroll`, `wait`, `fetch_html`, `locale` и др.).
    *   `firefox/`
        *   `firefox.py`: Реализация класса `Firefox`, наследующегося от `selenium.webdriver.Firefox`. Отвечает за инициализацию GeckoDriver, настройку опций, профиля, прокси для Firefox и "внедрение" (`_payload`) методов из `ExecuteLocator` и `JavaScript` в экземпляр драйвера.
        *   `firefox.json`: Файл конфигурации для драйвера Firefox.
    *   `js.py`: Класс `JavaScript` с методами для выполнения JS-скриптов.
    *   `executor.py`: Класс `ExecuteLocator` для поиска элементов и выполнения действий над ними на основе словарей-локаторов. Использует `asyncio` для некоторых операций.
    *   `proxy.py`: Функции для работы с прокси-серверами.
    *   `proxies.txt`: (Автоматически создаваемый/обновляемый) Файл для хранения списка прокси.

## Установка зависимостей

Перед использованием убедитесь, что установлены необходимые библиотеки:

```bash
pip install selenium requests fake-useragent
```

Также необходимо иметь установленный браузер Firefox и соответствующий ему GeckoDriver. Пути к ним указываются в конфигурационном файле.

## Конфигурация (`firefox.json`)

Настройка драйвера Firefox производится через файл `/src/webdriver/firefox/firefox.json`.

```json
{
  "options": [], // Дополнительные аргументы командной строки для Firefox (например, "--private")
  "disabled_options": [ "--kiosk", "--headless" ], // Опции, которые временно отключены (для информации)
  "profile_directory": {
    // Путь к профилю Firefox
    "os": "%LOCALAPPDATA%\\Mozilla\\Firefox\\Profiles\\95c5aq3n.default-release", // Путь к системному профилю (Windows)
    "internal": "webdriver\\firefox\\profiles\\95c5aq3n.default-release", // Путь к профилю внутри проекта
    "default": "os" // Какой профиль использовать по умолчанию ("os" или "internal")
                     // Можно также указать имя конкретного профиля при создании экземпляра Firefox(profile_name="...")
  },
  "executable_path": {
    // Пути к исполняемым файлам
    "firefox_binary": "bin\\webdrivers\\firefox\\ff\\core-127.0.2\\firefox.exe", // Путь к firefox.exe
    "geckodriver": "bin\\webdrivers\\firefox\\gecko\\33\\geckodriver.exe" // Путь к geckodriver.exe
  },
  "headers": {
    // Заголовки, которые будут установлены через preference (не прямые HTTP-заголовки запроса)
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ...", // Переопределение User-Agent
    "Accept": "text/html...",
    // ... другие заголовки
    "Connection": "keep-alive"
  },
  "proxy_enabled": false, // Включить/выключить использование прокси (true/false)
                          // Если true, модуль попытается загрузить, проверить и установить рабочий SOCKS4/SOCKS5 прокси
  "window_mode": null // Режим окна: null (обычный), "kiosk", "headless" и т.д.
                      // Можно переопределить при создании экземпляра Firefox(window_mode="...")
}
```

**Важно:** Пути в `executable_path` и `profile_directory` указаны относительно корня проекта (определяемого `header.__root__` или `gs.path.root`). Переменная `%LOCALAPPDATA%` будет автоматически заменена на соответствующий путь в Windows.

## Использование

### 1. Инициализация драйвера Firefox

```python
import asyncio
from pathlib import Path
from types import SimpleNamespace

# Предполагается, что структура проекта настроена и gs/header доступны
# import header
# from src import gs
from src.webdriver.firefox import Firefox
from src.logger.logger import logger # Используется для логирования

# Инициализация драйвера с использованием настроек из firefox.json
# Можно переопределить некоторые параметры при инициализации:
try:
    # Пример с указанием режима киоска
    driver = Firefox(window_mode="kiosk", profile_name="my_custom_profile")
    # Или просто использовать настройки по умолчанию из JSON
    # driver = Firefox()
    logger.info("Драйвер Firefox успешно запущен.")
except Exception as e:
    logger.critical(f"Не удалось инициализировать драйвер Firefox: {e}")
    # Выход или дальнейшая обработка ошибки
    exit()

# Теперь экземпляр 'driver' содержит как стандартные методы Selenium,
# так и добавленные методы из JavaScript и ExecuteLocator.
```

### 2. Навигация и базовые действия

```python
# Переход по URL
if driver.get_url("https://www.google.com"):
    logger.info(f"Успешно перешли на {driver.current_url}")
    # Ожидание загрузки (проверка document.readyState) уже встроено в get_url

    # Явное ожидание (если нужно)
    driver.wait(1.5) # Ожидание 1.5 секунды

    # Прокрутка страницы
    driver.scroll(scrolls=2, direction='down', delay=0.5) # Прокрутить 2 раза вниз с задержкой 0.5с

    # Получение языка страницы
    lang = driver.get_page_lang()
    logger.info(f"Язык страницы: {lang}") # Использует JavaScript

    # Получение referrer
    referrer = driver.get_referrer()
    logger.info(f"Referrer: {referrer}") # Использует JavaScript

else:
    logger.error("Не удалось загрузить страницу.")

# Получение HTML-кода текущей страницы
html = driver.fetch_html() # Вернет driver.page_source после успешного get_url
if html:
    logger.info(f"Получено {len(html)} байт HTML.")

# Получение HTML из локального файла
# local_file_path = Path("path/to/your/file.html").absolute()
# file_uri = local_file_path.as_uri() # Преобразует путь в file:///...
# html_local = driver.fetch_html(file_uri)
# if html_local:
#    logger.info(f"HTML из файла: {html_local[:100]}...")


```

### 3. Взаимодействие с элементами через `ExecuteLocator`

`ExecuteLocator` позволяет выполнять действия над элементами, используя словари или `SimpleNamespace` для описания локатора и действия.

```python
# Пример словаря-локатора для кнопки поиска Google
search_button_locator = {
    "locator_description": "Кнопка 'Поиск в Google'", # Описание для логов
    "by": "xpath",
    "selector": "(//input[@name='btnK'])[2]", # Селектор элемента
    "event": "click()", # Действие: клик
    "attribute": None, # Атрибут не получаем
    "if_list": "first", # Если найдено несколько, взять первый
    "mandatory": True, # Локатор обязателен, ошибка если не найден
    "timeout": 5 # Таймаут ожидания элемента (секунды)
}

# Локатор для поля ввода
search_input_locator = SimpleNamespace(
    locator_description="Поле ввода поиска",
    by="css selector",
    selector="textarea[name='q']",
    event="type(Мой поисковый запрос)", # Действие: ввести текст
    # event="clear();type(Мой запрос);send_keys(ENTER)", # Можно комбинировать события через ';'
    attribute=None,
    if_list="first",
    mandatory=True,
    timeout=5
)

# Локатор для получения атрибута (например, значение value)
some_value_locator = {
    "locator_description": "Получение значения value у кнопки",
    "by": "xpath",
    "selector": "(//input[@name='btnK'])[2]",
    "event": None, # Действия нет
    "attribute": "value", # Получить значение атрибута 'value'
    "if_list": "first",
    "mandatory": False, # Необязательный локатор
    "timeout": 3
}

# Локатор для получения текста всех ссылок в результатах
# (пример гипотетический, селектор может отличаться)
results_links_locator = {
    "locator_description": "Ссылки результатов поиска",
    "by": "css selector",
    "selector": "div.g a h3", # Примерный селектор заголовков ссылок
    "event": None,
    "attribute": "textContent", # Получить текстовое содержимое
    "if_list": "all", # Получить все найденные элементы
    "mandatory": False,
    "timeout": 10,
    "timeout_for_event": "visibility_of_all_elements_located" # Ожидать видимости всех элементов
}

# --- Выполнение локаторов ---
# Используем asyncio.run или существующий event loop для async функций

async def main_interaction():
    try:
        # 1. Ввести текст в поле поиска
        success_input = await driver.execute_locator(search_input_locator, typing_speed=0.05) # Медленный ввод
        if success_input:
            logger.info("Текст успешно введен.")
            await asyncio.sleep(1) # Небольшая пауза

            # 2. Кликнуть по кнопке поиска
            success_click = await driver.execute_locator(search_button_locator)
            if success_click:
                logger.info("Клик по кнопке выполнен.")
                await asyncio.sleep(2) # Пауза для загрузки результатов

                # 3. Получить значение атрибута
                button_value = await driver.execute_locator(some_value_locator)
                if button_value:
                    logger.info(f"Значение атрибута 'value' кнопки: {button_value}")

                # 4. Получить тексты всех ссылок
                link_texts = await driver.execute_locator(results_links_locator)
                if link_texts:
                    logger.info("Найдены тексты ссылок:")
                    for i, text in enumerate(link_texts):
                        logger.info(f"  {i+1}: {text}")
                else:
                    logger.warning("Ссылки результатов не найдены.")

            else:
                logger.error("Не удалось кликнуть по кнопке.")
        else:
            logger.error("Не удалось ввести текст.")

    except Exception as e:
        logger.error(f"Ошибка во время взаимодействия: {e}")

# Запуск асинхронной функции
# asyncio.run(main_interaction()) # В реальном коде

# --- Дополнительные возможности ExecuteLocator ---

# Получение WebElement (если event и attribute не указаны)
async def get_element():
     element = await driver.get_webelement_by_locator(search_input_locator)
     if element:
         logger.info(f"WebElement найден: {element.tag_name}")
         # Сделать элемент видимым (если он скрыт стилями)
         driver.unhide_DOM_element(element)
         logger.info("Попытка сделать элемент видимым (JS).")

         # Скриншот конкретного элемента
         screenshot_bytes = await driver.get_webelement_as_screenshot(search_input_locator)
         if screenshot_bytes:
             with open("element_screenshot.png", "wb") as f:
                 f.write(screenshot_bytes)
             logger.info("Скриншот элемента сохранен в element_screenshot.png")

# asyncio.run(get_element()) # В реальном коде

# Отправка сообщения с эмуляцией Shift+Enter (если нужно)
message_locator = search_input_locator # Используем тот же локатор поля ввода
# message_locator.event = None # Убираем предыдущее событие type
async def send_complex_message():
    message = "Первая строка;Вторая строка после переноса"
    success = await driver.send_message(message_locator, message=message, typing_speed=0.02)
    if success:
        logger.info("Сообщение с переносом строки отправлено.")

# asyncio.run(send_complex_message()) # В реальном коде

```

### 4. Завершение работы

```python
# Закрыть браузер и завершить сессию WebDriver
driver.quit()
logger.info("Драйвер Firefox закрыт.")
```

## Логирование

Модуль активно использует логгер, настроенный в `/src/logger/logger.py`. Уровень логирования и формат вывода можно настроить там же. Ошибки выполнения, таймауты и важные шаги протоколируются для облегчения отладки.

## Работа с прокси

Если в `firefox.json` установлено `"proxy_enabled": true`, то при инициализации `Firefox()`:

1.  Вызывается `download_proxies_list()` для загрузки/обновления `proxies.txt` с URL, указанного в `proxy.py`.
2.  Вызывается `get_proxies_dict()` для парсинга `proxies.txt`.
3.  Модуль перебирает случайные прокси SOCKS4/SOCKS5 из списка.
4.  Для каждого прокси вызывается `check_proxy()`, которая пытается сделать запрос через него.
5.  Первый успешно проверенный прокси устанавливается в настройках Firefox через `options.set_preference`.
6.  Если рабочий прокси не найден, выводится предупреждение в лог.
