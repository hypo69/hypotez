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

## Анализ кода

Этот markdown-файл, расположенный в `hypotez/src/webdriver/_docs/locator.md`, предоставляет объяснение структуры и использования локаторов в контексте автоматизации веб-интерфейса с использованием `executor` в проекте `hypotez`. Локаторы представляют собой объекты конфигурации, описывающие, как находить элементы на веб-странице и взаимодействовать с ними. Они используются классом `ExecuteLocator` для выполнения различных действий, таких как клики, отправка сообщений или извлечение атрибутов.

### 1. Блок-схема

```mermaid
graph LR
    A[Начало] --> B{Определение локатора (JSON)};
    B -- Пример: close_banner --> C{Разбор ключей локатора};
    C -- attribute: null --> D{Определение типа локатора (by)};
    D -- by: XPATH --> E{Определение селектора элемента};
    E -- selector: "//button[@id = 'closeXButton']" --> F{Определение поведения при множественных элементах (if_list)};
    F -- if_list: "first" --> G{Использовать мышь? (use_mouse)};
    G -- use_mouse: false --> H{Обязательное действие? (mandatory)};
    H -- mandatory: false --> I{Таймаут (timeout)};
    I -- timeout: 0 --> J{Условие ожидания (timeout_for_event)};
    J -- timeout_for_event: "presence_of_element_located" --> K{Выполняемое событие (event)};
    K -- event: "click()" --> L{Описание локатора (locator_description)};
    L -- locator_description: "Закрыть pop-up" --> M{Взаимодействие с executor};
    M --> N{Поиск элемента по XPATH};
    N --> O{Выполнение клика};
    O --> P{Если элемент не найден и действие не обязательное - продолжить};
    P --> Q[Конец];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style Q fill:#f9f,stroke:#333,stroke-width:2px
```

### 2. Диаграмма

```mermaid
flowchart TD
    subgraph Locator Configuration
        A[<code>close_banner</code><br>Locator Example]
        B[<code>attribute</code><br>Attribute to extract/use]
        C[<code>by</code><br>Locator Type (XPATH, VALUE)]
        D[<code>selector</code><br>Element selector expression]
        E[<code>if_list</code><br>Handling multiple elements]
        F[<code>use_mouse</code><br>Use mouse for event]
        G[<code>mandatory</code><br>Is action mandatory?]
        H[<code>timeout</code><br>Timeout for finding element]
        I[<code>timeout_for_event</code><br>Wait condition]
        J[<code>event</code><br>Event to execute (click, screenshot)]
        K[<code>locator_description</code><br>Locator description]
    end

    subgraph Executor
        L[<code>executor</code><br>Interaction with Locators]
        M[Find Element<br>Based on <code>by</code> and <code>selector</code>]
        N[Execute Event<br>If <code>event</code> is specified]
        O[Extract Attribute<br>If <code>attribute</code> is specified]
        P[Handle Errors<br>Based on <code>mandatory</code> flag]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    A --> I
    A --> J
    A --> K
    B --> L
    C --> L
    D --> L
    E --> L
    F --> L
    G --> L
    H --> L
    I --> L
    J --> L
    K --> L
    L --> M
    L --> N
    L --> O
    L --> P
```

### 3. Объяснение

#### Импорты
В данном документе отсутствуют импорты, так как он описывает структуру данных и их взаимодействие.

#### Классы
В документе описывается взаимодействие между локаторами и классом `ExecuteLocator`.  `ExecuteLocator` использует информацию из локаторов для выполнения действий над веб-элементами.

#### Функции
В данном документе функции не описаны, так как он служит для объяснения структуры данных локаторов и их использования.

#### Переменные
Локаторы - это словари (которые в коде могут быть преобразованы в `SimpleNamespace`), содержащие следующие ключи:

- `attribute`: Атрибут элемента, который нужно извлечь или использовать.
- `by`: Тип локатора (например, XPATH, VALUE).
- `selector`: Селектор элемента (например, XPATH-выражение).
- `if_list`: Указывает, что делать, если найдено несколько элементов (например, использовать первый).
- `use_mouse`: Указывает, использовать ли мышь для выполнения события.
- `mandatory`: Указывает, является ли действие обязательным.
- `timeout`: Время ожидания элемента.
- `timeout_for_event`: Условие ожидания элемента.
- `event`: Событие, которое нужно выполнить (например, click, screenshot).
- `locator_description`: Описание локатора.

#### Потенциальные ошибки и области для улучшения

- Отсутствие обработки исключений при взаимодействии с `executor`.
- Отсутствие валидации структуры локатора.
- Жесткая привязка к определенным типам локаторов (например, XPATH). Можно рассмотреть возможность расширения поддерживаемых типов.

#### Взаимосвязи с другими частями проекта

Локаторы используются в модулях, связанных с автоматизацией веб-интерфейса, в частности, в классе `ExecuteLocator`, который, вероятно, находится в модуле `src.webdriver`. Они предоставляют данные для поиска и взаимодействия с элементами на веб-странице.