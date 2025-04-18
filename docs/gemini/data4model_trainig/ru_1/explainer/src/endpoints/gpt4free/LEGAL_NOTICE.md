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

## Анализ кода `hypotez/src/endpoints/gpt4free/LEGAL_NOTICE.md`

### 1. Блок-схема

Этот файл представляет собой уведомление об отказе от ответственности и юридические условия использования репозитория.

```mermaid
graph LR
    A[Начало] --> B{Отказ от ответственности: Не связан с API-провайдерами};
    B -- Использование в образовательных целях --> C{Ограничение ответственности: Автор не несет ответственности};
    C -- Отсутствие гарантий --> D{Ответственность пользователя: Принятие рисков};
    D -- Соблюдение законодательства --> E{Возмещение ущерба: Защита автора};
    E -- Отсутствие одобрения --> F{Регулирующее право и юрисдикция};
    F --> G{Делимость положений};
    G --> H{Подтверждение понимания};
    H --> I{Обновления и изменения};
    I --> J{Непредвиденные последствия};
    J --> K{Образовательная цель};
    K --> Z[Конец];
```

### 2. Диаграмма

В данном файле отсутствуют импорты, поэтому диаграмма зависимостей не требуется.

### 3. Объяснение

- **Содержание**: Файл `LEGAL_NOTICE.md` содержит юридическое уведомление об отказе от ответственности, ограничениях и условиях использования репозитория `hypotez`. Он определяет границы ответственности автора и пользователей, а также указывает на образовательный характер проекта.

- **Основные положения**:
  - **Отказ от ответственности**: Указывает, что репозиторий не связан с API-провайдерами.
  - **Ограничение ответственности**: Автор не несет ответственности за ущерб, возникший в результате использования репозитория.
  - **Отсутствие гарантий**: Репозиторий предоставляется "как есть" без каких-либо гарантий.
  - **Ответственность пользователя**: Пользователи несут ответственность за риски, связанные с использованием репозитория.
  - **Соблюдение законодательства**: Пользователи должны соблюдать все применимые законы и правила.
  - **Возмещение ущерба**: Пользователи обязуются защищать автора от претензий, связанных с использованием репозитория.
  - **Отсутствие одобрения**: Включение стороннего контента не подразумевает одобрение автора.
  - **Регулирующее право и юрисдикция**: Определяет законы, регулирующие использование репозитория.
  - **Делимость положений**: Если какое-либо положение будет признано недействительным, это не повлияет на остальные положения.
  - **Подтверждение понимания**: Используя репозиторий, пользователи подтверждают, что прочитали, поняли и согласны с условиями.
  - **Обновления и изменения**: Автор оставляет за собой право изменять содержимое репозитория в любое время без предварительного уведомления.
  - **Непредвиденные последствия**: Автор не несет ответственности за последствия использования репозитория.
  - **Образовательная цель**: Проект предназначен исключительно для образовательных целей.

- **Роль в проекте `hypotez`**: Этот файл важен для защиты автора и предоставления пользователям четкого понимания условий использования репозитория. Он определяет правовые рамки проекта и снижает потенциальные риски.

- **Потенциальные области для улучшения**:
  - Уведомление может быть переведено на несколько языков для расширения аудитории.
  - Рассмотрение возможности добавления раздела FAQ для ответа на общие вопросы, связанные с юридическими аспектами.