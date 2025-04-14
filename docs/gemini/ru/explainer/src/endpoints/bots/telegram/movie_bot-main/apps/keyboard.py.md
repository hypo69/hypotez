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

### Анализ кода `hypotez/src/endpoints/bots/telegram/movie_bot-main/apps/keyboard.py`

#### 1. Блок-схема

```mermaid
graph LR
    A[Начало] --> B{Создание InlineKeyboardMarkup "find_movie"};
    B -- "Добавление кнопки 'Найти' с callback_data='new_movies'" --> C{Создание InlineKeyboardMarkup "choice"};
    C -- "Добавление кнопок 'Сериал' и 'Фильм' с соответствующими callback_data" --> D[Конец];
```

**Примеры для каждого логического блока:**

*   **A (Начало)**: Начало выполнения кода, инициализация модуля.
*   **B (Создание InlineKeyboardMarkup "find\_movie")**:
    ```python
    find_movie = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Найти', callback_data='new_movies')]
    ])
    ```
    Здесь создается объект `InlineKeyboardMarkup` с именем `find_movie`. Внутри него добавляется одна кнопка с текстом "Найти" и callback\_data "new\_movies".
*   **C (Создание InlineKeyboardMarkup "choice")**:
    ```python
    choice = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сериал', callback_data='series'),
         InlineKeyboardButton(text='Фильм', callback_data='film')]
    ])
    ```
    Здесь создается объект `InlineKeyboardMarkup` с именем `choice`.  Внутри него добавляются две кнопки: "Сериал" с callback\_data "series" и "Фильм" с callback\_data "film".
*   **D (Конец)**: Конец выполнения кода, переменные с клавиатурами инициализированы.

#### 2. Диаграмма

```mermaid
graph TD
    A[<code>keyboard.py</code><br>Определение InlineKeyboardMarkup]
    A --> B(InlineKeyboardButton)
    A --> C(InlineKeyboardMarkup)
    B --> D[<code>aiogram.types</code>]
    C --> D
```

**Анализ зависимостей:**

*   `InlineKeyboardButton` и `InlineKeyboardMarkup` импортируются из `aiogram.types`.
*   `InlineKeyboardButton` используется для создания отдельных кнопок.
*   `InlineKeyboardMarkup` используется для группировки кнопок в клавиатуру.

#### 3. Объяснение

*   **Импорты**:
    *   `from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup`: Этот импорт предоставляет классы для создания inline-кнопок (`InlineKeyboardButton`) и клавиатур (`InlineKeyboardMarkup`), которые используются в Telegram-ботах для предоставления интерактивных элементов интерфейса.
*   **Переменные**:
    *   `find_movie`: Объект `InlineKeyboardMarkup`, представляющий клавиатуру с одной кнопкой "Найти". Когда пользователь нажимает эту кнопку, боту отправляется callback\_data "new\_movies".
    *   `choice`: Объект `InlineKeyboardMarkup`, представляющий клавиатуру с двумя кнопками: "Сериал" и "Фильм". При нажатии на эти кнопки боту отправляются callback\_data "series" и "film" соответственно.
*   **Функциональность**:

Файл `keyboard.py` определяет два объекта `InlineKeyboardMarkup`, которые представляют собой клавиатуры для Telegram-бота. `find_movie` предоставляет кнопку "Найти", предположительно для поиска фильмов. `choice` предоставляет выбор между "Сериалом" и "Фильмом".  Эти клавиатуры могут быть использованы для управления взаимодействием пользователя с ботом, например, для навигации или фильтрации контента.

*   **Потенциальные улучшения**:
    *   Добавить документацию (docstrings) для каждой переменной, чтобы объяснить их назначение.
    *   Рассмотреть возможность создания функций для генерации клавиатур, чтобы упростить код и избежать дублирования.