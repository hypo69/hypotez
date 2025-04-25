# Модуль `keepass`
## Обзор
Модуль предоставляет функциональность для доступа к учетным данным, хранящимся в файле базы данных KeePass (`credentials.kdbx`).

## Подробнее
Модуль использует библиотеку `pykeepass` для взаимодействия с базой данных KeePass. 
Он  предоставляет следующие возможности:

*  **Чтение учетных данных из KeePass:** модуль позволяет извлекать учетные данные из KeePass, такие как API ключи, пароли, логины, используя кастомные свойства записей.
*  **Хранение учетных данных:**  данные, извлеченные из KeePass, сохраняются в объекте `ProgramSettings`, который является синглтоном, что обеспечивает единый доступ к учетным данным из разных частей приложения.
*  **Использование SimpleNamespace:** для удобного доступа к данным в объекте `ProgramSettings` используются объекты `SimpleNamespace`. Это позволяет обращаться к данным как к атрибутам объекта.

## Классы
### `ProgramSettings`
**Описание**: Класс для хранения настроек приложения и учетных данных, извлеченных из KeePass.
**Наследует**: 
    - `SimpleNamespace`
**Атрибуты**:
    - `credentials`:  Объект `SimpleNamespace`, содержащий учетные данные для различных сервисов:
    - `credentials.aliexpress`: Объект `SimpleNamespace` для хранения учетных данных Aliexpress.
    - `credentials.aliexpress.api_key`: API ключ Aliexpress.
    - `credentials.aliexpress.secret`: Secret ключ Aliexpress.
    - `credentials.aliexpress.tracking_id`: Tracking ID Aliexpress.
    - `credentials.aliexpress.email`: Email адрес Aliexpress.
    - `credentials.aliexpress.password`: Пароль для Aliexpress.
    - `credentials.openai`: Объект `SimpleNamespace` для хранения учетных данных OpenAI.
    - `credentials.openai.api_key`: API ключ OpenAI.
    - `credentials.openai.project_api`: API ключ проекта OpenAI.
    - `credentials.openai.assistant_id`: ID ассистента OpenAI.
    - `credentials.gemini`: Объект `SimpleNamespace` для хранения учетных данных Gemini.
    - `credentials.gemini.api_key`: API ключ Gemini.
    - `credentials.telegram`: Объект `SimpleNamespace` для хранения учетных данных Telegram.
    - `credentials.telegram.token`: Токен Telegram.
    - `credentials.discord`: Объект `SimpleNamespace` для хранения учетных данных Discord.
    - `credentials.discord.application_id`: ID приложения Discord.
    - `credentials.discord.public_key`: Public key Discord.
    - `credentials.discord.bot_token`: Bot token Discord.
    - `credentials.presta`: Объект `SimpleNamespace` для хранения учетных данных PrestaShop.
    - `credentials.presta.client`: Список объектов `SimpleNamespace`, содержащих учетные данные для каждого клиента PrestaShop.
    - `credentials.presta.client.api_key`: API ключ PrestaShop.
    - `credentials.presta.client.api_domain`: Домен API PrestaShop.
    - `credentials.presta.client.db_server`: Сервер базы данных PrestaShop.
    - `credentials.presta.client.db_user`: Пользователь базы данных PrestaShop.
    - `credentials.presta.client.db_password`: Пароль для базы данных PrestaShop.
    - `credentials.presta.translations`: Объект `SimpleNamespace` для хранения учетных данных для работы с переводом в PrestaShop.
    - `credentials.presta.translations.server`: Сервер базы данных для перевода.
    - `credentials.presta.translations.port`: Порт базы данных для перевода.
    - `credentials.presta.translations.database`: Название базы данных для перевода.
    - `credentials.presta.translations.user`: Пользователь базы данных для перевода.
    - `credentials.presta.translations.password`: Пароль для базы данных для перевода.
    - `credentials.smtp`: Список объектов `SimpleNamespace`, содержащих учетные данные для каждого SMTP-сервера.
    - `credentials.smtp.server`: SMTP-сервер.
    - `credentials.smtp.port`: Порт SMTP-сервера.
    - `credentials.smtp.user`: Пользователь SMTP-сервера.
    - `credentials.smtp.password`: Пароль SMTP-сервера.
    - `credentials.facebook`: Список объектов `SimpleNamespace`, содержащих учетные данные для Facebook.
    - `credentials.facebook.app_id`: ID приложения Facebook.
    - `credentials.facebook.app_secret`: Secret ключ приложения Facebook.
    - `credentials.facebook.access_token`: Access token Facebook.
    - `credentials.gapi`: Объект `SimpleNamespace` для хранения учетных данных для Google API.
    - `credentials.gapi.api_key`: API ключ Google API.
    - `credentials.vk`: Объект `SimpleNamespace` для хранения учетных данных VK API.
    - `credentials.vk.api_key`: API ключ VK API.
    - `credentials.vk.client_secret`: Secret ключ VK API.
    - `credentials.vk.access_token`: Access token VK API.
    - `credentials.vk.group_id`: ID группы VK.
    - `credentials.vk.user_id`: ID пользователя VK.

