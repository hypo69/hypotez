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

### Анализ кода файла `hypotez/src/endpoints/bots/telegram/digital_market/bot/migration/env.py`

#### 1. Блок-схема
```mermaid
flowchart LR
    A[Начало] --> B{context.is_offline_mode()};
    B -- Да --> C[run_migrations_offline()];
    B -- Нет --> D[run_migrations_online()];
    D --> E[asyncio.run(run_async_migrations())];
    E --> F[async_engine_from_config(...)];
    F --> G[connectable.connect()];
    G --> H[connection.run_sync(do_run_migrations)];
    H --> I[context.configure(connection=connection, target_metadata=target_metadata)];
    I --> J[context.begin_transaction()];
    J --> K[context.run_migrations()];
    K --> L[Конец];
    C --> M[url = config.get_main_option("sqlalchemy.url")];
    M --> N[context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})];
    N --> O[context.begin_transaction()];
    O --> P[context.run_migrations()];
    P --> L;
```

**Примеры для каждого логического блока:**

- **A[Начало]**: Начало выполнения скрипта миграции.
- **B{context.is_offline_mode()}**: Проверка, запущен ли скрипт в режиме оффлайн.
  - `Да`: Миграции выполняются без подключения к базе данных.
  - `Нет`: Миграции выполняются с подключением к базе данных.
- **C[run_migrations_offline()]**: Выполнение миграций в режиме оффлайн.
  - `url = config.get_main_option("sqlalchemy.url")`: Получение URL базы данных из конфигурации. Пример: `url = "postgresql://user:password@host:port/database"`
  - `context.configure(...)`: Конфигурирование контекста Alembic с URL и метаданными.
  - `context.run_migrations()`: Запуск миграций.
- **D[run_migrations_online()]**: Выполнение миграций в режиме онлайн.
- **E[asyncio.run(run_async_migrations())]**: Запуск асинхронных миграций.
- **F[async_engine_from_config(...)]**: Создание асинхронного движка SQLAlchemy из конфигурации.
  - Пример: `connectable = async_engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)`
- **G[connectable.connect()]**: Установление соединения с базой данных.
- **H[connection.run_sync(do_run_migrations)]**: Запуск синхронных миграций в асинхронном контексте.
- **I[context.configure(connection=connection, target_metadata=target_metadata)]**: Конфигурирование контекста Alembic с соединением и метаданными.
- **J[context.begin_transaction()]**: Начало транзакции базы данных.
- **K[context.run_migrations()]**: Запуск миграций.
- **L[Конец]**: Завершение выполнения скрипта миграции.
- **M[url = config.get_main_option("sqlalchemy.url")]**: Получение URL базы данных из конфигурации.
- **N[context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})]**: Конфигурирование контекста Alembic для оффлайн режима.
- **O[context.begin_transaction()]**: Начало транзакции базы данных.
- **P[context.run_migrations()]**: Запуск миграций.

#### 2. Диаграмма

```mermaid
flowchart TD
    A[Start] --> B{is_offline_mode};
    B -- Yes --> OfflineMigration[run_migrations_offline];
    B -- No --> OnlineMigration[run_migrations_online];

    OfflineMigration --> GetDBUrl[Get database_url from config];
    GetDBUrl --> ConfigureContextOffline[Configure Alembic context for offline];
    ConfigureContextOffline --> RunMigrationsOffline[Run migrations];

    OnlineMigration --> RunAsyncMigrations[asyncio.run(run_async_migrations)];
    RunAsyncMigrations --> CreateAsyncEngine[Create async engine from config];
    CreateAsyncEngine --> ConnectToDB[Connect to database];
    ConnectToDB --> RunSyncMigrations[connection.run_sync(do_run_migrations)];
    RunSyncMigrations --> ConfigureContextOnline[Configure Alembic context for online];
    ConfigureContextOnline --> RunMigrationsOnline[Run migrations];

    RunMigrationsOffline --> End;
    RunMigrationsOnline --> End;

    subgraph Offline Mode
    GetDBUrl
    ConfigureContextOffline
    RunMigrationsOffline
    end

    subgraph Online Mode
    RunAsyncMigrations
    CreateAsyncEngine
    ConnectToDB
    RunSyncMigrations
    ConfigureContextOnline
    RunMigrationsOnline
    end

    End[End];
```

**Объяснение зависимостей:**

- `sys`: Используется для модификации пути поиска модулей.
- `os.path`: Используется для работы с путями к файлам и директориям.
- `asyncio`: Используется для поддержки асинхронного программирования.
- `logging.config`: Используется для настройки логирования из файла конфигурации.
- `sqlalchemy`: Используется для работы с базой данных.
  - `pool`: Управление пулом соединений.
  - `engine`: Подключение к базе данных.
  - `ext.asyncio`: Асинхронная поддержка SQLAlchemy.
- `alembic`: Инструмент для миграций базы данных.
  - `context`: Предоставляет контекст для операций миграции.
- `bot.dao.database`: Содержит настройки базы данных, включая URL и базовый класс для моделей.
- `bot.dao.models`: Определяет модели базы данных (Product, Purchase, User, Category).

#### 3. Объяснение

**Импорты:**

