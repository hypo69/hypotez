# Модуль для управления веб-браузером

## Обзор

Модуль `browser_use.py` предоставляет класс `BrowserController` для управления веб-браузером (Chrome) с использованием Selenium. 
Он включает методы для навигации, поиска, скрапинга и взаимодействия с веб-страницами.

## Подробнее

`BrowserController` использует `Driver` из `src.webdriver` для инициализации веб-драйвера. 
В данном случае используется Firefox. 
Дополнительные параметры, такие как `window_mode`, позволяющие управлять отображением окна браузера (например, 'normal' для стандартного режима, 'fullscreen' для полноэкранного). 
В `BrowserController` реализована функция `search` для поиска в Google. 
Функция выполняет поиск по заданному запросу, затем извлекает текст с результатами поиска. 
Длина результатов ограничена 2500 символами.

## Классы

### `BrowserController`

**Описание**: Класс для управления веб-браузером (Chrome) с использованием Selenium. 
Предоставляет методы для навигации, поиска, скрапинга и взаимодействия.

**Атрибуты**:

- `driver` (Driver): Экземпляр класса Driver, представляющий веб-драйвер.

**Методы**:

- `__init__(self, window_mode:str =\'normal\')`: Инициализирует WebDriver для Firefox.
- `_check_driver(self) -> bool`: Проверяет, был ли драйвер успешно инициализирован. 
- `search(self, query: str, search_engine_url: str = "https://www.google.com") -> str`: Выполняет поиск в указанной поисковой системе.

## Методы класса

### `__init__`

```python
    def __init__(self, window_mode:str =\'normal\'):
        """
        Инициализирует WebDriver для Firefox.

        Args:
            window_mode (str): Режим отображения окна браузера. 
                             Например, 'normal' для стандартного режима, 'fullscreen' для полноэкранного. По умолчанию 'normal'.

        """
        self.driver = Driver(Firefox(window_mode = window_mode))
```
Инициализирует экземпляр класса `BrowserController`. 
Создает экземпляр `Driver` с `Firefox` как драйвером. 
Инициализирует Firefox в заданном режиме отображения окна браузера.


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
Проверяет, был ли веб-драйвер успешно инициализирован. 
Если драйвер не был инициализирован, выводится сообщение об ошибке с помощью `logger.error`.

### `search`

```python
    def search(self, query: str, search_engine_url: str = "https://www.google.com") -> str:
        """ Выполняет поиск в указанной поисковой системе. 

        Args:
            query (str): Текст поискового запроса.
            search_engine_url (str): URL поисковой системы. По умолчанию - Google.

        Returns:
            str: Текст с результатами поиска или сообщение об ошибке.

        """
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
Выполняет поиск в заданной поисковой системе по заданному запросу. 
Открывает страницу поисковой системы, вводит поисковый запрос в поле поиска, 
ждет загрузки результатов поиска и извлекает текст с результатами. 
Длина результатов поиска ограничивается 2500 символами.
 
**Параметры**:

- `query` (str): Текст поискового запроса.
- `search_engine_url` (str): URL поисковой системы. По умолчанию - Google.

**Возвращает**:

- `str`: Текст с результатами поиска или сообщение об ошибке.
 
**Вызывает исключения**:

- `TimeoutException`: Если время ожидания истекло во время поиска элемента или загрузки результатов.

**Пример**:
```python
# Инициализация веб-драйвера
driver = BrowserController()

# Выполнение поиска в Google по запросу "python"
results = driver.search(query="python", search_engine_url="https://www.google.com")

# Вывод результатов поиска
print(results)