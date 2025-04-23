### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный код демонстрирует базовое использование Google Sheets API для чтения данных из таблицы. Он использует OAuth 2.0 для аутентификации и авторизации, получает учетные данные пользователя, а затем извлекает и печатает значения из указанного диапазона в таблице Google Sheets.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
   - Импортируются библиотеки для работы с файловой системой, авторизацией и Google Sheets API.
   ```python
   from __future__ import print_function
   import os.path
   from pathlib import Path
   from google.auth.transport.requests import Request
   from google.oauth2.credentials import Credentials
   from google_auth_oauthlib.flow import InstalledAppFlow
   from googleapiclient.discovery import build
   from googleapiclient.errors import HttpError
   ```
2. **Определение области доступа (scopes) и идентификаторов таблицы**:
   - Определяются область доступа (чтение данных из Google Sheets) и идентификатор таблицы, из которой нужно извлечь данные.
   ```python
   SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
   SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
   SAMPLE_RANGE_NAME = 'Class Data!A2:E'
   ```
3. **Настройка пути к файлу с учетными данными**:
   - Определяется путь к файлу `client_secret_920776813054-crpf1rcav3uui51kq9q1lis64glkpatj.apps.googleusercontent.com.json`, который содержит учетные данные для доступа к Google API.
   ```python
   ROOT_DIRECTORY = Path.cwd().absolute()
   path = Path(ROOT_DIRECTORY,'google_api','secrets','client_secret_920776813054-crpf1rcav3uui51kq9q1lis64glkpatj.apps.googleusercontent.com.json')
   ```
4. **Функция `main()`**:
   - Функция выполняет основную логику работы с Google Sheets API.
   ```python
   def main():
       # Функция показывает базовое использование Sheets API.
       # Выводит значения из примера таблицы.
       creds = None
       # Файл token.json хранит access и refresh токены пользователя.
       # Он создается автоматически, когда поток авторизации завершается в первый раз.
       if os.path.exists(path):
           creds = Credentials.from_authorized_user_file(path, SCOPES)
       # Если нет доступных (валидных) учетных данных, пользователю предлагается войти в систему.
       if not creds or not creds.valid:
           if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
           else:
               flow = InstalledAppFlow.from_client_secrets_file(
                   'credentials.json', SCOPES)
               creds = flow.run_local_server(port=0)
           # Сохраняем учетные данные для следующего запуска
           with open('token.json', 'w') as token:
               token.write(creds.to_json())
   ```
5. **Авторизация и получение учетных данных**:
   - Проверяется наличие файла `token.json` с сохраненными учетными данными. Если файл существует, учетные данные загружаются из него.
   - Если файл не существует или учетные данные недействительны, выполняется процесс авторизации через `InstalledAppFlow`.
   - Полученные учетные данные сохраняются в файле `token.json` для последующего использования.
6. **Создание сервиса API и выполнение запроса**:
   - Создается экземпляр сервиса Google Sheets API с использованием полученных учетных данных.
   - Выполняется запрос к API для получения значений из указанного диапазона таблицы.
   ```python
   try:
       service = build('sheets', 'v4', credentials=creds)

       # Вызываем Sheets API
       sheet = service.spreadsheets()
       result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range=SAMPLE_RANGE_NAME).execute()
       values = result.get('values', [])

       if not values:
           print('No data found.')
           return

       print('Name, Major:')
       for row in values:
           # Выводим колонки A и E, которые соответствуют индексам 0 и 4.
           print('%s, %s' % (row[0], row[4]))
   except HttpError as err:
       print(err)
   ```
7. **Обработка полученных данных**:
   - Извлекаются значения из полученного результата.
   - Если данные не найдены, выводится сообщение об отсутствии данных.
   - В противном случае, перебираются строки и выводятся значения из указанных колонок (A и E).
8. **Обработка ошибок**:
   - Если во время выполнения запроса к API возникает ошибка, она выводится в консоль.
9. **Запуск функции `main()`**:
   - Если скрипт запускается как основная программа, вызывается функция `main()`.
   ```python
   if __name__ == '__main__':
       main()
   ```

Пример использования
-------------------------

```python
from __future__ import print_function
import os.path
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Области доступа, необходимые для работы с Google Sheets API.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# ID таблицы Google Sheets, из которой нужно получить данные.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'

# Диапазон ячеек, из которого нужно получить данные.
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

# Получение абсолютного пути к текущей рабочей директории.
ROOT_DIRECTORY = Path.cwd().absolute()

# Определение пути к файлу с учетными данными Google API.
path = Path(ROOT_DIRECTORY,'google_api','secrets','client_secret_920776813054-crpf1rcav3uui51kq9q1lis64glkpatj.apps.googleusercontent.com.json')

def main():
    """
    Демонстрирует базовое использование Google Sheets API для чтения данных из таблицы.
    Выводит значения из указанного диапазона ячеек.
    """
    creds = None
    # Файл token.json хранит access и refresh токены пользователя.
    # Он создается автоматически, когда поток авторизации завершается в первый раз.
    if os.path.exists(path):
        creds = Credentials.from_authorized_user_file(path, SCOPES)
    # Если нет доступных (валидных) учетных данных, пользователю предлагается войти в систему.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохраняем учетные данные для следующего запуска
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Создаем экземпляр сервиса Google Sheets API.
        service = build('sheets', 'v4', credentials=creds)

        # Получаем доступ к таблице.
        sheet = service.spreadsheets()

        # Выполняем запрос на получение данных из указанного диапазона.
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()

        # Извлекаем значения из результата.
        values = result.get('values', [])

        # Проверяем, были ли найдены данные.
        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        # Перебираем строки и выводим значения из колонок A и E.
        for row in values:
            # Выводим колонки A и E, которые соответствуют индексам 0 и 4.
            print('%s, %s' % (row[0], row[4]))
    except HttpError as err:
        print(err)

# Запускаем функцию main, если скрипт запущен напрямую.
if __name__ == '__main__':
    main()