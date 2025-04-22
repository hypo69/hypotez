# Модуль `credentials`

## Обзор

Модуль `credentials` предназначен для централизованного хранения и управления глобальными настройками проекта `hypotez`, такими как пути к директориям, учетные данные (логины, пароли) и ключи API. Он реализован с использованием паттерна Singleton, что гарантирует наличие только одного экземпляра настроек в течение всего времени работы приложения. Это упрощает доступ к конфигурации и предотвращает конфликты, связанные с разными настройками в разных частях кода.

## Подробнее

Модуль обеспечивает удобный способ загрузки, хранения и доступа к различным параметрам конфигурации, необходимым для работы приложения. Он использует библиотеку `pykeepass` для безопасного хранения учетных данных в базе данных KeePass. Настройки загружаются при инициализации класса `ProgramSettings`, который является Singleton, что обеспечивает глобальную точку доступа к настройкам приложения.

## Классы

### `ProgramSettings`

**Описание**: Класс `ProgramSettings` представляет собой Singleton, предназначенный для хранения основных параметров и настроек проекта. Он содержит пути к директориям, учетные данные для различных сервисов (Aliexpress, OpenAI, Gemini, Discord, Telegram, PrestaShop, SMTP, Facebook, GAPI, SerpAPI) и другие настройки, необходимые для работы приложения.

**Наследует**: Нет

**Атрибуты**:
- `host_name` (str): Имя хоста, на котором запущено приложение. По умолчанию определяется как `socket.gethostname()`.
- `base_dir` (Path): Корневая директория проекта. Определяется с помощью функции `set_project_root()`.
- `config` (SimpleNamespace): Объект, содержащий общие настройки из файла `config.json`.
- `credentials` (SimpleNamespace): Объект, содержащий учетные данные для различных сервисов.
    - `aliexpress` (SimpleNamespace): Учетные данные для Aliexpress API.
    - `presta` (SimpleNamespace): Учетные данные для PrestaShop.
        - `client` (SimpleNamespace): Клиентские учетные данные для PrestaShop.
    - `openai` (SimpleNamespace): Учетные данные для OpenAI API.
        - `owner` (SimpleNamespace):  Учетные данные для OpenAI API.
    - `gemini` (SimpleNamespace): Учетные данные для Google Gemini API.
        - `owner` (SimpleNamespace): Учетные данные для Google Gemini API.
    - `rev_com` (SimpleNamespace): Учетные данные для Rev.com API.
        - `owner` (SimpleNamespace): Учетные данные для Rev.com API.
    - `shutter_stock` (SimpleNamespace): Учетные данные для Shutterstock API.
        - `owner` (SimpleNamespace): Учетные данные для Shutterstock API.
    - `discord` (SimpleNamespace): Учетные данные для Discord API.
        - `owner` (SimpleNamespace): Учетные данные для Discord API.
    - `telegram` (SimpleNamespace): Учетные данные для Telegram API.
        - `bot` (SimpleNamespace): Учетные данные для Telegram Bot API.
    - `serpapi` (SimpleNamespace): Учетные данные для SerpAPI API.
        - `owner` (SimpleNamespace): Учетные данные для SerpAPI API.
    - `smtp` (List[SimpleNamespace]): Список учетных данных для SMTP.
    - `facebook` (List[SimpleNamespace]): Список учетных данных для Facebook.
    - `gapi` (Dict): Учетные данные для Google API.
- `path` (SimpleNamespace): Объект, содержащий пути к различным директориям проекта.
    - `root` (Path): Корневая директория проекта.
    - `src` (Path): Директория с исходным кодом проекта.
    - `bin` (Path): Директория с бинарными файлами (chrome, firefox, ffmpeg и т.д.).
    - `log` (Path): Директория для хранения логов.
    - `tmp` (Path): Директория для временных файлов.
    - `data` (Path): Директория для хранения данных.
    - `secrets` (Path): Директория для хранения секретных данных (паролей, ключей API).
    - `google_drive` (Path): Директория для интеграции с Google Drive.
    - `external_storage` (Path): Директория для внешнего хранилища.
    - `tools` (Path): Директория для хранения инструментов.
    - `dev_null` (str): Путь к `/dev/null` (или `nul` в Windows) для перенаправления вывода.
- `host` (str): Хост приложения.
- `git` (str): Имя репозитория Git.
- `git_user` (str): Имя пользователя Git.
- `current_release` (str): Текущая версия релиза.

**Принцип работы**:

1.  **Инициализация**: При создании экземпляра `ProgramSettings` загружаются общие настройки из файла `config.json` и учетные данные из базы данных KeePass.
2.  **Singleton**: Гарантируется, что в приложении существует только один экземпляр `ProgramSettings`.
3.  **Доступ к настройкам**: Настройки доступны через атрибуты экземпляра `ProgramSettings`.

**Методы**:

