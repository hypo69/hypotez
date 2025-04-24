# Модуль src.credentials

```rst
.. module:: src.credentials
```

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>

<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/readme.ru.md'>Русский</A>
</TD>
</TABLE>

Данный документ предоставляет обзор класса `ProgramSettings` и связанных с ним функций в модуле `src.credentials`.

## Оглавление

- [Обзор](#обзор)
- [Функции](#функции)
    - [`set_project_root`](#set_project_root)
    - [`singleton`](#singleton)
- [Классы](#классы)
    - [`ProgramSettings`](#programsettings)
        - [Атрибуты класса](#атрибуты-класса)
        - [Принцип работы](#принцип-работы)
        - [Методы класса](#методы-класса)
            - [`__init__`](#__init__)
            - [`_load_credentials`](#_load_credentials)
            - [`_open_kp`](#_open_kp)
            - [`_load_aliexpress_credentials`](#_load_aliexpress_credentials)
            - [`_load_openai_credentials`](#_load_openai_credentials)
            - [`_load_gemini_credentials`](#_load_gemini_credentials)
            - [`_load_telegram_credentials`](#_load_telegram_credentials)
            - [`_load_discord_credentials`](#_load_discord_credentials)
            - [`_load_PrestaShop_credentials`](#_load_prestashop_credentials)
            - [`_load_presta_translations_credentials`](#_load_presta_translations_credentials)
            - [`_load_smtp_credentials`](#_load_smtp_credentials)
            - [`_load_facebook_credentials`](#_load_facebook_credentials)
            - [`_load_gapi_credentials`](#_load_gapi_credentials)
            - [`now`](#now)
- [Управление Учетными Данными с Использованием KeePass](#управление-учетными-данными-с-использованием-keepass)
    - [Что такое KeePass?](#что-такое-keepass)
    - [Чем хорош KeePass?](#чем-хорош-keepass)
    - [Как KeePass Работает в Этом Проекте](#как-keepass-работает-в-этом-проекте)
    - [Структура базы данных `credentials.kdbx`](#структура-базы-данных-credentialskdbx)
- [Глобальный Экземпляр `ProgramSettings`](#глобальный-экземпляр-programsettings)
- [Примечания](#примечания)
- [Возможные исключения](#возможные-исключения)

## Обзор

Модуль `src.credentials` (файл `credentials.py`) управляет стартовыми установками и учетными данными программы `hypotez`. Он отвечает за загрузку и сохранение конфиденциальной информации (ключи API, пароли и т.д.) из зашифрованного файла базы данных KeePass (`credentials.kdbx`). Кроме того, модуль предоставляет функцию `set_project_root` для определения корневого каталога проекта на основе наличия определенных маркерных файлов.

## Функции

### `set_project_root`

**Назначение**: Находит корневую директорию проекта, начиная от директории текущего файла. Функция осуществляет поиск вверх по иерархии директорий до тех пор, пока не обнаружит директорию, содержащую один из указанных в списке `marker_files` файлов или каталогов.

**Параметры**:

-   `marker_files` (tuple, optional): Кортеж строк, представляющих имена файлов или каталогов. Наличие любого из этих маркеров в директории идентифицирует ее как корневую директорию проекта. По умолчанию используются `('__root__', '.git')`.

**Возвращает**:

-   `Path`: Возвращает объект Path, представляющий абсолютный путь к найденной корневой директории проекта. Если ни один из маркерных файлов не найден в родительских директориях до достижения корневой файловой системы, функция возвращает путь к директории, в которой расположен вызывающий скрипт.

**Как работает функция**:

1.  Функция определяет путь к директории, в которой находится текущий скрипт, используя `Path(__file__).resolve().parent`.
2.  Инициализируется переменная `__root__` текущим путем.
3.  Выполняется итерация по текущей директории и всем ее родительским директориям вверх по дереву.
4.  Для каждой директории в итерации проверяется наличие любого из файлов или каталогов, указанных в кортеже `marker_files`.
5.  При обнаружении первого совпадения, текущая директория устанавливается как `__root__`, и итерация прерывается.
6.  Если корневая директория найдена и не находится в `sys.path`, ее путь добавляется в начало `sys.path`, чтобы обеспечить корректный импорт модулей проекта.
7.  Функция возвращает найденный путь к корневой директории проекта.

**Примеры**:

```python
from src.credentials import set_project_root

# Определение корневой директории с использованием маркеров по умолчанию
root_dir = set_project_root()
print(f'Корневая директория проекта: {root_dir}')

# Определение корневой директории с использованием пользовательских маркеров
custom_markers = ('project_marker.txt', 'data')
custom_root_dir = set_project_root(marker_files=custom_markers)
print(f'Корневая директория проекта (с пользовательскими маркерами): {custom_root_dir}')
```

### `singleton`

**Назначение**: Декоратор, предназначенный для преобразования обычного класса в синглтон. Это гарантирует, что для данного класса будет создан только один экземпляр на протяжении всего выполнения программы.

**Параметры**:

-   `cls`: Класс, к которому применяется декоратор.

**Возвращает**:

-   `function`: Возвращает функцию-обертку, которая при каждом вызове возвращает один и тот же экземпляр декорированного класса.

**Как работает функция**:

1.  Декоратор `singleton` применятся к классу (`cls`).
2.  Внутри декоратора создается словарь `instances`, который будет хранить единственные экземпляры классов.
3.  Создается внутренняя функция `wrapper`, которая принимает произвольные позиционные (`*args`) и именованные (`**kwargs`) аргументы.
4.  При вызове `wrapper`, она проверяет, существует ли экземпляр класса `cls` в словаре `instances`.
5.  Если экземпляр не существует, он создается с переданными аргументами (`cls(*args, **kwargs)`) и сохраняется в `instances` по ключу `cls`.
6.  Независимо от того, был ли экземпляр только что создан или уже существовал, `wrapper` возвращает этот единственный экземпляр из словаря `instances`.
7.  Декоратор возвращает функцию `wrapper`, которая заменяет оригинальный класс. Теперь каждый вызов имени класса фактически является вызовом `wrapper`, возвращающей синглтон.

**Примеры**:

```python
from src.credentials import singleton

@singleton
class MySingletonClass:
    def __init__(cls, value):
        cls.value = value
        print(f"Создан экземпляр MySingletonClass с значением: {cls.value}")

# Первый вызов создает экземпляр
instance1 = MySingletonClass(10)
print(f"Значение instance1: {instance1.value}")

# Второй вызов возвращает тот же экземпляр
instance2 = MySingletonClass(20) # __init__ не будет вызван повторно
print(f"Значение instance2: {instance2.value}")

# Проверка, что это один и тот же объект
print(f"instance1 и instance2 являются одним и тем же объектом: {instance1 is instance2}")
```

## Классы

### `ProgramSettings`

**Описание**: Класс `ProgramSettings` инкапсулирует все основные параметры и настройки, необходимые для работы проекта `hypotez`. Он отвечает за загрузку конфигурации из файла `config.json` и, что наиболее важно, за безопасное извлечение и управление учетными данными из зашифрованной базы данных KeePass (`credentials.kdbx`). Этот класс реализован как синглтон, что гарантирует наличие только одного экземпляра настроек и учетных данных на протяжении всего выполнения программы.

**Наследует**: Не наследует явно от других классов.

**Атрибуты**:

-   `host_name` (str): Имя текущего хоста, на котором выполняется программа.
-   `base_dir` (Path): Объект `Path`, указывающий на корневую директорию проекта. Определяется с помощью функции `set_project_root`.
-   `config` (SimpleNamespace): Объект `SimpleNamespace`, содержащий все параметры конфигурации, загруженные из файла `config.json`. Доступ к параметрам осуществляется через атрибуты (например, `self.config.project_name`).
-   `credentials` (SimpleNamespace): Объект `SimpleNamespace`, содержащий все учетные данные, извлеченные из базы данных KeePass. Учетные данные организованы и доступны по путям, соответствующим структуре групп и записей в KeePass (например, `self.credentials.openai.api_key`).
-   `MODE` (str): Строка, определяющая текущий режим работы проекта (например, `'dev'`, `'prod'`, `'debug'`, `'test'`). Значение загружается из конфигурации.
-   `path` (SimpleNamespace): Объект `SimpleNamespace`, содержащий объекты `Path` для различных ключевых директорий проекта, таких как директории для логов, временных файлов, секретов и внешнего хранилища.

**Принцип работы**:

Класс `ProgramSettings` при инициализации выполняет следующие ключевые шаги:

1.  **Определение корневой директории**: Сначала определяется корневая директория проекта путем вызова функции `set_project_root`. Этот путь сохраняется в атрибуте `self.base_dir`.
2.  **Загрузка общей конфигурации**: Загружается файл `config.json`, расположенный в директории `src` относительно корневой директории. Конфигурация десериализуется в объект `SimpleNamespace` и присваивается атрибуту `self.config`. Также устанавливается имя проекта (`self.config.project_name`) на основе имени корневой директории.
3.  **Инициализация путей**: Используя загруженную конфигурацию (`self.config.path`) и корневую директорию (`self.base_dir`), инициализируется объект `SimpleNamespace` (`self.path`) с объектами `Path` для всех необходимых директорий (логи, temp, secrets, external).
4.  **Проверка на наличие новой версии (Placeholder)**: Вызывается метод `check_latest_release` (метод не предоставлен в коде, но упоминается в описании `__init__`), который, вероятно, проверяет наличие более новой версии проекта.
5.  **Загрузка учетных данных из KeePass**: Вызывается приватный метод `_load_credentials`, который отвечает за открытие базы данных KeePass и извлечение всех необходимых учетных данных. Эти данные сохраняются в атрибуте `self.credentials` в структуре, имитирующей дерево групп и записей KeePass.

Весь этот процесс происходит однократно при первом создании экземпляра класса `ProgramSettings` благодаря использованию декоратора `singleton`. Последующие "создания" экземпляра просто возвращают уже существующий объект, обеспечивая единый доступ к настройкам и учетным данным на протяжении всей программы.

**Примеры**:

```python
from src.credentials import ProgramSettings

# Создание (или получение существующего) экземпляра настроек
settings = ProgramSettings()

# Доступ к атрибутам класса
print(f'Имя хоста: {settings.host_name}')
print(f'Режим работы: {settings.MODE}')
print(f'Путь к директории логов: {settings.path.log}')

# Доступ к учетным данным (после их загрузки)
# Предполагая, что учетные данные OpenAI загружены
# openai_api_key = settings.credentials.openai.api_key
# print(f'Ключ API OpenAI: {openai_api_key}')
```

### Методы класса

#### `__init__`

```python
def __init__(cls, **kwargs) -> None:
    """
    Инициализирует единственный экземпляр класса ProgramSettings.

    Метод выполняет последовательную загрузку конфигурации, инициализацию путей
    к директориям проекта, проверку обновлений (placeholder) и загрузку
    учетных данных из базы данных KeePass.

    Args:
        **kwargs: Произвольные именованные аргументы (в текущей реализации не используются).

    Returns:
        None: Метод не возвращает значение.

    Raises:
        Exception: Если происходит ошибка при загрузке настроек из config.json.

    Как работает функция:
        1. Определяет имя хоста.
        2. Определяет корневую директорию проекта, используя `set_project_root`.
        3. Загружает конфигурационный файл `config.json` с использованием `j_loads_ns`.
        4. Выполняет проверку успешности загрузки конфигурации и логирует ошибку при неудаче.
        5. Устанавливает имя проекта из имени корневой директории.
        6. Инициализирует атрибут `path` объектами `Path` для ключевых директорий проекта, используя данные из `config.path`.
        7. Устанавливает режим работы (`MODE`) из конфигурации.
        8. Вызывает метод `check_latest_release` для проверки на наличие обновлений (метод не реализован в предоставленном коде).
        9. Вызывает метод `_load_credentials` для загрузки учетных данных из KeePass.

    Примеры:
        >>> # Инициализация происходит автоматически при первом обращении к классу-синглтону
        >>> settings = ProgramSettings()
        >>> # Дополнительные аргументы игнорируются благодаря реализации синглтона
        >>> settings_again = ProgramSettings(some_arg=123)
    """
    # Определение имени хоста
    cls.host_name:str = socket.gethostname()

    # Определение корневой директории проекта
    cls.base_dir:Path = set_project_root()

    # Загрузка конфигурации из config.json
    # Используется j_loads_ns для загрузки JSON с преобразованием в SimpleNamespace
    cls.config:SimpleNamespace = j_loads_ns(cls.base_dir / 'src' / 'config.json')

    # Проверка успешности загрузки конфигурации
    if not cls.config:
        logger.error('Ошибка при загрузке настроек')
        # ... placeholder для обработки критической ошибки, возможно выход из программы
        return # Метод инициализации не должен возвращать значение, но тут присутствует return

    # Установка имени проекта
    cls.config.project_name:str = cls.base_dir.name

    # Инициализация путей к ключевым директориям
    cls.path:SimpleNamespace = SimpleNamespace(
        log = cls.base_dir / cls.config.path.log,
        temp = cls.base_dir / cls.config.path.temp,
        secrets = cls.base_dir / cls.config.path.secrets,
        external = cls.base_dir / cls.config.path.external
    )
    # Установка режима работы
    cls.MODE:str = cls.config.mode.current

    # Проверка на наличие новой версии (placeholder)
    cls.check_latest_release() # Метод check_latest_release не предоставлен в коде

    # Загрузка учетных данных из KeePass
    cls._load_credentials()
```

#### `_load_credentials`

```python
def _load_credentials(cls) -> None:
    """
    Загружает учетные данные из файла базы данных KeePass.

    Метод инициализирует объект SimpleNamespace для хранения учетных данных,
    открывает базу данных KeePass и последовательно вызывает приватные методы
    для загрузки учетных данных для различных сервисов (Aliexpress, OpenAI,
    Gemini, Telegram, Discord, PrestaShop, SMTP, Facebook, Google API).
    При неудачной загрузке данных для конкретного сервиса логируется
    предупреждение.

    Args:
        Нет параметров для этого метода.

    Returns:
        None: Метод не возвращает значение.

    Raises:
        Может косвенно вызывать исключения из `_open_kp` или методов загрузки
        специфичных учетных данных, которые обрабатываются внутри метода
        (логирование предупреждения).

    Как работает функция:
        1. Инициализирует пустой объект SimpleNamespace `self.credentials`.
        2. Вызывает приватный метод `_open_kp` для открытия базы данных KeePass,
           передавая количество попыток.
        3. Если база данных успешно открыта (`kp` не None), выполняются
           последовательные вызовы методов загрузки учетных данных для каждого
           сервиса (`_load_aliexpress_credentials`, `_load_openai_credentials`,
           и т.д.).
        4. Каждый метод загрузки возвращает булево значение, указывающее на
           успешность операции. При неудаче (метод вернул `False`),
           логируется предупреждение о том, что учетные данные для данного
           сервиса не загружены.
        5. Если база данных KeePass не была успешно открыта, логируется
           критическое сообщение.

    Примеры:
        >>> # Метод вызывается автоматически при инициализации класса ProgramSettings
        >>> settings = ProgramSettings()
        >>> # Учетные данные будут доступны через settings.credentials
        >>> # Например: api_key = settings.credentials.openai.api_key
    """
    # Инициализация объекта для хранения учетных данных
    cls.credentials:SimpleNamespace = SimpleNamespace()

    # Открытие базы данных KeePass с 3 попытками
    kp:PyKeePass | None = cls._open_kp(retry = 3)

    # Загрузка учетных данных для различных сервисов, если база данных открыта
    if kp:
        # Загрузка учетных данных Aliexpress
        if not cls._load_aliexpress_credentials(kp):
            logger.warning('Учетные данные Aliexpress не загружены')

        # Загрузка учетных данных OpenAI
        if not cls._load_openai_credentials(kp):
            logger.warning('Учетные данные OpenAI не загружены')

        # Загрузка учетных данных GoogleAI (Gemini)
        if not cls._load_gemini_credentials(kp):
            logger.warning('Учетные данные GoogleAI не загружены')

        # Загрузка учетных данных Telegram
        if not cls._load_telegram_credentials(kp):
            logger.warning('Учетные данные Telegram не загружены')

        # Загрузка учетных данных Discord
        if not cls._load_discord_credentials(kp):
            logger.warning('Учетные данные Discord не загружены')

        # Загрузка учетных данных PrestaShop
        if not cls._load_PrestaShop_credentials(kp):
            logger.warning('Учетные данные PrestaShop не загружены')

        # Загрузка учетных данных PrestaShop Translations
        if not cls._load_presta_translations_credentials(kp):
            logger.warning('Учетные данные PrestaShop Translations не загружены')

        # Загрузка учетных данных SMTP
        if not cls._load_smtp_credentials(kp):
            logger.warning('Учетные данные SMTP не загружены')

        # Загрузка учетных данных Facebook
        if not cls._load_facebook_credentials(kp):
            logger.warning('Учетные данные Facebook не загружены')

        # Загрузка учетных данных Google API
        if not cls._load_gapi_credentials(kp):
            logger.warning('Учетные данные Google API не загружены')
    else:
        # Логирование критической ошибки, если базу данных не удалось открыть
        logger.critical('Не удалось открыть базу данных KeePass', exc_info=True)

```

#### `_open_kp`

```python
def _open_kp(cls, retry: int = 3) -> PyKeePass | None:
    """
    Открывает базу данных KeePass.

    Метод пытается открыть файл базы данных KeePass (`credentials.kdbx`),
    расположенный в директории секретов (`self.path.secrets`), используя
    мастер-пароль. Пароль считывается из файла `password.txt` в режиме
    разработки или запрашивается у пользователя через консоль в других режимах.
    Метод включает механизм повторных попыток в случае ошибки.

    Args:
        retry (int, optional): Количество попыток, которое будет предпринято
                               для открытия базы данных KeePass. По умолчанию 3.

    Returns:
        PyKeePass | None: Возвращает объект PyKeePass, представляющий открытую
                          базу данных, в случае успеха. Возвращает `None`, если
                          базу данных не удалось открыть после всех попыток.

    Raises:
        BinaryError: При ошибках с бинарными данными KeePass.
        CredentialsError: При ошибках, связанных с учетными данными
                          (например, неверный пароль).
        DefaultSettingsException: При ошибках с настройками по умолчанию
                                  PyKeePass.
        HeaderChecksumError: При ошибках проверки контрольной суммы заголовков.
        KeePassException: Общее исключение PyKeePass.
        PayloadChecksumError: При ошибках проверки контрольной суммы полезной
                              нагрузки.
        UnableToSendToRecycleBin: При ошибках при попытке отправить в корзину
                                  (если настроено).
        Exception: Ловит любые другие необработанные исключения.

    Как работает функция:
        1. Запускает цикл, который повторяется до тех пор, пока количество
           оставшихся попыток `retry` больше нуля.
        2. Внутри цикла пытается:
           a. Считать мастер-пароль из файла `password.txt` в директории
              секретов. Если файл пуст или чтение не удалось, используется
              None.
           b. Если пароль не считан из файла (`password` is None), запросить
              его у пользователя через консоль с использованием `getpass.getpass`.
              Перед запросом выводит приглашение.
           c. Открыть базу данных KeePass (`credentials.kdbx`) по указанному
              пути и с полученным паролем, используя `PyKeePass`.
           d. В случае успешного открытия, возвращает объект `PyKeePass`.
        3. Если при попытке открытия возникает исключение, логирует сообщение
           об ошибке с указанием исключения и оставшихся попыток.
        4. Уменьшает счетчик `retry`.
        5. Если количество попыток исчерпано (`retry < 1`) и базу данных не
           удалось открыть, логирует критическое сообщение и вызывает
           `sys.exit()` для завершения программы.
        6. Если цикл завершился без успешного открытия базы данных (т.е.,
           после исчерпания всех попыток), функция возвращает `None`.

    Примеры:
        >>> # Метод вызывается методом _load_credentials, который в свою очередь
        >>> # вызывается при инициализации ProgramSettings.
        >>> # Прямое использование обычно не требуется.
        >>> # Пример вызова внутри _load_credentials:
        >>> # kp = cls._open_kp(retry=3)
    """
    while retry > 0:
        try:
            # Попытка считать пароль из файла secrets/password.txt
            password:str | None = Path( cls.path.secrets / 'password.txt').read_text(encoding="utf-8") or None
            # Если пароль не считан из файла, запросить через консоль
            if not password:
                 print('Введите мастер-пароль KeePass: ', text_color='blue')
                 password = getpass.getpass().lower()

            # Открытие базы данных KeePass
            kp: PyKeePass = PyKeePass(str(cls.path.secrets / 'credentials.kdbx'),
                                      password = password)
            # Возврат объекта базы данных при успешном открытии
            return kp
        except Exception as ex:
            # Логирование ошибки при неудачной попытке
            print(f"Не удалось открыть базу данных KeePass. Исключение: {ex}, осталось попыток: {retry-1}.")
            # ... placeholder для дополнительной обработки или задержки
            retry -= 1
            # Выход из программы, если попытки исчерпаны
            if retry < 1:
                logger.critical('Не удалось открыть базу данных KeePass после нескольких попыток', exc_info=True)
                # ... placeholder для дополнительной обработки перед выходом
                sys.exit()
    # Возврат None, если базу данных не удалось открыть после всех попыток
    return None
```

#### `_load_aliexpress_credentials`

```python
def _load_aliexpress_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для Aliexpress API из базы данных KeePass.

    Ищет запись в группе 'suppliers/aliexpress/api'. При успешном нахождении
    извлекает и сохраняет в `self.credentials.aliexpress` ключи API, секрет,
    tracking_id, email и пароль.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно в этом методе,
        предполагается их обработка вызывающим методом `_load_credentials`.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'suppliers/aliexpress/api'.
        2. Если запись найдена:
           a. Создает объект SimpleNamespace `self.credentials.aliexpress`.
           b. Извлекает из записи поля 'UserName' (для email), 'Password',
              'Attribute(api_key)', 'Attribute(secret)', 'Attribute(tracking_id)'.
           c. Присваивает извлеченные значения соответствующим атрибутам
              в `self.credentials.aliexpress`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_aliexpress_credentials(kp)
        >>> # После успешной загрузки:
        >>> # api_key = gs.credentials.aliexpress.api_key
    """
    try:
        # Получение записи Aliexpress API
        entry: Entry | None = kp.find_entry_by_path('suppliers/aliexpress/api')
        if entry:
            # Инициализация объекта для учетных данных Aliexpress
            cls.credentials.aliexpress: SimpleNamespace = SimpleNamespace()
            # Извлечение данных из записи KeePass
            cls.credentials.aliexpress.api_key = entry.get_custom_property('api_key')
            cls.credentials.aliexpress.secret = entry.get_custom_property('secret')
            cls.credentials.aliexpress.tracking_id = entry.get_custom_property('tracking_id')
            cls.credentials.aliexpress.email = entry.username
            cls.credentials.aliexpress.password = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись не найдена
            logger.debug('Запись Aliexpress API не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных Aliexpress API: {ex}')
        return False
```

#### `_load_openai_credentials`

```python
def _load_openai_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для OpenAI (API ключи и ID ассистентов)
    из базы данных KeePass.

    Ищет записи в группах 'openai' и 'openai/assistants'. При успешном нахождении
    извлекает и сохраняет в `self.credentials.openai` API ключи и ID ассистентов.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если API ключ OpenAI успешно загружен.
              ID ассистентов загружается, если найдена соответствующая запись,
              но это не влияет на возвращаемое значение метода. Возвращает `False`,
              если API ключ не найден.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'openai'.
        2. Если запись 'openai' найдена:
           a. Инициализирует объект SimpleNamespace `self.credentials.openai`.
           b. Извлекает из записи 'openai' поле 'Password' (предполагается, что
              там хранится API ключ).
           c. Присваивает извлеченный API ключ атрибуту `self.credentials.openai.api_key`.
           d. Возвращает `True`.
        3. Пытается получить запись из KeePass по пути 'openai/assistants'.
        4. Если запись 'openai/assistants' найдена:
           a. Извлекает из этой записи поле 'Password' (предполагается, что там
              хранится ID ассистента).
           b. Присваивает извлеченный ID ассистента атрибуту `self.credentials.openai.assistant_id`.
        5. Если запись 'openai' не найдена, логируется отладочное сообщение и
           возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_openai_credentials(kp)
        >>> # После успешной загрузки:
        >>> # api_key = gs.credentials.openai.api_key
        >>> # assistant_id = gs.credentials.openai.assistant_id
    """
    try:
        # Получение записи OpenAI API ключа
        entry_api: Entry | None = kp.find_entry_by_path('openai')
        if entry_api:
            # Инициализация объекта для учетных данных OpenAI
            cls.credentials.openai: SimpleNamespace = SimpleNamespace()
            # Извлечение API ключа (хранится в поле Password)
            cls.credentials.openai.api_key = entry_api.password
            # Попытка загрузить ID ассистента
            try:
                entry_assistants: Entry | None = kp.find_entry_by_path('openai/assistants')
                if entry_assistants:
                    # Извлечение ID ассистента (хранится в поле Password)
                    cls.credentials.openai.assistant_id = entry_assistants.password
            except Exception as inner_ex:
                logger.debug(f'Ошибка при загрузке ID ассистента OpenAI: {inner_ex}')
            # Возврат True, так как API ключ найден
            return True
        else:
            # Логирование, если запись OpenAI API ключа не найдена
            logger.debug('Запись OpenAI API ключа не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных OpenAI: {ex}')
        return False
```

#### `_load_gemini_credentials`

```python
def _load_gemini_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для GoogleAI (Gemini API ключ) из базы данных KeePass.

    Ищет запись в группе 'gemini'. При успешном нахождении извлекает и сохраняет
    в `self.credentials.gemini` API ключ.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'gemini'.
        2. Если запись найдена:
           a. Инициализирует объект SimpleNamespace `self.credentials.gemini`.
           b. Извлекает из записи поле 'Password' (предполагается, что там
              хранится API ключ).
           c. Присваивает извлеченный API ключ атрибуту `self.credentials.gemini.api_key`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_gemini_credentials(kp)
        >>> # После успешной загрузки:
        >>> # api_key = gs.credentials.gemini.api_key
    """
    try:
        # Получение записи Gemini API ключа
        entry: Entry | None = kp.find_entry_by_path('gemini')
        if entry:
            # Инициализация объекта для учетных данных Gemini
            cls.credentials.gemini: SimpleNamespace = SimpleNamespace()
            # Извлечение API ключа (хранится в поле Password)
            cls.credentials.gemini.api_key = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись Gemini API ключа не найдена
            logger.debug('Запись Gemini API ключа не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных Gemini: {ex}')
        return False

```

#### `_load_telegram_credentials`

```python
def _load_telegram_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для Telegram (токен бота) из базы данных KeePass.

    Ищет запись в группе 'telegram'. При успешном нахождении извлекает и сохраняет
    в `self.credentials.telegram` токен.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'telegram'.
        2. Если запись найдена:
           a. Инициализирует объект SimpleNamespace `self.credentials.telegram`.
           b. Извлекает из записи поле 'Password' (предполагается, что там
              хранится токен).
           c. Присваивает извлеченный токен атрибуту `self.credentials.telegram.token`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_telegram_credentials(kp)
        >>> # После успешной загрузки:
        >>> # telegram_token = gs.credentials.telegram.token
    """
    try:
        # Получение записи Telegram
        entry: Entry | None = kp.find_entry_by_path('telegram')
        if entry:
            # Инициализация объекта для учетных данных Telegram
            cls.credentials.telegram: SimpleNamespace = SimpleNamespace()
            # Извлечение токена (хранится в поле Password)
            cls.credentials.telegram.token = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись Telegram не найдена
            logger.debug('Запись Telegram не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных Telegram: {ex}')
        return False
```

#### `_load_discord_credentials`

```python
def _load_discord_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для Discord (ID приложения, публичный ключ, токен бота)
    из базы данных KeePass.

    Ищет запись в группе 'discord'. При успешном нахождении извлекает и сохраняет
    в `self.credentials.discord` ID приложения, публичный ключ и токен бота.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'discord'.
        2. Если запись найдена:
           a. Инициализирует объект SimpleNamespace `self.credentials.discord`.
           b. Извлекает из записи поля 'UserName' (для application_id),
              'Attribute(public_key)', 'Password' (для bot_token).
           c. Присваивает извлеченные значения соответствующим атрибутам
              в `self.credentials.discord`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_discord_credentials(kp)
        >>> # После успешной загрузки:
        >>> # app_id = gs.credentials.discord.application_id
        >>> # bot_token = gs.credentials.discord.bot_token
    """
    try:
        # Получение записи Discord
        entry: Entry | None = kp.find_entry_by_path('discord')
        if entry:
            # Инициализация объекта для учетных данных Discord
            cls.credentials.discord: SimpleNamespace = SimpleNamespace()
            # Извлечение данных из записи KeePass
            cls.credentials.discord.application_id = entry.username
            cls.credentials.discord.public_key = entry.get_custom_property('public_key')
            cls.credentials.discord.bot_token = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись Discord не найдена
            logger.debug('Запись Discord не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных Discord: {ex}')
        return False
```

#### `_load_PrestaShop_credentials`

```python
def _load_PrestaShop_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает основные учетные данные для PrestaShop из базы данных KeePass.

    Ищет запись в группе 'prestashop/clients'. При успешном нахождении
    извлекает и сохраняет в `self.credentials.presta.client` API ключ,
    домен API, сервер БД, пользователя БД и пароль БД.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'prestashop/clients'.
        2. Если запись найдена:
           a. Инициализирует вложенный объект SimpleNamespace `self.credentials.presta.client`.
           b. Извлекает из записи поля 'UserName' (для пользователя БД),
              'Password' (для пароля БД), 'Attribute(api_key)',
              'Attribute(api_domain)', 'Attribute(db_server)'.
           c. Присваивает извлеченные значения соответствующим атрибутам
              в `self.credentials.presta.client`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_PrestaShop_credentials(kp)
        >>> # После успешной загрузки:
        >>> # presta_api_key = gs.credentials.presta.client.api_key
    """
    try:
        # Получение записи PrestaShop Client
        entry: Entry | None = kp.find_entry_by_path('prestashop/clients')
        if entry:
            # Инициализация объекта для учетных данных PrestaShop Client
            # Убедимся, что self.credentials.presta существует
            if not hasattr(cls.credentials, 'presta'):
                 cls.credentials.presta = SimpleNamespace()
            cls.credentials.presta.client: SimpleNamespace = SimpleNamespace()
            # Извлечение данных из записи KeePass
            cls.credentials.presta.client.api_key = entry.get_custom_property('api_key')
            cls.credentials.presta.client.api_domain = entry.get_custom_property('api_domain')
            cls.credentials.presta.client.db_server = entry.get_custom_property('db_server')
            cls.credentials.presta.client.db_user = entry.username
            cls.credentials.presta.client.db_password = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись PrestaShop Client не найдена
            logger.debug('Запись PrestaShop Client не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных PrestaShop Client: {ex}')
        return False
```

#### `_load_presta_translations_credentials`

```python
def _load_presta_translations_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для сервиса переводов PrestaShop из базы данных KeePass.

    Ищет запись в группе 'prestashop/translation'. При успешном нахождении
    извлекает и сохраняет в `self.credentials.presta.translations` сервер, порт,
    базу данных, пользователя и пароль.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'prestashop/translation'.
        2. Если запись найдена:
           a. Инициализирует вложенный объект SimpleNamespace `self.credentials.presta.translations`.
           b. Извлекает из записи поля 'UserName' (для пользователя), 'Password'
              (для пароля), 'URL' (для сервера), 'Title' (для базы данных)
              и 'Attribute(port)'.
           c. Присваивает извлеченные значения соответствующим атрибутам
              в `self.credentials.presta.translations`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_presta_translations_credentials(kp)
        >>> # После успешной загрузки:
        >>> # db_server = gs.credentials.presta.translations.server
        >>> # db_user = gs.credentials.presta.translations.user
    """
    try:
        # Получение записи PrestaShop Translations
        entry: Entry | None = kp.find_entry_by_path('prestashop/translation')
        if entry:
            # Инициализация объекта для учетных данных PrestaShop Translations
            # Убедимся, что self.credentials.presta существует
            if not hasattr(cls.credentials, 'presta'):
                 cls.credentials.presta = SimpleNamespace()
            cls.credentials.presta.translations: SimpleNamespace = SimpleNamespace()
            # Извлечение данных из записи KeePass
            cls.credentials.presta.translations.server = entry.url # URL используется для сервера
            cls.credentials.presta.translations.port = entry.get_custom_property('port')
            cls.credentials.presta.translations.database = entry.title # Title используется для имени БД
            cls.credentials.presta.translations.user = entry.username
            cls.credentials.presta.translations.password = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись PrestaShop Translations не найдена
            logger.debug('Запись PrestaShop Translations не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных PrestaShop Translations: {ex}')
        return False

```

#### `_load_smtp_credentials`

```python
def _load_smtp_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для SMTP-сервера из базы данных KeePass.

    Ищет запись в группе 'smtp'. При успешном нахождении извлекает и сохраняет
    в `self.credentials.smtp` сервер, порт, пользователя и пароль.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'smtp'.
        2. Если запись найдена:
           a. Инициализирует объект SimpleNamespace `self.credentials.smtp`.
           b. Извлекает из записи поля 'UserName' (для пользователя),
              'Password' (для пароля), 'URL' (для сервера) и 'Attribute(port)'.
           c. Присваивает извлеченные значения соответствующим атрибутам
              в `self.credentials.smtp`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_smtp_credentials(kp)
        >>> # После успешной загрузки:
        >>> # smtp_user = gs.credentials.smtp.user
        >>> # smtp_server = gs.credentials.smtp.server
    """
    try:
        # Получение записи SMTP
        entry: Entry | None = kp.find_entry_by_path('smtp')
        if entry:
            # Инициализация объекта для учетных данных SMTP
            cls.credentials.smtp: SimpleNamespace = SimpleNamespace()
            # Извлечение данных из записи KeePass
            cls.credentials.smtp.server = entry.url # URL используется для сервера
            cls.credentials.smtp.port = entry.get_custom_property('port')
            cls.credentials.smtp.user = entry.username
            cls.credentials.smtp.password = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись SMTP не найдена
            logger.debug('Запись SMTP не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных SMTP: {ex}')
        return False
```

#### `_load_facebook_credentials`

```python
def _load_facebook_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для Facebook (ID приложения, секрет приложения, токен доступа)
    из базы данных KeePass.

    Ищет запись в группе 'facebook'. При успешном нахождении извлекает и сохраняет
    в `self.credentials.facebook` ID приложения, секрет приложения и токен доступа.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'facebook'.
        2. Если запись найдена:
           a. Инициализирует объект SimpleNamespace `self.credentials.facebook`.
           b. Извлекает из записи поля 'UserName' (для app_id), 'Password'
              (для app_secret) и 'Attribute(access_token)'.
           c. Присваивает извлеченные значения соответствующим атрибутам
              в `self.credentials.facebook`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_facebook_credentials(kp)
        >>> # После успешной загрузки:
        >>> # fb_app_id = gs.credentials.facebook.app_id
        >>> # fb_access_token = gs.credentials.facebook.access_token
    """
    try:
        # Получение записи Facebook
        entry: Entry | None = kp.find_entry_by_path('facebook')
        if entry:
            # Инициализация объекта для учетных данных Facebook
            cls.credentials.facebook: SimpleNamespace = SimpleNamespace()
            # Извлечение данных из записи KeePass
            cls.credentials.facebook.app_id = entry.username
            cls.credentials.facebook.app_secret = entry.password
            cls.credentials.facebook.access_token = entry.get_custom_property('access_token')
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись Facebook не найдена
            logger.debug('Запись Facebook не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных Facebook: {ex}')
        return False
```

#### `_load_gapi_credentials`

```python
def _load_gapi_credentials(cls, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные для Google API (API ключ) из базы данных KeePass.

    Ищет запись в группе 'google/gapi'. При успешном нахождении извлекает и сохраняет
    в `self.credentials.gapi` API ключ.

    Args:
        kp (PyKeePass): Объект открытой базы данных KeePass.

    Returns:
        bool: Возвращает `True`, если учетные данные успешно загружены, иначе `False`.

    Raises:
        Исключения при работе с PyKeePass или атрибутами SimpleNamespace
        могут возникнуть, но не обрабатываются явно.

    Как работает функция:
        1. Пытается получить запись из KeePass по пути 'google/gapi'.
        2. Если запись найдена:
           a. Инициализирует вложенный объект SimpleNamespace `self.credentials.gapi`.
           b. Извлекает из записи поле 'Password' (предполагается, что там
              хранится API ключ).
           c. Присваивает извлеченный API ключ атрибуту `self.credentials.gapi.api_key`.
           d. Возвращает `True`.
        3. Если запись не найдена или при извлечении данных возникает ошибка,
           логируется отладочное сообщение и возвращается `False`.

    Примеры:
        >>> # Метод вызывается внутри _load_credentials
        >>> # success = cls._load_gapi_credentials(kp)
        >>> # После успешной загрузки:
        >>> # gapi_key = gs.credentials.gapi.api_key
    """
    try:
        # Получение записи Google API
        entry: Entry | None = kp.find_entry_by_path('google/gapi')
        if entry:
            # Инициализация объекта для учетных данных Google API
            # Убедимся, что self.credentials.google существует
            if not hasattr(cls.credentials, 'google'):
                 cls.credentials.google = SimpleNamespace()
            cls.credentials.google.gapi: SimpleNamespace = SimpleNamespace()
            # Извлечение API ключа (хранится в поле Password)
            cls.credentials.google.gapi.api_key = entry.password
            # Возврат True при успешной загрузке
            return True
        else:
            # Логирование, если запись Google API не найдена
            logger.debug('Запись Google API не найдена в KeePass.')
            return False
    except Exception as ex:
        # Логирование ошибки при загрузке
        logger.debug(f'Ошибка при загрузке учетных данных Google API: {ex}')
        return False

```

#### `now`

```python
def now(cls) -> str:
    """
    Возвращает текущую дату и время в формате, определенном в конфигурационном файле.

    Формат даты и времени извлекается из `self.config.date.format`.

    Args:
        Нет параметров для этого метода.

    Returns:
        str: Строка, представляющая текущую дату и время в заданном формате.

    Raises:
        Может возникнуть `AttributeError`, если формат даты не определен в конфигурации.

    Как работает функция:
        1. Получает текущую дату и время с использованием `datetime.now()`.
        2. Форматирует объект даты и времени в строку, используя формат,
           указанный в `self.config.date.format`.
        3. Возвращает отформатированную строку.

    Примеры:
        >>> # Метод доступен через глобальный экземпляр gs
        >>> current_timestamp = gs.now()
        >>> print(f'Текущая метка времени: {current_timestamp}')
        # Вывод будет зависеть от формата в config.json, например: 2023-10-27_10-30-00
    """
    # Получение текущей даты и времени
    current_time: datetime = datetime.now()
    # Форматирование в строку согласно формату из конфига
    formatted_time: str = current_time.strftime(cls.config.date.format)
    # Возврат отформатированной строки
    return formatted_time
```

## Управление Учетными Данными с Использованием KeePass

**Что такое KeePass?**

KeePass — это бесплатный и открытый менеджер паролей, который безопасно хранит ваши пароли и другую чувствительную информацию в зашифрованной базе данных. База данных защищена мастер-паролем, который является единственным паролем, который вам нужно запомнить. KeePass использует сильные алгоритмы шифрования (такие как AES и Twofish), чтобы гарантировать безопасность ваших данных.

**Чем хорош KeePass?**

-   **Безопасность**: KeePass использует отраслевые стандарты шифрования для защиты ваших данных, делая их высокозащищенными от несанкционированного доступа.
-   **Переносимость**: Вы можете хранить свою базу данных KeePass на USB-накопителе или в облачном хранилище и получать к ней доступ с нескольких устройств.
-   **Настройка**: KeePass позволяет организовывать ваши пароли в группы и подгруппы, что упрощает управление большим количеством учетных данных.
-   **Открытый Исходный Код**: Будучи проектом с открытым исходным кодом, KeePass прозрачен и может быть проверен сообществом на предмет его безопасности.

**Как KeePass Работает в Этом Проекте**

Учетные данные безопасно управляются с использованием базы данных KeePass (`credentials.kdbx`). Мастер-пароль для этой базы данных обрабатывается по-разному в зависимости от среды:

-   **Режим Разработки**: Пароль считывается из файла с именем `password.txt`, расположенного в директории `secrets`.
-   **Режим Продакшн**: Пароль вводится через консоль. (Необходимо удалить файл `password.txt` из директории `secrets`)

### Структура базы данных `credentials.kdbx`

База данных `credentials.kdbx` организована в группы и записи для удобного и структурированного хранения учетных данных. Ниже представлена структура групп и указано, какие учетные данные хранятся в соответствующих записях, а также как они доступны через атрибуты объекта `self.credentials` после загрузки методом `_load_credentials`:

```
credentials.kdbx
├── suppliers
│   └── aliexpress
│       └── api
│           └── entry (Aliexpress API credentials)
├── openai
│   ├── entry (OpenAI API keys)
│   └── assistants
│       └── entry (OpenAI assistant IDs)
├── gemini
│   └── entry (GoogleAI credentials)
├── telegram
│   └── entry (Telegram credentials)
├── discord
│   └── entry (Discord credentials)
├── prestashop
│   ├── entry (PrestaShop credentials) - Примечание: в коде используется prestashop/clients
│   └── clients
│       └── entry (PrestaShop client credentials)
│   └── translation
│       └── entry (PrestaShop translation credentials)
├── smtp
│   └── entry (SMTP credentials)
├── facebook
│   └── entry (Facebook credentials)
└── google
    └── gapi
        └── entry (Google API credentials)
```

Подробное описание доступа к учетным данным:

1.  **suppliers/aliexpress/api**:
    *   Содержит учетные данные для API Aliexpress.
    *   Доступны как: `self.credentials.aliexpress.api_key`, `self.credentials.aliexpress.secret`, `self.credentials.aliexpress.tracking_id`, `self.credentials.aliexpress.email`, `self.credentials.aliexpress.password`.
2.  **openai**:
    *   Содержит API ключи для OpenAI (в записи 'openai').
    *   Доступен как: `self.credentials.openai.api_key`.
3.  **openai/assistants**:
    *   Содержит идентификаторы ассистентов OpenAI (в записи 'openai/assistants').
    *   Доступен как: `self.credentials.openai.assistant_id`.
4.  **gemini**:
    *   Содержит учетные данные для GoogleAI (в записи 'gemini').
    *   Доступен как: `self.credentials.gemini.api_key`.
5.  **telegram**:
    *   Содержит учетные данные для Telegram (в записи 'telegram').
    *   Доступен как: `self.credentials.telegram.token`.
6.  **discord**:
    *   Содержит учетные данные для Discord (в записи 'discord').
    *   Доступны как: `self.credentials.discord.application_id`, `self.credentials.discord.public_key`, `self.credentials.discord.bot_token`.
7.  **prestashop/clients**:
    *   Содержит основные учетные данные для PrestaShop (в записи 'prestashop/clients').
    *   Доступны как: `self.credentials.presta.client.api_key`, `self.credentials.presta.client.api_domain`, `self.credentials.presta.client.db_server`, `self.credentials.presta.client.db_user`, `self.credentials.presta.client.db_password`.
8.  **prestashop/translation**:
    *   Содержит учетные данные для сервиса переводов PrestaShop (в записи 'prestashop/translation').
    *   Доступны как: `self.credentials.presta.translations.server`, `self.credentials.presta.translations.port`, `self.credentials.presta.translations.database`, `self.credentials.presta.translations.user`, `self.credentials.presta.translations.password`.
9.  **smtp**:
    *   Содержит учетные данные для SMTP (в записи 'smtp').
    *   Доступны как: `self.credentials.smtp.server`, `self.credentials.smtp.port`, `self.credentials.smtp.user`, `self.credentials.smtp.password`.
10. **facebook**:
    *   Содержит учетные данные для Facebook (в записи 'facebook').
    *   Доступны как: `self.credentials.facebook.app_id`, `self.credentials.facebook.app_secret`, `self.credentials.facebook.access_token`.
11. **google/gapi**:
    *   Содержит учетные данные для Google API (в записи 'google/gapi').
    *   Доступен как: `self.credentials.gapi.api_key`.

## Глобальный Экземпляр `ProgramSettings`

```python
# Глобальный экземпляр ProgramSettings
gs: ProgramSettings = ProgramSettings()
```

**Назначение**: Этот глобальный экземпляр класса `ProgramSettings`, доступный под именем `gs`, создается для обеспечения легкого доступа к настроенным параметрам и загруженным учетным данным из любого места в проекте без необходимости повторной инициализации класса. Благодаря декоратору `@singleton`, определение `gs = ProgramSettings()` всегда возвращает один и тот же объект после первого вызова.

**Как это используется?**

В других модулях проекта можно импортировать этот глобальный экземпляр:

```python
from src import gs

# Пример использования для доступа к учетным данным OpenAI
try:
    openai_api_key = gs.credentials.openai.api_key
    print(f'Ключ API OpenAI: {openai_api_key}')
except AttributeError:
    print('Учетные данные OpenAI не загружены.')

# Пример использования для доступа к путям директорий
log_directory = gs.path.log
print(f'Путь к директории логов: {log_directory}')
```

Этот подход упрощает управление зависимостями и обеспечивает единый источник истины для конфигурации и секретов проекта.

## Примечания

-   Модуль использует библиотеку `PyKeePass` для взаимодействия с файлом базы данных `credentials.kdbx`.
-   В коде предусмотрены блоки обработки исключений (`ex`), особенно при работе с файлами и KeePass.
-   Наличие файла `password.txt` с мастер-паролем в открытом виде в директории `secrets` является **потенциальной уязвимостью безопасности**, особенно в производственной среде. Этот механизм предусмотрен для удобства разработки, но требует пересмотра для повышения безопасности в продакшн-режиме (например, использование переменных окружения, безопасного ввода пароля при старте).

## Возможные исключения

В процессе работы с базой данных KeePass или загрузки конфигурации могут возникать следующие исключения:

-   `BinaryError`: Ошибки, связанные с некорректным форматом бинарных данных файла KeePass.
-   `CredentialsError`: Ошибки, связанные с неправильным мастер-паролем или ключом для файла KeePass.
-   `DefaultSettingsException`: Проблемы с настройками по умолчанию библиотеки PyKeePass.
-   `HeaderChecksumError`: Ошибки проверки контрольной суммы заголовков файла KeePass, указывающие на возможное повреждение файла.
-   `KeePassException`: Базовое исключение для всех ошибок, связанных с PyKeePass.
-   `PayloadChecksumError`: Ошибки проверки контрольной суммы содержимого файла KeePass.
-   `UnableToSendToRecycleBin`: Ошибки, возникающие при попытке переместить элементы в корзину (если эта функция KeePass используется).
-   `Exception`: Общее исключение, используемое для перехвата непредвиденных ошибок.

```