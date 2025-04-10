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

## Анализ кода `hypotez/src/utils/convertors/xml2dict.py`

### 1. Блок-схема
```mermaid
graph LR
    A[Начало: xml2dict или ET2dict] --> B{Вызов ET.fromstring(xml) или прямой вход element_tree};
    B -- xml2dict --> C[ET.fromstring(xml)];
    B -- ET2dict --> D[element_tree];
    C --> D;
    D --> E{Вызов _make_dict(element_tree.tag, _parse_node(element_tree))};
    E --> F{Вызов _parse_node(node)};
    F --> G{Инициализация tree={}, attrs={}};
    G --> H{Цикл по атрибутам node.attrib.items()};
    H -- Атрибуты есть --> I{Проверка attr_tag == '{http://www.w3.org/1999/xlink}href'};
    I -- Да --> H;
    I -- Нет --> J{Вызов _make_dict(attr_tag, attr_value)};
    J --> K{attrs.update(_make_dict(attr_tag, attr_value))};
    K --> H;
    H -- Атрибутов нет --> L{value = node.text.strip() if node.text else ''};
    L --> M{Если attrs, то tree['attrs'] = attrs};
    M --> N{has_child = False};
    N --> O{Цикл по дочерним элементам list(node)};
    O -- Дочерние элементы есть --> P{has_child = True};
    P --> Q{ctag = child.tag};
    Q --> R{ctree = _parse_node(child)};
    R --> S{cdict = _make_dict(ctag, ctree)};
    S --> T{Если ctree, то value = ''};
    T --> U{Если ctag нет в tree};
    U -- Да --> V{tree.update(cdict)};
    V --> O;
    U -- Нет --> W{old = tree[ctag]};
    W --> X{Если old не list, то tree[ctag] = [old]};
    X --> Y{tree[ctag].append(ctree)};
    Y --> O;
    O -- Дочерних элементов нет --> Z{Если not has_child, то tree['value'] = value};
    Z --> AA{Если list(tree.keys()) == ['value'], то tree = tree['value']};
    AA --> BB[return tree];
    E --> BB;
```

### 2. Диаграмма
```mermaid
graph TD
    A[xml2dict(xml: str) -> dict] --> B(ET.fromstring(xml));
    B --> C[ET2dict(element_tree: ET.Element) -> dict];
    C --> D[_make_dict(tag: str, value: any) -> dict];
    D --> E[re.compile(r"\{(.*)\}(.*)").search(tag)];
    E -- Match --> F{tag_values = {'value': value}, tag_values['xmlns'], tag = result.groups()};
    E -- No Match --> G{tag_values = value};
    F --> H{return {tag: tag_values}};
    G --> H;
    C --> I[_parse_node(node: ET.Element) -> dict | str];
    I --> J{tree = {}, attrs = {}};
    J --> K{for attr_tag, attr_value in node.attrib.items()};
    K -- Attributes --> L{if attr_tag == '{http://www.w3.org/1999/xlink}href': continue};
    L -- Not href --> M{attrs.update(_make_dict(attr_tag, attr_value))};
    M --> K;
    K -- No Attributes --> N{value = node.text.strip() if node.text is not None else ''};
    N --> O{if attrs: tree['attrs'] = attrs};
    O --> P{has_child = False};
    P --> Q{for child in list(node)};
    Q -- Children --> R{has_child = True};
    R --> S{ctag = child.tag};
    S --> T{ctree = _parse_node(child)};
    T --> U{cdict = _make_dict(ctag, ctree)};
    U --> V{if ctree: value = ''};
    V --> W{if ctag not in tree};
    W -- Not in tree --> X{tree.update(cdict)};
    X --> Q;
    W -- In tree --> Y{old = tree[ctag]};
    Y --> Z{if not isinstance(old, list): tree[ctag] = [old]};
    Z --> AA{tree[ctag].append(ctree)};
    AA --> Q;
    Q -- No Children --> BB{if not has_child: tree['value'] = value};
    BB --> CC{if list(tree.keys()) == ['value']: tree = tree['value']};
    CC --> DD{return tree};
    I --> DD;
    H --> DD;
```

**Зависимости:**

-   `xml2dict` зависит от `ET2dict` для преобразования XML в словарь.
-   `ET2dict` зависит от `_make_dict` и `_parse_node`.
-   `_parse_node` рекурсивно вызывает саму себя для обработки дочерних узлов XML.
-   `_make_dict` использует `re.compile` для обработки пространств имен XML.

### 3. Объяснение

**Импорты:**

-   `re`: Модуль для работы с регулярными выражениями, используется в функции `_make_dict` для извлечения информации о пространстве имен из тегов XML.
-   `xml.etree.cElementTree as ET`: Попытка импортировать модуль `cElementTree` для быстрой обработки XML. Если не удается (например, отсутствует), импортируется стандартный `xml.etree.ElementTree`. Модуль `ET` используется для разбора XML-строк и работы с элементами XML-дерева.

**Функции:**

