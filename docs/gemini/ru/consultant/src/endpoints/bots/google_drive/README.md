### **Анализ кода модуля `README.md`**

---

#### **1. Качество кода**:
   - **Соответствие стандартам**: 5/10
   - **Плюсы**:
     - Предоставлена подробная инструкция по настройке и использованию бота.
     - Указаны необходимые зависимости и команды для запуска.
     - Описаны доступные команды бота и поддерживаемые типы ссылок.
   - **Минусы**:
     - Отсутствует описание структуры кода и классов, что затрудняет понимание работы бота.
     - Многие части документации написаны на английском языке.
     - Не хватает подробностей о том, как реализована поддержка Teamdrive.

#### **2. Рекомендации по улучшению**:
   - Перевести все тексты на русский язык.
   - Добавить описание структуры основных модулей и классов проекта.
   - Предоставить примеры использования бота и настройки Teamdrive.
   - Унифицировать стиль оформления документации.
   - Добавить информацию о обработке ошибок и логировании.
   - Добавить описание взаимодействия с модулем `src.logger`.
   - Скорректировать названия файлов, чтобы соответствовали PEP8.

#### **3. Оптимизированный код**:

```markdown
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

# Google Drive Uploader Bot

Этот бот был моим первым проектом на Python, и вся заслуга принадлежит [CyberBoySumanjay](https://github.com/cyberboysumanjay).

### Вдохновлен ботом Sumanjay :D [Google Drive Uploader](https://telegram.dog/driveuploadbot)

Живая версия бота: [Gdriveupme_bot](http://telegram.dog/gdriveupme_bot)

# Обновление (30 мая 2020)

- Добавлена поддержка Teamdrive

`Teamdrive предназначен не для пользователей. Вам нужно жестко закодировать его.`
`Ожидайте V2 бота. Этот бот не имеет активной разработки. Я добавлю опцию Teamdrive для конкретного пользователя.`

# Как добавить Teamdrive

- Замените `TEAMDRIVE_FOLDER_ID` и `TEAMDRIVE_ID` в [creds.py](./creds.py)

### Что это?

```
Telegram-бот, написанный на Python
```

### Что он может делать?

```
Он может загружать ваши прямые и поддерживаемые ссылки в Google Drive.
```

### Установка модулей

```
sudo pip3 install -r requirements.txt
```

### Запуск бота

```
python3 bot.py
```

### Как это использовать

- Сначала авторизуйте бота с помощью команды `/auth`. Сгенерируйте ключ и отправьте его боту.
- Теперь вы можете отправить поддерживаемую ссылку боту.

### Доступные команды

- `/start` - Стартовое сообщение
- `/auth` - Авторизация
- `/revoke` - Удаление сохраненных учетных данных
- `/help` - Справка

## Поддерживаемые ссылки:

- Прямые ссылки
- Mega.nz ссылки
- Openload ссылки (больше не доступны)
- Dropbox ссылки

## Требования

- [Учетные данные Google Drive API](https://console.cloud.google.com/apis/credentials) (другой тип) `Обязательно`
- Telegram Bot Token (через BotFather) `Обязательно`
- Openload ftp логин и ключ `Опционально`
- Mega Email и пароль `Опционально`

`Если вы хотите изменить Openload Api и Mega Email Password, вы можете изменить это по указанному пути`

- Mega => Plugins > TEXT.py
- Openload => Plugins > dlopenload.py

## Настройка собственного бота

```
1. Создайте свои [учетные данные Google Drive API](https://console.cloud.google.com/apis/credentials) (другой тип) и скачайте его json.

2. Поместите его в корневой каталог бота и переименуйте в "client_secrets.json".

3. Замените свой Bot Token в [файле creds.py](./creds.py)

4. Ваш бот готов к размещению.
```

### Вы можете использовать Heroku для его размещения.

`Убедитесь, что вы изменили свой Bot Token и google client api перед размещением`

### Моя скрытая благодарность: :heart:

- [CyberBoySumanjay](https://github.com/cyberboysumanjay)
- [SpEcHiDe](https://github.com/SpEcHiDe)
- [Atulkadian](https://github.com/atulkadian)

# TODO

- Переименование файла при загрузке
- Добавление поддержки файлов Telegram [медленная загрузка :( ]
- Добавить Youtube-dl
- Исправить поддержку openload
- Добавление zippyshare, Mediafire, cloud mail, Yandex disk, Sourceforge {они уже написаны в PPE plugin, вы можете использовать их оттуда}
- Генератор прямых ссылок Google Drive

### Лицензия

- GPLv3