# Модуль scenario.py: Сценарий для Казаринова

## Обзор

Модуль `scenario.py` предназначен для реализации сценариев сбора информации о товарах с различных веб-сайтов, их обработки с использованием AI и последующего формирования отчетов. Основной класс `Scenario` наследуется от `QuotationBuilder` и выполняет парсинг данных о продуктах, их обработку с помощью моделей AI и сохранение результатов.

## Подробней

Модуль содержит функции и классы для:

- Извлечения URL из OneTab.
- Сбора информации о товарах с использованием различных граберов.
- Обработки полученных данных с помощью AI для перевода и анализа.
- Создания отчетов на основе обработанных данных.

## Функции

### `fetch_target_urls_onetab`

```python
def fetch_target_urls_onetab(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """
    Функция паресит целевые URL из полученного OneTab.
    """
    ...
```

**Назначение**: Извлекает целевые URL, цену и имя из OneTab URL.

**Параметры**:
- `one_tab_url` (str): URL OneTab, содержащий целевые URL.

**Возвращает**:
- `tuple[str, str, list[str]] | bool`: Кортеж, содержащий цену (str), имя (str) и список URL (list[str]). Возвращает `False` в случае ошибки.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: Возникает при ошибках, связанных с HTTP-запросами.

**Как работает функция**:

1. Функция выполняет GET-запрос к указанному `one_tab_url`.
2. Извлекает все URL из HTML-контента, находя ссылки с классом `tabLink`.
3. Извлекает данные из элемента `div` с классом `tabGroupLabel`, разделяет их на цену и имя.
4. В случае ошибки логирует её и возвращает `False`.

```ascii
A --> B --> C --> D
│       │       │       │
GET     Парсинг  Обработка  Возврат
OneTab  HTML    данных   результата
```

Где:
- `GET OneTab`: Выполнение HTTP GET запроса к OneTab URL.
- `Парсинг HTML`: Извлечение URL и данных из HTML-контента.
- `Обработка данных`: Разделение извлеченных данных на цену и имя.
- `Возврат результата`: Возврат кортежа с ценой, именем и списком URL.

**Примеры**:
```python
one_tab_url = "http://example.com/onetab"
price, mexiron_name, urls = fetch_target_urls_onetab(one_tab_url)
if price and mexiron_name and urls:
    print(f"Цена: {price}, Имя: {mexiron_name}, URL: {urls}")
else:
    print("Не удалось извлечь данные из OneTab.")
```

## Классы

### `Scenario`

```python
class Scenario(QuotationBuilder):
    """Исполнитель сценария для Казаринова"""
    ...
```

**Описание**: Класс `Scenario` предназначен для выполнения сценариев сбора и обработки данных о товарах.

**Наследует**:
- `QuotationBuilder`: Класс, предоставляющий функциональность для создания коммерческих предложений.

**Методы**:

- `__init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None, **kwards)`
- `run_scenario_async(self, urls: List[str], price: Optional[str] = '', mexiron_name: Optional[str] = gs.now, bot: Optional[telebot.TeleBot] = None, chat_id: Optional[int] = 0, attempts: int = 3) -> bool`

#### `__init__`

```python
 def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None, **kwards):
        """Сценарий сбора информации."""
        ...
```

**Описание**: Инициализирует экземпляр класса `Scenario`.

**Параметры**:
- `mexiron_name` (Optional[str]): Имя Mexiron. По умолчанию `gs.now`.
- `driver` (Optional[Firefox | Playwrid | str]): Экземпляр веб-драйвера. По умолчанию `None`.
- `**kwards`: Дополнительные аргументы.

**Как работает функция**:
1. Если `window_mode` нет в `kwards`, устанавливает `window_mode` в `normal`.
2. Инициализирует драйвер `Driver` с использованием `Firefox`, если `driver` не передан.
3. Вызывает конструктор родительского класса `QuotationBuilder`.

#### `run_scenario_async`

```python
async def run_scenario_async(
        self,
        urls: List[str],  
        price: Optional[str] = '',
        mexiron_name: Optional[str] = gs.now, 
        bot: Optional[telebot.TeleBot] = None,
        chat_id: Optional[int] = 0,
        attempts: int = 3,
    ) -> bool:
        """
        Executes the scenario: parses products, processes them via AI, and stores data.
        """
        ...
```

**Описание**: Выполняет основной сценарий: парсит продукты, обрабатывает их с помощью AI и сохраняет данные.

**Параметры**:
- `urls` (List[str]): Список URL для парсинга.
- `price` (Optional[str]): Цена. По умолчанию ''.
- `mexiron_name` (Optional[str]): Имя Mexiron. По умолчанию `gs.now`.
- `bot` (Optional[telebot.TeleBot]): Экземпляр Telegram бота. По умолчанию `None`.
- `chat_id` (Optional[int]): ID чата Telegram. По умолчанию 0.
- `attempts` (int): Количество попыток. По умолчанию 3.

**Возвращает**:
- `bool`: `True` в случае успешного завершения, `False` в случае ошибки.

**Как работает функция**:

1. Инициализирует список `products_list` для хранения данных о продуктах.
2. Итерируется по списку URL, собирая данные о товарах с использованием граберов.
3. Обрабатывает собранные данные с помощью AI для перевода на разные языки.
4. Создает отчеты на основе обработанных данных и сохраняет их.
5. В случае ошибки логирует её и отправляет сообщение в Telegram (если указан бот).

```ascii
A --> B --> C --> D --> E
│       │       │       │       │
Сбор    AI      Создание  Сохранение  Отправка
товаров Обработка  отчетов Данных   сообщений
```

Где:
- `Сбор товаров`: Сбор данных о товарах с использованием граберов.
- `AI Обработка`: Обработка данных с использованием AI для перевода на разные языки.
- `Создание отчетов`: Создание отчетов на основе обработанных данных.
- `Сохранение Данных`: Сохранение данных в файлы.
- `Отправка сообщений`: Отправка сообщений в Telegram (если указан бот).

**Примеры**:
```python
urls = ["http://example.com/product1", "http://example.com/product2"]
scenario = Scenario()
asyncio.run(scenario.run_scenario_async(urls=urls, mexiron_name="TestScenario"))
```

## Функции

### `run_sample_scenario`

```python
def run_sample_scenario():
    """"""
    ...
```

**Назначение**: Запускает пример сценария с предопределенным списком URL.

**Как работает функция**:

1. Определяет список URL `urls_list`.
2. Создает экземпляр класса `Scenario` с `window_mode = 'headless'`.
3. Запускает асинхронно метод `run_scenario_async` с заданными URL и именем сценария.

**Примеры**:
```python
run_sample_scenario()