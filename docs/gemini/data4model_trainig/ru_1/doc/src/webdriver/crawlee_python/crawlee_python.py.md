# Модуль `crawlee_python`

## Обзор

Модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee. Он позволяет настраивать параметры браузера, обрабатывать запросы и извлекать данные с веб-страниц.

## Подробней

Этот модуль позволяет создать кастомного краулера, использующего библиотеку Crawlee и Playwright для управления браузером. Он предоставляет возможность настройки различных параметров, таких как максимальное количество запросов, режим работы браузера (с графическим интерфейсом или без), тип используемого браузера (Chromium, Firefox, Webkit) и другие опции запуска браузера.

## Классы

### `CrawleePython`

**Описание**: Пользовательская реализация `PlaywrightCrawler` с использованием библиотеки Crawlee.

**Атрибуты**:
- `max_requests` (int): Максимальное количество запросов для выполнения во время обхода.
- `headless` (bool): Определяет, запускать ли браузер в режиме без графического интерфейса.
- `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
- `crawler` (PlaywrightCrawler): Экземпляр PlaywrightCrawler.
- `options` (Optional[List[str]]): Список дополнительных опций, передаваемых в браузер.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `CrawleePython`.
- `setup_crawler`: Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.
- `run_crawler`: Запускает обход веб-страниц с использованием `PlaywrightCrawler` и начального списка URL.
- `export_data`: Экспортирует весь набор данных в JSON-файл.
- `get_data`: Извлекает извлеченные данные.
- `run`: Основной метод для настройки, запуска обхода и экспорта данных.

#### `__init__`

```python
def __init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)
```

**Назначение**: Инициализирует класс `CrawleePython` с заданными параметрами.

**Параметры**:
- `max_requests` (int): Максимальное количество запросов для выполнения во время обхода. По умолчанию `5`.
- `headless` (bool): Определяет, запускать ли браузер в режиме без графического интерфейса. По умолчанию `False`.
- `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit'). По умолчанию `'firefox'`.
- `options` (Optional[List[str]]): Список дополнительных опций, передаваемых в браузер. По умолчанию `None`.

**Примеры**:
```python
crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium')
```

#### `setup_crawler`

```python
async def setup_crawler(self)
```

**Назначение**: Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.

Внутри этой функции определяется обработчик запросов по умолчанию (`request_handler`), который будет вызываться для каждой посещаемой страницы. Этот обработчик выполняет следующие действия:
- Логгирует информацию об обрабатываемом URL.
- Добавляет в очередь все ссылки, найденные на странице.
- Извлекает данные со страницы, используя API Playwright (например, заголовок и содержимое страницы).
- Помещает извлеченные данные в набор данных по умолчанию.

```python
@self.crawler.router.default_handler
async def request_handler(context: PlaywrightCrawlingContext) -> None:
    """
    Default request handler for processing web pages.

    :param context: The crawling context.
    :type context: PlaywrightCrawlingContext
    """
    context.log.info(f'Processing {context.request.url} ...')

    # Enqueue all links found on the page.
    await context.enqueue_links()

    # Extract data from the page using Playwright API.
    data = {
        'url': context.request.url,
        'title': await context.page.title(),
        'content': (await context.page.content())[:100],
    }

    # Push the extracted data to the default dataset.
    await context.push_data(data)
```

**Примеры**:
```python
await crawler.setup_crawler()
```

#### `run_crawler`

```python
async def run_crawler(self, urls: List[str])
```

**Назначение**: Запускает обход веб-страниц с использованием `PlaywrightCrawler` и начального списка URL.

**Параметры**:
- `urls` (List[str]): Список URL для начала обхода.

**Примеры**:
```python
await crawler.run_crawler(['https://www.example.com', 'https://www.example.org'])
```

#### `export_data`

```python
async def export_data(self, file_path: str)
```

**Назначение**: Экспортирует весь набор данных в JSON-файл.

**Параметры**:
- `file_path` (str): Путь для сохранения экспортированного JSON-файла.

**Примеры**:
```python
await crawler.export_data('data.json')
```

#### `get_data`

```python
async def get_data(self) -> Dict[str, Any]
```

**Назначение**: Извлекает извлеченные данные.

**Возвращает**:
- `Dict[str, Any]`: Извлеченные данные в виде словаря.

**Примеры**:
```python
data = await crawler.get_data()
print(data)
```

#### `run`

```python
async def run(self, urls: List[str])
```

**Назначение**: Основной метод для настройки, запуска обхода и экспорта данных.

**Параметры**:
- `urls` (List[str]): Список URL для начала обхода.

**Как работает функция**:
1. Вызывает метод `setup_crawler` для настройки краулера.
2. Вызывает метод `run_crawler` для запуска обхода веб-страниц.
3. Вызывает метод `export_data` для экспорта извлеченных данных в JSON-файл.
4. Получает извлеченные данные с помощью метода `get_data`.
5. Логгирует извлеченные данные.

**Примеры**:
```python
await crawler.run(['https://www.example.com'])
```

```python
if __name__ == '__main__':
    async def main():
        crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
        await crawler.run(['https://www.example.com'])

    asyncio.run(main())