# Модуль `credentials`

## Обзор

Модуль `credentials` предназначен для хранения глобальных настроек проекта, таких как пути, пароли, логины и параметры API. Он использует паттерн Singleton для обеспечения единственного экземпляра настроек в течение всего времени работы приложения.

## Подробнее

Этот модуль является центральным местом для хранения и управления всеми настройками, необходимыми для работы приложения. Он обеспечивает удобный доступ к конфигурационным данным и учетным данным, что упрощает управление и обслуживание проекта.

## Классы

### `ProgramSettings`

**Описание**:
`ProgramSettings` - класс настроек программы.
Синглтон, хранящий основные параметры и настройки проекта.

**Наследует**:
Нет

**Атрибуты**:

- `host_name` (str): Имя хоста, на котором запущена программа. По умолчанию получается из `socket.gethostname()`.
- `base_dir` (Path): Базовая директория проекта. По умолчанию определяется с помощью функции `set_project_root()`.
- `config` (SimpleNamespace): Объект, хранящий конфигурационные параметры, загруженные из файла `config.json`.
- `credentials` (SimpleNamespace): Объект, хранящий учетные данные для различных сервисов и API.
- `path` (SimpleNamespace): Объект, хранящий пути к различным директориям проекта.
- `host` (str): Хост. По умолчанию ''.
- `git` (str): Git. По умолчанию ''.
- `git_user` (str): Git пользователь. По умолчанию ''.
- `current_release` (str): Текущий релиз. По умолчанию ''.

**Принцип работы**:
Класс `ProgramSettings` использует паттерн Singleton, чтобы гарантировать, что в приложении существует только один экземпляр настроек. При создании экземпляра класса загружаются конфигурационные параметры из файла `config.json`, а также учетные данные из KeePass базы данных. Пути к различным директориям проекта определяются на основе базовой директории.

**Методы**:

- `__post_init__`: Выполняет инициализацию после создания экземпляра класса.
- `_load_credentials`: Загружает учетные данные из KeePass базы данных.
- `_open_kp`: Открывает KeePass базу данных.
- `_load_aliexpress_credentials`: Загружает учетные данные для Aliexpress API.
- `_load_openai_credentials`: Загружает учетные данные для OpenAI API.
- `_load_gemini_credentials`: Загружает учетные данные для Gemini API.
- `_load_discord_credentials`: Загружает учетные данные для Discord API.
- `_load_telegram_credentials`: Загружает учетные данные для Telegram API.
- `_load_prestashop_credentials`: Загружает учетные данные для PrestaShop.
- `_load_smtp_credentials`: Загружает учетные данные для SMTP.
- `_load_facebook_credentials`: Загружает учетные данные для Facebook.
- `_load_gapi_credentials`: Загружает учетные данные для Google API.
- `_load_serpapi_credentials`: Загружает учетные данные для SerpAPI.
- `now`: Возвращает текущую метку времени в формате год-месяц-день-часы-минуты-секунды-милисекунды.

## Функции

### `set_project_root`

**Описание**:
Определяет корневую директорию проекта.

```python
def set_project_root(marker_files: tuple = ('__root__', '.git')) -> Path:
    """
    Finds the root directory of the project starting from the current file's directory,
    searching upwards and stopping at the first directory containing any of the marker files.
    
    Args:
        marker_files (tuple): Filenames or directory names to identify the project root.
    
    Returns:
        Path: Path to the root directory if found, otherwise the directory where the script is located.
    """
```

**Параметры**:
- `marker_files` (tuple, optional): Кортеж файлов-маркеров для определения корневой директории. По умолчанию `('__root__', '.git')`.

**Возвращает**:
- `Path`: Путь к корневой директории проекта.

**Как работает**:
Функция начинает поиск корневой директории с директории, в которой расположен текущий файл, и поднимается вверх по дереву директорий. Поиск прекращается, когда найдена директория, содержащая хотя бы один из файлов-маркеров, указанных в параметре `marker_files`. Если корневая директория не найдена, возвращается директория, в которой расположен текущий файл.

**Примеры**:

```python
from pathlib import Path
# Пример вызова функции
root_dir = set_project_root()
print(f"Root directory: {root_dir}")
```

### `singleton`

**Описание**:
Декоратор для реализации Singleton.

```python
def singleton(cls):
    """Декоратор для реализации Singleton."""
```

**Параметры**:
- `cls`: Класс, для которого применяется паттерн Singleton.

**Возвращает**:
- Функция `get_instance`, которая возвращает единственный экземпляр класса.

**Как работает**:
Декоратор `singleton` создает функцию `get_instance`, которая хранит единственный экземпляр класса в словаре `instances`. При каждом вызове `get_instance` возвращается сохраненный экземпляр класса, если он существует, или создается новый экземпляр, который сохраняется в словаре `instances`.

