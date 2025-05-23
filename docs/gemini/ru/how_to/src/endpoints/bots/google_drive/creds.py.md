## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода определяет класс `Creds`, который хранит конфигурационные данные для взаимодействия с Google Drive API и Telegram ботом.

Шаги выполнения
-------------------------
1. Определяется класс `Creds`.
2. Переменная `TG_TOKEN` хранит токен Telegram бота.
3. Переменная `TEAMDRIVE_FOLDER_ID` хранит идентификатор папки на Google Drive.
4. Переменная `TEAMDRIVE_ID` хранит идентификатор Team Drive.
5. Приведены примеры значений для конфигурационных переменных.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.bots.google_drive.creds import Creds

# Создание объекта класса Creds
creds = Creds()

# Получение токена Telegram бота
tg_token = creds.TG_TOKEN

# Получение идентификатора Team Drive
teamdrive_id = creds.TEAMDRIVE_ID

# ...
```

**Важно**: Замените значения `TG_TOKEN`, `TEAMDRIVE_FOLDER_ID` и `TEAMDRIVE_ID` на свои реальные значения.