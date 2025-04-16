# Бот для загрузки файлов на Google Drive

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

# Google Drive Uploader Bot

`Это был мой первый проект на Python, и вся заслуга в его создании принадлежит` [CyberBoySumanjay](https://github.com/cyberboysumanjay)

### Вдохновлено ботом Sumanjay :D [Google Drive Uploader](https://telegram.dog/driveuploadbot)

Вот Live-версия бота [Gdriveupme_bot](http://telegram.dog/gdriveupme_bot)

# Обновление (30 мая 2020 г.)

*   Добавлена поддержка Teamdrive

`Teamdrive не предназначен для пользователей, вы должны жестко закодировать его,`
`Подождите V2 бота. У этого бота нет активной разработки. Я добавлю опцию Teamdrive для конкретного пользователя`

# Как добавить Teamdrive

*   Замените `TEAMDRIVE_FOLDER_ID` и `TEAMDRIVE_ID` в файле [creds.py](./creds.py)

### Что это такое?

```
   Telegram-бот, написанный на Python
```

### Что он умеет?

```
   Он может загружать ваши прямые и поддерживаемые ссылки в Google Drive.
```

### Установка модуля

```
  sudo pip3 install -r requirements.txt
```

### Запуск этого бота

```
python3 bot.py
```

### Как его использовать

*   Сначала авторизуйте бота с помощью команды `/auth`. Сгенерируйте ключ и отправьте его боту.
*   Теперь вы можете отправить поддерживаемую ссылку боту.

### Доступные команды

*   `/start` = Стартовое сообщение
*   `/auth` = Авторизовать вас
*   `/revoke` = Удалить ваши сохраненные учетные данные
*   `/help` = Текст справки

## Поддерживаемые ссылки:

*   Прямая ссылка
*   Mega.nz Link
*   openload link (больше не доступен)
*   Dropbox Link

## Требования

*   [Google Drive api Credential](https://console.cloud.google.com/apis/credentials) (другой тип) `Обязательно`
*   Telegram Bot Token (Using BotFather) `Обязательно`
*   Openload ftp login and Key `Необязательно`
*   Mega Email and Password `Необязательно`

`Если вы хотите изменить Openload Api и Mega Email Password, вы можете изменить их по указанному пути`

*   Mega => Plugins > TEXT.py
*   Openload => Plugins > dlopenload.py

## Настройка собственного бота

```
1. Создайте свой [Google Drive api Credential](https://console.cloud.google.com/apis/credentials) (другой тип) и загрузите его json

2. Вставьте его в корневой каталог бота и переименуйте в "client_secrets.json"

3. Замените свой токен бота в [файле creds.py](./creds.py)

4. Ваш бот готов к хостингу.
```

### Вы можете использовать Heroku для его размещения.

`Убедитесь, что вы изменили свой токен бота и google client api перед его размещением`

### Моя скрытая благодарность :heart:

*   [CyberBoySumanjay](https://github.com/cyberboysumanjay)
*   [SpEcHiDe](https://github.com/SpEcHiDe)
*   [Atulkadian](https://github.com/atulkadian)

## TODO

*   Переименование файла при загрузке
*   Добавление поддержки файлов Telegram [ медленная загрузка :( ]
*   Добавление Youtube-dl
*   Исправление поддержки openload
*   Добавление zippyshare, Mediafire, cloud mail, Yandex disk, Sourceforge {они уже написаны в PPE plugin, вы можете использовать их оттуда}
*   Генератор прямых ссылок Google Drive

### Лицензия

*   GPLv3