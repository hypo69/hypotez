## \file /src/keepass_documentation.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Документация по модулю KeePass для проекта hypotez
=================================================

Данный документ описывает функциональность и принципы работы подсистемы управления
учетными данными проекта `hypotez`, использующей базу данных KeePass (`credentials.kdbx`)
и библиотеку `pykeepass`. Основная задача подсистемы - безопасное хранение и загрузка
API ключей, логинов, паролей и других конфиденциальных данных, необходимых для работы
различных компонентов проекта.

Зависимости:
    - pykeepass (pip install pykeepass)

 .. module:: src.keepass
"""

# ИНСТРУКЦИЯ

# СОДЕРЖАНИЕ

- [Обзор](#обзор)
- [Подробней: Процесс работы с базой данных KeePass](#подробней-процесс-работы-с-базой-данных-keepass)
    - [Открытие базы данных](#открытие-базы-данных)
    - [Загрузка учетных данных](#загрузка-учетных-данных)
- [Загрузка учетных данных по категориям](#загрузка-учетных-данных-по-категориям)
    - [Aliexpress](#aliexpress)
    - [OpenAI](#openai)
    - [Gemini](#gemini)
    - [Telegram](#telegram)
    - [Discord](#discord)
    - [PrestaShop](#prestashop)
        - [Клиенты](#клиенты)
        - [Переводы](#переводы)
    - [SMTP](#smtp)
    - [Facebook](#facebook)
    - [Google API](#google-api)

---

# Документация по модулю KeePass

## Обзор

Модуль `keepass` в проекте `hypotez` предназначен для централизованного и безопасного
хранения и извлечения конфиденциальных учетных данных, таких как API ключи, логины,
пароли и настройки доступа к различным сервисам. Для этих целей используется
зашифрованная база данных KeePass (`credentials.kdbx`) и библиотека `pykeepass`
для программного доступа к ней.

Вся логика работы с базой данных KeePass инкапсулирована в классе
`ProgramSettings`. Этот класс реализован как синглтон, обеспечивая
единственную точку доступа к настроикам и учетным данным в рамках всего приложения.

Учетные данные внутри базы данных KeePass организованы иерархически с помощью
папок и записей. Для хранения специфических данных, не предусмотренных стандартными
полями записей KeePass, активно используются **кастомные свойства** записей.

Извлеченные учетные данные хранятся в объектах `SimpleNamespace`, что позволяет
удобно обращаться к ним как к атрибутам объекта (например, `settings.credentials.aliexpress.api_key`).

## Подробней: Процесс работы с базой данных KeePass

Работа с базой данных KeePass включает два основных этапа: открытие базы данных и
загрузка необходимых учетных данных.

### Открытие базы данных

**Назначение**: Открытие файла базы данных KeePass (`credentials.kdbx`) с использованием
пароля.

**Как работает**:
Процесс открытия базы данных выполняется методом, который:
1.  Осуществляет попытку чтения пароля из файла `password.txt`, если данный файл
    существует в файловой системе.
2.  При отсутствии файла `password.txt` или неудаче чтения, выполняет запрос
    пароля у пользователя через стандартный ввод (консоль).
3.  Использует библиотеку `pykeepass` для попытки открытия файла базы данных
    с использованием полученного пароля.
4.  При неудачной попытке открытия, процедура повторяет попытку несколько раз,
    предоставляя возможность повторного ввода пароля или исправления ошибки.
5.  В случае исчерпания всех попыток и невозможности открыть базу данных,
    программа завершает свое выполнение, предотвращая дальнейшую работу без доступа
    к необходимым учетным данным.

### Загрузка учетных данных

**Назначение**: Загрузка всех необходимых учетных данных из открытой базы данных
KeePass в структуру настроек приложения.

**Как работает**:
После успешного открытия базы данных вызывается метод, который координирует процесс
загрузки. Данный метод:
1.  Вызывает последовательно специализированные методы загрузки, каждый из которых
    отвечает за извлечение учетных данных для определенной категории сервисов или API
    (например, Aliexpress, OpenAI, PrestaShop и т.д.).
2.  Каждый категорийный метод использует функции навигации `pykeepass`, в частности
    `kp.find_groups()`, для обнаружения соответствующих групп и записей в иерархии
    базы данных KeePass.
3.  Из найденных записей извлекаются необходимые данные, используя стандартное поле
    пароля (`entry.password`) и **кастомные свойства** (`entry.custom_properties`).
4.  Извлеченные данные организуются и сохраняются в соответствующем разделе
    структуры `ProgramSettings.credentials`, часто с использованием объектов `SimpleNamespace`
    для удобства доступа по имени атрибута.

## Загрузка учетных данных по категориям

Данный раздел подробно описывает, как извлекаются учетные данные для различных
сервисов из базы данных KeePass.

### Aliexpress

**Назначение**: Загрузка API ключей и учетных данных аккаунта Aliexpress.

**Как работает**:
1.  Выполняется поиск группы с путем `suppliers/aliexpress/api`.
2.  Из найденной записи извлекаются следующие данные из кастомных свойств:
    -   `api_key`
    -   `secret`
    -   `tracking_id`
    -   `email`
3.  Также извлекается пароль записи (`entry.password`).
4.  Извлеченные данные сохраняются в структуре `ProgramSettings.credentials.aliexpress`.
    Доступ к ним осуществляется как к атрибутам объекта `SimpleNamespace`:
    `settings.credentials.aliexpress.api_key`, `settings.credentials.aliexpress.secret`,
    `settings.credentials.aliexpress.tracking_id`, `settings.credentials.aliexpress.email`,
    `settings.credentials.aliexpress.password`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.aliexpress`:
```python
# Пример структуры объекта SimpleNamespace после загрузки
settings.credentials.aliexpress = SimpleNamespace(
    api_key='your_aliexpress_api_key',
    secret='your_aliexpress_secret',
    tracking_id='your_aliexpress_tracking_id',
    email='your_aliexpress_email',
    password='your_aliexpress_password'
)
```

### OpenAI

**Назначение**: Загрузка API ключей и идентификаторов ассистентов OpenAI.

**Как работает**:
1.  Выполняется поиск группы с путем `openai`.
2.  Из каждой записи в этой группе извлекается кастомное свойство `api_key`.
3.  Имя записи используется как имя атрибута при сохранении в `ProgramSettings.credentials.openai`.
4.  Выполняется поиск группы с путем `openai/assistants`.
5.  Из каждой записи в этой группе извлекается кастомное свойство `assistant_id`.
6.  Имя записи используется как имя атрибута при сохранении в
    `ProgramSettings.credentials.openai.assistant_id`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.openai`:
```python
# Пример структуры объекта SimpleNamespace после загрузки API ключей
settings.credentials.openai = SimpleNamespace(
    default_api_key='sk-...', # если имя записи 'default_api_key'
    another_key='sk-...'     # если есть другая запись с именем 'another_key'
)

# Пример структуры объекта SimpleNamespace для ассистентов
settings.credentials.openai.assistant_id = SimpleNamespace(
    assistant_checker='asst_...', # если имя записи 'assistant_checker'
    assistant_writer='asst_...'   # если есть другая запись с именем 'assistant_writer'
)
```

### Gemini

**Назначение**: Загрузка API ключей Gemini.

**Как работает**:
1.  Выполняется поиск группы с путем `gemini`.
2.  Из каждой записи в этой группе извлекается кастомное свойство `api_key`.
3.  Имя записи используется как имя атрибута при сохранении в `ProgramSettings.credentials.gemini`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.gemini`:
```python
# Пример структуры объекта SimpleNamespace после загрузки
settings.credentials.gemini = SimpleNamespace(
    default_key='AIza...', # если имя записи 'default_key'
    another_key='AIza...'  # если есть другая запись с именем 'another_key'
)
```

### Telegram

**Назначение**: Загрузка API токенов Telegram.

**Как работает**:
1.  Выполняется поиск группы с путем `telegram`.
2.  Из каждой записи в этой группе извлекается кастомное свойство `token`.
3.  Имя записи используется как имя атрибута при сохранении в `ProgramSettings.credentials.telegram`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.telegram`:
```python
# Пример структуры объекта SimpleNamespace после загрузки
settings.credentials.telegram = SimpleNamespace(
    bot_main='123456:ABC-DEF...', # если имя записи 'bot_main'
    bot_notifications='789012:GHI-JKL...' # если есть другая запись с именем 'bot_notifications'
)
```

### Discord

**Назначение**: Загрузка API ключей и токенов Discord.

**Как работает**:
1.  Выполняется поиск группы с путем `discord`.
2.  Из каждой записи в этой группе извлекаются следующие данные из кастомных свойств:
    -   `application_id`
    -   `public_key`
    -   `bot_token`
3.  Каждый набор извлеченных данных сохраняется как отдельный объект `SimpleNamespace`.
4.  Эти объекты добавляются в список `ProgramSettings.credentials.discord`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.discord`:
```python
# Пример структуры списка объектов SimpleNamespace после загрузки
settings.credentials.discord = [
    SimpleNamespace(
        application_id='app_id_1',
        public_key='public_key_1',
        bot_token='bot_token_1'
    ),
    SimpleNamespace(
        application_id='app_id_2',
        public_key='public_key_2',
        bot_token='bot_token_2'
    )
]
```

### PrestaShop

**Назначение**: Загрузка учетных данных для различных экземпляров PrestaShop (клиентов)
и настроек доступа к базе данных переводов.

#### Клиенты

**Назначение**: Загрузка учетных данных для доступа к API и базам данных клиентских
установок PrestaShop.

**Как работает**:
1.  Выполняется поиск группы с путем `prestashop/clients`.
2.  Для *каждой* записи в этой группе извлекаются следующие данные из кастомных свойств:
    -   `api_key`
    -   `api_domain`
    -   `db_server`
    -   `db_user`
    -   `db_password`
3.  Каждый набор извлеченных данных сохраняется как отдельный объект `SimpleNamespace`.
4.  Эти объекты добавляются в список `ProgramSettings.credentials.presta.client`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.presta.client`:
```python
# Пример структуры списка объектов SimpleNamespace после загрузки
settings.credentials.presta.client = [
    SimpleNamespace(
        api_key='key1',
        api_domain='domain1.com',
        db_server='db_server1',
        db_user='db_user1',
        db_password='db_password1'
    ),
    SimpleNamespace(
        api_key='key2',
        api_domain='domain2.com',
        db_server='db_server2',
        db_user='db_user2',
        db_password='db_password2'
    )
]
```

#### Переводы

**Назначение**: Загрузка учетных данных для доступа к базе данных, содержащей переводы.

**Как работает**:
1.  Выполняется поиск группы с путем `prestashop/translation`.
2.  Из *первой* найденной записи в этой группе извлекаются следующие данные из
    кастомных свойств:
    -   `server`
    -   `port`
    -   `database`
    -   `user`
    -   `password`
3.  Извлеченные данные сохраняются в структуре `ProgramSettings.credentials.presta.translations`
    как атрибуты объекта `SimpleNamespace`: `settings.credentials.presta.translations.server`,
    `settings.credentials.presta.translations.port` и т.д.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.presta.translations`:
```python
# Пример структуры объекта SimpleNamespace после загрузки
settings.credentials.presta.translations = SimpleNamespace(
    server='translation_db_server',
    port='translation_db_port',
    database='translation_db_name',
    user='translation_db_user',
    password='translation_db_password'
)
```

### SMTP

**Назначение**: Загрузка учетных данных для доступа к SMTP серверам.

**Как работает**:
1.  Выполняется поиск группы с путем `smtp`.
2.  Для *каждой* записи в этой группе извлекаются следующие данные из кастомных свойств:
    -   `server`
    -   `port`
    -   `user`
    -   `password`
3.  Каждый набор извлеченных данных сохраняется как отдельный объект `SimpleNamespace`.
4.  Эти объекты добавляются в список `ProgramSettings.credentials.smtp`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.smtp`:
```python
# Пример структуры списка объектов SimpleNamespace после загрузки
settings.credentials.smtp = [
    SimpleNamespace(
        server='smtp.server1.com',
        port='587',
        user='user1@example.com',
        password='password1'
    ),
    SimpleNamespace(
        server='smtp.server2.com',
        port='465',
        user='user2@example.com',
        password='password2'
    )
]
```

### Facebook

**Назначение**: Загрузка API ключей и токенов Facebook.

**Как работает**:
1.  Выполняется поиск группы с путем `facebook`.
2.  Для *каждой* записи в этой группе извлекаются следующие данные из кастомных свойств:
    -   `app_id`
    -   `app_secret`
    -   `access_token`
3.  Каждый набор извлеченных данных сохраняется как отдельный объект `SimpleNamespace`.
4.  Эти объекты добавляются в список `ProgramSettings.credentials.facebook`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.facebook`:
```python
# Пример структуры списка объектов SimpleNamespace после загрузки
settings.credentials.facebook = [
    SimpleNamespace(
        app_id='app_id_1',
        app_secret='app_secret_1',
        access_token='access_token_1'
    ),
    SimpleNamespace(
        app_id='app_id_2',
        app_secret='app_secret_2',
        access_token='access_token_2'
    )
]
```

### Google API

**Назначение**: Загрузка API ключей Google.

**Как работает**:
1.  Выполняется поиск группы с путем `google/gapi`.
2.  Из каждой записи в этой группе извлекается кастомное свойство `api_key`.
3.  Извлеченные данные сохраняются в структуре `ProgramSettings.credentials.gapi`
    по ключу `api_key`.

**Примеры**:
Предполагаемое хранение в `ProgramSettings.credentials.gapi`:
```python
# Пример структуры после загрузки
settings.credentials.gapi = {
    'api_key': 'AIzaSy...' # если имя записи 'default' или подобное
}
```