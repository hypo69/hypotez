# Модуль `scenario`

## Обзор

Модуль `scenario` предназначен для реализации сценариев сбора и обработки данных о товарах с различных сайтов, их последующей обработки с использованием AI и генерации отчетов. Он включает в себя функции для извлечения URL из OneTab, запуска сценариев сбора данных, AI-обработки и создания отчетов.

## Подробней

Модуль `scenario` является ключевым компонентом для автоматизации процесса сбора информации о товарах, их анализа и подготовки отчетов. Он использует различные классы и функции для взаимодействия с веб-сайтами, AI-моделями и инструментами генерации отчетов. Сценарии выполняются для конкретного пользователя (Казаринова) и интегрированы с Telegram ботом для уведомлений.

## Функции

### `fetch_target_urls_onetab`

```python
def fetch_target_urls_onetab(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """
    Функция паресит целевые URL из полученного OneTab.

    Args:
        one_tab_url (str): URL OneTab.

    Returns:
        tuple[str, str, list[str]] | bool: Кортеж, содержащий цену, имя Mexiron и список URL, или False в случае ошибки.
    """
    ...
```

**Назначение**: Извлекает целевые URL, цену и имя из OneTab URL.

**Параметры**:
- `one_tab_url` (str): URL OneTab.

**Возвращает**:
- `tuple[str, str, list[str]] | bool`: Кортеж, содержащий цену (str), имя Mexiron (str) и список URL (list[str]), или False, если произошла ошибка.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: Если возникает ошибка при выполнении HTTP-запроса.

**Как работает функция**:
- Функция отправляет GET-запрос к указанному OneTab URL.
- Использует BeautifulSoup для парсинга HTML-контента.
- Извлекает ссылки из элементов `<a>` с классом `tabLink`.
- Извлекает цену и имя из элемента `<div>` с классом `tabGroupLabel`.
- В случае ошибки логирует исключение и возвращает `False, False, False`.

**Примеры**:
```python
one_tab_url = "https://www.one-tab.com/..."
price, mexiron_name, urls = fetch_target_urls_onetab(one_tab_url)
if urls:
    print(f"Цена: {price}, Имя: {mexiron_name}, URL: {urls}")
```

## Классы

### `Scenario`

```python
class Scenario(QuotationBuilder):
    """Исполнитель сценария для Казаринова"""

    def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None, **kwards):
        """Сценарий сбора информации."""
        ...
```

**Описание**: Класс `Scenario` является исполнителем сценариев для сбора и обработки информации о товарах.

**Наследует**: `QuotationBuilder`

**Атрибуты**:
- `driver`: Инстанс веб-драйвера для управления браузером.
- `mexiron_name`: Имя Mexiron, используемое в сценарии.

**Параметры**:
- `mexiron_name` (Optional[str]): Имя Mexiron. По умолчанию `gs.now`.
- `driver` (Optional[Firefox | Playwrid | str]): Инстанс веб-драйвера. По умолчанию `None`.
- `kwards`: Дополнительные параметры конфигурации.

**Принцип работы**:
- Класс инициализирует веб-драйвер и вызывает конструктор родительского класса `QuotationBuilder`.
- Веб-драйвер используется для навигации по сайтам и сбора данных.

**Методы**:

### `run_scenario_async`

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

**Назначение**: Запускает сценарий сбора данных, AI-обработки и генерации отчетов.

**Параметры**:
- `urls` (List[str]): Список URL для сбора данных.
- `price` (Optional[str]): Цена. По умолчанию ''.
- `mexiron_name` (Optional[str]): Имя Mexiron. По умолчанию `gs.now`.
- `bot` (Optional[telebot.TeleBot]): Инстанс Telegram бота для отправки уведомлений. По умолчанию `None`.
- `chat_id` (Optional[int]): ID чата Telegram для отправки уведомлений. По умолчанию 0.
- `attempts` (int): Количество попыток выполнения сценария. По умолчанию 3.

**Возвращает**:
- `bool`: True, если сценарий выполнен успешно, иначе False.

**Как работает функция**:
1. **Сбор товаров**:
   - Перебирает список URL.
   - Получает граббер для каждого URL с помощью `get_graber_by_supplier_url`.
   - Собирает поля товара с использованием граббера.
   - Преобразует и сохраняет данные о товаре.
2. **AI processing**:
   - Обрабатывает список товаров с использованием AI-модели `gemini`.
   - Переводит данные на языки `ru` и `he`.
3. **Report creating**:
   - Создает отчеты на основе обработанных данных.
   - Отправляет уведомления в Telegram (если указан бот).

**Примеры**:
```python
urls = ["https://example.com/product1", "https://example.com/product2"]
s = Scenario(window_mode='headless')
asyncio.run(s.run_scenario_async(urls=urls, mexiron_name='test_scenario'))
```

## Функции

### `run_sample_scenario`

```python
def run_sample_scenario():
    """"""
    ...
```

**Назначение**: Запускает пример сценария сбора данных.

**Параметры**: Отсутствуют.

**Как работает функция**:
- Определяет список URL.
- Создает экземпляр класса `Scenario` с параметром `window_mode='headless'`.
- Запускает сценарий с использованием `asyncio.run`.

**Примеры**:
```python
run_sample_scenario()