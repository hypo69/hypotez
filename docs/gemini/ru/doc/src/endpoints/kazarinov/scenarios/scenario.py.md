# Модуль `scenario.py`

## Обзор

Модуль `scenario.py` предназначен для исполнения сценариев, связанных с парсингом товаров, их обработкой с использованием искусственного интеллекта и сохранения полученных данных. Он содержит класс `Scenario`, который выполняет эти действия, используя различные инструменты, такие как веб-драйвер, грабберы и AI-модели. Модуль разработан специально для проекта "Казаринов".

## Подробнее

Модуль предоставляет функциональность для автоматизированного сбора информации о товарах с различных веб-сайтов, обработки этой информации с помощью AI моделей для перевода и анализа, а также генерации отчетов. Он включает в себя взаимодействие с веб-драйвером для навигации по сайтам, грабберы для извлечения данных о товарах и AI модели для обработки текста и перевода.

## Классы

### `Config`

**Описание**: Класс для хранения конфигурации, специфичной для модуля "Казаринов".

**Атрибуты**:

- `ENDPOINT` (str): Конечная точка (endpoint) для "Казаринов", значение по умолчанию - "kazarinov".

### `Scenario`

**Описание**: Класс `Scenario` предназначен для выполнения сценария сбора информации о товарах, их обработки и сохранения.
**Наследует**:
- `QuotationBuilder`: класс, отвечающий за создание коммерческих предложений.
**Атрибуты**:
- `driver`: Инстанс веб-драйвера для управления браузером.

**Методы**:

- `__init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None, **kwargs)`: Инициализирует экземпляр класса `Scenario`.
- `run_scenario_async(self, urls: List[str], price: Optional[str] = '', mexiron_name: Optional[str] = gs.now, bot: Optional[telebot.TeleBot] = None, chat_id: Optional[int] = 0, attempts: int = 3) -> bool`: Асинхронно выполняет сценарий сбора информации о товарах, их обработки с использованием AI и сохранения данных.

## Методы класса

### `__init__`

```python
def __init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None, **kwargs) -> None:
    """
    Инициализирует экземпляр класса `Scenario`.

    Args:
        mexiron_name (Optional[str], optional): Имя для идентификации сценария. По умолчанию `gs.now`.
        driver (Optional[Firefox | Playwrid | str], optional): Инстанс веб-драйвера или его тип. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, передаваемые драйверу.

    """
    ...
```

**Назначение**: Инициализирует объект класса `Scenario`, устанавливая драйвер (если не передан, создается экземпляр Firefox) и вызывая конструктор родительского класса `QuotationBuilder`.

