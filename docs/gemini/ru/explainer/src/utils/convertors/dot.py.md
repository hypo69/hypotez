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

### Анализ кода `hypotez/src/utils/convertors/dot.py`

#### 1. Блок-схема:

```mermaid
graph LR
    A[Начало: Получение dot_file (путь к DOT-файлу) и png_file (путь для сохранения PNG-файла)] --> B{Существует ли dot_file?};
    B -- Да --> C[Чтение содержимого dot_file];
    B -- Нет --> E[Вывод сообщения об ошибке: Файл не найден];
    C --> D[Создание объекта Source из содержимого DOT];
    D --> F[Установка формата source в PNG];
    F --> G[Рендеринг source в png_file];
    G --> H[Конец: PNG-файл создан];
    E --> H;
    H -- Готово --> I{Обработка ошибок при рендеринге?};
    I -- Да --> J[Вывод сообщения об ошибке рендеринга];
    I -- Нет --> H;
```

**Примеры для каждого логического блока:**

-   **A**: `dot_file = 'graph.dot'`, `png_file = 'graph.png'`
-   **B**: Проверка, существует ли файл `graph.dot` на диске.
-   **C**: Чтение содержимого файла `graph.dot` в строку.
-   **D**: Создание объекта `graphviz.Source` из содержимого `graph.dot`.
-   **E**: Вывод сообщения в консоль, что файл `graph.dot` не найден.
-   **F**: Установка формата для рендеринга в PNG.
-   **G**: Рендеринг графа и сохранение его в файл `graph.png`.
-   **H**: Завершение процесса.
-   **I**: Проверка, возникла ли ошибка при рендеринге.
-   **J**: Вывод сообщения об ошибке рендеринга в консоль.

#### 2. Диаграмма:

```mermaid
graph TD
    subgraph src.utils.convertors
        dot2png[dot2png(dot_file: str, png_file: str) -> None]
    end

    subgraph graphviz
        Source[Source(dot_content: str)]
    end

    subgraph sys
        sys[sys]
    end
    
    Start --> dot2png
    dot2png --> Source
    dot2png --> sys
    
    style Start fill:#f9f,stroke:#333,stroke-width:2px
```

**Объяснение зависимостей:**

-   Функция `dot2png` использует класс `Source` из библиотеки `graphviz` для создания графа из DOT-контента и его рендеринга в PNG-файл.
-   Функция `dot2png` использует модуль `sys` для обработки аргументов командной строки.

#### 3. Объяснение:

-   **Импорты**:
    -   `import sys`: Используется для доступа к аргументам командной строки, если скрипт запускается как исполняемый.
    -   `from graphviz import Source`: Импортирует класс `Source` из библиотеки `graphviz`. Этот класс используется для представления DOT-графа и его рендеринга в различные форматы, включая PNG.

-   **Классы**:
    -   `graphviz.Source`: Класс, представляющий DOT-граф. Он принимает DOT-контент в виде строки и предоставляет методы для рендеринга графа в различные форматы.

-   **Функции**:
    -   `dot2png(dot_file: str, png_file: str) -> None`:
        -   **Аргументы**:
            -   `dot_file` (str): Путь к входному DOT-файлу.
            -   `png_file` (str): Путь для сохранения выходного PNG-файла.
        -   **Возвращаемое значение**:
            -   `None`: Функция ничего не возвращает.
        -   **Назначение**:
            -   Преобразует DOT-файл в PNG-изображение.
        -   **Пример**:
            -   `dot2png('example.dot', 'output.png')`: Преобразует файл `example.dot` в `output.png`.
        -   **Логика работы**:
            1.  Чтение содержимого DOT-файла.
            2.  Создание объекта `Source` из содержимого DOT-файла.
            3.  Установка формата вывода в PNG.
            4.  Рендеринг графа в PNG-файл.
        -   **Обработка ошибок**:
            -   `FileNotFoundError`: Возникает, если DOT-файл не существует.
            -   `Exception`: Возникает при других ошибках во время преобразования.

-   **Переменные**:
    -   `dot_file` (str): Путь к входному DOT-файлу.
    -   `png_file` (str): Путь для сохранения выходного PNG-файла.
    -   `dot_content` (str): Содержимое DOT-файла, прочитанное как строка.
    -   `source` (graphviz.Source): Объект `Source`, представляющий DOT-граф.

**Потенциальные ошибки и области для улучшения:**

1.  **Отсутствие обработки ошибок Graphviz**: Функция обрабатывает `FileNotFoundError` и общие исключения, но не обрабатывает специфические ошибки, которые может вызвать `graphviz`.
2.  **Логирование**: Отсутствует логирование с использованием модуля `logger` из `src.logger.logger`. Ошибки следует логировать с использованием `logger.error`.
3.  **Обработка аргументов командной строки**: Код проверяет количество аргументов, но не проверяет, существуют ли файлы, указанные в аргументах.

**Цепочка взаимосвязей с другими частями проекта:**

-   Этот модуль (`dot.py`) находится в `src.utils.convertors`, что указывает на его роль как утилиты для преобразования файлов. Он может использоваться другими частями проекта, которым необходимо преобразовывать DOT-файлы в PNG-изображения. Например, он может быть частью системы автоматической генерации документации или визуализации графов зависимостей в проекте.