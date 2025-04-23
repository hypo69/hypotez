# Module Name

## Overview

Описание принципов работы с базой данных KeePass, используемой в проекте для хранения зашифрованных учетных данных. Модуль использует библиотеку `pykeepass` для доступа к файлу `credentials.kdbx` и реализует механизм загрузки различных учетных данных, таких как API-ключи, пароли и логины, из иерархической структуры базы данных KeePass.

## More details

Модуль предназначен для централизованного управления учетными данными, необходимыми для работы с различными сервисами и API. Он обеспечивает безопасное хранение и удобный доступ к этим данным через класс `ProgramSettings`, который является синглтоном. Это гарантирует, что все части приложения используют один и тот же экземпляр настроек.

## Classes

### `ProgramSettings`

**Description**: Класс-синглтон для управления настройками и учетными данными, хранящимися в базе данных KeePass.

**Inherits**: Класс не наследует от других классов.

**Attributes**:
- `kp`: Объект базы данных KeePass.
- `credentials`: Объект `SimpleNamespace`, содержащий учетные данные для различных сервисов.

**Working principle**:
1. Класс `ProgramSettings` является синглтоном, что означает, что у него может быть только один экземпляр. Это обеспечивается через метакласс `Singleton`.
2. При создании экземпляра класса происходит открытие базы данных KeePass с использованием метода `_open_kp`.
3. После открытия базы данных вызывается метод `_load_credentials` для загрузки учетных данных из базы данных KeePass и сохранения их в атрибуте `credentials`.
4. Класс предоставляет методы для получения учетных данных для различных сервисов, таких как Aliexpress, OpenAI, Gemini, Discord, PrestaShop, SMTP, Facebook и Google API.

**Methods**:
- `_open_kp`: Открывает базу данных KeePass.
- `_load_credentials`: Загружает учетные данные из базы данных KeePass.

## Class Methods

### `_open_kp`

```python
def _open_kp():
    """ Открывает базу данных KeePass.

    Args:
        Нет аргументов.

    Returns:
        None

    Raises:
        SystemExit: Если не удается открыть базу данных после нескольких попыток.

    """
```

**Purpose**: Открывает базу данных KeePass, используя пароль из файла или запрашивая его у пользователя.

**How the function works**:

1. Функция пытается прочитать пароль из файла `password.txt`.
2. Если файл не существует, функция запрашивает пароль у пользователя через консоль.
3. Функция пытается открыть базу данных KeePass с использованием полученного пароля.
4. Если открытие не удалось, функция повторяет попытку несколько раз.
5. Если все попытки неудачны, программа завершает работу.

**Examples**:
Вызов функции:

```python
ProgramSettings._open_kp()
```

### `_load_credentials`

```python
def _load_credentials():
    """ Загружает учетные данные из базы данных KeePass.

    Args:
        Нет аргументов.

    Returns:
        None

    Raises:
        Нет исключений.

    """
```

**Purpose**: Загружает учетные данные для различных сервисов из базы данных KeePass и сохраняет их в атрибуте `credentials`.

**How the function works**:

1. Функция вызывает методы загрузки учетных данных для каждой категории учетных данных, таких как Aliexpress, OpenAI, Gemini, Telegram, Discord, PrestaShop, SMTP, Facebook и Google API.
2. Эти методы используют `kp.find_groups` для поиска групп и записей в базе данных KeePass.
3. Далее, из каждой записи извлекаются необходимые данные (например, API ключи, пароли, логины) через `entry.custom_properties` и `entry.password`.
4. Извлеченные данные сохраняются в `ProgramSettings.credentials` в виде атрибутов.

**Examples**:
Вызов функции:

```python
ProgramSettings._load_credentials()
```

## Class Parameters

- `kp`: Объект базы данных KeePass.
- `credentials`: Объект `SimpleNamespace`, содержащий учетные данные для различных сервисов.

**Examples**:

Пример использования класса `ProgramSettings`:

```python
settings = ProgramSettings()
aliexpress_credentials = settings.credentials.aliexpress
print(aliexpress_credentials.api_key)
```
```