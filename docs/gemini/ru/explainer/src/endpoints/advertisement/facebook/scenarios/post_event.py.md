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

## Анализ кода `hypotez/src/endpoints/advertisement/facebook/scenarios/post_event.py`

### 1. Блок-схема

```mermaid
graph TD
    A[Начало: post_event(d: Driver, event: SimpleNamespace)] --> B{post_title(d, event.title)?};
    B -- Нет --> H[Конец: return];
    B -- Да --> C{dt, tm = event.start.split()};
    C --> D{post_date(d, dt.strip())?};
    D -- Нет --> H;
    D -- Да --> E{post_time(d, tm.strip())?};
    E -- Нет --> H;
    E -- Да --> F{post_description(d, f"{event.description}\\n{event.promotional_link}")?};
    F -- Нет --> H;
    F -- Да --> G{d.execute_locator(locator = locator.event_send)?};
    G -- Нет --> H;
    G -- Да --> I[time.sleep(30)];
    I --> J[Конец: return True];
    H[Конец: return];
```

**Примеры для каждого логического блока:**

*   **A**: `post_event(driver, event_data)` - Запуск процесса публикации события.
*   **B**: `post_title(driver, event_data.title)` - Проверка, успешно ли отправлен заголовок события. Если нет, функция завершается.
*   **C**: `dt, tm = event_data.start.split()` - Разделение строки `event_data.start`, содержащей дату и время, на отдельные переменные `dt` (дата) и `tm` (время).
*   **D**: `post_date(driver, dt.strip())` - Проверка, успешно ли отправлена дата события. Если нет, функция завершается.
*   **E**: `post_time(driver, tm.strip())` - Проверка, успешно ли отправлено время события. Если нет, функция завершается.
*   **F**: `post_description(driver, f"{event_data.description}\\n{event_data.promotional_link}")` - Проверка, успешно ли отправлено описание события, включая рекламную ссылку. Если нет, функция завершается.
*   **G**: `driver.execute_locator(locator = locator.event_send)` - Попытка отправить событие через веб-драйвер, используя локатор кнопки отправки. Если не успешно, функция завершается.
*   **H**: `return` - Завершение функции с возвратом `None` (в случаях неудачи) или `True` (в случае успеха).
*   **I**: `time.sleep(30)` - Принудительная приостановка выполнения программы на 30 секунд.
*   **J**: `return True` - Успешное завершение функции.

### 2. Диаграмма

```mermaid
flowchart TD
    subgraph src.endpoints.advertisement.facebook.scenarios
        post_event[post_event(d: Driver, event: SimpleNamespace) : bool]
        post_title[post_title(d: Driver, title: str) : bool]
        post_date[post_date(d: Driver, date: str) : bool]
        post_time[post_time(d: Driver, time: str) : bool]
        post_description[post_description(d: Driver, description: str) : bool]
    end

    subgraph src.webdriver
        Driver
    end

    subgraph src.utils
        j_loads_ns[j_loads_ns(path: Path) : SimpleNamespace]
    end

    subgraph src.logger
        logger[logger]
    end

    post_event --> post_title
    post_event --> post_date
    post_event --> post_time
    post_event --> post_description
    post_title --> Driver
    post_date --> Driver
    post_time --> Driver
    post_description --> Driver

    post_title --> logger
    post_date --> logger
    post_time --> logger
    post_description --> logger

    post_event --> Driver
    post_event --> j_loads_ns
    
    j_loads_ns --> Path
```

**Объяснение зависимостей:**

*   `post_event`, `post_title`, `post_date`, `post_time`, и `post_description` - функции, определенные в файле `post_event.py`, предназначенные для выполнения различных этапов публикации события в Facebook.
*   `Driver` - класс, импортированный из `src.webdriver.driver`, используется для управления браузером и взаимодействия с веб-страницей Facebook.
*   `j_loads_ns` - функция, импортированная из `src.utils.jjson`, используется для загрузки данных из JSON-файла в виде `SimpleNamespace`.
*   `logger` - объект, импортированный из `src.logger.logger`, используется для логирования ошибок и другой информации.
*   `Path` - класс из модуля `pathlib`, используется для работы с путями к файлам и директориям.

### 3. Объяснение

#### Импорты:

*   `socket.timeout`: Импортируется, но не используется в предоставленном коде. Возможно, остался от предыдущих итераций разработки.
*   `time`: Используется для приостановки выполнения скрипта на заданное количество секунд (`time.sleep(30)`).
*   `pathlib.Path`: Используется для определения путей к файлам, в частности, к файлу с локаторами (`post_event.json`).
*   `types.SimpleNamespace`: Используется для создания объектов, атрибуты которых могут быть произвольно добавлены. В данном случае применяется для хранения данных о событии и локаторах.
*   `typing.Dict, typing.List`: Используются для аннотации типов, что улучшает читаемость и облегчает отладку кода.
*   `urllib.parse.urlencode`: Импортируется, но не используется в предоставленном коде. Возможно, остался от предыдущих итераций разработки.
*   `selenium.webdriver.remote.webelement.WebElement`: Импортируется, но не используется в предоставленном коде. Возможно, остался от предыдущих итераций разработки.
*   `src.gs`: Импортирует глобальные настройки проекта.
*   `src.webdriver.driver.Driver`: Импортирует класс `Driver`, используемый для управления браузером Selenium.
*   `src.utils.jjson.j_loads_ns`: Импортирует функцию `j_loads_ns` для загрузки данных из JSON-файлов и представления их в виде объектов `SimpleNamespace`.
*   `src.logger.logger.logger`: Импортирует объект `logger` для логирования событий и ошибок.

