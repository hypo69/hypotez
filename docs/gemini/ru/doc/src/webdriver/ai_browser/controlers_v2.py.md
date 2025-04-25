# Модуль управления веб-браузером с использованием Selenium

## Обзор

Этот модуль предоставляет класс `BrowserController` для управления веб-браузером (Chrome) с использованием Selenium. 
Он предлагает методы для навигации, поиска, скрапинга и взаимодействия с веб-страницами.

## Подробней

Класс `BrowserController` предоставляет следующие возможности:

- **Инициализация:**
    - Запускает Chrome WebDriver в headless режиме (без графического интерфейса) по умолчанию для автоматизации.
    - Настраивает опции Chrome WebDriver, включая размер окна и отключение песочницы.
- **Проверка драйвера:**
    - Проверяет, был ли драйвер успешно инициализирован.
- **Поиск в Интернете:**
    - Выполняет поиск в указанной поисковой системе (по умолчанию Google) по заданному запросу.
    - Ищет поле поиска на странице (пробует разные селекторы CSS).
    - Вводит запрос, нажимает Enter и ждет загрузки результатов поиска.
    - Извлекает текст с результатами поиска и возвращает его.

## Классы

### `BrowserController`

**Описание**: Класс для управления веб-браузером (Chrome) с использованием Selenium. Предоставляет методы для навигации, поиска, скрапинга и взаимодействия.

**Атрибуты**:

- `driver (Optional[webdriver.Chrome]):`  Экземпляр WebDriver для Chrome. Инициализируется в конструкторе.

**Методы**:

- `__init__(self, headless: bool = True)`:
    - Инициализирует WebDriver для Chrome.
    - Принимает аргумент `headless` (по умолчанию `True`), чтобы запускать браузер в headless режиме.
- `_check_driver(self) -> bool`:
    - Проверяет, был ли драйвер успешно инициализирован.
    - Возвращает `True`, если драйвер доступен, иначе `False`.
- `search(self, query: str, search_engine_url: str = "https://www.google.com") -> str`:
    - Выполняет поиск в указанной поисковой системе.
    - Принимает запрос `query` и URL поисковой системы `search_engine_url` (по умолчанию Google).
    - Возвращает текст с результатами поиска, ограниченный 2500 символами.

## Методы класса

### `__init__`

```python
    def __init__(self, headless: bool = True):
        """
        Инициализирует WebDriver для Chrome.

        Args:
            headless (bool): Запускать ли браузер в "безголовом" режиме (без GUI).
                             True по умолчанию для автоматизации.
        """
        self.driver: Optional[webdriver.Chrome] = None
        options = ChromeOptions()
        if headless:
            logger.info("Настройка Chrome для запуска в headless режиме.")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu") # Часто нужен для headless
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("user-agent=Mozilla/5.0...") # Пример User Agent

        try:
            logger.info("Инициализация Chrome WebDriver...")
            # WebDriverManager автоматически скачает/обновит драйвер
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("Chrome WebDriver успешно инициализирован.")
        except WebDriverException as ex:
             # Используем ваш формат логгера
             logger.error("Критическая ошибка: Не удалось инициализировать Chrome WebDriver.", ex, exc_info=True)
        except Exception as ex:
             logger.error("Неожиданная ошибка при инициализации Chrome WebDriver.", ex, exc_info=True)
```

**Описание**:
- Инициализирует WebDriver для Chrome с помощью `webdriver.Chrome`.
- Запускает браузер в headless режиме (`headless=True`) по умолчанию.
- Устанавливает опции Chrome WebDriver, включая размер окна, отключение песочницы и другие настройки.
- Использует `ChromeDriverManager` для автоматической загрузки и обновления драйвера Chrome.
- Логирует действия с помощью `logger.info` и `logger.error` для отладки.

**Параметры**:

- `headless (bool)`:  Запускать ли браузер в headless режиме.

**Возвращает**:

- `None`.

### `_check_driver`

```python
    def _check_driver(self) -> bool:
        """ Проверяет, был ли драйвер успешно инициализирован. """
        if self.driver is None:
            # Используем ваш формат
            logger.error("Драйвер браузера не был инициализирован.", None, exc_info=False)
            return False
        return True
```

**Описание**:
- Проверяет, инициализирован ли драйвер браузера (`self.driver`).
- Если драйвер не инициализирован, выводит сообщение об ошибке в лог с помощью `logger.error`.
- Возвращает `True`, если драйвер доступен, иначе `False`.

**Параметры**:

- `None`.

**Возвращает**:

- `bool`: `True`, если драйвер доступен, иначе `False`.

### `search`

```python
    def search(self, query: str, search_engine_url: str = "https://www.google.com") -> str:
        """ Выполняет поиск в указанной поисковой системе. """
        if not self._check_driver(): return "Ошибка: Драйвер браузера недоступен."

        logger.info(f"[Browser Action] Поиск: \'{query}\' на {search_engine_url}")
        try:
            self.driver.get(search_engine_url)
            wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIMEOUT)
            # Ищем поле поиска (пробуем разные селекторы)
            search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name=\'q\'], input[name=\'q\']")))
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            # Ждем загрузки результатов
            wait.until(EC.presence_of_element_located((By.ID, "search")))
            # time.sleep(1) # Пауза не рекомендуется, лучше ждать конкретный элемент

            # Извлекаем текст с результатами
            results_text = self.driver.find_element(By.TAG_NAME, 'body').text
            max_len = 2500 # Ограничиваем длину
            if len(results_text) > max_len:
                logger.debug(f"Результаты поиска обрезаны до {max_len} символов.", exc_info=False)
                results_text = results_text[:max_len] + "..."

            return f"Результаты поиска по запросу \'{query}\':\\n{results_text}"

        except TimeoutException as ex:
             logger.error(f"Timeout",ex)
```

**Описание**:
- Проверяет, доступен ли драйвер браузера.
- Открывает указанную поисковую систему (`search_engine_url`).
- Использует `WebDriverWait` для ожидания появления поля поиска.
- Вводит запрос `query` в поле поиска.
- Нажимает Enter и ждет загрузки результатов поиска.
- Извлекает текст с результатами поиска и возвращает его, ограниченный 2500 символами.
- Логирует действия с помощью `logger.info`, `logger.debug` и `logger.error`.

**Параметры**:

- `query (str)`:  Поисковый запрос.
- `search_engine_url (str)`:  URL поисковой системы.

**Возвращает**:

- `str`: Текст с результатами поиска.

## Примеры

```python
# Создание инстанса класса
browser = BrowserController()

# Выполнение поиска в Google
results = browser.search("Как сделать сайт")
print(results)

# Закрытие браузера
browser.driver.quit()