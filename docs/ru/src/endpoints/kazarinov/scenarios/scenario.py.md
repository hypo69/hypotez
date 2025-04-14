# Модуль: Сценарий для Казаринова

## Обзор

Модуль `scenario.py` предназначен для выполнения сценариев сбора информации о товарах, их обработки с использованием AI и формирования отчетов. Основной класс `Scenario` наследуется от `QuotationBuilder` и использует веб-скрапинг, AI-обработку и генерацию отчетов для создания ценовых предложений.

## Подробнее

Этот модуль является частью проекта `hypotez` и отвечает за автоматизацию процесса сбора данных о товарах с различных веб-сайтов, их анализ с помощью AI-моделей (например, Google Gemini) и формирование отчетов. Он включает в себя функции для парсинга веб-страниц, извлечения информации о товарах, перевода данных на разные языки и создания отчетов в формате JSON. Модуль также интегрирован с Telegram ботом для уведомления о ходе выполнения сценария.

## Функции

### `fetch_target_urls_onetab`

```python
def fetch_target_urls_onetab(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """
    Функция паресит целевые URL из полученного OneTab.
    """
```

**Назначение**: Извлекает целевые URL, цену и название из OneTab URL.

**Параметры**:

-   `one_tab_url` (str): URL OneTab страницы.

**Возвращает**:

-   `tuple[str, str, list[str]] | bool`: Кортеж, содержащий цену, название и список URL, или `False` в случае ошибки.

**Вызывает исключения**:

-   `requests.exceptions.RequestException`: При ошибке выполнения HTTP-запроса.

**Как работает функция**:

1.  Выполняет HTTP-запрос к указанному OneTab URL.
2.  Использует `BeautifulSoup` для парсинга HTML-содержимого страницы.
3.  Извлекает все URL-адреса, находящиеся в элементах `<a>` с классом `tabLink`.
4.  Извлекает данные из элемента `<div>` с классом `tabGroupLabel`, разделяя их на цену и название.
5.  Возвращает цену, название и список URL. В случае ошибки возвращает `False`.

**ASCII flowchart**:

```
A: HTTP-запрос к OneTab URL
|
B: Парсинг HTML с BeautifulSoup
|
C: Извлечение URL, цены и названия
|
D: Возврат цены, названия и списка URL
```

**Примеры**:

```python
one_tab_url = "https://www.one-tab.com/..."
price, mexiron_name, urls = fetch_target_urls_onetab(one_tab_url)
if urls:
    print(f"Цена: {price}, Название: {mexiron_name}, URL: {urls[0]}")
else:
    print("Не удалось получить данные из OneTab URL.")
```

## Классы

### `Scenario`

```python
class Scenario(QuotationBuilder):
    """Исполнитель сценария для Казаринова"""
```

**Описание**: Класс `Scenario` предназначен для выполнения сценариев сбора информации о товарах, их обработки с использованием AI и формирования отчетов.

**Наследует**:

-   `QuotationBuilder`: Класс, предоставляющий функциональность для создания ценовых предложений.

**Методы**:

-   `__init__`: Инициализирует экземпляр класса `Scenario`.
-   `run_scenario_async`: Выполняет основной сценарий: парсит продукты, обрабатывает их через AI и сохраняет данные.

### `Scenario.__init__`

```python
    def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None, **kwards):
        """Сценарий сбора информации."""
```

**Назначение**: Инициализирует экземпляр класса `Scenario`.

**Параметры**:

-   `mexiron_name` (Optional[str]): Имя Mexiron. По умолчанию `gs.now`.
-   `driver` (Optional[Firefox | Playwrid | str]): Экземпляр драйвера веб-браузера. По умолчанию `None`.
-   `**kwards`: Дополнительные параметры конфигурации.

**Как работает конструктор**:

1.  Устанавливает режим окна в значение 'normal', если он не указан в параметрах `kwards`.
2.  Создает экземпляр драйвера `Driver` с использованием `Firefox` и переданных параметров `kwards`, если драйвер не был передан явно.
3.  Вызывает конструктор родительского класса `QuotationBuilder` с переданными параметрами.

**Примеры**:

```python
s = Scenario(mexiron_name="test", window_mode="headless")
```

### `Scenario.run_scenario_async`

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
```

**Назначение**: Выполняет основной сценарий: парсит продукты, обрабатывает их через AI и сохраняет данные.

**Параметры**:

-   `urls` (List[str]): Список URL для парсинга.
-   `price` (Optional[str]): Цена. По умолчанию ''.
-   `mexiron_name` (Optional[str]): Имя Mexiron. По умолчанию `gs.now`.
-   `bot` (Optional[telebot.TeleBot]): Экземпляр Telegram бота для отправки уведомлений. По умолчанию `None`.
-   `chat_id` (Optional[int]): ID чата Telegram для отправки уведомлений. По умолчанию `0`.
-   `attempts` (int): Количество попыток выполнения парсинга. По умолчанию `3`.

**Возвращает**:

-   `bool`: `True`, если сценарий выполнен успешно, иначе `False`.

**Как работает функция**:

1.  Инициализирует пустой список `products_list` для хранения данных о товарах.
2.  Перебирает список URL-адресов для парсинга.
3.  Для каждого URL определяет граббер с помощью `get_graber_by_supplier_url`.
4.  Если граббер не найден, логирует ошибку и отправляет уведомление в Telegram (если бот указан).
5.  Вызывает метод `grab_page_async` граббера для извлечения полей товара.
6.  Если происходит ошибка при получении полей товара, логирует ошибку и отправляет уведомление в Telegram.
7.  Преобразует полученные поля товара с помощью `convert_product_fields`.
8.  Сохраняет данные о товаре с помощью `save_product_data`.
9.  После сбора данных о товарах выполняет AI-обработку для каждого языка в списке `langs_list` (he, ru).
10. Отправляет уведомление в Telegram о начале AI-обработки.
11. Вызывает метод `process_llm_async` для обработки данных с использованием AI.
12. Если AI-обработка завершается с ошибкой, логирует ошибку и отправляет уведомление в Telegram.
13. После успешной AI-обработки создает отчет с помощью `ReportGenerator`.
14. Сохраняет данные в формате JSON и создает отчеты в формате DOCX (если указано).
15. Возвращает `True` после успешного завершения сценария.

**ASCII flowchart**:

```
A: Инициализация products_list
|
B: Перебор URL из списка urls
|
C: Определение граббера для URL
|
D: Извлечение полей товара с помощью grab_page_async
|
E: Преобразование полей товара
|
F: Сохранение данных о товаре
|
G: AI-обработка для каждого языка
|
H: Создание отчета с помощью ReportGenerator
|
I: Сохранение данных в формате JSON
|
J: Возврат True
```

**Примеры**:

```python
urls_list = ["https://www.example.com/product1", "https://www.example.com/product2"]
s = Scenario(window_mode="headless")
asyncio.run(s.run_scenario_async(urls=urls_list, mexiron_name="test_scenario"))
```

## Функции

### `run_sample_scenario`

```python
def run_sample_scenario():
    """"""
```

**Назначение**: Запускает пример сценария.

**Как работает функция**:

1.  Создает список URL-адресов `urls_list` для демонстрации.
2.  Создает экземпляр класса `Scenario` с параметром `window_mode` установленным в `headless`.
3.  Запускает асинхронный сценарий `run_scenario_async` с использованием `asyncio.run`, передавая список URL-адресов и имя сценария.

**Примеры**:

```python
run_sample_scenario()