# Сценарий для Казаринова

## Обзор

Модуль содержит класс `Scenario`, реализующий сценарий для Казаринова. Он использует WebDriver, Google Generative AI (Gemini) и другие инструменты для сбора, обработки и создания отчетов о товарах.

## Детали

Модуль реализует сценарий для сбора информации о товарах, их обработки с помощью AI и создания отчетов. Сценарий использует WebDriver для сбора данных с веб-сайтов, Google Generative AI для обработки текстов и создания описаний на разных языках, а также ReportGenerator для создания отчетов в формате JSON и DOCX.

## Классы

### `class Config`

**Описание**: Класс конфигурации для сценария Казаринова.

**Атрибуты**:

- `ENDPOINT:str`: Название конечной точки для сценария, по умолчанию "kazarinov".

### `class Scenario(QuotationBuilder)`

**Описание**: Класс, реализующий сценарий для Казаринова. 
**Inherits**:  Наследуется от `QuotationBuilder`.

**Атрибуты**:

- `driver:Optional[Firefox | Playwrid | str]`:  Экземпляр WebDriver, по умолчанию Firefox.
- `mexiron_name:Optional[str]`: Имя мексирончика, по умолчанию `gs.now`.

**Методы**:

- `__init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None, **kwargs)`: 
    **Описание**: Инициализирует экземпляр класса `Scenario`.
    **Parameters**:
    - `mexiron_name:Optional[str]`: Имя мексирончика, по умолчанию `gs.now`.
    - `driver:Optional[Firefox | Playwrid | str]`: Экземпляр WebDriver, по умолчанию Firefox.
    - `**kwargs`: Дополнительные параметры для WebDriver.
- `run_scenario_async(self, urls: List[str],  price: Optional[str] = '', mexiron_name: Optional[str] = gs.now, bot: Optional[telebot.TeleBot] = None, chat_id: Optional[int] = 0, attempts: int = 3) -> bool`: 
    **Описание**: Запускает сценарий асинхронно.
    **Parameters**:
    - `urls: List[str]`: Список URL-адресов товаров для обработки.
    - `price: Optional[str]`: Цена товара, по умолчанию ''.
    - `mexiron_name: Optional[str]`: Имя мексирончика, по умолчанию `gs.now`.
    - `bot: Optional[telebot.TeleBot]`: Экземпляр Telegram-бота, по умолчанию `None`.
    - `chat_id: Optional[int]`: ID чата в Telegram, по умолчанию 0.
    - `attempts: int`: Количество попыток, по умолчанию 3.
    **Returns**: 
    - `bool`:  `True` если сценарий выполнен успешно, `False` в случае ошибки.

## Функции

### `run_sample_scenario()`

**Описание**: Запускает тестовый сценарий.

## Принцип работы

1. **Сбор товаров**: Функция `run_scenario_async()` собирает товары по указанным URL-адресам. 
    - Используется `get_graber_by_supplier_url()` для получения грабера по URL-адресу. 
    - Graber парсит страницу товара и извлекает необходимые данные.
    - Функция проверяет, что graber найден для каждого URL-адреса, и сообщает об ошибке в случае отсутствия.
    - Если грабер найден, `grab_page_async()` извлекает поля товара. 
    - Проверяет, что поля товара получены успешно.
    - Преобразует полученные поля товара в формат `product_data` с помощью `convert_product_fields()`.
    - Сохраняет `product_data` с помощью `save_product_data()`. 
2. **Обработка AI**:  `process_llm_async()` отправляет список компонентов сборки компьютера в Gemini.
    - Gemini парсит данные, переводит текст на нужные языки (`he`, `ru`) и возвращает список словарей с информацией о товаре.
    - Проверяет, что модель работает успешно и не пропускает ошибки.
3. **Создание отчета**: `create_reports_async()` из модуля `ReportGenerator` создает отчеты в формате JSON и DOCX.
    - Сохраняет отчет в JSON-формате.
    - Запускает функцию `create_reports_async()` для генерации отчета в формате DOCX.

## Параметры

- `urls: List[str]`: Список URL-адресов товаров для обработки.
- `price: Optional[str]`: Цена товара, по умолчанию ''.
- `mexiron_name: Optional[str]`: Имя мексирончика, по умолчанию `gs.now`.
- `bot: Optional[telebot.TeleBot]`: Экземпляр Telegram-бота, по умолчанию `None`.
- `chat_id: Optional[int]`: ID чата в Telegram, по умолчанию 0.
- `attempts: int`: Количество попыток, по умолчанию 3.

## Примеры

```python
# Запускаем сценарий с несколькими URL-адресами
urls_list:list[str] = ['https://www.morlevi.co.il/product/21039',
                           'https://www.morlevi.co.il/product/21018',
                           'https://www.ivory.co.il/catalog.php?id=85473',
                           'https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe',
                           'https://www.ivory.co.il/catalog.php?id=85473',
                           'https://www.morlevi.co.il/product/21018']

s = Scenario(window_mode = 'normal')
asyncio.run(s.run_scenario_async(urls = urls_list, mexiron_name = 'test price quotation', ))

```