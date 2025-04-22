# Документация модуля `src.credentials`

## Обзор

Этот документ предоставляет обзор класса `ProgramSettings`.

Модуль предназначен для загрузки и хранения информации об учетных данных (API-ключи, пароли и т. д.) из файла базы данных KeePass `credentials.kdbx`. Он также включает функцию `set_project_root` для определения корневого каталога проекта.

## Содержание

- [Функции](#функции)
  - [`set_project_root`](#set_project_root)
  - [`singleton`](#singleton)
- [Классы](#классы)
  - [`ProgramSettings`](#programsettings)

## Функции

### `set_project_root`

**Назначение**: Функция находит корневой каталог проекта, начиная с текущего каталога. Поиск выполняется вверх по каталогам до тех пор, пока не будет найден каталог, содержащий один из файлов в списке `marker_files`.

**Параметры**:

- `marker_files` (tuple): Кортеж строк, представляющих имена файлов или каталогов, используемых для идентификации корневого каталога проекта. По умолчанию ищет следующие маркеры: `pyproject.toml`, `requirements.txt`, `.git`.

**Возвращает**:

- `Path`: Путь к корневому каталогу проекта, если он найден, в противном случае - путь к каталогу, в котором расположен скрипт.

### `singleton`

**Назначение**: Декоратор для создания класса-одиночки (singleton).

**Параметры**:

- `cls`: Класс, который следует преобразовать в одиночку.

**Возвращает**:

- `function`: Функция, возвращающая экземпляр класса-одиночки.

## Классы

### `ProgramSettings`

**Описание**: Класс для настроек программы. Он устанавливает основные параметры и настройки проекта. Он загружает конфигурацию из `config.json` и данные учетных данных из файла базы данных KeePass `credentials.kdbx`.

**Атрибуты**:

- `host_name` (str): Имя хоста.
- `base_dir` (Path): Путь к корневому каталогу проекта.
- `config` (SimpleNamespace): Объект, содержащий конфигурацию проекта.
- `credentials` (SimpleNamespace): Объект, содержащий учетные данные.
- `MODE` (str): Режим работы проекта (например, `dev`, `prod`).
- `path` (SimpleNamespace): Объект, содержащий пути к различным каталогам проекта.

**Методы**:

- `__init__(self, **kwargs)`: Инициализирует экземпляр класса.
  - Загружает конфигурацию проекта из `config.json`.
  - Инициализирует атрибут `path` путями к различным каталогам проекта.
  - Вызывает `check_latest_release` для проверки новой версии проекта.
  - Загружает учетные данные из `credentials.kdbx`.

- `_load_credentials(self) -> None`: Загружает учетные данные из KeePass.

- `_open_kp(self, retry: int = 3) -> PyKeePass | None`: Открывает базу данных KeePass. Обрабатывает возможные исключения при открытии базы данных.

- `_load_aliexpress_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Aliexpress из KeePass.

- `_load_openai_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные OpenAI из KeePass.

- `_load_gemini_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные GoogleAI из KeePass.

- `_load_telegram_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Telegram из KeePass.

- `_load_discord_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Discord из KeePass.

- `_load_PrestaShop_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные PrestaShop из KeePass.

- `_load_presta_translations_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные PrestaShop Translations из KeePass.

- `_load_smtp_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные SMTP из KeePass.

- `_load_facebook_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Facebook из KeePass.

- `_load_gapi_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Google API из KeePass.

- `now(self) -> str`: Возвращает текущую временную метку в формате, указанном в файле `config.json`.

**Возможные исключения**:

- `BinaryError`: Исключение для ошибок двоичных данных.
- `CredentialsError`: Исключение для ошибок данных учетных данных.
- `DefaultSettingsException`: Исключение для ошибок настроек по умолчанию.
- `HeaderChecksumError`: Исключение для ошибок контрольной суммы заголовка.
- `KeePassException`: Исключение для ошибок базы данных KeePass.
- `PayloadChecksumError`: Исключение для ошибок контрольной суммы полезной нагрузки.
- `UnableToSendToRecycleBin`: Исключение для ошибок отправки в корзину.
- `Exception`: Общее исключение.

### Методы класса `ProgramSettings`

#### `__init__`

```python
def __init__(self, **kwargs):
    """
    Инициализирует экземпляр класса ProgramSettings.

    Args:
        **kwargs: Произвольные ключевые аргументы.

    Raises:
        Exception: Если не удается загрузить настройки или возникают другие ошибки.
    """
    # Загружает конфигурацию проекта из config.json.
    self.config = j_loads_ns(self.base_dir / 'src' / 'config.json')
    if not self.config:
        logger.error('Ошибка при загрузке настроек')
        ... # Тут происходит обработка ошибок и выход из программы
        return

    # Устанавливает имя проекта из имени базового каталога
    self.config.project_name = self.base_dir.name

    # Инициализирует пути к различным каталогам проекта
    self.path = SimpleNamespace()
    self.path.tmp = Path(self.config.path.tmp)  # Каталог для временных файлов
    self.path.log = Path(self.config.path.log)  # Каталог для файлов журнала
    self.path.storage = Path(self.config.path.storage)  # Каталог для хранения данных
    self.path.gdrive = Path(self.config.path.gdrive)  # Каталог для Google Drive
    self.path.secrets = self.base_dir / 'secrets'  # Каталог для секретов (пароли и ключи)

    # Создает необходимые каталоги, если они не существуют
    for p in [self.path.tmp, self.path.log, self.path.storage, self.path.gdrive, self.path.secrets]:
        p.mkdir(parents=True, exist_ok=True)

    # Проверяет наличие новой версии проекта
    check_latest_release()

    # Загружает учетные данные из KeePass
    self._load_credentials()

    # Другие операции, которые могут быть выполнены при инициализации
    ...
```

**Принцип работы**:

Функция `__init__` инициализирует класс `ProgramSettings`. Внутри этой функции происходит загрузка настроек из файла `config.json`, установка путей к различным директориям проекта, проверка наличия новой версии проекта и загрузка учетных данных из базы данных KeePass.

#### `_load_credentials`

```python
def _load_credentials(self) -> None:
    """
    Загружает учетные данные из KeePass.

    Raises:
        CredentialsError: Если не удается загрузить учетные данные.
    """
    kp = None # Переменная для хранения объекта KeePass
    # Открывает базу данных KeePass
    kp = self._open_kp()
    if not kp:
        return

    # Загружает учетные данные из базы данных KeePass
    success = True
    success &= self._load_aliexpress_credentials(kp)
    success &= self._load_openai_credentials(kp)
    success &= self._load_gemini_credentials(kp)
    success &= self._load_telegram_credentials(kp)
    success &= self._load_discord_credentials(kp)
    success &= self._load_PrestaShop_credentials(kp)
    success &= self._load_presta_translations_credentials(kp)
    success &= self._load_smtp_credentials(kp)
    success &= self._load_facebook_credentials(kp)
    success &= self._load_gapi_credentials(kp)

    # Если не удалось загрузить все учетные данные, выбрасывает исключение
    if not success:
        raise CredentialsError('Не удалось загрузить учетные данные')

    # Присваивает имя хоста
    self.host_name = os.environ.get('HOSTNAME')
    logger.info(f'Загрузка учетных данных завершена. Имя хоста: {self.host_name}')
```

**Принцип работы**:

Функция `_load_credentials` загружает все необходимые учетные данные из базы данных KeePass, используя приватные методы `_load_*_credentials` для каждой категории учетных данных (Aliexpress, OpenAI, Gemini и т.д.). Если загрузка хотя бы одной категории не удалась, выбрасывается исключение `CredentialsError`.

#### `_open_kp`

```python
def _open_kp(self, retry: int = 3) -> PyKeePass | None:
    """
    Открывает базу данных KeePass.

    Args:
        retry (int): Количество попыток повтора.

    Returns:
        PyKeePass | None: Объект PyKeePass, если база данных успешно открыта, иначе None.

    Raises:
        Exception: Если не удается открыть базу данных KeePass после нескольких попыток.
    """
    # Пытается открыть базу данных KeePass несколько раз
    while retry > 0:
        try:
            # Определяет пароль из файла или запрашивает его у пользователя
            password:str = Path( self.path.secrets / 'password.txt').read_text(encoding="utf-8") or None
            kp = PyKeePass(str(self.path.secrets / 'credentials.kdbx'), 
                           password = password or getpass.getpass(print('Введите мастер-пароль KeePass: ').lower()))
            return kp
        except Exception as ex:
            print(f"Не удалось открыть базу данных KeePass. Исключение: {ex}, осталось {retry-1} попыток.")
            ... #Логирование ошибки
            retry -= 1
            if retry < 1:
                logger.critical('Не удалось открыть базу данных KeePass после нескольких попыток', exc_info=True)
                ... #Выход из программы
                sys.exit()
```

**Принцип работы**:

Функция `_open_kp` открывает базу данных KeePass, используя библиотеку `PyKeePass`. Пароль для базы данных берется либо из файла `password.txt`, либо запрашивается у пользователя через консоль. Если открыть базу данных не удается, функция повторяет попытку несколько раз, прежде чем завершить работу с ошибкой.

#### `_load_aliexpress_credentials`

```python
def _load_aliexpress_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные Aliexpress из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает группу Aliexpress API из базы данных KeePass
        group = kp.find_groups(path="suppliers/aliexpress/api")[0]
        # Извлекает учетные данные из записей в группе
        self.credentials.aliexpress = SimpleNamespace()
        self.credentials.aliexpress.api_key = group.find_entries(title="api_key")[0].password
        self.credentials.aliexpress.secret = group.find_entries(title="secret")[0].password
        self.credentials.aliexpress.tracking_id = group.find_entries(title="tracking_id")[0].password
        self.credentials.aliexpress.email = group.find_entries(title="email")[0].password
        self.credentials.aliexpress.password = group.find_entries(title="password")[0].password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные Aliexpress', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_aliexpress_credentials` загружает учетные данные для Aliexpress API из базы данных KeePass. Она ищет группу с путем `suppliers/aliexpress/api` и извлекает значения для `api_key`, `secret`, `tracking_id`, `email` и `password` из записей в этой группе.

#### `_load_openai_credentials`

```python
def _load_openai_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные OpenAI из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает записи OpenAI API keys и OpenAI assistant IDs
        api_key_entry = kp.find_entries(path="openai", title="api_key")[0]
        assistant_id_entry = kp.find_entries(path="openai/assistants", title="assistant_id")[0]

        # Извлекает учетные данные из записей
        self.credentials.openai = SimpleNamespace()
        self.credentials.openai.api_key = api_key_entry.password
        self.credentials.openai.assistant_id = assistant_id_entry.password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные OpenAI', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_openai_credentials` загружает учетные данные для OpenAI API из базы данных KeePass. Она ищет записи `api_key` в группе `openai` и `assistant_id` в группе `openai/assistants`, извлекает соответствующие пароли и сохраняет их в атрибутах объекта `self.credentials.openai`.

#### `_load_gemini_credentials`

```python
def _load_gemini_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные GoogleAI (Gemini) из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись Gemini API key
        entry = kp.find_entries(path="gemini", title="api_key")[0]
        # Извлекает учетные данные из записи
        self.credentials.gemini = SimpleNamespace()
        self.credentials.gemini.api_key = entry.password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные Gemini', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_gemini_credentials` загружает учетные данные для GoogleAI (Gemini) из базы данных KeePass. Она ищет запись `api_key` в группе `gemini`, извлекает соответствующий пароль и сохраняет его в атрибуте объекта `self.credentials.gemini`.

#### `_load_telegram_credentials`

```python
def _load_telegram_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные Telegram из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись Telegram token
        entry = kp.find_entries(path="telegram", title="token")[0]
        # Извлекает учетные данные из записи
        self.credentials.telegram = SimpleNamespace()
        self.credentials.telegram.token = entry.password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные Telegram', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_telegram_credentials` загружает учетные данные для Telegram из базы данных KeePass. Она ищет запись `token` в группе `telegram`, извлекает соответствующий пароль и сохраняет его в атрибуте объекта `self.credentials.telegram`.

#### `_load_discord_credentials`

```python
def _load_discord_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные Discord из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись Discord credentials
        entry = kp.find_entries(path="discord", title="credentials")[0]
        # Извлекает учетные данные из записи
        self.credentials.discord = SimpleNamespace()
        self.credentials.discord.application_id = entry.username
        self.credentials.discord.public_key = entry.notes
        self.credentials.discord.bot_token = entry.password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные Discord', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_discord_credentials` загружает учетные данные для Discord из базы данных KeePass. Она ищет запись `credentials` в группе `discord`, извлекает `application_id` из имени пользователя, `public_key` из заметок и `bot_token` из пароля, и сохраняет их в атрибутах объекта `self.credentials.discord`.

#### `_load_PrestaShop_credentials`

```python
def _load_PrestaShop_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные PrestaShop из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись PrestaShop credentials
        client = kp.find_entries(path="prestashop/clients", title="credentials")[0]
        # Извлекает учетные данные из записи
        self.credentials.presta = SimpleNamespace()
        self.credentials.presta.client = SimpleNamespace()

        self.credentials.presta.client.api_key = client.username
        self.credentials.presta.client.api_domain = client.notes
        self.credentials.presta.client.db_server = client.password
        self.credentials.presta.client.db_user = client.title
        self.credentials.presta.client.db_password = client.comment
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные PrestaShop', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_PrestaShop_credentials` загружает учетные данные для PrestaShop из базы данных KeePass. Она ищет запись `credentials` в группе `prestashop/clients`, извлекает `api_key` из имени пользователя, `api_domain` из заметок, `db_server` из пароля, `db_user` из заголовка и `db_password` из комментария, и сохраняет их в атрибутах объекта `self.credentials.presta.client`.

#### `_load_presta_translations_credentials`

```python
def _load_presta_translations_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные PrestaShop Translations из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись PrestaShop translation
        entry = kp.find_entries(path="prestashop/translation", title="credentials")[0]
        # Извлекает учетные данные из записи
        self.credentials.presta.translations = SimpleNamespace()
        self.credentials.presta.translations.server = entry.username
        self.credentials.presta.translations.port = entry.notes
        self.credentials.presta.translations.database = entry.password
        self.credentials.presta.translations.user = entry.title
        self.credentials.presta.translations.password = entry.comment
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные PrestaShop Translations', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_presta_translations_credentials` загружает учетные данные для PrestaShop Translations из базы данных KeePass. Она ищет запись `credentials` в группе `prestashop/translation`, извлекает `server` из имени пользователя, `port` из заметок, `database` из пароля, `user` из заголовка и `password` из комментария, и сохраняет их в атрибутах объекта `self.credentials.presta.translations`.

#### `_load_smtp_credentials`

```python
def _load_smtp_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные SMTP из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись SMTP credentials
        entry = kp.find_entries(path="smtp", title="credentials")[0]
        # Извлекает учетные данные из записи
        self.credentials.smtp = SimpleNamespace()
        self.credentials.smtp.server = entry.username
        self.credentials.smtp.port = entry.notes
        self.credentials.smtp.user = entry.title
        self.credentials.smtp.password = entry.password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные SMTP', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_smtp_credentials` загружает учетные данные для SMTP из базы данных KeePass. Она ищет запись `credentials` в группе `smtp`, извлекает `server` из имени пользователя, `port` из заметок, `user` из заголовка и `password` из пароля, и сохраняет их в атрибутах объекта `self.credentials.smtp`.

#### `_load_facebook_credentials`

```python
def _load_facebook_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные Facebook из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись Facebook credentials
        entry = kp.find_entries(path="facebook", title="credentials")[0]
        # Извлекает учетные данные из записи
        self.credentials.facebook = SimpleNamespace()
        self.credentials.facebook.app_id = entry.username
        self.credentials.facebook.app_secret = entry.notes
        self.credentials.facebook.access_token = entry.password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные Facebook', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_facebook_credentials` загружает учетные данные для Facebook из базы данных KeePass. Она ищет запись `credentials` в группе `facebook`, извлекает `app_id` из имени пользователя, `app_secret` из заметок и `access_token` из пароля, и сохраняет их в атрибутах объекта `self.credentials.facebook`.

#### `_load_gapi_credentials`

```python
def _load_gapi_credentials(self, kp: PyKeePass) -> bool:
    """
    Загружает учетные данные Google API из KeePass.

    Args:
        kp (PyKeePass): Объект PyKeePass.

    Returns:
        bool: True, если учетные данные успешно загружены, иначе False.
    """
    try:
        # Получает запись Google API credentials
        entry = kp.find_entries(path="google/gapi", title="credentials")[0]
        # Извлекает учетные данные из записи
        self.credentials.gapi = SimpleNamespace()
        self.credentials.gapi.api_key = entry.password
        return True
    except Exception as ex:
        logger.error('Не удалось загрузить учетные данные Google API', ex, exc_info=True)
        return False
```

**Принцип работы**:

Функция `_load_gapi_credentials` загружает учетные данные для Google API из базы данных KeePass. Она ищет запись `credentials` в группе `google/gapi`, извлекает `api_key` из пароля и сохраняет его в атрибуте объекта `self.credentials.gapi`.

#### `now`

```python
def now(self) -> str:
    """
    Возвращает текущую временную метку в формате, указанном в файле `config.json`.

    Returns:
        str: Текущая временная метка в формате, указанном в `self.config.now_format`.
    """
    # Возвращает текущую временную метку в формате, указанном в config.json
    return datetime.now().strftime(self.config.now_format)
```

**Принцип работы**:

Функция `now` возвращает текущую дату и время в виде строки, отформатированной в соответствии с форматом, указанным в файле конфигурации (`config.json`).

### Notes

- Модуль использует PyKeePass для работы с файлом `credentials.kdbx`.
- В коде присутствуют блоки обработки исключений (`ex`).
- Файл паролей (`password.txt`) содержит пароли в открытом виде. Это потенциальная уязвимость. Необходимо разработать безопасный механизм хранения паролей.

### Initialization and Configuration

При запуске проект инициализирует и настраивает различные параметры и учетные данные. В этом документе объясняется, как эти значения устанавливаются и управляются.

#### Determining the Project's Root Directory

Проект автоматически определяет свой корневой каталог, выполняя поиск вверх от текущего каталога файла для определенных файлов-маркеров (`pyproject.toml`, `requirements.txt`, `.git`). Это гарантирует, что проект сможет найти свои ресурсы независимо от текущего рабочего каталога.

```python
def set_project_root(marker_files=('__root__','.git')) -> Path:
    """
    Находит корневой каталог проекта, начиная с текущего каталога файла,
    выполняя поиск вверх и останавливаясь в первом каталоге, содержащем любой из файлов-маркеров.

    Args:
        marker_files (tuple): Имена файлов или каталогов для идентификации корневого каталога проекта.

    Returns:
        Path: Путь к корневому каталогу, если он найден, в противном случае - каталог, в котором расположен скрипт.
    """
    __root__:Path # Объявляет переменную для хранения корневого каталога
    current_path:Path = Path(__file__).resolve().parent # Определяет текущий путь к файлу
    __root__ = current_path # Инициализирует корневой каталог текущим путем
    for parent in [current_path] + list(current_path.parents): # Итерируется по текущему и родительским каталогам
        if any((parent / marker).exists() for marker in marker_files): # Проверяет наличие маркеров в каталоге
            __root__ = parent # Обновляет корневой каталог, если маркер найден
            break
    if __root__ not in sys.path: # Проверяет, есть ли корневой каталог в sys.path
        sys.path.insert(0, str(__root__)) # Добавляет корневой каталог в sys.path
    return __root__ # Возвращает корневой каталог
```

#### Loading Configuration

Проект загружает свои настройки по умолчанию из файла `config.json`, расположенного в каталоге `src`. Этот JSON-файл содержит различные параметры конфигурации, такие как:

- **Author Information**: Информация об авторе.
- **Available Modes**: Поддерживаемые режимы (`dev`, `debug`, `test`, `prod`).
- **Paths**: Каталоги для журналов, временных файлов, внешнего хранилища и Google Drive.
- **Project Details**: Имя, версия и информация о выпуске проекта.

```python
self.config = j_loads_ns(self.base_dir / 'src' / 'config.json') # Загружает конфигурацию из config.json
if not self.config: # Проверяет, удалось ли загрузить конфигурацию
    logger.error('Ошибка при загрузке настроек')
    ... # Тут происходит обработка ошибок и выход из программы
    return

self.config.project_name = self.base_dir.name # Устанавливает имя проекта из имени базового каталога
```

#### Managing Credentials Using KeePass

**What is KeePass?**

KeePass is a free and open-source password manager that securely stores your passwords and other sensitive information in an encrypted database. The database is protected by a master password, which is the only password you need to remember. KeePass uses strong encryption algorithms (such as AES and Twofish) to ensure the security of your data.

**Why is KeePass Good?**

- **Security**: KeePass uses industry-standard encryption to protect your data, making it highly secure against unauthorized access.
- **Portability**: You can store your KeePass database on a USB drive or in cloud storage and access it from multiple devices.
- **Customization**: KeePass allows you to organize your passwords into groups and subgroups, making it easier to manage a large number of credentials.
- **Open Source**: Being an open-source project, KeePass is transparent and can be reviewed by the community for its security.

**How KeePass Works in This Project**

Credentials are securely managed using the KeePass database (`credentials.kdbx`). The master password for this database is handled differently depending on the environment:

- **Development Mode**: The password is read from a file named `password.txt` located in the `secrets` directory.
- **Production Mode**: The password is entered via the console. (Remove the `password.txt` file from the `secrets` directory)

```python
def _open_kp(self, retry: int = 3) -> PyKeePass | None:
    """ Открывает базу данных KeePass
    Args:
        retry (int): Количество повторов
    """
    while retry > 0: # Цикл повторных попыток
        try:
            password:str = Path( self.path.secrets / 'password.txt').read_text(encoding="utf-8") or None # Чтение пароля из файла
            kp = PyKeePass(str(self.path.secrets / 'credentials.kdbx'), # Открытие базы данных KeePass
                           password = password or getpass.getpass(print('Введите мастер-пароль KeePass: ').lower())) # Ввод пароля пользователем, если файл не найден
            return kp # Возврат объекта PyKeePass
        except Exception as ex:
            print(f"Не удалось открыть базу данных KeePass. Исключение: {ex}, {retry-1} попыток осталось.")
            ... #Логирование ошибки
            retry -= 1 # Уменьшение счетчика попыток
            if retry < 1: # Если попытки закончились
                logger.critical('Не удалось открыть базу данных KeePass после нескольких попыток', exc_info=True)
                ... #Выход из программы
                sys.exit()
```

#### KeePass Database Tree Structure

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
│   ├── entry (PrestaShop credentials)
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

#### Detailed Structure Description:

1. **suppliers/aliexpress/api**:
   - Contains Aliexpress API credentials.
   - Example entry: `self.credentials.aliexpress.api_key`, `self.credentials.aliexpress.secret`, `self.credentials.aliexpress.tracking_id`, `self.credentials.aliexpress.email`, `self.credentials.aliexpress.password`.

2. **openai**:
   - Contains OpenAI API keys.
   - Example entry: `self.credentials.openai.api_key`.

3. **openai/assistants**:
   - Contains OpenAI assistant IDs.
   - Example entry: `self.credentials.openai.assistant_id`.

4. **gemini**:
   - Contains GoogleAI credentials.
   - Example entry: `self.credentials.gemini.api_key`.

5. **telegram**:
   - Contains Telegram credentials.
   - Example entry: `self.credentials.telegram.token`.

6. **discord**:
   - Contains Discord credentials.
   - Example entry: `self.credentials.discord.application_id`, `self.credentials.discord.public_key`, `self.credentials.discord.bot_token`.

7. **prestashop**:
   - Contains PrestaShop credentials.
   - Example entry: `self.credentials.presta.client.api_key`, `self.credentials.presta.client.api_domain`, `self.credentials.presta.client.db_server`, `self.credentials.presta.client.db_user`, `self.credentials.presta.client.db_password`.

8. **prestashop/clients**:
   - Contains PrestaShop client credentials.