- `import sys`: Модуль `sys` предоставляет доступ к некоторым переменным и функциям, взаимодействующим с интерпретатором Python. Здесь используется для добавления пути к директории проекта в `sys.path`, чтобы можно было импортировать модули из других частей проекта.
- `from os.path import dirname, abspath`: Модуль `os.path` предоставляет функции для работы с путями к файлам. `dirname` возвращает имя директории, а `abspath` возвращает абсолютный путь.
- `sys.path.insert(0, dirname(dirname(abspath(__file__))))`: Добавляет корневую директорию проекта в `sys.path`. Это позволяет импортировать модули из других частей проекта, например, `bot.dao.database` и `bot.dao.models`.
- `import asyncio`: Модуль `asyncio` используется для асинхронного программирования. Он позволяет запускать несколько задач параллельно.
- `from logging.config import fileConfig`: Модуль `logging.config` позволяет настраивать логирование из файла конфигурации.
- `from sqlalchemy import pool`: Модуль `sqlalchemy` используется для работы с базами данных. `pool` управляет пулом соединений, что позволяет эффективно использовать соединения с базой данных.
- `from sqlalchemy.engine import Connection`: `Connection` представляет собой соединение с базой данных, используемое для выполнения запросов.
- `from sqlalchemy.ext.asyncio import async_engine_from_config`: `async_engine_from_config` создает асинхронный движок SQLAlchemy из конфигурации.
- `from alembic import context`: Модуль `alembic` используется для миграций базы данных. `context` предоставляет контекст для операций миграции.
- `from bot.dao.database import Base, database_url`: Импортирует `Base` и `database_url` из модуля `bot.dao.database`. `Base` является базовым классом для моделей SQLAlchemy, а `database_url` содержит URL для подключения к базе данных.
- `from bot.dao.models import Product, Purchase, User, Category`: Импортирует модели базы данных: `Product`, `Purchase`, `User` и `Category`.

**Переменные:**

- `config = context.config`: Получает объект конфигурации Alembic.
- `target_metadata = Base.metadata`: Устанавливает метаданные, которые Alembic будет использовать для определения изменений в схеме базы данных. `Base.metadata` содержит информацию о структуре таблиц, определенных в моделях SQLAlchemy.

**Функции:**

- `run_migrations_offline() -> None`:
  - Запускает миграции в "оффлайн" режиме, то есть без подключения к базе данных.
  - `url = config.get_main_option("sqlalchemy.url")`: Получает URL базы данных из конфигурации.
  - `context.configure(...)`: Настраивает контекст Alembic с URL базы данных и метаданными.
  - `context.begin_transaction()`: Начинает транзакцию.
  - `context.run_migrations()`: Запускает миграции.
- `do_run_migrations(connection: Connection) -> None`:
  - Выполняет миграции, используя предоставленное соединение с базой данных.
  - `context.configure(connection=connection, target_metadata=target_metadata)`: Настраивает контекст Alembic с соединением и метаданными.
  - `context.begin_transaction()`: Начинает транзакцию.
  - `context.run_migrations()`: Запускает миграции.
- `run_async_migrations() -> None`:
  - Запускает миграции в асинхронном режиме.
  - `connectable = async_engine_from_config(...)`: Создает асинхронный движок SQLAlchemy из конфигурации.
  - `async with connectable.connect() as connection`: Устанавливает асинхронное соединение с базой данных.
  - `await connection.run_sync(do_run_migrations)`: Запускает синхронные миграции в асинхронном контексте.
  - `await connectable.dispose()`: Закрывает соединение с базой данных.
- `run_migrations_online() -> None`:
  - Запускает асинхронные миграции, используя `asyncio.run()`.
  - `asyncio.run(run_async_migrations())`: Запускает асинхронные миграции.

**Логика работы:**

Скрипт `env.py` определяет, как Alembic должен подключаться к базе данных и выполнять миграции. Он поддерживает два режима работы:

- **Оффлайн**: Миграции выполняются без подключения к базе данных. Это полезно для генерации SQL-скриптов, которые затем могут быть выполнены вручную.
- **Онлайн**: Миграции выполняются с подключением к базе данных. Это позволяет Alembic автоматически применять изменения к схеме базы данных.

Скрипт определяет функции для запуска миграций в обоих режимах. В онлайн режиме используется асинхронное программирование для подключения к базе данных и выполнения миграций.

**Потенциальные ошибки и области для улучшения:**

- **Обработка ошибок**: В коде отсутствует явная обработка ошибок. Если при выполнении миграций возникнет ошибка, скрипт завершится с исключением. Следует добавить обработку исключений, чтобы обеспечить более надежную работу скрипта.
- **Логирование**: В коде отсутствует логирование. Следует добавить логирование, чтобы можно было отслеживать ход выполнения миграций и выявлять ошибки.

**Взаимосвязи с другими частями проекта:**

- `bot.dao.database`: Этот модуль определяет настройки подключения к базе данных и базовый класс для моделей. Скрипт `env.py` использует этот модуль для получения URL базы данных и метаданных моделей.
- `bot.dao.models`: Этот модуль определяет модели базы данных. Скрипт `env.py` использует эти модели для определения изменений в схеме базы данных.