**Методы**:
    - `_open_kp()`: Открывает файл базы данных KeePass.
    - `_load_credentials()`: Загружает учетные данные из KeePass.
    - `_load_aliexpress()`: Загружает учетные данные для Aliexpress.
    - `_load_openai()`: Загружает учетные данные для OpenAI.
    - `_load_gemini()`: Загружает учетные данные для Gemini.
    - `_load_telegram()`: Загружает учетные данные для Telegram.
    - `_load_discord()`: Загружает учетные данные для Discord.
    - `_load_prestashop()`: Загружает учетные данные для PrestaShop.
    - `_load_smtp()`: Загружает учетные данные для SMTP.
    - `_load_facebook()`: Загружает учетные данные для Facebook.
    - `_load_google_api()`: Загружает учетные данные для Google API.
    - `_load_vk_api()`: Загружает учетные данные для VK API.

**Примеры**:
    ```python
    # Создание экземпляра ProgramSettings
    settings = ProgramSettings()

    # Получение API ключа OpenAI
    openai_api_key = settings.credentials.openai.api_key
    ```
## Параметры класса
- `credentials`: Объект `SimpleNamespace`, хранящий все учетные данные.


## Функции 
### `get_program_settings()`:
**Назначение**: Возвращает экземпляр класса `ProgramSettings`, который используется для доступа к настройкам приложения и учетным данным.

**Примеры**:
    ```python
    # Получение экземпляра ProgramSettings
    settings = get_program_settings()

    # Получение API ключа Aliexpress
    aliexpress_api_key = settings.credentials.aliexpress.api_key
    ```
## Внутренние функции
### `_open_kp()`:
**Назначение**: Открывает файл базы данных KeePass.
**Параметры**:
    - `path`: Путь к файлу базы данных KeePass.
**Возвращает**:
    - Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Вызывает исключения**:
    - `FileNotFoundError`: Если файл базы данных KeePass не найден.
    - `KeyError`: Если в файле `password.txt` нет пароля или если введенный пароль не верен.
**Как работает функция**:
    - Сначала функция проверяет наличие файла `password.txt`.
    - Если файл существует, она пытается прочитать пароль из него.
    - Если файл не существует, она запрашивает пароль у пользователя через консоль.
    - После получения пароля функция пытается открыть файл базы данных KeePass.
    - Если попытка открытия неудачна, функция повторяет попытку несколько раз.
    - Если все попытки неудачны, функция вызывает исключение `KeyError`.
**Примеры**:
    ```python
    # Открытие файла базы данных KeePass
    kp = _open_kp(path='credentials.kdbx')
    ```

### `_load_credentials()`:
**Назначение**: Загружает учетные данные из KeePass.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных из KeePass.
**Как работает функция**:
    - Функция вызывает методы `_load_aliexpress()`, `_load_openai()`, `_load_gemini()`, `_load_telegram()`, `_load_discord()`, `_load_prestashop()`, `_load_smtp()`, `_load_facebook()`, `_load_google_api()`, `_load_vk_api()` для загрузки учетных данных для каждого сервиса.
**Примеры**:
    ```python
    # Загрузка учетных данных из KeePass
    _load_credentials(kp=kp)
    ```
