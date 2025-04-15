### **Системные инструкции для обработки кода проекта `hypotez`**

=========================================================================================

Описание функциональности и правил для генерации, анализа и улучшения кода. Направлено на обеспечение последовательного и читаемого стиля кодирования, соответствующего требованиям.

---

### **Основные принципы**

#### **1. Общие указания**:
- Соблюдай четкий и понятный стиль кодирования.
- Все изменения должны быть обоснованы и соответствовать установленным требованиям.

#### **2. Комментарии**:
- Используй `#` для внутренних комментариев.
- Документация всех функций, методов и классов должна следовать такому формату: 
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """ 
            Args:
                param (str): Описание параметра `param`.
                param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.
    
            Returns:
                dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.
    
            Raises:
                SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

            Ехаmple:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Комментарии и документация должны быть четкими, лаконичными и точными.

#### **3. Форматирование кода**:
- Используй одинарные кавычки. `a:str = 'value'`, `print('Hello World!')`;
- Добавляй пробелы вокруг операторов. Например, `x = 5`;
- Все параметры должны быть аннотированы типами. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Не используй `Union`. Вместо этого используй `|`.

#### **4. Логирование**:
- Для логгирования Всегда Используй модуль `logger` из `src.logger.logger`.
- Ошибки должны логироваться с использованием `logger.error`.
Пример:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ех, exc_info=True)
    ```
#### **5 Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```




---

### **Основные требования**:

#### **1. Формат ответов в Markdown**:
- Все ответы должны быть выполнены в формате **Markdown**.

#### **2. Формат комментариев**:
- Используй указанный стиль для комментариев и документации в коде.
- Пример:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Всегда делай подробные объяснения в комментариях. Избегай расплывчатых терминов, 
- таких как *«получить»* или *«делать»*
-  . Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
- Вместо: *«получаем»*, *«возвращаем»*, *«преобразовываем»* используй имя объекта *«функция получае»*, *«переменная возвращает»*, *«код преобразовывает»* 
- Комментарии должны непосредственно предшествовать описываемому блоку кода и объяснять его назначение.

#### **3. Пробелы вокруг операторов присваивания**:
- Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.
- Примеры:
  - **Неправильно**: `x=5`
  - **Правильно**: `x = 5`

#### **4. Использование `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- Пример:

```python
# Неправильно:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Правильно:
data = j_loads('config.json')
```

#### **5. Сохранение комментариев**:
- Все существующие комментарии, начинающиеся с `#`, должны быть сохранены без изменений в разделе «Улучшенный код».
- Если комментарий кажется устаревшим или неясным, не изменяйте его. Вместо этого отметьте его в разделе «Изменения».

#### **6. Обработка `...` в коде**:
- Оставляйте `...` как указатели в коде без изменений.
- Не документируйте строки с `...`.
```

#### **7. Аннотации**
Для всех переменных должны быть определены аннотации типа. 
Для всех функций все входные и выходные параметры аннотириваны
Для все параметров должны быть аннотации типа.


### **8. webdriver**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

## Анализ кода `hypotez/src/suppliers/scenario/scenario_executor.py`

### 1. Блок-схема

```mermaid
graph TD
    A[Начало: run_scenario_files] --> B{scenario_files_list является Path?};
    B -- Да --> C[Преобразовать scenario_files_list в список];
    B -- Нет --> D{scenario_files_list является списком?};
    D -- Нет --> E[Вызвать TypeError];
    D -- Да --> F{scenario_files_list не пустой?};
    F -- Да --> G[Использовать scenario_files_list];
    F -- Нет --> H[Использовать s.scenario_files];
    G --> I[Инициализация _journal['scenario_files']];
    H --> I;
    I --> J{Цикл по scenario_file в scenario_files_list};
    J -- Да --> K[Инициализация _journal['scenario_files'][scenario_file.name]];
    K --> L{Вызвать run_scenario_file(s, scenario_file)};
    L -- Успех --> M[Обновить _journal['scenario_files'][scenario_file.name]['message'] и logger.success];
    L -- Ошибка --> N[Обновить _journal['scenario_files'][scenario_file.name]['message'] и logger.error];
    L -- Исключение --> O[logger.critical и обновить _journal['scenario_files'][scenario_file.name]['message']];
    J -- Нет --> P[Конец: run_scenario_files];
    M --> J;
    N --> J;
    O --> J;

    subgraph Пример обработки scenario_files_list как Path
    A1[scenario_files_list = Path('path/to/scenario.json')] --> B
    end

    subgraph Пример обработки scenario_files_list как list
    A2[scenario_files_list = [Path('path/to/scenario1.json'), Path('path/to/scenario2.json')]] --> B
    end

    subgraph Пример обработки s.scenario_files
    A3[s.scenario_files = [Path('path/to/scenario3.json'), Path('path/to/scenario4.json')]] --> H
    end
```

### 2. Диаграмма

```mermaid
flowchart TD
    subgraph header.py
    Start_Header --> Determine_Project_Root["Определение корневой директории проекта"]
    Determine_Project_Root --> Import_Global_Settings["Импорт глобальных настроек: <br><code>from src import gs</code>"]
    End_Header
    end

    A[Начало] --> B(run_scenario_files);
    B --> C{Вызов run_scenario_file для каждого файла};
    C --> D(run_scenario_file);
    D --> E{Загрузка сценариев из файла (j_loads)};
    E --> F{Цикл по сценариям};
    F --> G(run_scenario);
    G --> H{Получение URL из сценария};
    H --> I{Получение списка продуктов (s.related_modules.get_list_products_in_category)};
    I --> J{Цикл по URL продуктов};
    J --> K{Переход на страницу продукта (d.get_url)};
    K --> L{Сбор данных со страницы продукта (s.related_modules.grab_product_page)};
    L --> M{Асинхронный сбор данных со страницы продукта (s.related_modules.grab_page)};
    M --> N{Создание объекта Product};
    N --> O{Вставка собранных данных (insert_grabbed_data)};
    O --> P[Конец];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style P fill:#f9f,stroke:#333,stroke-width:2px
```

**Объяснение диаграммы:**

- Диаграмма `mermaid` описывает поток выполнения основных функций, начиная с `run_scenario_files` и заканчивая обработкой отдельных продуктов.
- **header.py**: Определяет корневую директорию проекта и импортирует глобальные настройки.
- Функция `run_scenario_files` вызывает `run_scenario_file` для каждого переданного файла сценария.
- `run_scenario_file` загружает сценарии из файла с использованием `j_loads` и вызывает `run_scenario` для каждого сценария.
- `run_scenario` получает URL из сценария, собирает список продуктов и затем, в цикле, переходит на страницу каждого продукта, собирает данные и вставляет их.

### 3. Объяснение

**Импорты:**

- `os`, `sys`, `requests`, `asyncio`, `time`, `tempfile`, `datetime`, `math`, `pathlib`, `typing`, `json`: Стандартные библиотеки Python для работы с операционной системой, системными вызовами, HTTP-запросами, асинхронным программированием, временем, временными файлами, датой и временем, математическими функциями, путями к файлам, типами и JSON соответственно.
- `header`: Локальный модуль, вероятно, содержащий определение корневого каталога проекта и общие переменные.
- `src.gs`: Глобальные настройки проекта.
- `src.utils.printer`: Модуль для "pretty" печати данных.
- `src.utils.jjson`: Модуль для работы с JSON, использующий `j_loads` для загрузки и `j_dumps` для сохранения данных.
- `src.endpoints.prestashop.product_async`: Модуль для асинхронной работы с продуктами PrestaShop, включая класс `PrestaProductAsync` и перечисление `ProductFields`.
- `src.endpoints.prestashop.db`: Модуль для управления кампаниями продуктов в базе данных PrestaShop.
- `src.logger.logger`: Модуль для логирования событий.
- `src.logger.exceptions`: Модуль, содержащий пользовательские исключения.

**Классы:**

- `Product`: Не показан в предоставленном коде, но, вероятно, представляет собой класс для хранения информации о продукте.
- `PrestaShop`:  Предположительно класс для взаимодействия с API PrestaShop (его определение отсутствует в предоставленном коде).
- `ProductFields`: Перечисление, содержащее поля продукта.
- `ProductCampaignsManager`: Менеджер для управления кампаниями продуктов в БД PrestaShop.

**Функции:**

- `dump_journal(s, journal: dict) -> None`:
  - Аргументы: `s` (объект поставщика), `journal` (словарь с данными журнала).
  - Назначение: Сохраняет данные журнала в JSON-файл.
  - Пример: `dump_journal(supplier_instance, {'name': 'test_scenario', 'data': {'key': 'value'}})`
- `run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool`:
  - Аргументы: `s` (объект поставщика), `scenario_files_list` (список путей к файлам сценариев или путь к одному файлу).
  - Назначение: Выполняет сценарии из списка файлов.
  - Возвращает: `True`, если все сценарии выполнены успешно, `False` в противном случае.
  - Пример: `run_scenario_files(supplier_instance, [Path('scenario1.json'), Path('scenario2.json')])`
- `run_scenario_file(s, scenario_file: Path) -> bool`:
  - Аргументы: `s` (объект поставщика), `scenario_file` (путь к файлу сценария).
  - Назначение: Загружает и выполняет сценарии из файла.
  - Возвращает: `True`, если сценарий выполнен успешно, `False` в противном случае.
  - Пример: `run_scenario_file(supplier_instance, Path('scenario.json'))`
- `run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool`:
  - Аргументы: `s` (объект поставщика), `scenarios` (список или словарь сценариев).
  - Назначение: Выполняет список сценариев.
  - Возвращает: Результат выполнения сценариев или `False` в случае ошибки.
  - Пример: `run_scenarios(supplier_instance, [{'url': 'http://example.com', 'actions': []}])`
- `run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool`:
  - Аргументы: `supplier` (объект поставщика), `scenario` (словарь с деталями сценария), `scenario_name` (имя сценария).
  - Назначение: Выполняет полученный сценарий.
  - Возвращает: Результат выполнения сценария.
  - Пример: `run_scenario(supplier_instance, {'url': 'http://example.com', 'actions': []}, 'test_scenario')`
- `insert_grabbed_data_to_prestashop(f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool`:
  - Аргументы: `f` (экземпляр `ProductFields` с информацией о продукте), `coupon_code` (код купона), `start_date` (дата начала акции), `end_date` (дата окончания акции).
  - Назначение: Вставляет информацию о продукте в PrestaShop.
  - Возвращает: `True`, если вставка прошла успешно, `False` в противном случае.
  - Пример: `insert_grabbed_data_to_prestashop(product_fields, coupon_code='SUMMER20', start_date='2024-06-01', end_date='2024-08-31')`

**Переменные:**

- `_journal`: Глобальный словарь для отслеживания выполнения сценариев.
- `timestamp`: Текущее время в формате, определенном в `gs.now`.
- `s`: Объект поставщика (supplier).
- `d`: Объект драйвера (webdriver).
- `f`: Объект `ProductFields`, содержащий данные о продукте.

**Потенциальные ошибки и области для улучшения:**

- Обработка исключений в `run_scenario_files` и `run_scenario_file` записывает только сообщение об ошибке в журнал, но не возвращает `False`, что может привести к неправильной обработке ошибок на более высоких уровнях.
- В функции `run_scenarios`, `_journal['scenario_files'][-1][scenario] = str(res)` может вызывать исключение, если `_journal['scenario_files']` пуст. Необходимо добавить проверку.
- Отсутствует обработка случая, когда не указаны сценарии (пустой `s.current_scenario` и `scenarios`).
- Нет описания класса `Product`.
- В `run_scenario` присутствует строка `insert_grabbed_data(f)`, но нет определения этой функции в предоставленном коде.
- Не указано, откуда берется переменная `Product` в `run_scenario`.
- В `run_scenario` переменная `_journal` не передается в функцию `dump_journal`, а используется глобальная переменная `_journal`.

**Взаимосвязи с другими частями проекта:**

- `header.py`: Определяет корневой каталог проекта и импортирует глобальные настройки.
- `src.gs`: Глобальные настройки используются для получения текущего времени.
- `src.utils.jjson`: Используется для загрузки и сохранения JSON-файлов.
- `src.endpoints.prestashop`: Содержит классы и методы для взаимодействия с PrestaShop.
- `src.logger`: Используется для логирования событий.

Этот модуль является ключевым компонентом для выполнения сценариев сбора данных с сайтов поставщиков и вставки их в PrestaShop. Он использует множество других модулей проекта `hypotez` для выполнения своих задач.