**Как работает функция**:
- Функция сначала проверяет наличие аргумента `window_mode` в `kwargs` и устанавливает его в `normal`, если он не был передан.
- Если `driver` не передан, то создается инстанс драйвера `Driver` с использованием `Firefox` и переданными `kwargs`.
- Затем вызывается конструктор родительского класса `QuotationBuilder` с переданными аргументами, включая имя сценария `mexiron_name` и драйвер.

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
    Асинхронно выполняет сценарий: парсит продукты, обрабатывает их через AI и сохраняет данные.

    Args:
        urls (List[str]): Список URL-адресов для парсинга.
        price (Optional[str], optional): Цена. По умолчанию ''.
        mexiron_name (Optional[str], optional): Имя сценария. По умолчанию `gs.now`.
        bot (Optional[telebot.TeleBot], optional): Экземпляр Telegram бота для отправки уведомлений. По умолчанию `None`.
        chat_id (Optional[int], optional): ID чата Telegram для отправки уведомлений. По умолчанию 0.
        attempts (int, optional): Количество попыток выполнения сценария. По умолчанию 3.

    Returns:
        bool: Возвращает `True` после успешного выполнения сценария.
    """
    ...
```

**Назначение**: Асинхронно выполняет основной сценарий, включающий сбор данных о товарах с заданных URL, их обработку с использованием AI для перевода и анализа, а также сохранение результатов и генерацию отчетов.

**Параметры**:
- `urls` (List[str]): Список URL-адресов, с которых необходимо собрать данные о товарах.
- `price` (Optional[str], optional): Цена, которая будет добавлена к данным о товарах. По умолчанию пустая строка.
- `mexiron_name` (Optional[str], optional): Имя сценария, используемое для идентификации и сохранения результатов. По умолчанию текущее время.
- `bot` (Optional[telebot.TeleBot], optional): Экземпляр Telegram бота для отправки уведомлений о ходе выполнения сценария. По умолчанию `None`.
- `chat_id` (Optional[int], optional): Идентификатор чата в Telegram, куда будут отправляться уведомления. По умолчанию 0.
- `attempts` (int, optional): Количество попыток выполнения сценария в случае неудачи. По умолчанию 3.

**Возвращает**:
- `bool`: `True` в случае успешного завершения сценария.

**Как работает функция**:

1. **Инициализация**:
   - Инициализирует пустой список `products_list` для хранения данных о товарах.
   - Устанавливает индекс языка `lang_index` равным 2.

2. **Сбор товаров**:
   - Итерируется по списку URL-адресов `urls`.
   - Для каждого URL пытается получить граббер (`graber`) с помощью функции `get_graber_by_supplier_url`.
   - Если граббер не найден, логирует ошибку и отправляет уведомление в Telegram (если бот предоставлен).
   - Вызывает метод `grab_page_async` граббера для получения полей товара.
   - Если получение полей товара не удалось, логирует ошибку и отправляет уведомление в Telegram.
   - Преобразует полученные поля товара с помощью метода `convert_product_fields`.
   - Сохраняет полученные данные о товаре с помощью метода `save_product_data`.
   - Добавляет данные о товаре в список `products_list`.

3. **AI Processing**:
   - Определяет список языков `langs_list` для перевода (`"he"`, `"ru"`).
   - Итерируется по списку языков.
   - Для каждого языка вызывает метод `process_llm_async` для обработки данных о товарах с использованием AI.
   - Если обработка AI не удалась, логирует исключение и отправляет уведомление в Telegram.

4. **Report Creating**:
   - Отправляет уведомление в Telegram о создании файла отчета.
   - Извлекает данные для текущего языка из результата обработки AI.
   - Добавляет цену и валюту в данные.
   - Сохраняет данные в формате JSON.
   - Создает отчет с помощью класса `ReportGenerator`.

5. **Завершение**:
   - Возвращает `True` после успешного выполнения сценария.

### Внутренние функции:
В данном коде нету внутренних функций

**Примеры**:
```python
import asyncio
from src.endpoints.kazarinov.scenarios.scenario import Scenario

async def main():
    s = Scenario(window_mode='normal')
    urls_list = [
        'https://www.morlevi.co.il/product/21039',
        'https://www.morlevi.co.il/product/21018',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://www.morlevi.co.il/product/21018'
    ]
    await s.run_scenario_async(urls=urls_list, mexiron_name='test_price_quotation')

if __name__ == "__main__":
    asyncio.run(main())
```

## Функции

### `run_sample_scenario`

```python
def run_sample_scenario() -> None:
    """ """
    ...
```

**Назначение**: Запускает демонстрационный сценарий с предопределенным списком URL-адресов.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция создает список URL-адресов `urls_list`.
- Создается экземпляр класса `Scenario` с параметром `window_mode`, установленным в `normal`.
- Асинхронно запускается сценарий `run_scenario_async` с передачей списка URL-адресов и имени сценария.

### Внутренние функции:
В данном коде нету внутренних функций

**Примеры**:
```python
from src.endpoints.kazarinov.scenarios.scenario import run_sample_scenario

run_sample_scenario()
```

## Параметры класса

- `mexiron_name` (Optional[str]): Имя сценария для идентификации результатов.
- `driver` (Optional[Firefox | Playwrid | str]): Инстанс веб-драйвера или его тип.
- `urls` (List[str]): Список URL-адресов для парсинга.
- `price` (Optional[str]): Цена, добавляемая к данным о товарах.
- `bot` (Optional[telebot.TeleBot]): Экземпляр Telegram бота для отправки уведомлений.
- `chat_id` (Optional[int]): ID чата Telegram для отправки уведомлений.
- `attempts` (int): Количество попыток выполнения сценария.

## Примеры

Пример запуска демонстрационного сценария:

```python
from src.endpoints.kazarinov.scenarios.scenario import Scenario
import asyncio

async def main():
    # Создание инстанса сценария
    s = Scenario(window_mode='normal')
    # Список URL для обработки
    urls_list = [
        'https://www.morlevi.co.il/product/21039',
        'https://www.morlevi.co.il/product/21018',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://www.morlevi.co.il/product/21018'
    ]
    # Запуск сценария
    await s.run_scenario_async(urls=urls_list, mexiron_name='test_price_quotation')

if __name__ == "__main__":
    asyncio.run(main())
```
Этот пример демонстрирует создание экземпляра класса `Scenario` и запуск метода `run_scenario_async` с заданными параметрами, такими как список URL-адресов и имя сценария.