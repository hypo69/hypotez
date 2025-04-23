# Module: src.credentials

## Overview

This document provides an overview of the `ProgramSettings` class, which is responsible for loading and storing credentials and project settings from a KeePass database and a configuration file.

## Table of Contents

- [Functions](#functions)
  - [`set_project_root`](#set_project_root)
  - [`singleton`](#singleton)
- [Classes](#classes)
  - [`ProgramSettings`](#programsettings)
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

## Functions

### `set_project_root`

**Description**: Находит корневой каталог проекта, начиная с текущего каталога файла. Поиск выполняется вверх по каталогам, пока не будет найден каталог, содержащий один из файлов в списке `marker_files`.

**Parameters**:

- `marker_files` (tuple): Кортеж строк, представляющих имена файлов или каталогов, используемых для идентификации корневого каталога проекта. По умолчанию выполняется поиск следующих маркеров: `pyproject.toml`, `requirements.txt`, `.git`.

**Returns**:

- `Path`: Путь к корневому каталогу проекта, если он найден, в противном случае — путь к каталогу, в котором расположен скрипт.

**How the function works**:

- Функция получает путь к текущему файлу и его родительскому каталогу.
- Она ищет родительские каталоги, пока не найдет один из файлов-маркеров (`pyproject.toml`, `requirements.txt`, `.git`).
- Если маркер найден, функция возвращает путь к этому каталогу.
- Если маркер не найден, функция возвращает путь к каталогу, в котором расположен скрипт.

**Examples**:
```python
from pathlib import Path

# Предположим, что текущий файл находится в подкаталоге проекта
# и корневой каталог содержит файл pyproject.toml
root_path = set_project_root(marker_files=('pyproject.toml',))
print(root_path)
# Output: Path('/путь/к/корневому/каталогу')

# Если файлы-маркеры не найдены, возвращается каталог, в котором находится скрипт
root_path = set_project_root(marker_files=('nonexistent_file',))
print(root_path)
# Output: Path('/путь/к/текущему/каталогу')
```

### `singleton`

**Description**: Декоратор для создания класса-одиночки (singleton).

**Parameters**:

- `cls`: Класс, который должен быть преобразован в класс-одиночку.

**Returns**:

- `function`: Функция, возвращающая экземпляр класса-одиночки.

## Classes

### `ProgramSettings`

**Description**: Класс для настроек программы. Устанавливает основные параметры и настройки проекта. Загружает конфигурацию из `config.json` и данные учетных данных из файла базы данных KeePass `credentials.kdbx`.

**Attributes**:

- `host_name` (str): Имя хоста.
- `base_dir` (Path): Путь к корневому каталогу проекта.
- `config` (SimpleNamespace): Объект, содержащий конфигурацию проекта.
- `credentials` (SimpleNamespace): Объект, содержащий учетные данные.
- `MODE` (str): Режим работы проекта (например, 'dev', 'prod').
- `path` (SimpleNamespace): Объект, содержащий пути к различным каталогам проекта.

**Methods**:

- [`__init__(self, **kwargs)`](#__init__): Инициализирует экземпляр класса.
- [`_load_credentials(self) -> None`](#_load_credentials): Загружает учетные данные из KeePass.
- [`_open_kp(self, retry: int = 3) -> PyKeePass | None`](#_open_kp): Открывает базу данных KeePass. Обрабатывает возможные исключения при открытии базы данных.
- [`_load_aliexpress_credentials(self, kp: PyKeePass) -> bool`](#_load_aliexpress_credentials): Загружает учетные данные Aliexpress из KeePass.
- [`_load_openai_credentials(self, kp: PyKeePass) -> bool`](#_load_openai_credentials): Загружает учетные данные OpenAI из KeePass.
- [`_load_gemini_credentials(self, kp: PyKeePass) -> bool`](#_load_gemini_credentials): Загружает учетные данные GoogleAI из KeePass.
- [`_load_telegram_credentials(self, kp: PyKeePass) -> bool`](#_load_telegram_credentials): Загружает учетные данные Telegram из KeePass.
- [`_load_discord_credentials(self, kp: PyKeePass) -> bool`](#_load_discord_credentials): Загружает учетные данные Discord из KeePass.
- [`_load_PrestaShop_credentials(self, kp: PyKeePass) -> bool`](#_load_prestashop_credentials): Загружает учетные данные PrestaShop из KeePass.
- [`_load_presta_translations_credentials(self, kp: PyKeePass) -> bool`](#_load_presta_translations_credentials): Загружает учетные данные PrestaShop Translations из KeePass.
- [`_load_smtp_credentials(self, kp: PyKeePass) -> bool`](#_load_smtp_credentials): Загружает учетные данные SMTP из KeePass.
- [`_load_facebook_credentials(self, kp: PyKeePass) -> bool`](#_load_facebook_credentials): Загружает учетные данные Facebook из KeePass.
- [`_load_gapi_credentials(self, kp: PyKeePass) -> bool`](#_load_gapi_credentials): Загружает учетные данные Google API из KeePass.
- [`now(self) -> str`](#now): Возвращает текущую временную метку в формате, указанном в файле `config.json`.

**Working principle**:

Класс `ProgramSettings` инициализирует настройки проекта, загружая конфигурацию из файла `config.json` и учетные данные из базы данных KeePass (`credentials.kdbx`).  Он также определяет корневой каталог проекта и предоставляет доступ к различным путям проекта. Класс использует паттерн Singleton, чтобы гарантировать, что существует только один экземпляр класса. Это позволяет получить доступ к настройкам проекта и учетным данным из любого места в коде без необходимости повторной загрузки конфигурации.

### `__init__`

**Description**: Инициализирует экземпляр класса `ProgramSettings`.

**Parameters**:

- `**kwargs`: Произвольные ключевые аргументы.

**How the method works**:

- Загружает конфигурацию проекта из файла `config.json`.
- Инициализирует атрибут `path` с путями к различным каталогам проекта.
- Вызывает `check_latest_release` для проверки новой версии проекта.
- Загружает учетные данные из `credentials.kdbx`.

### `_load_credentials`

**Description**: Загружает учетные данные из KeePass.

**How the method works**:

- Вызывает метод `_open_kp` для открытия базы данных KeePass.
- Вызывает методы `_load_*_credentials` для загрузки различных типов учетных данных (Aliexpress, OpenAI, Gemini, Telegram, Discord, PrestaShop, SMTP, Facebook, Google API).
- Если база данных KeePass не открывается, выводит сообщение об ошибке.

### `_open_kp`

**Description**: Открывает базу данных KeePass. Обрабатывает возможные исключения при открытии базы данных.

**Parameters**:

- `retry` (int): Количество попыток повторного открытия базы данных. По умолчанию 3.

**Returns**:

- `PyKeePass | None`: Объект `PyKeePass`, представляющий открытую базу данных, или `None`, если не удалось открыть базу данных после нескольких попыток.

**How the method works**:

- Выполняет попытки открыть базу данных KeePass, используя пароль, указанный в файле `password.txt` (если он существует) или введенный пользователем через консоль.
- В случае ошибки открытия базы данных повторяет попытку несколько раз.
- Если после нескольких попыток не удается открыть базу данных, записывает критическую ошибку в лог и завершает работу программы.

### `_load_aliexpress_credentials`

**Description**: Загружает учетные данные Aliexpress из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает учетные данные Aliexpress (api_key, secret, tracking_id, email, password) из базы данных KeePass.
- Сохраняет учетные данные в атрибутах объекта `self.credentials.aliexpress`.

### `_load_openai_credentials`

**Description**: Загружает учетные данные OpenAI из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает API-ключ OpenAI из базы данных KeePass.
- Сохраняет API-ключ в атрибуте объекта `self.credentials.openai.api_key`.

### `_load_gemini_credentials`

**Description**: Загружает учетные данные GoogleAI из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает API-ключ GoogleAI из базы данных KeePass.
- Сохраняет API-ключ в атрибуте объекта `self.credentials.gemini.api_key`.

### `_load_telegram_credentials`

**Description**: Загружает учетные данные Telegram из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает токен Telegram из базы данных KeePass.
- Сохраняет токен в атрибуте объекта `self.credentials.telegram.token`.

### `_load_discord_credentials`

**Description**: Загружает учетные данные Discord из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает идентификатор приложения Discord, открытый ключ и токен бота из базы данных KeePass.
- Сохраняет эти учетные данные в атрибутах объекта `self.credentials.discord`.

### `_load_PrestaShop_credentials`

**Description**: Загружает учетные данные PrestaShop из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает учетные данные клиента PrestaShop (api_key, api_domain, db_server, db_user, db_password) из базы данных KeePass.
- Сохраняет эти учетные данные в атрибутах объекта `self.credentials.presta.client`.

### `_load_presta_translations_credentials`

**Description**: Загружает учетные данные PrestaShop Translations из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает учетные данные для переводов PrestaShop (server, port, database, user, password) из базы данных KeePass.
- Сохраняет эти учетные данные в атрибутах объекта `self.credentials.presta.translations`.

### `_load_smtp_credentials`

**Description**: Загружает учетные данные SMTP из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает учетные данные SMTP (server, port, user, password) из базы данных KeePass.
- Сохраняет эти учетные данные в атрибутах объекта `self.credentials.smtp`.

### `_load_facebook_credentials`

**Description**: Загружает учетные данные Facebook из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает идентификатор приложения Facebook, секрет приложения и токен доступа из базы данных KeePass.
- Сохраняет эти учетные данные в атрибутах объекта `self.credentials.facebook`.

### `_load_gapi_credentials`

**Description**: Загружает учетные данные Google API из KeePass.

**Parameters**:

- `kp` (PyKeePass): Объект `PyKeePass`, представляющий открытую базу данных KeePass.

**Returns**:

- `bool`: `True`, если учетные данные успешно загружены, `False` в противном случае.

**How the method works**:

- Извлекает API-ключ Google API из базы данных KeePass.
- Сохраняет API-ключ в атрибуте объекта `self.credentials.gapi.api_key`.

### `now`

**Description**: Возвращает текущую временную метку в формате, указанном в файле `config.json`.

**Returns**:

- `str`: Текущая временная метка в строковом формате.

**How the method works**:

- Получает формат временной метки из конфигурации проекта.
- Форматирует текущее время с использованием указанного формата.
- Возвращает отформатированную временную метку в виде строки.