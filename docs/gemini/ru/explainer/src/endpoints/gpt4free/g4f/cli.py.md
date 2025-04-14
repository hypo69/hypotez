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

### Анализ кода `hypotez/src/endpoints/gpt4free/g4f/cli.py`

#### 1. Блок-схема

```mermaid
graph LR
    A[Начало: Запуск скрипта cli.py] --> B{Определение парсера аргументов argparse.ArgumentParser}
    B --> C{Определение подпарсеров: "api" и "gui"}
    C --> D{Парсинг аргументов командной строки}
    D --> E{Проверка режима (args.mode)}
    E -- Режим "api" --> F[Вызов run_api_args(args)]
    E -- Режим "gui" --> G[Вызов run_gui_args(args)]
    E -- Иначе --> H[Вывод справки парсера]
    F --> I[Импорт AppConfig и run_api из g4f.api]
    I --> J[Настройка AppConfig с аргументами командной строки]
    J --> K{Проверка аргумента cookie_browsers}
    K -- Есть аргумент cookie_browsers --> L[Замена g4f.cookies.browsers на основе аргумента]
    K -- Нет аргумента cookie_browsers --> M[Пропуск]
    L --> N[Вызов run_api с аргументами командной строки]
    M --> N
    G --> O[Вызов run_gui_args(args) - функция из g4f.gui.run]
    H --> P[Выход с кодом ошибки 1]
    N --> Q[Завершение работы API]
    O --> R[Завершение работы GUI]
    P --> S[Завершение]
    Q --> S
    R --> S
    S[Завершение]
```

Примеры для каждого логического блока:

- **A**: `python cli.py api --port 8080 --debug`
- **B**: Создание объекта `argparse.ArgumentParser` для описания аргументов командной строки.
- **C**: Добавление подпарсеров `api` и `gui`, каждый со своим набором аргументов.
- **D**: `args = parser.parse_args()` - получение значений аргументов, переданных пользователем.
- **E**: `if args.mode == "api":` - проверка, запущен ли скрипт в режиме `api` или `gui`.
- **F**: `run_api_args(args)` - вызов функции для запуска API с переданными аргументами.
- **G**: `run_gui_args(args)` - вызов функции для запуска GUI с переданными аргументами.
- **H**: `parser.print_help()` - вывод справки, если режим не указан или указан неверно.
- **I**: `from g4f.api import AppConfig, run_api` - импорт необходимых компонентов для запуска API.
- **J**: `AppConfig.set_config(...)` - настройка конфигурации API на основе аргументов командной строки.
- **K**: `if args.cookie_browsers:` - проверка, указаны ли браузеры для извлечения cookie.
- **L**: `g4f.cookies.browsers = [...]` - замена списка браузеров для cookie на основе аргументов.
- **M**: Пропуск, если `cookie_browsers` не указаны.
- **N**: `run_api(...)` - запуск API с указанными параметрами.
- **O**: `run_gui_args(args)` - запуск GUI.
- **P**: `exit(1)` - завершение программы с кодом ошибки.
- **Q**: Завершение работы API.
- **R**: Завершение работы GUI.
- **S**: Завершение программы.

#### 2. Диаграмма

```mermaid
flowchart TD
    A[argparse.ArgumentParser] --> B(subparsers.add_parser("api"))
    A --> C(subparsers.add_parser("gui"))
    B --> D{get_api_parser()}
    C --> E{gui_parser()}
    D --> F(api_parser.add_argument)
    E --> G(gui_parser.add_argument)
    F --> H(g4f.Provider)
    G --> I(run_gui_args)
    A --> J{parser.parse_args()}
    J --> K{args.mode == "api"}
    K -- True --> L{run_api_args(args)}
    K -- False --> M{args.mode == "gui"}
    M -- True --> N{run_gui_args(args)}
    M -- False --> O{parser.print_help()}
    L --> P{g4f.api.AppConfig}
    L --> Q{g4f.api.run_api}
    P --> R(AppConfig.set_config)
    Q --> S(run_api)
```

**Объяснение зависимостей:**

-   `argparse`: Используется для создания парсера аргументов командной строки.  
    `ArgumentParser` - основной класс, который позволяет определять, какие аргументы принимает скрипт.  
    `add_argument` - метод, используемый для добавления отдельных аргументов с их параметрами (например, `--port`, `--debug`).  
    `parse_args` - метод, который анализирует аргументы командной строки и возвращает объект, содержащий значения этих аргументов.
-   `g4f.Provider`: Используется для получения списка доступных провайдеров для chat completion и image generation.
-   `g4f.gui.run`: Модуль, содержащий функции для запуска графического интерфейса (GUI).
-   `g4f.api`: Модуль, содержащий функции для запуска API.
-   `g4f.cookies`: Модуль, содержащий функции для работы с cookie браузеров.
-   `run_api_args`: Функция для запуска API на основе аргументов командной строки.
-   `run_gui_args`: Функция для запуска GUI на основе аргументов командной строки.

#### 3. Объяснение

**Импорты:**