### `_load_aliexpress()`:
**Назначение**: Загружает учетные данные для Aliexpress.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для Aliexpress.
**Как работает функция**:
    - Функция ищет группу `suppliers/aliexpress/api` в базе данных KeePass.
    - Если группа найдена, функция извлекает из записи `api_key`, `secret`, `tracking_id`, `email` из кастомных свойств записи и `password` из пароля записи.
    - Эти данные сохраняются в `ProgramSettings.credentials.aliexpress` в виде атрибутов `api_key`, `secret`, `tracking_id`, `email` и `password`.
**Примеры**:
    ```python
    # Загрузка учетных данных для Aliexpress
    _load_aliexpress(kp=kp)
    ```
### `_load_openai()`:
**Назначение**: Загружает учетные данные для OpenAI.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для OpenAI.
**Как работает функция**:
    - Функция ищет группу `openai` в базе данных KeePass.
    - Если группа найдена, функция извлекает из записи `api_key`, `project_api` из кастомных свойств записи. Имя записи становится именем атрибута `ProgramSettings.credentials.openai`.
    - Далее, из группы `openai/assistants` извлекаются `assistant_id` из кастомных свойств записи. Имя записи становится именем атрибута `ProgramSettings.credentials.openai.assistant_id`.
**Примеры**:
    ```python
    # Загрузка учетных данных для OpenAI
    _load_openai(kp=kp)
    ```
### `_load_gemini()`:
**Назначение**: Загружает учетные данные для Gemini.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для Gemini.
**Как работает функция**:
    - Функция ищет группу `gemini` в базе данных KeePass.
    - Если группа найдена, функция извлекает из записи `api_key` из кастомных свойств записи. Имя записи становится именем атрибута `ProgramSettings.credentials.gemini`.
**Примеры**:
    ```python
    # Загрузка учетных данных для Gemini
    _load_gemini(kp=kp)
    ```
### `_load_telegram()`:
**Назначение**: Загружает учетные данные для Telegram.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для Telegram.
**Как работает функция**:
    - Функция ищет группу `telegram` в базе данных KeePass.
    - Если группа найдена, функция извлекает из записи `token` из кастомных свойств записи. Имя записи становится именем атрибута `ProgramSettings.credentials.telegram`.
**Примеры**:
    ```python
    # Загрузка учетных данных для Telegram
    _load_telegram(kp=kp)
    ```
### `_load_discord()`:
**Назначение**: Загружает учетные данные для Discord.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для Discord.
**Как работает функция**:
    - Функция ищет группу `discord` в базе данных KeePass.
    - Если группа найдена, функция извлекает из записи `application_id`, `public_key` и `bot_token` из кастомных свойств записи.
    - Эти данные сохраняются в `ProgramSettings.credentials.discord` в виде атрибутов `application_id`, `public_key` и `bot_token`.
**Примеры**:
    ```python
    # Загрузка учетных данных для Discord
    _load_discord(kp=kp)
    ```
### `_load_prestashop()`:
**Назначение**: Загружает учетные данные для PrestaShop.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для PrestaShop.
**Как работает функция**:
    - Функция ищет группу `prestashop/clients` в базе данных KeePass.
    - Если группа найдена, функция извлекает из каждой записи `api_key`, `api_domain`, `db_server`, `db_user`, `db_password` из кастомных свойств.
    - Каждый набор данных добавляется как объект `SimpleNamespace` в список `ProgramSettings.credentials.presta.client`.
    - Далее, функция ищет группу `prestashop/translation` в базе данных KeePass.
    - Если группа найдена, функция извлекает из первой записи `server`, `port`, `database`, `user`, `password` из кастомных свойств.
    - Эти данные сохраняются в `ProgramSettings.credentials.presta.translations`.
**Примеры**:
    ```python
    # Загрузка учетных данных для PrestaShop
    _load_prestashop(kp=kp)
    ```