#### Классы:

*   `Driver` (из `src.webdriver.driver`): Отвечает за управление экземпляром веб-браузера и выполнение операций на веб-странице, таких как ввод текста, нажатие кнопок и скроллинг.

#### Функции:

*   `post_title(d: Driver, title: str) -> bool`: Отправляет заголовок события.
    *   Аргументы:
        *   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        *   `title` (str): Заголовок события.
    *   Возвращает:
        *   `bool`: `True`, если заголовок успешно отправлен, иначе `None`.
    *   Пример:
        ```python
        driver = Driver(...)
        title = "Campaign Title"
        post_title(driver, title)
        ```
*   `post_date(d: Driver, date: str) -> bool`: Отправляет дату события.
    *   Аргументы:
        *   `d` (Driver): Экземпляр драйвера.
        *   `date` (str): Дата события.
    *   Возвращает:
        *   `bool`: `True`, если дата успешно отправлена, иначе `None`.
    *   Пример:
        ```python
        driver = Driver(...)
        date = "2024-07-28"
        post_date(driver, date)
        ```
*   `post_time(d: Driver, time: str) -> bool`: Отправляет время события.
    *   Аргументы:
        *   `d` (Driver): Экземпляр драйвера.
        *   `time` (str): Время события.
    *   Возвращает:
        *   `bool`: `True`, если время успешно отправлено, иначе `None`.
*   `post_description(d: Driver, description: str) -> bool`: Отправляет описание события.
    *   Аргументы:
        *   `d` (Driver): Экземпляр драйвера.
        *   `description` (str): Описание события.
    *   Возвращает:
        *   `bool`: `True`, если описание успешно отправлено, иначе `None`.
*   `post_event(d: Driver, event: SimpleNamespace) -> bool`: Управляет процессом публикации события.
    *   Аргументы:
        *   `d` (Driver): Экземпляр драйвера.
        *   `event` (SimpleNamespace): Объект, содержащий данные о событии (заголовок, описание, дата, время).
    *   Возвращает:
        *   `bool`: `True`, если все этапы публикации прошли успешно.

#### Переменные:

*   `locator`: Объект `SimpleNamespace`, содержащий локаторы элементов веб-страницы, загруженные из JSON-файла (`post_event.json`).
*   `d`: Экземпляр класса `Driver`, используемый для управления браузером.
*   `event`: Экземпляр класса `SimpleNamespace`, содержащий данные о событии.
*   `title`, `date`, `time`, `description`: Строковые переменные, содержащие соответствующие данные о событии.

#### Потенциальные ошибки и области для улучшения:

1.  **Обработка ошибок:** Функции `post_title`, `post_date`, `post_time`, и `post_description` возвращают `None` в случае ошибки, но функция `post_event` предполагает, что они возвращают `False`. Это может привести к непредсказуемому поведению.  Следует возвращать `False` или явно обрабатывать `None`.
2.  **Логирование:** Логирование ошибок выполняется с `exc_info=False`, что не включает трассировку стека.  Рекомендуется включать трассировку стека (`exc_info=True`) для упрощения отладки.
3.  **Ожидание:**  Использование `time.sleep(30)` является плохой практикой.  Рекомендуется использовать более надежные методы ожидания, основанные на событиях (например, `WebDriverWait`).
4.  **Дублирование кода:** Функции `post_title`, `post_date`, `post_time` имеют очень похожую структуру.  Рекомендуется рассмотреть возможность рефакторинга для уменьшения дублирования кода.
5. **Отсутствие обработки исключений** В коде отсутствуют блоки `try ... except` для обработки возможных исключений при взаимодействии с веб-элементами.
6. **Неиспользуемые импорты** В коде присутствуют неиспользуемые импорты, такие как `urllib.parse.urlencode` и `selenium.webdriver.remote.webelement.WebElement`.

#### Взаимосвязи с другими частями проекта:

*   Файл использует `src.webdriver.driver.Driver` для взаимодействия с веб-браузером, что позволяет автоматизировать действия на странице Facebook.
*   Локаторы элементов интерфейса загружаются из JSON-файла с помощью `src.utils.jjson.j_loads_ns`, что обеспечивает гибкость и упрощает поддержку.
*   Для логирования используется `src.logger.logger.logger`, что позволяет отслеживать ход выполнения программы и выявлять ошибки.
*   Глобальные настройки (`src.gs`) используются для определения пути к файлу с локаторами.