*   `__post_init__(self)`: Выполняет инициализацию после создания экземпляра класса.
*   `_load_credentials(self) -> None`: Загружает учетные данные из настроек.
*   `_open_kp(self, retry: int = 3) -> PyKeePass | None`: Открывает базу данных KeePass.
*   `_load_aliexpress_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Aliexpress API из KeePass.
*   `_load_openai_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные OpenAI API из KeePass.
*   `_load_gemini_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные GoogleAI API из KeePass.
*   `_load_telegram_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Telegram API из KeePass.
*   `_load_discord_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Discord API из KeePass.
*   `_load_prestashop_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные PrestaShop из KeePass.
*   `_load_serpapi_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные SerpAPI из KeePass.
*   `_load_smtp_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные SMTP из KeePass.
*   `_load_facebook_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Facebook из KeePass.
*   `_load_gapi_credentials(self, kp: PyKeePass) -> bool`: Загружает учетные данные Google API из KeePass.
*   `now(self) -> str`: Возвращает текущую метку времени в формате год-месяц-день-часы-минуты-секунды-милисекунды.

## Функции

### `set_project_root`

**Назначение**: Находит корневой каталог проекта, начиная с директории текущего файла, и добавляет его в `sys.path`.

**Параметры**:
- `marker_files` (tuple): Список файлов или директорий, наличие которых указывает на корневой каталог проекта. По умолчанию `('__root__', '.git')`.

**Возвращает**:
- `Path`: Путь к корневому каталогу проекта.

**Как работает функция**:
Функция `set_project_root` выполняет поиск корневого каталога проекта, начиная с директории, в которой находится текущий файл. Она итерируется по родительским директориям, пока не найдет директорию, содержащую один из файлов-маркеров (например, `__root__` или `.git`). Если корневой каталог найден, он добавляется в `sys.path`, чтобы обеспечить возможность импорта модулей из этого каталога. Если корневой каталог не найден, возвращается директория, в которой находится текущий файл.

**Примеры**:

```python
from pathlib import Path
import sys

# Пример вызова функции без указания marker_files
root_path = set_project_root()
print(f"Root path: {root_path}")
print(f"sys.path: {sys.path}")

# Пример вызова функции с указанием marker_files
root_path = set_project_root(marker_files=('my_marker.txt',))
print(f"Root path: {root_path}")
print(f"sys.path: {sys.path}")
```

### `singleton`

**Назначение**: Декоратор для реализации паттерна Singleton.

**Параметры**:
- `cls` (class): Класс, для которого нужно реализовать Singleton.

**Возвращает**:
- `function`: Функция `get_instance`, которая возвращает единственный экземпляр класса.

**Как работает функция**:
Декоратор `singleton` принимает класс в качестве аргумента и возвращает функцию `get_instance`, которая управляет созданием экземпляров этого класса. При первом вызове `get_instance` создается экземпляр класса и сохраняется в словаре `instances`. При последующих вызовах возвращается уже существующий экземпляр из словаря.

**Примеры**:

```python
@singleton
class MyClass:
    def __init__(self, value):
        self.value = value

# Создание первого экземпляра
instance1 = MyClass(10)
print(f"Instance 1 value: {instance1.value}")

# Создание второго экземпляра (вернет тот же экземпляр, что и instance1)
instance2 = MyClass(20)
print(f"Instance 2 value: {instance2.value}")

