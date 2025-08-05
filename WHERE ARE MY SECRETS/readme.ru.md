<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Корень ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/README.MD'>Документация кода (англ.)</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/readme.ru.md'>Документация кода</A>
</TD>

</TABLE>

# Служебная папка

Это служебная папка, содержащая файлы-примеры:

-   `credentials.kdbx` — база данных паролей в формате KeePass.
-   `password.txt` — текстовый файл, содержащий пароль.
-   JSON-файлы для Google API.

# резервная копия файлов на гугл диске 👉 Google account `koxava.serner@gamil.com`
## Формат данных в `credentials.kdbx`

Файл `credentials.kdbx` служит базой данных паролей в формате KeePass. Он содержит конфиденциальные учетные данные, Используетсяые для различных API и сервисов. Ниже приведены основные группы и поля, ожидаемые в базе данных:

### Группы и их содержимое

1.  **Suppliers > Aliexpress > API**
    -   `api_key`: Ключ API для доступа к Aliexpress API.
    -   `secret`: Секретный ключ для Aliexpress API.
    -   `tracking_id`: Идентификатор отслеживания.
    -   `email`: Адрес электронной почты для аккаунта Aliexpress.
    -   `password`: Пароль для аккаунта Aliexpress.

2.  **OpenAI**
    -   `api_key`: Ключ API для доступа к OpenAI.
    -   Дополнительные свойства могут быть определены для конкретных настроек проекта.

3.  **Gemini**
    -   `api_key`: Ключ API для доступа к Gemini.

4.  **Discord**
    -   `application_id`: ID приложения Discord.
    -   `public_key`: Публичный ключ для приложения Discord.
    -   `bot_token`: Токен бота Discord.

5.  **Telegram**
    -   Токены и настройки для бота Telegram.

6.  **Prestashop**
    -   **Translations (Переводы)**
        -   `server`: Адрес сервера базы данных.
        -   `port`: Порт для подключения к базе данных.
        -   `database`: Имя базы данных.
        -   `user`: Имя пользователя для подключения к базе данных.
        -   `password`: Пароль для подключения к базе данных.
    -   **Clients (Клиенты)**
        -   Каждый клиент хранит свои параметры подключения.

7.  **SMTP**
    -   Каждая запись содержит параметры SMTP-сервера:
        -   `server`: Адрес SMTP-сервера.
        -   `port`: Порт SMTP-сервера.
        -   `user`: Имя пользователя для SMTP.
        -   `password`: Пароль для SMTP.

8.  **Facebook**
    -   Каждая запись содержит:
        -   `app_id`: ID приложения Facebook.
        -   `app_secret`: Секрет приложения Facebook.
        -   `access_token`: Токен доступа для работы с Facebook API.

9.  **Google API (GAPI)**
    -   `api_key`: Ключ API для доступа к Google API.

### Важные замечания

-   Файл `password.txt` содержит одну строку с паролем для доступа к базе данных `credentials.kdbx`. Важно, чтобы **первая строка** содержала **только** пароль.
-   Рекомендуется удалять файл `password.txt` с компьютеров, к которым могут получить доступ посторонние лица.
-   При изменении пароля базы данных вручную, файл `password.txt` также необходимо обновить вручную. **Это ОБЯЗАТЕЛЬНО!**
-   Убедитесь, что структура и имена групп соответствуют ожидаемому формату, чтобы приложение могло корректно загрузить конфиденциальные данные.

Для визуального представления структуры KeePass, пожалуйста, обратитесь к следующему изображению: ![Основная структура KeePass](keepass_main_structure.png).
<br>
<img src="..\images\kepass_main_structure.png" alt="Изображение структуры KeePass"  />
<br>

