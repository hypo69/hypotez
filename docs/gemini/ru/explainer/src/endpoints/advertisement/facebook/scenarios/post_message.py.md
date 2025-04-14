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
- таких как *«получить»* или *«делать»*. Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
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

### **Анализ кода `post_message.py`**

#### **1. Блок-схема**

```mermaid
graph TD
    A[Начало - post_message] --> B{Вызов post_title};
    B -- Успешно --> C{Вызов d.wait(0.5)};
    B -- Неудача --> I[Конец - post_message (False)];
    C --> D{Вызов upload_media};
    D -- Успешно --> E{Вызов d.wait(0.5)};
    D -- Неудача --> I;
    E --> F{Вызов d.execute_locator(locator.send)};
    F -- True (Элемент найден) --> I[Конец - post_message (True)];
    F -- False (Элемент не найден) --> G{Вызов d.execute_locator(locator.finish_editing_button)};
    G -- Успешно --> H{Вызов publish};
    G -- Неудача --> I;
    H -- Успешно --> I[Конец - post_message (True)];
    H -- Неудача --> I;
```

**Описание блок-схемы:**

1.  **Начало `post_message`**: Функция `post_message` управляет процессом публикации сообщения в Facebook.
2.  **Вызов `post_title`**: Вызывается функция `post_title` для добавления заголовка и описания к сообщению.
    *   Пример: `post_title(driver, message)` добавляет заголовок и описание сообщения, используя данные из объекта `message`.
3.  **`d.wait(0.5)`**: Задержка в 0.5 секунды для ожидания загрузки элементов страницы.
4.  **Вызов `upload_media`**: Вызывается функция `upload_media` для загрузки медиафайлов (изображений или видео) к сообщению.
    *   Пример: `upload_media(driver, message.products, no_video=no_video, without_captions=without_captions)` загружает медиафайлы, используя список `message.products`.
5.  **`d.wait(0.5)`**: Задержка в 0.5 секунды для ожидания загрузки элементов страницы.
6.  **`d.execute_locator(locator.send)`**: Проверяется, найден ли элемент `locator.send` на странице.
    *   Если элемент найден, функция возвращает `True`.
7.  **`d.execute_locator(locator.finish_editing_button)`**: Если элемент `locator.send` не найден, выполняется попытка найти и нажать кнопку "Завершить редактирование".
8.  **Вызов `publish`**: Вызывается функция `publish` для публикации сообщения.
9.  **Конец `post_message`**: Функция завершается, возвращая `True` или `False` в зависимости от успеха публикации.

#### **2. Диаграмма**

```mermaid
flowchart TD
    A[<code>post_message.py</code><br>Основной сценарий публикации сообщения] --> B(<code>post_title</code><br>Добавление заголовка и описания);
    A --> C(<code>upload_media</code><br>Загрузка медиафайлов);
    A --> D{<code>d.execute_locator(locator.send)</code><br>Проверка кнопки "Отправить"};
    A --> E{<code>d.execute_locator(locator.finish_editing_button)</code><br>Поиск кнопки "Завершить редактирование"};
    A --> F(<code>publish</code><br>Публикация сообщения);
    B --> G[<code>src.webdriver.driver.Driver</code><br>Управление браузером];
    C --> G;
    D --> G;
    E --> G;
    F --> G;
    A --> H[<code>src.utils.jjson.j_loads_ns</code><br>Загрузка локаторов из JSON];
    H --> I[<code>src.gs</code><br>Глобальные настройки];
    C --> J[<code>src.logger.logger</code><br>Логирование ошибок];
    F --> J;
    B --> J;
    E --> J;
    D --> J;
    subgraph src.webdriver
    G[<code>src.webdriver.driver.Driver</code>]
    end
    subgraph src.utils
    H[<code>src.utils.jjson.j_loads_ns</code>]
    end
    subgraph src.logger
    J[<code>src.logger.logger</code>]
    end
```

**Объяснение зависимостей:**

*   `post_message.py`: Основной файл, который управляет сценарием публикации сообщения.
*   `post_title`: Функция для добавления заголовка и описания. Зависит от `src.webdriver.driver.Driver` для взаимодействия с веб-страницей и `src.logger.logger` для логирования.
*   `upload_media`: Функция для загрузки медиафайлов. Зависит от `src.webdriver.driver.Driver` для управления браузером, `src.logger.logger` для логирования ошибок и `src.utils.jjson.j_loads_ns` для загрузки локаторов.
*   `d.execute_locator(locator.send)`: Метод для проверки наличия кнопки "Отправить". Зависит от `src.webdriver.driver.Driver` для взаимодействия с веб-страницей.
*   `d.execute_locator(locator.finish_editing_button)`: Метод для поиска кнопки "Завершить редактирование". Зависит от `src.webdriver.driver.Driver` для взаимодействия с веб-страницей и `src.logger.logger` для логирования.
*   `publish`: Функция для публикации сообщения. Зависит от `src.webdriver.driver.Driver` для управления браузером и `src.logger.logger` для логирования.
*   `src.webdriver.driver.Driver`: Модуль для управления браузером через Selenium.
*   `src.utils.jjson.j_loads_ns`: Модуль для загрузки данных из JSON-файлов в виде namespace.
*   `src.gs`: Модуль, содержащий глобальные настройки и пути.
*   `src.logger.logger`: Модуль для логирования событий и ошибок.

#### **3. Объяснение**

**Импорты:**