**Примеры**:

```python
@singleton
class MyClass:
    pass

# Пример вызова декоратора
instance1 = MyClass()
instance2 = MyClass()
print(instance1 is instance2)  # Выведет: True
```

## Методы класса `ProgramSettings`

### `__post_init__`

**Описание**:
Выполняет инициализацию после создания экземпляра класса.

```python
def __post_init__(self):
    """Выполняет инициализацию после создания экземпляра класса."""
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.

**Как работает**:
После создания экземпляра класса `ProgramSettings` этот метод выполняет следующие действия:

1. Загружает конфигурационные параметры из файла `config.json` с помощью функции `j_loads_ns`.
2. Устанавливает формат метки времени, имя проекта, хост, Git и текущий релиз на основе загруженных конфигурационных параметров.
3. Определяет пути к различным директориям проекта на основе базовой директории.
4. Добавляет пути к директориям с бинарными файлами в системные пути.
5. Отключает предупреждения GTK.
6. Загружает учетные данные из KeePass базы данных с помощью метода `_load_credentials`.

**Примеры**:

```python
# Пример создания экземпляра класса ProgramSettings
settings = ProgramSettings()
```

### `_load_credentials`

**Описание**:
Загружает учетные данные из KeePass базы данных.

```python
def _load_credentials(self) -> None:
    """ Загружает учетные данные из настроек."""
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.

**Как работает**:
Этот метод выполняет следующие действия:

1. Открывает KeePass базу данных с помощью метода `_open_kp`.
2. Загружает учетные данные для различных сервисов и API с помощью соответствующих методов:
   - `_load_aliexpress_credentials`
   - `_load_openai_credentials`
   - `_load_gemini_credentials`
   - `_load_discord_credentials`
   - `_load_telegram_credentials`
   - `_load_prestashop_credentials`
   - `_load_smtp_credentials`
   - `_load_facebook_credentials`
   - `_load_gapi_credentials`
   - `_load_serpapi_credentials`

**Примеры**:

```python
# Пример вызова метода _load_credentials
settings = ProgramSettings()
settings._load_credentials()
```

### `_open_kp`

**Описание**:
Открывает KeePass базу данных.

```python
def _open_kp(self, retry: int = 3) -> PyKeePass | None:
    """ Open KeePass database
    Args:
        retry (int): Number of retries
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `retry` (int, optional): Количество попыток открытия базы данных. По умолчанию `3`.

**Возвращает**:
- `PyKeePass | None`: Экземпляр класса `PyKeePass`, представляющий открытую базу данных, или `None`, если не удалось открыть базу данных после нескольких попыток.

**Как работает**:
Этот метод пытается открыть KeePass базу данных, используя пароль, указанный в файле `password.txt` или введенный пользователем. Если не удалось открыть базу данных, метод повторяет попытку указанное количество раз. В случае неудачи выводится сообщение об ошибке и программа завершается.

**Примеры**:

```python
# Пример вызова метода _open_kp
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    print("KeePass database opened successfully")
else:
    print("Failed to open KeePass database")
