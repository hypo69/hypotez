## \file hypotez/src/credentials.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

                ```rst
 .. module:: src.credentials
 ```

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>


<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/readme.ru.md'>Русский</A>
</TD>
</TABLE>

Этот документ предоставляет обзор класса `ProgramSettings`.

ProgramSettings
==================

## Обзор

ProgramSettings загружает и хранит учетные данные (ключи API, пароли и т. д.) из файла базы данных KeePass `credentials.kdbx`. Он также включает функцию `set_project_root` для определения корневого каталога проекта.

## Функции

### `set_project_root`

**Описание**: Функция определяет корневой каталог проекта, начиная с текущего каталога. Поиск идет вверх по каталогам до тех пор, пока не будет найден каталог, содержащий один из файлов в списке `marker_files`.

**Параметры**:

- `marker_files` (tuple): Кортеж строк, представляющих имена файлов или каталогов, используемые для идентификации корневого каталога проекта. По умолчанию ищет следующие маркеры: `pyproject.toml`, `requirements.txt`, `.git`.

**Возвращает**:

- `Path`: Путь к корневому каталогу проекта, если он найден, в противном случае - путь к каталогу, в котором расположен скрипт.

### `singleton`

**Описание**: Декоратор для создания класса-одиночки (singleton).

**Параметры**:

- `cls`: Класс, который должен быть преобразован в класс-одиночку.

**Возвращает**:

- `function`: Функция, которая возвращает экземпляр класса-одиночки.

## Классы

### `ProgramSettings`

**Описание**: Класс для настроек программы. Он устанавливает основные параметры и настройки проекта. Он загружает конфигурацию из `config.json` и данные учетных данных из файла базы данных KeePass `credentials.kdbx`.

**Атрибуты**:

- `host_name` (str): Имя хоста.
- `base_dir` (Path): Путь к корневому каталогу проекта.
- `config` (SimpleNamespace): Объект, содержащий конфигурацию проекта.
- `credentials` (SimpleNamespace): Объект, содержащий учетные данные.
- `MODE` (str): Режим работы проекта (например, 'dev', 'prod').
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

## Заметки

- Модуль использует PyKeePass для работы с файлом `credentials.kdbx`.
- В коде присутствуют блоки обработки исключений (`ex`).
- Файл паролей (`password.txt`) содержит пароли в открытом виде. Это потенциальная уязвимость. Необходимо разработать безопасный механизм хранения паролей.

## Инициализация и конфигурация

Когда проект запускается, он инициализирует и настраивает различные параметры и учетные данные. В этом документе объясняется, как эти значения устанавливаются и управляются.

### Определение корневого каталога проекта

Проект автоматически определяет свой корневой каталог, выполняя поиск вверх от текущего каталога файла для определенных файлов-маркеров (`pyproject.toml`, `requirements.txt`, `.git`). Это гарантирует, что проект сможет найти свои ресурсы независимо от текущего рабочего каталога.

```python
def set_project_root(marker_files=('__root__','.git')) -> Path:
    """
    Функция определяет корневой каталог проекта, начиная с текущего каталога файла,
    выполняя поиск вверх и останавливаясь на первом каталоге, содержащем любой из файлов-маркеров.
    
    Args:
        marker_files (tuple): Имена файлов или каталогов для идентификации корневого каталога проекта.
    
    Returns:
        Path: Путь к корневому каталогу, если он найден, в противном случае - каталог, в котором расположен скрипт.
    """
    __root__:Path
    current_path:Path = Path(__file__).resolve().parent
    __root__ = current_path
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            __root__ = parent
            break
    if __root__ not in sys.path:
        sys.path.insert(0, str(__root__))
    return __root__
```

### Загрузка конфигурации

Проект загружает свои настройки по умолчанию из файла `config.json`, расположенного в каталоге `src`. Этот JSON-файл содержит различные параметры конфигурации, такие как:

- **Информация об авторе**: Подробности об авторе.
- **Доступные режимы**: Поддерживаемые режимы (`dev`, `debug`, `test`, `prod`).
- **Пути**: Каталоги для журналов, временных файлов, внешнего хранилища и Google Drive.
- **Сведения о проекте**: Имя, версия и информация о выпуске проекта.

```python
self.config = j_loads_ns(self.base_dir / 'src' / 'config.json')
if not self.config:
    logger.error('Error loading settings')
    ...
    return

self.config.project_name = self.base_dir.name
```

### Управление учетными данными с помощью KeePass

**Что такое KeePass?**

KeePass - это бесплатный менеджер паролей с открытым исходным кодом, который надежно хранит ваши пароли и другую конфиденциальную информацию в зашифрованной базе данных. База данных защищена главным паролем, который является единственным паролем, который вам нужно запомнить. KeePass использует надежные алгоритмы шифрования (такие как AES и Twofish) для обеспечения безопасности ваших данных.

**Почему KeePass хорош?**

- **Безопасность**: KeePass использует отраслевые стандарты шифрования для защиты ваших данных, что делает его очень безопасным от несанкционированного доступа.
- **Портативность**: Вы можете хранить свою базу данных KeePass на USB-накопителе или в облачном хранилище и получать к ней доступ с нескольких устройств.
- **Настройка**: KeePass позволяет организовывать ваши пароли в группы и подгруппы, что упрощает управление большим количеством учетных данных.
- **Открытый исходный код**: Будучи проектом с открытым исходным кодом, KeePass является прозрачным и может быть проверен сообществом на предмет его безопасности.

