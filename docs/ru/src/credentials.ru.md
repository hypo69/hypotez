# Документация модуля `src.credentials`

## Обзор

Данный документ предоставляет обзор класса `ProgramSettings`, который отвечает за загрузку и хранение учетных данных из базы данных KeePass (`credentials.kdbx`), а также за определение корневого каталога проекта.

## Оглавление

- [Обзор](#обзор)
- [Функции](#функции)
  - [`set_project_root`](#set_project_root)
  - [`singleton`](#singleton)
- [Классы](#классы)
  - [`ProgramSettings`](#programsettings)
    - [`__init__`](#init)
    - [`_load_credentials`](#_load_credentials)
    - [`_open_kp`](#_open_kp)
    - Методы загрузки учетных данных:
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
- [Примечания](#примечания)
- [Инициализация и настройка](#инициализация-и-настройка)
  - [Определение корневой директории проекта](#определение-корневой-директории-проекта)
  - [Загрузка конфигурации](#загрузка-конфигурации)
  - [Управление учетными данными с использованием KeePass](#управление-учетными-данными-с-использованием-keePass)
- [Глобальный экземпляр `ProgramSettings`](#глобальный-экземпляр-programsettings)

## Функции

### `set_project_root`

**Назначение**: Функция `set_project_root` находит корневую директорию проекта, начиная от текущего каталога. Поиск идёт вверх по директориям, пока не будет найдена директория, содержащая один из файлов из списка `marker_files`.

**Параметры**:

- `marker_files` (tuple): Кортеж строк, представляющих имена файлов или каталогов, которые используются для определения корневой директории проекта. По умолчанию ищутся маркеры `pyproject.toml`, `requirements.txt`, `.git`.

**Возвращает**:

- `Path`: Путь к корневой директории проекта, если она найдена, иначе - путь к директории, в которой расположен скрипт.

**Как работает функция**:

- Функция получает путь к директории, в которой расположен текущий файл.
- Перебирает текущую директорию и все её родительские директории.
- Для каждой директории проверяет, содержит ли она хотя бы один из маркерных файлов.
- Если маркерный файл найден, функция возвращает путь к этой директории.
- Если маркерные файлы не найдены, функция возвращает путь к директории, в которой расположен скрипт.

**Примеры**:

```python
from pathlib import Path
# Пример вызова функции с маркерными файлами по умолчанию
root_path = set_project_root()
print(f"Корневая директория проекта: {root_path}")

# Пример вызова функции с пользовательскими маркерными файлами
root_path = set_project_root(marker_files=('my_marker_file.txt', 'config_dir'))
print(f"Корневая директория проекта: {root_path}")
```

### `singleton`

**Назначение**: Декоратор для создания класса-синглтона.

**Параметры**:

- `cls`: Класс, который должен быть преобразован в синглтон.

**Возвращает**:

- `function`: Функция, возвращающая экземпляр класса-синглтона.

**Как работает функция**:

- Декоратор `singleton` принимает класс в качестве аргумента.
- Создаёт словарь `instances` для хранения экземпляров классов-синглтонов.
- Возвращает внутреннюю функцию `getinstance`, которая при первом вызове создаёт экземпляр класса и сохраняет его в словаре `instances`.
- При последующих вызовах `getinstance` возвращает сохранённый экземпляр класса из словаря `instances`.

**Примеры**:

```python
@singleton
class MySingletonClass:
    def __init__(self):
        print("Singleton instance created")

# Создание экземпляров класса
instance1 = MySingletonClass()  # Singleton instance created
instance2 = MySingletonClass()

# Проверка, что оба экземпляра являются одним и тем же объектом
print(instance1 is instance2)  # True
```

## Классы

### `ProgramSettings`

**Описание**: Класс настроек программы. Устанавливает основные параметры и настройки проекта. Загружает конфигурацию из `config.json` и данные учетных данных из файла `credentials.kdbx` в базе данных KeePass.

**Атрибуты**:

- `host_name` (str): Имя хоста.
- `base_dir` (Path): Путь к корневой директории проекта.
- `config` (SimpleNamespace): Объект, содержащий конфигурацию проекта.
- `credentials` (SimpleNamespace): Объект, содержащий учетные данные.
- `MODE` (str): Режим работы проекта (например, \'dev\', \'prod\').
- `path` (SimpleNamespace): Объект, содержащий пути к различным директориям проекта.

**Методы**:

#### `__init__`

**Назначение**: Инициализирует экземпляр класса `ProgramSettings`.

**Как работает метод**:

- Загружает конфигурацию проекта из файла `config.json`.
- Инициализирует атрибут `path` с путями к различным директориям проекта.
- Вызывает метод `check_latest_release` для проверки наличия новой версии проекта.
- Загружает учетные данные из файла `credentials.kdbx`.

**Примеры**:

```python
settings = ProgramSettings()
print(f"Режим работы: {settings.MODE}")
print(f"API ключ OpenAI: {settings.credentials.openai.api_key}")
```

#### `_load_credentials`

**Назначение**: Загружает учетные данные из базы данных KeePass.

**Как работает метод**:

- Вызывает `_open_kp` для открытия базы данных KeePass.
- Вызывает методы `_load_*_credentials` для загрузки учетных данных для различных сервисов.

#### `_open_kp`

**Назначение**: Открывает базу данных KeePass.

**Параметры**:

- `retry` (int): Количество попыток открытия базы данных.

**Возвращает**:

- `PyKeePass | None`: Объект `PyKeePass`, представляющий открытую базу данных, или `None`, если не удалось открыть базу данных после нескольких попыток.

**Как работает метод**:

- Пытается открыть базу данных KeePass, используя пароль, считанный из файла `password.txt` (если файл существует) или введенный пользователем в консоли.
- Если не удается открыть базу данных, повторяет попытку несколько раз (количество попыток задается параметром `retry`).
- Если после нескольких попыток не удается открыть базу данных, выводит сообщение об ошибке и завершает работу программы.

**Примеры**:

```python
kp = self._open_kp(retry=3)
if kp:
    print("База данных KeePass успешно открыта")
else:
    print("Не удалось открыть базу данных KeePass")
```

#### `_load_aliexpress_credentials`

**Назначение**: Загружает учетные данные Aliexpress из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает учетные данные Aliexpress (api_key, secret, tracking_id, email, password) из базы данных KeePass.
- Сохраняет извлеченные учетные данные в атрибуты объекта `self.credentials.aliexpress`.

#### `_load_openai_credentials`

**Назначение**: Загружает учетные данные OpenAI из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает API ключ OpenAI из базы данных KeePass.
- Сохраняет извлеченный API ключ в атрибут объекта `self.credentials.openai.api_key`.

#### `_load_gemini_credentials`

**Назначение**: Загружает учетные данные GoogleAI (Gemini) из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает API ключ Gemini из базы данных KeePass.
- Сохраняет извлеченный API ключ в атрибут объекта `self.credentials.gemini.api_key`.

#### `_load_telegram_credentials`

**Назначение**: Загружает учетные данные Telegram из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает токен Telegram бота из базы данных KeePass.
- Сохраняет извлеченный токен в атрибут объекта `self.credentials.telegram.token`.

#### `_load_discord_credentials`

**Назначение**: Загружает учетные данные Discord из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает идентификатор приложения Discord, публичный ключ и токен бота из базы данных KeePass.
- Сохраняет извлеченные учетные данные в атрибуты объекта `self.credentials.discord`.

#### `_load_PrestaShop_credentials`

**Назначение**: Загружает учетные данные PrestaShop из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает API ключ, домен API, сервер базы данных, имя пользователя базы данных и пароль базы данных PrestaShop из базы данных KeePass.
- Сохраняет извлеченные учетные данные в атрибуты объекта `self.credentials.presta.client`.

#### `_load_presta_translations_credentials`

**Назначение**: Загружает учетные данные для переводов PrestaShop из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает сервер, порт, имя базы данных, имя пользователя и пароль для переводов PrestaShop из базы данных KeePass.
- Сохраняет извлеченные учетные данные в атрибуты объекта `self.credentials.presta.translations`.

#### `_load_smtp_credentials`

**Назначение**: Загружает учетные данные SMTP из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает сервер, порт, имя пользователя и пароль SMTP из базы данных KeePass.
- Сохраняет извлеченные учетные данные в атрибуты объекта `self.credentials.smtp`.

#### `_load_facebook_credentials`

**Назначение**: Загружает учетные данные Facebook из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает идентификатор приложения, секрет приложения и токен доступа Facebook из базы данных KeePass.
- Сохраняет извлеченные учетные данные в атрибуты объекта `self.credentials.facebook`.

#### `_load_gapi_credentials`

**Назначение**: Загружает учетные данные Google API из базы данных KeePass.

**Параметры**:

- `kp` (`PyKeePass`): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Возвращает**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**Как работает метод**:

- Извлекает API ключ Google API из базы данных KeePass.
- Сохраняет извлеченный API ключ в атрибут объекта `self.credentials.gapi.api_key`.

#### `now`

**Назначение**: Возвращает текущую метку времени в формате, указанном в файле `config.json`.

**Возвращает**:

- `str`: Текущая метка времени в формате, указанном в `config.json`.

**Как работает метод**:

- Форматирует текущее время с использованием формата, определенного в конфигурации (`self.config.time_format`).

**Примеры**:

```python
current_time = settings.now()
print(f"Текущее время: {current_time}")
```

## Примечания

- Модуль использует PyKeePass для работы с файлом `credentials.kdbx`.
- В коде присутствуют блоки обработки исключений (`ex`).
- Файл паролей (`password.txt`) содержит пароли в открытом виде. Это потенциальная уязвимость. Необходимо разработать механизм безопасного хранения паролей.

## Инициализация и настройка

При запуске проект инициализирует и настраивает различные конфигурации и учетные данные. Этот документ объясняет, как эти значения устанавливаются и управляются.

### Определение корневой директории проекта

Проект автоматически определяет свою корневую директорию, ища вверх от текущей директории файла для определенных маркерных файлов (`pyproject.toml`, `requirements.txt`, `.git`). Это гарантирует, что проект может найти свои ресурсы независимо от текущей рабочей директории.

```python
def set_project_root(marker_files=('__root__','.git')) -> Path:
    """
    Находит корневую директорию проекта, начиная с текущей директории файла,
    ища вверх и останавливаясь на первой директории, содержащей любой из маркерных файлов.
    
    Args:
        marker_files (tuple): Имена файлов или директорий для идентификации корневой директории проекта.
    
    Returns:
        Path: Путь к корневой директории, если найдена, иначе директория, где находится скрипт.
    """
    ...
```

### Загрузка конфигурации

Проект загружает свои настройки по умолчанию из файла `config.json`, расположенного в директории `src`. Этот JSON-файл содержит различные параметры конфигурации, такие как:

- **Информация об Авторе**: Детали об авторе.
- **Доступные Режимы**: Поддерживаемые режимы (`dev`, `debug`, `test`, `prod`).
- **Пути**: Директории для логов, временных файлов, внешнего хранилища и Google Drive.
- **Детали Проекта**: Название, версия и информация о релизе проекта.

```python
self.config = j_loads_ns(self.base_dir / 'src' / 'config.json')
if not self.config:
    logger.error('Ошибка при загрузке настроек')
    ...
    return

self.config.project_name = self.base_dir.name
```

### Управление учетными данными с использованием KeePass

**Что такое KeePass?**

KeePass — это бесплатный и открытый менеджер паролей, который безопасно хранит ваши пароли и другую чувствительную информацию в зашифрованной базе данных. База данных защищена мастер-паролем, который является единственным паролем, который вам нужно запомнить. KeePass использует сильные алгоритмы шифрования (такие как AES и Twofish), чтобы гарантировать безопасность ваших данных.

**Чем хорош KeePass?**

- **Безопасность**: KeePass использует отраслевые стандарты шифрования для защиты ваших данных, делая их высокозащищенными от несанкционированного доступа.
- **Переносимость**: Вы можете хранить свою базу данных KeePass на USB-накопителе или в облачном хранилище и получать к ней доступ с нескольких устройств.
- **Настройка**: KeePass позволяет организовывать ваши пароли в группы и подгруппы, что упрощает управление большим количеством учетных данных.
- **Открытый Исходный Код**: Будучи проектом с открытым исходным кодом, KeePass прозрачен и может быть проверен сообществом на предмет его безопасности.

**Как KeePass Работает в Этом Проекте**

Учетные данные безопасно управляются с использованием базы данных KeePass (`credentials.kdbx`). Мастер-пароль для этой базы данных обрабатывается по-разному в зависимости от среды:

- **Режим Разработки**: Пароль считывается из файла с именем `password.txt`, расположенного в директории `secrets`.
- **Режим Продакшн**: Пароль вводится через консоль. (Удалите файл `password.txt` из директории `secrets`)

```python
def _open_kp(self, retry: int = 3) -> PyKeePass | None:
    """ Открывает базу данных KeePass
    Args:
        retry (int): Количество попыток
    """
    ...
```

Дерево базы данных `credentials.kdbx`:

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

### Подробное описание структуры:

1. **suppliers/aliexpress/api**:
   - Содержит учетные данные для API Aliexpress.
   - Пример записи: `self.credentials.aliexpress.api_key`, `self.credentials.aliexpress.secret`, `self.credentials.aliexpress.tracking_id`, `self.credentials.aliexpress.email`, `self.credentials.aliexpress.password`.

2. **openai**:
   - Содержит API ключи для OpenAI.
   - Пример записи: `self.credentials.openai.api_key`.

3. **openai/assistants**:
   - Содержит идентификаторы ассистентов OpenAI.
   - Пример записи: `self.credentials.openai.assistant_id`.

4. **gemini**:
   - Содержит учетные данные для GoogleAI.
   - Пример записи: `self.credentials.gemini.api_key`.

5. **telegram**:
   - Содержит учетные данные для Telegram.
   - Пример записи: `self.credentials.telegram.token`.

6. **discord**:
   - Содержит учетные данные для Discord.
   - Пример записи: `self.credentials.discord.application_id`, `self.credentials.discord.public_key`, `self.credentials.discord.bot_token`.

7. **prestashop**:
   - Содержит учетные данные для PrestaShop.
   - Пример записи: `self.credentials.presta.client.api_key`, `self.credentials.presta.client.api_domain`, `self.credentials.presta.client.db_server`, `self.credentials.presta.client.db_user`, `self.credentials.presta.client.db_password`.

8. **prestashop/clients**:
   - Содержит учетные данные для клиентов PrestaShop.
   - Пример записи: `self.credentials.presta.client.api_key`, `self.credentials.presta.client.api_domain`, `self.credentials.presta.client.db_server`, `self.credentials.presta.client.db_user`, `self.credentials.presta.client.db_password`.

9. **prestashop/translation**:
   - Содержит учетные данные для переводов PrestaShop.
   - Пример записи: `self.credentials.presta.translations.server`, `self.credentials.presta.translations.port`, `self.credentials.presta.translations.database`, `self.credentials.presta.translations.user`, `self.credentials.presta.translations.password`.

10. **smtp**:
    - Содержит учетные данные для SMTP.
    - Пример записи: `self.credentials.smtp.server`, `self.credentials.smtp.port`, `self.credentials.smtp.user`, `self.credentials.smtp.password`.

11. **facebook**:
    - Содержит учетные данные для Facebook.
    - Пример записи: `self.credentials.facebook.app_id`, `self.credentials.facebook.app_secret`, `self.credentials.facebook.access_token`.

12. **google/gapi**:
    - Содержит учетные данные для Google API.
    - Пример записи: `self.credentials.gapi.api_key`.

### Примечания:

- Каждая группа (`group`) в KeePass соответствует определенному пути (`path`).
- Каждая запись (`entry`) в группе содержит конкретные учетные данные.
- Методы `_load_*_credentials` загружают данные из соответствующих групп и записей в базе данных KeePass и сохраняют их в атрибуты объекта `self.credentials`.

## Глобальный экземпляр `ProgramSettings`

```python
# Global instance of ProgramSettings
gs: ProgramSettings = ProgramSettings()
```

**Зачем это нужно?**

Этот глобальный экземпляр `ProgramSettings` (`gs`) создается для того, чтобы обеспечить доступ к настройкам и учетным данным проекта из любого места в коде. Таким образом, вам не нужно каждый раз создавать новый экземпляр класса `ProgramSettings`, когда вам нужно получить доступ к настройкам или учетным данным.

**Как это используется?**

В других модулях проекта вы можете импортировать этот глобальный экземпляр и использовать его для доступа к настройкам и учетным данным:

```python
from src import gs

# Пример использования
api_key = gs.credentials.openai.api_key
```

Это упрощает доступ к настройкам и учетным данным, делая код более чистым и удобным для использования.