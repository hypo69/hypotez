## \file hypotez/src/endpoints/bots/google_drive/README.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Google Drive Uploader Bot
===============================================================
Этот бот для Telegram позволяет загружать файлы из различных источников на Google Drive.
Поддерживаются ссылки на прямые файлы, Mega.nz, Dropbox, а также различные сервисы, такие как zippyshare, Mediafire, cloud mail, Yandex disk, Sourceforge.

Bот как можно использовать этот бот:

### Как использовать этот бот
------------------------

#### 1. Авторизация
-  Используйте команду `/auth` для авторизации бота. Бот сгенерирует ключ, который нужно отправить.
-  Сохраните этот ключ.

#### 2. Загрузка файлов
-  Отправьте ссылку на файл, который нужно загрузить, боту.

#### 3. Доступные команды:
-  `/start`: запуск бота, приветственное сообщение
-  `/auth`: авторизация
-  `/revoke`: удаление авторизационных данных
-  `/help`: помощь

### Требования
------------------------

-  [Google Drive API Credential](https://console.cloud.google.com/apis/credentials) (тип: "Другие") -  необходимо
-  Telegram Bot Token (полученный через @BotFather) -  необходимо
-  Openload FTP логин и ключ -  необязательно
-  Mega Email и Пароль -  необязательно


### Настройка собственного бота
------------------------

1.  Создайте [Google Drive API Credential](https://console.cloud.google.com/apis/credentials) (тип: "Другие") и скачайте его в формате JSON.
2.  Переместите этот файл в корневую директорию бота и переименуйте в "client_secrets.json".
3.  Замените токен бота в файле [creds.py](./creds.py).
4.  Ваш бот готов к запуску.


### Дополнительные возможности (TODO):
------------------------

-  Переименование файлов при загрузке
-  Поддержка загрузки файлов Telegram (медленная загрузка)
-  Добавление YouTube-dl
-  Исправление поддержки Openload
-  Добавление поддержки zippyshare, Mediafire, cloud mail, Yandex disk, Sourceforge
-  Генератор прямых ссылок на Google Drive
### Лицензия
------------------------

-  GPLv3


### Примечания
------------------------

-  Teamdrive  не для пользователей.  Нужно вносить изменения вручную.
-  Ожидайте версии 2 бота, в ней будет добавлена опция Teamdrive.