**Как KeePass работает в этом проекте**

Учетные данные надежно управляются с помощью базы данных KeePass (`credentials.kdbx`). Главный пароль для этой базы данных обрабатывается по-разному в зависимости от среды:

- **Режим разработки**: Пароль считывается из файла с именем `password.txt`, расположенного в каталоге `secrets`.
- **Производственный режим**: Пароль вводится через консоль. (Удалите файл `password.txt` из каталога `secrets`)

```python
def _open_kp(self, retry: int = 3) -> PyKeePass | None:
    """ Открывает базу данных KeePass
    Args:
        retry (int): Количество попыток
    """
    while retry > 0:
        try:
            password:str = Path( self.path.secrets / 'password.txt').read_text(encoding="utf-8") or None
            kp = PyKeePass(str(self.path.secrets / 'credentials.kdbx'), 
                           password = password or getpass.getpass(print('Enter KeePass master password: ').lower()))
            return kp
        except Exception as ex:
            print(f"Failed to open KeePass database. Exception: {ex}, {retry-1} retries left.")
            ...
            retry -= 1
            if retry < 1:
                logger.critical('Failed to open KeePass database after multiple attempts', exc_info=True)
                ...
                sys.exit()
```

### Древовидная структура базы данных KeePass

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
   - Содержит учетные данные Aliexpress API.
   - Пример записи: `self.credentials.aliexpress.api_key`, `self.credentials.aliexpress.secret`, `self.credentials.aliexpress.tracking_id`, `self.credentials.aliexpress.email`, `self.credentials.aliexpress.password`.

2. **openai**:
   - Содержит ключи OpenAI API.
   - Пример записи: `self.credentials.openai.api_key`.

3. **openai/assistants**:
   - Содержит идентификаторы помощников OpenAI.
   - Пример записи: `self.credentials.openai.assistant_id`.

4. **gemini**:
   - Содержит учетные данные GoogleAI.
   - Пример записи: `self.credentials.gemini.api_key`.

5. **telegram**:
   - Содержит учетные данные Telegram.
   - Пример записи: `self.credentials.telegram.token`.

6. **discord**:
   - Содержит учетные данные Discord.
   - Пример записи: `self.credentials.discord.application_id`, `self.credentials.discord.public_key`, `self.credentials.discord.bot_token`.

7. **prestashop**:
   - Содержит учетные данные PrestaShop.
   - Пример записи: `self.credentials.presta.client.api_key`, `self.credentials.presta.client.api_domain`, `self.credentials.presta.client.db_server`, `self.credentials.presta.client.db_user`, `self.credentials.presta.client.db_password`.

8. **prestashop/clients**:
   - Содержит учетные данные клиента PrestaShop.
   - Пример записи: `self.credentials.presta.client.api_key`, `self.credentials.presta.client.api_domain`, `self.credentials.presta.client.db_server`, `self.credentials.presta.client.db_user`, `self.credentials.presta.client.db_password`.

9. **prestashop/translation**:
   - Содержит учетные данные перевода PrestaShop.
   - Пример записи: `self.credentials.presta.translations.server`, `self.credentials.presta.translations.port`, `self.credentials.presta.translations.database`, `self.credentials.presta.translations.user`, `self.credentials.presta.translations.password`.

10. **smtp**:
    - Содержит учетные данные SMTP.
    - Пример записи: `self.credentials.smtp.server`, `self.credentials.smtp.port`, `self.credentials.smtp.user`, `self.credentials.smtp.password`.

11. **facebook**:
    - Содержит учетные данные Facebook.
    - Пример записи: `self.credentials.facebook.app_id`, `self.credentials.facebook.app_secret`, `self.credentials.facebook.access_token`.

12. **google/gapi**:
    - Содержит учетные данные Google API.
    - Пример записи: `self.credentials.gapi.api_key`.

### Заметки:

- Каждая группа (`group`) в KeePass соответствует определенному пути (`path`).
- Каждая запись (`entry`) в группе содержит определенные учетные данные.
- Методы `_load_*_credentials` загружают данные из соответствующих групп и записей в базе данных KeePass и сохраняют их в атрибутах объекта `self.credentials`.

### Глобальный экземпляр `ProgramSettings`

```python
# Глобальный экземпляр ProgramSettings
gs: ProgramSettings = ProgramSettings()
```

**Зачем это нужно?**

Этот глобальный экземпляр `ProgramSettings` (`gs`) создается для предоставления доступа к настройкам проекта и учетным данным из любой точки кода. Таким образом, вам не нужно создавать новый экземпляр класса `ProgramSettings` каждый раз, когда вам нужно получить доступ к настройкам или учетным данным.

**Как это используется?**

В других модулях проекта вы можете импортировать этот глобальный экземпляр и использовать его для доступа к настройкам и учетным данным:

```python
from src import gs

# Пример использования
api_key = gs.credentials.openai.api_key
```

Это упрощает доступ к настройкам и учетным данным, делая код более чистым и удобным в использовании.