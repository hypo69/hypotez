# 🧠 CODE_RULES.RU.v0.2.0

**Проект:** hypotez
**Версия:** 0.2.0
**Автор:** hypo69
**Лицензия:** MIT ([https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT))
**Дата:** 2025

---

## ⚙️ 0. Общие сведения

Этот документ определяет **единые стандарты кодирования и документирования** для всех модулей проекта **hypotez**.
Инструкция охватывает форматы заголовков файлов, docstring/docblock для функций и классов, принципы именования, работу с JSON, логирование и обязательные правила чистоты кода.

---

## 🔖 1. Общие правила форматирования кода

1. Все файлы кодируются в **UTF-8**.
2. В коде запрещено использование глобальных переменных — они выносятся в класс `Config`.
3. Все импорты выравниваются и упорядочиваются:

   ```python
   from header import __root__
   from src import gs
   from src.logger import logger
   from src.utils.printer import pprint
   from src.utils.json import j_loads, j_loads_ns, j_dumps, save_text_file, read_text_file
   ```
4. Все функции объявляют переменные **в начале** тела функции.
5. Проверка условий всегда в формате `if not ...: return`.
6. Для проверки отсутствия данных используется `if not data`, **не** `if data is None`.
7. Строки с `...` являются маркерами отладки и **не изменяются**.
8. **JSON** и файловые операции выполняются только через:

   * `j_loads`, `j_loads_ns` — для чтения;
   * `j_dumps`, `save_text_file` — для записи.
     Эти функции логируют ошибки автоматически и создают директории при необходимости.
9. Вызовы `j_loads` / `save_text_file` требуют проверки результата, но **не оборачиваются в try/except**.
10. **Логирование** только через `logger` из `src.logger.logger`:

    ```python
    logger.error("Ошибка чтения файла", ex, exc_info=True)
    ```
11. **Вывод** — только через `pprint` из `src.utils.printer`.
12. **Timestamp** получаем только через `gs.now`.
13. Для WordPress или Web-файлов можно указывать дополнительный тег:

    ```
    # Platform: WordPress
    ```
14. Комментарии, начинающиеся с `#`, **никогда не изменяются** — это служебные строки.
15. Примеры в docstring обязаны быть **рабочими** и минимальными.
16. В коде допускаются только **типовые аннотации**.
17. Все модули импортируются относительно `__root__`, который задаётся в `header.py`.
18. **Блоки ReStructuredText** вида:

    ```rst
    .. module:: ...
    ```

    или заключённые в

    ````
    ```rst
    ...
    ````

    ```
    **запрещены**.  
    Если такие блоки встречаются — их необходимо **удалить полностью**.  
    Использовать только стандартные docstring (`"""..."""`) или docblock (`/** ... */`).  
    ```

---

## 🧩 2. Шапки файлов (`hypo69 header`)

Структура заголовка обязательна для всех файлов проекта.
Она содержит назначение, примеры, а также обязательные мета-данные (имя файла, проект, автор, лицензия и год).

---

### 🐍 Python

```python
# -*- coding: utf-8 -*-
# =============================================================================
# Название процесса: <Название логического процесса или модуля>
# =============================================================================
# Описание:
#   <Подробно опиши назначение модуля, его классов и функций>
#   <Укажи, какие пакеты или API используются>
#
# Примеры:
#   >>> from src.module import ClassName
#   >>> ClassName().execute()
#
# File: <имя_файла.py>
# Project: <Project Name>
# Package: <PackageName>
# Module: <ModuleName>
# Class: <ClassName>
# Function: <FunctionName>
# Author: hypo69
# License: MIT (https://opensource.org/licenses/MIT)
# Copyright: © 2025 hypo69
# =============================================================================
```

---

### 🧱 PHP

```php
<?php
# -*- coding: utf-8 -*-
# =============================================================================
# Название процесса: <Название логического процесса или блока логики>
# =============================================================================
# Описание:
#   <Опиши подробно, что делает код, какие хуки, фильтры или функции реализует>
#   <Если файл связан с WordPress — укажи контекст использования>
#
# Примеры:
#   1. Как вызвать функцию:
#        add_action('wp_footer', 'custom_footer_text');
#   2. Как расширить функционал:
#        include_once get_stylesheet_directory() . '/custom-functions.php';
#
# File: <имя_файла.php>
# Project: <Project name, например Neve Child Theme>
# IF Package - Package: <PackageName>
# IF Module  - Module: <ModuleName>
# IF Class   - Class: <ClassName>
# IF Function- Function: <FunctionName>
# Author: hypo69
# License: MIT (https://opensource.org/licenses/MIT)
# Copyright: © 2025 hypo69
# =============================================================================
```

---

### ⚙️ JavaScript / TypeScript

```javascript
/**
 * =============================================================================
 * Название процесса: <Название логического процесса или скрипта>
 * =============================================================================
 * Описание:
 *   <Опиши подробно назначение кода, ключевые функции, взаимодействие с DOM или API>
 *   <Если код подключается к WordPress, укажи место вызова>
 *
 * Примеры:
 *   document.addEventListener('DOMContentLoaded', () => {
 *       console.log('Script initialized');
 *   });
 *
 * File: <имя_файла.js/ts>
 * Project: <Project Name>
 * Module: <ModuleName>
 * Class: <ClassName>
 * Function: <FunctionName>
 * Author: hypo69
 * License: MIT (https://opensource.org/licenses/MIT)
 * Copyright: © 2025 hypo69
 * =============================================================================
 */