### `_load_smtp()`:
**Назначение**: Загружает учетные данные для SMTP.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для SMTP.
**Как работает функция**:
    - Функция ищет группу `smtp` в базе данных KeePass.
    - Если группа найдена, функция извлекает из каждой записи `server`, `port`, `user` и `password` из кастомных свойств.
    - Каждый набор данных добавляется как объект `SimpleNamespace` в список `ProgramSettings.credentials.smtp`.
**Примеры**:
    ```python
    # Загрузка учетных данных для SMTP
    _load_smtp(kp=kp)
    ```
### `_load_facebook()`:
**Назначение**: Загружает учетные данные для Facebook.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для Facebook.
**Как работает функция**:
    - Функция ищет группу `facebook` в базе данных KeePass.
    - Если группа найдена, функция извлекает из каждой записи `app_id`, `app_secret` и `access_token` из кастомных свойств.
    - Каждый набор данных добавляется как объект `SimpleNamespace` в список `ProgramSettings.credentials.facebook`.
**Примеры**:
    ```python
    # Загрузка учетных данных для Facebook
    _load_facebook(kp=kp)
    ```
### `_load_google_api()`:
**Назначение**: Загружает учетные данные для Google API.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для Google API.
**Как работает функция**:
    - Функция ищет группу `google/gapi` в базе данных KeePass.
    - Если группа найдена, функция извлекает из записи `api_key` из кастомных свойств записи.
    - Этот данные сохраняются в `ProgramSettings.credentials.gapi` по ключу `api_key`.
**Примеры**:
    ```python
    # Загрузка учетных данных для Google API
    _load_google_api(kp=kp)
    ```
### `_load_vk_api()`:
**Назначение**: Загружает учетные данные для VK API.
**Параметры**:
    - `kp`: Объект `pykeepass.KeePass` - объект, представляющий файл базы данных KeePass.
**Возвращает**:
    - `None`
**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при извлечении учетных данных для VK API.
**Как работает функция**:
    - Функция ищет группу `vk/api` в базе данных KeePass.
    - Если группа найдена, функция извлекает из записи `api_key`, `client_secret` и `access_token` из кастомных свойств.
    - Эти данные сохраняются в `ProgramSettings.credentials.vk` в виде атрибутов `api_key`, `client_secret` и `access_token`.
    - Далее, функция ищет группу `vk/group_id` в базе данных KeePass.
    - Если группа найдена, функция извлекает из первой записи `group_id` из кастомных свойств.
    - Этот данные сохраняются в `ProgramSettings.credentials.vk` по ключу `group_id`.
    - Далее, функция ищет группу `vk/user_id` в базе данных KeePass.
    - Если группа найдена, функция извлекает из первой записи `user_id` из кастомных свойств.
    - Этот данные сохраняются в `ProgramSettings.credentials.vk` по ключу `user_id`.
**Примеры**:
    ```python
    # Загрузка учетных данных для VK API
    _load_vk_api(kp=kp)
    ```


## Примеры
    ```python
    # Получение экземпляра ProgramSettings
    settings = get_program_settings()

    # Получение API ключа OpenAI
    openai_api_key = settings.credentials.openai.api_key
    ```
    ```python
    # Открытие файла базы данных KeePass
    kp = _open_kp(path='credentials.kdbx')

    # Загрузка учетных данных из KeePass
    _load_credentials(kp=kp)

    # Получение API ключа Aliexpress
    aliexpress_api_key = settings.credentials.aliexpress.api_key

    # Получение ID ассистента OpenAI
    assistant_id = settings.credentials.openai.assistant_id

    # Получение токена Telegram
    telegram_token = settings.credentials.telegram.token

    # Получение ID приложения Discord
    discord_application_id = settings.credentials.discord.application_id

    # Получение учетных данных для первого клиента PrestaShop
    prestashop_client = settings.credentials.presta.client[0]
    prestashop_api_key = prestashop_client.api_key

    # Получение учетных данных для SMTP-сервера
    smtp_server = settings.credentials.smtp[0]
    smtp_server_address = smtp_server.server

    # Получение учетных данных для Facebook
    facebook_app_id = settings.credentials.facebook[0].app_id

    # Получение API ключа Google API
    google_api_key = settings.credentials.gapi.api_key

    # Получение API ключа VK API
    vk_api_key = settings.credentials.vk.api_key
    ```