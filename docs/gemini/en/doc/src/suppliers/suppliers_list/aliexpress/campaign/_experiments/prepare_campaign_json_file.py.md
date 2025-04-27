# Подготовка файла с настройками рекламной кампании для AliExpress

## Обзор

Этот модуль предназначен для подготовки файла с настройками рекламной кампании для AliExpress. 

## Детали

Файл `prepare_campaign_json_file.py` предназначен для подготовки настроек рекламной кампании. 

## Функции

### `process_campaign_category`

**Purpose**: Функция обрабатывает категорию рекламной кампании.

**Parameters**:

- `campaign_name` (str): Название рекламной кампании.

**Returns**:

- None: Функция ничего не возвращает.

**How the Function Works**:

- Функция получает название рекламной кампании.
- Проверяет существование категории и создает ее, если необходимо.
- Обрабатывает все продукты в категории.

**Examples**:

```python
process_campaign_category(campaign_name='lighting')
```

### `process_campaign`

**Purpose**: Функция обрабатывает рекламную кампанию.

**Parameters**:

- `campaign_name` (str): Название рекламной кампании.

**Returns**:

- None: Функция ничего не возвращает.

**How the Function Works**:

- Функция получает название рекламной кампании.
- Проверяет существование кампании и создает ее, если необходимо.
- Обрабатывает все категории в кампании.

**Examples**:

```python
process_campaign(campaign_name='lighting')
```

### `process_all_campaigns`

**Purpose**: Функция обрабатывает все рекламные кампании.

**Parameters**:

- None: Функция не принимает параметров.

**Returns**:

- None: Функция ничего не возвращает.

**How the Function Works**:

- Функция получает список всех рекламных кампаний.
- Обрабатывает каждую кампанию с помощью функции `process_campaign`.

**Examples**:

```python
process_all_campaigns()
```

## Параметры

- `campaign_name` (str): Название рекламной кампании.

## Examples 

```python
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor

campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'
campaign_editor = AliCampaignEditor(campaign_name=campaign_name, campaign_file=campaign_file)
```

## Примечания

- В коде используются следующие модули:
    - `header`: модуль с настройками и конфигурацией
    - `Path`: модуль для работы с файлами и каталогами
    - `AliCampaignEditor`: класс для управления рекламными кампаниями на AliExpress
    - `gs`: модуль для работы с Google Sheets
    - `process_campaign_category`, `process_campaign`, `process_all_campaigns`: функции для обработки рекламных кампаний
    - `get_filenames`, `get_directory_names`: функции для работы с файлами и каталогами
    - `pprint`: функция для форматированного вывода данных
    - `logger`: модуль для логирования
- В коде используются следующие переменные:
    - `campaign_name`: название рекламной кампании
    - `campaign_file`: имя файла с настройками рекламной кампании
    - `campaign_editor`: экземпляр класса `AliCampaignEditor`
- В коде используются следующие константы:
    - `locales`: словарь с языками и валютами
- В коде используются следующие функции:
    - `process_campaign_category`: функция для обработки категории рекламной кампании
    - `process_campaign`: функция для обработки рекламной кампании
    - `process_all_campaigns`: функция для обработки всех рекламных кампаний
    - `get_filenames`: функция для получения списка файлов в каталоге
    - `get_directory_names`: функция для получения списка каталогов в каталоге
    - `pprint`: функция для форматированного вывода данных
    - `logger.info`: функция для записи информационного сообщения в лог
    - `logger.error`: функция для записи сообщения об ошибке в лог
- В коде используются следующие классы:
    - `AliCampaignEditor`: класс для управления рекламными кампаниями на AliExpress
- В коде используются следующие исключения:
    - `Exception`: общее исключение
- В коде используются следующие методы:
    - `__init__`: конструктор класса
    - `process_campaign_category`: метод для обработки категории рекламной кампании
    - `process_campaign`: метод для обработки рекламной кампании
    - `process_all_campaigns`: метод для обработки всех рекламных кампаний
    - `get_filenames`: метод для получения списка файлов в каталоге
    - `get_directory_names`: метод для получения списка каталогов в каталоге
    - `pprint`: метод для форматированного вывода данных
    - `logger.info`: метод для записи информационного сообщения в лог
    - `logger.error`: метод для записи сообщения об ошибке в лог
- В коде используются следующие переменные:
    - `campaign_name`: название рекламной кампании
    - `campaign_file`: имя файла с настройками рекламной кампании
    - `campaign_editor`: экземпляр класса `AliCampaignEditor`