-   `_parse_node(node: ET.Element) -> dict | str`:
    -   **Аргументы**:
        -   `node`: XML-элемент (`ET.Element`), который нужно преобразовать в словарь.
    -   **Возвращаемое значение**:
        -   `dict | str`: Представление XML-узла в виде словаря или строки.
    -   **Назначение**:
        -   Рекурсивно разбирает XML-узел и его атрибуты, формируя словарь. Если у узла есть атрибуты, они сохраняются в ключе `'attrs'`. Дочерние узлы также рекурсивно разбираются и добавляются в словарь. Если у узла нет атрибутов и дочерних элементов, возвращается только текстовое значение узла.
    -   **Пример**:
        ```xml
        <element attr1="value1">text</element>
        ```
        Результат:
        ```python
        {'element': {'attrs': {'attr1': 'value1'}, 'value': 'text'}}
        ```

-   `_make_dict(tag: str, value: any) -> dict`:
    -   **Аргументы**:
        -   `tag`: Имя тега XML-элемента (`str`).
        -   `value`: Значение, связанное с тегом (`any`).
    -   **Возвращаемое значение**:
        -   `dict`: Словарь с именем тега в качестве ключа и значением в качестве значения словаря.
    -   **Назначение**:
        -   Создает словарь, где ключ — это имя тега, а значение — это переданное значение. Если в теге обнаружено пространство имен (например, `{http://www.w3.org/1999/xlink}href`), извлекает информацию о пространстве имен и добавляет её в словарь.
    -   **Пример**:
        ```python
        _make_dict('tag', 'value')
        ```
        Результат:
        ```python
        {'tag': 'value'}
        ```

-   `xml2dict(xml: str) -> dict`:
    -   **Аргументы**:
        -   `xml`: XML-строка (`str`), которую нужно разобрать.
    -   **Возвращаемое значение**:
        -   `dict`: Словарь, представляющий XML.
    -   **Назначение**:
        -   Преобразует XML-строку в словарь. Использует `ET.fromstring` для разбора XML-строки в дерево элементов, а затем вызывает `ET2dict` для преобразования дерева в словарь.
    -   **Пример**:
        ```python
        xml2dict('<root><element>text</element></root>')
        ```
        Результат:
        ```python
        {'root': {'element': {'value': 'text'}}}
        ```

-   `ET2dict(element_tree: ET.Element) -> dict`:
    -   **Аргументы**:
        -   `element_tree`: XML-дерево элементов (`ET.Element`), которое нужно преобразовать в словарь.
    -   **Возвращаемое значение**:
        -   `dict`: Словарь, представляющий XML-дерево элементов.
    -   **Назначение**:
        -   Преобразует XML-дерево элементов в словарь. Вызывает `_make_dict` с корневым тегом дерева и результатом `_parse_node` для преобразования дерева в словарь.
    -   **Пример**:
        ```python
        root = ET.fromstring('<root><element>text</element></root>')
        ET2dict(root)
        ```
        Результат:
        ```python
        {'root': {'element': {'value': 'text'}}}
        ```

**Переменные:**

-   `tree`: Используется в `_parse_node` для построения словаря, представляющего XML-узел.
-   `attrs`: Используется в `_parse_node` для хранения атрибутов XML-узла.
-   `value`: Используется в `_parse_node` для хранения текстового значения XML-узла.
-   `has_child`: Используется в `_parse_node` для отслеживания, есть ли у XML-узла дочерние элементы.
-   `ctag`: Используется в `_parse_node` для хранения тега дочернего элемента.
-   `ctree`: Используется в `_parse_node` для хранения результата рекурсивного вызова `_parse_node` для дочернего элемента.
-   `cdict`: Используется в `_parse_node` для хранения результата вызова `_make_dict` для дочернего элемента.
-   `old`: Используется в `_parse_node` для хранения предыдущего значения тега при обработке повторяющихся тегов.
-   `tag_values`: Используется в `_make_dict` для хранения значения тега.
-   `result`: Используется в `_make_dict` для хранения результата поиска регулярного выражения в теге.
-   `element_tree`: Используется в `xml2dict` и `ET2dict` для хранения XML-дерева элементов.

**Потенциальные ошибки и области для улучшения:**

-   Обработка атрибута `href`: Атрибуты `href` (с пространством имен `http://www.w3.org/1999/xlink`) игнорируются. Возможно, стоит добавить опциональную обработку этих атрибутов.
-   Обработка пространств имен: Код обрабатывает пространства имен, но обработка может быть улучшена для более сложных случаев.
-   Отсутствие обработки исключений: В функциях не предусмотрена обработка исключений, которые могут возникнуть при разборе XML (например, при некорректном XML).
-   Излишняя сложность: Функция `_parse_node` довольно сложная и может быть упрощена для повышения читаемости и производительности.

**Взаимосвязи с другими частями проекта:**

Данный модуль предоставляет утилиты для преобразования XML в словари, которые могут использоваться в других частях проекта `hypotez`, где требуется обработка XML-данных. Например, модуль может использоваться для разбора конфигурационных файлов в формате XML или для обработки данных, полученных из внешних источников в формате XML.