```

### `_load_aliexpress_credentials`

**Описание**:
Загружает учетные данные для Aliexpress API из KeePass базы данных.

```python
def _load_aliexpress_credentials(self, kp: PyKeePass) -> bool:
    """ Load Aliexpress API credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для Aliexpress API из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.aliexpress`.

**Примеры**:

```python
# Пример вызова метода _load_aliexpress_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_aliexpress_credentials(kp)
    if success:
        print("Aliexpress credentials loaded successfully")
    else:
        print("Failed to load Aliexpress credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_openai_credentials`

**Описание**:
Загружает учетные данные для OpenAI API из KeePass базы данных.

```python
def _load_openai_credentials(self, kp: PyKeePass) -> bool:
    """ Load OpenAI credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для OpenAI API из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.openai`.

**Примеры**:

```python
# Пример вызова метода _load_openai_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_openai_credentials(kp)
    if success:
        print("OpenAI credentials loaded successfully")
    else:
        print("Failed to load OpenAI credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_gemini_credentials`

**Описание**:
Загружает учетные данные для Gemini API из KeePass базы данных.

```python
def _load_gemini_credentials(self, kp: PyKeePass) -> bool:
    """ Load GoogleAI credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для Gemini API из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.gemini`.

**Примеры**:

```python
# Пример вызова метода _load_gemini_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_gemini_credentials(kp)
    if success:
        print("Gemini credentials loaded successfully")
    else:
        print("Failed to load Gemini credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_telegram_credentials`

**Описание**:
Загружает учетные данные для Telegram API из KeePass базы данных.

```python
def _load_telegram_credentials(self, kp: PyKeePass) -> bool:
    """Load Telegram credentials from KeePass.

    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для Telegram API из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.telegram`.

**Примеры**:

```python
# Пример вызова метода _load_telegram_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_telegram_credentials(kp)
    if success:
        print("Telegram credentials loaded successfully")
    else:
        print("Failed to load Telegram credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_discord_credentials`

**Описание**:
Загружает учетные данные для Discord API из KeePass базы данных.

```python
def _load_discord_credentials(self, kp: PyKeePass) -> bool:
    """ Load Discord credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для Discord API из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.discord`.

**Примеры**:

```python
# Пример вызова метода _load_discord_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_discord_credentials(kp)
    if success:
        print("Discord credentials loaded successfully")
    else:
        print("Failed to load Discord credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_prestashop_credentials`

**Описание**:
Загружает учетные данные для PrestaShop из KeePass базы данных.

```python
def _load_prestashop_credentials(self, kp: PyKeePass) -> bool:
    """ Load prestashop credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.
    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для PrestaShop из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.presta.client`.

**Примеры**:

```python
# Пример вызова метода _load_prestashop_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_prestashop_credentials(kp)
    if success:
        print("Prestashop credentials loaded successfully")
    else:
        print("Failed to load Prestashop credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_serpapi_credentials`

**Описание**:
Загружает учетные данные для SerpAPI из KeePass базы данных.

```python
def _load_serpapi_credentials(self, kp: PyKeePass) -> bool:
    """ Load OpenAI credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для SerpAPI из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.serpapi`.

**Примеры**:

```python
# Пример вызова метода _load_serpapi_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_serpapi_credentials(kp)
    if success:
        print("SerpAPI credentials loaded successfully")
    else:
        print("Failed to load SerpAPI credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_smtp_credentials`

**Описание**:
Загружает учетные данные для SMTP из KeePass базы данных.

```python
def _load_smtp_credentials(self, kp: PyKeePass) -> bool:
    """ Load SMTP credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для SMTP из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.smtp`.

**Примеры**:

```python
# Пример вызова метода _load_smtp_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_smtp_credentials(kp)
    if success:
        print("SMTP credentials loaded successfully")
    else:
        print("Failed to load SMTP credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_facebook_credentials`

**Описание**:
Загружает учетные данные для Facebook из KeePass базы данных.

```python
def _load_facebook_credentials(self, kp: PyKeePass) -> bool:
    """ Load Facebook credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для Facebook из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.facebook`.

**Примеры**:

```python
# Пример вызова метода _load_facebook_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_facebook_credentials(kp)
    if success:
        print("Facebook credentials loaded successfully")
    else:
        print("Failed to load Facebook credentials")
else:
    print("Failed to open KeePass database")
```

### `_load_gapi_credentials`

**Описание**:
Загружает учетные данные для Google API из KeePass базы данных.

```python
def _load_gapi_credentials(self, kp: PyKeePass) -> bool:
    """ Load Google API credentials from KeePass
    Args:
        kp (PyKeePass): The KeePass database instance.

    Returns:
        bool: True if loading was successful, False otherwise.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `kp` (PyKeePass): Экземпляр класса `PyKeePass`, представляющий открытую базу данных.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает**:
Этот метод извлекает учетные данные для Google API из KeePass базы данных и сохраняет их в атрибутах объекта `self.credentials.gapi`.

**Примеры**:

```python
# Пример вызова метода _load_gapi_credentials
settings = ProgramSettings()
kp = settings._open_kp()
if kp:
    success = settings._load_gapi_credentials(kp)
    if success:
        print("GAPI credentials loaded successfully")
    else:
        print("Failed to load GAPI credentials")
else:
    print("Failed to open KeePass database")
```

### `now`

**Описание**:
Возвращает текущую метку времени в формате год-месяц-день-часы-минуты-секунды-милисекунды.

```python
@property
def now(self) -> str:
    """Возвращает текущую метку времени в формате год-месяц-день-часы-минуты-секунды-милисекунды.

    Этот метод возвращает строку, представляющую текущую метку времени, в формате `год_месяц_день_часы_минуты_секунды_миллисекунды`.

    Args:
        dformat (str, optional): Формат для метки времени. По умолчанию `\'%y_%m_%d_%H_%M_%S_%f\'`.

    Returns:
        str: Текущая метка времени в строковом формате.
    """
```

**Параметры**:
- `self`: Ссылка на экземпляр класса.

**Возвращает**:
- `str`: Текущая метка времени в строковом формате.

**Как работает**:
Этот метод возвращает текущую метку времени, используя формат, определенный в конфигурационных параметрах (`self.config.timestamp_format`).

**Примеры**:

```python
# Пример вызова метода now
settings = ProgramSettings()
current_time = settings.now
print(f"Current time: {current_time}")
```