-   `from __future__ import annotations`: Позволяет использовать аннотации типов, в том числе ссылки на классы, которые еще не определены.
-   `import argparse`: Модуль для парсинга аргументов командной строки.
-   `from argparse import ArgumentParser`: Импорт класса `ArgumentParser` из модуля `argparse`.
-   `from g4f import Provider`: Импорт класса `Provider` из библиотеки `g4f`, который используется для работы с различными поставщиками языковых моделей.
-   `from g4f.gui.run import gui_parser, run_gui_args`: Импорт `gui_parser` (парсер аргументов для GUI) и `run_gui_args` (функция для запуска GUI) из модуля `g4f.gui.run`.
-   `import g4f.cookies`: Импорт модуля для работы с cookies.

**Классы:**

В данном коде классы не определены, но используются:

-   `argparse.ArgumentParser`: Класс для создания парсера аргументов командной строки.
-   `g4f.Provider`: Класс, представляющий провайдера языковой модели.
-   `g4f.api.AppConfig`: Класс для конфигурации API.

**Функции:**

-   `get_api_parser() -> ArgumentParser`:
    -   Создает и возвращает парсер аргументов для режима `api`.
    -   Использует `argparse.ArgumentParser` для определения аргументов командной строки, таких как `--bind`, `--port`, `--debug`, `--model`, `--provider`, `--proxy`, `--workers`, `--disable-colors`, `--ignore-cookie-files`, `--g4f-api-key`, `--ignored-providers`, `--cookie-browsers`, `--reload`, `--ssl-keyfile`, `--ssl-certfile`, `--log-config`.
    -   Аргументы используются для настройки API, например, указание порта, включение режима отладки, выбор модели и провайдера.
    -   Пример:
        ```python
        parser = get_api_parser()
        args = parser.parse_args(['--port', '8080', '--debug'])
        print(args.port)  # Вывод: 8080
        print(args.debug) # Вывод: True
        ```
-   `main() -> None`:
    -   Главная функция, точка входа в программу.
    -   Создает основной парсер аргументов и добавляет подпарсеры `api` и `gui`.
    -   В зависимости от режима, выбранного пользователем (`args.mode`), вызывает `run_api_args` или `run_gui_args`.
    -   Если режим не указан, выводит справку.
    -   Пример:
        ```bash
        python cli.py api --port 8080
        python cli.py gui
        python cli.py # Вывод справки
        ```
-   `run_api_args(args: argparse.Namespace) -> None`:
    -   Настраивает и запускает API на основе аргументов командной строки.
    -   Импортирует `AppConfig` и `run_api` из `g4f.api`.
    -   Устанавливает конфигурацию `AppConfig` с помощью аргументов, переданных из командной строки (`args`).
    -   Запускает API с использованием функции `run_api`, передавая ей соответствующие аргументы.
    -   Пример:
        ```python
        # Пример использования (предполагается, что args уже содержит значения)
        import argparse
        class Args:
            ignore_cookie_files: bool = False
            ignored_providers: list[str] = []
            g4f_api_key: str | None = None
            provider: str | None = None
            image_provider: str | None = None
            proxy: str | None = None
            model: str | None = None
            gui: bool = False
            demo: bool = False
            cookie_browsers: list[str] = []
            bind: str | None = None
            port: int | None = None
            debug: bool = False
            workers: int | None = None
            disable_colors: bool = False
            reload: bool = False
            ssl_keyfile: str | None = None
            ssl_certfile: str | None = None
            log_config: str | None = None

        args = Args()
        args.port = 8080
        args.debug = True

        run_api_args(args)
        ```

**Переменные:**

-   `parser: argparse.ArgumentParser`: Основной парсер аргументов командной строки.
-   `subparsers: argparse._SubParsersAction`: Объект для добавления подпарсеров (`api` и `gui`).
-   `args: argparse.Namespace`: Объект, содержащий значения аргументов командной строки, распарсенные с помощью `parser.parse_args()`.
-   `api_parser: argparse.ArgumentParser`: Парсер аргументов для режима `api`.

**Потенциальные ошибки и области для улучшения:**

-   Отсутствует обработка исключений при запуске API и GUI.
-   Не все аргументы командной строки имеют проверку типов.
-   Не документированы все функции и классы.
-   Жестко заданные значения по умолчанию для некоторых аргументов.
-   Отсутствует логирование работы приложения.

**Взаимосвязи с другими частями проекта:**

-   `g4f.api`: Используется для запуска API, который, вероятно, предоставляет интерфейс для взаимодействия с языковыми моделями.
-   `g4f.gui.run`: Используется для запуска графического интерфейса, который может предоставлять удобный способ взаимодействия с языковыми моделями.
-   `g4f.Provider`: Используется для выбора и настройки провайдеров языковых моделей.
-   `g4f.cookies`: Используется для работы с cookies, что может быть необходимо для аутентификации и авторизации при использовании API.

Этот скрипт (`cli.py`) является точкой входа в приложение и отвечает за парсинг аргументов командной строки и запуск соответствующих режимов (API или GUI). Он тесно связан с модулями `g4f.api`, `g4f.gui.run`, `g4f.Provider` и `g4f.cookies`.