```

---

### 🧩 HTML

```html
<!--
===============================================================================
Название процесса: <Название логического процесса или шаблона>
===============================================================================
Описание:
    <Подробное описание HTML-фрагмента, его назначения и связей с другими файлами>
    <Если используется в WordPress — укажи, какой шаблон вызывает этот блок>

Примеры:
    <header class="site-header">
        <h1><?php bloginfo('name'); ?></h1>
    </header>

File: <имя_файла.html>
Project: <Project Name>
Module: <ModuleName>
Author: hypo69
License: MIT (https://opensource.org/licenses/MIT)
Copyright: © 2025
===============================================================================
-->
```

---

### 🎨 CSS / SCSS

```css
/*
===============================================================================
Название процесса: <Название набора стилей или логического блока>
===============================================================================
Описание:
    <Опиши, какие классы и элементы оформляются>
    <Укажи область применения — глобальные стили, компоненты или страницы>

Примеры:
    body {
        background-color: #fafafa;
        color: #333;
    }

File: <имя_файла.css/scss>
Project: <Project Name>
Module: <ModuleName>
Author: hypo69
License: MIT (https://opensource.org/licenses/MIT)
Copyright: © 2025
===============================================================================
*/
```

---

## ⚙️ 3. Формат функций и классов (`hypo69 docblock`)

Документация функций и классов оформляется в едином стиле для каждого языка.
Описание всегда начинается с **назначения функции или класса**, далее аргументы, возвращаемое значение, исключения и пример.

---

### 🐍 Python

```python
def function_name(param: str, param1: Optional[int | dict] = None) -> dict | None:
    """! Описание назначения функции

    Args:
        param (str): Основной параметр.
        param1 (Optional[int | dict], optional): Дополнительный параметр. По умолчанию `None`.

    Returns:
        dict | None: Результат выполнения функции.

    Raises:
        SomeError: Если входные данные некорректны.

    Example:
        >>> result = function_name("data", {"opt": 1})
        >>> print(result)
        {'status': 'ok'}
    """
    result: dict = {}
    if not param:
        return None
    ...
    return result
```

---

### ⚙️ JavaScript / TypeScript

```javascript
/**
 * Выполняет основное действие с переданными данными.
 *
 * @param {string} param1 - Основной параметр.
 * @param {number|Object} [param2=null] - Дополнительный параметр.
 * @returns {Object|null} Результат выполнения функции.
 * @throws {Error} Если входные данные некорректны.
 *
 * @example
 * const data = processData("text", 42);
 * console.log(data);
 */
function processData(param1, param2 = null) {
    if (!param1) throw new Error("Некорректный параметр");
    const result = {};
    ...
    return result;
}
```

---

### 🧱 PHP

```php
<?php
/**
 * Выполняет основное действие с переданными данными.
 *
 * @param string $param1 Основной параметр
 * @param int|array|null $param2 Дополнительный параметр
 * @return array|null Результат выполнения функции
 * @throws InvalidArgumentException Если параметры некорректны
 *
 * @example
 * $res = process_data("input", [1, 2]);
 * var_dump($res);
 */
function process_data(string $param1, int|array|null $param2 = null): ?array {
    if (!$param1) {
        throw new InvalidArgumentException("param1 не должен быть пустым");
    }
    $result = [];
    ...
    return $result;
}
```

---

### 🧩 Классы

**Python**

```python
class DataProcessor:
    """! Класс выполняет обработку данных

    Attributes:
        config (dict): Настройки обработки.
        name (str): Имя объекта.
    """

    def __init__(self, config: dict, name: str) -> None:
        """Инициализация экземпляра класса."""
        self.config = config
        self.name = name

    def run(self, data: str) -> bool:
        """Запуск обработки данных."""
        if not data:
            raise ValueError("Пустые данные")
        ...
        return True
```

**JavaScript**

```javascript
class DataProcessor {
    /**
     * @param {Object} config - Конфигурация обработки.
     * @param {string} name - Имя экземпляра.
     */
    constructor(config, name) {
        this.config = config;
        this.name = name;
    }

    /**
     * Запускает обработку данных.
     * @param {string} data - Входные данные.
     * @returns {boolean} Успешность выполнения.
     * @throws {Error} Если данные пустые.
     */
    run(data) {
        if (!data) throw new Error("Пустые данные");
        ...
        return true;
    }
}
```

**PHP**

```php
<?php
class DataProcessor {
    private array $config;
    private string $name;

    public function __construct(array $config, string $name) {
        $this->config = $config;
        $this->name = $name;
    }

    public function run(string $data): bool {
        if (!$data) {
            throw new RuntimeException("Пустые данные");
        }
        ...
        return true;
    }
}
```

---

## 🧩 4. Примеры оформления комментариев

* Комментарий всегда **перед кодом**, который он описывает.
* Использовать чёткие технические формулировки:

  * ✅ «Проверка наличия файла перед чтением»
  * ❌ «Проверяем файл»
* `...` оставляется без изменений.

Примеры:

**Python**

```python
# Проверка наличия файла перед обработкой
if not file_path.exists():
    raise FileNotFoundError(f"Файл не найден: {file_path}")
```

**JavaScript**

```javascript
// Проверка наличия элемента перед вызовом метода
if (!element) throw new Error("Элемент не найден");
```

**PHP**

```php
// Проверка наличия ключа перед обработкой массива
if (!array_key_exists('key', $data)) {
    throw new InvalidArgumentException("Ключ отсутствует");
}
```

---

## 📋 5. Изменения версии 0.1.10

| Раздел        | Изменение                | Описание                           |
| ------------- | ------------------------ | ---------------------------------- |
| Общие правила | ➕ Добавлен пункт о `rst` | Блоки `rst ... ` запрещены         |
| Заголовки     | 🔄 Обновлены             | WAPKI заменён на hypo69 header     |
| DocBlock      | 🔄 Обновлены             | Добавлены унифицированные шаблоны  |
| Структура     | ✅ Единообразие           | Всё выровнено по Markdown и UTF-8  |
| Финал         | 🧩 Полный документ       | Все инструкции собраны в один файл |

