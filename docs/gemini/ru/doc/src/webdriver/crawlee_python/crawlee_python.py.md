# Crawlee Python Crawler

## Обзор

Этот модуль предоставляет собственную реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee.  Позволяет настроить параметры браузера, обрабатывать запросы и извлекать данные с веб-страниц. 

##  Подробней

Модуль `CrawleePython` предназначен для сбора данных с веб-страниц. Он использует библиотеку Crawlee для создания и управления  PlaywrightCrawler. 

* **Crawlee**:  Библиотека для создания веб-краулеров, поддерживающая как Playwright, так и Puppeteer.
* **PlaywrightCrawler**:  Класс Crawlee, который позволяет легко взаимодействовать с браузером.
* **Playwright**:  Библиотека для автоматизации браузеров, позволяющая управлять браузером, взаимодействовать с веб-страницами, имитировать пользовательское поведение.


## Классы

### `CrawleePython`

**Описание**:  Класс, реализующий `PlaywrightCrawler` для сбора данных с веб-страниц.

**Атрибуты**:

* `max_requests` (int): Максимальное количество запросов, которые нужно выполнить во время сканирования.
* `headless` (bool): Запускать браузер в безголовом режиме (headless mode).
* `browser_type` (str): Тип браузера, который будет использоваться ('chromium', 'firefox', 'webkit').
* `crawler` (PlaywrightCrawler): Экземпляр `PlaywrightCrawler`.

**Методы**:

* `__init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)`: Инициализирует `CrawleePython` с указанными параметрами.
* `setup_crawler(self)`:  Настраивает экземпляр  `PlaywrightCrawler` с указанной конфигурацией.
* `request_handler(self, context: PlaywrightCrawlingContext)`: Обработчик по умолчанию для обработки веб-страниц.
* `run_crawler(self, urls: List[str])`: Запускает сканирование с начальным списком URL-адресов.
* `export_data(self, file_path: str)`: Экспортирует весь набор данных в файл JSON.
* `get_data(self)`: Возвращает извлеченные данные.
* `run(self, urls: List[str])`: Главный метод для настройки, запуска сканирования и экспорта данных.


## Функции

### `request_handler`

**Назначение**: Обработчик по умолчанию для обработки веб-страниц.

**Параметры**:

* `context` (PlaywrightCrawlingContext): Контекст сканирования.

**Как работает функция**:
* Записывает в лог информацию о том, что обрабатывается URL-адрес. 
*  Добавляет в очередь все ссылки, найденные на странице.
* Извлекает данные со страницы с использованием API Playwright.
*  Отправляет извлеченные данные в набор данных по умолчанию.


##  Примеры

```python
# Пример использования
if __name__ == '__main__':
    async def main():
        crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
        await crawler.run(['https://www.example.com'])

    asyncio.run(main())
```

**Пример работы с данными:**

```python
# Импорт библиотеки для работы с CSV
import csv

# Открытие файла CSV на чтение
with open('results.csv', 'r', newline='', encoding='utf-8') as csvfile:
    # Создание объекта для чтения CSV-файла
    reader = csv.DictReader(csvfile)
    # Проход по строкам CSV-файла
    for row in reader:
        # Вывод данных из каждой строки
        print(f'URL: {row["url"]}')
        print(f'Title: {row["title"]}')
        print(f'Content: {row["content"]}\n')