*   `time`: Используется для добавления временных задержек в процессе выполнения.
*   `pathlib.Path`: Используется для работы с путями к файлам и директориям.
*   `typing.Dict, List, Optional`: Используются для аннотации типов переменных и функций.
*   `selenium.webdriver.remote.webelement.WebElement`: Используется для представления веб-элементов на странице.
*   `src.gs`: Импортирует глобальные настройки проекта.
*   `src.webdriver.driver.Driver`: Импортирует класс `Driver` для управления браузером.
*   `src.utils.jjson.j_loads_ns`: Импортирует функцию `j_loads_ns` для загрузки данных из JSON-файлов в виде namespace.
*   `src.utils.printer.pprint`: Импортирует функцию `pprint` для удобной печати данных.
*   `src.logger.logger`: Импортирует модуль `logger` для логирования событий и ошибок.

**Переменные:**

*   `locator`: Объект `SimpleNamespace`, содержащий локаторы элементов страницы, загруженные из JSON-файла `post_message.json`.

**Функции:**

*   `post_title(d: Driver, message: SimpleNamespace | str) -> bool`:
    *   Аргументы:
        *   `d` (`Driver`): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        *   `message` (`SimpleNamespace | str`): Объект `SimpleNamespace`, содержащий заголовок и описание, или строка сообщения.
    *   Возвращаемое значение:
        *   `bool`: `True`, если заголовок и описание успешно добавлены, иначе `None`.
    *   Назначение: Добавляет заголовок и описание к сообщению в поле ввода.
    *   Пример:
        ```python
        driver = Driver(...)
        message = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        post_title(driver, message)
        ```
*   `upload_media(d: Driver, media: SimpleNamespace | List[SimpleNamespace] | str | list[str], no_video: bool = False, without_captions: bool = False) -> bool`:
    *   Аргументы:
        *   `d` (`Driver`): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        *   `media` (`SimpleNamespace | List[SimpleNamespace] | str | list[str]`): Список объектов `SimpleNamespace` или строк, содержащих пути к медиафайлам.
        *   `no_video` (`bool`): Флаг, указывающий, нужно ли игнорировать видеофайлы.
        *   `without_captions` (`bool`): Флаг, указывающий, нужно ли пропускать обновление подписей.
    *   Возвращаемое значение:
        *   `bool`: `True`, если медиафайлы успешно загружены, иначе `None`.
    *   Назначение: Загружает медиафайлы на страницу и обновляет подписи.
    *   Пример:
        ```python
        driver = Driver(...)
        products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        upload_media(driver, products)
        ```
*   `update_images_captions(d: Driver, media: List[SimpleNamespace], textarea_list: List[WebElement]) -> None`:
    *   Аргументы:
        *   `d` (`Driver`): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        *   `media` (`List[SimpleNamespace]`): Список объектов `SimpleNamespace`, содержащих детали для обновления.
        *   `textarea_list` (`List[WebElement]`): Список элементов `textarea`, в которые добавляются подписи.
    *   Возвращаемое значение:
        *   `None`
    *   Назначение: Добавляет описания к загруженным медиафайлам.
*   `publish(d: Driver, attempts: int = 5) -> bool`:
    *   Аргументы:
        *   `d` (`Driver`): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        *   `attempts` (`int`): Количество попыток публикации.
    *   Возвращаемое значение:
        *   `bool`: `True`, если сообщение успешно опубликовано.
    *   Назначение: Осуществляет публикацию сообщения.
*   `promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool`:
    *   Аргументы:
        *   `d` (`Driver`): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        *   `category` (`SimpleNamespace`): Объект `SimpleNamespace`, содержащий детали категории.
        *   `products` (`List[SimpleNamespace]`): Список объектов `SimpleNamespace`, содержащих медиа и детали для публикации.
        *    `no_video` (`bool`): Флаг, указывающий, нужно ли игнорировать видеофайлы.
    *   Возвращаемое значение:
        *   `bool`: `True`, если продвижение поста прошло успешно.
    *   Назначение: Управляет процессом продвижения поста.
*   `post_message(d: Driver, message: SimpleNamespace, no_video: bool = False, images: Optional[str | list[str]] = None, without_captions: bool = False) -> bool`:
    *   Аргументы:
        *   `d` (`Driver`): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        *   `message` (`SimpleNamespace`): Объект `SimpleNamespace`, содержащий детали сообщения.
        *   `no_video` (`bool`): Флаг, указывающий, нужно ли игнорировать видеофайлы.
         *   `images` (`Optional[str | list[str]]`): Список изображений.
        *   `without_captions` (`bool`): Флаг, указывающий, нужно ли пропускать обновление подписей.
    *   Возвращаемое значение:
        *   `bool`: `True`, если сообщение успешно опубликовано.
    *   Назначение: Управляет процессом публикации сообщения.

**Потенциальные ошибки и области для улучшения:**

1.  **Обработка исключений**: В функции `upload_media` есть блок `try...except` для обработки ошибок при загрузке медиа, но пропуск ошибок может привести к неполной загрузке медиафайлов.
2.  **Логирование**: Добавить более подробное логирование для отслеживания процесса загрузки медиа и публикации сообщения.
3.  **Повторные попытки**: Функция `publish` содержит логику повторных попыток, но можно добавить лимит на количество повторных попыток, чтобы избежать бесконечного цикла.
4.  **Аннотации**: В коде встречаются места, где не хватает аннотаций типов, что ухудшает читаемость и поддержку кода.

**Взаимосвязи с другими частями проекта:**

*   Файл `post_message.py` является частью модуля `src.endpoints.advertisement.facebook.scenarios` и отвечает за реализацию сценария публикации сообщения в Facebook.
*   Он использует `src.webdriver.driver.Driver` для управления браузером и взаимодействия с веб-страницей Facebook.
*   Он использует `src.utils.jjson.j_loads_ns` для загрузки локаторов элементов страницы из JSON-файлов.
*   Он использует `src.logger.logger` для логирования событий и ошибок.
*   Он использует глобальные настройки из `src.gs`, такие как пути к файлам и директориям.