# Проверка, что instance1 и instance2 - это один и тот же объект
print(f"instance1 is instance2: {instance1 is instance2}")
```

### `ProgramSettings.__post_init__`

**Назначение**: Выполняет постобработку после инициализации экземпляра класса `ProgramSettings`.

**Как работает функция**:
Метод `__post_init__` выполняет следующие действия:
1.  Загружает общие настройки из файла `config.json` с помощью функции `j_loads_ns` и сохраняет их в атрибуте `config`.
2.  Устанавливает формат временной метки из атрибута `timestamp_format` файла конфигурации или использует значение по умолчанию (`%y_%m_%d_%H_%M_%S_%f`).
3.  Устанавливает имя проекта из имени корневой директории.
4.  Инициализирует объект `path` с путями к различным директориям проекта.
5.  Определяет пути к бинарным файлам (gtk, ffmpeg, graphviz, wkhtmltopdf) и добавляет их в `sys.path`.
6.  Подавляет вывод GTK в консоль.
7.  Вызывает метод `_load_credentials` для загрузки учетных данных из базы данных KeePass.

### `ProgramSettings._load_credentials`

**Назначение**: Загружает учетные данные из базы данных KeePass и сохраняет их в атрибуте `credentials`.

**Как работает функция**:

1.  Открывает базу данных KeePass с помощью метода `_open_kp`.
2.  Загружает учетные данные для различных сервисов (Aliexpress, OpenAI, Gemini, Discord, Telegram, PrestaShop, SMTP, Facebook, GAPI, SerpAPI) с помощью соответствующих методов (`_load_aliexpress_credentials`, `_load_openai_credentials` и т.д.).

### `ProgramSettings._open_kp`

**Назначение**: Открывает базу данных KeePass.

**Параметры**:
- `retry` (int): Количество попыток открытия базы данных в случае ошибки. По умолчанию 3.

**Возвращает**:
- `PyKeePass | None`: Объект `PyKeePass`, представляющий открытую базу данных, или `None`, если не удалось открыть базу данных после нескольких попыток.

**Как работает функция**:
Функция `_open_kp` пытается открыть базу данных KeePass, используя пароль, указанный в файле `password.txt` (если он существует), или запрашивая пароль у пользователя через консоль. Если открытие базы данных не удалось, функция повторяет попытку указанное количество раз. В случае неудачи выводит сообщение об ошибке и завершает работу приложения.

### `ProgramSettings._load_aliexpress_credentials`

**Назначение**: Загружает учетные данные для Aliexpress API из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_aliexpress_credentials` пытается найти группу `api` в базе данных KeePass по пути `suppliers/aliexpress` и извлечь из нее учетные данные (api\_key, secret, tracking\_id, email, password). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_openai_credentials`

**Назначение**: Загружает учетные данные для OpenAI API из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_openai_credentials` пытается найти группы, содержащие ключи API в базе данных KeePass по пути `openai`, и извлечь из них учетные данные (api\_key, project\_api).  Создает новый `SimpleNamespace` для каждого API ключа и устанавливает атрибуты `api_key` и `project_api` для каждого ключа.
Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_gemini_credentials`

**Назначение**: Загружает учетные данные для Google Gemini API из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_gemini_credentials` пытается найти группу `gemini` в базе данных KeePass и извлечь из нее учетные данные (api\_key). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_telegram_credentials`

**Назначение**: Загружает учетные данные для Telegram API из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_telegram_credentials` пытается найти группу `telegram` в базе данных KeePass и извлечь из нее учетные данные (token). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_discord_credentials`

**Назначение**: Загружает учетные данные для Discord API из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_discord_credentials` пытается найти группу `discord` в базе данных KeePass и извлечь из нее учетные данные (application\_id, public\_key, bot\_token). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_prestashop_credentials`

**Назначение**: Загружает учетные данные для PrestaShop из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_prestashop_credentials` пытается найти группу `prestashop` в базе данных KeePass и извлечь из нее учетные данные для каждого клиента (api\_key, api\_domain, db\_server, db\_user, db\_password). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_serpapi_credentials`

**Назначение**: Загружает учетные данные для SerpAPI из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_serpapi_credentials` пытается найти группу `serpapi.com` в базе данных KeePass и извлечь из нее учетные данные (api\_key). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_smtp_credentials`

**Назначение**: Загружает учетные данные для SMTP из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_smtp_credentials` пытается найти группу `smtp` в базе данных KeePass и извлечь из нее учетные данные (server, port, user, password). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_facebook_credentials`

**Назначение**: Загружает учетные данные для Facebook из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_facebook_credentials` пытается найти группу `facebook` в базе данных KeePass и извлечь из нее учетные данные (app\_id, app\_secret, access\_token). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings._load_gapi_credentials`

**Назначение**: Загружает учетные данные для Google API из базы данных KeePass.

**Параметры**:
- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:
- `bool`: `True`, если загрузка учетных данных прошла успешно, `False` в противном случае.

**Как работает функция**:
Функция `_load_gapi_credentials` пытается найти группу `google/gapi` в базе данных KeePass и извлечь из нее учетные данные (api\_key). Если группа не найдена или произошла ошибка при извлечении учетных данных, функция возвращает `False`.

### `ProgramSettings.now`

**Назначение**: Возвращает текущую метку времени в формате, определенном в конфигурации.

**Возвращает**:
- `str`: Текущая метка времени в строковом формате.

**Как работает функция**:
Функция `now` форматирует текущую дату и время с использованием формата, указанного в атрибуте `timestamp_format` объекта `config`.

## Параметры класса

- `host_name` (str): Имя хоста, на котором запущено приложение.
- `base_dir` (Path): Корневая директория проекта.
- `config` (SimpleNamespace): Объект, содержащий общие настройки из файла `config.json`.
- `credentials` (SimpleNamespace): Объект, содержащий учетные данные для различных сервисов.
- `path` (SimpleNamespace): Объект, содержащий пути к различным директориям проекта.
- `host` (str): Хост приложения.
- `git` (str): Имя репозитория Git.
- `git_user` (str): Имя пользователя Git.
- `current_release` (str): Текущая версия релиза.

## Примеры

```python
from src.credentials import ProgramSettings

# Получение экземпляра настроек
settings = ProgramSettings()

# Доступ к настройкам
print(f"Project name: {settings.config.project_name}")
print(f"API key: {settings.credentials.aliexpress.api_key}")
print(f"Log directory: {settings.path.log}")
print(f"Current timestamp: {settings.now}")
```