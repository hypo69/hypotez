### **Как использовать блок кода для настройки учетных данных бота Google Drive**
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `Creds`, который предназначен для хранения учетных данных, необходимых для работы бота Google Drive. Он включает в себя токен Telegram бота (`TG_TOKEN`), идентификатор папки Team Drive (`TEAMDRIVE_FOLDER_ID`) и идентификатор самого Team Drive (`TEAMDRIVE_ID`). Эти параметры необходимы для аутентификации и определения места для загрузки файлов в Google Drive.

Шаги выполнения
-------------------------
1. **Определение класса `Creds`**:
   - Создается класс `Creds`, который будет использоваться для хранения учетных данных.

2. **Установка токена Telegram бота (`TG_TOKEN`)**:
   - Присвойте значение переменной `TG_TOKEN` токен вашего Telegram бота. Этот токен используется для аутентификации бота в Telegram.

3. **Установка идентификатора папки Team Drive (`TEAMDRIVE_FOLDER_ID`)**:
   - Если вам нужно загружать файлы в определенную папку Team Drive, присвойте значение переменной `TEAMDRIVE_FOLDER_ID` идентификатор этой папки.

4. **Установка идентификатора Team Drive (`TEAMDRIVE_ID`)**:
   - Если вы используете Team Drive, присвойте значение переменной `TEAMDRIVE_ID` идентификатор вашего Team Drive.

Пример использования
-------------------------

```python
from src.endpoints.bots.google_drive.creds import Creds

# Создание экземпляра класса Creds
creds = Creds()

# Установка учетных данных
creds.TG_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
creds.TEAMDRIVE_FOLDER_ID = "YOUR_TEAMDRIVE_FOLDER_ID"
creds.TEAMDRIVE_ID = "YOUR_TEAMDRIVE_ID"

# Теперь вы можете использовать эти учетные данные для работы с Google Drive API
# Например, для загрузки файлов в указанную папку Team Drive
print(f"Токен Telegram бота: {creds.TG_TOKEN}")
print(f"ID папки Team Drive: {creds.TEAMDRIVE_FOLDER_ID}")
print(f"ID Team Drive: {creds.TEAMDRIVE_ID}")